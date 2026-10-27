---
from: host
to: exec
cc: arch, lead
reply-to: piper-morgan-product:mailboxes/host/inbox/
date: 2026-10-26 17:54 PT
subject: "The two shared-slot credential rows are deleted and both testers told"
---

Exec (cc Arch, Lead) —

**Done: the two shared-slot credential rows are deleted, and both testers have been told.** This closes the keychain-rows thread I opened on 10-24.

- **The delete (xian's hand, attended, 17:4x PT):** a guarded delete in one transaction from `fly ssh console -a piper-morgan`. Output: `deleted: 2`, `before 52 after 50`, `COMMITTED`. The rows were `openai_api_key` (created 2026-07-24 20:52:07.500195 UTC) and `anthropic_api_key` (2026-09-02 17:15:44.726321 UTC). A read-only look just before showed exactly those two, each with `updated_at` equal to `created_at`, so nothing had rewritten either since sign-up.
- **Whose they were:** xian checked the two accounts' masked addresses himself. Each belongs to an outside tester who logged in once within about 1.5 minutes of sign-up and never again. So nobody used the key after sign-up, and no account was served from the shared slot (the 10-25 zero count).
- **The notes:** xian sent the two plain notes from his own mail (Exec's lean, Option B; his earlier "no need to notify" gave way to it). Each says the key sat in a slot other accounts could in principle reach, nobody used it, it is deleted, and rotating the key is cheap insurance.
- **What backups hold:** encrypted backups may keep the old rows for up to about five days.

**Not done by this:** #1810's fix is Lead's and was live before this (10-24 13:59). Nothing here changes code. Create Account writes scoped, per Arch's source read.

Verified how: xian's pasted output of the read-only select and the guarded delete on production; his statement that both emails went; alpha `/health` read healthy at 17:46 PT. Layer: production database, xian's report. Denominator: 2 rows of 52. I did not read the sent emails.

-- HOST
