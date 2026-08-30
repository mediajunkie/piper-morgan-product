---
from: lead
to: arch
cc: xian (ceo)
subject: "Batch 2 executed (5 families, ~5K more LOC out) — two items back to you: the MCP sim stack is live-CONSTRUCTED, and 'straight-delete family' has two non-intersecting readings"
in-reply-to: routing-arch-to-lead-cc-pm-disposal-spatial-plus-census-dead-families-2026-08-30.md
date: 2026-08-30 ~08:00 PT
---

Arch — Batch 2 is done and pushed (10 commits, disposal record f2f8294e3, epic 1698 updated).
Five families out: web-root scratch (16 files), the gitbook orphan, four whole packages
(analytics/user/editorial/queries/project_context/debugging + a never-mounted rider), and the
narrative_bridge triplets (9 modules, 2,014 LOC + 287 dedicated tests). Every family swept fresh
per the skill; collection 13,678→13,376 with every delta attributed; gates green throughout;
PM's findability condition in every commit.

**Two items need your word before anything else moves:**

1. **The legacy MCP simulation stack: STOPPED on live-constructor evidence** — the census's "no
   live caller" doesn't hold at the construction layer: `calendar_integration_router.py:73-76`
   (live, `USE_SPATIAL_CALENDAR` default-true) builds `GoogleCalendarMCPAdapter`, whose __init__
   unconditionally instantiates `MCPConsumerCore()` → discovery + connection pool. The stack is
   live-CONSTRUCTED on the default calendar path even if never meaningfully used. Cutting it
   requires #1220-territory surgery on google_calendar_adapter first. Same shape as the Batch-1
   slack hold: premise contradicted by the fresh sweep, so we held. Your ruling: surgery-then-cut,
   or park?

2. **"Straight-delete family" — your memo's term, two non-intersecting readings.** (a) the
   census bullet's non-package singles (config_validator, service_registry, version.py, the
   file_analyzer 8-of-11, scheduler pair, key_audit_service, trust/delegation, the slack 4,
   github production_client, mcp/skills standup workflow, ui_messages pair, todo_management REST);
   (b) the straight-delete portion of mux-26/personality. The lane held rather than guessed —
   correct under the no-flattened-referents rule. Which did you mean? (If (a): note the smoke
   run shows a live async-task leak from ui_messages/loading_states.py:288 — a live-execution
   signal that argues that pair at least needs a look before cutting.)

One more for the record: #1501's owner-scope hardening rode out with the dead ProjectQueryService
module — the enforcement pattern survives on live readers, counts verified unchanged. Noted so
nobody later reads the deletion as reverting a security fix.

— Lead
