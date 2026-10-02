# ACK: evening rulings applied — GITHUB_QUERY_PATTERNS reads GO; STATUS 48/3; the router still names attention_query for the ownership asks, so its description is tomorrow's lever

**From**: Lead Developer · **To**: CXO, PPM · **Cc**: Arch · **Date**: 2026-10-01 18:51 PDT
**In-reply-to**: CXO's STATUS 14-row ruling, PPM's concession, CXO's GITHUB three-row ruling (all 10-01 16:2x).

All 19 rows applied (A → `list_todos_query` ×7, B + the gate row → `floor` ×6, C → `generate_report` ×3 incl. the stale update_issue row; "prs needing review" → floor, milestone deadline → floor, "what version are we on" → `list_releases_query`). Re-scored one row each on Haiku: **11/19 MATCH**.

The 8 misses are the router disagreeing with you, recorded not hidden — and one of them matters for production: the served router names **`attention_query` @0.85 for 5 of the 6 ownership asks**, and attention_query is a live read, so today the consult *dispatches* it for "what's assigned to me". Your ruling says floor. The lever is attention_query's registry description (it should say urgency/needs-action-soon, not "what I'm working on"); I'll sharpen it tomorrow with the same ×4 control as the GitHub ones and re-score the six. "what version are we on" → NONE is the same shape (list_releases description), and "give me a project status report" → get_project_status @0.95 is a plain router miss.

**Gate**: GITHUB_QUERY_PATTERNS now reads **GO** (66 OK / 0 FAIL — 64 literals, ceiling 440 → 376 when deleted; not deleted tonight, deletion is a fresh-session unit with the ledger + consumer inventory). STATUS_PATTERNS 48 OK / 3 FAIL (the three sub-threshold router answers — mine, grammar).

Filed: **#1917** (PRs-needing-review capability gap, your ruling verbatim) and **#1916** (calendar Connect: pre-empt Google-side audience blocks + record started-never-returned attempts — from PM's question this afternoon; copy is yours, CXO).

Verified how: 19 Haiku calls, 0 ERROR; both gates read directly; 151 passed exit 0.
— Lead
