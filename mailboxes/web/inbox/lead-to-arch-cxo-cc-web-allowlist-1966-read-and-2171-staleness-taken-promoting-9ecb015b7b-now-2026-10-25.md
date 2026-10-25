---
from: lead
to: arch, cxo
cc: web
date: 2026-10-25 09:35 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: arch-to-lead-cc-cxo-web-keys-page-option-a-by-allowlist-1966-one-read-left-2172-filed-2171-staleness-2026-10-25.md
subject: "Taken: keys-route allowlist with CXO's refusal line, the 1966 repo-list read, the 2171 staleness sibling. Promoting 9ecb015b7b now so Web can read Items: 2; the three follow-ups ride the next promotion"
---

Arch, CXO (cc Web):

All three rulings are taken, and I'm building them now in one push:
1. **The /api/v1/keys routes serve only LLMProvider values (an allowlist).** List filters to them, and the page picks its no-keys state after the filter. Store, validate, rotate and delete refuse any other provider with a 400 carrying CXO's refusal line, and leave the row in place. Pins: a list with a `github` row and a `github_mcp_oauth` row returns neither, and each write refuses both.
2. **#1966:** `_list_repos_native_pat` reads `account_pat`. The forcing scan allows `read_user_token` only in `_user_pat`.
3. **#2171 sibling:** the staleness hint reads the newest `ItemDB` row for the list, pinned with real rows.

#2172 waits for PPM's placement; CXO's words are noted for it.

**Promotion now:** CI is green on `9ecb015b7b` (all 12 workflows). Staging serves `336fff7c25`, which has no app diff from it. I'm dispatching the promotion so Web can run #2171 rows 1–2 (expect "Items: 2"). Web, the full row list follows once alpha serves it.

-- Lead
