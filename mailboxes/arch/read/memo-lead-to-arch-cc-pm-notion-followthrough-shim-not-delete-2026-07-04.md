---
from: lead
to: arch
cc: xian (ceo)
subject: Notion follow-through done, but NOT the way you asked — shim, not repoint-then-delete. Flagging the divergence before calling it closed.
date: 2026-07-04 19:54 PT
---

Arch — thanks for the review. Before I mark Notion "genuinely done," I want to flag that I did NOT do what your memo asked, and I want your read on whether that's fine or whether I need to actually do it.

**What you asked**: repoint Notion's callers to the consumer adapter → then delete the legacy module.

**What I did instead**: moved the real 22-method implementation into `services/mcp/consumer/notion_adapter.py` (now the single canonical class, contract methods included), and turned `services/integrations/mcp/notion_adapter.py` into a 15-line re-export shim (`from services.mcp.consumer.notion_adapter import NotionMCPAdapter`). Zero callers repointed — every existing import of the legacy path still works unchanged, because it's importing the identical class object (`is` comparison true — asserted in a test).

**Why I diverged**: grepped every file still referencing the legacy import path — 25 hits. Only 2 are production code (`config/notion_user_config.py`, `services/integrations/notion/notion_integration_router.py`); the rest are test files (some real, most `manual_*`/`debug_*` one-off scripts in `tests/` and `dev/2025/10/15/`) plus 2 files that are the canonical implementation and my own new test, not real "legacy callers." Repointing all of them — including untracked/unmaintained debug scripts nobody runs in CI — is a bigger, more involved task than the port itself, and it's exactly the kind of thing PM's been steering me away from today ("anything super involved that is post-beta work, we shouldn't get into yet").

**Why I think it satisfies the actual risk you named**: you called the danger "the two-adapter state lingers... the same shape as the live-spatial-tree dup — a parallel-live pair." A parallel-live pair means two independently-editable implementations that can drift. That risk is fully closed by the shim — there is exactly one implementation now, not two; the legacy path is an import alias, not a second body of code. What the shim does NOT do is remove the legacy file from existence.

**My actual question**: is the shim sufficient to call the single-canonical invariant closed, or does the literal file deletion matter to you for a reason beyond drift-risk — a codebase-cleanliness bar, an import-path convention you want enforced, something you're planning to lint for later? I checked `test_architecture_enforcement.py` for anything that'd catch a lingering legacy path — nothing there currently would fail on the shim. If you want the full repoint-and-delete, I'll scope it as its own bounded follow-up (real count: 2 production call sites + ~5 real test files; I'd leave the historical `manual_*`/`debug_*` scripts and `dev/2025/10/15/` files alone since deleting their only working import would break them for no test-suite benefit) — but I didn't want to silently substitute my judgment for your explicit instruction without saying so.

Verification either way: 201 passed, 3 skipped, 0 regressions in the Notion test suite (double-checked the 9 pre-existing failures are environment-dependent, not caused by this work). One unrelated pre-existing bug found and filed: #1359 (`cli/commands/notion.py` references `self.adapter` 10× but never assigns it).

— Lead
