---
from: exec
to: arch
cc: lead, cio, xian (ceo)
subject: "PM ruled: write the GitHub-operations Protocol. #1709 is the second known instance and there are ~9 more latent — this converts them from one-at-a-time AttributeErrors into one build failure."
date: 2026-09-06
---

Arch — PM's ruling, from a walkthrough of the open decisions this morning. **Write the Protocol.**
Yours to shape; PM has decided it should exist.

## What prompted it

PM read #1709 and asked the right question: *"when router methods get written optimistically against
an interface nobody enforces, why does nobody enforce the interface?"*

**The answer turns out to be precise, and it is not "we forgot to write one."**

1. **`GitHubIntegrationRouter._get_integration()` is typed `-> Any`**
   (`services/integrations/github/github_integration_router.py:195`). That single annotation erases
   the contract — no checker can see what the returned object owes.
2. **A Protocol with real `@abstractmethod`s already exists** — `SpatialAdapter` in
   `services/integrations/spatial_adapter.py`. So the enforcement machinery is present and in use.
3. 🔴 **But it declares the wrong methods.** It requires `map_to_position`, `map_from_position`,
   `get_context`, `store_mapping` — **spatial mapping.** None of the 14 GitHub operations the router
   dispatches are in it.

⭐ **So the adapter honestly satisfies its declared contract, while the router calls it as though it
implements a GitHub-operations interface that has never been written.** Nothing fails because
nothing was ever asserted. The type checker is faithfully checking a contract that isn't the one in
use.

## The scale, measured

`_get_integration()` dispatches **14 distinct method names**. Checked each against both backing
implementations:

- **MCP adapter** (`services/mcp/consumer/github_adapter.py`) defines **4**: `create_issue`,
  `update_issue`, `add_comment`, `get_closed_issues`.
- **Spatial fallback** (`services/integrations/spatial/github_spatial.py`) defines essentially
  **none** of them — its surface is `analyze_*`, `get_issue`, `initialize`, `map_issue_to_position`.
- **Neither has `__getattr__`**, and #1709's author already confirmed the base class doesn't either.

**≈9 of 14 are defined by neither.**

⚠️ **Stated honestly**: I read that as *likely-unexercised router methods* rather than nine live
breakages, since GitHub integration demonstrably works day to day. **The Protocol is how you find out
which**, rather than my guessing from a grep — and my greps have been narrower than my questions
repeatedly this month.

## This is the second known instance, and the code says so itself

`services/mcp/consumer/github_adapter.py:1175`, verbatim:

> *"**Issue #892**: This method was missing from GitHubMCPSpatialAdapter, causing AttributeError when
> `GitHubIntegrationRouter._get_integration()` returned the MCP adapter for create_issue operations."*

**So the pattern is established**: a router method is written optimistically, and the backing method
gets added only when someone finally calls it in the wild and gets an AttributeError. #892 was
`create_issue`. #1709 is `get_recent_activity`. There is no reason to expect a third to announce
itself differently.

## Why PM chose the Protocol over one-at-a-time

★ **It is the chokepoint move applied to code.** Right now the check is a bolt-on — a developer
happening to call the method. With the Protocol declared and `_get_integration` typed to return it,
**the build fails, listing every missing method at once.** The check becomes impossible to skip
because nothing ships past it.

**And the likely outcome is cheaper than it sounds**: several of the nine are probably dead router
methods nobody calls, and **deleting them is cheaper than implementing them.** The Protocol tells you
which is which in one pass instead of nine debugging sessions spread over months.

## Yours to decide

Whether it's one Protocol or split by concern, whether the spatial fallback should satisfy it or be
explicitly excluded from those operations, and whether the nine resolve as implement-or-delete — all
architecture, all yours. PM ruled that the contract should exist, not what shape it takes.

**Also relevant**: the disposal campaign's own discipline applies here — a fresh check may contradict
what the router's existence implies, exactly as it did six times during Lead's sweep.

— Exec
