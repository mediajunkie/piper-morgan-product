# Architecture plan — config behind the MCP server (#1157 fix)

**Author**: PA · **Date**: 2026-06-05 · **Tracking**: #1157 (+ #1145)
**Decision basis**: Cowork test (config-path unreachable) + OpenLaws independent convergence on the same
fix + Cowork agent's architecture memo. **This plans the fix; build is a separate gated step.**

## The problem (one line)
Config lives as dotfiles under `~/.claude/plugins/config/dinp/...`. The agent writes them directly —
works in Claude Code (agent owns the FS), breaks in Cowork (sandboxed FS, no real `$HOME`). The "run
anywhere" thesis needs config reachable from any surface.

## The fix
**The MCP server owns config.** The agent never touches `~/.claude`; it calls server tools. The server
(a normal local process with normal FS access) writes the files wherever it likes. Reachable identically
from Claude Code, Cowork, any MCP client.

## Current state (verified 2026-06-05)
- `server.py`: config-blind — one tool (`ask_piper`), pure `/intent` passthrough. ~118 lines.
- Config read/write today = **filesystem instructions scattered in meet-piper** (~8 path references:
  cold-start check, company-profile read, two write sites, cache-migration, etc.) + implicit assumptions
  in ask/consult that a profile file exists.
- So the fix = add config tools to the server + repoint the skills' file-ops at those tools.

## Server-side design (new tools on the existing MCP server)

Four tools (mirror the Cowork memo + OpenLaws convergence):
- `get_profile()` → returns the PM profile (the piper-morgan/CLAUDE.md content), or a clear
  "not-configured / has-placeholders" signal.
- `save_profile(content)` → persists the PM profile. Creates dirs, backs up prior version.
- `get_company_profile()` / `save_company_profile(content)` → the shared cross-context profile.

**Where the server stores it**: keep the canonical path (`~/.claude/plugins/config/dinp/...`) as the
server's *own* storage location — the server has real FS access, so it CAN write there even when the
agent can't. This preserves backward-compat (a Claude Code session that reads the file directly still
works) AND fixes Cowork (the agent goes through the tool). Best of both.

**Degradation (the key risk)**: today skills can read the file even if the server is down. With
server-owned config, a down server = no config. **Mitigation**: the server maintains the file as a
**read-only mirror at the canonical path** (it already writes there), so non-setup skills can fall back
to reading the file directly if `get_profile` is unreachable. Server is source-of-truth; file is cache.

**Validation in one place**: placeholder-detection, schema version, migration-from-cache — all move into
the server, out of the skill prose.

## Skill-side changes
- **meet-piper**: replace all `~/.claude/...` read/write instructions with `get_profile` (the cold-start
  check) + `save_profile` / `save_company_profile` (the writes). The catch-22 disappears — no agent FS
  access needed. (Also the natural moment to do the brief-default + progressive-reveal refactor, but
  keep that SEPARATE — one change at a time.)
- **ask-piper / consult-piper**: where they assume a profile exists, read via `get_profile` (graceful
  if unconfigured). Minor — they mostly don't read config yet.

## Sequencing (Gall's Law — smallest working version first)
1. **Add `get_profile` + `save_profile` to server.py** (PM profile only; JSON or front-matter-md store;
   write-through to the canonical file as the mirror). Test standalone.
2. **Repoint meet-piper's PM-profile write** at `save_profile` + the cold-start check at `get_profile`.
   Gate: run meet-piper in BOTH Claude Code and Cowork → completes in both (the actual #1157 fix).
3. **Add company-profile tools** + repoint (the cross-context profile).
4. **Repoint ask/consult config reads** at `get_profile` with file-mirror fallback.
5. (Separate, later) brief-default + progressive-reveal meet-piper refactor.

## Open questions (for the plan discussion with PM)
1. **Store format**: keep front-matter-markdown (human-editable, matches today) vs. JSON (cleaner for a
   tool API)? Lean: markdown stays the on-disk mirror (humans edit it); the tool can return it as-is or
   parsed. Don't force JSON if markdown's working.
2. **Company-profile behind server too, or stays a plain file?** (Cowork memo's open Q.) If sibling
   non-Piper plugins must read it without an MCP dependency, a plain file is friendlier. Lean: server
   owns it + keeps the file mirror, so both work.
3. **Schema version now?** Cheap early, expensive to retrofit once sibling plugins depend on it. Lean:
   add a `schema_version` field now, even at v1.
4. **Does this need the dedicated-Piper-port work (#1156-ish / the Lead memo)?** No — config tools live
   on the *skunkworks MCP server* (server.py), independent of which port the *Piper app* runs on. Clean.
5. **OpenLaws convergence**: study their zip BEFORE finalizing — adopt their conventions where they're
   ahead (PM offering it). Plan stays provisional until that read.

## What this is NOT
- Not the dedicated-Piper-instance work (that's the Piper app's port; this is the plugin's MCP server).
- Not the brief-default meet-piper refactor (separate, sequenced after).
- Not a platform change (Option 3) — entirely plugin-side.

## Strategic note
This strengthens PDR-005's ratified "MCP-server alongside FastAPI" mechanism (server owns config too) and
is the substrate the reintegration thread needs (one source of truth for who-you-are, reachable
everywhere). The fan-out should describe the *fixed* design, not the broken one.
