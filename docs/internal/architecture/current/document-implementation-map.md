# Document implementation map (as built)

- **Author**: Arch (Chief Architect), 2026-11-26, at xian's request (Exec 01M8CFVC6M).
- **Purpose**: the built picture of documents, for a later comparison with the MUX vision for documents (`docs/internal/design/mux/`). This map makes no comparison and no recommendations; the last section lists the facts a comparison will need.
- **Read at**: `origin/main` `3151f88377`. The document code paths below are identical at beta's served build `cf3486389e`: `git diff --stat cf3486389e origin/main` on every file named here is empty.

**Verified how**: a read-only sweep by an Explore subagent (Sonnet), then Arch re-read each load-bearing claim from source:
- who writes the index: `git grep` for `ingest_pdf(`, `_ingest_and_anchor`, `upload_pdf`, `ingest_path` and `collection.add`;
- whether the CLI is imported anywhere;
- the chat `search_documents` entry;
- the `/documents` redirect;
- the `/api/v1/documents` callers in templates and JS;
- the chunker.

"Served" in this map means **the code is in the build beta serves**. It does not mean a served read of beta: I made no browser or HTTP read of these paths today. Where a served read exists elsewhere, it is cited.

---

## 1. The headline: two stores that never meet

Documents live in **two independent stores**, and no served path connects them.

| | **Upload store** | **Knowledge index** |
|---|---|---|
| What it holds | The file a person uploaded (encrypted bytes on disk) plus a DB row | Text chunks of PDFs with embeddings, plus an ownership anchor row |
| DB table | `uploaded_files` (`UploadedFileDB`, `services/database/models.py:1593`) | `documents` (`DocumentDB`, `models.py:614`), the ADR-071 anchor |
| Bytes | `UPLOAD_DIR/<user>/<ts>_<id>_<name>` (`/data/uploads` on Fly, on the volume since #1401) | Chroma `PersistentClient`, collection `pm_knowledge` (`services/knowledge_graph/ingestion.py:76`, `:102`); `./data/chromadb`, which is the machine's own disk on Fly until #2244 lands |
| Written by | `POST /api/v1/files/upload` (`web/api/routes/files.py:81`) | `DocumentService._ingest_and_anchor` (`services/knowledge_graph/document_service.py:129`) only |
| Written in practice by | Every person who uploads on the Documents page | **Nothing served.** `_ingest_and_anchor`'s callers are `upload_pdf` (no callers) and `ingest_path`. `ingest_path`'s one caller is `cli/commands/documents.py:112`, a click CLI run as `python -m cli.commands.documents`, which nothing in the app imports. Also `scripts/backfill_documents_1238.py`, an operator script. |
| Read by | Summarize, analyze, question, compare and reference (REST and chat) | `find_decisions` (search), `get_relevant_context`, `suggest_documents`, and the Radar feed's `list_for_user` |

What follows:
- **An upload is never indexed.** Nothing embeds or chunks it. Every served document feature works on the upload store by reading the file's text at request time (§4).
- **On beta the knowledge index holds only what an operator put there with the CLI or the backfill.** It is also emptied at every deploy until #2244, so it is most likely empty. That is inferred and has not been read on the machine.
- **#2244 still matters**, because #2226's local-embedding plan requires a durable store first (decisions.log 2026-10-31, the line naming `pm_knowledge_minilm_l6`). But its served check, "an ingest that survives a second deploy", can only be produced through the operator CLI today, not through the product.

---

## 2. Stage by stage

Status key: **S** = in the served build and reachable from a served page or chat. **B** = built but not reachable from any served surface. **K** = refuses without the person's own OpenAI key (until #2226). **L** = needs the person's own LLM key (any provider).

### 2.1 Upload (S)
- **Route**: `POST /api/v1/files/upload` (`files.py:81`).
- **Limits**: up to 10 MB (`:59`). Types are `.txt .pdf .docx .md .json` (`:60`, `:67`); refused with 413 (size) or 415 (type).
- **Write path**:
  - The bytes are encrypted with `FieldEncryptionService` (`services/file_context/storage.py:88`).
  - In production with no `ENCRYPTION_MASTER_KEY`, the route answers 503 "Piper can't store files right now." (`files.py:188-194`).
  - The DB row is written after the file; if the row fails, the file is removed (`:252-256`).
  - A boot probe checks the upload folder is writable (`web/startup.py`, `UploadStorageProbePhase`, #1656).
- **What it doesn't set**: no project, no conversation, and no index write.
- **Other routes on the store** (S): `GET /list` (uploads plus artifacts, #355), `GET /{id}`, `/download`, `/preview`, `POST /download-bulk`, `PUT /{id}/tags`, `DELETE /{id}`.
- **Page**: `templates/files.html`, served at `/files` under the nav label "Documents" (`templates/components/nav_rail.html:68`). It covers upload (drag and drop), list, tags, preview, bulk download, delete, and renaming an artifact.

### 2.2 Text extraction (S for the upload store; B for the index)
- **Upload store**: `services/analysis/document_analyzer.py`.
  - `classify_document_type` (`:62`) returns pdf, text or unknown.
  - `extract_document_text` (`:96`).
  - **`.docx` is accepted at upload and classifies as unknown**, so analyze and summarize answer the unsupported message for it.
- **Index**: PDF only, `pypdf` (`ingestion.py:318`); `upload_pdf` and `ingest_path` refuse anything else.

### 2.3 Chunk and enrich (B, K, L)
- **Chunking**: `ingestion.py:312-335`. Chunks are 1,000 words with a 200-word overlap. Note for #2226: a 256-token window, its stated condition, is far smaller than a 1,000-word chunk.
- **Enrichment**: one LLM call per document, on the first chunk (`_analyze_document_relationships`, `task_type="relationship_analysis"`). It is **called twice** (`ingestion.py:242` and `:254`), a duplicated block.
- **Chunk metadata**: the analysis keys (`main_concepts`, `document_type`, `project_area`, …) plus `source`, `chunk_index`, `total_chunks` and `ingested_at`. **No `user_id` or `document_id` in chunk metadata.** `project_area` is a free-text string the LLM writes, not a project id.
- **Ids**: `pdf_<md5[:8]>_chunk_<i>`. The 8-hex-character base id is the join key to the anchor row.

### 2.4 Embed and index (B, K)
- **Embedding function**: `RequestKeyedOpenAIEmbeddingFunction` (`ingestion.py:25`), `text-embedding-ada-002`. It takes the request-bound key only, with no operator fallback (#1812). With no bound key it raises before any chunk is written.
- **Collection**: one shared collection, `pm_knowledge`. Ownership is not a collection or a Chroma filter. Reads over-fetch, then intersect base ids with the person's readable set from the `documents` table (`document_service.py:182-193`), fail-closed.
- **Unfiltered reads**: `DocumentIngester.search` and `search_with_context` (`ingestion.py:341`, `:420`) apply no owner filter. They have no callers outside that file.
- **#2226** (local MiniLM embeddings, new collection) is planned in decisions.log 2026-10-31 and `docs/internal/planning/2226-local-embeddings-weight-lead-2026-10-31.md`. No code for it exists yet.

### 2.5 Search
- **REST**: `GET /api/v1/documents/search` (`web/api/routes/documents.py:462`, **B, K**) calls `handle_search_documents` and then `find_decisions` over the index. Its only page caller is `templates/documents.html:537`, which is unreachable: `GET /documents` redirects to `/files` (`web/api/routes/ui.py:568-581`, #1270 band-aid).
- **Chat** (S): the `search_documents` intent (aliases `find_documents`, `search_notion`; `services/intent_service/workflow_entries.py:4582-4597`) goes to `_handle_search_documents_notion` (`services/intent/intent_service.py:6890`).
  - It is a **Notion** search. It never reads uploads or the index.
  - Without Notion, chat says it can't search documents from chat yet.
- **Radar** (S): `services/radar/sources.py:132` lists the person's `documents` rows (anchor table), not uploads.

### 2.6 Summarize, analyze, question, compare, reference (S for summarize and analyze in chat; L)
- **Engine**: `handle_analyze_document` (`services/intent_service/document_handlers.py:81`) loads the upload row by id and owner (or an owned artifact, #1657), then calls `DocumentAnalyzer.analyze` (`document_analyzer.py:130`).
- **Summary call**: one LLM call, `task_type=summarize`, JSON response, over **the first 3,000 characters** of the text (`document_analyzer.py:210-215`, `:327-331`). The prompt is `JSON_SUMMARY_PROMPT` (`services/prompts/summarization.py:123`). The output is parsed into the domain `DocumentSummary` (`services/domain/models.py:1140`) and rendered as markdown.
- **Formats**: `handle_summarize_document` (`document_handlers.py:306`) offers bullet, paragraph and detailed.
- **Chat** (S): `summarize_document` goes to `run_summarize_document_workflow` (`workflow_entries.py:1320`). It resolves the file with `FileResolver` (uploads plus artifacts) and picks the format from the person's words. `analyze_document` in chat reaches `handle_analyze_document` through `_analyze_bound_held_file` (`intent_service.py:7248`).
- **REST only** (B; `/api/v1/documents/{id}/…`, page callers only in the unreachable `documents.html` and `document_window.html`):
  - question, over the first 4,000 characters (`document_handlers.py:285-294`);
  - compare (`:371`);
  - reference in conversation (`:492`).

### 2.7 Delete and erase
- **Per-file delete** (S): `DELETE /api/v1/files/{id}` (`files.py:490`) removes the file and the `uploaded_files` row. It touches neither the index nor the anchor table, which is consistent with §1, since an upload is never indexed.
- **Account erase** (`scripts/erase_user.py`, operator): runs grants, then upload files, then index chunks (matched through the person's `documents.chromadb_base_id` rows), then Postgres, then Redis.
  - **Chunks with no anchor row are not found.** Anchoring is best-effort (`_anchor_document` logs and continues on failure, `document_service.py:154`).
  - After #2244, erase reads the same store path as the app.
  - Volume snapshots keep a copy until they age out (HOST's custody note, 01M8CFD6V6).

---

## 3. Domain objects: code versus models

Columns follow `docs/internal/design/mux/objects-catalog.md` (identity, persistence, lifecycle, ownership, relationships).

| Object | Where | Persisted | Lifecycle | Owner and anchor | Relationships | Used by served code? |
|---|---|---|---|---|---|---|
| `UploadedFile` / `UploadedFileDB` | `domain/models.py:791`, `database/models.py:1593` | `uploaded_files` | none | `owner_id` FK users, NOT NULL, cascade | none: no project, no conversation | **Yes**, the live document object |
| `DocumentDB` (anchor) | `database/models.py:614` | `documents` | none | `owner_id` NOT NULL (ADR-071 D2); `is_global_pm_domain` (D1 exemption) | `chromadb_base_id` → index chunks; no link to `uploaded_files` | Read by Radar and search; written only by the CLI and the backfill |
| `Document` | `domain/models.py:834` | no table | none | none | none | **No.** No non-test importer |
| `DocumentSummary`, `SummarySection` | `domain/models.py:1140` | response only | n/a | n/a | n/a | Yes (summarize) |
| `DocumentSample`, `ContentSample` | `domain/models.py:1085` | no | n/a | n/a | n/a | No |
| Index chunk | Chroma `pm_knowledge` | Chroma | none | none in metadata; ownership only through the anchor join | `project_area` free text | Only through the index readers above |

**Where code and models disagree**:
1. **The MUX catalog's "Document → UploadedFile" is not built.** The domain `Document` has no table and no caller. The anchor `DocumentDB` is a different thing, an index ownership record, and it has no link to `UploadedFile`.
2. Two objects are both called "document": the upload a person sees on the Documents page, and the index entry behind search. They share no id.
3. Neither store relates a document to a project or a conversation. The only project-like field is the LLM's `project_area` string on index chunks.
4. The catalog lists Document and UploadedFile with no lifecycle. That matches the code: neither has a lifecycle state.

---

## 4. Surfaces at a glance

| Surface | Reaches | Status |
|---|---|---|
| `/files` page ("Documents") | upload, list, tags, preview, download, delete | S |
| Chat "summarize / analyze <file>" | upload store, through `FileResolver` | S, L |
| Chat "search / find documents" | Notion only | S |
| Radar feed | `documents` anchor rows | S |
| `/api/v1/documents/search` | index | B, K (no reachable page) |
| `/api/v1/documents/{id}/question`, `/compare`, `/reference` | upload store | B, L (no reachable page) |
| `templates/documents.html`, `components/document_window.html` | the above | B: redirected; listed as dead in `tests/test_completion_ratchets.py:334-336` |
| `python -m cli.commands.documents` | index ingest and search | operator only, K |
| `scripts/backfill_documents_1238.py`, `scripts/erase_user.py` | index and anchor | operator only |

Settings that touch documents:
- `UPLOAD_DIR`;
- `ENCRYPTION_MASTER_KEY`;
- `PIPER_DATA_DIR` (from #2244);
- `PIPER_PM_USER_ID` (global-domain owner);
- `ENABLE_MCP_FILE_SEARCH`, default off (`file_resolver.py`);
- `ENABLE_KNOWLEDGE_GRAPH`, default off. It gates the separate `KnowledgeGraphService` node store, not this index.

No flag gates uploads.

## 5. Unreached code (no non-test caller found)

- `services/knowledge_graph/processors.py` (`PDFProcessor`, a second copy of the chunker)
- `DocumentService.upload_pdf`
- `DocumentIngester.search` and `search_with_context`
- The domain `Document`, `DocumentSample` and `ContentSample`
- `templates/documents.html` and `components/document_window.html` (redirected)
- `templates/home.html`'s upload CSS and `UPLOAD_CONFIG`, which no markup uses
- `history_sidebar.html:725` still links to `/documents`, which redirects

## 6. Facts the MUX comparison will need

These are questions the built picture raises, for xian and CXO. They are not rulings.
1. Which "document" does the vision mean: the file a person uploads, the indexed knowledge, or one object that is both? Today they are two objects with no shared id.
2. Should an upload be indexed? Today it never is, so semantic search over a person's own uploads does not exist on any served surface.
3. Should documents belong to projects or conversations? Neither store has the relation.
4. The summary reads only the first 3,000 characters of a document.
5. `.docx` is accepted but can't be read.
6. Chat's "search documents" means Notion.
