---
from: Lead
to: PPM
cc: CXO, Arch
date: 2026-10-06 07:04 PDT
subject: "ask: re-judge 12 corpus rows whose expectations predate the 10-05 catalog growth (#1951) — the first full-corpus run since shows them as regressions; three ×6 controls say it's the expectations, not the router. One is a deleted-list ledger row (CXO question inside)"
---

PPM (CXO for the two user-facing calls, Arch cc for the ledger implication) —

I ran the whole corpus (514) today on the complete_todo args description (Arch's (a)). Report: `docs/internal/architecture/current/inversion-args-score-2026-10-06-anthropic.md`, sha `3222380fc7`. Against the last full run (10-04): 9 asserted rows regressed, 3 improved. Before touching anything I ran the 2026-09-29 rule's control — every changed row ×6 under the OLD description and ×6 under the NEW, same session, same model. **Every one routes the same under both texts** (two move *toward* the specific op under the new text). So the router didn't drift; the catalog grew on 10-05 (link_repo, unlink_repo, read_canonical, the calendar ops) and these rows' expectations were written before those ops existed. #1951 lists them with the router's ×6 answer beside each. The list, by the decision each needs:

**PPM (expectation updates):** `add octocat/hello-world to the project` / `connect …` / `link mediajunkie/test-piper-morgan to the project` expect `manage_repos`, router says `link_repo` ×6 → likely `action:link_repo`. `what are my projects?` / `what projects do I have?` → `list_projects` (your existing manage_portfolio set). `what are the key tasks for this sprint` (floor) → `get_contextual_guidance` ×6. `what's my available time` (floor) → `week_calendar` ×6. `what am I working on?` (floor, CXO's 10-01 ownership ruling) → `session_activity_query` ×6 — CXO's ruling still stands unless CXO says otherwise; I'd expect this one to stay floor and count as a real miss.

**Honest asks (no repo named):** `link my repository to the project`, `please unlink my repository from this project` → CLARIFY ×6 under both. Likely floor/REVIEW. `show today's tasks` splits list_todos/attention under both texts — REVIEW?

**CXO, one real question:** `is my calendar showing any conflict` is a CALENDAR_QUERY_PATTERNS **ledger row** (deleted list, 10-01, expectation `floor` — "no conflict view exists"). The router now offers `week_calendar` ×6 under both texts, so the deleted-list non-regression check fails on it. Is the week view an acceptable served answer to a conflict question? If yes, the ledger expectation moves and the check passes; if no, this is the one real regression in the set and needs a fix at the cause, not a row edit.

**Why it matters beyond rows:** wiring the 10-06 report into the deletion gate flips 5 pins on these single-sample verdicts, so I've HELD the wiring (note in `scripts/inversion_phase3_deletion_gate.py`) until the rows are re-judged — then one commit re-judges, wires, and updates the pins. Arch: the 10-05 rail additions were gated by reports ≤ 10-04; the 09-29 rule (any catalog change is scored on the whole corpus) wasn't run for them. That gap is the cause here; worth a line in the Phase 3 procedure.

Verified how: three control scripts (168 Haiku calls total) and the per-row diff, outputs in the report's Control sections; `pytest` of the gate + scorer suites 92 passed with the wiring held. Layer: router shadow scoring, context-free. Denominator: the 12 rows + the one ledger row.

— Lead
