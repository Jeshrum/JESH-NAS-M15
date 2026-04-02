# JESH NAS M15

> NAS100 Opening Range Breakout | 16-Year Backtest | Prop Firm Ready
> **Timeframe: M15 (15-minute) only**
> **Session: 9:30 AM – 11:30 AM NY · Lagos: 2:30–4:30 PM WAT (summer) · 3:30–5:30 PM WAT (winter)**

---

## Backtest Results (2010–2026)

> All results on the M15 timeframe. Do not use any other timeframe.

![Backtest Report](https://raw.githubusercontent.com/Jeshrum/JESH-NAS-M15/main/images/backtest_report_v2.png)

| Metric | Result |
|---|---|
| Period | Nov 2010 – Mar 2026 |
| Timeframe | M15 (15-minute bars) |
| Initial Capital | $10,000 |
| **Final Balance** | **$37,816** |
| **Net Profit** | **+$27,816 (+278%)** |
| Total Trades | 1,714 |
| Win Rate | **52.8%** |
| Profit Factor | **1.75** |
| Avg R:R | 1.57 |
| Max Drawdown | −10.9% |
| Prop Firm Floor Breached | **Never** |

> Winning combo: Limit Entry + 3R TP + **9:30–11:30 AM NY** (Lagos: 2:30–4:30 PM WAT summer · 3:30–5:30 PM WAT winter) + Sweeps OFF. 1% risk, $0.50 commission/side.

---

## How It Works

**Step 1 — Opening Range**
The first 15-minute candle at **9:30 AM NY (2:30 PM Lagos WAT summer · 3:30 PM Lagos WAT winter)** sets the range. High = long trigger. Low = short trigger.

**Step 2 — Signal fires**
Price closes a 15m candle above the range high (long) or below the range low (short) → triangle appears + entry/SL/TP levels auto-populated on chart.

**Step 3 — Place limit order**
Place a limit order at the First Bar High (long) or First Bar Low (short). Set SL and TP. Walk away.

**Step 4 — Force close**
All positions force-closed before **5:00 PM NY (11:00 PM Lagos WAT)**. No overnight risk.

---

## Setup — TradingView

1. Open **MNQ1!** or **NAS100** chart → set to **M15 (15-minute) timeframe**
2. Pine Editor → paste contents of `JESH_NAS_M15.pine` → Save → Add to chart
3. Open settings → set your Account Size and Risk Mode
4. Be at your screen: **9:30 AM – 11:30 AM NY (Lagos: 2:30–4:30 PM WAT summer · 3:30–5:30 PM WAT winter)**

> Free TradingView plan works. Use MNQ1! (CME) for the most accurate data.

---

## Settings

| Setting | Value | Notes |
|---|---|---|
| Account Size | $10,000 | Your prop firm account |
| Risk Mode | Conservative 1% | $100 max loss per trade on $10k — use during eval |
| Session | 9:30–11:30 AM NY | Lagos: 2:30–4:30 PM WAT (summer) · 3:30–5:30 PM WAT (winter) |
| Entry | Limit order at First Bar High/Low | Never market order |
| Take Profit | 3R | 3× your risk distance |

---

## Execution — Every Trade, Every Time

```
Signal fires → place LIMIT order at level shown
SL  → exactly as shown on label
TP  → 3R level shown on label
Done → close the platform, go live your life
```

**One trade per direction per day. If limit not filled by 11:30 AM NY (4:30 PM Lagos WAT summer · 5:30 PM Lagos WAT winter) → cancelled automatically.**

---

## Session Times

> The strategy always runs on **9:30 AM – 11:30 AM New York (ET)**. Lagos time shifts by 1 hour when US Daylight Saving Time is active (roughly March–November).

| Location | Summer (Mar–Nov) | Winter (Nov–Mar) |
|---|---|---|
| **New York (ET)** | **9:30 AM – 11:30 AM** | **9:30 AM – 11:30 AM** |
| **Nigeria / Ghana (WAT)** | **2:30 PM – 4:30 PM** | **3:30 PM – 5:30 PM** |
| London (GMT/BST) | 2:30 PM – 4:30 PM | 2:30 PM – 4:30 PM |
| Johannesburg (SAST) | 3:30 PM – 5:30 PM | 4:30 PM – 6:30 PM |
| Nairobi (EAT) | 4:30 PM – 6:30 PM | 5:30 PM – 7:30 PM |

> If it's winter and you're in Lagos — your session starts at **3:30 PM**, not 2:30 PM.

---

## Monthly Stats — 2021 to 2026 (1% Risk, $10k Account)

> Each month is independent. P&L and % calculated on a flat $10,000 base at 1% risk ($100/trade). No compounding.

### 2021

| Month | Trades | Wins | Losses | Win Rate | P&L | % |
|---|---|---|---|---|---|---|
| Jan | 7 | 3 | 4 | 42.9% | +$254 | +2.5% |
| Feb | 7 | 3 | 4 | 42.9% | +$1,514 | +15.1% |
| Mar | 13 | 6 | 7 | 46.2% | +$412 | +4.1% |
| Apr | 8 | 4 | 4 | 50.0% | +$770 | +7.7% |
| May | 7 | 2 | 5 | 28.6% | +$377 | +3.8% |
| Jun | 3 | 0 | 3 | 0.0% | −$299 | −3.0% |
| **Jul** | 7 | **6** | 1 | **85.7%** | **+$2,745** | **+27.5%** |
| Aug | 8 | 3 | 5 | 37.5% | +$311 | +3.1% |
| Sep | 6 | 3 | 3 | 50.0% | +$705 | +7.1% |
| Oct | 11 | 6 | 5 | 54.5% | +$1,309 | +13.1% |
| Nov | 10 | 6 | 4 | 60.0% | +$1,924 | +19.2% |
| Dec | 10 | 3 | 7 | 30.0% | +$1,165 | +11.7% |
| **Total** | **97** | **45** | **52** | **46.4%** | **+$11,186** | **+111.9%** |

### 2022 *(rate hike cycle — still profitable)*

| Month | Trades | Wins | Losses | Win Rate | P&L | % |
|---|---|---|---|---|---|---|
| Jan | 9 | 5 | 4 | 55.6% | +$871 | +8.7% |
| **Feb** | 8 | **6** | 2 | **75.0%** | **+$1,449** | **+14.5%** |
| Mar | 7 | 2 | 5 | 28.6% | +$48 | +0.5% |
| Apr | 8 | 3 | 5 | 37.5% | −$188 | −1.9% |
| May | 11 | 3 | 8 | 27.3% | +$233 | +2.3% |
| Jun | 8 | 4 | 4 | 50.0% | −$156 | −1.6% |
| Jul | 3 | 1 | 2 | 33.3% | −$17 | −0.2% |
| Aug | 8 | 5 | 3 | 62.5% | +$1,081 | +10.8% |
| Sep | 8 | 5 | 3 | 62.5% | +$964 | +9.6% |
| Oct | 7 | 4 | 3 | 57.1% | +$1,050 | +10.5% |
| Nov | 6 | 3 | 3 | 50.0% | +$425 | +4.3% |
| **Dec** | 10 | **7** | 3 | **70.0%** | **+$2,196** | **+22.0%** |
| **Total** | **93** | **48** | **45** | **51.6%** | **+$7,956** | **+79.6%** |

### 2023

| Month | Trades | Wins | Losses | Win Rate | P&L | % |
|---|---|---|---|---|---|---|
| Jan | 9 | 6 | 3 | 66.7% | +$1,094 | +10.9% |
| Feb | 6 | 2 | 4 | 33.3% | +$235 | +2.4% |
| Mar | 2 | 1 | 1 | 50.0% | −$20 | −0.2% |
| Apr | 3 | 2 | 1 | 66.7% | +$168 | +1.7% |
| May | 3 | 1 | 2 | 33.3% | −$54 | −0.5% |
| Jun | 8 | 4 | 4 | 50.0% | +$470 | +4.7% |
| **Jul** | 4 | **4** | 0 | **100%** | **+$670** | **+6.7%** |
| Aug | 13 | 5 | 8 | 38.5% | +$929 | +9.3% |
| Sep | 10 | 6 | 4 | 60.0% | +$1,454 | +14.5% |
| **Oct** | 4 | **4** | 0 | **100%** | **+$364** | **+3.6%** |
| Nov | 11 | 6 | 5 | 54.5% | +$575 | +5.8% |
| Dec | 7 | 4 | 3 | 57.1% | −$8 | −0.1% |
| **Total** | **80** | **45** | **35** | **56.3%** | **+$5,878** | **+58.8%** |

### 2024

| Month | Trades | Wins | Losses | Win Rate | P&L | % |
|---|---|---|---|---|---|---|
| Jan | 8 | 4 | 4 | 50.0% | +$710 | +7.1% |
| **Feb** | 13 | **9** | 4 | **69.2%** | **+$1,655** | **+16.6%** |
| Mar | 7 | 5 | 2 | 71.4% | +$947 | +9.5% |
| Apr | 11 | 7 | 4 | 63.6% | +$1,826 | +18.3% |
| May | 12 | 8 | 4 | 66.7% | +$1,389 | +13.9% |
| **Jun** | 12 | 6 | 6 | 50.0% | **+$2,292** | **+22.9%** |
| Jul | 5 | 1 | 4 | 20.0% | +$407 | +4.1% |
| Aug | 11 | 3 | 8 | 27.3% | −$129 | −1.3% |
| Sep | 7 | 3 | 4 | 42.9% | −$62 | −0.6% |
| Oct | 7 | 3 | 4 | 42.9% | +$24 | +0.2% |
| Nov | 7 | 3 | 4 | 42.9% | +$675 | +6.8% |
| Dec | 8 | 2 | 6 | 25.0% | −$392 | −3.9% |
| **Total** | **108** | **54** | **54** | **50.0%** | **+$9,344** | **+93.4%** |

### 2025

| Month | Trades | Wins | Losses | Win Rate | P&L | % |
|---|---|---|---|---|---|---|
| Jan | 7 | 4 | 3 | 57.1% | +$144 | +1.4% |
| Feb | 8 | 3 | 5 | 37.5% | +$233 | +2.3% |
| **Mar** | 7 | 4 | 3 | 57.1% | **+$1,934** | **+19.3%** |
| Apr | 11 | 3 | 8 | 27.3% | +$1,309 | +13.1% |
| May | 12 | 5 | 7 | 41.7% | +$331 | +3.3% |
| Jun | 6 | 4 | 2 | 66.7% | +$254 | +2.5% |
| Jul | 10 | 4 | 6 | 40.0% | +$308 | +3.1% |
| Aug | 8 | 5 | 3 | 62.5% | +$1,255 | +12.6% |
| Sep | 10 | 3 | 7 | 30.0% | +$313 | +3.1% |
| Oct | 6 | 3 | 3 | 50.0% | +$849 | +8.5% |
| Nov | 4 | 2 | 2 | 50.0% | +$436 | +4.4% |
| Dec | 5 | 1 | 4 | 20.0% | −$360 | −3.6% |
| **Total** | **94** | **41** | **53** | **43.6%** | **+$7,006** | **+70.1%** |

### 2026 *(Jan–Mar)*

| Month | Trades | Wins | Losses | Win Rate | P&L | % |
|---|---|---|---|---|---|---|
| Jan | 11 | 5 | 6 | 45.5% | +$1,537 | +15.4% |
| Feb | 13 | 5 | 8 | 38.5% | +$940 | +9.4% |
| Mar | 5 | 1 | 4 | 20.0% | −$40 | −0.4% |
| **YTD** | **29** | **11** | **18** | **37.9%** | **+$2,437** | **+24.4%** |

### 5-Year Summary

| Year | Trades | Win Rate | P&L | % Return |
|---|---|---|---|---|
| 2021 | 97 | 46.4% | +$11,186 | +111.9% |
| 2022 | 93 | 51.6% | +$7,956 | +79.6% |
| 2023 | 80 | 56.3% | +$5,878 | +58.8% |
| 2024 | 108 | 50.0% | +$9,344 | +93.4% |
| 2025 | 94 | 43.6% | +$7,006 | +70.1% |
| 2026 (Jan–Mar) | 29 | 37.9% | +$2,437 | +24.4% |

---

## Python Backtest Engine

Full bar-by-bar Python backtest replicating the Pine Script logic. No lookahead bias.

```bash
cd backtest
pip install pandas numpy matplotlib seaborn pytz
python3 download_histdata.py   # process histdata.com M1 data
python3 run_backtest.py        # run full backtest
```

Get NAS100 M1 data from [histdata.com](https://www.histdata.com/download-free-forex-data/?/metatrader/1-minute-bar-quotes/NSXUSD). Place year folders in `~/Downloads/` before running.

Edit `backtest/config.py` to change account size, risk mode, or prop firm limits.

---

## FAQ

**Do I need TradingView Pro?** No. Free plan works.

**What chart symbol?** MNQ1! on CME (most accurate). NAS100 or US100 also work.

**What if I miss the signal?** Skip the day. Never chase. Another signal comes tomorrow.

**What timeframe?** M15 (15 minutes) only. Any other timeframe gives wrong signals.

**What broker?** Any that offers NAS100/MNQ. Tradovate, Pepperstone, IC Markets, FXCM.

**Is it prop firm safe?** Yes. Never breached the 10% max drawdown floor in 16 years. Use 1% risk during evaluation.


*JESH NAS M15 — Built by Jesh | 16 years of NAS100 edge | 354,006 bars backtested*

> Trading involves significant risk. Past performance does not guarantee future results.
