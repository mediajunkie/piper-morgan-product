# BYOC hosted distribution — exploration scope (6/6)

**Origin**: PM directive 6/6, alongside the DinP marketplace structure ask: "We may also need to start
exploring hosted solutions soon, as that was part of the MVP distro work anyhow to come and now includes
hosting MCP, plugins, marketplace(s), etc." Non-blocking for v0.4; capturing durably so it's tracked, not
carried in conversation.

**This is a scoping doc, not a plan-to-execute.** It names the problem, the three things that need
hosting, the constraints we've already discovered, and open questions — so the eventual MVP-distro work
starts from a written baseline.

## Why hosting comes up now

The current BYOC plugin works but carries **two local prerequisites** that don't scale past xian's own
testing:

1. **Each user needs a local Piper Morgan server running** (`python main.py`, :8001). The plugin's MCP
   server forwards to it. Fine for the builder; a non-starter for a distributed user.
2. **Each user installs via `--plugin-dir` (CLI) or a hand-passed Desktop zip.** The
   `/plugin marketplace add <url>` path — the one that would let users install from a catalog without
   touching a local directory — **fails on the current CLI** ("source type your Claude Code version does
   not support") and needs a published catalog to point at.

Both dissolve with hosting. Hosting was always part of the MVP distribution arc; the plugin work has now
made concrete *what* needs to be hosted.

## The three things that need hosting

1. **The MCP server** — so the plugin talks to a hosted Piper endpoint instead of `localhost:8001`.
   Anthropic now supports hosted/remote MCP (the platform "lapped us" here — see the platform-laps-you
   memory). Migration question: what stays local (user's own data/credentials) vs. moves to a hosted
   Piper. Auth becomes real (today's localhost server is auth-optional).
2. **The plugins** — so a plugin zip/dir is fetched from a URL rather than hand-installed. Ties to the
   marketplace catalog.
3. **The marketplace catalog** — so `/plugin marketplace add <dinp-url>` resolves to the live DinP
   catalog and lists piper-morgan (+ future klatch, cross-pollinator). This is the wrapper level above
   individual plugins.

## Constraints already discovered (carry into the hosting design)

- **Never ship credentials in a distributed plugin zip.** (OpenLaws precedent: an eval zip shipped a
  live API key in plaintext to external evaluators.) Hosted auth must replace any in-zip creds.
- **Desktop enforces a manifest `description` max-length** the CLI doesn't (cap 486–578 chars). Any
  hosted-catalog tooling must validate against the *stricter* surface.
- **Harness ≠ session for tool access** — a hosted plugin must be tested on each surface (CLI / Cowork /
  Desktop Code tab) independently; availability on one doesn't imply another.
- **Server-owned config** (the #1157 design) assumes the server has filesystem access on the user's
  machine. A *hosted* server changes that assumption — config storage location/ownership needs a
  rethink for the hosted case (per-user cloud config? still local file with a hosted compute plane?).
  This is the biggest open design question hosting introduces.

## Open questions for PM / architecture

1. **What migrates vs. stays local?** (Per the platform-laps-you discipline: map it explicitly.) User
   data + credentials almost certainly stay user-controlled; Piper compute could host. Where's the line?
2. **Config ownership in the hosted case** — the #1157 server-owned-config design is local-server-shaped.
   Does hosted Piper read/write per-user config in the cloud, or does a thin local shim retain the
   `~/.claude/plugins/config/dinp/` file? (Affects privacy story — today the answer "all local, never
   cloud" is a selling point.)
3. **Build vs. adopt** — Anthropic's hosted-MCP + (eventual) hosted-marketplace primitives may cover
   most of this. Default to adopting the platform version where it exists rather than DIY (sunk-cost
   discipline). What's genuinely Piper-specific and must be built?
4. **Sequencing against the OpenLaws MCP-to-market work** (xian's late-June/July focus) — there's likely
   transferable hosting architecture between the two (firewall: architecture only, no client specifics).

## Relationship to other docs

- DinP marketplace structure: `byoc/poc/dinp/README.md` (skunkworks) — "Graduation & hosting" section.
- Architecture lessons: `dev/active/pa-byoc-plugin-architecture-lessons.md`.
- Tracked as GitHub issue **#1162** (under the skunkworks epic #1145).
