# =============================================================================
# JESH NAS M15 — Data Feed Module
# =============================================================================
# Handles downloading and loading OHLCV data.
#
# Supported sources:
#   1. TradingView CSV export  ← RECOMMENDED for accurate NAS100 data
#   2. Yahoo Finance download  (15m limited to last 60 days on free tier)
#
# HOW TO EXPORT FROM TRADINGVIEW:
#   1. Open NAS100 / US100 chart on 15min timeframe
#   2. Click the Export icon (top-right of chart, looks like a download arrow)
#   3. Save the file as "NAS100_15m.csv"
#   4. Drop it into this folder: JESH NAS M15/backtest/
#   5. In config.py set: TV_CSV_FILE = "NAS100_15m.csv"
# =============================================================================

import os
import pandas as pd
import pytz
import yfinance as yf
from config import SYMBOL, TIMEFRAME, DATA_START, DATA_END, TIMEZONE


TV_CSV_FILE = "NAS100_15m.csv"   # Set to None to use Yahoo Finance instead


def load_tradingview_csv(filepath: str) -> pd.DataFrame:
    """
    Load and normalise a TradingView CSV export.

    TradingView exports in this format:
        time,open,high,low,close,Volume
        2024-01-02 09:30:00,16500.0,16520.0,16490.0,16510.0,12345

    Handles both:
      - UTC timestamps  (TradingView default)
      - Exchange-local  (when TV is set to exchange time)
    """
    print(f"[DATA] Loading TradingView CSV: {filepath}")

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"\n[ERROR] TradingView CSV not found: {filepath}\n"
            "  → Export it from TradingView (chart → download icon)\n"
            "  → Save as NAS100_15m.csv in the backtest/ folder\n"
            "  → Or set TV_CSV_FILE = None in data_feed.py to use Yahoo Finance"
        )

    # Peek at the first data row to detect if timestamps are tz-aware
    with open(filepath, "r") as _f:
        _header = _f.readline()
        _first  = _f.readline().strip()

    # Detect time column name
    _cols = [c.strip().lower() for c in _header.split(",")]
    _time_col = next((c for c in _cols if c in ["time", "datetime", "date", "timestamp"]), None)
    if _time_col is None:
        raise ValueError(f"[ERROR] Could not find datetime column. Columns found: {_cols}")

    # Detect if first timestamp has tz offset (e.g. "-05:00" or "+00:00")
    _first_val = _first.split(",")[_cols.index(_time_col)]
    _has_tz = "+" in _first_val[10:] or (_first_val.count("-") > 2)

    if _has_tz:
        df = pd.read_csv(filepath, index_col=_time_col,
                         parse_dates=True)
        df.index = pd.to_datetime(df.index, utc=True)
    else:
        df = pd.read_csv(filepath, index_col=_time_col,
                         parse_dates=True)

    df.columns = [c.strip().lower() for c in df.columns]
    df.index.name = "datetime"

    # Localise to NY time
    tz = pytz.timezone(TIMEZONE)
    if df.index.tz is None:
        try:
            df.index = df.index.tz_localize("UTC").tz_convert(tz)
            print(f"[DATA] Timestamps localised: UTC → {TIMEZONE}")
        except Exception:
            df.index = df.index.tz_localize(tz)
            print(f"[DATA] Timestamps localised as {TIMEZONE}")
    else:
        df.index = df.index.tz_convert(tz)

    # Keep only OHLCV columns
    rename_map = {"vol": "volume", "vol.": "volume"}
    df.rename(columns=rename_map, inplace=True)
    keep = [c for c in ["open", "high", "low", "close", "volume"] if c in df.columns]
    df = df[keep].copy()
    df = df.apply(pd.to_numeric, errors="coerce")
    df.dropna(subset=["open", "high", "low", "close"], inplace=True)
    df.sort_index(inplace=True)

    print(f"[DATA] Loaded {len(df):,} bars  |  {df.index[0]}  →  {df.index[-1]}")
    return df


def download_data(symbol=SYMBOL, timeframe=TIMEFRAME,
                  start=DATA_START, end=DATA_END,
                  cache=True) -> pd.DataFrame:
    """
    Download OHLCV data from Yahoo Finance.
    NOTE: Yahoo free tier limits 15m data to the last 60 days.
    For longer history use load_tradingview_csv() instead.
    """
    cache_file = f"cache_{symbol.replace('=','').replace('^','')}_{timeframe}_{start}_{end}.csv"

    if cache and os.path.exists(cache_file):
        print(f"[DATA] Loading cached data from {cache_file}")
        df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
        return df

    print(f"[DATA] Downloading {symbol} {timeframe} from {start} to {end}...")
    df = yf.download(
        tickers=symbol,
        start=start,
        end=end,
        interval=timeframe,
        auto_adjust=True,
        progress=False,
    )

    if df.empty:
        raise ValueError(
            f"No data returned for {symbol}.\n"
            "  Yahoo Finance 15m data is limited to the last 60 days.\n"
            "  → Export from TradingView for longer history (see instructions above)."
        )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.columns = [c.lower() for c in df.columns]
    df = df[["open", "high", "low", "close", "volume"]].copy()
    df.dropna(inplace=True)

    if cache:
        df.to_csv(cache_file)
        print(f"[DATA] Saved to cache: {cache_file}")

    print(f"[DATA] Loaded {len(df):,} bars from {df.index[0]} to {df.index[-1]}")
    return df


def get_data() -> pd.DataFrame:
    """
    Master data loader — call this from run_backtest.py.
    Uses TradingView CSV if TV_CSV_FILE is set, otherwise Yahoo Finance.
    """
    if TV_CSV_FILE and os.path.exists(TV_CSV_FILE):
        return load_tradingview_csv(TV_CSV_FILE)
    elif TV_CSV_FILE and not os.path.exists(TV_CSV_FILE):
        print(f"[DATA] TV CSV not found ({TV_CSV_FILE}) — falling back to Yahoo Finance")
    return download_data()
