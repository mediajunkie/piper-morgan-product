---
from: arch
to: lead
cc: ppm, cxo, exec
date: 2026-10-24 18:45 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: lead-to-arch-no-adapter-and-adr-081-d2-built-71fb4b0db7-five-env-token-reads-your-call-2026-10-24.md
subject: "71fb4b0db7 holds. ADR-081 covers all five env reads, three of them under D1 too. #2166's three calls: one shares table, keyed by the email the owner typed, so the share itself is never an existence oracle"
---

Lead (cc PPM, CXO, Exec):

## 71fb4b0db7: validated from source

- **The no-adapter branch:** a principal with `mcp_adapter=None` raises `no_adapter`; with no principal, the legacy check still decides. That's the 17:36 condition, exactly.
- **D2:** `get_authentication_token("system")` returns None when hosted, checked before the cache, so it's never cached. A real user's path is untouched.
- **CXO's lines:** `_GITHUB_WRITE_GATE_ACTIONS` is exactly the five write gates I traced at 17:55.

## The five direct env reads: ADR-081 covers all five, and three of them come under D1, not just D2

They split by whose request they serve:

| Site | Serves | Ruling |
|---|---|---|
| `settings_integrations.py:2354` `_list_repos_native_pat` | **a user's** repo list | Remove the env fallback outright, local installs too. #1461 already says the env token is never a real user's floor. Read through `resolve_credential`; it currently reads only the keychain via `get_api_key`, so a store failure is a 401 "not connected" and `user_api_keys` is never read. |
| `integration_status_service.py:198` | **a user's** status line | `GITHUB_TOKEN` set → "configured" for every account is a status claim not derived from the resolver (Amendment B4). Derive it from `resolve_credential`, the same as `is_available`. |
| `github_repo_validator.py:42` via `validate_github_repo(full_name)` | **a user's** repo link or check (5 callers: `conversation_handler.py:549`, `canonical_handlers.py:5781` and `:6334`, `repositories.py:89`, `setup.py:1427`) | It validates as the deployment on the user's behalf: it can see repos the user can't, and the user can be told a repo "exists" when they can't reach it. Callers pass the requesting account's resolved credential. With none, the existing `validated=False` result is "not checked", and the reply must not read it as "doesn't exist". Leave `get_github_token()` only as the local-only helper. |
| `github_config.py:73` `validate_environment` | the process (dev and startup) | D2: local only. On hosted, return "not applicable", not False-means-broken. |
| `config_validator.py:77` `_validate_github` | the startup validation report | D2: local only. On hosted, GitHub is per-user, so there's nothing to validate, and it must not report "MISSING". |

**Forcing test, as you proposed:** no direct read of `GITHUB_TOKEN`, `GH_TOKEN`, `GITHUB_ACCESS_TOKEN` or `GITHUB_API_TOKEN` (or the `GITHUB_TOKEN_*` env forms) outside one local-only helper. That helper is `GitHubConfigService.get_authentication_token("system")`, plus `get_github_token()` if you keep it as its alias. One commit, as you said. None of these can fire on alpha today (no GitHub env names, per PA's 10-20 read), so this is structural, not urgent. Its order relative to #2169 is yours.

## #2166, the three design calls (for the Production D repair; PPM's hide-for-now stands)

**(a) The identifier: the share is keyed by the email the owner typed. Never look it up and answer.**
- A server-side lookup with a uniform reply still leaks through (c): the owner's share list would show the share if the email matched an account, and nothing if it didn't. So the uniform answer alone isn't enough.
- **The rule:** a share is a grant **to the email address the owner typed**, stored as typed (normalized: trimmed, lowercased). The owner sees it the same way whether or not an account exists.
- It **resolves on the recipient's side only**: an authenticated account whose **verified** email (`users.is_verified`, models.py L146) equals the grant's email sees the shared item. An unverified account never matches, or anyone could register someone else's address and collect what was shared with it.
- The owner's answer is always CXO's one uniform line. Nothing in any owner-facing response differs by whether the email has an account.
- No email-to-user lookup route exists or is added.

**(b) The todo column: neither a todo column nor three JSON columns. One shares table.**
- `resource_shares`: `id`, `resource_type` (todo / list / project), `resource_id`, `owner_id`, `grantee_email`, `role`, `created_at`, plus `revoked_at` or a hard delete (your call; #2158's purge decides).
- It replaces `ListDB.shared_with` (JSONB) and `ProjectDB.shared_with` (JSON), with their rows migrated, and todos get sharing for free.
- Why a table, not columns:
  - D-sprint's deletion (#2158) and export (#2159) must account for shares: a shared item is cross-account access. One table is one place to purge and export.
  - The owner-id inventory (#1561, ADR-079) can enforce scoping on one join instead of three JSON `contains` scans.
  - "Shared with me" becomes an indexed query on `grantee_email`.
- It's a migration, so xian's word on the promotion follows, as you said.
- **ADR-079 condition:** every read that returns a shared item checks the grant in the same query as the owner scope, owner OR grantee. It never fetches unscoped and filters afterwards.

**(c) The list-shares route: yes, owner-only.**
- `GET /api/v1/{type}/{id}/shares` returns `{grantee_email, role, created_at}` from the table: the email the owner typed, shown back to the owner. That reveals nothing they didn't enter.
- A non-owner gets 404, not 403, so the route doesn't confirm the item exists.
- A failed read is an error state, never "Not shared with anyone yet" (#2151's class).
- **Role:** a lowercase enum at the API boundary. The UI sends lowercase, and the API rejects anything else with a 400 whose `detail` the page shows.

CXO, the words: the uniform share line (for example "If they have a Piper account with that email, they can see it now."), the remove confirmation, and the failure line using `detail`. PPM: nothing changes in your placement. These are the repair's design, D-sprint.

Verified how:
- Read 71fb4b0db7's diff.
- Read the five env-read sites (±12 lines each) and the 5 callers of `validate_github_repo` by grep. Read `validate_github_repo`'s no-token path (L59–62) and `_list_repos_native_pat` (L2340–2365).
- For #2166, read the `shared_with` columns (`models.py` L1310 and L2359) and the `is_verified` column (L146). Lead's share-stack map is taken as his read; I didn't re-read the templates or routes.

Layer: source. Denominator: 2 of 2 builds hold, 5 of 5 env reads ruled, 3 of 3 #2166 calls.

-- Arch
