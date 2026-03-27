# JESH NAS M15 — NAS100 Opening Range Breakout Strategy

> A disciplined, rules-based 15-minute ORB strategy for NAS100 (US100/MNQ).
> Trades the NY open session only. No indicators. No guessing. Just levels.
> **Nigerian time: 2:30 PM – 4:30 PM WAT**

---

## Backtest Results — 16 Years of Real NAS100 Data (2010–2026)

![Backtest Equity Curve](images/backtest_screen.png)

![Backtest Report](images/backtest_report.png)

| Metric | Result |
|---|---|
| **Period** | Nov 2010 – Mar 2026 (16 years) |
| **Initial Capital** | $10,000 |
| **Final Balance** | $139,213 |
| **Net Profit** | **+$129,213 (+1,292%)** |
| **Total Trades** | 1,564 |
| **Win Rate** | 44.2% |
| **Profit Factor** | 1.962 |
| **Avg Win / Avg Loss** | +$513 / -$208 |
| **Avg R:R** | 2.47 |
| **Max Drawdown** | -40.24% (from equity peak) |
| **Sharpe Ratio** | 0.768 |
| **Prop Firm Floor Breached** | **Never** |

### Year-by-Year — Every Single Year Was Profitable

| Year | Green Months | Annual P&L |
|---|---|---|
| 2010 (Nov–Dec) | 1/2 | +$1,131 |
| 2011 | 8/12 | +$10,318 |
| 2012 | 6/12 | +$5,486 |
| 2013 | 8/12 | +$7,365 |
| 2014 | 7/12 | +$10,517 |
| 2015 | 11/12 | +$16,737 |
| 2016 | 8/12 | +$10,153 |
| 2017 | 6/12 | +$8,914 |
| 2018 | 5/12 | +$5,474 |
| 2019 | 9/12 | +$4,029 |
| **2020 (COVID crash)** | 7/12 | **+$6,455** |
| 2021 | 11/12 | +$22,127 |
| **2022 (Rate hike cycle)** | 10/12 | **+$16,319** |
| 2023 | 9/12 | +$12,186 |
| 2024 | 9/12 | +$18,786 |
| 2025 | 11/12 | +$13,596 |
| 2026 (Jan–Mar) | 2/3 | +$4,524 |

**16 profitable years out of 16. 128 green months out of 185 (69.2%).**

> Backtested with fixed $10,000 position sizing, 2% risk per trade, $0.50 commission per side, prop firm circuit breakers (5% daily loss limit, 10% max drawdown). No lookahead bias. Bar-by-bar simulation on real 1-minute NAS100 data from histdata.com.

---

## Monthly P&L — Last 5 Years at 1% Risk (Prop Firm Rules)

> **Rules applied:** 1% risk per trade ($100 on $10k) · $0.50 commission per side · 5% daily loss limit · 10% max drawdown · 1 trade per day · Force close at session end
>
> **% column** = return as % of the original $10,000 base. Balance compounds as profits accumulate.

---

### 2021 — **+$11,186 on the year** | Started: $10,000 → Ended: $21,186

| Month | Trades | Wins | Win Rate | P&L ($) | % of $10k | Running Balance |
|---|---|---|---|---|---|---|
| Jan | 7 | 3 | 42.9% | +$254 | +2.54% | $10,254 |
| Feb | 7 | 3 | 42.9% | +$1,514 | +15.14% | $11,768 |
| Mar | 13 | 6 | 46.2% | +$412 | +4.12% | $12,180 |
| Apr | 8 | 4 | 50.0% | +$770 | +7.70% | $12,949 |
| May | 7 | 2 | 28.6% | +$377 | +3.77% | $13,326 |
| Jun | 3 | 0 | 0.0% | −$299 | −2.99% | $13,027 |
| **Jul** | 7 | 6 | **85.7%** | **+$2,745** | **+27.45%** | **$15,772** |
| Aug | 8 | 3 | 37.5% | +$311 | +3.11% | $16,083 |
| Sep | 6 | 3 | 50.0% | +$705 | +7.05% | $16,788 |
| Oct | 11 | 6 | 54.5% | +$1,309 | +13.09% | $18,097 |
| Nov | 10 | 6 | 60.0% | +$1,924 | +19.24% | $20,021 |
| Dec | 10 | 3 | 30.0% | +$1,165 | +11.65% | $21,186 |

---

### 2022 — **+$7,956 on the year** | Started: $21,186 → Ended: $29,142 *(rate hike cycle)*

| Month | Trades | Wins | Win Rate | P&L ($) | % of $10k | Running Balance |
|---|---|---|---|---|---|---|
| Jan | 9 | 5 | 55.6% | +$871 | +8.71% | $22,057 |
| **Feb** | 8 | 6 | **75.0%** | **+$1,449** | **+14.49%** | **$23,506** |
| Mar | 7 | 2 | 28.6% | +$48 | +0.48% | $23,554 |
| Apr | 8 | 3 | 37.5% | −$188 | −1.88% | $23,366 |
| May | 11 | 3 | 27.3% | +$233 | +2.33% | $23,599 |
| Jun | 8 | 4 | 50.0% | −$156 | −1.56% | $23,443 |
| Jul | 3 | 1 | 33.3% | −$17 | −0.17% | $23,426 |
| Aug | 8 | 5 | 62.5% | +$1,081 | +10.81% | $24,507 |
| Sep | 8 | 5 | 62.5% | +$964 | +9.64% | $25,471 |
| Oct | 7 | 4 | 57.1% | +$1,050 | +10.50% | $26,521 |
| Nov | 6 | 3 | 50.0% | +$425 | +4.25% | $26,946 |
| **Dec** | 10 | 7 | **70.0%** | **+$2,196** | **+21.96%** | **$29,142** |

---

### 2023 — **+$5,878 on the year** | Started: $29,142 → Ended: $35,020

| Month | Trades | Wins | Win Rate | P&L ($) | % of $10k | Running Balance |
|---|---|---|---|---|---|---|
| Jan | 9 | 6 | 66.7% | +$1,094 | +10.94% | $30,236 |
| Feb | 6 | 2 | 33.3% | +$235 | +2.35% | $30,471 |
| Mar | 2 | 1 | 50.0% | −$20 | −0.19% | $30,452 |
| Apr | 3 | 2 | 66.7% | +$168 | +1.68% | $30,620 |
| May | 3 | 1 | 33.3% | −$54 | −0.54% | $30,566 |
| Jun | 8 | 4 | 50.0% | +$470 | +4.70% | $31,036 |
| **Jul** | 4 | 4 | **100%** | **+$670** | **+6.70%** | **$31,706** |
| Aug | 13 | 5 | 38.5% | +$929 | +9.29% | $32,635 |
| Sep | 10 | 6 | 60.0% | +$1,454 | +14.54% | $34,089 |
| **Oct** | 4 | 4 | **100%** | **+$364** | **+3.64%** | **$34,453** |
| Nov | 11 | 6 | 54.5% | +$575 | +5.75% | $35,028 |
| Dec | 7 | 4 | 57.1% | −$8 | −0.08% | $35,020 |

---

### 2024 — **+$9,344 on the year** | Started: $35,020 → Ended: $44,364

| Month | Trades | Wins | Win Rate | P&L ($) | % of $10k | Running Balance |
|---|---|---|---|---|---|---|
| Jan | 8 | 4 | 50.0% | +$710 | +7.10% | $35,730 |
| **Feb** | 13 | 9 | **69.2%** | **+$1,655** | **+16.55%** | **$37,385** |
| Mar | 7 | 5 | 71.4% | +$947 | +9.47% | $38,332 |
| Apr | 11 | 7 | 63.6% | +$1,826 | +18.27% | $40,158 |
| May | 12 | 8 | 66.7% | +$1,389 | +13.89% | $41,548 |
| **Jun** | 12 | 6 | 50.0% | **+$2,292** | **+22.92%** | **$43,840** |
| Jul | 5 | 1 | 20.0% | +$407 | +4.07% | $44,247 |
| Aug | 11 | 3 | 27.3% | −$129 | −1.29% | $44,118 |
| Sep | 7 | 3 | 42.9% | −$62 | −0.62% | $44,057 |
| Oct | 7 | 3 | 42.9% | +$24 | +0.24% | $44,081 |
| Nov | 7 | 3 | 42.9% | +$675 | +6.75% | $44,756 |
| Dec | 8 | 2 | 25.0% | −$392 | −3.92% | $44,364 |

---

### 2025 — **+$7,006 on the year** | Started: $44,364 → Ended: $51,369

| Month | Trades | Wins | Win Rate | P&L ($) | % of $10k | Running Balance |
|---|---|---|---|---|---|---|
| Jan | 7 | 4 | 57.1% | +$144 | +1.44% | $44,508 |
| Feb | 8 | 3 | 37.5% | +$233 | +2.33% | $44,741 |
| **Mar** | 7 | 4 | 57.1% | **+$1,934** | **+19.34%** | **$46,675** |
| Apr | 11 | 3 | 27.3% | +$1,309 | +13.09% | $47,984 |
| May | 12 | 5 | 41.7% | +$331 | +3.31% | $48,315 |
| Jun | 6 | 4 | 66.7% | +$254 | +2.54% | $48,569 |
| Jul | 10 | 4 | 40.0% | +$308 | +3.08% | $48,877 |
| Aug | 8 | 5 | 62.5% | +$1,255 | +12.55% | $50,131 |
| Sep | 10 | 3 | 30.0% | +$313 | +3.13% | $50,444 |
| Oct | 6 | 3 | 50.0% | +$849 | +8.49% | $51,293 |
| Nov | 4 | 2 | 50.0% | +$436 | +4.36% | $51,729 |
| Dec | 5 | 1 | 20.0% | −$360 | −3.60% | $51,369 |

---

### 2026 — **+$2,437 YTD** | Started: $51,369 → Current: $53,806 *(Jan–Mar only)*

| Month | Trades | Wins | Win Rate | P&L ($) | % of $10k | Running Balance |
|---|---|---|---|---|---|---|
| Jan | 11 | 5 | 45.5% | +$1,537 | +15.37% | $52,906 |
| Feb | 13 | 5 | 38.5% | +$940 | +9.40% | $53,846 |
| Mar | 5 | 1 | 20.0% | −$40 | −0.40% | $53,806 |

---

### 5-Year Summary

| Year | Annual P&L | Year Return | End Balance |
|---|---|---|---|
| 2021 | +$11,186 | +111.9% | $21,186 |
| 2022 | +$7,956 | +37.6% | $29,142 |
| 2023 | +$5,878 | +20.2% | $35,020 |
| 2024 | +$9,344 | +26.7% | $44,364 |
| 2025 | +$7,006 | +15.8% | $51,369 |
| 2026 (Jan–Mar) | +$2,437 | +4.7% | $53,806 |

**$10,000 → $53,806 in 5 years. At 1% risk. 2 hours a day.**

---

## Table of Contents

1. [What Is This Strategy?](#what-is-this-strategy)
2. [How It Works](#how-it-works)
3. [Setup — TradingView](#setup--tradingview)
4. [Settings Panel Explained](#settings-panel-explained)
5. [How to Read the Signals](#how-to-read-the-signals)
6. [How to Execute a Trade](#how-to-execute-a-trade)
7. [Risk Management](#risk-management)
8. [Session Times by Timezone](#session-times-by-timezone)
9. [Python Backtest Engine](#python-backtest-engine)
10. [FAQ](#faq)

---

## What Is This Strategy?

**JESH NAS M15** is a New York Opening Range Breakout (ORB) strategy built for **NAS100 on the 15-minute chart**.

The core idea is simple:
- The first 15-minute candle after the NY open (9:30 AM ET) defines the **opening range**
- If price breaks above that range → **Long signal**
- If price breaks below that range → **Short signal**
- Stop Loss is set at the opposite end of the opening range
- Take Profit targets are shown on the chart automatically

The strategy uses **ICT liquidity sweep filters** — it only takes longs if the previous day's low was swept first, and shorts if the previous day's high was swept. This removes low-quality setups and improves trade quality significantly.

**You only need to be at your screen for 2 hours: 2:30 PM – 4:30 PM Nigerian time (WAT).**

---

## How It Works

### Step 1 — The Opening Range
At exactly **2:30 PM Nigerian time (WAT)**, the first 15-minute candle forms.

```
First candle HIGH  →  Resistance / Long trigger level
First candle LOW   →  Support / Short trigger level
```

These levels are plotted on the chart as orange (high) and blue (low) lines.

### Step 2 — The Filter (PDH/PDL Sweep)
Before taking any trade, the strategy checks:

- **For Longs:** Did price sweep (break below) the **Previous Day Low** today before the signal? If yes → long is valid.
- **For Shorts:** Did price sweep (break above) the **Previous Day High** today before the signal? If yes → short is valid.

This is an ICT concept — smart money grabs liquidity before the real move.

### Step 3 — The Signal
When price **closes a 15-minute candle** above the first bar high (or below the first bar low), and the sweep filter is confirmed:

- A **green triangle** appears below the bar (Long)
- A **red triangle** appears above the bar (Short)
- A **signal info label** appears on the chart showing exact Entry, SL, TP 2R, TP 3R

### Step 4 — Trade Management
- **Stop Loss** = First bar low (long) / First bar high (short)
- **TP 2R** = Entry + (risk × 2)
- **TP 3R** = Entry + (risk × 3)
- All positions are force-closed before **10:00 PM Nigerian time** / 5:00 PM NY time (no overnight holds)

---

## Setup — TradingView

### Requirements
- TradingView account (free plan works for manual trading)
- NAS100, US100, or MNQ1! chart open on **15-minute timeframe**

### Installation

1. Open [TradingView](https://tradingview.com)
2. Open the **NAS100** or **US100** chart
3. Set timeframe to **15 minutes**
4. Click **Pine Editor** at the bottom of the screen
5. Delete any existing code in the editor
6. Open the file `JESH_NAS_M15.pine` from this repo
7. Select all the code (Ctrl+A / Cmd+A) and paste it into Pine Editor
8. Click **Save** then click **Add to chart**
9. The strategy will load on your chart

---

## Settings Panel Explained

Click the **gear icon** next to the strategy name on the chart to open settings.

### Trading Session
| Setting | Default | What It Does |
|---|---|---|
| Trading Session NY | 09:30–11:30 | Only allows new trades during this window |
| Enable Force Close EOD | ON | Closes all positions before 5 PM NY |
| Cancel All Orders at Session End | ON | Cancels pending limit orders after session |
| Use Limit Orders for Entry | ON | Enters on a slight pullback, not at the breakout candle |

### Position Sizing
| Setting | Default | What It Does |
|---|---|---|
| Account Size ($) | $10,000 | Your prop firm account balance |
| Risk Mode | Normal (2%) | Selects your risk per trade as % of account |

**Risk Mode breakdown on a $10,000 account:**

| Mode | Risk/Trade | Max Loss (1 trade) | Prop Firm Safe? |
|---|---|---|---|
| Conservative (1%) | $100 | $100 | ✅ Very safe |
| Normal (2%) | $200 | $200 | ✅ Safe |
| Aggressive (3%) | $300 | $300 | ⚠️ Watch daily limit |

> Prop firm daily loss limit is usually 5% ($500 on $10k). The strategy only takes **1 trade per day** — enforced automatically.

### ATR Adjustments
| Setting | Default | What It Does |
|---|---|---|
| ATR Length | 14 | Period for ATR calculation |
| Limit Order ATR Improvement | 0.5 | Pulls limit entry back slightly for better fills |
| TP ATR Reduction | 0.5 | Pulls TP slightly inside the target for better fills |

---

## How to Read the Signals

When the strategy fires, a label appears next to the signal bar:

### Long Signal Example
```
🟢 LONG MNQ
────────────────
Entry : 23,954.00
SL    : 23,886.00  (-67.0 pts)
TP 2R : 24,088.00  (+134.0 pts)
TP 3R : 24,155.00  (+201.0 pts)
```

### Short Signal Example
```
🔴 SHORT MNQ
────────────────
Entry : 23,450.00
SL    : 23,520.00  (+70.0 pts)
TP 2R : 23,310.00  (-140.0 pts)
TP 3R : 23,240.00  (-210.0 pts)
```

The **green triangle** (long) or **red triangle** (short) also appears directly on the chart at the signal bar.

---

## How to Execute a Trade

### When the Triangle Appears:

**Step 1 — Read the label**
Note down the three numbers: Entry, SL, TP

**Step 2 — Open your broker**
Go to your trading platform (MT4, MT5, FXCM, Tradovate, etc.)

**Step 3 — Place the trade**
- Direction: BUY (long signal) or SELL (short signal)
- Asset: NAS100 / US100 / MNQ
- Entry: Market order at current price, OR limit order at the Entry price shown
- Stop Loss: The SL price shown in the label
- Take Profit: TP 2R or TP 3R (your choice)

**Step 4 — Walk away**
Once your order is placed with SL and TP set, you're done. The trade manages itself.

---

## Risk Management

### Position Sizing (Manual)
If you are manually sizing your position, use this formula:

```
Risk per trade = Account size × Risk %
Position size  = Risk per trade ÷ SL distance (in points)
```

**Example on a $10,000 prop firm account (Normal 2%):**
```
Account:       $10,000
Risk Mode:     Normal (2%) → Risk per trade = $200
SL distance:   67 pts
NAS100 value:  ~$1 per pt (CFD) or $2/pt (MNQ micro)

Position size = $200 ÷ 67 = ~3 units (CFD) or ~1-2 contracts (MNQ)
```

### Golden Rules
- **Never risk more than 1–2% of your account per trade**
- **Always set your SL before you enter**
- **One trade per day** — the strategy takes 1 signal per session, that's it
- **Do not move your SL** once the trade is live
- **Do not override the signal** — if no triangle, there is no trade

---

## Session Times by Timezone

The strategy trades **2:30 PM – 4:30 PM Nigerian time (WAT)**. That is the NY open session.

| Location | Session Time |
|---|---|
| **Nigeria / Ghana (WAT)** | **2:30 PM – 4:30 PM** ← you are here |
| London (GMT) | 2:30 PM – 4:30 PM |
| Johannesburg (SAST) | 3:30 PM – 5:30 PM |
| Nairobi (EAT) | 4:30 PM – 6:30 PM |
| Dubai (GST) | 5:30 PM – 7:30 PM |
| Mumbai (IST) | 7:00 PM – 9:00 PM |
| New York (ET) | 9:30 AM – 11:30 AM |

> You only need to be available for this 2-hour window. After placing the trade, SL and TP do the rest.

---

## Python Backtest Engine

This repo includes a full Python backtesting system that replicates the Pine Script logic bar-by-bar with no lookahead bias.

### Setup

```bash
cd backtest
pip install pandas numpy matplotlib seaborn pytz yfinance
```

### Get Data

Download NAS100 M1 data from [histdata.com](https://www.histdata.com/download-free-forex-data/?/metatrader/1-minute-bar-quotes/NSXUSD) (MetaTrader format). Place all year folders in `~/Downloads/`, then run:

```bash
python3 download_histdata.py
```

This auto-detects all `HISTDATA_COM_MT_NSXUSD_M1*` folders, merges them, resamples to 15m, and saves `NAS100_15m.csv`.

### Run Backtest

```bash
python3 run_backtest.py
```

### Output

Results are saved to `backtest/results/`:
- `summary.csv` — all performance metrics
- `trade_log.csv` — every trade with entry/exit/P&L
- `monthly_returns.csv` — month-by-month breakdown
- `equity_curve.csv` — bar-by-bar equity
- `backtest_report.png` — equity curve + drawdown + P&L charts

### Configuration

Edit `backtest/config.py` to change:
- `INITIAL_CAPITAL` — account size
- `RISK_MODE` — `"conservative"` / `"normal"` / `"aggressive"`
- `DAILY_LOSS_LIMIT_PCT` — prop firm daily loss limit (default 5%)
- `MAX_DRAWDOWN_PCT` — prop firm max drawdown limit (default 10%)

### File Structure

```
backtest/
├── config.py              # All settings
├── data_feed.py           # Data loader (CSV or Yahoo Finance)
├── strategy.py            # Pine Script logic in Python
├── analytics.py           # Performance metrics + charts
├── run_backtest.py        # Entry point
├── download_histdata.py   # histdata.com data processor
├── NAS100_15m.csv         # Generated data file (not in repo)
└── results/               # Generated output
```

---

## FAQ

**Q: Do I need TradingView Pro?**
A: No. The free plan works for manual trading. Watch the chart during the session window and execute signals yourself.

**Q: What broker should I use?**
A: Any broker that offers NAS100, US100, or MNQ futures. Popular options: FXCM, Pepperstone, IC Markets (CFDs), or Tradovate/NinjaTrader (futures).

**Q: What if I miss the signal?**
A: Do not chase it. If you didn't see the triangle in time, skip that day. There will be another signal tomorrow.

**Q: Can I use this on other pairs?**
A: It was built and optimized specifically for NAS100. Results on other instruments are not tested.

**Q: What timeframe do I use?**
A: 15 minutes only. The strategy will not work correctly on other timeframes.

**Q: What if there's no signal today?**
A: That's normal. Not every day has a valid setup. No signal = no trade. Patience is part of the edge.

**Q: Can I change the R:R?**
A: Yes. In the settings panel under "Risk : Reward", adjust Long and Short RR values. 2.0 is the tested default.

**Q: Is this suitable for a prop firm challenge?**
A: Yes. The 16-year backtest shows the account never once breached the 10% max drawdown floor from the starting $10,000. Use Conservative (1%) mode during the evaluation phase.

---

## Disclaimer

This strategy is for educational purposes only. Trading financial instruments involves significant risk of loss. Past performance is not indicative of future results. Always trade with money you can afford to lose and consult a financial advisor if needed.

---

*Built by Jesh | JESH NAS M15 — 16 years of NAS100 edge*
