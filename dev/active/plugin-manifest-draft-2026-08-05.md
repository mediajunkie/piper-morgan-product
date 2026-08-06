# Plugin manifest — draft + the gap it exposed

**PA · 2026-08-05** · Phase 0 distribution item **(2)** · **For**: Lead, Arch, PPM
**Source**: `code.claude.com/docs/en/plugins-reference`, fetched and read this session — **not recalled**

---

## ⛔ Why this is a draft in `dev/active/` and NOT at `.claude-plugin/plugin.json`

**Putting a manifest at the live path would make this repository itself a Claude Code plugin**, discovered
by every agent working in it. That is a live behavioural change to the whole cohort's environment, made
as a side effect of a spec task. **Not doing that unilaterally.** Move it when someone decides to.

## What the item actually was — three corrections to my own re-scope

Last fire I recorded the plan item as *"author a plugin manifest, then validate."* Reading the reference
corrects that further:

1. ⭐ **The manifest is OPTIONAL.** *"If omitted, Claude Code auto-discovers components in default
   locations and derives the plugin name from the directory name. Use a manifest when you need to provide
   metadata or custom component paths."*
2. ⭐ **`name` is the ONLY required field** — kebab-case, no spaces. Everything else is optional metadata.
3. **`claude plugin validate <path> [--strict]`** takes a path. Unrecognized fields are **warnings, not
   errors**; `--strict` promotes them. **A plugin with only unrecognized-field warnings still passes and
   still loads.**

**So the blocking work is far smaller than "author a manifest" implied.** What matters for a *directory
submission* is the metadata a reviewer reads, not schema compliance — compliance is nearly free.

## 🔴 The gap this exposed, and it's a PDR-006 question

**PDR-006 distributes a plugin that connects to a hosted MCP endpoint at `mcp.pipermorgan.ai`.** The
reference documents plugin MCP servers in exactly one shape:

```json
{ "mcpServers": { "plugin-database": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
    "args": [...], "env": {...} } } }
```

**Command-based. A local process.** I searched the page for a remote form — `url`, `type: http`, `sse`,
`streamable` — and **found none** (the one `"url"` hit is the author field).

⚠️ **Stated as the limit it is: absence from THIS page is not proof the capability doesn't exist.** Remote
MCP may be documented elsewhere, or supported without being in this reference. **I have not established
that it isn't.** What I have established is that **the shape PDR-006 needs is not on the page that
specifies plugin MCP configuration** — which is enough to make it a question worth answering before
Phase 2 rather than during it.

**Two possibilities, and they cost very differently:**

| | consequence |
|---|---|
| **(a)** remote MCP is declarable directly | manifest gains a few lines; nothing else changes |
| **(b)** plugins only host **local** MCP servers | **the plugin must ship a stdio shim that proxies to `mcp.pipermorgan.ai`** — a real component, with its own auth, error handling and update path, that PDR-006 does not currently describe |

**(b) is not a detail.** It puts a piece of software we'd have to write and maintain between the user and
the endpoint, and it's the kind of thing that gets discovered during implementation.

## Draft manifest — verified fields only

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
  "name": "piper-morgan",
  "displayName": "Piper Morgan",
  "description": "An AI product-management assistant that keeps context across sessions and works with your GitHub, Notion, Slack, and Calendar.",
  "version": "0.1.0",
  "author": {
    "name": "Design in Product",
    "url": "https://pipermorgan.ai"
  },
  "homepage": "https://pipermorgan.ai",
  "repository": "https://github.com/mediajunkie/piper-morgan-product",
  "license": "TBD — PM decision, see below",
  "keywords": ["product-management", "pm", "issues", "github", "notion"]
}
```

**Every field above appears in the reference's Complete Schema.** No `mcpServers` block — see the gap
above; **I'm not inventing the remote shape.**

### Open, and not mine to decide

- **`license`** — the repo is public (PM confirmed), but *public* is not the same as *licensed*. A
  directory submission naming a license we haven't chosen is a claim, not metadata. **PM's call.**
- **`version`** — `0.1.0` is a placeholder. Note the reference's behaviour: **setting `version` pins the
  plugin to that string and users only get updates when it's bumped; omitting it falls back to the git
  commit SHA, so every commit is a new version.** For a beta that ships often, that's a real choice, not
  a formality. ⚠️ **And `0.9.0` is reserved for the BETA release** per our own version scheme — don't
  drift into it accidentally.
- **`description`** — written for a human browsing a directory, not for a model. **CXO's lane**, and per
  their own finding this week the scope belongs *inside* the primary claim rather than trailing it.

## Next, in order

1. **Answer the remote-MCP question** (Arch/Lead) — it gates whether a shim exists. Cheapest first step is
   checking the MCP-server docs and `plugin-marketplaces` page rather than this one.
2. **PM: license.**
3. Only then is `claude plugin validate` meaningful — and note **it can't run from my seat**: `claude` is
   not on PATH or at the common install paths here.
