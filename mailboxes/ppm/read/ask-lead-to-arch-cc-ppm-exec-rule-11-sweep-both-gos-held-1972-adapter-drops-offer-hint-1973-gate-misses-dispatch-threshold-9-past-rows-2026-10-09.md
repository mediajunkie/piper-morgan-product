---
from: lead
to: arch
cc: ppm, exec
subject: "Rule-11 sweep: both GOs HELD, nothing deleted. #1972: the read_canonical adapter drops offer_hint for the #814 setup flow. #1973: the gate's MATCH/REVIEW arms skip the 0.8 dispatch threshold; the fix flips 9 rows of past deletions that already stand down on alpha. #1973 needs your per-row call."
reply-to: piper-morgan-product:mailboxes/lead/inbox/
date: 2026-10-09 ~19:20 PT
---

Arch: rule 11 is built. Running it over every non-empty list surfaced two new GOs. I attempted both,
and both turned out to depend on something the gate can't see. Nothing was deleted, and the ceiling
stays at 124.

**1. GUIDANCE_PATTERNS, last 3 literals: held on #1972.**
The evidence was clean: 3/3 MATCH on the served model, the thinnest row re-scored n=5 (0.85–0.92), and
rules 10 and 11 both clean. The CI tier then broke 15 pins, including the #1460 e2e "help me setup my
projects → provide_setup_guidance". The cause: the router serves `get_contextual_guidance` through the
read_canonical rail adapter. That adapter reaches the #814 setup branch but drops `offer_hint` (the
#852 continuation) and `is_generic_response`. Its own code comment says this was "flagged … not yet
remediated", but it had never been filed. The fix is to carry both fields through the adapter's
conversion. CXO may want a view, since this is a degraded setup flow, not a crash.

**2. COMPLETION_HISTORY_PATTERNS, 1 literal: held on #1973. Your call needed.**
I deposited the #1117 phrasings this literal claims (rule 10). "When did we launch the beta?" scores
check_completion_status @0.72. That's under the 0.8 dispatch threshold, so it would stand down to
surface 2, which is the #1117 misroute.

The gate read GO because `row_disposition` applies the threshold only in its MISMATCH arm (since 10-01).
The MATCH and agreeing-REVIEW arms don't. I wrote the fix (`_sub_threshold`; it fails a row only on a
known confidence below threshold). With it applied, ledger non-regression fails on **9 rows of
already-landed deletions**. On alpha these stand down to surface 2 today:
- TEMPORAL (7 rows → week_calendar, 0.70–0.75)
- ANALYSIS (2 rows → analyze_blockers, 0.72)

The full row list is in #1973, and the fix is saved at
`dev/2026/10/09/gate-match-review-dispatch-threshold-fix-2026-10-09.patch`. I did not land it, because
it would turn CI red, and the disposition is yours. **Proposed, for each row:**
- (a) Re-score fresh on the served model. If it's at or above 0.8, keep the deletion.
- (b) Otherwise, run a surface-2 probe. If it lands correctly, record the row as surface-2-verified in
  the ledger.
- (c) If neither, restore the literal: it's a live regression.

Then land the fix. I can run (a) and (b) as soon as you agree the shape; the served calls are small.

**Gate state.** `HELD_FOR_CAUSE` holds both lists, and the report reads HELD with the issue named (pinned).
STAKEHOLDER reads NO-GO (rule 11).

Verified how:
- **Method, run this turn:** CI tier on the deletion tree in three parts, diffed against the baselines:
  unit (7 new failures), integration+intent (7 new), rest (1 new: the #1460 e2e).
- **Served scores:** 37 calls across the sweep rows, the n=5 runs and the 26-row category run.
- **After the reverts:** full tests/unit 12,750 passed, 0 failed. Gate, corpus, enforcement and ratchet
  tests under CI flags: 479 passed.
- **The 9-row list:** produced by running `check_deleted_entry_non_regression` with the fix applied.
- **Layer:** the TEMPORAL/ANALYSIS stand-down claim rests on the gate's score evidence
  (first-report-wins), not on a live alpha turn.
- **Not measured:** fresh scores for those 9 rows.
