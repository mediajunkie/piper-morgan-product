# Slack RECONNECT — approach plan (Lead Dev, 2026-06-30)

**Status**: PLAN (PM moved Slack up from "last" on 2026-06-30 since the rest of the RECONNECT autonomous queue is drained + team's on slow cycles). Execute on resume.

## Context
Slack is on the **keychain / ADR-058 model** (per-user tokens in the keychain), **not** the github binding model. So these are keychain-model fixes/features — orthogonal to the binding model, **except** #1334's disconnect, which a future Arch binding-migration (#1335 gate) would reshape. Workstreams: WS-7 = client/oauth tech-debt+bug; WS-6 = inbound onboarding.

## Scope — four open items

| # | WS | What | Type | Gate |
|---|---|---|---|---|
| **#1110** | WS-7 | `SlackClient` calls `config_service.get_config()` **without `user_id`** at 3 sites (`slack_client.py:77/89/116`); `__init__` (:57) stores no user_id — but `get_config` requires it post-ADR-058 → multi-tenancy isolation bug (latent; masked in #1085) | bug | none — clean TDD |
| **#1334** | — | duplicate `/slack/disconnect` route (`settings_integrations.py:440` + `2146`); first-registered (440) wins and does NOT revoke Slack-side; the more-complete 2146 (revokes via OAuth handler) is dead | bug | none — reconcile the two defs |
| **#1109** | WS-7 | Slack OAuth state store is a **class-level in-proc dict** (`oauth_handler.py:46` `_oauth_states`) → only single-process safe; move to **Redis** | tech-debt / infra | Redis (6379, available) |
| **#1201** | WS-6 | Slack **inbound** (Socket Mode / app-token) setup has **no product path** — invisible, manual, dev-mediated (machinery exists in `socket_mode_runner.py`) | feature / UX | **CXO** (user-facing onboarding flow + copy) |

## Recommended sequence + rationale

1. **#1110 (multi-tenancy bug) — FIRST.** Correctness/isolation + foundational (other Slack work builds on a correctly user-scoped client). **Approach**: thread `user_id` into `SlackClient` (store in `__init__`) and pass it to `get_config(user_id=...)` at :77/:89/:116. **Check #1085** (slices 2/3, where the bug is masked) so the fix doesn't regress how callers construct `SlackClient`. TDD: a test asserting `SlackClient` forwards `user_id` to `get_config`.

2. **#1334 (slack-dup disconnect) — SECOND.** Concrete bug. **Approach**: read both `/slack/disconnect` defs (440 vs 2146); the 2146 version revokes via the OAuth handler (`revoke_workspace_access`) — that's the behavior to KEEP; delete the duplicate so the live route revokes Slack-side. **Hold** the connector-agnostic-disconnect-helper part of #1334 — that pairs with the Arch binding-migration call (#1335). Just fix the dup + ensure Slack-side revoke now.

3. **#1109 (Redis OAuth state) — THIRD.** Infra/tech-debt, independent. **Approach**: move `_oauth_states` (class-level dict, `oauth_handler.py:46`) to Redis (6379). The issue quotes the intended shape verbatim. TDD with fakeredis / a Redis fixture. Watch nonce TTL + cleanup.

4. **#1201 (inbound onboarding) — LAST + CXO-gated.** Largest + user-facing. **Approach**: build a product path for Socket Mode / app-token setup (mirror the `settings_github.html` token-entry precedent). **Flag CXO before building the UI** (onboarding flow + copy — same as set-default-repo's UX wanted CXO). The inbound machinery (`socket_mode_runner.py`) already works; this is the discover-and-configure-it path.

## Cross-cutting / gates
- **Binding-migration (Arch, #1335 gate)**: if Arch migrates Slack → binding model, connect/disconnect reshape. Do #1334's *dup fix* now (independent); hold the *helper*.
- **#1108** (OAuth recovery UX) is cited by #1109/#1201 — check whether in scope or separate at execution.
- **Verify-before-extend**: read the cited files first; the issues are precise but confirm line numbers (they drift).

## First execution step (on resume)
Start **#1110**: read `slack_client.py` (`__init__` :57, get_config sites :77/:89/:116) + `slack/config_service.py` (get_config signature) + #1085's tests → write the failing test (SlackClient forwards user_id) → thread user_id → green → close properly. Then #1334 → #1109 → #1201 (CXO).

## Refs
RECONNECT scope §2e/§11 · ADR-058 / #734 (multi-tenancy) · #1085 (slices 2/3) · #1192 family (connect-UX) · #1108 (OAuth recovery) · #1335 (gate / binding-migration) · #1334.
