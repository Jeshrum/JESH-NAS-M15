# =============================================================================
# JESH NAS M15 — Data Builder
# =============================================================================
# Loads raw M1 HistData CSVs (2010-2026), resamples to M15, saves to
# NAS100_15m.csv ready for the backtest engine.
#
# Run once:
#   cd "JESH NAS M15/backtest"
#   python3 data_builder.py
# =============================================================================

import os
import glob
import pandas as pd

# ─── Path to your raw M1 data folders ────────────────────────────────────────
DATA_ROOT = "/Users/mac/Desktop/fl/orb_alert_bot/backtest_data/NAS 2010-2026 DATA"
OUTPUT_FILE = "NAS100_15m.csv"

# ─── HistData M1 CSV format ───────────────────────────────────────────────────
# Columns: date, time, open, high, low, close, volume
# Example: 2010.11.14,18:01,2135.0,2135.0,2134.5,2134.5,0
COLUMNS = ["date", "time", "open", "high", "low", "close", "volume"]


def load_all_m1() -> pd.DataFrame:
    pattern = os.path.join(DATA_ROOT, "**", "*.csv")
    files   = sorted(glob.glob(pattern, recursive=True))

    if not files:
        raise FileNotFoundError(
            f"No CSV files found in {DATA_ROOT}\n"
            "Check that DATA_ROOT points to your NAS 2010-2026 DATA folder."
        )

    print(f"[DATA] Found {len(files)} M1 CSV files — loading...")
    frames = []

    for fp in files:
        try:
            df = pd.read_csv(fp, header=None, names=COLUMNS)
            df["datetime"] = pd.to_datetime(
                df["date"] + " " + df["time"], format="%Y.%m.%d %H:%M"
            )
            df.set_index("datetime", inplace=True)
            df.drop(columns=["date", "time"], inplace=True)
            df = df[["open", "high", "low", "close", "volume"]].astype(float)
            frames.append(df)
        except Exception as e:
            print(f"  [WARN] Skipping {os.path.basename(fp)}: {e}")

    combined = pd.concat(frames).sort_index()
    combined = combined[~combined.index.duplicated(keep="first")]
    print(f"[DATA] Loaded {len(combined):,} M1 bars  |  "
          f"{combined.index[0]}  →  {combined.index[-1]}")
    return combined


def resample_to_m15(df: pd.DataFrame) -> pd.DataFrame:
    print("[DATA] Resampling M1 → M15...")

    # HistData timestamps are in GMT+2 (MetaTrader server time, no DST)
    # NY session 9:30-16:00 = 14:30-21:00 GMT+2
    # We label bars as UTC and convert to NY in the strategy engine
    df.index = df.index.tz_localize("Etc/GMT-2").tz_convert("UTC")

    m15 = df.resample("15min").agg({
        "open":   "first",
        "high":   "max",
        "low":    "min",
        "close":  "last",
        "volume": "sum",
    }).dropna(subset=["open", "high", "low", "close"])

    print(f"[DATA] Resampled to {len(m15):,} M15 bars  |  "
          f"{m15.index[0]}  →  {m15.index[-1]}")
    return m15


def main():
    print("\n" + "=" * 55)
    print("  JESH NAS M15 — Data Builder")
    print("=" * 55)

    m1  = load_all_m1()
    m15 = resample_to_m15(m1)

    m15.to_csv(OUTPUT_FILE)
    print(f"[DATA] Saved → {OUTPUT_FILE}  ({os.path.getsize(OUTPUT_FILE) / 1e6:.1f} MB)")
    print("\nDone! Run optimizer.py next.\n")


if __name__ == "__main__":
    main()
