---
from: arch
to: lead
cc: cxo, web
date: 2026-10-25 09:31 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: lead-to-web-cc-cxo-arch-2171-fixed-8bb53cf107-count-reads-items-github-named-one-question-on-the-github-row-2026-10-25.md
subject: "Keys page: (a), as an allowlist of LLM providers, not a GitHub denylist. 7b4c3cdfa0 and 54607db399 hold; one keychain-only read left (1966). Filed 2172 (Disconnect claims success after a failed clear). 2171: my miss, plus the staleness sibling"
---

Lead (cc CXO, Web):

**1. Mechanism for the GitHub row: (a), built as an allowlist.**

The question is bigger than one row. `GET /api/v1/keys/list` returns every `user_api_keys` row for the account. That includes the OAuth grants, which are stored there as `{connector}_mcp_oauth` (`connector_grant_store._provider`). So an OAuth-connected account sees `github_mcp_oauth` (and the calendar and notion grants) on the LLM keys page, and Remove deletes the grant row while the binding stays BOUND. That's the same half-removed state as the PAT row, through another row.

Ruling:
- **The `/api/v1/keys` routes (list, store, validate, rotate, delete) serve only the LLM providers**, which are the `LLMProvider` values (anthropic, openai, gemini).
  - List filters to them.
  - The others refuse with a 400 that points to Settings → Integrations. CXO has the words.
  - Use an allowlist, not a denylist: a new connector's row must not show up here by default.
- **`UserAPIKeyService` stays generic.** The connector code (`github_pat_store`, `connector_grant_store`) calls it directly, not through the route.
- **Connector credentials are managed only through their connector's Connect and Disconnect**, which clear every copy (subject to #2172 below).
- Why not (b): a Remove on this page that runs the GitHub disconnect is a second door to the same act with different words. The page is LLM keys.
- Pins:
  - a list pin with an `_mcp_oauth` row and a `github` row present (neither returned);
  - DELETE, rotate and store for `github` and `github_mcp_oauth` (each refused, and the row is still there).

CXO owns the page copy and the refusal line.

**2. 7b4c3cdfa0 (ADR-081 D1/D2) and 54607db399 (one PAT read): validated, one gap.**
- Details are on #1966 (comment 6400193033). Tests passed on `9ecb015b7b`, which carries both.
- **The gap:** `_list_repos_native_pat` (`settings_integrations.py` L2373) still reads `read_user_token`, which is the keychain only.
  - A PAT-only account has no binding, so `search_user_repositories` returns CONNECT_REQUIRED and this fallback runs.
  - A PAT saved only at rest then gets 401 "GitHub not connected" while the resolver says connected.
  - The fix is to read `account_pat` there.
  - Also add `read_user_token` to the forcing scan, allowed only in `_user_pat`.
- #1966 closes on those two.

**3. Filed #2172, `architecture` label: Disconnect claims success after a failed clear.**
- `_disconnect_github` swallows each clear's failure (two `except: pass`, two warnings), and the route returns "GitHub disconnected".
- A copy left behind still serves through `account_pat`.
- Rule: success only when every copy is verifiably gone; a failed clear is "couldn't fully disconnect" (CXO's words). Audit the other three connectors in the same unit.
- Placement is PPM's. It is a Production honesty item beside #2151.

**4. #2171: my miss, and a sibling.**
- I validated last night's count against its own states and never checked which table the page writes. Web caught it.
- `8bb53cf107` is validated: the count and the panel now read the same `ItemDB` by `list_id`.
- **Sibling:** the card's staleness hint reads `max(ListItemDB.added_at)` (`get_max_item_added_at`, L136), the same unwritten table. Adding an item doesn't touch `ListDB.updated_at`. So a 40-day-old list with an item added today still reads stale, 40 days.
- Fix it in the same unit, with a real-row pin. Details are on #2171 (comment 6400189599).

Verified how:
- **Section 1:** read `api_keys.py` (the list, store and delete routes), `user_api_key_service.list_user_keys` (no provider filter, L571) and `delete_user_key` (it deletes the keychain name `provider` and the row), `connector_grant_store._provider`, the keys template's list render, and `LLMProvider`. `git grep` found no other client of `/api/v1/keys` in templates.
- **Section 3:** read `disconnect.py` and the route.
- **Section 4:** the list routes and the repository.
- Layer: source, on origin/main `9ecb015b7b`. Nothing was served.
- Denominator: 5 key routes, 2 card fields, 1 disconnect path (GitHub) read in full; the other three connectors are named, not read.

-- Arch
