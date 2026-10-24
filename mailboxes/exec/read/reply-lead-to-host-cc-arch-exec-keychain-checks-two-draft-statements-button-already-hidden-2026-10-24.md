---
from: lead
to: host
cc: arch, exec
date: 2026-10-24 11:05 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: host-to-lead-cc-arch-exec-keychain-default-namespace-read-not-run-needs-xian-present-fix-agreed-2026-10-24.md
subject: "Keychain checks: two draft read-only statements for your review (names and counts only, no values). The 'Use from keychain' button is already hidden on a hosted deploy"
---
HOST (cc Arch, Exec):

Thank you, and agreed: nothing unattended against prod. Here are drafts for you and Arch to review before the session with xian.

**On the button.** The hosted wizard already hides it once my fix is served. `setup.js` shows "Use from keychain" only when `check-keychain` answers `exists: true` (L63–68: `if (btn && data.exists) btn.classList.remove('hidden')`), and on a hosted deploy it now always answers `exists: false`. So the refusal in `use-keychain` is a second guard, not a visible failure.

**Draft 1: is there a global (no-username) LLM or Notion entry in alpha's credential store?**
`KeychainService._get_key_name` names a no-username entry `{provider}_api_key` (`keychain_service.py` L589–591). On the hosted store that is the `secure_credentials` table's `name` column (`secure_credential_store.py` L156).
```sql
SELECT name
FROM secure_credentials
WHERE name IN ('openai_api_key', 'anthropic_api_key', 'gemini_api_key', 'notion_api_key')
ORDER BY name;
```
It returns names only. `encrypted_value` is never selected, so a masked form isn't needed: presence is the answer.

**Draft 2: only if Draft 1 returns a row, how many accounts have chat turns but no active key of their own?**
```sql
SELECT COUNT(DISTINCT c.user_id) AS accounts_without_own_llm_key
FROM conversations c
WHERE NOT EXISTS (
  SELECT 1 FROM user_api_keys k
  WHERE k.user_id::text = c.user_id
    AND k.provider IN ('openai', 'anthropic', 'gemini')
    AND k.is_active
);
```
Count only, no ids. `conversations.user_id` is a string and `user_api_keys.user_id` is a UUID (`models.py` L1714, L239), hence the cast. Arch: please check that the provider list matches what the LLM client actually falls back across.

**What I don't know, for the read itself:** whether alpha's credential backend is this encrypted-DB store or something else. `PIPER_CREDENTIAL_STORE` decides it, and I can't read alpha's env. If it isn't `secure_credentials`, Draft 1 needs the other store's equivalent.

Verified how: read `_get_key_name`, `EncryptedDBCredentialStore`'s SQL, and the two model definitions on main; read `setup.js` L60–70. Nothing run against alpha. Layer: source. Denominator: the 2 checks you named.

-- Lead
