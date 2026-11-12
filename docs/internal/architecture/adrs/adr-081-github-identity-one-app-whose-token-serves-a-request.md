---
type: adr
number: 81
title: "GitHub identity: a request is served as its account, one published Piper app mints the grant, and no deployment identity exists on a hosted deploy"
status: "ACCEPTED (D3's compatibility check passed 2026-11-11)"
valid_from: "2026-10-24"
last_updated: "2026-11-11"
---

# ADR-081: GitHub identity — whose token serves a request, which app mints it, and who else may act

**Status**: **ACCEPTED, 2026-10-24** (Arch-authored, on xian's go-ahead in the Production-map rulings, 2026-10-24 17:28: "one ADR on GitHub identity"). D3 is accepted on the condition that its compatibility check passes; if it fails, D3's fallback governs. **2026-11-11: the condition is met (Arch, from #2174's two runs); D3 governs and the fallback does not apply.** See "D3's check, result" under D3. Finding F5 in `docs/internal/planning/production-map-review-round2-2026-10-23.md`.
**Amends**: ADR-070 D3 and Amendment B (this ADR is the identity half; Amendment B stays the resolver half).
**Related issues**: #1966, #2123, #1514 (GitHub part), #1325, #2136, #1061, and #2151 (the `is_available()` ruling, 10-24 16:49).

## Context

Six issues across three sprints each decide part of one question: when Piper touches GitHub, **whose identity is acting, and which app minted that identity's token?** Separately they disagree.
- #1514 wants a published OAuth app.
- #1325 wants GitHub-App installation tokens, so that Piper holds no user token.
- #2123 found reads made with the deployment's token on behalf of an account.
- #2136 wants agent seats to stop acting as the admin account.
- #1966 wants one resolver.
- #1061 wants multiple installations.

What exists today, from source (10-24):

- **The grant comes from a classic GitHub OAuth App** (`services/mcp/consumer/github_oauth_handler.py`, "OAuth 2.0 authorization-code flow for a GitHub OAuth App").
  - Each deployment registers its own app: the client id and secret come from env `GITHUB_OAUTH_CLIENT_ID`/`_SECRET`, else the keychain.
  - It requests the scope `["repo"]`, which is full read/write on every repo the user can reach ("confirm minimal set" is still open in the code).
  - Tokens don't expire, and there is no refresh step.
- **The user's own PAT is a second leg** (ADR-070 Amendment B2). It's read from `user_api_keys`, then the keychain.
- **A "system" principal can still resolve a deployment token.** `GitHubConfigService.get_authentication_token("system")` falls back to env `GITHUB_TOKEN` and the related names, then to a "system" keychain row, with no hosted guard. On alpha none of those names is set (PA's names-only read, 10-20). The fix for #2123 (`dedbe6e3ad`) stopped principal-bearing reads from using it, but the fallback itself remains.
- **Agent seats act as the admin account** (`mediajunkie`) when they push and edit on GitHub (#2136).

## Decision

### D1: A request is served as its account, and only as its account

Every GitHub read or write made for a request uses **the requesting account's own credential**, resolved by the one resolver (`resolve_credential`, ADR-070 B1–B2). There are no exceptions for a session configured earlier, for another principal or for the deployment.
- A write is the user's own act on GitHub, attributed to them.
- A read sees only what that account can see.

This is #2121's rule and #2123's ruling made general. It is the reason D5 rejects installation tokens for user work.

**Status follows the resolver** (Amendment B4, extended 10-24):
- A gate such as `is_available()` takes its answer from `resolve_credential`.
- "Not connected" means CONNECT_REQUIRED, which is only *verified* absence: no binding and no stored PAT.
- A store failure or any other degrade is a failed read. It is never "not connected" (ADR-080; #2151, 10-24 07:55 and 16:49).

### D2: A hosted deploy has no GitHub identity of its own

GitHub has the same rule as the LLM key (PDR-005 Amendment 1 §2, "Piper never spends an operator's key"): **on a hosted deploy, no GitHub credential belongs to the deployment.**
- The env token names and the "system" keychain row are honored only when `not is_hosted_deployment()`, which means a local install, where the operator is the user.
- On a hosted deploy, `get_authentication_token("system")` returns None by construction, and a principal-less caller gets no GitHub.
- Work that runs without a request, such as the standup or background reflection, runs **for an account** and uses that account's credential (D1). It is never principal-less.

This closes #2123's last unread leg (a "system" keychain row) structurally rather than by a database count.

### D3: One published Piper GitHub App mints the user's grant (user-to-server tokens)

The classic per-deployment OAuth App is replaced by **one GitHub App, published by Piper Morgan**. Its **user access tokens** ("user-to-server") are the OAuth leg's grant.

Why a GitHub App and not a published OAuth App:
- **Least privilege.** Fine-grained permissions replace `repo`'s full control: Issues and Pull requests read/write, Contents read, Metadata read. Add more only when a feature needs it, recorded in this ADR.
- **The user picks the repos.** The user installs the app on the repositories they choose. Piper can only touch what the user granted, and the user can see that list.
- **It still acts as the user.** A user access token is bounded by both the user's access and the installation's, and its writes are attributed to the user. D1 holds.
- **It expires and refreshes.** A token that expires, with a refresh token held in the grant store, can be revoked and limits the damage from a leak.
  - Cost: the resolver gains a refresh step. A *rejected* refresh (GitHub refuses the refresh token, read from the reply's `error` field) maps to STALE_TOKEN; a refresh that could not complete (timeout, connection failure, 5xx) maps to UNREACHABLE and leaves the stored pair untouched; neither maps to CONNECT_REQUIRED (Arch, 2026-11-11, on CXO's condition; #2342).
- **It is #1514's GitHub piece.** One app, registered once, with no per-install client setup.

**Condition (the compatibility check, before any build):**
1. The deployed `github-mcp-server` (v1.5.0 or its successor) serves the read and write tools we call with a GitHub App user access token as its bearer.
2. Our native REST reads (milestones, labels, the native-path list) do the same.

This is unverified today. Whoever builds it (Lead) checks it first, against a test installation, and records the result in this ADR.
- **Fallback if it fails:** one published GitHub **OAuth App** with the narrowest scope that serves our tools. D1, D2 and D4 are unchanged. The gain is #1514's "one app", and the least-privilege benefit is lost until the server supports App tokens.

Onboarding copy and the install step's experience are CXO's. The app's registration under xian's GitHub account, and the custody of its private key, are HOST's to record.

**D3's check, tooling (Lead, 2026-11-04; #2174):** `scripts/github_app_token_check.py` runs the check once a test GitHub App is installed and a user access token exists. It takes the token from `GITHUB_CHECK_TOKEN` only, calls every github-mcp-server tool Piper uses and the REST reads named above, and prints PASS or FAIL per call and totals, never the token or any body; `--writes` also creates, comments on and closes one issue in a test repository. The result, tool by tool with the versions tested, is recorded here when it runs.

**D3's check, result (Arch's validation, 2026-11-11; #2174).** Condition met; D3 governs.
- **Condition 1 (the MCP tools).** Piper's GitHub adapter (`services/mcp/consumer/github_adapter.py`) calls nine github-mcp-server tools: `search_issues`, `search_pull_requests`, `search_repositories`, `list_issues`, `list_branches`, `list_releases`, `issue_read`, `issue_write` (create and update) and `add_issue_comment`. All nine passed with a GitHub App user access token as the bearer. `issue_write create` passed on 11-07, when it made the test issue through the App; the rest passed on 11-11 with a refreshed token. `_RESOLVE_TOOL` (`resolve_resource`) is a provisional placeholder, not a github-mcp-server tool, and is outside this condition.
- **Condition 2 (native REST).** `GET /user`, milestones, labels and `/user/repos` passed.
- **Least privilege.** "A private repo the App is not installed on is refused" passed.
- **D1 (writes are the user's).** The test issue's comment is authored by the test user, with `performed_via_github_app` set to the test App (Exec's API read).
- **Refresh.** A refresh with the stored refresh token, four days after it was issued, minted a working access token. The old access token's 401 shows only that it was dead: it had passed its 8 hours on 11-07. It does not show that a refresh revokes the previous access token. (Correction, Arch, 2026-11-11 19:08)
- **Server.** The run went through `fly proxy` to `piper-morgan-gh-mcp`, the sidecar both `fly.toml` and `fly.mcp.toml` point `GITHUB_MCP_SERVER_URL` at. Its image is pinned to `ghcr.io/github/github-mcp-server:v1.5.0` in `deploy/fly/github-mcp.fly.toml`. Lead records the running machine's version alongside the two tables below.
- **Verified how:** the 15-row table xian ran on Amber on 11-11, the 11-07 run, and Exec's API read of the test issue, set against a source reading of the adapter's tool constants and the deploy files. Layer: GitHub API and the deployed MCP sidecar through a proxy. Not seen: the MCP server's own logs.

**D3's check, the two tables and the versions (Lead, 2026-11-11; #2174).** Both runs were xian's, on Amber, from `~/Development/piper-morgan-product`, through `fly proxy` to `piper-morgan-gh-mcp`, against the test repository `dinp-machine/piper-test-activity` with the test App `piper-morgan-d3-check`. No token, secret or client ID is recorded here.

Run 1, 2026-11-07 16:23 PT, first token, `--writes` (script at `abfe9f115f`):

```
rest GET /user                                    PASS
rest GET milestones                               PASS
rest GET labels                                   PASS
rest GET /user/repos                              PASS
narrowing: private repo not installed is refused  PASS
search_issues                                     PASS
search_pull_requests                              PASS
search_repositories                               PASS
list_issues                                       PASS
list_branches                                     PASS
list_releases                                     PASS
issue_write create                                FAIL tool-error
--- 12 calls: 11 pass, 1 fail
```

The one FAIL was the script's, not the server's: the create made issue 43 through the App (Exec's API read at 16:24: created by the test user, `performed_via_github_app.slug = piper-morgan-d3-check`), and the script then failed to read the new issue's number from the reply. Fixed in `ad35f8325d`, which also added `--issue N`.

Run 2, 2026-11-11 18:52 PT, the refreshed token, `--writes --issue 43` (script at `ad35f8325d`):

```
rest GET /user                                    PASS
rest GET milestones                               PASS
rest GET labels                                   PASS
rest GET /user/repos                              PASS
narrowing: private repo not installed is refused  PASS
search_issues                                     PASS
search_pull_requests                              PASS
search_repositories                               PASS
list_issues                                       PASS
list_branches                                     PASS
list_releases                                     PASS
issue_write create                                SKIPPED (--issue 43)
issue_read get                                    PASS
add_issue_comment                                 PASS
issue_write update (close)                        PASS
--- 15 calls: 14 pass, 0 fail
```

Versions:
- **github-mcp-server:** the image is pinned to `v1.5.0` in `deploy/fly/github-mcp.fly.toml`. The running machine's version was **not read** for either run: no seat runs `fly`, and the check script did not print the server's own version until 2026-11-11 (#2341). The read is asked of xian through Exec. Until it is recorded here, "v1.5.0" is the pin, not a measurement.
- **GitHub REST:** `X-GitHub-Api-Version: 2022-11-28`, sent by the script on every REST row.

How the token expires and refreshes (the check's item 4):
- Observed: the first access token was good for 8 hours (Exec, 11-07). The refresh on 11-11, four days later, used the stored refresh token and the App's client secret, returned a new access token, and the old access token then answered 401 on `GET /user`. That 401 is explained by the 8-hour expiry alone, so it is not evidence that a refresh revokes the previous access token.
- From GitHub's documentation, not observed here: a refresh also returns a new refresh token and the one used stops working, and a refresh token lasts about six months. So the grant store must write the new pair back on every refresh, in one step.
- For the next run of the check: `scripts/github_app_refresh_check.py` (#2341) does the refresh, the old-token 401 check, the proxy and the table as one command with hidden prompts, and its table names the server's handshake version.
- For the build: a refresh is a resolver step, and a *rejected* refresh (GitHub refuses the refresh token, read from the reply's `error` field) maps to STALE_TOKEN; a refresh that could not complete (timeout, connection failure, 5xx) maps to UNREACHABLE and leaves the stored pair untouched; neither maps to CONNECT_REQUIRED (Arch, 2026-11-11, on CXO's condition; #2342).

**D3's build (#2342, 2026-11-12).** The unit layer is on main and inert until the App is registered and its secrets are set. Arch's rulings are on issue 2342 and in decisions.log.

- **The switch is configuration.** App mode is on only when `GITHUB_APP_CLIENT_ID` and `GITHUB_APP_CLIENT_SECRET` are both set (`services/mcp/consumer/github_app_grant.py`). `GITHUB_APP_SLUG` gives the install link. With App mode off, the classic app behaves as before.
- **The grant record** is one value in the encrypted `github_mcp_oauth` row: both tokens, both expiries and `minted_by: github_app`. A value without the marker is a classic grant and never serves in App mode.
- **Refresh** happens in the one resolver before a token with under five minutes left is used, under a per-owner lock, and in the background every 30 minutes for grants with under two hours left, because the decrypt-only MCP app can't refresh (`services/mcp/consumer/github_app_refresh.py`, `services/scheduler/github_app_refresh_job.py`).
- **Why a binding is stale is stored** in `connector_bindings.status_reason`: `cutover` or `refresh_rejected`. The reply is picked by it.
- **The cutover is a script in xian's hand**, `scripts/github_app_cutover.py`, run in the same sitting as setting the secrets. It is a dry run by default. With `--apply`, for every stored grant the App did not mint, it tries the revoke at GitHub with the classic app's credentials, marks the binding stale with `cutover`, and deletes the token. It leaves personal tokens, saved repository choices and App grants alone, prints counts only, and finds nothing on a second run.

### D4: The user's own PAT stays a supported leg

Amendment B2's PAT leg stays, with #1966 option (i). It is the user's own credential, pasted in by them, encrypted at rest and never shared. It serves self-hosting and users who won't install an app.
- Settings recommends a fine-grained PAT (CXO's words).
- The order stays: the app grant first, then the PAT.
- The PAT leg's store failures raise, per D1 and the 10-24 16:49 ruling.

### D5: Installation (server-to-server) tokens never serve a user's request

#1325's end state is **rejected for user work**. An installation token acts as the app, so:
- writes stop being the user's;
- reads stop being bounded by the user's own access.

Both break D1. Holding a user token is the price of acting as the user, and D3's expiring user tokens are the safest form of it. #1325 closes as superseded by D3.

Installation tokens have one legitimate use in this system, D6, and it isn't a product path.

### D6: Agent seats have their own identity, separate from the product's

The cohort's agent seats act on the repository through a **separate GitHub App, the seats app** (#2136, approved by xian 10-21).
- Its installation tokens are scoped to `piper-morgan-product` and minted on Amber.
- It holds no Administration, Environments, Deployments or Secrets permission.

The product app (D3) and the seats app never share an app, key or token. The product app never acts for an agent, and the seats app never acts for a user.

The acceptance bar is #2136's own (HOST): from a seat, `.permissions.admin` reads false, and a push to `ops/restarter` is refused.

### D7: Multiple installations are native to D3, and the rest stays Enterprise

A GitHub App is installed once per user or org, so D3 already supports many installations for per-user grants. 1.0 needs nothing more. #1061's workspace-level credential management, shared by an organization's members, stays Enterprise, and is a bet-gate question.

## What each issue becomes

| Issue | Under this ADR |
|---|---|
| #1966 (two resolvers) | D1: the remaining callers, the `is_available()` gate included, derive from `resolve_credential`. Stays the precondition for sprint H (F15). |
| #2123 (deployment token on activity reads) | D1 fixed it in `dedbe6e3ad`; D2 removes the remaining leg by construction. Closes when the D2 gate and its pin land. |
| #1514 (published apps), GitHub part | D3. Calendar and Notion stay in #1514; Slack's part is Fast Follow. |
| #1325 (installation-token auth) | D5: superseded by D3; close with a pointer here. |
| #2136 (seat identity) | D6: unchanged in shape, recorded as architecture. |
| #1061 (multi-installation) | D7: Enterprise, unchanged. |

PPM files the one tracking issue F5 asks for, "GitHub identity: one app/token model and whose token serves a read", which links these six. Build order inside it is Lead's: D2's gate, then D1's gate convergence (#1966 and #2151), then D3's check, then D3.

## Consequences

**Positive:**
- One answer to "who is acting".
- Least-privilege grants the user can see.
- No deployment identity for anything to leak through.
- Agents stop being indistinguishable from the admin.

**Negative:**
- D3 adds a refresh path and an install step.
- A user who installs the app on too few repos gets honest "can't see that repo" answers. These need words (CXO) and a resolve-miss reason (`RESOURCE_NOT_FOUND`), never "no issues".
- The fallback path loses least privilege.

**Not changed:**
- The self-hosted MCP server (PM 08-29).
- The binding meaning "OAuth connected" (B3).
- Calendar and Notion grant models.

## Verified how

Read `github_oauth_handler.py` (L40–215: the classic OAuth App, the `repo` scope, no refresh), `config_service.py` `get_authentication_token` (L127–208: the "system" env and keychain fallback, no hosted guard), `github_adapter.py` `resolve_credential` and its PAT legs (L1428–1506), ADR-070 D3 and Amendment B, CONNECTORS.md's GitHub row, and the six issues' bodies and latest comments.

Layer: source and documents. D3's compatibility with `github-mcp-server` is **unverified** and is stated as its condition.

Denominator: GitHub only; 6 of the 6 issues F5 names are mapped.
