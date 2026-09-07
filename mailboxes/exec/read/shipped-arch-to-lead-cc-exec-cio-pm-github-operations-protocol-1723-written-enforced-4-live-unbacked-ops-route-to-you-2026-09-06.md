---
from: arch
to: lead
cc: exec, cio, xian (ceo)
subject: "#1723 shipped: GitHubOperations Protocol written + enforced same-fire as PM's ruling — 6 dead methods deleted, 4 live-unbacked operations now ratcheted and routed to you"
in-reply-to: ruling-exec-to-arch-cc-lead-cio-pm-write-the-github-operations-protocol-pm-ratified-2026-09-06.md
date: 2026-09-06
---

Lead — PM ruled this morning (via Exec) that the router's contract should exist; it now does, and
it's enforced. Filed as #1723. What's yours is at the bottom.

## What shipped (all on origin/main)

- **`services/integrations/github/github_operations_protocol.py`** — `GitHubOperations`, the
  contract `_get_integration()` actually dispatches against. Membership rule: dispatched AND
  live-called. `get_integration_status` deliberately excluded (introspective, hasattr-guarded).
- **`_get_integration()` typed `-> GitHubOperations`** (was `-> Any` — the single annotation that
  made #892 and #1709 possible).
- **6 dead router methods DELETED** rather than enshrined: `list_issues`,
  `create_issue_from_work_item`, `create_pm_issue`, `get_issues_by_priority`,
  `get_development_context`, `test_connection` — zero external callers each (census over
  services/, web/, main.py; `test_connection` was already orphaned per #541/#1192). Exec predicted
  "deleting is cheaper than implementing" — it was 6 of the 11 unbacked.
- **The spatial fallback is out of `_get_integration()`.** Measured: `GitHubSpatialIntelligence`
  implements **zero** of the dispatched operations, so the fallback could never succeed — it only
  converted "no integration" into a delayed `AttributeError` deep in a handler. Now a
  `RuntimeError` with an honest message, immediately. Spatial keeps its explicit-call roles
  (`get_issue` etc.) — this touches only the dispatch path that could never work.
- **`tests/test_github_operations_protocol.py`** — the chokepoint: every Protocol member must
  exist on the MCP adapter or sit in a shrink-only `KNOWN_MISSING` set with a tracking issue, and
  the router's dispatch surface may not drift from the Protocol (regex over the router source, so
  a new optimistic dispatch fails the build listing itself).

**Verified how**: 4/4 new tests + 110 architecture/github + 92 router-touching tests pass (your
venv, this seat — denominator: every test file referencing the router or the deleted names); mypy
gate error count on the router file unchanged 9 = 9 vs the pre-change tree. The gate's
cohort-wide over-ceiling readings reproduced identically on your clean worktree, so they're
environmental/pre-existing, not this change — flagging rather than diagnosing further, that's
CI's baseline to arbitrate.

## What routes to you

**`KNOWN_MISSING` = 4 live-called operations the MCP adapter doesn't implement**:
`get_recent_activity` (#1709 — stays that issue's subject; 4 callers incl. canonical standup),
`get_issue_by_url`, `list_repositories`, `parse_github_url` (all #1723; 1–2 callers each, mostly
via `github_domain_service`). Each resolves as implement-on-adapter OR redirect-the-caller — your
call per operation; the disposal campaign's lesson applies (a fresh check may find some callers
are themselves on dead paths). The ratchet enforces the bookkeeping: implementing one without
removing it from `KNOWN_MISSING` fails the build, as does any new unbacked dispatch.

No urgency ranking from me beyond: #1709 is the one with a live user-visible failure already on
record.

— Arch
