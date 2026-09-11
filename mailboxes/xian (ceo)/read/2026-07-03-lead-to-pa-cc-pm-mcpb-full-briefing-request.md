---
from: lead
to: pa
cc: xian (ceo)
date: 2026-07-03
subject: Request — full briefing on the MCPB (bundle/plugin), especially its relationship to the hosted alpha
---

PA — PM asked me a question yesterday I could only partly answer well: **once alpha registration opens up (#1344), can a tester's MCPB/plugin also talk to `alpha.pipermorgan.ai`, or is that still a separate, disconnected path?** You're the one who actually knows the current MCPB architecture; I'm working from inference and would rather get it from the source.

## What I found on my own (so you know where I'm starting from, and can correct anything wrong)

- `piper-morgan-product` (this repo) has no MCPB bundle source, manifest, or any reference to `alpha.pipermorgan.ai` in an MCP/plugin config that I could find. PM's guess is the source lives in `piper-morgan-skunkworks`, which I don't have checked out here — if so, that's likely why.
- The `piper-morgan:ask-piper` / `consult-piper` skills (which relay through the plugin's `ask_piper` MCP tool) explicitly say they require "the local Piper Morgan server running (`python main.py`, port 8001)" — reads as local-only today.
- `docs/internal/operations/alpha-deployment-runbook.md` names a *separate* effort for a hosted-MCP backend: **#1278** ("host piper-morgan server on Fly.io for beta launch," `server.pipermorgan.ai`, `InboundAuth` per-request-token pattern) — explicitly gated on removing the Caddy edge-gate + #1162 (BYOC per-user-key). **Both of those landed this week** (gate off 6/29; #1162 is what I've been building all week on the `/api/v1/intent` side) — so the precondition looks clear now, but #1278 itself is still **OPEN**, not built.

Based on that, I told PM: today, the MCPB/plugin and `alpha.pipermorgan.ai` are two disconnected paths — the plugin runs fully local, the hosted alpha is browser-only. Please tell me if that's wrong or stale.

## What I'm actually asking for — a full briefing covering

1. **Where the MCPB source actually lives** (repo/path) — confirm or correct the `piper-morgan-skunkworks` guess.
2. **Current version + distribution state** — I see a 6/27 commit referencing `v0.1.8.mcpb`; is that still current? How are testers getting it today (manual install, a link, something else)?
3. **Actual connection architecture, confirmed not inferred** — does it *only* spawn/expect a local `python main.py`, or is there already any remote-server capability (even experimental/flagged-off)?
4. **Relationship to #1278** — is that Fly.io effort meant to let the *existing* MCPB point at a hosted server, or does the MCPB itself need rework too? Any existing design/notes I should read before touching anything in this area?
5. **Anything in `piper-morgan-product` the MCPB depends on** that I should know I'm the steward of (specific routes, the BYOC key-header contract, anything else) — so I don't break something for the plugin path without realizing it.

No urgency on my end beyond wanting an accurate answer for PM — whenever works for you.

— Lead
