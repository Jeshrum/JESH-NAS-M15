# =============================================================================
# JESH NAS M15 — Run Backtest
# =============================================================================
# Entry point. Run this file to execute the full backtest.
#
#   cd "JESH NAS M15/backtest"
#   python3 run_backtest.py
#
# To change settings (capital, risk mode, dates), edit config.py only.
# =============================================================================

from data_feed   import download_data
from strategy    import run_strategy
from analytics   import (build_trade_log, compute_summary,
                         compute_monthly_returns, print_summary,
                         save_results, plot_results)
from config      import SAVE_TRADE_LOG, SAVE_EQUITY_CURVE, SHOW_PLOTS


def main():
    print("\n" + "="*55)
    print("  JESH NAS M15 — Backtest Engine Starting...")
    print("="*55)

    # ── 1. Load Data ─────────────────────────────────────────────────────────
    df = download_data()

    # ── 2. Run Strategy ──────────────────────────────────────────────────────
    print("[ENGINE] Running strategy simulation...")
    results = run_strategy(df)

    trades        = results["trades"]
    equity_curve  = results["equity_curve"]
    final_balance = results["final_balance"]

    if not trades:
        print("\n[WARNING] No trades were generated.")
        print("  Check that your data covers the NY session (9:30–11:30 AM ET).")
        print("  Also verify that PDH/PDL sweep conditions are being met.")
        return

    print(f"[ENGINE] Simulation complete. {len(trades)} trades generated.")

    # ── 3. Analytics ─────────────────────────────────────────────────────────
    trade_log = build_trade_log(trades)
    summary   = compute_summary(trades, equity_curve, final_balance)
    monthly   = compute_monthly_returns(trades)

    # ── 4. Print Results ─────────────────────────────────────────────────────
    print_summary(summary, monthly)

    # ── 5. Save Results ───────────────────────────────────────────────────────
    save_results(trade_log, summary, monthly, equity_curve)

    # ── 6. Plot ───────────────────────────────────────────────────────────────
    if SHOW_PLOTS:
        plot_results(equity_curve, trades, monthly)


if __name__ == "__main__":
    main()
