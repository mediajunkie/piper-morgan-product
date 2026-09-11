---
from: Lead Developer
to: Chief Architect (Arch)
cc: PM (xian), Principal Product Manager (PPM)
date: 2026-06-14
subject: PM ratified MCP for the connector model — Arch owns the ADR + substrate design
priority: standard
response-requested: ADR + topology at your cadence (no M3 dependency)
---

# Decision handed off — connectors go MCP

**PM ruling (2026-06-14)**: the connector model moves to **MCP** (Piper as MCP *consumer*), not the bespoke native per-connector model. PM's rationale: it's the direction the ecosystem is moving; staying native is "dated and clunky."

**Trigger / why this surfaced**: #1226 — during M3 UAT, GitHub repo-resolution failed silently ("no open issues" despite a full repo; token was fine, but config had no stable home). Pulling the thread showed it's **systemic**: all four connectors (GitHub / Calendar / Slack / Notion) share cwd-relative flat-file config (`data/*_preferences.json`) + four inconsistent keychain credential conventions.

**Your lane — the ADR + the design** (PM ratified the *direction*; the *how* is yours):
- The **MCP-consumer substrate** — Piper consumes via MCP servers; foundation already exists at `services/mcp/consumer/*_adapter.py` (cicd, devenvironment, gitbook, github, google_calendar, linear).
- The **auth model** — how much moves to the MCP layer vs. stays in Piper. This is the crux: if the MCP server owns the connector OAuth/token, the #1226 silent-config-failure class goes away structurally.
- The **per-connector migration path** — native `services/integrations/{connector}/` → MCP consumers, retiring bespoke clients.
- **MCP-server maturity per connector** — GitHub/Calendar look well-served; Slack/Notion need a maturity check (a real sequencing input).

**Input doc** (scope + current-state map + 8 decomposable workstreams + phasing): `docs/internal/architecture/connector-refactor-sprint-scope-2026-06-14.md` — §0 records the decision.

**Anchor issue**: **#1220** (now the migration umbrella). Absorbs #1199, #1226, #1109, #1110.

**Sequencing**: Lead will decompose the doc into the WS-1..8 issue tree **once your topology/ADR lands**, so we don't decompose against the wrong shape. No M3 dependency — M3 closes independently; this is M4/M5 (PPM to place the milestone).

— Lead Developer, 2026-06-14
