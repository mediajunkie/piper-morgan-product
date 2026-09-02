---
last_updated: 2026-09-01
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — rewritten 2026-09-01 at the 22:17 STOP (frontmatter is the checkable claim; this
prose line is not, and must not be trusted over it).

## 🔴 NEXT FIRE (09-02 START) — nothing owed on a clock.

**First move, and it is now evidence-backed rather than a hunch**: ⚠️ **re-verify every "blocked on X"
row before trusting it.** On 09-01 **five of nine rows were stale within 36 hours of a clean rebuild** —
each blocker had cleared and the row hadn't. `aging-standing-items.sh` **structurally cannot see this**
(the rows are recently dated *and* carry a stated blocker — exactly what healthy looks like to it).
Proposed to CIO as a third mechanism, **stale-blocker rot**, with the five instances.

**Standing pickup if idle**: run `scripts/aging-standing-items.sh`, then **check each blocker by hand
anyway** — the check covers deferral, not this.

## ⚠️ Instrument state — read before scoring anything

- **CT rubric v2.3.5.** Three invariants **PM-ratified 08-31** (question · verdict shape · fabrication
  auto-fail) — changing those needs PM; criteria/examples/branches stay CXO-editable.
- **C-axis**: corpus carries `context_requirement`. Report **per bucket, never pooled.**
  `not_applicable` (10 of 61) = **full marks at C=2, do not dock.** The C=2-clustering diagnostic applies
  to the **`required` bucket only** (49 of 61).
- 🔴 **BYOC Recomposition Rubric is v0.4**, and **T scores ADDITION as well as survival** — the observed
  failures were the host *adding* claims (scope leak; unverified reassurance), not losing them. Still
  `PENDING-PROBE`: it can inform design, **it cannot close a Layer-B gate on T.**
- ⭐ **Three of my predictions were falsified this week** — *structure beats prose*, *directives beat
  descriptors*, *five directives yield five clauses*. **All three assumed the host executes literally.
  It synthesises.** Carry that bias forward as a known one.

## Live threads (watch only)

- **#1717** — two directives drafted for Lead (scope-leak; unverified-reassurance). MVP, not urgent.
- **#1463 class-discriminator test** (2 calls) — designed, **needs its own PM authorization**, not asked.
- **#1386 · spatial review · Jake loop-back (PM sends) · misfiled-is-not-deferred (Exec watch item)** —
  others' or trigger-based.
- **Voice watch** — re-arms on the next deploy touching floor/decline copy.

## Cron

Job **`8207809c`**, expires **~09-06**. 🔴 **Rotate at the last fire before that** — delete → create →
verify exactly one.
