---
from: arch
to: ppm
cc: cxo, exec, lead
date: 2026-11-01 06:45 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "PDR-102: answers to Q1, Q2, Q5; a new #2226 condition (m); a proposed C7"
---

PPM (cc CXO, Exec, Lead),

I read the draft against the tables and the ingest and summarize code. The constraints hold with one exception: C2 for connector documents needs a schema decision. That decision isn't needed before #2226 or #1624. It's needed before the first connector-ingest unit.

**Q1. Can C2 and C4 hold with today's tables?**
- **Uploads (#2226): yes, with one condition I've added as (m) on #2226.**
  - Today a document's knowledge id is `"pdf_" + md5(file)[:8]` (`ingestion.py:247`), and `documents.chromadb_base_id` is unique across all accounts. `upsert_document` reassigns the owner when the id exists, so a second account uploading the same PDF would take the first account's row.
  - It's latent: the web upload route doesn't ingest into the knowledge store yet, and only the CLI calls `ingest_path`.
  - (m): the id becomes the owner's `uploaded_files.id`. `documents` gains `uploaded_file_id` (FK, cascade) and a full content hash as its version. That also gives C2's "which item, which version" for uploads.
- **Connector documents: no, not with today's schema.**
  - `documents.source` is a free string (a filename or a path), with no connector, item id or version.
  - Nothing ingests from a connector today, so nothing breaks C2 now.
  - Rule: **an ADR before the first connector-ingest unit is scheduled.** It adds a typed source (uploaded, generated, connector) plus connector, external id and version columns. I'll write it when that unit is placed. Placing one is the trigger. #2226 and #1624 don't need it.
- **C4: yes, no ADR.**
  - `artifacts` already has `source_type` and `source_conversation_id`.
  - Rule: the first unit that persists a document-derived artifact records `payload["derived_from"] = [{document_id, version}]`, with a pin test.
  - As far as I read, #1624's summarize answers in chat and doesn't persist an artifact, so it isn't that unit unless its scope changes.

**Q2. Is C6 already true?**
- **Generative calls: true across hosted vendors.** The document analyzer calls `LLMClient.complete`, which picks among `anthropic`, `openai` and `gemini` per user (#2131).
- There's no local provider. Adding one is a new `LLMProvider` member and client, not a redesign.
- Unverified: whether the analyzer's `response_format={"type": "json_object"}` works on every provider. I didn't trace the Anthropic and Gemini adapters.
- **Embeddings: not true today.** They're OpenAI-only (`RequestKeyedOpenAIEmbeddingFunction`). #2226's ruling replaces it with local MiniLM, after which C6 holds there too.
- Record it in the PDR as one single-vendor point, closed by #2226.

**Q5. What's missing?** I propose **C7: derived knowledge has its source's scope and lifetime.** Chunks, embeddings and summaries are readable by exactly who can read the document (#1238's owner scoping already enforces this on reads). They're deleted when the document or the account is deleted.
- Unverified: whether deleting an account removes its vector-store chunks today. `uploaded_files` cascades from `users`, and `documents.owner_id` has no cascade declared. Whoever builds #2226 should check and pin it.
- Without C7, "your data" in C3 has no delete half.

Q3 and Q4 are CXO's.

Recorded in decisions.log at 06:44. Condition (m) is on #2226 (comment 6559473742).

Verified how: I read `services/database/models.py` (`DocumentDB`, `UploadedFileDB`, `ArtifactDB`, `ArtifactSourceType`), `document_service.py:40-160`, `document_repository.py:80-105`, `ingestion.py:28,247`, `document_analyzer.py:200-216` and `services/llm/config.py:10-14`. I grepped for callers of `ingest_path` and `upload_pdf` outside tests. Layer: source, nothing run. Denominator: the document tables and the one upload-to-knowledge path. The Notion and Slack connectors weren't read, since they ingest nothing.

-- Arch
