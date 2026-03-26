# =============================================================================
# JESH NAS M15 — HistData.com Downloader
# =============================================================================
# Downloads NSXUSD (NAS100) 1-minute data from histdata.com
# Resamples to 15-minute bars and saves as NAS100_15m.csv
#
# Usage:
#   python3 download_histdata.py
#
# Downloads selected years, merges them, resamples to 15m,
# and saves ready-to-use NAS100_15m.csv in the backtest folder.
# =============================================================================

import os
import io
import time
import zipfile
import webbrowser
import pandas as pd

# ─── Configuration ────────────────────────────────────────────────────────────
YEARS_TO_DOWNLOAD = [2023, 2024, 2025]   # Add/remove years as needed
OUTPUT_FILE       = "NAS100_15m.csv"
RAW_FOLDER        = "histdata_raw"       # Folder to store downloaded ZIPs

REFERER_URL  = "https://www.histdata.com/download-free-forex-data/?/metatrader/1-minute-bar-quotes/NSXUSD"


# ─── Parse MetaTrader M1 CSV ──────────────────────────────────────────────────
def parse_mt_csv(raw_bytes: bytes, year: int) -> pd.DataFrame | None:
    """
    Parse MetaTrader 1-minute CSV from ZIP.
    Format: <DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>
    e.g.:   20240102,000000,16500.00,16510.00,16490.00,16505.00,1234
    """
    try:
        zf = zipfile.ZipFile(io.BytesIO(raw_bytes))
        csv_name = [n for n in zf.namelist() if n.endswith(".csv")][0]
        raw_csv  = zf.read(csv_name).decode("utf-8", errors="ignore")

        lines = [l for l in raw_csv.strip().splitlines() if l and not l.startswith("<")]
        if not lines:
            return None

        rows = []
        for line in lines:
            parts = line.split(",")
            if len(parts) < 6:
                continue
            try:
                dt  = pd.to_datetime(parts[0] + parts[1], format="%Y%m%d%H%M%S")
                rows.append({
                    "datetime": dt,
                    "open":     float(parts[2]),
                    "high":     float(parts[3]),
                    "low":      float(parts[4]),
                    "close":    float(parts[5]),
                    "volume":   float(parts[6]) if len(parts) > 6 else 0,
                })
            except (ValueError, IndexError):
                continue

        if not rows:
            return None

        df = pd.DataFrame(rows).set_index("datetime")
        print(f"     Parsed {len(df):,} 1m bars for {year}")
        return df

    except Exception as e:
        print(f"     Parse error for {year}: {e}")
        return None


# ─── Resample 1m → 15m ───────────────────────────────────────────────────────
def resample_to_15m(df: pd.DataFrame) -> pd.DataFrame:
    """Resample 1-minute OHLCV bars into 15-minute bars."""
    df_15m = df.resample("15min").agg({
        "open":   "first",
        "high":   "max",
        "low":    "min",
        "close":  "last",
        "volume": "sum",
    }).dropna(subset=["open", "close"])
    return df_15m


# ─── Main ─────────────────────────────────────────────────────────────────────
def open_browser_downloads():
    """Open the histdata download page in the browser."""
    print("\n  Opening histdata.com in your browser...")
    print("  On the page:")
    print("  1. Make sure 'MetaTrader' platform is selected")
    print("  2. Select YEAR from the dropdown")
    print("  3. Click the green DOWNLOAD button")
    print(f"  4. Move the downloaded ZIP to: {os.path.abspath(RAW_FOLDER)}/\n")
    time.sleep(1)
    webbrowser.open(REFERER_URL)


def main():
    os.makedirs(RAW_FOLDER, exist_ok=True)
    all_frames = []

    print("\n" + "="*55)
    print("  JESH NAS M15 — HistData.com Data Processor")
    print("="*55)
    print(f"  Instrument : NSXUSD (NAS100 / Nasdaq)")
    print(f"  Years      : {YEARS_TO_DOWNLOAD}")
    print(f"  Output     : {OUTPUT_FILE}")
    print("="*55 + "\n")

    # Check if any ZIPs already exist in histdata_raw/
    found_zips = [
        f for f in os.listdir(RAW_FOLDER)
        if f.lower().endswith(".zip")
    ]

    if not found_zips:
        print(f"[INFO] No ZIP files found in histdata_raw/")
        print(f"[INFO] Opening browser to download them now...\n")
        open_browser_downloads()
        print_manual_instructions()
        return

    print(f"[INFO] Found {len(found_zips)} ZIP file(s):")
    for z in found_zips:
        print(f"       • {z}")

    # Check which years are missing
    missing = [y for y in YEARS_TO_DOWNLOAD
               if not any(str(y) in f for f in found_zips)]
    if missing:
        print(f"\n[INFO] Missing years: {missing}")
        print(f"[INFO] Opening browser to download them...\n")
        open_browser_downloads()
        print(f"  After downloading, move ZIPs to:")
        print(f"  {os.path.abspath(RAW_FOLDER)}/")
        print(f"  Then run this script again.\n")
        # Still process what we have
        print("[INFO] Processing available ZIPs now...\n")

    for year in YEARS_TO_DOWNLOAD:
        matches = [f for f in found_zips if str(year) in f]
        if not matches:
            print(f"  [SKIP] No ZIP found for {year}")
            continue

        zip_path = os.path.join(RAW_FOLDER, matches[0])
        print(f"  [READ] {matches[0]}")
        with open(zip_path, "rb") as f:
            raw_bytes = f.read()

        df_1m = parse_mt_csv(raw_bytes, year)
        if df_1m is not None:
            all_frames.append(df_1m)

    if not all_frames:
        print("\n[ERROR] Could not parse any data from the ZIP files.")
        print("  Make sure files are MetaTrader format from histdata.com")
        print_manual_instructions()
        return

    # ── Merge all years ──────────────────────────────────────────────────────
    print(f"\n[PROCESS] Merging {len(all_frames)} year(s) of 1m data...")
    df_all = pd.concat(all_frames).sort_index()
    df_all = df_all[~df_all.index.duplicated(keep="first")]
    print(f"[PROCESS] Total 1m bars: {len(df_all):,}")

    # ── Resample to 15m ──────────────────────────────────────────────────────
    print("[PROCESS] Resampling to 15-minute bars...")
    df_15m = resample_to_15m(df_all)
    print(f"[PROCESS] Total 15m bars: {len(df_15m):,}")
    print(f"[PROCESS] Date range: {df_15m.index[0]}  →  {df_15m.index[-1]}")

    # ── Save ─────────────────────────────────────────────────────────────────
    df_15m.to_csv(OUTPUT_FILE)
    print(f"\n[DONE] Saved to: {OUTPUT_FILE}")
    print(f"       Run python3 run_backtest.py to start the backtest.\n")


def print_manual_instructions():
    """Print manual download steps."""
    raw_abs = os.path.abspath(RAW_FOLDER)
    print("─" * 55)
    print("  HOW TO DOWNLOAD NAS100 DATA FROM HISTDATA.COM")
    print("─" * 55)
    print()
    print("  STEP 1 — Open this URL in your browser:")
    print()
    print("  https://www.histdata.com/download-free-forex-data/")
    print("  ?/metatrader/1-minute-bar-quotes/NSXUSD")
    print()
    print("  STEP 2 — For each year you want (2023, 2024, 2025):")
    print("    • Select the year from the dropdown")
    print("    • Click the green DOWNLOAD button")
    print("    • A ZIP file will download automatically")
    print()
    print("  STEP 3 — Move ALL downloaded ZIPs into this folder:")
    print(f"    {raw_abs}/")
    print()
    print("  STEP 4 — Run this script again:")
    print("    python3 download_histdata.py")
    print()
    print("  The script will parse, merge, resample to 15m")
    print(f"  and save ready-to-use {OUTPUT_FILE}")
    print("─" * 55)


if __name__ == "__main__":
    main()
