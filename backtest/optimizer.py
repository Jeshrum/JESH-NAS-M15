# =============================================================================
# JESH NAS M15 — Strategy Optimizer
# =============================================================================
# Run: python3 optimizer.py
# Tests all strategy combos on 16 years of NAS100 M15 data.
# Prints ranked results table. Takes ~2 min to run.
# =============================================================================

import os
import itertools
import pandas as pd
import numpy as np
import pytz
from dataclasses import dataclass
from typing import Optional

DATA_FILE       = "NAS100_15m.csv"
INITIAL_CAPITAL = 10_000
COMMISSION      = 0.50   # per side per contract
RISK_PCT        = 0.01   # 1% risk per trade (fixed for fair comparison)
TIMEZONE        = "America/New_York"

# ─── Parameter Grid ───────────────────────────────────────────────────────────
GRID = {
    "session_end":    ["11:30", "16:00"],           # stop new entries at
    "force_close":    ["16:55"],                     # force close time
    "entry_type":     ["market", "limit"],           # market = crossover price, limit = FB level
    "tp_type":        ["pdh_pdl", "1R", "2R", "3R"],# TP method
    "sweep_filter":   [True, False],                 # require PDH/PDL sweep
    "atr_adjust":     [0.0],                         # ATR adjustment (0 = off, clean levels)
}


@dataclass
class Trade:
    entry_date:  pd.Timestamp
    direction:   str
    entry_price: float
    sl_price:    float
    tp_price:    float
    qty:         float
    exit_date:   Optional[pd.Timestamp] = None
    exit_price:  Optional[float]        = None
    exit_reason: Optional[str]          = None
    pnl:         float                  = 0.0


def compute_atr(df, length=14):
    h, l, c = df["high"], df["low"], df["close"]
    tr = pd.concat([(h-l), (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(span=length, adjust=False).mean()


def run_combo(df, session_end, force_close, entry_type, tp_type, sweep_filter, atr_adjust):
    tz = pytz.timezone(TIMEZONE)
    if df.index.tz is None:
        df = df.copy(); df.index = df.index.tz_localize("UTC").tz_convert(tz)
    else:
        df = df.copy(); df.index = df.index.tz_convert(tz)

    df["atr"] = compute_atr(df)

    sess_start_min = 9 * 60 + 30
    sess_end_min   = int(session_end.split(":")[0]) * 60 + int(session_end.split(":")[1])
    force_min      = int(force_close.split(":")[0]) * 60 + int(force_close.split(":")[1])

    balance       = float(INITIAL_CAPITAL)
    trades        = []
    equity        = []

    current_date        = None
    first_bar_high      = None
    first_bar_low       = None
    prev_day_high       = None
    prev_day_low        = None
    pdh_swept           = False
    pdl_swept           = False
    pdh_confirmed       = False
    pdl_confirmed       = False
    trade_taken         = False
    active              = None
    current_day_bars    = []
    prev_close          = None

    for ts, row in df.iterrows():
        d    = ts.date()
        bmin = ts.hour * 60 + ts.minute
        o, h, l, c = row["open"], row["high"], row["low"], row["close"]
        atr  = row["atr"]

        # New day
        if d != current_date:
            if current_day_bars:
                prev_day_high = max(b["h"] for b in current_day_bars)
                prev_day_low  = min(b["l"] for b in current_day_bars)
            current_day_bars = []
            current_date     = d
            first_bar_high   = None
            first_bar_low    = None
            pdh_swept        = False
            pdl_swept        = False
            pdh_confirmed    = False
            pdl_confirmed    = False
            trade_taken      = False
            prev_close       = None

        current_day_bars.append({"h": h, "l": l})

        in_session   = sess_start_min <= bmin < sess_end_min
        past_force   = bmin >= force_min

        # First bar
        if bmin == sess_start_min and first_bar_high is None:
            first_bar_high = h
            first_bar_low  = l

        # Sweep detection
        if prev_day_high and not pdh_swept and h > prev_day_high:
            pdh_swept = True
        if prev_day_low and not pdl_swept and l < prev_day_low:
            pdl_swept = True
        if pdh_swept and not pdh_confirmed and len(current_day_bars) >= 2:
            pdh_confirmed = True
        if pdl_swept and not pdl_confirmed and len(current_day_bars) >= 2:
            pdl_confirmed = True

        # Force close
        if active and past_force:
            ep = o
            raw = (ep - active.entry_price) * active.qty if active.direction == "long" \
                  else (active.entry_price - ep) * active.qty
            active.exit_date = ts; active.exit_price = ep; active.exit_reason = "force_close"
            active.pnl = raw - COMMISSION * active.qty * 2
            balance += active.pnl
            trades.append(active); active = None

        # Manage active trade
        if active:
            hit_tp = hit_sl = False
            if active.direction == "long":
                if h >= active.tp_price: hit_tp = True; ep = active.tp_price
                elif l <= active.sl_price: hit_sl = True; ep = active.sl_price
            else:
                if l <= active.tp_price: hit_tp = True; ep = active.tp_price
                elif h >= active.sl_price: hit_sl = True; ep = active.sl_price
            if hit_tp or hit_sl:
                raw = (ep - active.entry_price) * active.qty if active.direction == "long" \
                      else (active.entry_price - ep) * active.qty
                active.exit_date = ts; active.exit_price = ep
                active.exit_reason = "tp" if hit_tp else "sl"
                active.pnl = raw - COMMISSION * active.qty * 2
                balance += active.pnl
                trades.append(active); active = None

        # Entry conditions
        can_enter = (
            in_session and not trade_taken and active is None and
            not past_force and first_bar_high and first_bar_low and
            prev_day_high and prev_day_low and prev_close and
            not np.isnan(atr) and atr > 0
        )

        if can_enter:
            long_cross  = prev_close <= first_bar_high and c > first_bar_high
            short_cross = prev_close >= first_bar_low  and c < first_bar_low

            long_ok  = long_cross  and prev_day_high > first_bar_high
            short_ok = short_cross and prev_day_low  < first_bar_low

            if sweep_filter:
                long_ok  = long_ok  and pdl_confirmed
                short_ok = short_ok and pdh_confirmed

            def calc_tp(direction, entry, sl):
                if tp_type == "pdh_pdl":
                    return prev_day_high if direction == "long" else prev_day_low
                risk = abs(entry - sl)
                mult = {"1R": 1.0, "2R": 2.0, "3R": 3.0}[tp_type]
                return entry + risk * mult if direction == "long" else entry - risk * mult

            if long_ok:
                entry = first_bar_high if entry_type == "limit" else c
                sl    = first_bar_low
                tp    = calc_tp("long", entry, sl)
                dist  = entry - sl
                if dist > 0 and tp > entry:
                    risk_amt = INITIAL_CAPITAL * RISK_PCT
                    qty = max(1, round(risk_amt / dist))
                    balance -= COMMISSION * qty * 2
                    active = Trade(ts, "long", entry, sl, tp, qty)
                    trade_taken = True

            elif short_ok:
                entry = first_bar_low if entry_type == "limit" else c
                sl    = first_bar_high
                tp    = calc_tp("short", entry, sl)
                dist  = sl - entry
                if dist > 0 and tp < entry:
                    risk_amt = INITIAL_CAPITAL * RISK_PCT
                    qty = max(1, round(risk_amt / dist))
                    balance -= COMMISSION * qty * 2
                    active = Trade(ts, "short", entry, sl, tp, qty)
                    trade_taken = True

        equity.append({"datetime": ts, "equity": balance})
        prev_close = c

    if active:
        ep = df["close"].iloc[-1]
        raw = (ep - active.entry_price) * active.qty if active.direction == "long" \
              else (active.entry_price - ep) * active.qty
        active.pnl = raw - COMMISSION * active.qty * 2
        balance += active.pnl
        trades.append(active)

    if not trades:
        return None

    wins   = [t for t in trades if t.pnl > 0]
    losses = [t for t in trades if t.pnl <= 0]
    wr     = len(wins) / len(trades) * 100
    gp     = sum(t.pnl for t in wins)
    gl     = abs(sum(t.pnl for t in losses))
    pf     = gp / gl if gl > 0 else 999.0
    net    = balance - INITIAL_CAPITAL
    avg_w  = gp / len(wins) if wins else 0
    avg_l  = gl / len(losses) if losses else 0
    rr     = avg_w / avg_l if avg_l > 0 else 0

    eq_s = pd.Series([e["equity"] for e in equity])
    dd   = ((eq_s - eq_s.cummax()) / eq_s.cummax() * 100).min()

    return {
        "session_end":  session_end,
        "entry":        entry_type,
        "tp":           tp_type,
        "sweep":        sweep_filter,
        "trades":       len(trades),
        "win_rate":     round(wr, 1),
        "profit_factor":round(pf, 2),
        "net_$":        round(net, 0),
        "avg_rr":       round(rr, 2),
        "max_dd%":      round(dd, 1),
        "final_bal":    round(balance, 0),
    }


def main():
    print("\n" + "="*60)
    print("  JESH NAS M15 — Optimizer")
    print("="*60)

    if not os.path.exists(DATA_FILE):
        print(f"[ERROR] {DATA_FILE} not found. Run data_builder.py first.")
        return

    print(f"[DATA] Loading {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE, index_col=0, parse_dates=True)
    print(f"[DATA] {len(df):,} bars loaded  |  {df.index[0]} → {df.index[-1]}")

    keys   = [k for k in GRID if k != "atr_adjust"]
    combos = list(itertools.product(*[GRID[k] for k in keys]))
    total  = len(combos)
    print(f"[OPT]  Testing {total} combinations...\n")

    results = []
    for i, combo in enumerate(combos, 1):
        params = dict(zip(keys, combo))
        print(f"  [{i:>2}/{total}] {params}", end=" ... ", flush=True)
        r = run_combo(df, atr_adjust=0.0, **params)
        if r:
            results.append(r)
            print(f"WR={r['win_rate']}%  PF={r['profit_factor']}  Net=${r['net_$']:+,.0f}")
        else:
            print("no trades")

    if not results:
        print("\n[WARN] No results. Check data.")
        return

    rdf = pd.DataFrame(results)
    rdf.sort_values("profit_factor", ascending=False, inplace=True)
    rdf.reset_index(drop=True, inplace=True)

    print("\n" + "="*100)
    print("  TOP RESULTS — Ranked by Profit Factor")
    print("="*100)
    print(rdf.to_string(index=True))

    print("\n" + "="*60)
    print("  BEST COMBO:")
    best = rdf.iloc[0]
    for k, v in best.items():
        print(f"    {k:<18} {v}")

    rdf.to_csv("results/optimizer_results.csv", index=False)
    print("\n[OUTPUT] Full results saved → results/optimizer_results.csv")
    print("="*60 + "\n")


if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    main()
