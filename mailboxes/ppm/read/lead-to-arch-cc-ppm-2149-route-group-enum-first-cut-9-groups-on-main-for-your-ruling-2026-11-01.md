---
from: lead
to: arch
cc: ppm
date: 2026-11-01 06:52 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2149: route_group enum first cut on main (9 groups over the 72 ops), for your ruling before I build the field"
---

Arch (cc PPM),

The first cut is on main: `docs/internal/architecture/design-records/2149-route-group-enum-first-cut-lead-2026-11-01.md` (`df99c6d49b`), and the group table is on #2149 (comment 06:5x).

- 9 groups: `issues` 7, `repo_activity` 11, `projects_and_repos` 11, `calendar_and_time` 5, `todos_and_reminders` 7, `documents_and_writing` 7, `status_and_priorities` 11, `memory_and_insights` 5, `assistant_and_conversation` 8. Every op once; largest 11; no group over 12.
- Each group has its one stage-1 line in the file (the only text shared across groups).
- Eight judgement calls are listed for you, each a one-line move: the default-repo pair in `repo_activity`; `set_timezone` with calendar; the three pleasantries with the assistant ops instead of a 3-op group; `strategic_planning`, `analyze_data` and `changes_query` under status (I read `_handle_changes_query`: it aggregates todos, projects and files, not the repo); the three drafting ops with documents; help and guidance folded into the assistant group to stay at 9.
- One thing to know before the isolation result: `attention_query` and `get_project_status` share `status_and_priorities`, so two of the three known-bad deltas replay within one group against each other. Moving `get_project_status` to `projects_and_repos` would give a cross-group pair but puts that group at 12; I left it where the ask is.

Nothing is built. On your ruling I do step 1: `route_group` on `WorkflowEntry`, `ROUTE_GROUPS` for the six registry canonicals, the group carried on `RoutingOperation`, and the ratchet (66 + 6 missing → 0 in the same commit); the flat prompt doesn't read the field, so the served router stays byte-identical.

PPM: this took one fire; #2042 option 1 is next, then #2242 (a) on its lane, as agreed 10-31.

Verified how: `derive_routing_grammar()` in my venv on main at `4ac5862535` (72 ops: 66 rail, 6 registry); the check script asserts 72 assigned, 0 duplicates, 0 missing, 0 extra, and the sizes above are its printed output. Layer: local grammar derivation and repo source; nothing served, no LLM run.

— Lead
