# =============================================================================
# JESH NAS M15 — Strategy Engine
# =============================================================================
# Converts the Pine Script logic into Python bar-by-bar simulation.
#
# Core Logic:
#   - First 15min candle of NY session (9:30 AM) = Opening Range
#   - Long  signal: close crosses ABOVE first bar HIGH (if PDL swept today)
#   - Short signal: close crosses BELOW first bar LOW  (if PDH swept today)
#   - SL   = opposite end of opening range
#   - TP   = prev day high/low (adjusted by ATR * tp_atr_reduction)
#   - Entry via limit order (adjusted by ATR * limit_atr_improvement)
#   - One trade per day maximum
#   - Force close before session end
# =============================================================================

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Optional
import pytz
from config import (
    SESSION_START, SESSION_END, FORCE_CLOSE_TIME, TIMEZONE,
    ATR_LENGTH, LIMIT_ATR_IMPROVEMENT, TP_ATR_REDUCTION,
    INITIAL_CAPITAL, COMMISSION_PER_SIDE, RISK_MODES, RISK_MODE
)


# ─── Trade Record ─────────────────────────────────────────────────────────────
@dataclass
class Trade:
    entry_date:     pd.Timestamp
    direction:      str             # "long" or "short"
    entry_price:    float
    sl_price:       float
    tp_price:       float
    qty:            float
    exit_date:      Optional[pd.Timestamp] = None
    exit_price:     Optional[float]        = None
    exit_reason:    Optional[str]          = None   # "tp" | "sl" | "force_close"
    pnl:            float                  = 0.0
    pnl_pct:        float                  = 0.0
    risk_amount:    float                  = 0.0


# ─── ATR Calculation ──────────────────────────────────────────────────────────
def compute_atr(df: pd.DataFrame, length: int = ATR_LENGTH) -> pd.Series:
    high  = df["high"]
    low   = df["low"]
    close = df["close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low  - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(span=length, adjust=False).mean()


# ─── Main Strategy ────────────────────────────────────────────────────────────
def run_strategy(df: pd.DataFrame) -> dict:
    """
    Run the JESH NAS M15 strategy bar-by-bar on the provided OHLCV DataFrame.
    DataFrame index must be timezone-aware (America/New_York preferred).
    Returns a results dict with trade log, equity curve, and summary stats.
    """

    # ── Localize timestamps to NY time ──────────────────────────────────────
    tz = pytz.timezone(TIMEZONE)
    if df.index.tz is None:
        df = df.copy()
        df.index = df.index.tz_localize("UTC").tz_convert(tz)
    else:
        df = df.copy()
        df.index = df.index.tz_convert(tz)

    # ── Pre-compute ATR ─────────────────────────────────────────────────────
    df["atr"] = compute_atr(df, ATR_LENGTH)

    # ── Risk settings ───────────────────────────────────────────────────────
    risk_pct    = RISK_MODES[RISK_MODE]
    balance     = INITIAL_CAPITAL

    # ── Parse session times ─────────────────────────────────────────────────
    sess_start_h, sess_start_m = map(int, SESSION_START.split(":"))
    sess_end_h,   sess_end_m   = map(int, SESSION_END.split(":"))
    force_h,      force_m      = map(int, FORCE_CLOSE_TIME.split(":"))

    # ── State variables ─────────────────────────────────────────────────────
    trades:         list[Trade]  = []
    equity_curve:   list[dict]   = []

    current_date        = None
    first_bar_high      = None
    first_bar_low       = None
    prev_day_high       = None
    prev_day_low        = None
    day_high_tracker    = []
    day_low_tracker     = []
    pdh_swept_today     = False
    pdl_swept_today     = False
    pdh_swept_confirmed = False
    pdl_swept_confirmed = False
    trade_taken_today   = False
    active_trade: Optional[Trade] = None

    # Track previous day OHLC
    prev_day_bars: list = []
    current_day_bars: list = []

    prev_close = None   # for crossover detection

    # ── Bar-by-bar loop ──────────────────────────────────────────────────────
    for i, (ts, row) in enumerate(df.iterrows()):

        bar_date  = ts.date()
        bar_hour  = ts.hour
        bar_min   = ts.minute
        o, h, l, c = row["open"], row["high"], row["low"], row["close"]
        atr = row["atr"]

        # ── New day detected ────────────────────────────────────────────────
        if bar_date != current_date:
            # Roll previous day stats
            if current_day_bars:
                prev_day_bars   = current_day_bars.copy()
                if prev_day_bars:
                    prev_day_high = max(b["high"] for b in prev_day_bars)
                    prev_day_low  = min(b["low"]  for b in prev_day_bars)

            current_day_bars    = []
            current_date        = bar_date
            first_bar_high      = None
            first_bar_low       = None
            pdh_swept_today     = False
            pdl_swept_today     = False
            pdh_swept_confirmed = False
            pdl_swept_confirmed = False
            trade_taken_today   = False
            prev_close          = None

        # Track current day bars
        current_day_bars.append({"high": h, "low": l, "close": c, "ts": ts})

        # ── Capture first bar of NY session (9:30 AM) ───────────────────────
        in_session = (
            (bar_hour * 60 + bar_min) >= (sess_start_h * 60 + sess_start_m) and
            (bar_hour * 60 + bar_min) <  (sess_end_h   * 60 + sess_end_m)
        )

        is_first_bar = (
            bar_hour == sess_start_h and
            bar_min  == sess_start_m and
            first_bar_high is None
        )

        if is_first_bar:
            first_bar_high = h
            first_bar_low  = l

        # ── Sweep detection (confirmed on NEXT bar) ──────────────────────────
        if prev_day_high is not None and not pdh_swept_today:
            if h > prev_day_high:
                pdh_swept_today = True

        if prev_day_low is not None and not pdl_swept_today:
            if l < prev_day_low:
                pdl_swept_today = True

        # Confirm sweep on the bar AFTER it occurred
        if i > 0:
            if pdh_swept_today and not pdh_swept_confirmed:
                # Check if sweep happened on previous bar
                if len(current_day_bars) >= 2:
                    pdh_swept_confirmed = True

            if pdl_swept_today and not pdl_swept_confirmed:
                if len(current_day_bars) >= 2:
                    pdl_swept_confirmed = True

        # ── Force close check ────────────────────────────────────────────────
        past_force_close = (bar_hour * 60 + bar_min) >= (force_h * 60 + force_m)

        if active_trade is not None and past_force_close:
            active_trade.exit_date   = ts
            active_trade.exit_price  = o  # exit at open of force-close bar
            active_trade.exit_reason = "force_close"
            if active_trade.direction == "long":
                raw_pnl = (active_trade.exit_price - active_trade.entry_price) * active_trade.qty
            else:
                raw_pnl = (active_trade.entry_price - active_trade.exit_price) * active_trade.qty
            commission = COMMISSION_PER_SIDE * active_trade.qty * 2
            active_trade.pnl     = raw_pnl - commission
            active_trade.pnl_pct = active_trade.pnl / balance * 100
            balance += active_trade.pnl
            trades.append(active_trade)
            active_trade = None

        # ── Manage active trade SL/TP ────────────────────────────────────────
        if active_trade is not None:
            hit_tp = False
            hit_sl = False

            if active_trade.direction == "long":
                if h >= active_trade.tp_price:
                    hit_tp = True
                    exit_p = active_trade.tp_price
                elif l <= active_trade.sl_price:
                    hit_sl = True
                    exit_p = active_trade.sl_price
            else:
                if l <= active_trade.tp_price:
                    hit_tp = True
                    exit_p = active_trade.tp_price
                elif h >= active_trade.sl_price:
                    hit_sl = True
                    exit_p = active_trade.sl_price

            if hit_tp or hit_sl:
                active_trade.exit_date   = ts
                active_trade.exit_price  = exit_p
                active_trade.exit_reason = "tp" if hit_tp else "sl"
                if active_trade.direction == "long":
                    raw_pnl = (exit_p - active_trade.entry_price) * active_trade.qty
                else:
                    raw_pnl = (active_trade.entry_price - exit_p) * active_trade.qty
                commission = COMMISSION_PER_SIDE * active_trade.qty * 2
                active_trade.pnl     = raw_pnl - commission
                active_trade.pnl_pct = active_trade.pnl / balance * 100
                balance += active_trade.pnl
                trades.append(active_trade)
                active_trade = None

        # ── Entry conditions ─────────────────────────────────────────────────
        can_enter = (
            in_session and
            not trade_taken_today and
            active_trade is None and
            not past_force_close and
            first_bar_high is not None and
            first_bar_low  is not None and
            prev_day_high  is not None and
            prev_day_low   is not None and
            prev_close     is not None and
            not np.isnan(atr) and atr > 0
        )

        if can_enter:
            # Long: close crosses above first bar high, PDH > first bar high, PDL swept
            long_cross  = prev_close <= first_bar_high and c > first_bar_high
            long_valid  = (
                long_cross and
                prev_day_high > first_bar_high and
                pdl_swept_confirmed
            )

            # Short: close crosses below first bar low, PDL < first bar low, PDH swept
            short_cross = prev_close >= first_bar_low and c < first_bar_low
            short_valid = (
                short_cross and
                prev_day_low < first_bar_low and
                pdh_swept_confirmed
            )

            if long_valid:
                entry_price = first_bar_high - (atr * LIMIT_ATR_IMPROVEMENT)
                sl_price    = first_bar_low
                tp_price    = prev_day_high - (atr * TP_ATR_REDUCTION)

                sl_dist     = entry_price - sl_price
                if sl_dist > 0 and tp_price > entry_price:
                    risk_amount = balance * risk_pct
                    qty         = max(1, round(risk_amount / sl_dist))
                    commission  = COMMISSION_PER_SIDE * qty * 2

                    active_trade = Trade(
                        entry_date   = ts,
                        direction    = "long",
                        entry_price  = entry_price,
                        sl_price     = sl_price,
                        tp_price     = tp_price,
                        qty          = qty,
                        risk_amount  = risk_amount,
                    )
                    balance     -= commission  # deduct commission on entry
                    trade_taken_today = True

            elif short_valid:
                entry_price = first_bar_low - (atr * LIMIT_ATR_IMPROVEMENT)
                sl_price    = first_bar_high
                tp_price    = prev_day_low + (atr * TP_ATR_REDUCTION)

                sl_dist     = sl_price - entry_price
                if sl_dist > 0 and tp_price < entry_price:
                    risk_amount = balance * risk_pct
                    qty         = max(1, round(risk_amount / sl_dist))
                    commission  = COMMISSION_PER_SIDE * qty * 2

                    active_trade = Trade(
                        entry_date   = ts,
                        direction    = "short",
                        entry_price  = entry_price,
                        sl_price     = sl_price,
                        tp_price     = tp_price,
                        qty          = qty,
                        risk_amount  = risk_amount,
                    )
                    balance     -= commission
                    trade_taken_today = True

        # ── Track equity curve ───────────────────────────────────────────────
        unrealized = 0.0
        if active_trade is not None:
            if active_trade.direction == "long":
                unrealized = (c - active_trade.entry_price) * active_trade.qty
            else:
                unrealized = (active_trade.entry_price - c) * active_trade.qty

        equity_curve.append({
            "datetime": ts,
            "balance":  balance,
            "equity":   balance + unrealized,
        })

        prev_close = c

    # ── Force close any open trade at end of data ────────────────────────────
    if active_trade is not None:
        last_close = df["close"].iloc[-1]
        active_trade.exit_date   = df.index[-1]
        active_trade.exit_price  = last_close
        active_trade.exit_reason = "force_close"
        if active_trade.direction == "long":
            raw_pnl = (last_close - active_trade.entry_price) * active_trade.qty
        else:
            raw_pnl = (active_trade.entry_price - last_close) * active_trade.qty
        commission = COMMISSION_PER_SIDE * active_trade.qty * 2
        active_trade.pnl     = raw_pnl - commission
        active_trade.pnl_pct = active_trade.pnl / balance * 100
        balance += active_trade.pnl
        trades.append(active_trade)

    return {
        "trades":       trades,
        "equity_curve": pd.DataFrame(equity_curve).set_index("datetime"),
        "final_balance": balance,
    }
