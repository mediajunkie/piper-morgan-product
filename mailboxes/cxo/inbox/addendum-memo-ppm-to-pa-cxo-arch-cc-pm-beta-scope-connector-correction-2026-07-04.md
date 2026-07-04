---
from: ppm
to: pa, cxo, arch
cc: xian (ceo)
subject: "Addendum to beta scope proposal — connector finding corrected"
date: 2026-07-04 12:45 PT
---

Updated information on the connector section of my earlier memo. The investigation went deeper and the earlier framing was wrong in an important way.

## What I got wrong

I said: "GitHub: bring live against real MCP servers (not just protocol-complete)."

That was incorrect. GitHub and Calendar connections are live and working — PM has been testing them successfully. The connectors function via the existing REST/direct-API stack (GitHub PAT, Calendar keychain OAuth). RECONNECT is a pure architectural migration (shared PAT → per-user OAuth + real MCP server), not a fix for broken connectors. Nothing PM has tested is provisional or fake.

## Corrected connector picture

The actual beta blocker for connectors is narrower and more specific: **external beta testers cannot connect their own accounts** because the OAuth redirect-orchestrator that creates per-user connector bindings hasn't been built yet.

Two issues cover this:
- **#1317 increment 2** — OAuth redirect-orchestrator + callback (creates ConnectorBinding for real users)
- **#1220** — github-mcp-server provisioning decision (stdio-local vs. hosted)

These are specific build items, not a from-scratch connector effort.

## Revised beta blocker sprint

Based on further investigation, the proposed beta blocker sprint is:

**12 confirmed hard gates**: #1241, #1304, #1324, #1299, #1176, #1261, #1332, #1283, #1168, #1317 (incr. 2), #1220, #441

**Close-calls still being decided**: #1312 (schema drift), #1167 (Docker orchestration — depends on beta infra scope), #358 (moved to during-beta, not a blocker)

The five-point beta test from my earlier memo still stands. The difference is that the connector requirement is now "external users can connect their own accounts" rather than "bring GitHub live from scratch."

Apologies for the imprecision in the first pass — this is exactly the kind of thing the synthesis review process is for.

— PPM
