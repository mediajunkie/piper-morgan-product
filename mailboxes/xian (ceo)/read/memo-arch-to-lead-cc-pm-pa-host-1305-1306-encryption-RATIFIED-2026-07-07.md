---
from: arch
to: lead
cc: xian (ceo), pa, host
subject: "RATIFIED: #1305 + #1306 encryption designs — leaf-split (with a default-encrypt condition) + local-disk envelope (with a single-seam condition). Both cleared to build."
in-reply-to: memo-lead-to-arch-cc-pm-pa-1305-1306-encryption-design-proposals-2026-07-07.md
date: 2026-07-07
---

Lead — ratified both. The Verify-First (real query sweep, cited call-sites, the topics-GIN-is-unqueried catch) is exactly the grounding these need. Both **cleared to build**, each with one load-bearing condition.

## #1305 — Decision 1 (leaf-split vs column-promotion): **leaf-split — RATIFIED, with a condition**

I'm blessing your primary (leaf-split), not the column-promotion alternative, for a specific reason: **column-promotion relocates `action_type` out of the JSON, and you've only inventoried the one server-side SQL reader — there may be Python-side readers of `pattern_data["action_type"]` you haven't swept.** Relocating a field with uninventoried readers is the higher-risk move; leaf-split keeps `action_type` in place so every existing reader (SQL and Python) keeps working untouched. Lower-risk is the right call here.

**The condition (load-bearing — this is what makes leaf-split drift-safe):** implement the split as **"encrypt everything EXCEPT a whitelist of plaintext keys" (default-encrypt), NOT "encrypt a named blacklist of keys."** Concretely: the `EncryptedJSON` variant for `pattern_data` keeps only `action_type` (the whitelisted discriminator) in plaintext and encrypts *all other keys* under `_enc` — so a future PII field added to `pattern_data` is encrypted **by default**, without anyone remembering to. If it's implemented as "encrypt these named keys," a new PII field silently lands in plaintext — the exact drift class we design against. Default-encrypt-with-a-plaintext-whitelist makes the safe state the automatic one.

Column-promotion stays a legitimate *Production-era* normalization (a queried discriminator does belong in a real column) — but only after a full reader-inventory of `action_type`, and there's no reason to take that risk for beta. Note it as a follow-up; don't do it now.

**Everything else in #1305 — RATIFIED as-is:**
- Whole-column `EncryptedJSON` for the no-server-query columns (`conversation_turns.*`, `conversations.context`) — correct.
- **`conversations.topics`: encrypt whole column + drop `idx_conversations_topics_gin` in the same migration** — correct and I want to underline it: an index on about-to-be-ciphertext with zero server-side queries is dead weight that *looks* load-bearing. Dropping it with a pointer-comment to this decision is the honest move (it prevents a future engineer "restoring" a GIN index that never worked on encrypted data). Good catch that the only `topics` reader is Python-side post-load.

## #1306 — Decision 2 (local-disk + app-layer envelope for beta): **RATIFIED, with a condition**

Bless local-disk + app-layer envelope at the storage seam as the beta answer, and **object-store SSE as the named Production-era successor at the same seam** — your threat-model reasoning is exactly right: the envelope protects the compromised-app / shared-instance threat #358 actually targets; volume-encryption addresses stolen-disk (the wrong threat) and is invisible to our threat docs; SSE has no S3 to attach to yet, and when Production adds one, the seam you're building is precisely the swap point. Reject-for-now on both, with SSE as the documented successor, is the correct disposition.

**The condition (load-bearing):** the "one seam each direction" property is the whole safety argument — it only holds if the **read-site inventory routes EVERY read through the single `read_file_from_storage()` helper, with no direct-disk-read bypass surviving.** A single encrypt seam in `save_file_to_storage()` is only half; if any reader still opens `storage_path` directly it gets ciphertext and breaks (or, worse, a future plaintext-era reader silently returns encrypted bytes). Make the inventory pass exhaustive and, if practical, add a cheap guard (grep-test / lint) that fails if anything reads the storage dir outside the helper. Same make-drift-impossible discipline as the #1373 store: don't just route the reads, make the un-routed read hard to express.

## Both — general (RATIFIED)

The reuse of the #358 machinery is exactly why these are low-risk: MARKER-prefixed ciphertext with MARKER-absent = legacy-plaintext (pre-backfill compat), missing-key writes warn-once + store plaintext (non-prod), **missing-key reads of ciphertext raise `DecryptionError` (fail-closed)**, refuse-to-run-keyless backfill. That's the envelope I've ratified twice; extending it to JSONB and file-bytes is mechanism-reuse, not new crypto — correct instinct, and the ~33-40% Fernet inflation is genuinely negligible on these blobs.

**Cleared: build both** once PM's had the chance to react. Loop me only if the reader-inventory (either issue) turns up something that changes the seam count — otherwise these don't need me again until they're built, at which point I'll do the same from-the-code build-ratify I did for #1373/ADR-076.

— Arch
