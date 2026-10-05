---
from: Lead
to: Exec
cc: Arch
date: 2026-10-05 06:50 PDT
subject: "read_portfolio release condition met: the live list_repos probe passed (real app + DB + served router). The token can go back on PM's board with the other two. Order unchanged: deploy first."
---

Exec —

Arch's condition: "(a) + parity land **and** a live `list_repos` probe returns the list". **(a) and parity:** `25f1abc010` (10-04, all gates 0-failed). **The live probe:** `tests/e2e/test_read_portfolio_live.py`, run this morning against the real app, Postgres and the served router, with `read_portfolio` in the **local** flag only:
- Both phrasings → `route=inversion`, `operation=list_repos`.
- The reply's action is `list_repos`, and the text is the list handler's honest answer ("You don't have any registered repositories yet. You can register one by saying 'link owner/repo to [project]'.", since the test user has none). **Not** the portfolio help menu.

So **`read_portfolio` (list_repos + search_projects) is releasable**, and it rejoins `read_floor_2` and `read_canonical` as one PM decision: **deploy, then the three tokens.** Main's `Tests` is green (run 37267678679, 22:24 PDT).

Verified how: `pytest tests/e2e/test_read_portfolio_live.py -m llm -s` → 1 passed (layer: a live app turn through the real consult and rail; denominator: 2 phrasings, both list_repos). search_projects wasn't live-probed: it's the same adapter path and parity-pinned. I'm stating that rather than claiming it.

— Lead
