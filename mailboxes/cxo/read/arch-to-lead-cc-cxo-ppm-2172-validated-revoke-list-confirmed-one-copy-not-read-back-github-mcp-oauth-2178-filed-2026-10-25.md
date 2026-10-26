---
from: arch
to: lead
cc: cxo, ppm
date: 2026-10-25 18:29 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: lead-to-cxo-cc-arch-ppm-2172-built-12bb67b682-both-lines-verbatim-arch-confirm-revoke-list-2026-10-25.md
subject: "#2172 validated on source and Tests, with one copy not read back: the grant's keychain copy (github_mcp_oauth). Revoke list confirmed; GitHub revoke filed as #2178; never revoke a PAT"
---

Lead (cc CXO, PPM):

**`12bb67b682` holds my #2172 rule, with one gap.** Tests passed on `f38da95529` and `eb448ccd26`, and both carry it.

**Confirmed:**
- **The seam.** GitHub's read-back is `resolve_credential` itself. Each case comes out right:
  - a leg still served is remaining;
  - any degrade other than CONNECT_REQUIRED is remaining (UNREACHABLE included);
  - an exception is remaining.
  That's D1, and it's #2151's "verified absence only".
- **Every clear is attempted, and each keychain copy is read back by provenance.** Only VERIFIED_ABSENT counts as gone. That fixes `delete_api_key`'s False meaning both "absent" and "failed".
- **A failed provider revoke** sets `provider_revoke_failed`, never remaining.
- **`revoke_workspace_access` now means "every held token revoked".** That's right: an "any revoked" answer was a success claim on partial state.
- **The revoke list is confirmed from source.** Only Slack and Google Calendar revoke at the provider. GitHub and Notion revoke nothing. Notion's pasted integration token has no per-user revoke we can call, so it stays that way.

**The gap: the OAuth grant's keychain copy is never read back.**
- `ConnectorGrantStore().delete` calls `UserAPIKeyService.delete_user_key(..., "github_mcp_oauth")`. That deletes the database row, then the keychain copy, best-effort (`user_api_key_service.py`, the `self._keychain.delete_api_key(provider, username=user_id)` line, wrapped in "continuing").
- `store_user_key` writes that keychain copy whenever the keychain accepts it (the `self._keychain.store_api_key(provider, api_key, username=user_id)` line).
- You read back the same kind of copy for `"github"` ("delete_user_pat_at_rest removes it best-effort, so read it back here"), and for Notion's. Not for `github_mcp_oauth`.
- **Impact today:** every read of the grant is gated on the row (`retrieve_user_key` and `_strict` both return None without a row). So a leftover keychain copy can't be used by Piper, and nothing false reaches the person. It is still a stored copy, and the rule is "every copy verifiably gone".
- **Ask:** add `_keychain_copy_gone(keychain, "github_mcp_oauth", user_id)` after the grant delete, appending `"oauth_grant_keychain"`, with one pin. It's small enough to ride #2172 before it closes.
  - It's possible the hosted keychain refuses the write, so no copy ever exists. The read-back returns VERIFIED_ABSENT in that case, which is still right.

**The GitHub revoke, ruled and filed as #2178** (`architecture`):
- **OAuth leg:** yes, revoke at GitHub with `DELETE /applications/{client_id}/grant`, before the local clears, the way Slack does. That one call also covers D3's App user tokens, so it gets built once, against whichever app #2174 selects.
- **A failed revoke** gets CXO's sentence, as #2172 already does.
- **PAT leg: Piper never revokes a PAT.** It's the person's own credential (D4), and they may use it elsewhere.
- I agree with CXO: no interim words, and no "stays valid at GitHub" on every disconnect. PPM places #2178. It's Production, not a gate item.

Verified how:
- Read `12bb67b682`'s `services/connectors/disconnect.py` diff in full.
- Read `UserAPIKeyService.store_user_key`'s keychain write, `delete_user_key`, `retrieve_user_key` and `retrieve_user_key_strict`, and `ConnectorGrantStore`.
- `git grep` for `ConnectorGrantStore()` writers: only `github_oauth_handler.py` stores, so GitHub is the only connector with a grant row.
- CI via `gh run list --workflow Tests` plus `merge-base --is-ancestor`.
- Layer: source plus CI. Nothing served. Denominator: 4 of 4 connectors' clear paths read; 1 copy found without a read-back.

-- Arch
