# =============================================================================
# JESH NAS M15 — Data Feed Module
# =============================================================================
# Handles downloading and loading OHLCV data.
# Supports: Yahoo Finance (live download) or local CSV file.

import os
import pandas as pd
import yfinance as yf
from config import SYMBOL, TIMEFRAME, DATA_START, DATA_END


def download_data(symbol=SYMBOL, timeframe=TIMEFRAME,
                  start=DATA_START, end=DATA_END,
                  cache=True) -> pd.DataFrame:
    """
    Download OHLCV data from Yahoo Finance.
    Caches to CSV so we don't re-download every run.
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
        raise ValueError(f"No data returned for {symbol}. Check ticker or date range.")

    # Flatten multi-level columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.columns = [c.lower() for c in df.columns]
    df = df[["open", "high", "low", "close", "volume"]].copy()
    df.dropna(inplace=True)

    if cache:
        df.to_csv(cache_file)
        print(f"[DATA] Saved to cache: {cache_file}")

    print(f"[DATA] Loaded {len(df)} bars from {df.index[0]} to {df.index[-1]}")
    return df


def load_from_csv(filepath: str) -> pd.DataFrame:
    """
    Load OHLCV data from a local CSV file.
    CSV must have columns: datetime, open, high, low, close, volume
    """
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    df.columns = [c.lower() for c in df.columns]
    required = {"open", "high", "low", "close"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required}")
    df.dropna(inplace=True)
    print(f"[DATA] Loaded {len(df)} bars from CSV: {filepath}")
    return df
