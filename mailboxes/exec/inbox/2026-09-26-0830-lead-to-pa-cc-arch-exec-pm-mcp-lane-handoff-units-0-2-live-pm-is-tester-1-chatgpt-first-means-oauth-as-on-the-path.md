# MCP lane handoff to PA (PM's call this morning): units 0–2 live at mcp.pipermorgan.ai; PM is tester #1, ChatGPT first — which puts the OAuth authorization server on the path

**From**: Lead · **To**: PA · **Cc**: Arch (re-scope trigger fired), Exec (sprint plan), PM (b: relays PM's ruling) · **Date**: 2026-09-26 10:39 PDT

PM, verbatim this morning: *"The first MCP tester will be me, and the client can be ChatGPT first, and then Claude after that… let's let Piper Alpha drive the MCP testing program as part of skunkworks and free you up to work on MVP critical-path epics."* So this is yours from here; I return to epic 0. Everything below is what you inherit, verified from outside this morning, not from the plan.

## What's live (MCP app `piper-morgan-mcp`, release v5 = origin/main `65740438ae`)
- `https://mcp.pipermorgan.ai/health` → 200 with git_sha. Every other path is deny-by-default 401.
- **Identity** (unit 1): `mcp_access_tokens` (hash-only at rest; migration `n1462mcpt` applied on alpha v142), `MCPTokenVerifier` through the SDK's bearer auth; no anonymous path; a backend fault refuses (was a 500 on the first probe — fixed). PM set `DATABASE_URL` on the app; a garbage bearer now refuses via the real lookup.
- **Resources** (unit 2, no tools, no prompts — FastMCP's tool/prompt handlers are stripped and the capability object is pinned): `piper://me/profile`, `piper://me/colleague-model` (#1510 verified store + PIPER.md priorities, per CXO — never #1735), `piper://me/github/issues` (via the user's binding; `connect_required` when unbound; cap stated). Honest-empty shapes throughout.
- Runbook: `docs/internal/architecture/current/mcp/server-README.md`. Plan + progress: `…/mcp/phase-c-build-plan-2026-09-25.md`. Arch's scope: `…/mcp/phase-c-minimal-alpha-slice-2026-09-25.md`. Deploy: `fly deploy -c fly.mcp.toml -a piper-morgan-mcp --remote-only --build-arg PIPER_GIT_SHA=$(git rev-parse HEAD)` from a detached worktree. Mint: `scripts/mint_mcp_token.sh` over `fly ssh console` (raw token printed ONCE, masked echo; deliver like an invite token — never the repo). Before any tester connects: set `min_machines_running = 1` in `fly.mcp.toml` (a cold start read 000 once this morning).

## The consequence of "ChatGPT first" — Arch, this is your Q1 trigger
ChatGPT connectors speak OAuth 2.1 + dynamic client registration and offer no bearer field (Arch's Q1 ruling, 09-25: "if PM's pick is claude.ai/ChatGPT, there's no workaround and unit 4 goes on critical path"). So **unit 4 — the OAuth authorization server — is now on the path for tester #1's first client.** The SDK ships the frame: `mcp.server.auth.provider.OAuthAuthorizationServerProvider` (`register_client` / `authorize` / `exchange_authorization_code` / `load_access_token` / refresh + revoke) + `AuthSettings.client_registration_options`; what's ours to build is the provider backed by Piper's login (the `authorize` step redirects to a Piper consent page for an already-signed-in user, issues a code bound to that user, and the access tokens it mints can simply be `mcp_access_tokens` rows — the verifier already exists). Claude Desktop/Code as the SECOND client can use a plain minted bearer via `mcp-remote --header` with nothing more built.

**Who builds unit 4 — your call with Arch, PM's rule in mind.** Two honest options: (a) I land it as one more Lead-reviewed lane (it touches the identity boundary; roughly a day; then PA owns everything after), or (b) you dispatch it under skunkworks with Arch's review. I lean (a) for the identity-boundary reason, but PM asked to free me up "as much as possible" and I'll follow your read of that.

## Named gaps to state to the tester (Arch's acceptance item 4 — you own the comms now)
#1458 cross-caller isolation is OPEN (this slice is safe because there is exactly one caller); the recomposition rubric's T-MCP-surface axis is UNMEASURED and this build is precisely what unblocks measuring it (CXO, 09-25); the #1510 store today holds only `reminder_clear_verb:*` confirmations, so the colleague-model resource will read nearly empty for most users until more of the rail stores through it — honest, not broken.

Verified how: `/health`, no-bearer and garbage-bearer probes from outside this morning (200 / 401 / 401); the refusal reason on the app's logs (warning = lookup ran); tests 92/92 in `tests/unit/services/mcp/server/` at commit. Layer: live endpoint + unit. Denominator: units 0–2 of 4; unit 3 (first contact) not yet exercised by anyone.

— Lead
