# JESH NAS M15 — Daily Playbook
> Backtested 16 Years (2010–2026) · $10k → $37,816 · 52.8% Win Rate · PF 1.75

---

## The One-Line Summary

**Wait for NAS100 to break its 9:30 AM opening range, enter a limit order back at that level, target 3× your risk, close before NY close.**

---

## Non-Negotiable Rules

1. **Only trade 9:30–11:30 AM NY (Lagos: 2:30–4:30 PM WAT summer · 3:30–5:30 PM WAT winter)** — no signals outside this window
2. **Limit orders only** — never chase with a market order
3. **One trade per direction per day** — if your long TP is hit, no second long that day
4. **Force close by 4:55 PM NY (Lagos: 10:55 PM WAT)** — no overnight positions, ever
5. **Cancel all pending orders at 11:30 AM NY (Lagos: 4:30 PM WAT summer · 5:30 PM WAT winter)** — if the limit wasn't filled, move on
6. **Never move your stop loss** — set it and leave it at the First Bar Low/High

---

## Pre-Market Checklist (Before 9:30 AM NY · Lagos: before 2:30 PM WAT summer · 3:30 PM WAT winter)

- [ ] Mark **Previous Day High (PDH)** on chart
- [ ] Mark **Previous Day Low (PDL)** on chart
- [ ] Check economic calendar — avoid NFP, FOMC, CPI days
- [ ] Confirm NAS100 is open (no holiday)
- [ ] Account within prop firm rules (check daily loss limit)

---

## The Setup — Step by Step

### 9:30 AM NY (2:30 PM Lagos WAT summer · 3:30 PM Lagos WAT winter) — First Bar Forms

The 9:30 AM 15-minute candle is your **Opening Range**.
- **First Bar High (FBH)** = top of that candle
- **First Bar Low (FBL)** = bottom of that candle

### After 9:30 AM NY — Wait for the Break

**LONG SIGNAL:**
- Close crosses ABOVE the First Bar High
- Previous Day High must be ABOVE the First Bar High (room to run)
- PDH filter confirms bullish bias for the day

**SHORT SIGNAL:**
- Close crosses BELOW the First Bar Low
- Previous Day Low must be BELOW the First Bar Low (room to run)
- PDL filter confirms bearish bias for the day

### Entry — Limit Order

Do NOT enter at the crossover candle close.
**Place a limit order back at the First Bar High (long) or First Bar Low (short).**
Price usually pulls back to fill you. If it doesn't fill by 11:30 AM NY → cancel it.

### Stop Loss

- **Long:** Stop at First Bar LOW
- **Short:** Stop at First Bar HIGH

Never widen it. Never move it.

### Take Profit — 3R

- **Long TP:** Entry + (Entry − SL) × 3
- **Short TP:** Entry − (SL − Entry) × 3

Example: Entry 20,000 · SL 19,950 · Risk = 50 pts → TP = 20,150

### Force Close

If TP is not hit by **4:55 PM NY (Lagos: 10:55 PM WAT)** → close at market, take whatever is on the table.

---

## Position Sizing by Account

| Account | Risk Mode | Risk/Trade | Notes |
|---|---|---|---|
| $5,000 | Conservative 1% | $50 | Prop firm eval phase |
| $10,000 | Conservative 1% | $100 | Prop firm eval phase |
| $25,000 | Normal 2% | $500 | Funded account |
| $50,000 | Normal 2% | $1,000 | Funded account |
| $100,000 | Normal 2% | $2,000 | Scaling phase |
| $200,000 | Aggressive 3% | $6,000 | Advanced scaling |

**Formula:** Qty = Risk Dollar ÷ (Entry − SL in points)

---

## Prop Firm Rules to Never Break

| Rule | Limit | Your Buffer |
|---|---|---|
| Daily Loss Limit | 5% of account | Never risk more than 1–2% per trade |
| Max Drawdown | 10% of account | Stop trading if down 6% on the month |
| No Overnight Positions | Strict | Force close handles this automatically |
| Consistency Rule | Some firms require it | Never bet more than 30% of profit in one day |

---

## What to Do When Things Go Wrong

**SL hit:** Log the trade. Do not re-enter same direction. Wait for next day.

**Limit not filled by 11:30 AM NY:** Cancel. Do not lower the limit to chase. Move on.

**2 losses in a row:** Reduce risk to 0.5% for next 3 days. Reset.
> Two consecutive losses can be variance — the strategy loses 47.2% of trades by design. But they can also mean you're in a choppy market or your execution is off. Dropping to 0.5% for 3 days keeps you in the game without the emotional pressure of full risk. You stay sharp, the account stays protected, and you reset your psychology before going back to full size. Protecting capital during a cold streak is what separates funded traders from blown accounts.

**SL hit today:** You're done for the day. At 1% risk per trade with one trade per direction, your maximum possible daily loss is −1% (or −2% if both a long and short fill and both stop out). That's by design — this strategy structurally cannot blow a prop firm's 5% daily loss limit in a single session.

**Feeling emotional:** Close the platform. The setup will come back tomorrow.

---

## Scaling Path — $5k to $1M

| Phase | Account | Monthly Target | Strategy |
|---|---|---|---|
| 1 — Eval | $5k prop | Pass challenge | 1% risk, strict rules |
| 2 — Funded | $25k–50k funded | $1,000–2,000/mo | 1–2% risk |
| 3 — Scale | $100k funded | $4,000–6,000/mo | 2% risk |
| 4 — Compound | $200k+ | $10,000+/mo | 2% risk, multiple accounts |
| 5 — Target | $1M managed | Scale into live capital | Proven track record |

**Key:** Don't rush phases. Pass the eval clean. Build the track record. Scale the size.

---

## Daily Trade Journal Template

```
Date        : ___________
Direction   : LONG / SHORT
Lagos Time  : ___________ (2:30 PM WAT summer · 3:30 PM WAT winter)

First Bar High : _______   First Bar Low : _______
PDH : _______   PDL : _______
Entry (Limit)  : _______
SL  : _______   TP : _______
Risk $  : _______   Qty : _______

Outcome : TP / SL / Force Close / Not Filled
PnL     : $_______
Notes   : ________________________________
```

---

*Strategy optimized via 16-year backtest (2010–2026) on NAS100 M15 data.*
*Best combo: Limit Entry · 3R TP · 9:30–11:30 AM NY · Sweeps OFF*
