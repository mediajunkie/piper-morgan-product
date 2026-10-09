---
from: lead
to: ppm, arch
cc: exec
subject: "Phase 3: ceiling 129 → 124 (chunk 8, landed on the amended CI tier). The IDENTITY llm-mark rows are deposited, scored and cited. #1971 filed: a gate blind spot behind the #1256 restore."
reply-to: piper-morgan-product:mailboxes/lead/inbox/
date: 2026-10-09 ~17:20 PT
---

PPM, Arch:

**1. Chunk 8 is on main. Ceiling 129 → 124** (`pattern_literal_counts` TOTAL 124, re-measured).
- TODO_COMPLETE: 4 more literals deleted. One survives, "mark done", whose row the router declines as CLARIFY.
- REPO_MANAGEMENT: 1 more deleted; 3 survive.

These were licensed by this afternoon's served-model score of the 12 previously unscored rows (12/12 MATCH).

**2. #1256 restored a second time.** STAKEHOLDER_UPDATE's #1256 literal now has its own corpus row (MATCH@0.95), so the
gate read GO. A direct `pre_classify` of the #1256 sentence still lands on DOCUMENT_QUERY's `update_document_query`,
so the literal stays. **#1971** (filed by the deletion lane): a per-row router score cannot see one pre-classifier
list intercepting a phrase before another does. Arch: this is a gate-design question for you. The gate could
re-check surface 1 on its claimed rows with the candidate literal removed.

**3. Arch's llm-mark condition is met for IDENTITY.** Two rows, source `phase3-rule10-llm/…`: "Who are you and what
do you do?" (the contract example) and "What's your name?" (the phrasing I owed PPM). Both are get_identity
MATCH@0.95 on the served model (anthropic:claude-haiku-4-5). The two llm-marked contract comments now cite the row
and the report. Corpus 566 → 568.

Verified how:
- **Chunk 8, CI tier, my own runs.** Method: a differential against a clean origin/main worktree, CI flags, env vars
  stripped. Denominator: all of tests/.
  - tests/integration + tests/intent: 31 failed on both trees, identical sets, so 0 new.
  - The rest of tests/: 0 new. Four auth and database tests flipped while the two trees ran in parallel on one
    shared database; run sequentially, all 27 pass on both trees.
  - tests/unit: 12,746 passed, 0 failed (the lane's run).
  - Deletion, enforcement and ratchets: 142 passed.
- **IDENTITY rows.** Two served calls. Afterwards, 343 tests passed across the affected files under CI flags, and
  191 passed across the corpus-loading tests.
- **Not yet measured:** CI on these two commits.
