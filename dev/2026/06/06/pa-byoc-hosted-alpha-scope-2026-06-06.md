# BYOC hosted alpha — scoping (Beatrice Mercier, 6/6)

**Origin**: PM 6/6, extending the hosted-distribution thread (#1162). Goal: let an *outside* alpha tester
(Beatrice Mercier, getting a Claude Pro account) try the BYOC plugin with **minimal hassle** — without
standing up the full Piper backend herself. Treat as the first concrete step of #1162 hosting research.

## The dependency wall (why local-run is too much for an outside tester)

Verified 6/6 against the repo: the Piper backend is **not** a python script — it's a docker-compose
stack of **5 stateful services** (Postgres 15, Redis 7, ChromaDB, Temporal, Traefik) + **231 python deps
including torch 2.7.1, transformers, sentence-transformers, chromadb** (multi-GB). `uv` can pull python
libs but cannot stand up the stateful services. So **bundling the backend in the plugin (Option 1) is
out** — it's shipping the whole product stack, not a plugin. Hosting (Option 2) is the path.

## Minimal-hassle alpha package (recipe)

1. **Hosted Piper instance** — deploy the M2-closing production build to a URL. API key lives
   server-side (never ships to the tester). Behind a **shared alpha auth token** (don't expose an open
   Piper + key to the internet).
2. **Alpha plugin build** — the v0.4.x plugin with:
   - the `.mcp.json` env baked to point `ask_piper` at the **hosted URL + alpha token** (instead of
     `localhost:8001`), so the tester sets nothing.
   - **`uv` bundled** for the tester's platform (see decision below).
3. **Tester experience**: install the zip in Claude Desktop → `meet-piper` (local config via bundled uv,
   private to her machine) → `ask-piper` / `consult-piper` (local shim → hosted Piper). Near-zero setup.

Config stays **local** (`~/.claude/plugins/config/dinp/`) — private, not on our multi-tenant instance.
(Full remote-MCP hosting where the tester needs *zero* local runtime is the larger #1162 target; it
reopens the where-does-config-live question, so the local-shim + hosted-backend split sidesteps it now.)

## Decision: bundle `uv` for the alpha?

- **For one known-platform tester: yes, cheap.** `uv` is a single static binary (~30-40MB); bundling
  just Beatrice's platform is one binary, no matrix. Combined with the hosted backend it gives her
  near-zero hassle. `.mcp.json` points at `${CLAUDE_PLUGIN_ROOT}/bin/uv` instead of relying on PATH.
- **Don't build a general bundled-uv pipeline yet.** At broad distribution it becomes a platform matrix
  (mac arm64 / mac x64 / linux / windows) + update maintenance — and the real end-state (hosted
  *remote* MCP) removes local uv entirely, so investing heavily in bundled-uv is investing in an interim
  we'll later discard. Bundle for the alpha tester(s); revisit only if a mid-size cohort needs it before
  remote-MCP lands.

## Rate-limiting (PM-flagged)

A hosted-with-our-key instance must be rate-limited or our Anthropic spend scales with tester usage.
Near-term guard: per-token request cap and/or a daily ceiling on the hosted instance. This is the
*interim* cost guard; **BYO-key (below) is the structural fix.**

## Roadmap: BYO-key / "seamless" alignment (PM thought) — with honest caveats

PM's instinct: a BYOC user "already has a Pro account and a key," so usage could align seamlessly to
*their* account, removing our spend. The direction is philosophically coherent (BYOC → BYO-key) and
solves cost-scaling. Two honesty flags so we don't design on a false premise:

1. **Pro account ≠ API key.** Claude Pro/Max is the *consumer subscription* (claude.ai, Desktop, Code);
   the Anthropic *API* (console.anthropic.com, pay-per-token, where API keys live) is a separate product.
   A Pro user does **not** automatically have an API key. So "already has a key" holds for power users,
   not all testers. Near-term realistic version = **BYO-API-key**: the tester pastes their own Anthropic
   key (stored via the plugin/keychain), and local-or-hosted Piper uses it. Requires they have/get a key.
2. **"Seamless, no separate key" needs a platform primitive that doesn't exist today.** The dream where
   Piper's LLM calls piggyback on the user's existing Claude Desktop session (no key at all) isn't
   possible with the current plugin/MCP architecture — the MCP server is a separate process making its
   own server-side calls; there's no API for "use the host app's Claude session." If Anthropic ever
   exposed host-inference to plugins, that changes (another platform-may-lap-us candidate). Track as an
   aspiration, not a near-term mechanism.

**Sequencing**: hosted-with-our-key + rate-limit (now, for Beatrice) → BYO-API-key option (removes our
spend; near-term roadmap) → seamless host-session inference (aspirational, platform-dependent).

## Open decisions for PM

1. Proceed with the hosted-alpha package as scoped? (recommended)
2. Bundle uv for Beatrice's platform (which OS is she on?) — or have her run the one-line uv installer?
3. M2-closing production build as the deployable artifact — coordinate with Lead Dev now or after M2 close?
4. Where to host the temporary instance (existing infra? a cheap VPS? — out of my lane to pick; flag for PM/Lead/architecture).

## Feeds
- #1162 (hosted distribution) — this is its first concrete deliverable.
- DinP marketplace `byoc/poc/dinp/README.md` "Graduation & hosting".
- Architecture lessons `dev/active/pa-byoc-plugin-architecture-lessons.md`.
