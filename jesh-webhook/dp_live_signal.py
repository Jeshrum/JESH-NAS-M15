"""
DOCTOR PRAISE XAUUSD — Live Signal Engine
Runs every 15 minutes inside the JESH NAS Railway server.
Fetches XAUUSD data via Yahoo Finance (GC=F), detects London Close ORB signals,
sends Telegram alerts. No TradingView Pro needed.

Strategy rules:
  ORB window  : 10:00–11:00 AM NY (4 × M15 candles)
  Breakout    : M15 close crosses above ORB high (LONG) or below ORB low (SHORT)
  Entry       : Limit at ORB high (long) / ORB low (short)
  Stop Loss   : Other side of range
  Take Profit : 1.5R
  Force close : 1:00 PM NY
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

NY            = pytz.timezone("America/New_York")
ORB_START     = time(10, 0)
ORB_END       = time(11, 0)
TRADE_START   = time(11, 0)
TRADE_END     = time(13, 0)
FORCE_CLOSE   = time(13, 0)
TARGET_R      = 1.5
ACCOUNT_SIZE  = int(os.environ.get("DP_ACCOUNT_SIZE", "10000"))
RISK_PCT      = float(os.environ.get("DP_RISK_PCT", "0.015"))  # 1.5%

# ── In-memory state (resets on redeploy — fine for daily signals) ─────────────
_dp_state = {
    "last_date":         None,
    "orb_high":          None,
    "orb_low":           None,
    "orb_done":          False,
    "long_sent":         False,
    "short_sent":        False,
    "orb_start_sent":    False,
    "force_close_sent":  False,
}


def _send(text: str):
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    r = requests.post(TELEGRAM_URL, json=payload, timeout=10)
    r.raise_for_status()


def _fetch_xauusd_15m() -> pd.DataFrame:
    import yfinance as yf
    df = yf.download("GC=F", period="5d", interval="15m",
                     auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError("No XAUUSD data from Yahoo Finance")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.columns = [c.lower() for c in df.columns]
    df = df[["open", "high", "low", "close"]].dropna()
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC").tz_convert(NY)
    else:
        df.index = df.index.tz_convert(NY)
    df.sort_index(inplace=True)
    return df


def _lot_size(risk_dollar: float, dist: float) -> float:
    """Convert dollar risk and point distance to Gold lots (1 lot = 100 oz)."""
    if dist <= 0:
        return 0.01
    # 1 lot Gold = $100 per $1 move → lot = risk / (dist * 100)
    lot = risk_dollar / (dist * 100)
    return max(0.01, round(lot * 100) / 100)


def _lagos_time(ny_t: str, is_summer: bool) -> str:
    """Convert a NY time string like '10:00 AM' to Lagos WAT."""
    offset = 4 if is_summer else 5  # Lagos = NY + 5 (summer DST) or +6 (winter)
    # Just return the label — no need for exact math here
    return f"{'Summer: ' if is_summer else 'Winter: '}{ny_t} + {offset}h WAT"


def dp_check_signals():
    """Core logic — called every 15 minutes by the scheduler."""
    now_ny = datetime.now(NY)
    today  = now_ny.date()
    t      = now_ny.time()

    # Reset state at start of each new day
    if _dp_state["last_date"] != today:
        _dp_state["last_date"]        = today
        _dp_state["orb_high"]         = None
        _dp_state["orb_low"]          = None
        _dp_state["orb_done"]         = False
        _dp_state["long_sent"]        = False
        _dp_state["short_sent"]       = False
        _dp_state["orb_start_sent"]   = False
        _dp_state["force_close_sent"] = False
        log.info("[DP] New day — state reset for %s", today)

    # Skip weekends
    if now_ny.weekday() >= 5:
        log.info("[DP] Weekend — skipping")
        return

    # Determine summer/winter (US DST: roughly Mar–Nov)
    is_summer = bool(now_ny.dst())

    lagos_orb   = "3:00–4:00 PM WAT" if is_summer else "4:00–5:00 PM WAT"
    lagos_trade = "4:00–6:00 PM WAT" if is_summer else "5:00–7:00 PM WAT"
    lagos_fc    = "6:00 PM WAT"      if is_summer else "7:00 PM WAT"

    # ── ORB start ping (at 10:00 AM NY) ──────────────────────────────────────
    if (ORB_START <= t < time(10, 16) and
            not _dp_state["orb_start_sent"]):
        _send(
            "🔔 <b>DOCTOR PRAISE — ORB Starting</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Gold range is now building.\n"
            "4 × M15 candles (10:00–11:00 AM NY).\n"
            "Watch for breakout signal from 11:00 AM NY.\n"
            f"⏰ Lagos: {lagos_orb}"
        )
        _dp_state["orb_start_sent"] = True
        log.info("[DP] ORB start alert sent")

    # ── Force close ping (at 1:00 PM NY) ─────────────────────────────────────
    if (FORCE_CLOSE <= t < time(13, 16) and
            not _dp_state["force_close_sent"]):
        _send(
            "⚠️ <b>DOCTOR PRAISE — Force Close 1:00 PM NY</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Close any open XAUUSD position NOW.\n"
            "Cancel any unfilled limit orders.\n"
            "No holding past session end.\n"
            f"⏰ Lagos: {lagos_fc}"
        )
        _dp_state["force_close_sent"] = True
        log.info("[DP] Force close alert sent")
        return

    # ── Outside ORB or trade window — nothing to do ───────────────────────────
    if not (ORB_START <= t < TRADE_END):
        log.info("[DP] Outside active window (%s NY) — skipping", t.strftime("%H:%M"))
        return

    # ── Fetch data ────────────────────────────────────────────────────────────
    try:
        df = _fetch_xauusd_15m()
    except Exception as e:
        log.error("[DP] Data fetch failed: %s", e)
        return

    today_bars = df[df.index.date == today]
    if today_bars.empty:
        log.info("[DP] No bars for today yet")
        return

    # ── Build ORB from 10:00–10:45 AM bars ───────────────────────────────────
    orb_bars = today_bars[
        (today_bars.index.time >= ORB_START) &
        (today_bars.index.time < ORB_END)
    ]
    if orb_bars.empty:
        log.info("[DP] No ORB bars yet")
        return

    _dp_state["orb_high"] = float(orb_bars["high"].max())
    _dp_state["orb_low"]  = float(orb_bars["low"].min())

    # ORB is done once we're past 11:00 AM and have at least 1 candle there
    trade_bars = today_bars[today_bars.index.time >= TRADE_START]
    if trade_bars.empty:
        log.info("[DP] ORB built — waiting for trade window (11:00 AM NY)")
        return

    _dp_state["orb_done"] = True
    orb_h = _dp_state["orb_high"]
    orb_l = _dp_state["orb_low"]

    if _dp_state["long_sent"] and _dp_state["short_sent"]:
        log.info("[DP] Both signals already sent today")
        return

    # Need at least 2 trade-window bars for crossover detection
    if len(trade_bars) < 2:
        prev_close = orb_bars["close"].iloc[-1]   # last ORB bar
        curr_close = trade_bars["close"].iloc[-1]
    else:
        prev_close = trade_bars["close"].iloc[-2]
        curr_close = trade_bars["close"].iloc[-1]

    risk_dollar = ACCOUNT_SIZE * RISK_PCT
    dist        = orb_h - orb_l

    # ── LONG signal ───────────────────────────────────────────────────────────
    long_cross = prev_close <= orb_h and curr_close > orb_h
    if long_cross and not _dp_state["long_sent"]:
        entry = round(orb_h, 2)
        sl    = round(orb_l, 2)
        tp    = round(entry + TARGET_R * dist, 2)
        lot   = _lot_size(risk_dollar, dist)

        _send(
            "🟢 <b>DOCTOR PRAISE LONG · XAUUSD</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>Limit Entry</b>  <code>{entry}</code>\n"
            f"🛑 <b>Stop Loss</b>    <code>{sl}</code>\n"
            f"🎯 <b>1.5R Target</b>  <code>{tp}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 Risk: <b>${int(risk_dollar)}</b>  |  Lot: <b>{lot}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"⏰ Lagos: {lagos_trade}\n"
            "📋 Place LIMIT order · Set SL &amp; TP · Walk away"
        )
        _dp_state["long_sent"] = True
        log.info("[DP] LONG signal sent — entry: %s sl: %s tp: %s", entry, sl, tp)

    # ── SHORT signal ──────────────────────────────────────────────────────────
    short_cross = prev_close >= orb_l and curr_close < orb_l
    if short_cross and not _dp_state["short_sent"]:
        entry = round(orb_l, 2)
        sl    = round(orb_h, 2)
        tp    = round(entry - TARGET_R * dist, 2)
        lot   = _lot_size(risk_dollar, dist)

        _send(
            "🔴 <b>DOCTOR PRAISE SHORT · XAUUSD</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>Limit Entry</b>  <code>{entry}</code>\n"
            f"🛑 <b>Stop Loss</b>    <code>{sl}</code>\n"
            f"🎯 <b>1.5R Target</b>  <code>{tp}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 Risk: <b>${int(risk_dollar)}</b>  |  Lot: <b>{lot}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"⏰ Lagos: {lagos_trade}\n"
            "📋 Place LIMIT order · Set SL &amp; TP · Walk away"
        )
        _dp_state["short_sent"] = True
        log.info("[DP] SHORT signal sent — entry: %s sl: %s tp: %s", entry, sl, tp)

    if not long_cross and not short_cross:
        log.info("[DP] No signal this bar — orb_h: %s orb_l: %s close: %s",
                 orb_h, orb_l, curr_close)
