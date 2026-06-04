# Skunkworks MVP BYOC plugin — thin-PoC scope sketch (step 3)

**Author**: PA · **Date**: 2026-06-03 · **Status**: working sketch (digging in with PM)
**Architecture parent**: `dev/active/pa-skunkworks-to-v17-roadmap-bridge-2026-05-31.md` (decided 6/1–6/2)
**Reference structure**: `mediajunkie/claude-for-legal` (forked Anthropic legal plugin)

---

## What we're building (the thinnest end-to-end proof)

A single plugin that proves the **full stack works**: skill → MCP → real Piper API. Per PM's Gall's-Law
order, **MCP-first**: get the smallest working piece (one MCP tool hitting one real API call) running and
tested *before* layering the skill and packaging.

## The simplifying finding (why `/intent` makes this genuinely thin)

`POST /api/v1/intent` is **auth-optional** and runs on **localhost:8001**. So "make the API reachable
from the MCP" — which we'd flagged as a dependency — is **nearly free**: the MCP just does an HTTP POST
to a local, unauthenticated endpoint. No token plumbing, no OAuth, no remote. The only runtime
dependency is "Piper is running locally" (`python main.py`), which is fine for a local-dev PoC. This is
the payoff of picking `/intent` as the first rung.

## Build sequence (concrete)

**Rung 1 — the MCP server (smallest working piece):**
- One MCP tool — `ask_piper(message: str)` — that POSTs `{message, session_id}` to
  `http://localhost:8001/api/v1/intent` and returns Piper's `IntentResponse`.
- Language: **Python** (codebase-native; bundle `uv` per plugin convention) — unless we prefer Node.
- Test gate: install the MCP locally, ask Piper a question conversationally, confirm it routes
  MCP → `/intent` → response. *That alone proves the new layer.*

**Rung 2 — the skill on top:**
- A `SKILL.md` that guides the agent to use `ask_piper` for a real PM task, reading the `CLAUDE.md`
  profile for voice + the trust-gradient (propose, don't execute).
- Candidate (the B+C we picked): *"ask Piper to read your situation and propose your next step, in your
  voice."*

**Rung 3 — assemble the plugin:**
- `plugin.json` + parent `marketplace.json` (two-tier, from sub-pass 4.a) + `CLAUDE.md` template +
  the onboarding skill (built) + the new skill + `.mcp.json` pointing at the local MCP server.

## Open decisions for PM (the dig-in)

1. **`/intent` scope for the PoC** — `/intent` is the *full* engine; for some intent types it may
   *execute* an action, not just propose. Do we (a) scope the PoC to conversational ask/propose
   messages (safer, thinner), or (b) let it do whatever the engine does? *PA lean: (a).*
2. **MCP language** — Python (codebase-native, bundled uv) vs Node. *PA lean: Python.*
3. **First skill: thin passthrough vs full B+C** — for the *very* first cut, is the skill a bare
   "ask Piper" passthrough (proves MCP→/intent, smallest piece), with the profile-reading B+C behavior
   added as the next increment? Or build B+C directly? *PA lean: passthrough first, then B+C — most
   Gall's-Law.*
4. **Where it's built** — the skunkworks repo (`piper-morgan-skunkworks/byoc/`) alongside the 4.a PoC,
   yes? And do we want a tracked issue for it (the M5/distribution-not-in-issues gap I flagged)?

## What this is NOT (scope guard)
- Not auth, not remote MCP, not `/insights` (rung 2 endpoint, deferred — needs auth).
- Not MCP Apps / interactive HTML (later Gall's-Law rung).
- Not the production substrate — predecessor-study that feeds PDR-005 + Arch Q6/Q7.
