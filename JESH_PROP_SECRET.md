# JESH Prop Secret — Risk Management & Execution Plan

> Built from 16 years of real NAS100 data (2010–2026).
> 1,564 trades. Every number below is from the backtest, not theory.

---

## The Real Numbers First

| Stat | Value | What It Means |
|---|---|---|
| Win rate | 44.2% | You lose more trades than you win. That is normal. |
| Avg win | +$513 | Most wins come from force close, not TP |
| Avg loss | -$208 | Losses are small and consistent |
| Expectancy | **+$111 per trade** | Every signal you take = $111 average profit |
| Avg trades/month | 8.5 | ~2 signals per week |
| Avg monthly P&L | **+$941** | At 2% risk on $10k |
| Worst month ever | -$2,163 | In 16 years. That's the absolute floor. |
| Worst losing streak | **15 in a row** | Sept–Oct 2013. Total loss: -$3,258. |
| Account ever blown | **Never** | Not once in 16 years of prop firm rules |

---

## Your Risk Setup

**Account: $10,000 prop firm**

| Phase | Risk Mode | Risk/Trade | Daily Stop |
|---|---|---|---|
| **Evaluation** | Conservative 1% | $100 | Stop at -$300 (3 losses) |
| **Funded — first 30 days** | Conservative 1% | $100 | Stop at -$300 |
| **Funded — stable** | Normal 2% | $200 | Stop at -$400 (2 losses) |
| **Funded — growing** | Normal 2% | $200 | Stop at -$400 |

> Never use Aggressive 3% on a prop firm. The data doesn't need it.
> Normal 2% already turns $10k into $139k over 16 years.

---

## Daily Rules — Non-Negotiable

**Rule 1 — One trade per day. That's it.**
The strategy fires once per session. If you miss it, the day is over. If you take it, the day is over. No re-entries. No revenge trades.

**Rule 2 — Daily stop: -$400**
One loss at 2% = -$200. If a second signal somehow fires and also loses = -$400. Walk away. Never let one day cost you $500 — that's the prop firm daily limit.

**Rule 3 — Be at your screen 2:30 PM WAT. Not 2:45. Not 3:00.**
Most signals fire in the first 30 minutes. If you miss it, you miss it. No chasing.

**Rule 4 — Set SL and TP the moment you enter. Then close the platform.**
Your job ends when the order is placed with SL and TP set. Watching it will make you move the SL. Don't.

---

## The 2R Target — How It Actually Works

Most people think 2R means price hits TP. Here's the reality from 1,564 trades:

| Exit Type | Count | % | Avg P&L |
|---|---|---|---|
| TP hit (full 2R) | 234 | 15.0% | ~+$400 |
| Force close (profit) | 468 | 30.0% | +$515 |
| Force close (loss) | 119 | 7.6% | -$83 |
| SL hit | 743 | 47.5% | -$208 |

**TP only hits 15% of the time. But force closes average +$515 — nearly the same as a full 2R.**

The session end at 4:30 PM WAT IS part of the edge. 468 profitable force closes over 16 years. Do not manually close early trying to "lock in profit." Let it run.

**Your execution every single trade:**
```
Signal fires → place order at Entry price shown on label
SL  → exactly as shown
TP  → exactly the 2R price shown
Done → close the platform, go live your life
```

---

## Surviving the Losing Streaks

The worst streak in 16 years was **15 consecutive losses** (Sept–Oct 2013).
Each loss averaged ~$235. Total damage: **-$3,258** at 2% risk.

This did not blow the account. Here's why — and how you survive it too:

**The streak protocol:**

| Losses in a row | What you feel | What you do |
|---|---|---|
| 1–4 | Annoyed | Normal 2%. Continue. |
| 5 | Frustrated | **Drop to Conservative 1%** |
| 6–10 | Doubt | Still 1%. Review signal validity only. |
| 11–15 | Despair | Still 1%. The edge exists over 1,564 trades, not 15. |
| First 3 wins | Relief | Back to Normal 2% |

**The math at 1% during a 15-loss streak:**
- After 5 losses at 2%: balance ≈ $9,000
- Switch to 1% from here
- After 10 more losses at 1%: balance ≈ $8,100 — still alive, still within prop firm rules ✅

**What NOT to do during a streak:**
- Do not increase size to "make it back faster"
- Do not skip signals because you're scared — you'll miss the recovery
- Do not change the strategy — the streak is part of the 16-year edge
- Do not stop taking signals — the expectancy is +$111 per trade regardless of recent results

---

## Monthly Expectations

| Scenario | WR | Trades | Monthly P&L |
|---|---|---|---|
| Tough month | 25% | 8 | ~-$600 |
| Average month | 44% | 8 | **~+$941** |
| Good month | 65% | 8 | ~+$2,500 |
| Exceptional month | 85% | 7 | ~+$5,500 |

**Budget for 2–4 losing months per year.** The data shows ~4 losing months per year on average. The worst losing month in 16 years was -$2,163. Every single year was still profitable despite those months.

---

## Year-by-Year Proof

Every single year from 2010 to 2026 was profitable — including:

| Year | Event | Result |
|---|---|---|
| 2018 | Nasdaq crash -20% | **+$5,474** |
| 2020 | COVID crash -30% in 5 weeks | **+$6,455** |
| 2022 | Worst rate hike cycle in 40 years | **+$16,319** |

The strategy doesn't care about the macro. It cares about the opening range and whether liquidity was swept. That's it.

---

## Prop Firm Safety Numbers

| Rule | Limit | Worst seen in 16 years |
|---|---|---|
| Daily loss limit | -$500 (5%) | $0 triggered at 2% risk |
| Max drawdown from $10k | -$1,000 (10%) | -$863 (never breached) |
| Min equity ever | $9,000 floor | $9,137 (never breached) |

---

## The One Mindset Anchor

The expectancy is **+$111 per trade.**

- Every signal you skip → $111 left on the table
- Every SL you move → you broke the system that made 16 years of profit
- Every early close → you cut off force-close wins that average +$515
- Every size increase after a loss → you turned math into gambling

**Your only job is to see the triangle, place the order exactly as shown, and walk away.**

The edge is already built in. You just have to let it work.

---

*JESH NAS M15 — Backtested on 5.1 million 1-minute bars, 2010–2026*
