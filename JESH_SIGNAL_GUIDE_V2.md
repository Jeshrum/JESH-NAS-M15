# JESH NAS M15 — Signal Guide V2
> Quick reference for reading and acting on every signal

---

## Signal Types

### ▲ LONG SIGNAL
**What it looks like on chart:**
- Green triangle below the bar
- Signal card appears: "▲ LONG · NAS100"
- Shows: Limit Entry | SL | TP (3R)

**What triggered it:**
1. 15m close crossed ABOVE the 9:30 AM First Bar High
2. Previous Day High is above the First Bar High
3. No long trade taken yet today

**What you do:**
1. Do nothing — the limit order is already placed at First Bar High
2. Set your SL alert at First Bar Low
3. Set your TP alert at the 3R level shown
4. Walk away

---

### ▼ SHORT SIGNAL
**What it looks like on chart:**
- Red triangle above the bar
- Signal card appears: "▼ SHORT · NAS100"
- Shows: Limit Entry | SL | TP (3R)

**What triggered it:**
1. 15m close crossed BELOW the 9:30 AM First Bar Low
2. Previous Day Low is below the First Bar Low
3. No short trade taken yet today

**What you do:**
1. Do nothing — the limit order is already placed at First Bar Low
2. Set your SL alert at First Bar High
3. Set your TP alert at the 3R level shown
4. Walk away

---

## Reading the Signal Card

```
▲  LONG  ·  NAS100
Limit Entry   20,000.00
Stop Loss     19,950.00   −50 pts
Take Profit   20,150.00   +150 pts
R:R  1:3.0   Risk $100   Qty 2
```

| Field | Meaning |
|-------|---------|
| Limit Entry | Place your BUY LIMIT order here |
| Stop Loss | Place your STOP LOSS here — never move it |
| Take Profit | Place your TAKE PROFIT here |
| R:R | Risk to reward ratio (3:1 means win 3x what you risk) |
| Risk $ | Dollar amount at risk (1% of account) |
| Qty | Number of contracts to trade |

---

## Signal Outcome Scenarios

### ✅ TP Hit
- Limit filled → price moved in your direction → hit 3R target
- Account up $150–$6,000 depending on size
- No more longs/shorts in that direction today (one TP per direction rule)

### ❌ SL Hit
- Limit filled → price reversed → hit stop loss
- Account down $50–$2,000 depending on size
- Log the trade. No revenge trading. Wait for tomorrow.

### ⏳ Limit Not Filled
- Signal fired but price never pulled back to your limit
- Orders auto-cancelled at 11:30 NY session end
- No loss, no trade. Move on.

### ⏰ Force Closed
- Trade was open but neither TP nor SL hit by 16:55 NY
- Position closed at market price
- Could be a small win or small loss — either is acceptable

---

## Chart Levels Reference

| Level | Color | Meaning |
|-------|-------|---------|
| PDH line (dashed red) | Red | Previous Day High — ceiling for longs to target |
| PDL line (dashed green) | Green | Previous Day Low — floor for shorts to target |
| FB High (dotted orange) | Orange | First Bar High — long entry level |
| FB Low (dotted blue) | Blue | First Bar Low — short entry level |
| Blue background | Blue (faint) | 9:30–11:30 NY active session |
| Red background | Red (faint) | Force close window — no new trades |

---

## Broker / Platform Setup

**TradingView:**
1. Add `JESH NAS M15 — V2 Optimized` strategy to NAS100/US100 M15 chart
2. Set account size to match your prop firm account
3. Set risk mode to Conservative (1%) during evaluation
4. Enable alerts on Long Signal + Short Signal

**Execution (MNQ / NAS100 CFD):**
- Use the limit price from the signal card
- Set SL and TP as bracket orders immediately
- Walk away — do not monitor tick by tick

---

*Signals are generated once per session per direction. If you miss it, wait for tomorrow.*
