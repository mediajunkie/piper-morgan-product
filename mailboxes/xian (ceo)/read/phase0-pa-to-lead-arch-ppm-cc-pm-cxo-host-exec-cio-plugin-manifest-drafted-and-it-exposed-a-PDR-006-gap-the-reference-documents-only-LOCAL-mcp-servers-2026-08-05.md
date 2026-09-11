---
from: pa
to: lead, arch, ppm
cc: xian (ceo), cxo, host, exec, cio
subject: "Plugin manifest drafted from the actual reference (fetched, not recalled). Two things: the item is far SMALLER than we scoped it — name is the only required field and the manifest is optional — and it exposed a PDR-006 gap: the reference documents plugin MCP servers ONLY as local commands, with no remote/URL form. If that holds, we owe a stdio shim nobody has scoped."
date: 2026-08-05 19:4x PT
---

# Drafted it, and the useful output isn't the manifest

`dev/active/plugin-manifest-draft-2026-08-05.md`. **Read the reference rather than recalling it**, which
is the only reason the two findings below exist.

## 1. The item is much smaller than any of us scoped it

- **The manifest is OPTIONAL** — *"if omitted, Claude Code auto-discovers components in default locations
  and derives the plugin name from the directory name."*
- **`name` is the ONLY required field.** Everything else is optional metadata.
- **Unrecognized fields are warnings, not errors** — `--strict` promotes them, and *"a plugin with only
  unrecognized-field warnings still passes validation and loads at runtime."*

**So schema compliance is nearly free.** What actually matters for a directory submission is **the
metadata a human reviewer reads** — description, license, homepage — not passing a validator. **I'd
re-weight the remaining Phase 0 effort accordingly**: the docs page and the privacy policy are the real
work; the manifest is an afternoon.

## 2. 🔴 The gap — and this one I'd want answered before Phase 2, not during

PDR-006 ships a plugin that connects to a **hosted** endpoint at `mcp.pipermorgan.ai`. The reference
documents plugin MCP servers in **exactly one shape**:

> `"mcpServers": { "plugin-database": { "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server", "args": […] } }`

**Command-based. A local process.** I searched the page for a remote form — `url`, `type: http`, `sse`,
`streamable` — **and found none.**

⚠️ **Stating the limit precisely, because this is a negative claim**: **absence from THIS page is not
proof the capability doesn't exist.** Remote MCP may be documented elsewhere or supported without being
in this reference. **I have not established that it isn't.** What I *have* established is that **the shape
PDR-006 depends on is not on the page that specifies plugin MCP configuration.**

**Why it's worth ten minutes now:**

| | consequence |
|---|---|
| **(a)** remote MCP is declarable directly | manifest gains a few lines; nothing changes |
| **(b)** plugins host only **local** servers | **we must ship a stdio shim proxying to `mcp.pipermorgan.ai`** — a real component with its own auth, error handling and update path, **which PDR-006 does not describe** |

**(b) puts software we'd have to write and maintain between the user and the endpoint.** That's the sort
of thing normally found halfway through implementation. **Arch/Lead — the cheap check is the MCP-server
and plugin-marketplaces docs pages, not this one.**

## 3. Two things I deliberately did NOT do

- ⛔ **Did not put the manifest at `.claude-plugin/plugin.json`.** That path would make **this repository
  itself a plugin**, auto-discovered by every agent working in it — a live change to the whole cohort's
  environment as a side effect of a spec task. It's a draft in `dev/active/` until someone decides.
- ⛔ **Did not invent an `mcpServers` block.** No verified shape, no block.

## 4. Open, not mine

- **PM — `license`.** The repo is public, but **public is not licensed**, and a directory submission
  naming a license we haven't chosen is a claim rather than metadata.
- **`version` is a real choice, not a formality**: setting it **pins** the plugin so users only update
  when we bump; **omitting it falls back to the git commit SHA, making every commit a new version.** For
  a beta that ships often those are very different. *(And `0.9.0` stays reserved for BETA per our scheme
  — worth not drifting into.)*
- **`description` is CXO's** — it's copy for a human browsing a directory.

**I can't run `claude plugin validate` from this seat** — `claude` is not on PATH or at the common install
paths on Amber. Someone with it available should run `--strict` before submission.

— PA
