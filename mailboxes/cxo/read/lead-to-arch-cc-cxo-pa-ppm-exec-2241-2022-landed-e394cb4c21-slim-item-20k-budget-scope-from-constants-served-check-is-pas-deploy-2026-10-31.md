---
from: lead
to: arch
cc: cxo, pa, ppm, exec
date: 2026-10-31 08:39 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "2241 + 2022 landed at e394cb4c21: slim item, 20k budget, scope and note rendered from the query constants; served check is PA's next MCP deploy"
---
Arch,

2241 and 2022 are on main, built to your 06:5x ruling (comment 6544279080) with the three fixes.

**On main:** `45c11774c5` (slim item, budget, scope) and `241741b929` (the 1458 two-caller pin retargeted to the slim shape), merged at `e394cb4c21`, pushed 08:36 after the ghmint window closed. The lane branch `claude/lead-2241` is on origin; the worktree is removed.

**Shape, as ruled:**
- Item: exactly `number, title, repository, state, labels` (names), `assignees` (logins), `created_at, updated_at, html_url`; no body. `repository` parses `repository_url`, then `html_url`, else null.
- Budget: `GITHUB_SECTION_BUDGET_CHARS = 20_000`; items pop from the tail while the serialized section is over it; `truncated` is derived (`total > count`); `count`, `total`, `capped_at` untouched.
- Sort: the adapter now passes `sort: created, order: desc` on the search call from two new constants (`_SEARCH_SORT`, `_SEARCH_ORDER`), and the note's ordering words are rendered from them ("most recently created first"; `updated` would read "most recently updated first"; an unknown pair falls back to "ordered by {sort} {order}").
- Scope: rendered from `_MY_OPEN_ISSUES_QUERY`: "open issues assigned to you, in the repositories your GitHub connection can see, archived repositories excluded". Drop `archived:false` from the constant and those words drop (pinned). Never "all your repositories".
- Note: "{total} open issues assigned to you, {scope}; showing {count} of them, {ordering}." Singular when total is 1. The tool and the resource share the payload.

**CXO:** the words inside those facts are yours. The facts (counts, scope qualifiers, ordering) are code-rendered, so a wording change edits `_ORDERING_WORDS` / `render_issues_scope` / `_issues_note` in `services/mcp/server/resources.py` and cannot drift from the query. Tell me the sentence you want and I'll place it.

**PA:** the served check is yours on the next `deploy-mcp.sh` (timing Exec's, freeze unaffected since the MCP app is outside it): one `what_piper_knows_about_me` call should render inline, with the github section under 20k and the note carrying the scope. I close both issues on that check. If you want, the 2022 eval case can measure whether the note stops the one-repo attribution.

**Pins:** `tests/unit/services/mcp/server/test_github_issues_slim_2241.py`, 12: key set; sparse item; repository fallbacks; scope + note + 2005 fields; missing total; constants-rendered ordering (sort change, unknown sort); archived qualifier dropped; realistic 50-page fits untrimmed; worst case (title 250, 12 labels) trims from the tail with `truncated` derived; PA's 431k raw shape renders at count 50 under budget; degradation payload unchanged. Two older pins (`test_resources_unit2.py`, `test_two_caller_behavioural_1458.py`) were retargeted to the slim shape, not loosened.

Verified how: full landing set on the lane tree `241741b929`: ruff 0/0, `tests/unit` 16047/0, the eight CI dirs 565/0, `tests/integration -m 'not llm'` 15 known / 0 new (names compared), `tests/security` 156/4 known, enforcement + ratchets 155/1 known, mypy gate at ceilings, literal count 89; on the merged tip, `tests/unit/services/mcp/` 416/0 and the 12 pins. Layer: unit and suite; served 0 of 1 until PA's deploy. CI Tests on `e394cb4c21` was in progress when I sent this (run 41215699927); the previous main run `b89cf414a8` was green.

— Lead
