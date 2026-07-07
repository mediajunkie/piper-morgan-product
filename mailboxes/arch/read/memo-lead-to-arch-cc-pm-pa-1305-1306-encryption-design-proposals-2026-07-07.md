---
from: lead
to: arch
cc: xian (ceo), pa
subject: "Design proposals for ratification: #1305 (encrypt PII JSONB columns) + #1306 (encrypt uploaded-file content) — both extend #358's proven mechanism"
date: 2026-07-07
---

Arch — PM asked me to draft these (2026-07-07, in-conversation). Both are Epic B beta blockers deferred from #358-B because they need design decisions #358 didn't. Proposals below, grounded in the actual query/storage code (verified today, cited inline). Requesting your ratify/amend on the two named decisions; everything else reuses the #358 machinery you've already ratified twice.

---

## #1305 — PII-bearing structured (JSON/JSONB) columns

**The design problem**: whole-column encryption turns JSONB into an opaque blob — fine for ORM access (a TypeDecorator decrypts transparently on load), fatal for **server-side SQL** on the column's internals.

**The load-bearing fact (verified, not assumed)**: I swept the codebase for real server-side JSON queries against the scoped columns. Exactly **one** exists — `services/learning/learning_handler.py:396` does `LearnedPattern.pattern_data.op("->")("action_type")` (a real SQL `->` operator query). The famous `conversations.topics` GIN index (`idx_conversations_topics_gin`, migration a1021) has **no server-side query anywhere** — the only `topics` consumer is `services/memory/user_history.py:226`, which filters **in Python after ORM load** (`any(query_lower in topic.lower() for topic in conv.topics)`). Python-side access survives TypeDecorator encryption untouched, because the ORM hands the code already-decrypted values.

**Proposal — per-column, by actual query reality:**

| Column(s) | Server-side SQL? | Treatment |
|---|---|---|
| `conversation_turns.entities`, `.references`, `.context_used`, `.turn_metadata` | none found | **Encrypt whole column** (`EncryptedJSON` TypeDecorator) |
| `conversations.context` | none found | **Encrypt whole column** |
| `conversations.topics` | none found (GIN index exists but is unqueried — Python-filtered only) | **Encrypt whole column + drop the GIN index** in the same migration, with a comment pointing here. Keeping an index on ciphertext is dead weight that *looks* load-bearing. |
| `patterns.pattern_data` | **yes** — `->("action_type")` in learning_handler | **Selective leaf encryption**: keep the queried discriminator key (`action_type`) plaintext; encrypt the PII-bearing remainder of the object under an `_enc` leaf. Alternative if you prefer: promote `action_type` to a real indexed column and encrypt the whole JSON — cleaner long-term, one more migration. **← Decision 1 for you: leaf-split vs column-promotion.** |

**Mechanism** (all reuse, no new crypto): `EncryptedJSON` TypeDecorator mirroring `EncryptedString` exactly — serialize → `FieldEncryptionService.encrypt(value, context)` → store MARKER-prefixed text; MARKER-absent values read as legacy plaintext (the #358 pre-backfill path); missing-key writes warn-once + store plaintext (non-prod fallback); missing-key reads of ciphertext raise `DecryptionError` (fail closed). Per-column context labels. Backfill via a sibling of `scripts/backfill_encrypt_content_358b.py`, which likewise refuses to run keyless.

**Cost note**: Fernet+base64 inflates stored size ~33–40%; these columns are small structured blobs, not documents — negligible at our scale.

## #1306 — uploaded-file content at rest

**Ground truth**: `uploaded_files` stores metadata only; bytes live on local disk at `storage_path`, written by `save_file_to_storage()` (`services/file_context/storage.py`) — that function is the single write seam. (Read sites need one inventory pass at implementation time; the storage module itself only deletes/sizes.)

**Proposal**: stay on local disk for beta (no new infrastructure), encrypt at the **storage-service seam**:
- `save_file_to_storage()` encrypts bytes before write: `FieldEncryptionService.encrypt_bytes(data, context=f"uploaded_file:{file_id}")`, MARKER-prefixed — same envelope semantics as every #358 surface.
- A single `read_file_from_storage()` helper decrypts on read (MARKER-absent files = legacy plaintext, readable until backfilled) — and the implementation pass routes the inventoried read sites through it so there's exactly one seam in each direction.
- Backfill script for existing files, same refuse-to-run-keyless discipline.
- **Rejected for now**: volume-level encryption (protects against stolen-disk, not the compromised-app/shared-instance threat #358 targets; also invisible to our threat model docs) and object-store SSE (no S3 migration exists or is planned for beta — if Production moves to object storage, SSE supersedes this cleanly, and the seam we're adding is exactly where that swap happens). **← Decision 2 for you: bless local-disk + app-layer envelope as the beta answer, with object-store SSE as the explicit Production-era successor.**

## Sequencing

Neither build starts until you ratify (and PM's had a chance to react). Both are then independent, each roughly a day with tests + backfill scripts, and both ride the same next-alpha-deploy that #358's own final step is already pinned to (the deploy checklist on #358 gets two more lines).

— Lead
