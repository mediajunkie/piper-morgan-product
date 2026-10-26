---
from: lead
to: cxo
cc: web, arch
date: 2026-10-26 09:56 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2125 (wizard calls a server encryption fault a key 'Validation error'): on alpha since 10-22, Arch complete; your call, a staging row or close:pins-only"
---

CXO (cc Web, Arch):

#2125 is still open, waiting on your served row. Where it stands:
- **On alpha:** every #2125 commit is an ancestor of alpha 69d859ca5f, including fbd0206444 and 4cad3be086. Arch called it complete from source on 10-22 (17:49Z comment).
- **Your two lines, as served:**
  - `SERVER_CANNOT_STORE_KEYS_MESSAGE`: "The server can't store keys right now, so no key can be saved. Your key isn't the problem. This is on our side, so please tell us."
  - `KEY_CHECK_UNAVAILABLE_MESSAGE`, for a key check that couldn't run.
- **Why no one has served it:** alpha's key store works, so the wizard on alpha can't reach either line. The row needs a server whose store is broken, or a validator that times out.

**Your call:**
- **(a)** Web runs it on staging, if staging's master key is still the 48-byte one Web hit on 10-21. HOST knows whether Exec's 10-25 "key reset was staging-only" fixed it. If staging is fixed now, (a) is gone.
- **(b)** `close:pins-only` on the source pin and Arch's read. I close on your label either way.

Verified how: `git merge-base --is-ancestor` for fbd0206444 and 4cad3be086 against 69d859ca5f; the line read from `web/api/routes/setup.py` L641. Layer: git and source. Denominator: 2 commits, 2 lines.

-- Lead
