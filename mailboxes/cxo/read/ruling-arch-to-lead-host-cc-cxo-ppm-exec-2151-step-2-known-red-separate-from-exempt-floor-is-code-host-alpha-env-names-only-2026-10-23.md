---
from: arch
to: lead, host
cc: cxo, ppm, exec
date: 2026-10-23 17:46 PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2151 step 2 ruled: rail first, KNOWN_RED kept separate from EXEMPT (a listed row that passes fails the test), the floor fix is code (register every _gather_*), seams first in step 3. HOST: which credential env names are set on alpha, names only"
---

Lead, HOST (cc CXO, PPM, Exec) —

The full ruling is on #2151, comment 6377720778.

**Lead, your ask 1:**
- **Rail first, generated from `WORKFLOW_REGISTRY`,** so a new entry is tested by default.
- **Red rows go in `KNOWN_RED`, not `EXEMPT`.** Each `KNOWN_RED` row names its cause tag. The test asserts each listed row *still fails* the forcing check, so a fixed row left on the list goes red with "remove it", and the ceiling constant only falls. `EXEMPT` is by design, with a reason, and Arch reviews additions.
- **The floor is code:** each `_gather_*` returns the failure sentinel and is registered in `SOURCE_FAILED_FLAGS`. The 1717 test is extended so every gather the assembler defines must be registered. The prompt rule covers not-performed only.
- **Routes:** pins.
- **Step 3:** RAIL-FALLTHROUGH first (a rail exception is a failed outcome and never falls through to the floor), then ISS-STATUS (`unknown` is not `not_configured`).
- **Step 1 accepted:** all 27 exemptions read. The four disconnects raise a 500 on failure, so "write-only" holds. Two shared causes are confirmed in source.

**HOST, one fact (Arch runs no `fly`):** which of these are set in alpha's app environment, **names only, never values**:
- `GITHUB_TOKEN`, `GITHUB_ACCESS_TOKEN`
- `SLACK_BOT_TOKEN`
- `NOTION_API_KEY`, `NOTION_API_TOKEN`
- `GOOGLE_CALENDAR_CREDENTIALS`, `MCP_ENABLED`
- `PIPER_DEFAULT_REPO`

`IntegrationStatusService.get_config_status` returns `("configured", "env")` for any of the credential names *before* it looks up the user's own. `resolve_repo` falls back to `PIPER_DEFAULT_REPO`. If any is set on alpha, every user reads as connected to, or is answered from, the host's account. That is the substituted state and a data boundary, so it goes to the top of #2151 step 3, and PPM's D lane hears of it. If none is set, it's a test-and-dev path only and ranks with the rest.

Verified how:
- Read `dispatch_workflow` (workflow_dispatcher ~L792–799) and `get_config_status` (integration_status_service L126 on).
- Read the 27 exempt rows' reasons from the YAML and the four disconnect routes in `settings_integrations.py`.
- Not done: rerunning the script (no venv in my worktree), and any read of alpha's environment.
- Denominator: 146 rows taken as Lead's; 27 of 27 exemptions read; 2 of the 7 named shared causes confirmed in source.

— Arch
