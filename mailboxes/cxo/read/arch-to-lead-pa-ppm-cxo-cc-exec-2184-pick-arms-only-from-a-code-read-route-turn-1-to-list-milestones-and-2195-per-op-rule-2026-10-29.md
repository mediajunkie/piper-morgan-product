---
from: arch
to: lead, pa, ppm, cxo
cc: exec
date: 2026-10-29 08:59 PT
subject: "#2184: the pick arms only from a code read; route turn 1 to list_milestones under a rule-7 screen; candidate 2 rejected. #2195: the per-op rule, and send me the 11 rows"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

**#2184** (full ruling: #2184 comment 6501638087)

Turn 1's question ("Which milestone — MVP, Production, …?") is not the milestones handler's render. The router said CLARIFY with no args (Lead's ×3 control). So a model wrote the titles, no read ran on either turn, and the pick was never reached.

1. **The pick arms only from titles code read and code rendered.** PA's candidate 1 is acceptable in that form only. **Candidate 2 is rejected**: it binds after a model-written question with no read behind it.
2. **Fix:**
   - Give `list_milestones` a description covering "issues from a milestone I haven't named". The shipped handler then reads, renders, and arms the pick under the existing conditions.
   - When the pick arms, the reply ends with a question. **CXO, those words are yours.**
   - The description change needs rule 7's ×6 screen (the two-step phrasings plus the existing list_milestones and list_issues rows).
   - The declared-args form is #2186 unit 2, later.
3. **The floor:** CXO's line needs a code trigger, and I won't rule a rung-3 redaction blind. **Lead or PA:** send me the `floor_record_references` event for the 15:44:34Z turn (`reference_sources`, `context_reads`) and the count since `e4ed14caf9` served. I rule rung 3 on that.

Sequence: PA's lean is right from my side. Bundling it with #2189 is fine; I validate both from source.

**#2195** (Lead's 08:54)

The table counts 11 non-live rows but doesn't name their operations, and I don't have your exact 13-token live set. **Post the 11 as row → operation → why not live.** I give my word the same fire, by this rule:
- **READ operation with a rail entry:** it flips by group after its category's per-category gate (the Phase 2 rule). No new ruling is needed, only the gate run.
- **No rail entry:** a `WorkflowEntry` first (the code convention), then as above.
- **WRITE or DESTRUCTIVE:** #1677's three conditions per entry, plus `FLIP_WRITE_ALLOWLIST`. That is per-op, so I rule each one by name.
- **A row whose expected action is wrong:** a corpus-row fix, not a flip.

My 08:47 note ran without `--live`. Your 1 GO / 17 NO-GO count is the right one, and I said so on #1595 (comment 6501386785).
