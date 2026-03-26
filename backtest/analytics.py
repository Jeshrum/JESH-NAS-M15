# =============================================================================
# JESH NAS M15 — Analytics & Reporting Module
# =============================================================================
# Takes raw trade list + equity curve and produces:
#   - Summary stats (win rate, profit factor, Sharpe, max DD)
#   - Monthly performance breakdown
#   - Trade log CSV
#   - Equity curve plot
#   - Monthly returns heatmap

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from config import INITIAL_CAPITAL, RISK_MODE, OUTPUT_DIR


def build_trade_log(trades: list) -> pd.DataFrame:
    """Convert list of Trade objects into a clean DataFrame."""
    if not trades:
        return pd.DataFrame()

    rows = []
    for t in trades:
        rows.append({
            "entry_date":   t.entry_date,
            "exit_date":    t.exit_date,
            "direction":    t.direction.upper(),
            "entry_price":  round(t.entry_price, 2),
            "exit_price":   round(t.exit_price,  2) if t.exit_price else None,
            "sl_price":     round(t.sl_price,     2),
            "tp_price":     round(t.tp_price,     2),
            "qty":          t.qty,
            "exit_reason":  t.exit_reason,
            "pnl":          round(t.pnl, 2),
            "pnl_pct":      round(t.pnl_pct, 4),
            "risk_amount":  round(t.risk_amount, 2),
        })
    return pd.DataFrame(rows)


def compute_summary(trades: list, equity_curve: pd.DataFrame,
                    final_balance: float) -> dict:
    """Compute all performance metrics from trades + equity curve."""

    if not trades:
        return {"error": "No trades found"}

    log = build_trade_log(trades)
    closed = log[log["exit_reason"].notna()].copy()

    total_trades  = len(closed)
    winners       = closed[closed["pnl"] > 0]
    losers        = closed[closed["pnl"] <= 0]
    win_rate      = len(winners) / total_trades * 100 if total_trades else 0

    gross_profit  = winners["pnl"].sum()
    gross_loss    = abs(losers["pnl"].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float("inf")

    net_profit    = final_balance - INITIAL_CAPITAL
    net_pct       = net_profit / INITIAL_CAPITAL * 100

    avg_win       = winners["pnl"].mean() if len(winners) > 0 else 0
    avg_loss      = losers["pnl"].mean()  if len(losers)  > 0 else 0
    avg_rr        = abs(avg_win / avg_loss) if avg_loss != 0 else float("inf")

    # Max Drawdown
    eq = equity_curve["equity"]
    rolling_max   = eq.cummax()
    drawdown      = (eq - rolling_max) / rolling_max * 100
    max_drawdown  = drawdown.min()

    # Sharpe Ratio (annualised, assumes 252 trading days, ~10 trades/day slots)
    daily_equity  = equity_curve["equity"].resample("1D").last().dropna()
    daily_returns = daily_equity.pct_change().dropna()
    sharpe        = (daily_returns.mean() / daily_returns.std() * np.sqrt(252)
                     if daily_returns.std() > 0 else 0)

    return {
        "initial_capital":  INITIAL_CAPITAL,
        "final_balance":    round(final_balance,  2),
        "net_profit":       round(net_profit,      2),
        "net_profit_pct":   round(net_pct,         2),
        "total_trades":     total_trades,
        "winning_trades":   len(winners),
        "losing_trades":    len(losers),
        "win_rate":         round(win_rate,         2),
        "profit_factor":    round(profit_factor,    3),
        "avg_win":          round(avg_win,          2),
        "avg_loss":         round(avg_loss,         2),
        "avg_rr":           round(avg_rr,           2),
        "max_drawdown_pct": round(max_drawdown,     2),
        "sharpe_ratio":     round(sharpe,           3),
        "risk_mode":        RISK_MODE,
    }


def compute_monthly_returns(trades: list) -> pd.DataFrame:
    """Produce a month-by-month P&L breakdown."""
    if not trades:
        return pd.DataFrame()

    log = build_trade_log(trades)
    log = log[log["exit_date"].notna()].copy()
    log["month"] = pd.to_datetime(log["exit_date"]).dt.to_period("M")

    monthly = log.groupby("month").agg(
        trades      = ("pnl", "count"),
        wins        = ("pnl", lambda x: (x > 0).sum()),
        gross_pnl   = ("pnl", "sum"),
        avg_pnl     = ("pnl", "mean"),
    ).reset_index()

    monthly["win_rate"]  = (monthly["wins"] / monthly["trades"] * 100).round(1)
    monthly["gross_pnl"] = monthly["gross_pnl"].round(2)
    monthly["avg_pnl"]   = monthly["avg_pnl"].round(2)
    return monthly


def print_summary(summary: dict, monthly: pd.DataFrame):
    """Pretty-print results to terminal."""
    sep = "═" * 55

    print(f"\n{sep}")
    print(f"  JESH NAS M15 — Backtest Results  [{summary['risk_mode'].upper()}]")
    print(sep)
    print(f"  Initial Capital  : ${summary['initial_capital']:>10,.2f}")
    print(f"  Final Balance    : ${summary['final_balance']:>10,.2f}")
    print(f"  Net Profit       : ${summary['net_profit']:>+10,.2f}  ({summary['net_profit_pct']:+.2f}%)")
    print(f"  Max Drawdown     : {summary['max_drawdown_pct']:>+10.2f}%")
    print(f"  Sharpe Ratio     : {summary['sharpe_ratio']:>10.3f}")
    print(sep)
    print(f"  Total Trades     : {summary['total_trades']:>10}")
    print(f"  Win Rate         : {summary['win_rate']:>9.1f}%")
    print(f"  Profit Factor    : {summary['profit_factor']:>10.3f}")
    print(f"  Avg Win          : ${summary['avg_win']:>+10,.2f}")
    print(f"  Avg Loss         : ${summary['avg_loss']:>+10,.2f}")
    print(f"  Avg R:R          : {summary['avg_rr']:>10.2f}")
    print(sep)

    if not monthly.empty:
        print("\n  MONTHLY BREAKDOWN")
        print(f"  {'Month':<12} {'Trades':>6} {'Wins':>5} {'WR%':>6} {'P&L':>10}")
        print(f"  {'-'*12} {'-'*6} {'-'*5} {'-'*6} {'-'*10}")
        for _, row in monthly.iterrows():
            sign = "+" if row["gross_pnl"] >= 0 else ""
            print(f"  {str(row['month']):<12} {int(row['trades']):>6} "
                  f"{int(row['wins']):>5} {row['win_rate']:>5.1f}% "
                  f"  {sign}${row['gross_pnl']:>8,.2f}")
        print()


def save_results(trade_log: pd.DataFrame, summary: dict,
                 monthly: pd.DataFrame, equity_curve: pd.DataFrame):
    """Save all results to CSV files."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    trade_log.to_csv(f"{OUTPUT_DIR}/trade_log.csv", index=False)
    pd.DataFrame([summary]).to_csv(f"{OUTPUT_DIR}/summary.csv", index=False)
    monthly.to_csv(f"{OUTPUT_DIR}/monthly_returns.csv", index=False)
    equity_curve.to_csv(f"{OUTPUT_DIR}/equity_curve.csv")
    print(f"[OUTPUT] Results saved to /{OUTPUT_DIR}/")


def plot_results(equity_curve: pd.DataFrame, trades: list, monthly: pd.DataFrame):
    """
    Plot:
      1. Equity curve with drawdown overlay
      2. Monthly P&L bar chart
      3. Trade P&L distribution
    """
    log = build_trade_log(trades)
    eq  = equity_curve["equity"]

    sns.set_theme(style="darkgrid")
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle("JESH NAS M15 — Backtest Report", fontsize=15, fontweight="bold", y=0.98)
    gs  = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35)

    # ── 1. Equity Curve ──────────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(eq.index, eq.values, color="#00C853", linewidth=1.5, label="Equity")
    ax1.axhline(INITIAL_CAPITAL, color="gray", linestyle="--", linewidth=0.8, label="Starting Capital")
    ax1.fill_between(eq.index, eq.values, INITIAL_CAPITAL,
                     where=(eq.values >= INITIAL_CAPITAL), alpha=0.15, color="#00C853")
    ax1.fill_between(eq.index, eq.values, INITIAL_CAPITAL,
                     where=(eq.values <  INITIAL_CAPITAL), alpha=0.20, color="#FF1744")
    ax1.set_title("Equity Curve", fontsize=11)
    ax1.set_ylabel("Account Balance ($)")
    ax1.legend(fontsize=9)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    # ── 2. Drawdown ──────────────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[1, :])
    rolling_max = eq.cummax()
    drawdown    = (eq - rolling_max) / rolling_max * 100
    ax2.fill_between(drawdown.index, drawdown.values, 0, color="#FF1744", alpha=0.6)
    ax2.set_title("Drawdown (%)", fontsize=11)
    ax2.set_ylabel("Drawdown %")
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.1f}%"))

    # ── 3. Monthly P&L bar chart ─────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[2, 0])
    if not monthly.empty:
        colors = ["#00C853" if v >= 0 else "#FF1744" for v in monthly["gross_pnl"]]
        ax3.bar(monthly["month"].astype(str), monthly["gross_pnl"], color=colors)
        ax3.axhline(0, color="white", linewidth=0.8)
        ax3.set_title("Monthly P&L ($)", fontsize=11)
        ax3.set_ylabel("P&L ($)")
        plt.setp(ax3.get_xticklabels(), rotation=45, ha="right", fontsize=8)
        ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    # ── 4. Trade P&L Distribution ────────────────────────────────────────────
    ax4 = fig.add_subplot(gs[2, 1])
    if not log.empty:
        wins  = log[log["pnl"] > 0]["pnl"]
        losses= log[log["pnl"] <= 0]["pnl"]
        ax4.hist(wins,   bins=20, color="#00C853", alpha=0.7, label="Winners")
        ax4.hist(losses, bins=20, color="#FF1744", alpha=0.7, label="Losers")
        ax4.axvline(0, color="white", linewidth=1)
        ax4.set_title("Trade P&L Distribution", fontsize=11)
        ax4.set_xlabel("P&L ($)")
        ax4.legend(fontsize=9)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(f"{OUTPUT_DIR}/backtest_report.png", dpi=150, bbox_inches="tight")
    print(f"[OUTPUT] Chart saved to /{OUTPUT_DIR}/backtest_report.png")
    plt.show()
