# Plugin-marketplace hosting — research (2026-06-07)

**Question (PM)**: how does hosting a plugin work, so a tester installs from our hosted marketplace /
plugin location and doesn't need to manually install or update it? Feeds #1162 (hosted distribution),
nonblocking for Beatrice. Sourced from official Claude Code docs (code.claude.com/docs) via research agent
+ local CLI (v2.1.166) primary-source.

## How it works (the mechanism)

A **marketplace = a Git repo** (GitHub recommended) containing `.claude-plugin/marketplace.json` that
lists plugins; each plugin has its own `.claude-plugin/plugin.json`. The flow:

```
/plugin marketplace add <owner/repo | git-url | path>     # one-time, per user
/plugin install <plugin>@<marketplace>                     # install
/plugin marketplace update [name]  +  /plugin update <plugin>  +  /reload-plugins   # updates
```

**Plugin `source` types** (in each marketplace.json plugin entry):
| source | shape | notes |
|---|---|---|
| relative path | `"source": "./piper-morgan"` | **Git-marketplace only** — fails if marketplace added as a bare URL (only the json is fetched, not the files) |
| github | `{"source":"github","repo":"owner/repo","ref?":"v1.0.0"}` | pins to SHA if no ref |
| url (git) | `{"source":"url","url":"https://…​.git","ref?":"main"}` | GitLab/Bitbucket/self-host |
| git-subdir | `{"source":"git-subdir","url":…,"path":"sub/dir"}` | monorepo; recent-version gated |
| npm | `{"source":"npm","package":"@org/x","version?":"2.1.0"}` | public/private registry |

**Updates / no-manual-reinstall** (PM's actual goal):
- **Auto-update**: ON by default for *official* Anthropic marketplaces; **OFF by default for third-party**
  (ours), toggle per-marketplace in `/plugin` → Marketplaces, or set `autoUpdate: true` in managed
  settings (`extraKnownMarketplaces`). On auto-update, Claude prompts `/reload-plugins` to apply.
- **Versioning**: `plugin.json` `version` wins (silently overrides marketplace entry — don't set both).
  **Omit version → every commit = a new version**; set version → must bump per release or it won't update.
- So "doesn't need to manually update" = enable auto-update on our marketplace + bump version per release.

**CLI vs Desktop**: Desktop's plugin browser shows plugins from *configured* marketplaces, but you add the
marketplace via the **CLI / `extraKnownMarketplaces` in `.claude/settings.json`** (no "add marketplace by
URL" button in the Desktop GUI). The **"source type your Claude Code version does not support"** error we
hit = Desktop trying to parse a direct **zip/url** source it doesn't support → the fix is to use the
**marketplace approach** (github source), not a raw zip. So our current hand-passed-zip path is exactly
what the marketplace approach replaces.

## ⚠️ The critical implication for US: the embedded credential blocks a public marketplace

Our current alpha plugin **embeds the basic-auth credential** in `.mcp.json`
(`PIPER_BASE_URL=https://piperalpha:<pw>@alpha.pipermorgan.ai`). That's fine for a hand-passed zip to a
trusted tester, but a **hosted marketplace = the plugin lives in a repo**, and a public repo with the
cred in it = the password is public. So hosting forces a fork:

- **Option A — extract the credential** (research's recommended, more secure): plugin ships *without* the
  cred; the tester supplies it (env var / keychain / a `meet-piper`-style setup step), or auth moves
  server-side (the **BYO-key direction** we already flagged). Then the marketplace can be **public**, and
  updates flow without ever re-sharing a secret. This is the clean end-state and it converges with the
  BYO-key roadmap.
- **Option B — private marketplace**: host the marketplace in a **private GitHub repo**; testers need repo
  access + a `GITHUB_TOKEN` (env var, for background auto-update). Keeps the embedded cred but adds a
  GitHub-access barrier for each tester. Heavier per-tester; fine for a tiny trusted set.

**Recommendation**: for >1 tester or any auto-update ambition, go **Option A** — decouple auth from the
plugin so the marketplace can be public and updates are frictionless. This is the same "don't ship creds
in a distributed plugin" lesson (OpenLaws precedent) at the marketplace layer, and it's the on-ramp to
BYO-key. The current embedded-cred zip stays the right tool *only* for the hand-passed trusted-tester case.

## Concrete path to host the dinp marketplace

1. A **GitHub repo** (e.g. `mediajunkie/dinp-plugins`, or reuse skunkworks) with
   `.claude-plugin/marketplace.json` + the `piper-morgan` plugin (github-source or relative-path).
2. **Decouple the credential** (Option A) so the repo can be public — auth becomes user-supplied or
   server-side. (This is the gating design decision, not a mechanics problem.)
3. Testers: `/plugin marketplace add mediajunkie/dinp-plugins` → `/plugin install piper-morgan@dinp`.
   Or ship `extraKnownMarketplaces` + `enabledPlugins` in a project `.claude/settings.json` for
   trust-the-folder auto-install.
4. Enable **auto-update** on the marketplace + **bump `plugin.json` version** per release → testers get
   updates without manual reinstall (PM's goal).

## Open questions
- Desktop's exact support for marketplace-install (vs CLI) on the current build — the docs say browse-only
  in the GUI; confirm whether a Desktop tester can fully install-from-marketplace without the CLI.
- The auth-decoupling design (Option A): env var vs keychain vs server-side/BYO-key — ties to #1162 auth.
- Does our hosted Piper's basic-auth even survive Option A, or does it become per-user auth at that point?

## Feeds / refs
- #1162 hosted distribution; `pa-byoc-hosted-distribution-exploration-2026-06-07.md`,
  `pa-byoc-hosted-alpha-runbook-2026-06-06.md`, `pa-byoc-hosted-alpha-scope-2026-06-06.md`.
- Sources: code.claude.com/docs — plugin-marketplaces, discover-plugins, plugins, desktop.
