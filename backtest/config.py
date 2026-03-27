# =============================================================================
# JESH NAS M15 — Backtest Configuration
# =============================================================================
# Edit these values to change how the backtest runs.
# No need to touch any other file for basic configuration.

# ─── Account Settings ────────────────────────────────────────────────────────
INITIAL_CAPITAL     = 10_000        # Prop firm account size ($)
COMMISSION_PER_SIDE = 0.50          # Commission per contract per side ($)

# ─── Risk Modes ──────────────────────────────────────────────────────────────
# Choose one: "conservative" | "normal" | "aggressive"
RISK_MODE = "normal"

RISK_MODES = {
    "conservative": 0.01,   # 1% risk per trade
    "normal":       0.02,   # 2% risk per trade
    "aggressive":   0.03,   # 3% risk per trade
}

# ─── Strategy Parameters ─────────────────────────────────────────────────────
SESSION_START       = "09:30"       # NY time — session open
SESSION_END         = "11:30"       # NY time — stop new entries
FORCE_CLOSE_TIME    = "16:55"       # NY time — force close all positions
TIMEZONE            = "America/New_York"

# ATR settings
ATR_LENGTH          = 14
LIMIT_ATR_IMPROVEMENT = 0.5        # Pull limit entry back by ATR * this value
TP_ATR_REDUCTION    = 0.5          # Pull TP back by ATR * this value

# ─── Data Settings ───────────────────────────────────────────────────────────
SYMBOL              = "QQQ"         # Nasdaq 100 ETF (Yahoo Finance — proxy for NAS100)
TIMEFRAME           = "15m"         # 15-minute candles
DATA_START          = "2026-01-26"   # Yahoo free tier: 15m limited to last 60 days
DATA_END            = "2026-03-26"

# ─── Prop Firm Risk Rules ─────────────────────────────────────────────────────
# Circuit breakers — trading halts if these are breached
DAILY_LOSS_LIMIT_PCT  = 0.05    # 5%  daily loss limit  → $500 on $10k account
MAX_DRAWDOWN_PCT      = 0.10    # 10% max drawdown limit → $1,000 on $10k account

# ─── Output Settings ─────────────────────────────────────────────────────────
OUTPUT_DIR          = "results"     # Folder where results are saved
SAVE_TRADE_LOG      = True
SAVE_EQUITY_CURVE   = True
SHOW_PLOTS          = True
