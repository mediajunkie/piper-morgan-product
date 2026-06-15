# Option A — decouple the plugin credential (plan)

**Decision**: PM chose Option A (2026-06-07) — get the access credential OUT of the plugin so the plugin
can ship from a **public** marketplace with **auto-update**, without ever shipping a secret. This doc is
the plan; not yet built (PM hasn't tested the current embedded-cred zip yet — this is the next-step design).

## Why (what it unlocks)
- **Public marketplace + frictionless updates**: a hosted marketplace = the plugin lives in a repo. A
  public repo can't contain the basic-auth password. Decoupling lets the repo be public → testers
  `marketplace add` + `install` + **auto-update** (no hand-passed zips, no re-sharing a secret per update).
- **"Never ship creds in a distributed plugin"** (OpenLaws precedent) applied at the marketplace layer.
- **On-ramp to BYO-key**: the same change (auth not baked into the plugin; supplied per-user) is the
  structural prerequisite for each user funding their own LLM usage later.

## Current → target

| | Now (embedded-cred zip) | Target (Option A) |
|---|---|---|
| `.mcp.json` `PIPER_BASE_URL` | `https://piperalpha:<pw>@alpha.pipermorgan.ai` (secret in URL) | `https://alpha.pipermorgan.ai` (host only — **no secret**) |
| credential location | baked in the plugin zip | **local, user-supplied** (server-owned config), never in the repo |
| how server authenticates | httpx reads creds from the URL | server reads credential from local config → sends auth header |
| distributable how | hand-passed zip only | **public marketplace** (or private), with auto-update |

## Design — three parts

**1. Plugin carries no secret.** `.mcp.json` `PIPER_BASE_URL` = the bare host (`https://alpha.pipermorgan.ai`).
Nothing secret anywhere in the plugin repo. (Repo can be public.)

**2. Credential lives in local, server-owned config — set once by the user.** Reuse the #1157
server-owned-config pattern (the MCP server already owns read/write under
`~/.claude/plugins/config/dinp/piper-morgan/`). Add a small credential store there (e.g.
`credentials` entry / file the server reads). A **one-time setup step** writes it:
   - **`/piper-morgan:connect`** (new tiny skill, or a step folded into `meet-piper`): prompts the user
     for their Piper access credential and saves it via a server `save_credential` tool. Server-owned →
     works on every surface (the #1157 win), no shell-env fiddling (important for Desktop testers).
   - Fallback: a `PIPER_API_TOKEN` env var the server also checks (for CLI/power users).

**3. Server sends auth from config, not URL.** `server.py`:
   - read the credential from server-owned config (env-var fallback);
   - send it on the httpx call via `auth=` (basic-auth) or an `Authorization: Bearer` header (token) —
     **auth-scheme-flexible** so we can switch the hosted side later without re-touching the plugin;
   - **if no credential configured → return a clear "not connected — run `/piper-morgan:connect`" signal**
     (honest degradation), and on a **401** from the host, say the same. ask-piper/consult-piper surface
     that prompt instead of a raw error.

## Near-term vs end-state (the credential itself)

- **Near-term (alpha): shared access password, supplied out-of-band.** The credential the user pastes at
  `connect` = the shared Caddy basic-auth password (PM gives it to each tester directly, e.g. in the
  INSTRUCTIONS or a DM — NOT in the repo). Plugin is public; the password is distributed separately. Same
  security level as today, minus the public-repo leak. Minimal change to the hosted side (keep Caddy
  basic-auth).
- **End-state: per-user credentials.** Each tester gets their own token; the hosted Piper validates
  per-user (revocable per tester, usage attributable). Converges with BYO-key (the user's own Anthropic
  key, eventually). Bigger hosted-side change (per-user auth / accounts) — deferred.

## Work items (when we build it)
1. **plugin `.mcp.json`** — `PIPER_BASE_URL` → bare host (drop the creds). [trivial]
2. **`server.py`** — add `save_credential`/`get_credential` (server-owned config); read credential +
   send via httpx `auth=`/header; no-credential + 401 → "run connect" signal. [small]
3. **`/piper-morgan:connect` skill** (or meet-piper step) — prompt + store the credential. [small]
4. **ask-piper / consult-piper** — detect "not connected"/401 → prompt `/connect` (honest degradation). [small]
5. **Marketplace repo** — public GitHub repo with `.claude-plugin/marketplace.json` + the (now
   secret-free) plugin; enable auto-update; bump `plugin.json` version per release. [small]
6. **Hosted side** — near-term: keep Caddy basic-auth (credential = shared pw). End-state: per-user tokens.

## Sequencing
This is the **gate** between "hand-passed zip to trusted testers" (where we are) and "public hosted
marketplace with auto-update" (where PM wants to go). Build it once the current embedded-cred zip is
proven on Desktop (so we're decoupling a known-working plugin, not debugging two changes at once).

## Open questions for PM
1. **Credential UX**: a `/connect` setup prompt (server-stored, Desktop-friendly — recommended) vs a
   `PIPER_API_TOKEN` env var (CLI-friendly) — or both?
2. **Shared password vs per-user tokens** for the alpha: shared (minimal, now) vs per-user (revocable,
   more work). Recommend shared near-term, per-user at the BYO-key step.
3. **Marketplace public vs private**: public (needs the decouple — this plan) vs private GitHub repo
   (keeps embedded cred, needs each tester's `GITHUB_TOKEN`). This plan assumes public.

## Refs
- `pa-plugin-marketplace-hosting-research-2026-06-07.md` (the mechanics this unblocks)
- `pa-byoc-hosted-alpha-scope-2026-06-06.md` / `pa-byoc-hosted-distribution-exploration-2026-06-06.md` (BYO-key)
- #1162; #1157 (server-owned-config, the pattern reused here)
