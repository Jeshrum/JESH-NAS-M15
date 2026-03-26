# JESH NAS M15 — NAS100 Opening Range Breakout Strategy

> A disciplined, rules-based 15-minute ORB strategy for NAS100 (US100/MNQ).
> Trades the NY open session only. No indicators. No guessing. Just levels.
> **Nigerian time: 2:30 PM – 4:30 PM WAT**

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
9. [Strategy Performance](#strategy-performance)
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

The strategy also uses **ICT liquidity sweep filters** — it only takes longs if the previous day's low was swept first, and shorts if the previous day's high was swept. This removes low-quality setups and dramatically improves win rate.

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
- All positions are force-closed before 10:00 PM Nigerian time / 5:00 PM NY time (no overnight holds)

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

### Risk : Reward
| Setting | Default | What It Does |
|---|---|---|
| Long Risk:Reward | 2.0 | TP = Entry + (SL distance × 2) |
| Short Risk:Reward | 2.0 | TP = Entry − (SL distance × 2) |

> You can change these to 1.5, 2.5, 3.0 — experiment with what suits your style.

### Position Sizing
| Setting | Default | What It Does |
|---|---|---|
| Position Size Type | Risk-Based | Calculates contracts based on dollar risk |
| Risk Amount ($) | $300 | How much USD you risk per trade |

> Risk-Based sizing automatically sizes your position so that if SL is hit, you lose exactly $300 (or whatever you set).

### ATR Adjustments
| Setting | Default | What It Does |
|---|---|---|
| ATR Length | 14 | Period for ATR calculation |
| Limit Order ATR Improvement | 0.5 | Pulls limit entry back slightly from breakout for better fills |

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

**Example:**
```
Account: $5,000
Risk %:  2% → Risk per trade = $100
SL distance: 67 pts
NAS100 point value: ~$1 per pt (CFD) or $2/pt (MNQ micro)

Position = $100 ÷ 67 = ~1.5 units (round down to 1)
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

## Strategy Performance

Backtested on **NAS100 / US100 (15-minute), Jan 2026 – Mar 2026**

| Metric | Value |
|---|---|
| Total Trades | 49 |
| Win Rate | 55.10% |
| Profit Factor | 2.155 |
| Total P&L | +$3,100.32 |
| Max Drawdown | $795.77 (0.52%) |
| Initial Capital | $150,000 |

> Past performance does not guarantee future results. Always use proper risk management.

---

## FAQ

**Q: Do I need TradingView Pro?**
A: No. The free plan works for manual trading. You just watch the chart during the session window and execute signals yourself.

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

---

## Disclaimer

This strategy is for educational purposes only. Trading financial instruments involves significant risk of loss. Past performance is not indicative of future results. Always trade with money you can afford to lose and consult a financial advisor if needed.

---

*Built by Jesh | Powered by Roboquant.ai Pine Script engine*
