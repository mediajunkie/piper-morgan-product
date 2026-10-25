---
type: adr
number: 81
title: "GitHub identity: a request is served as its account, one published Piper app mints the grant, and no deployment identity exists on a hosted deploy"
status: "ACCEPTED (D3 conditional on its compatibility check)"
valid_from: "2026-10-24"
last_updated: "2026-10-24"
---

# ADR-081: GitHub identity — whose token serves a request, which app mints it, and who else may act

**Status**: **ACCEPTED, 2026-10-24** (Arch-authored, on xian's go-ahead in the Production-map rulings, 2026-10-24 17:28: "one ADR on GitHub identity"). D3 is accepted on the condition that its compatibility check passes; if it fails, D3's fallback governs. Finding F5 in `docs/internal/planning/production-map-review-round2-2026-10-23.md`.
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
  - Cost: the resolver gains a refresh step. A failed refresh maps to STALE_TOKEN, never CONNECT_REQUIRED.
- **It is #1514's GitHub piece.** One app, registered once, with no per-install client setup.

**Condition (the compatibility check, before any build):**
1. The deployed `github-mcp-server` (v1.5.0 or its successor) serves the read and write tools we call with a GitHub App user access token as its bearer.
2. Our native REST reads (milestones, labels, the native-path list) do the same.

This is unverified today. Whoever builds it (Lead) checks it first, against a test installation, and records the result in this ADR.
- **Fallback if it fails:** one published GitHub **OAuth App** with the narrowest scope that serves our tools. D1, D2 and D4 are unchanged. The gain is #1514's "one app", and the least-privilege benefit is lost until the server supports App tokens.

Onboarding copy and the install step's experience are CXO's. The app's registration under xian's GitHub account, and the custody of its private key, are HOST's to record.

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
