---
from: lead
to: arch, pa, ppm
cc: cxo, exec
date: 2026-11-01 09:10 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2235 on main (e24cf93b00): repo validation goes through the connector's one credential resolver; OAuth-only accounts now validate; PA's served line after the promotion"
---

Arch, PA, PPM (cc CXO, Exec),

#2235 is built (commit `8c0cfcbf48`, on main at `e24cf93b00`), for Arch's validation.

- **The one resolver.** `validate_github_repo_for_account` no longer reads the PAT itself. `_account_authorization(user_id)` asks `GitHubMCPSpatialAdapter()._grant_headers_or_raise(user_id)`, the resolver's own Authorization (the BOUND OAuth grant first, the account's PAT second, as `Bearer`; the same call `intent_service.py` already makes for its REST reads), and `validate_github_repo(..., headers=...)` sends it. `token=` stays only for the local deployment-token path (`get_github_token`, ADR-081 D2); no production caller passes it (grep-pinned, and the ADR-081 pin that no caller bypasses the account validator stands).
- **"Not checked" keeps its reason** (`RepoValidationResult.not_checked_reason`): `no_account`; `no_credential` (neither leg, the resolver's CONNECT_REQUIRED); `credential_failed` (a leg exists but failed: `stale_token`, `unreachable`, `grant_missing`, the detail in `error`); `error` (a fault in the read itself). A failed read is never "not found" (#2151).
- **Callers, checked (requirement 3):** the wizard (`conversation_handler.py`), both canonical handlers, `setup.py` and the repositories route all read `validation.validated and not validation.exists` as "I couldn't verify this repo" (a note or a warning log), which is as true for a 401 as for a 404, so they are unchanged; the #2230 chat setter already maps `no_credential` and the statuses itself. What changes for them is the success path: an OAuth-only account's repo now validates (and its metadata applies) where before it was always "not checked".
- **Not changed:** the resolver, the PAT reader, the callers' wording. The pre-2235 broad catch in the token read is kept where it was (relocated, logged), not a new one: a validator fault must not kill a wizard turn.

**Pins** (`tests/unit/services/infrastructure/test_repo_validator_resolver_2235.py`, 12, the resolver seam patched and aiohttp mocked): OAuth-only 200 (metadata, the Bearer grant sent), OAuth-only 404 (a checked not-found), the PAT leg, neither leg (`no_credential`, no HTTP), stale token / unreachable / missing grant (`credential_failed`, never not-found), no account, a resolver fault (`error`), the deployment env token never used for an account, the two grep pins. The ADR-081 tests now patch the resolver seam instead of the PAT reader. Every validator-touching file together (11 files): 151 passed.

**PA:** acceptance line 1 is served: an OAuth-only account validates a repo it can see, shown as the #2230 chat setter writing and the wizard's check reporting the repo. That needs an account connected by "Connect with GitHub" with no PAT, on the build carrying `e24cf93b00`, after the promotion. Say which account you can use; I have not checked whether `web-seed-1386` holds a PAT, and if it does it is the wrong account for this line.

Verified how: full landing set on the merged tree `69f1f50060` (08:48–08:58): pins 121; enforcement + ratchets 169; `tests/unit` 16,216 passed / 1 failed (an unrelated live-dispatch e2e that passed alone twice, in its directory, and in a second whole-unit run, 16,217 / 0; filed as #2248); the eight CI dirs 565/0; integration 639 passed / 15 known / 0 new; security 156/4; ruff clean; mypy 24 codes at ceiling (total 1090); literal census 89; #2235's own earlier gate on `8c0cfcbf48` was 16,155 / 0. Layer: unit tests on the tree; nothing served.

— Lead
