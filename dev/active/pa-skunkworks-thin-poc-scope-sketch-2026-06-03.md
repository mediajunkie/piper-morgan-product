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

## Decisions — LOCKED (PM 2026-06-03). Tracked: **#1145**.

1. **`/intent` scope** → **(a) scope to conversational ask/propose** intents (safer, thinner). ✓
2. **MCP language** → **Python native, bundle `uv`**. ✓
3. **First skill** → **bare "ask Piper" passthrough first** (smallest piece, proves MCP→/intent), then
   add profile-reading B+C as the next increment. ✓
4. **Where + tracking** → build in **`piper-morgan-skunkworks/byoc/`**; **tracked issue filed = #1145**. ✓

## Rung-1 status — BUILT + API-contract VERIFIED (2026-06-03)

- **Built** in skunkworks (`0f85af8`): `mcp/server.py` (one `ask_piper` tool, PEP-723 inline deps,
  no-silent-failure handling) + `.mcp.json` wired (`${CLAUDE_PLUGIN_ROOT}/mcp/server.py`) + `mcp/README.md`
  (test recipe). `py_compile` OK.
- **API contract verified live**: Piper running on :8001; direct `POST /api/v1/intent` (auth-optional,
  no token) → HTTP 200. Response shape confirmed: human text in `"message"`, classification in `"intent"`
  (`{category, action, confidence, floor_hit}`). Server's field-extraction handles both. Sample: "what
  should I focus on today?" → Piper answered **offer-first** ("what's on your plate? any blockers?"),
  `intent.category=PRIORITY`, `floor_hit=true` — the conscious-floor / colleague behavior the PoC exists
  to demonstrate.
- **Install gate — ✅ PASS (2026-06-04, PM-at-keyboard)**. Full chain verified live:
  - `uv run server.py` standalone → "Installed 29 packages" + silent stdio wait (PEP-723 bootstrap
    works; no venv).
  - `claude --plugin-dir …` → plugin loaded; **`ask_piper` exposed** as `piper-morgan plugin` tool.
  - **`${CLAUDE_PLUGIN_ROOT}` RESOLVED on first try** — no path-debugging needed (unlike 4.a). Key
    unknown, now closed.
  - `use ask_piper …` → `Called plugin:piper-morgan:piper-morgan` → real Piper responded **offer-first**,
    classified **PRIORITY / get_top_priority, confidence 1.0, floor_hit**. End-to-end skill→MCP→/intent
    round trip confirmed.
  - **RUNG 1 GATED PASS.** The thin BYOC plugin proves the stack.

- **Findings from the gate run** (file as discovered work):
  1. **Temporal-context bug**: Piper said "it's pretty late in the evening" at 11:30 AM. `current_time`
     context is wrong (server clock/timezone). → tracked issue.
  2. **Emergent composition pattern (reframes rung 2)**: the *host* Claude — unprompted — offered to
     gather PM's real context via ITS own MCP access (Notion/Calendar/Gmail/Slack/Granola) and feed it
     to Piper, because Piper hit its floor ("no backlog visibility"). The payoff loop is richer than
     "skill reads profile": **host agent enriches Piper at the floor.** Strong rung-2 direction.
- **Minor polish (later)**: `intent` is a dict; server prints it raw — could extract `category`/`action`.

## What this is NOT (scope guard)
- Not auth, not remote MCP, not `/insights` (rung 2 endpoint, deferred — needs auth).
- Not MCP Apps / interactive HTML (later Gall's-Law rung).
- Not the production substrate — predecessor-study that feeds PDR-005 + Arch Q6/Q7.
