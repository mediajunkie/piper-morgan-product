# Rung 2 build plan — the bare passthrough skill (`ask-piper`)

**Author**: PA · **Date**: 2026-06-04 eve (plan only; build in the morning, fresh) · **Tracking**: #1145
**Scope decision (locked, PM 6/4)**: bare passthrough skill FIRST. Composition pattern (host-enriches-
Piper-at-the-floor) is glimpsed + queued as rung 3 — **do NOT build it into rung 2.**
**Prereq met**: rung 1 gated PASS 6/4 (plugin installs, `ask_piper` MCP tool live, end-to-end verified).

---

## Goal (one sentence)

Add a minimal skill to the plugin that teaches the agent *when and how to reach for the `ask_piper`
MCP tool* — proving the **skill layer** sits cleanly on top of the working MCP layer. Nothing more.

## What "bare passthrough" means (and does NOT mean)

- **IS**: a `SKILL.md` that says "when the user wants Piper's own take on a PM question, call `ask_piper`
  with their request and relay Piper's response (including its intent classification)." A thin guide
  over the existing tool.
- **IS NOT**: profile-reading, voice-shaping, trust-gradient enactment, or host-side context-gathering.
  Those are rung 3+. If the skill starts reaching into `~/.claude/plugins/config/dinp/piper-morgan/
  CLAUDE.md` or calling other MCPs, scope has crept — stop.

## The build (Gall's-Law smallest step)

### File to create
`piper-morgan-skunkworks/byoc/poc/dinp/piper-morgan/skills/ask-piper/SKILL.md`
(mirrors the existing `skills/cold-start-interview/SKILL.md` location convention.)

### Frontmatter (match cold-start's shape)
```
---
name: ask-piper
description: >
  Relay a natural-language PM question to the user's locally-running Piper Morgan
  (via the ask_piper MCP tool) and surface Piper's own answer + intent
  classification. Use when the user wants *Piper's* take on a PM task — priorities,
  drafting, status — rather than a generic answer. Requires the local Piper server
  (python main.py, :8001).
---
```

### Body (sketch — finalize at build time)
1. **One-line purpose**: this skill is the thin bridge to Piper's conscious-floor engine via `ask_piper`.
2. **When to use** (1–3 bullets): user explicitly wants Piper's view; a PM-shaped request (priorities/
   drafting/status); NOT for general questions the host can answer directly.
3. **How to use** (the passthrough contract):
   - Call `ask_piper(message=<the user's PM request, verbatim or lightly cleaned>)`.
   - Relay Piper's response. Surface the intent classification (category/action/confidence/floor_hit)
     so the user sees how Piper read it.
   - **No-silent-failure**: if `ask_piper` returns the "couldn't reach Piper" message, tell the user
     plainly that the local server isn't up (`python main.py`), don't fake an answer.
4. **Scope guard (in the skill, so future edits hold the line)**: this skill is a passthrough. It does
   NOT read the PM profile, shape voice, or gather context from other tools — those are later rungs.

## Acceptance test (rung-2 gate, PM-at-keyboard, morning)

Same install path as rung 1 (`claude --plugin-dir …`), then in that session:
1. `/` shows the new `ask-piper` skill under `(piper-morgan)`. ✓
2. Invoke the skill (e.g. "use the ask-piper skill to ask what I should focus on") → it calls
   `ask_piper` → real Piper responds with intent classification surfaced. ✓
3. Stop the local Piper server, re-invoke → skill reports the server-down message cleanly (no faked
   answer). ✓ (verifies the no-silent-failure path end-to-end)

If all three: **rung 2 gated PASS.** Then rung 3 conversation (composition pattern).

## Notes / watch-items
- Skills load from disk per CLI invocation (4.a finding) — edit in place, restart `claude`, live.
- Watch whether a skill + an MCP tool of overlapping name (`ask_piper` tool vs `ask-piper` skill) reads
  cleanly in the `/` surface or confuses; rename the skill if so (e.g. `consult-piper`).
- Keep the diff small: one new `SKILL.md`, no changes to `plugin.json`/`.mcp.json`/the MCP server.

## Next-session task — dedicated skunkworks Piper instance (NOT tonight)

**Why**: skunkworks tests share :8001 with whatever else is using the local Piper server. At 6/4
~10:52 PM `ask_piper` returned Piper's own "AI service temporarily unavailable / reasoning engine"
error (server reachable, downstream LLM call failed). The skill handled it correctly (relayed the
error, no fabrication — verified). **Cause NOT established** — could be Lead Dev restarting the shared
server, an LLM-API hiccup, or something else. **Do not guess; investigate tomorrow** (check Piper's
logs around that timestamp). A dedicated skunkworks instance would *isolate* us from shared-server
churn regardless of the specific cause.

**The fix is easy** — `server.py` already reads `PIPER_BASE_URL` (line 21, defaults :8001). So:
- Run a dedicated skunkworks Piper on a different port (e.g. :8002), and
- set `PIPER_BASE_URL=http://localhost:8002` for the skunkworks MCP (env in `.mcp.json` or shell).

**Why not tonight**: standing up a 2nd Piper instance is real setup (its own process, possibly DB/LLM
config) — open-ended, late-hour work we agreed to defer. Both rungs are already gated PASS; the conflict
only affects *future* tests and is transient. Capture, resume next session.

**Tracked discovered work** (both surfaced by the BYOC consumer-trace, both filed 6/4):
- **#1151** — `/intent` returns `intent.original_message: ""` (empty) — stable across both gate runs,
  independent of the LLM error. Data-fidelity gap in the intent contract.
- **#1150** — `/intent` temporal-context wrong (said "late evening" at ~11:30 AM).
- **Open question (investigate tomorrow, do NOT guess)**: cause of the 10:52 PM "AI service unavailable"
  — check Piper logs around that time. May or may not relate to #1151's empty original_message.

## Morning startup pointer
Resume: this plan + the scope sketch (`pa-skunkworks-thin-poc-scope-sketch-2026-06-03.md`) + #1145.
Piper must be running locally for the gate test (`cd piper-morgan-product && python main.py`).
