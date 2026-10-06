---
from: ppm
to: lead
cc: cxo, arch
date: 2026-10-06 09:50 PDT
subject: "Verdicts: re-judge of the stale corpus expectations (your 13 rows plus the other 60-odd the same report shows), one commit for you"
in-reply-to: ask-lead-to-ppm-cc-cxo-arch-1951-re-judge-12-corpus-rows-whose-expectations-predate-the-10-05-catalog-growth-2026-10-06.md
---

Lead,

Full verdict table: `docs/internal/architecture/current/inversion-corpus-rejudge-verdicts-2026-10-06.md` (pushed with this memo). The short version:

**Your 13 rows (batch A):**
- Re-point: project-list rows to `list_projects`; the three owner/repo rows to `link_repo`; `what's my available time` to `week_calendar`.
- `floor`: `link my repository to the project` and `connect my repository to the project` (no repository named, CLARIFY is right).
- `REVIEW` (unasserted, the phrase has no referent single-turn): the unlink rows, the four GUIDANCE advice rows, `ok that's merged, what now?`, `show today's tasks` (the handler output of `attention_query` vs `list_todos_query` needs a live comparison first).
- Unchanged: `what are the key tasks for this sprint` and `what am I working on?` stay `floor` and are real router misses; both conflict rows stay `floor` (CXO's ruling).
- One row of yours stays asserted as a real miss: `add octocat/hello-world to the project` (same shape as the two owner/repo rows that route).

**The finding you need before wiring anything into the deletion gate: your 12 or 13 rows are only the regression delta, not the whole set.** The same report holds 76 mismatch lines. Counted by hand from my tables: 22 phrases are op-split re-points (the Archive and restore rows, `list my archive projects`, the repo-list rows, the calendar rows, `prs needing review`, status-report rows, and others), 8 are honest-CLARIFY rows that should be `floor`, 7 more are `REVIEW`, and 18 are real router misses that stay. The shared-subset REGRESSION cells (PORTFOLIO 3/7, QUERY 10/12) are entirely in the re-point class; the named regressions are the Archive rows, `what projects do I have?` and `analyze the file I uploaded`, and none of them is on your list.

**Two real misses worth your attention because the router picked a write verb for a read ask:** `show priorities for this sprint` (`prioritize`) and `edit my project description` (`update_document`). Neither is a re-point candidate. A guard clause in the `prioritize` description is the likely fix.

**What I need from you, in order:**
1. One commit that applies the table (yaml and `build_inversion_corpus_phase0.py` hold the rows; I do not edit either), wires the three 10-06 reports into the gate, and updates the five pins; then the full-corpus run in the same lane per Arch's rule. The post-re-point regression delta against the 08-12 baseline should be zero; I have not re-run the scorer, so that claim rests on your run.
2. A live turn-2 probe for the GUIDANCE advice phrases (state something, then ask the phrase). Single-turn CLARIFY on a subject-less ask is honest, but only a second turn shows whether it also holds up on a real one. GUIDANCE deletion stays NO-GO, as you said, until it exists.
3. Confirm with one grep that `analyze_document` is the live uploaded-file handler before the `analyze the file I uploaded` re-point (conditional in my table).

**Arch:** please add the full-corpus rule step to the Phase 3 procedure doc so the next lane does not learn it from a regression table. **CXO:** the repo-less link/connect rows will now depend on CLARIFY wording; a one-line armed question that names what is missing ("Which repository?") is worth a read.

Optional, one description commit and one rescore: a "sprint/backlog tasks" clause on `get_contextual_guidance`, an "in the way / obstacle" clause on `analyze_blockers`, and the `prioritize` guard.

**Verified how:** method: read the 10-06 week_calendar full-corpus report, `router_matches` in `scripts/inversion_phase1_shadow_score.py`, and grepped `action_registry.py` plus `services/intent_service/*.py` for each named destination, all this turn. Layer: scorer semantics and registry source. Not run: the handler tests (`test_project_list_source_1530.py`, `test_projects_lane_honesty_1645.py`; no pytest or venv on this seat), any live router call, any re-score. Denominator: 76 mismatch lines of 514 rows; the 391 matched rows and the 55 existing `REVIEW` rows were not re-read. Unverified: what `update_document`, `strategic_planning`, `search_documents` and `list_milestones` do in the live catalog, and the handler-level difference between `attention_query` and `get_top_priority` for the "important/priorities" rows.

**Board (no PM action needed):** `#1951` (this re-judge) and `#1949` (`show me all project plans`, a `REVIEW` row in my table) are Epic 0 corpus-row issues with no `Gate class:` line. #1951 is the Phase 3 tail by definition, so I am holding both unmilestoned alongside #1942 and #1943 until Arch's answer on #1943 settles where Epic 0 items live. Gate count unchanged at 29.

PPM
