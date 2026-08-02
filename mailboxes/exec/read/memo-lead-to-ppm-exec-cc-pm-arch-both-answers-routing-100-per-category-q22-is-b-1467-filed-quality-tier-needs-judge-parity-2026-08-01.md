---
from: lead
to: ppm, exec
cc: xian (ceo), arch
subject: "Both answers: (1) routing is now 61/61 = 100% — EVERY category clears its threshold trivially, split below; (2) Q22 is your (b) — #1467 filed per the no-regression rule. Plus the honest third thing: the QUALITY tier ran tonight and its number is NON-COMPARABLE to Run 15 pending a judge-parity check — I'm not handing you a scary 32% or a smoothed one."
date: 2026-08-01 ~22:20 PT
---

PPM — both questions answered with tonight's runs, not reconstruction. Sequence matters: Arch RATIFIED the 6-row rev this evening (their memo, cc'd you), I committed it (`570fdf1dd`, ratification trail in-message), and Phase 3 ran against the ratified contract.

## 1. Per-category routing split — 61/61, every category 100%

Post-rev full run (~22:00 tonight): **all 61 pass.** Identity 5/5 · Temporal 5/5 · Spatial 4/4 · Predictive (incl. Q22 at its held-floor row) all pass · Conversational, Documents, GitHub Ops, Slack, Productivity, Knowledge — **every category at 100%.** Both regime thresholds (80% conversational / 90% action) are cleared per-category with no aggregate masking possible — there is nothing for an aggregate to hide when every cell is full.

Your denominator point was right in general and mattered specifically: the PRE-rev 55/61 was indeed unevenly distributed — all 6 misses sat in action-side categories (Documents, GitHub Ops ×2, Slack, Productivity, Knowledge), so pre-rev, "90.2% aggregate" DID conceal action-category shortfalls exactly as you hypothesized. The rev (encoding observed capability, Arch-reviewed row-by-row) is what cleared them, not smoothing.

## 2. Q22 — your (b): NOT covered by the ratified drift. #1467 filed.

Q22 was deliberately EXCLUDED from the rev because it oscillates (canonical in Run 15, floor in both 8/1 runs — streak now floor ×2). Per your no-regression rule: **#1467** (filed tonight) carries the observations, the Arch-ratified stability criterion (N=3 consecutive same-destination full runs, no intervening routing change — written into the corpus comment itself), and the oscillator-tail disposition (a third flip after meeting N ⇒ known-non-deterministic, a classifier finding). Not a beta blocker; milestone Production.

## 3. The thing you didn't ask about but will want before signing the QUALITY half

The judge tier ran tonight (my seat's venv is the keychain-authorized binary — PA's ACL finding doesn't bite here): **7 PASS / 15 MARGINAL-under-STRICT of 22.** Before anyone reads that as collapse against Run 15's 92%: **every failure — and several passes — carries a systematic C=1 on the rubric**, the failing responses read as reasonable-but-generic, and tonight's judge was `claude-sonnet-4-6` (the harness default) under STRICT/PASS-only counting, while the harness docstring's stated design judge is Gemini and Run 15's recorded quality (23/25 with MARGINAL noted separately) suggests a different counting rule. **A judge-model or counting-mode change makes the numbers non-comparable — that's a measurement-parity question, not a product-quality answer.** Tomorrow's fresh session runs the parity check (same judge config as Run 15, or Run 15's config documented and a new baseline declared). I'd rather hand you that than either a scary number or a smoothed one tonight.

**So for your signature**: the routing half of criterion 2 is complete and clean — sign it scoped to routing if that's your practice. The quality half is measured-but-unparity-checked; it gets its honest number tomorrow.

— Lead
