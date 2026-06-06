# BYOC plugin architecture — running lessons log

**Purpose** (PM request 6/6): systematically document what we're learning about the Anthropic plugin
architecture — skills, MCP servers, packaging, install, validation, per-surface behavior — as we build
+ test the skunkworks BYOC plugin (#1145). Append-only; the durable knowledge base for this lane.
**Firewall note**: OpenLaws-derived lessons are kept architecture-only (no client specifics).

---

## Packaging & structure

- **A plugin is the canonical unit** (PM 6/1). Contains: `.claude-plugin/plugin.json` (manifest) +
  `.mcp.json` (MCP server config) + `CLAUDE.md` (root template) + `skills/<name>/SKILL.md` (one dir per
  skill) + `mcp/server.py` (the server). MCPB and hosted-MCP are NOT the packaging unit.
- **Two-tier marketplace structure**: a parent `.claude-plugin/marketplace.json` can aggregate multiple
  plugins, each pointed at by relative `source`; each plugin then has its own `.claude-plugin/plugin.json`.
  Ours: `dinp/.claude-plugin/marketplace.json` (parent) + `dinp/piper-morgan/.claude-plugin/plugin.json`.
  (`claude plugin tag` reported the marketplace entry as `plugins[0]` in the parent marketplace.json.)
- **`marketplace` is the wrapper level above plugin** — out of scope for the skunkworks PoC.

## Skills

- A skill = `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`, optional
  `argument-hint`) + markdown body = instructions injected into the agent's context.
- **Skills can't call skills** like functions (a skill is injected instructions, not a callable). The
  shared primitive across skills is the **MCP tool**, not skill-to-skill calls. (Drove the rung-3
  primitive/composed-on-the-MCP-tool architecture.)
- **Invocation differs by surface**: Cowork strips the plugin prefix (`/meet-piper`); Claude Code needs
  the full namespaced form (`/piper-morgan:meet-piper`). (OpenLaws convention; adopt in tester docs.)
- **`${CLAUDE_PLUGIN_ROOT}`** resolves to the plugin's install dir; use it for in-plugin file refs
  (`.mcp.json` server path, skill `Read` of reference files). Relative paths do NOT resolve in Cowork —
  always fully-qualify via `${CLAUDE_PLUGIN_ROOT}`.
- **Root `CLAUDE.md` is NOT loaded as context** (`claude plugin tag` warning 6/6): "CLAUDE.md at the
  plugin root is not loaded as project context. To ship context, use a skill instead." So our root
  CLAUDE.md template is a *storage template* meet-piper mirrors — fine — but don't expect it to inject.
- **🔴 Desktop SKILL injection broken — Anthropic #15178** (open since Dec 2025, via OpenLaws README):
  personal-uploaded plugin SKILL.md content is NOT injected into `<available_skills>` on Claude Desktop;
  MCP tools register fine, skill *prose* doesn't propagate. Their validated Desktop path = skill sideload
  + standalone MCP. **OPEN for us**: our Cowork-tab test showed skills working — so Cowork tab ≠ Desktop
  plugin-zip behavior; need to confirm the Code tab. (Phase-C re-test.)

## MCP server

- **PEP-723 inline deps** (`# /// script` header) + `uv run server.py` self-bootstraps deps — no venv.
  Worked cleanly on CLI install ("Installed 29 packages" + stdio wait). Lighter than OpenLaws's packaged
  `pyproject.toml` + `uv.lock` + `src/` form (which is more production-shaped; adopt when the server grows).
- **`.mcp.json` launch**: `{command: "uv", args: ["run", "${CLAUDE_PLUGIN_ROOT}/mcp/server.py"]}`.
  OpenLaws uses `uv --directory ${CLAUDE_PLUGIN_ROOT}/servers/<name> run <entry>` (packaged project form).
- **`.mcp.json` can carry `env`** (OpenLaws passes API base + key there — but ⚠️ NEVER ship live creds in
  a distributed zip; theirs leaked a key to evaluators). Ours is auth-optional localhost = no creds. Good.
- **Config ownership (#1157 fix)**: the SERVER should own user-config read/write (tools `get/save_profile`),
  NOT the agent writing to `~/.claude` (breaks in Cowork's sandboxed FS). Server has normal process FS
  access on any surface. Keep the canonical file as a human-editable + down-server-fallback mirror.

## Install & validation

- **`claude --plugin-dir <path-or-.zip>`** = canonical CLI install (per-session). `--plugin-url <url>` =
  fetch a zip from URL.
- **`claude plugin tag <source-dir>`** VALIDATES a plugin (+ creates a release git tag). Use it to
  validate before distributing. NOTE: it takes the *source dir*, not a zip (a zip arg → "PK" JSON error,
  it tries to parse the zip as JSON). Side effect: creates a `{name}--v{version}` git tag — delete with
  `git tag -d` if unintended.
- **`claude plugin` subcommands**: details / disable / enable / init / install / list / marketplace /
  prune / tag.
- **🔴 OPEN INVESTIGATION (6/6): Desktop "Plugin validation failed" on the v0.3 zip.**
  - Source dir validates CLEAN via `claude plugin tag` (only the benign root-CLAUDE.md warning).
  - v0.3 zip has the IDENTICAL root structure to the v0.2 zip that installed fine yesterday → structure
    is NOT the cause; it's content in the v0.3 edits (plugin.json desc, .mcp.json unchanged, server.py +5
    tools, meet-piper repointed) OR Desktop validates stricter than the CLI.
  - Bisect in progress: PM testing whether v0.2 still installs. If v0.2 fails too → Desktop validator
    changed (environmental). If only v0.3 fails → my edit. Awaiting result + any error detail.
  - Hypotheses to check if it's my edit: (a) description length/chars (578 vs v0.2's 486 — em-dashes?);
    (b) server.py size/syntax under Desktop's loader; (c) a Desktop schema rule the CLI doesn't enforce.

- **🔬 BISECT RESULT (6/6): isolated to `plugin.json` description LENGTH.** v0.2 (desc **486 chars**)
  installs in Desktop; v0.3 (desc **578 chars**) fails "Plugin validation failed". The 4-file diff
  between them: only `plugin.json` is install-schema-relevant (README/SKILL/server.py aren't checked at
  install-validate time). Within plugin.json, only version + description changed. → **strong hypothesis:
  Desktop enforces a manifest `description` max-length (between 486 and 578) that the CLI `claude plugin
  tag` validator does NOT enforce.** Test: v0.3.1 trims description to **372 chars** (single variable).
  - **If v0.3.1 installs → CONFIRMED**: Desktop caps description length; CLI doesn't. Keep plugin.json
    descriptions short (≤~480, ideally far less). Capture the exact cap if findable.
  - **🤝 OpenLaws relevance (PM 6/6)**: may be a "killer fix" for OpenLaws too — their plugin.json
    description was long (the v0.3-era one we studied ran ~470+ chars and read like marketing copy).
    Their team is investigating their own install issues; **flag this length-cap finding to them.** The
    convergence now cuts both ways: they gave us server-owned-config; we may have caught their install
    blocker. (Firewall: share the architecture finding, not their specifics.)
  - **Lesson — CLI validator ≠ Desktop validator.** `claude plugin tag` passing the source does NOT
    guarantee Desktop install. Desktop applies stricter/different schema checks (length cap is the first
    confirmed instance). Always test the actual target surface, not just CLI validation.

## Naming

- Plugin `name` field = the **slug** (`piper-morgan`, lowercase-hyphenated) — it's the identifier, tied
  to the config path (`dinp/piper-morgan/`) + skill namespace (`/piper-morgan:<skill>`). Do NOT change it.
- Display capitalization ("Piper morgan" seen in UI 6/6) is likely the slug being title-cased by the UI;
  fix is a display-name field IF the manifest supports one (don't guess fields into the manifest mid-
  validation-failure) — OPEN, pending where exactly PM saw it.

## Cross-surface (Code CLI / Cowork / Desktop)

- **Filesystem**: Claude Code = agent owns home FS (can write ~/.claude). Cowork = sandboxed file tools
  (connected folders + scratchpad only) + isolated shell (no real $HOME). → config must not depend on
  agent FS access (the #1157 lesson).
- **Skill loading**: works on CLI + Cowork tab (observed); Desktop plugin-zip = #15178 open question.
- **Honest degradation**: skills should detect missing tools/connectors and fall back honestly (consult-
  piper asked the user when no GitHub tool existed in Cowork — generalized correctly).
