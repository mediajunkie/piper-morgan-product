# OpenLaws plugin study — transferable architecture findings (firewall-clean)

**Author**: PA · **Date**: 2026-06-05 · **Source**: OpenLaws eval package (PM-provided, authorized).
**Firewall discipline**: this captures the TRANSFERABLE plugin architecture + conventions ONLY. No
OpenLaws domain/legal specifics, no credentials, no client-confidential content. Attribution = "confirmed
independently on a sibling project," not copied specifics. (Per company-profile cross-pollination rule.)

## 🔴 SECURITY — flagged to PM directly (not a Piper finding, OpenLaws-side)
The distributed `.mcp.json` hardcodes a **live API key in plaintext**, and ships an `.env` with creds, in
a zip going to external evaluators. Real exposure. PM flagged for OpenLaws to fix (Keychain/env-at-runtime
+ rotate the leaked key). Recorded here only as "saw it, flagged it" — key value NOT reproduced anywhere.
*Lesson for Piper's own fan-out zip: never ship credentials in the plugin envelope.* (Ours doesn't — the
skunkworks MCP is auth-optional localhost — but worth a pre-fanout check.)

## The config question (PM's actual ask) — ANSWERED

**OpenLaws did NOT implement MCP-side config. They went simplest: no persistent config at all.**
- `openlaws-setup` skill explicitly: *"does NOT write any configuration file… no shell commands."*
- Preferences (jurisdiction, role) are handled **per-session**: the assistant asks when it needs one, or
  the user names it in the question. *"Persistent preferences across sessions aren't available yet; that
  capability is coming later."*

So the convergence is **earlier-stage than assumed**: OpenLaws hit the same "don't write config outside
the MCP" wall and **backed off to no-cross-session-config** rather than building server-side config. This
is effectively a **4th option** for #1157 we hadn't weighed:

> **Option 0 — no persistent config; per-session preferences, asked-or-named-in-question.**
> Pro: zero filesystem dependency, works on every surface trivially, no setup step to fail. Dead simple.
> Con: nothing persists — the user re-states context every session (no "Piper already knows how I work").
> For Piper specifically that's a bigger loss than for OpenLaws — Piper's WHOLE value prop is the
> persistent calibration profile. So Option 0 is right for OpenLaws (stateless research) but **wrong for
> Piper** (the profile IS the product). Reinforces: Piper needs Option 1 (server-owns-config), and
> server-owned config is the thing that lets persistence work across surfaces. The convergence confirms
> the PROBLEM; Piper's product shape demands going further to the server-owned SOLUTION.

## 🔴 BIG transferable finding — Claude Desktop SKILL injection is BROKEN (Anthropic #15178)

OpenLaws README: **[Anthropic issue #15178]** (open since Dec 2025) — *personal-uploaded plugin SKILL.md
content is NOT injected into the agent's `<available_skills>` at session start on Claude Desktop.* The MCP
server registers fine + tools are reachable; **the SKILL prose does not propagate.** Their validated
Desktop path is a **direct skill sideload + standalone MCP** workaround, NOT the plugin zip.

**This is huge for OUR Desktop test + fan-out.** It may explain things in our own Cowork run — and means
our zip-based Desktop fan-out could have skills that don't load even though the MCP works. **Action**:
verify against our test — did our `consult-piper`/`meet-piper` SKILL prose actually load in Desktop, or
did it work via MCP + Cowork's own skill handling? (Our run showed skills working, so Cowork ≠ Desktop
plugin-zip here — worth pinning down which surface does what.) MUST address in the fan-out: tell testers
the known-good install path per surface.

## Other transferable conventions worth adopting

1. **Real packaged MCP server** (`pyproject.toml` + `uv.lock` + `src/` package + entry-point script +
   full `tests/` suite) vs. our single-file PEP-723 `server.py`. Theirs is more production-shaped; ours
   is thinner-by-design for a PoC. Adopt the packaged form when the skunkworks MCP grows config tools
   (#1157) — tests especially.
2. **`uv --directory ${CLAUDE_PLUGIN_ROOT}/servers/<name> run <entry>`** launch pattern (vs our
   `uv run ${CLAUDE_PLUGIN_ROOT}/mcp/server.py`). Theirs runs a packaged project; cleaner for deps.
3. **Plugin hooks** — they ship a `Stop` hook (`check_audit_artifacts.sh`) via `hooks/hooks.json`. We
   don't use plugin-level hooks yet; a model for later (e.g. a post-consult provenance-check hook).
4. **MCPB build alongside the plugin** (`mcpb/build/...`) — they keep an MCPB bundle too, for the surface
   where that's the install path. (Consistent with: plugin is canonical, MCPB is a build target, not the
   unit — matches our PDR-005 framing.)
5. **Setup skill = connection CHECK, not interview.** `openlaws-setup` just probes the MCP (`✓ connected
   / ⚪ configured-unverified / ✗ not-found`) + offers sample queries. Contrast meet-piper's 17-Q
   interview. Reinforces our brief-default finding — though Piper genuinely needs MORE setup than OpenLaws
   (calibration profile vs. stateless research), so the answer isn't "copy theirs," it's "brief default +
   progressive reveal" (our finding) lands between the two.
6. **Per-surface invocation note**: Cowork strips the plugin prefix (`/openlaws-setup`); Code needs the
   full `/openlaws-research-agent:openlaws-setup`. Good tester-doc convention — adopt for our README.
7. **`.gitignore` + zip `-x` exclusions** for runtime artifacts (we did this for the zip; they document
   the sync discipline). Confirms our approach.

## Net for the config-fix plan (#1157)
- **Option 1 (server-owns-config) stays the recommendation** — the convergence CONFIRMS the problem, and
  Piper's product shape (persistent calibration = the value prop) demands the fuller solution OpenLaws
  deferred. Add "Option 0 = no-persistent-config" to the plan as the considered-and-rejected baseline
  (right for stateless research, wrong for Piper).
- **Adopt**: packaged-MCP-server form + tests when the server grows config tools; per-surface invocation
  doc; the #15178 Desktop-skill-injection caveat in the fan-out + tester instructions.
- **Pre-fanout MUST**: confirm our Desktop skill-load path given #15178 (don't ship a fan-out that breaks
  on the exact surface we're inviting people to test).
