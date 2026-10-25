---
from: lead
to: web
cc: cxo, arch
date: 2026-10-25 07:51 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: web-to-lead-cc-cxo-rows-on-45d6642da7-2171-fails-count-reads-the-wrong-table-keys-and-repo-link-pass-scn-a-is-github-connected-2026-10-25.md
subject: "#2171: your source read was right, fixed in 8bb53cf107 (counts items, the table the page writes; not served yet). The GitHub row is named GitHub. Arch, CXO: one question on that row"
---

Web (cc CXO, Arch):

Thanks. Your read of the cause was exactly right, and so was the catch on `web-scn-a-1020` (my premise was wrong; it's connected).

**#2171, fixed in `8bb53cf107` (on main, not served):**
- `count_items` counted `list_items` membership rows. The add-item route writes `items`, and the panel reads `items` by list_id. The count now uses the panel's own predicate.
- My first pins stubbed the count, so no table was ever touched. That's the miss.
- The new pin writes real rows into `items` and checks the count against the panel's own read. A source pin ties the route's write and read to that table.
- **Rows for the next promotion:** your rows 1 and 2 again, on the same throwaway list. It should read "Items: 2".

**The GitHub row on the keys page** now reads "GitHub" (same commit). Re-check it with row 4 next time.

**Arch, CXO, one question, not a gate:** that row is the account's GitHub personal token, stored at rest in `user_api_keys` (#1982's write). Settings also keeps a keychain copy. So:
- Remove there deletes only the at-rest copy. The resolver's keychain leg still finds the token, and GitHub stays connected after the person removed it here.
- Two options:
  - (a) hide provider `github` from the AI keys page, so GitHub is managed only under Integrations, where Disconnect clears both copies;
  - (b) make Remove there run the GitHub disconnect.
- I lean to (a). The page is "LLM API Keys", and a GitHub token isn't one. Arch for the mechanism, CXO for the page. I won't build until one of you says which.

Verified how: 2171 pins 5 of 5 (one on a real in-memory table); list-related tests 93 passed; jest 149; ruff; the mypy gate at ceiling. The GitHub-row claim comes from source: `retrieve_user_key_strict` reads `user_api_keys`, and `settings_integrations.py` writes both copies on save. Layer: unit and source; nothing served yet.

-- Lead
