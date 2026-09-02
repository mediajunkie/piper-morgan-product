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

## ✅ RESOLVED 2026-08-05 — the gap was MINE, not the platform's

**Plugins DO support remote MCP.** The reference documents **four** transports, not one:

| transport | fields |
|---|---|
| `stdio` | `command`, `args`, `env` |
| **`http`, `sse`, `ws`** | **`url`, `headers`, `headersHelper`** |

**So `mcp.pipermorgan.ai` is a supported shape and PDR-006's premise holds. No stdio shim is owed.**
(Arch fetched and confirmed; the taxonomy lives in the placeholder-substitution table, not the
`mcpServers` config section, whose two examples really are both `command`-based.)

⭐ **Better than a negated risk**: **`headersHelper` is the documented mechanism for supplying *dynamic*
auth headers per request** (vs static `headers`) — which is a **carrier for Arch's condition 1**, the
fail-closed per-call `owner_id` resolution. That requirement now has a named transport instead of needing
one invented.

⛔ **How I got it wrong, recorded because the mechanism is reusable**: the answer was at **line 691 of the
page dump I already had.** My search was `grep -i '…\|sse\|…' | head -8`. **`-i sse` matches
"pa·sse·d" and "proce·sse·s"** — ordinary prose — producing **exactly 8 noise hits that filled the
`head -8`**. Line 691 sat below the cut. **A pattern that is too LOOSE, paired with a truncating `head`,
EVICTS the true positive.** Opposite cause from the too-narrow predicates we've been cataloguing, same
false negative. **Never `head` a search you intend to draw a NEGATIVE conclusion from.**

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
  "license": "Apache-2.0",
  "keywords": ["product-management", "pm", "issues", "github", "notion"]
}
```

**Every field above appears in the reference's Complete Schema.** The `mcpServers` block is now
**authorable** — `http` transport with `url` + `headersHelper` — but is deliberately still absent here
until `mcp.pipermorgan.ai` exists and its auth shape is decided (Phase 2, Arch's condition 1).

### Resolved

- ✅ **`license`** — `Apache-2.0`, adopted 2026-08-13 (commit `a4547d7c4`; `LICENSE` + `NOTICE` at repo
  root). This was decided two weeks before it reached this draft — the delay, not the decision, was
  the defect (Exec's finding, 2026-08-30). Copyright holder confirmed PM-ruled 2026-08-29: Christian
  Crumlish. **Why Apache over MIT** (PM's own rationale, from the adoption commit): the explicit patent
  grant and trademark carve-out (§6), dovetailing with a separate trademark process — the real concern
  was an "evil Piper" fork stripping the ethical architecture, which **no OSS license family
  prevents** (freedom-to-run-for-any-purpose is foundational to OSD/FSF definitions). The actual
  protection is trademark + `docs/legal/values.md`, referenced via `NOTICE` §4(d) — **the license is
  deliberately not doing that work.** If this manifest or its listing copy ever touches values/ethics/
  what-a-fork-owes, `values.md` is the load-bearing artifact, not this field.

### Open, and not mine to decide

- **`version`** — `0.1.0` is a placeholder. Note the reference's behaviour: **setting `version` pins the
  plugin to that string and users only get updates when it's bumped; omitting it falls back to the git
  commit SHA, so every commit is a new version.** For a beta that ships often, that's a real choice, not
  a formality. ⚠️ **And `0.9.0` is reserved for the BETA release** per our own version scheme — don't
  drift into it accidentally.
- **`description`** — written for a human browsing a directory, not for a model. **CXO's lane**, and per
  their own finding this week the scope belongs *inside* the primary claim rather than trailing it.

## Next, in order

1. ✅ **Remote-MCP question answered** — supported; no shim owed; `headersHelper` carries condition 1.
2. ✅ **License answered** — `Apache-2.0`, decided 08-13, confirmed to this draft 08-30.
3. `claude plugin validate` is now meaningful against the two resolved fields above — still note
   **it can't run from my seat**: `claude` is not on PATH or at the common install paths here.
