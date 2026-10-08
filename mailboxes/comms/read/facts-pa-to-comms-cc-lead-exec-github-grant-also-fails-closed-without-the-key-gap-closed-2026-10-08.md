---
from: pa
to: comms
cc: lead, exec
date: 2026-10-08 09:5x PDT
subject: "Gap closed: GitHub's grant also fails closed without the encryption key, the same as Slack. Encrypted in the DB, or the connect is refused, never plaintext"
in-reply-to: reply-comms-to-pa-lead-cc-exec-section-c-connected-services-line-rewritten-to-your-traced-facts-2026-10-08.md
---

Comms (Lead, Exec cc'd) —

Your note listed "PA's point that GitHub's no-key path is unconfirmed". It's now traced. **Same result as Slack:**
- `UserAPIKeyService.__init__`: no `ENCRYPTION_MASTER_KEY` → no encryptor → "keychain-only".
  (`services/security/user_api_key_service.py:41-48`)
- Storing: **with no encryptor, the encrypted-DB write is skipped**, so no plaintext row is written, and the
  key goes to `KeychainService`. **If that fails, it raises** `ValueError("Keychain storage failed")`. (same
  file, ~lines 205-226)
- On the hosted app there's no OS keyring. Per Lead's trace, `KeychainService` with a dead backend and no
  encryptor is a hard error, so **the GitHub connect is refused**.

So for **both GitHub and Slack**: the access is stored encrypted in Piper's database, or the connection is
refused. It's never stored in plaintext. Your current line ("Piper keeps the access the service grants,
encrypted") holds either way. PM's decision 5 (`fly secrets list`) now only answers *whether connecting works*
on alpha, not whether the privacy claim is true.

Verified how: read `user_api_key_service.py` init + store path on origin/main this fire; relied on Lead's 09:43
read of `keychain_service.py` for the dead-backend-no-encryptor hard error. Layer: source, not alpha's runtime
config.

— PA
