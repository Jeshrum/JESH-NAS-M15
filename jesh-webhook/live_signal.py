"""
JESH NAS M15 — Live Signal Engine
Runs every 15 minutes on Railway. Fetches real NAS100 data, detects signals,
sends Telegram alerts. No TradingView Pro needed.
"""

import os
import logging
import requests
import pandas as pd
import numpy as np
import pytz
from datetime import datetime, time, timedelta

log = logging.getLogger(__name__)

BOT_TOKEN    = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID      = os.environ["TELEGRAM_CHAT_ID"]
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

NY           = pytz.timezone("America/New_York")
SESSION_START = time(9, 30)
SESSION_END   = time(11, 30)
FORCE_CLOSE   = time(16, 55)
ATR_LEN       = 14
TARGET_R      = 3.0

# ── State (in-memory, resets on redeploy — fine for daily signals) ───────────
_state = {
    "last_signal_date": None,   # date of last signal sent
    "long_sent_today":  False,
    "short_sent_today": False,
    "session_open_sent": False,
    "force_close_sent": False,
}


def send_telegram(text: str):
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    r = requests.post(TELEGRAM_URL, json=payload, timeout=10)
    r.raise_for_status()


def fetch_nas100_15m() -> pd.DataFrame:
    """Fetch last 5 days of NAS100 15m data via Yahoo Finance (QQQ proxy)."""
    import yfinance as yf
    df = yf.download("QQQ", period="5d", interval="15m",
                     auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError("No data from Yahoo Finance")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.columns = [c.lower() for c in df.columns]
    df = df[["open", "high", "low", "close"]].dropna()
    # Convert to NY time
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC").tz_convert(NY)
    else:
        df.index = df.index.tz_convert(NY)
    df.sort_index(inplace=True)
    return df


def compute_atr(df: pd.DataFrame, length: int = ATR_LEN) -> pd.Series:
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low  - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(span=length, adjust=False).mean()


def check_signals():
    """Core logic — called every 15 minutes by the scheduler."""
    now_ny = datetime.now(NY)
    today  = now_ny.date()
    t      = now_ny.time()

    # Reset daily state at midnight
    if _state["last_signal_date"] != today:
        _state["last_signal_date"]  = today
        _state["long_sent_today"]   = False
        _state["short_sent_today"]  = False
        _state["session_open_sent"] = False
        _state["force_close_sent"]  = False
        log.info("New day — state reset for %s", today)

    # Skip weekends
    if now_ny.weekday() >= 5:
        log.info("Weekend — skipping")
        return

    # ── Session open ping ────────────────────────────────────────────────────
    if (SESSION_START <= t < time(9, 46) and
            not _state["session_open_sent"]):
        send_telegram(
            "🔔 <b>JESH Session Open — 9:30 AM NY</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Opening Range is now being set.\n"
            "Watch for breakout signal until 11:30 AM NY.\n"
            "⏰ Lagos: 2:30 PM WAT (summer) · 3:30 PM WAT (winter)"
        )
        _state["session_open_sent"] = True
        log.info("Session open alert sent")
        return

    # ── Force close ping ─────────────────────────────────────────────────────
    if (FORCE_CLOSE <= t < time(17, 10) and
            not _state["force_close_sent"]):
        send_telegram(
            "⚠️ <b>JESH Force Close — 4:55 PM NY</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Close any open NAS100 position NOW.\n"
            "No overnight positions allowed.\n"
            "⏰ Lagos: 10:55 PM WAT"
        )
        _state["force_close_sent"] = True
        log.info("Force close alert sent")
        return

    # ── Only run signal logic during session ─────────────────────────────────
    if not (SESSION_START <= t < SESSION_END):
        log.info("Outside session window (%s NY) — skipping signal check", t.strftime("%H:%M"))
        return

    if _state["long_sent_today"] and _state["short_sent_today"]:
        log.info("Both signals already sent today — skipping")
        return

    # ── Fetch data ───────────────────────────────────────────────────────────
    try:
        df = fetch_nas100_15m()
    except Exception as e:
        log.error("Data fetch failed: %s", e)
        return

    df["atr"] = compute_atr(df)

    # ── Identify today's bars ────────────────────────────────────────────────
    today_bars = df[df.index.date == today]
    if today_bars.empty:
        log.info("No bars for today yet")
        return

    # ── Previous day high / low ──────────────────────────────────────────────
    yesterday = today - timedelta(days=1)
    # Walk back to find the last trading day
    for i in range(1, 6):
        prev_day = today - timedelta(days=i)
        prev_bars = df[df.index.date == prev_day]
        if not prev_bars.empty:
            pdh = prev_bars["high"].max()
            pdl = prev_bars["low"].min()
            break
    else:
        log.info("Could not find previous trading day")
        return

    # ── First bar of session (9:30 candle) ───────────────────────────────────
    session_bars = today_bars[
        (today_bars.index.time >= SESSION_START) &
        (today_bars.index.time < SESSION_END)
    ]
    if session_bars.empty:
        log.info("No session bars yet")
        return

    first_bar  = session_bars.iloc[0]
    fb_high    = first_bar["high"]
    fb_low     = first_bar["low"]

    # Need at least 2 bars to detect a crossover
    if len(session_bars) < 2:
        log.info("Only first bar so far — waiting for crossover")
        return

    # ── Signal detection ─────────────────────────────────────────────────────
    prev_close = session_bars["close"].iloc[-2]
    curr_close = session_bars["close"].iloc[-1]
    curr_bar   = session_bars.iloc[-1]
    atr        = curr_bar["atr"]

    if np.isnan(atr) or atr <= 0:
        log.info("ATR not ready")
        return

    # LONG: close crosses above first bar high, PDH > FB high
    long_cross = prev_close <= fb_high and curr_close > fb_high
    long_valid = long_cross and pdh > fb_high

    # SHORT: close crosses below first bar low, PDL < FB low
    short_cross = prev_close >= fb_low and curr_close < fb_low
    short_valid = short_cross and pdl < fb_low

    # ── Send LONG signal ─────────────────────────────────────────────────────
    if long_valid and not _state["long_sent_today"]:
        entry = round(fb_high, 2)
        sl    = round(fb_low, 2)
        dist  = entry - sl
        tp1   = round(entry + dist * 1.0, 2)
        tp2   = round(entry + dist * 2.0, 2)
        tp3   = round(entry + dist * TARGET_R, 2)
        risk  = int(os.environ.get("RISK_DOLLAR", "100"))
        qty   = max(1, round(risk / dist)) if dist > 0 else 1

        send_telegram(
            "🟢 <b>JESH LONG SIGNAL · NAS100</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>Limit Entry</b>  <code>{entry}</code>\n"
            f"🛑 <b>Stop Loss</b>    <code>{sl}</code>\n"
            f"🎯 <b>1R Target</b>    <code>{tp1}</code>\n"
            f"🎯 <b>2R Target</b>    <code>{tp2}</code>\n"
            f"🎯 <b>3R TP</b>        <code>{tp3}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 Risk: <b>${risk}</b>  |  Qty: <b>{qty}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⏰ Lagos: 2:30–4:30 PM WAT (summer) · 3:30–5:30 PM (winter)\n"
            "📋 Place LIMIT order · Set SL &amp; TP · Walk away"
        )
        _state["long_sent_today"] = True
        log.info("LONG signal sent — entry: %s sl: %s tp3: %s", entry, sl, tp3)

    # ── Send SHORT signal ────────────────────────────────────────────────────
    elif short_valid and not _state["short_sent_today"]:
        entry = round(fb_low, 2)
        sl    = round(fb_high, 2)
        dist  = sl - entry
        tp1   = round(entry - dist * 1.0, 2)
        tp2   = round(entry - dist * 2.0, 2)
        tp3   = round(entry - dist * TARGET_R, 2)
        risk  = int(os.environ.get("RISK_DOLLAR", "100"))
        qty   = max(1, round(risk / dist)) if dist > 0 else 1

        send_telegram(
            "🔴 <b>JESH SHORT SIGNAL · NAS100</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>Limit Entry</b>  <code>{entry}</code>\n"
            f"🛑 <b>Stop Loss</b>    <code>{sl}</code>\n"
            f"🎯 <b>1R Target</b>    <code>{tp1}</code>\n"
            f"🎯 <b>2R Target</b>    <code>{tp2}</code>\n"
            f"🎯 <b>3R TP</b>        <code>{tp3}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 Risk: <b>${risk}</b>  |  Qty: <b>{qty}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⏰ Lagos: 2:30–4:30 PM WAT (summer) · 3:30–5:30 PM (winter)\n"
            "📋 Place LIMIT order · Set SL &amp; TP · Walk away"
        )
        _state["short_sent_today"] = True
        log.info("SHORT signal sent — entry: %s sl: %s tp3: %s", entry, sl, tp3)

    else:
        log.info("No signal this bar — long_valid=%s short_valid=%s", long_valid, short_valid)
