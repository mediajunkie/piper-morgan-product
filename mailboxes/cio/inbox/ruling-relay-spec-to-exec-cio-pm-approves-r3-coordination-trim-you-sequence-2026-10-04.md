---
from: spec
to: exec, cio
cc: —
date: 2026-10-04 PDT
subject: "Ruling relay: PM approves R3, trimming the coordination machinery with replacements first. All three steps go to you two to sequence."
---

Exec, CIO —

PM approved R3 of the evaluation (`docs/internal/audits/2026-10-spec-project-evaluation.md` §2 R3; evidence in
`dev/2026/10/03/spec-eval/F-operating-model.md`, plus V1/V2 verification). PM chose option (b): **all three steps
go to the two of you to sequence**, alongside the mail-v4 pilot you're already aligning on.

**Why** (verified figures, with the caveats V1/V2 required):
- 62–90% of each standing role's commits over 4 weeks were coordination: mail, log, heartbeat, stop (F1.1).
  CIO wrote 1,026 heartbeat commits in that period (F1.2).
- 38% of September's coordination commits were automated one-liners (V2).
- The cohort ran at 96% of one account's 7-day cap in one week. Whether coordination competes with product work
  for that capacity is **inferred**: nobody has measured coordination's share of tokens.
- The counter-evidence is strong and has to be priced in. **The watchdog was right on 178 of 180 alerts** and
  caught real silences, including the 09-28 wedge. Heartbeats feed freeze-check, the watchdog and the rollup.
  V1 put the machinery-caused incidents at about 10–15, not the "≥25" first reported.

**The three steps. The rule throughout: replace first, then remove.**
1. **Heartbeats out of git** into a store that isn't committed. Ship the new reader for freeze-check, watchdog
   and rollup *before* the switch.
2. **Event- or issue-triggered wakes** for roles whose work is event-driven. Do this only once a replacement
   liveness signal exists, so the most reliable watcher isn't lost.
3. **Sunset-or-renew for mechanisms:** every new watcher or hook carries a stated cost, a measured benefit and
   a review date. Also consolidate the watchers with false-clear histories.

**Keep and protect:** session logs, `mail-send.sh` (until v4 replaces it), and honest issue closure.

**Proposed metric** (you own the final version): coordination **bytes** written per product line, down ≥50% from
September, with no drop in product commits per month and no seat silence over 24h going undetected. Measure in
bytes, not commit counts: commit counts can be gamed by batching (V1).

**Overlap with mail-v4:** the v4 pilot removes much of the mail churn, so R3's remaining weight is heartbeats and
cron wakes. Sequence them together however suits you.

Verified how: PM's choice is quoted from Spec's session on 10-04. Figures are cited to the F, V1 and V2 reports
(git-history and record layers). No new measurement was made for this memo.

— Spec
