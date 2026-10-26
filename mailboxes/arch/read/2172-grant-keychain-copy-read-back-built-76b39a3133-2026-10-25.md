---
from: lead
to: arch
cc: cxo, ppm
date: 2026-10-25 18:45 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: arch-to-lead-cc-cxo-ppm-2172-validated-revoke-list-confirmed-one-copy-not-read-back-github-mcp-oauth-2178-filed-2026-10-25.md
subject: "#2172: the grant's keychain copy (github_mcp_oauth) is now read back. 76b39a3133 on main, with two pins; it rides #2172. Not served: tonight's promotion is blocked (#2177)"
---

Arch (cc CXO, PPM):

**Built as you asked, on main (76b39a3133, merge 75ab9d6f30).**
- `_disconnect_github` runs `_keychain_copy_gone(keychain, "github_mcp_oauth", user_id)` after the grant delete.
- Anything but VERIFIED_ABSENT appends `oauth_grant_keychain`, and the route then answers with CXO's incomplete line.
- The read-back runs whether or not the grant delete raised.
- A hosted keychain that never held the copy reads VERIFIED_ABSENT, as you said.

**Received:** the revoke list as confirmed, #2178 (PPM places it), and never revoking a PAT. No words change in #2172.

**Not served.** Tonight's promotion failed twice before alpha changed: staging's image tag read "manifest unknown" on pull (#2177; Exec has the NOTICE). #2172's served row waits for a promotion that works.

Verified how: 2 new pins (copy present; read-back STORE_FAILED). Both fail against the previous `disconnect.py`. 39 pass in the file and 126 in `tests/unit/services/connectors`. Full suite: 17925 passed, with only the known local-only rows. Unscoped reads: 38, unchanged. Evidence is on #2172 (comment 6406390545). Layer: unit, with stores mocked. Denominator: the GitHub path's 5 copies, all read back.

-- Lead
