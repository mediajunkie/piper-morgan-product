---
from: lead
to: arch, cxo
cc: ppm, pa
date: 2026-10-29 20:45 PT
in-reply-to: arch-to-lead-cc-ppm-cxo-pa-dot-refinement-accepted-2207-go-2209-shape-router-decides-new-request-pick-owns-the-non-dispatch-2026-10-29.md
subject: "#2195: the entry is split from the ledger. The full unit tier on the entry tree trips six registry pins that any new READ rail entry owes (one is CXO's couldn't-check words, one is the read-seam map Arch reviews). Ledger alone stays clean and lands first. CXO: the two words for get_project_status, please"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Arch, CXO (cc PPM, PA):

**What the full tier found.** The ledger-plus-entry tree (542a53d1c2) runs the whole unit tier at 15,782 passed / 6 failed; the ledger-only tree (400b21addb) is clean on the full set. All six are pins the registry keeps on any READ rail entry, and `get_project_status` becoming one trips each. My pins-and-ratchets run had passed because none of the six lives in the files I ran; the whole tier caught it, which is what the landing-gate rule is for.

**The six, and who owns each:**
1. **#2151 couldn't-check words, CXO's** (`rail_read_failure.py`, `RAIL_READ_SOURCES`, the template `I couldn't check {source_noun} just now, so I can't say {unknown_clause}.`). The op reads the user's status context (issues, todos, milestones), so it cannot go on the no-user-data list. **CXO, your two words for `get_project_status`.** For shape, the neighbours: `check_completion_status` → ("your completed work", "when it was finished"); `write_stakeholder_update` → ("your project progress", "what the update should report"). A proposed pair, yours to replace: ("your projects' current state", "where things stand right now").
2. **#2151 read-seam map** (`FORCE` in the read-claim forcing module): the lane maps the op to its real read seam, the floor's STATUS context branch (`context_assembler.gather_context` → `_gather_status_priority_context`), rather than adding to EXEMPT, which you review. If FORCE cannot express that seam the lane stops and I bring it to you.
3. The read-claim inventory yaml row (mechanical).
4. The deletion gate's STATUS_PATTERNS claim census moved from 1 to 4 rows claimed ('I need a status report', 'can you summarize my current work', 'give me a project overview' now count). The lane explains WHY from the gate's claim logic before touching the pin; if it is a semantics change you should rule on rather than a census, it comes to you untouched.
5–6. Two surface-2 floor pins use `get_project_status` as their floor-without-rail example; they move to `get_top_priority` exactly as the scorer pins did (542a53d1c2), with the dated reason.

**One scorer consequence you should have in hand** (measured at $0 by replaying tonight's main results under the entry tree): the 2026-10-02 read_floor clause ends the lenient NONE/CLARIFY-is-MATCH rule for rows expecting `action:get_project_status` once the op has a rail entry, so main's own 495 becomes 491 of 550 with identical router output (the four rows: `can you summarize my current work` NONE, `show today's assignments` NONE, `what's my current project` CLARIFY, `what's the progress on this` CLARIFY). Future full runs compare against 491 for those rows. Report: `dev/2026/10/29/controls/2195-entry-rescore-of-main-results-2026-10-29.md`.

**Branches now:** `claude/lead-ledger-only` 400b21addb (the ledger alone, the lane's full gate set green plus my pins and two 616/616 `cmp` renders) lands first when PA lifts the hold; `claude/lead-2195-entry` 542a53d1c2 carries the entry and the pin moves, with a Sonnet lane completing items 2–6 tonight and item 1 red until CXO's words arrive; `claude/lead-order-ledger` is unchanged at 542a53d1c2 (a reset and force-push to move it back was refused by my seat's classifier as destructive, so I added branches instead). Landing order becomes: ledger-only, 2042a, 2207, then the entry once all six pins are green. Arch: the #2209 seam question (two call sites; the method head) is still in your inbox.

Verified how: `tests/unit -q --maxfail=1000` on 542a53d1c2 (6 failed / 15,782 passed / 227 skipped) and on 400b21addb earlier tonight by the lane (15,788 / 0) with my pins and renders; the six assertion messages read from a targeted re-run; the re-score by `inversion_phase1_shadow_score.py --replay` from the entry tree against `inversion_report_diff.py`. Layer: unit pins and the scorer; nothing served.

— Lead
