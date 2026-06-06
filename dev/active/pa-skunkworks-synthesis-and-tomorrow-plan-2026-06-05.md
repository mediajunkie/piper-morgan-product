# Skunkworks BYOC — synthesis (June 5) + tomorrow's plan

**Author**: PA · **Date**: 2026-06-05 eve · **Tracking**: #1145
**Purpose**: single resume-point. Where the arc stands + ordered plan for next session. Read this first.

---

## Where we are (the arc, banked)

A working **3-skill BYOC plugin** calling real Piper Morgan, tested across **two surfaces** (Claude Code CLI + Cowork/Desktop), with the architecture's hard problem found and a fix designed.

**Built + gated (all PASS):**
- **Rung 1** — MCP server (`ask_piper` → `POST /api/v1/intent`, auth-optional localhost). Install gate passed; `${CLAUDE_PLUGIN_ROOT}` resolves.
- **Rung 2** — `ask-piper` skill (bare passthrough). Gate passed.
- **Rung 3** — `consult-piper` skill (host enriches Piper at the floor: gather GitHub → re-ask → honest provenance). Gate passed — and **degraded beautifully** in Cowork with no GitHub tool (fell back to asking the user, never fabricated). The honesty-as-ground principle held under a novel failure mode.
- **meet-piper** (renamed from cold-start-interview), **ask-piper**, **consult-piper** = the 3 layered skills.
- Plain-language scrub shipped (no floor/floor_hit/context_keys leaking to users). Plugin v0.2.0, clean Desktop zip built.

**Tested on Cowork/Desktop — the high-value findings:**
- 🔴 **#1157 config-not-portable** (the headline): plugin writes config to `~/.claude` (CLI idiom); Cowork's sandboxed FS can't reach it → setup can't complete. Fix designed: **server-owns-config**.
- 🔴 **#15178 (Anthropic, open since Dec 2025)**: personal-uploaded plugin SKILL.md does NOT load on Claude Desktop (MCP works, skill prose doesn't). Found in OpenLaws's README. **Could break our Desktop-zip fan-out.** Unverified for our plugin — must confirm.
- **OpenLaws independent convergence**: they hit the same config wall, backed off to **Option 0 (no persistent config)** — right for stateless research, wrong for Piper (the calibration profile IS Piper's value). Confirms #1157's problem; Piper needs the fuller server-owned solution.

**Discovered-work filed**: #1150 (temporal), #1151 (empty original_message), #1155 (floor ignores connected GitHub), #1157 (config portability — headline). All BYOC consumer-trace.

**Other findings captured (not yet built)**: meet-piper too long → brief-default + progressive-reveal; serial-vs-form = generative-vs-enumerable; consult ask-user fallback should be a designed path.

**Decisions ratified today**: v18 roadmap (yesterday) + **PDR-005 v1.0 BYOC** (today) — both validated by the lived experience of building this.

---

## The two pre-fan-out MUST-DOs (gating the fan-out)

The fan-out should describe a *fixed, working-on-the-target-surface* plugin — not one with a known-broken setup path. So before fan-out:

1. **#1157 config fix** — implement server-owns-config (plan: `pa-skunkworks-config-fix-architecture-plan-2026-06-05.md`). Gate = meet-piper completes in BOTH Claude Code AND Cowork.
2. **#15178 Desktop skill-load** — confirm whether our plugin's skills load on Claude Desktop via zip. If broken (likely, per OpenLaws), document the known-good install path per surface in the tester instructions + fan-out. (May be a "skills sideload + standalone MCP" workaround, or "Cowork works, Desktop-zip doesn't yet.")

---

## Tomorrow's plan (ordered)

**Phase A — confirm the surface reality (#15178). ~30 min, do FIRST.**
- It's cheap and it gates everything: no point building the config fix if we can't say how to install the plugin on Desktop at all. Verify whether our `meet-piper`/`ask-piper`/`consult-piper` SKILL prose loads on a Desktop zip install (vs. Cowork, where it worked). Pin down which surface uses which mechanism. Document the per-surface install path. (Adopt OpenLaws's per-surface invocation-note convention.)

**Phase B — build the #1157 config fix. The main event.**
- Per the plan doc, Gall's-Law sequence:
  1. Add `get_profile` + `save_profile` to `server.py` (PM profile; markdown-on-disk mirror at canonical path so it's both server-owned AND file-readable for backward-compat + down-server fallback).
  2. Repoint meet-piper's PM-profile write → `save_profile`; cold-start check → `get_profile`.
  3. **Gate: run meet-piper in BOTH Claude Code AND Cowork → completes in both.** (This IS the #1157 fix proven.)
  4. Add company-profile tools + repoint.
  5. Repoint ask/consult config reads → `get_profile` (file-mirror fallback).
- Open Qs to settle with PM at build start: store format (lean markdown-mirror), schema_version now (lean yes), company-profile behind server too (lean yes + file mirror).
- Adopt OpenLaws conventions where ahead: packaged MCP server form + tests when the server grows.

**Phase C — re-test both surfaces, then FAN OUT.**
- Re-run the gate tests on the fixed plugin across Code + Cowork.
- Then the fan-out memo — now genuinely strong: "working 3-skill BYOC plugin, tested on 2 surfaces, found + fixed BYOC's core hard problem (config portability), with a working honest-degradation demo and independent convergence with OpenLaws." Far beyond "PoC works."

**Lower priority / parallel** (not gating fan-out):
- #1155 (Piper consumes its own GitHub) — the clean long-term fix for consult's gather; product-floor lane.
- meet-piper brief-default + progressive-reveal refactor (after config fix; SEPARATE change).
- consult ask-user fallback → designed path.

**Standing**: PDR-005 v1.0 ratified → Docs swapping canonical + Architect Q6/Q7 unblocked (the config-fix is real input to Q6/Q7). Audit triage #1141/#1142 still pending PM. Discovered-work weekly sweep done (next Fri).

---

## The throughline (worth keeping in view)

The principle that's held all the way down: **honesty as the ground, room for the LLM to elaborate** — proven at the runtime (consult degraded honestly under a novel failure), the architecture (server-owns-config is the honest fix for surface-portability), and the language (three-registers scrub). The reintegration thread (one Piper across surfaces) keeps showing up: server-owned config IS its substrate, and OpenLaws convergence is it appearing in the wild.

Key docs: scope-sketch, rung3-design-spine, config-fix-architecture-plan, cowork-desktop-test-findings, openlaws-plugin-study, rung2/rung3-build-plans. All on origin/main.
