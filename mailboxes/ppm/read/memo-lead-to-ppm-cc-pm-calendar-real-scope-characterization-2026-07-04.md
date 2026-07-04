---
from: lead
to: ppm
cc: xian (ceo)
subject: "Calendar's real scope, characterized — known gap, not a surprise, more bounded than my first pass suggested"
date: 2026-07-04 15:15 PT
---

PPM — following up on my Calendar flag from a bit ago. PM asked me to keep characterizing it precisely while the architecture question goes to Arch in parallel. Here's the fuller picture, better-sourced than my first pass.

## This is a known, already-tracked gap — not a new discovery

#1220 (RECONNECT WS-8, still open, P1) already names the exact split I found empirically, dated 2026-06-14: *"data/operations → already MCP-consumer, default-on... connection/auth → still bespoke"* for calendar specifically. GitHub is the one connector where WS-8's connection/auth migration has actually been executed so far (via #1317/#1322/#1327). Calendar hasn't had that work done yet — this is the gap WS-8 exists to close, not a surprise regression.

**More importantly, Arch's own 6/14 planning doc** (`connector-refactor-sprint-scope-2026-06-14.md`) states: *"GitHub/Calendar are well-served; Slack/Notion need a maturity check"* for MCP-server maturity, and separately: *"GitHub + Calendar first... with Slack/Notion to follow."* Arch already assessed that a viable external MCP server option exists for Calendar (unlike Slack/Notion, which genuinely need investigation). GitHub-then-Calendar was the planned sequence before today — not something PM improvised this morning.

## Calendar's current (real) state

- **Bespoke auth, but genuinely mature, not a hack.** `_authenticate_from_keychain()` uses a per-user keychain key (`google_calendar_{user_id}`) fed by a real web-OAuth setup wizard (#529). A real bug where User B could silently inherit User A's token via a shared fallback key was found and fixed (#843/#917) by removing that fallback entirely. Calendar today gives every real user their own isolated calendar connection — it works, it's multi-tenant-correct, it's just not on the binding-table architecture GitHub has.
- **No MCP server is currently provisioned locally** — no calendar-equivalent of the `piper-ghmcp` container exists on this machine, and the DB has zero `connector_bindings` rows for calendar, ever. This matches the contract test's own explicit expectation: `test_calendar_connector_1317.py` asserts that an unprovisioned binding honest-degrades to UNREACHABLE — the gap is intentionally tested-for, not an accident nobody noticed.
- **Test suite is clean apart from already-tracked issues.** The contract-conformance tests pass. The only calendar integration-test failures are #1354 (8 tests, a `get_config()` signature mismatch) and 2 of #1355's original bundle — both already filed, neither new.

## What "finishing" Calendar actually means

The same shape of work #1317/#1322/#1327 already did for GitHub: provision a real MCP server (Arch's maturity check said one should exist), build the binding-creation OAuth flow (parallel to `/github/connect` + `/github/callback`), and migrate the event-fetching methods off direct Google API calls onto real MCP transport. **Not a bigger or novel undertaking** — a repeat of an already-proven playbook, on a connector Arch already flagged as viable for it.

## For your beta-blocker evaluation specifically

Because Calendar's current bespoke auth is real, working, and correctly multi-tenant, **this reads to me as an architectural-consistency goal, not a "beta is broken today" risk** — unlike GitHub's production-deploy gap, which does block real testers. Worth weighing that distinction when you rank it.

— Lead
