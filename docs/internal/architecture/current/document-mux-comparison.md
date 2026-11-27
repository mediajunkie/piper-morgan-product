# Documents: the MUX vision against what is built

- **Author**: Arch (Chief Architect), 2026-11-27, prep for the week-1 document discussion with xian (Tuesday 12-01; Exec 01M8F85S17).
- **Reads with**:
  - `document-implementation-map.md`, the built picture (2026-11-26);
  - CXO's person-side page, `docs/internal/design/mux/documents-person-side-cxo-2026-11-27.md`, which answers the map's six questions from the person's side. This page doesn't repeat it.
- **Sources for the vision**:
  - `docs/internal/design/mux/objects-catalog.md` (the Document and UploadedFile rows);
  - `views-objects-roadmap.md` ("Document Model (Future Implementation)" and "File vs Document Distinction");
  - `views-catalog.md`;
  - `artifact-model-design-952.md` (ratified 2026-06-08 and built);
  - issues 712 and 713 (Document Viewer and Documents lifecycle UI, both open).
- **What this is**: where the vision and the build agree, where they part, and the two decisions as options with their costs. These are options, not rulings. The decisions are xian's, with PPM and CXO.

## 1. The vision in four claims

1. **File and Document are two things.** A File is a static upload with no lifecycle. A Document is evolving content with a genesis (requested, seeded or derived), versions, and an optional lifecycle (`views-objects-roadmap.md`, "File vs Document Distinction").
2. **A Document points at its source File** (catalog: "Document → UploadedFile"; the model sketch: `genesis.source: File | Document`).
3. **Documents carry lifecycle** ("Depends on genesis"), shown in a Document Viewer and on the Documents view (712, 713).
4. **Artifact is the unifying lens** over uploads, analyzed documents, insights and generated content. Each keeps its own identity, and the lens doesn't flatten them (952, ratified: "flatten everything into one model" was rejected as MUX flattening).

## 2. Claim by claim, against the build

| Vision claim | Built | Gap |
|---|---|---|
| 1. File and Document are two things | **File is built:** `UploadedFile`/`uploaded_files`, owner-scoped, encrypted bytes, no lifecycle. **The vision's Document is mostly built as `Artifact`** (`artifacts`): owned content with `source_type` (generated), `source_conversation_id`, `lifecycle_state` and a payload. The domain class literally named `Document` has no table and no caller (map section 3). | **Naming.** What the vision calls a Document, the code calls an Artifact, and the code's own "Document" is dead. In the room, "document" needs one meaning. |
| 2. A Document points at its File | **No link.** `artifacts` has no file reference. The index's anchor (`documents`, ADR-071) has no link to `uploaded_files`. | Any Document-to-File relation is new: one nullable reference. |
| 3. Documents carry lifecycle | `artifacts.lifecycle_state` exists (nullable). Uploads have none, which matches the vision. There's no viewer; 712 and 713 are open. | The viewer and lifecycle UI are unbuilt. Nothing here is broken, only unbuilt. |
| 4. Artifact as the unifying lens | Built for generated content (#355): saved chat outputs, listed beside uploads on `/files` (`GET /api/v1/files/list`, uploads plus artifacts). The lossless round-trip exists in memory for three origin types; DB persistence covers the core fields (952's scope note). | The lens shows uploads and artifacts in one list, but there's no "upload became a document" step. |

**Outside the vision entirely: the knowledge index.** The vision doesn't name the index (the `pm_knowledge` chunks and their `documents` anchor). In the build it's a third store, written only by an operator CLI (map section 1). So the vision's question "is it a File or a Document" doesn't reach it. It's a search structure that either covers uploads or doesn't.

## 3. The two decisions, as options with costs

CXO's page calls these the two real product decisions (its questions 2 and 3). Here they are from the build's side.

### 3.1 Does an upload become searchable?

| Option | What it means in code | Cost and risk |
|---|---|---|
| **A. Index on upload, now** | Upload calls the existing ingest (`DocumentService._ingest_and_anchor`). The anchor row gains `uploaded_file_id`. Delete and erase follow the link. | It needs the person's own OpenAI key for embeddings until #2226 (map 2.4), so most testers get "can't search" anyway. The index has been on the volume since 11-26 (#2244, served from `cd26a9b2e4`), though its served "survives a deploy" row is still xian's CLI check. Shared base ids mean #2465 must land first. The extractor covers PDF only until #2443's table feeds the ingest too. |
| **B. Index on upload, after #2226** | The same code, gated on local embeddings (and #2244's served row). | Waits on #2226, which is planned with no code. #2244 is served; its last row is xian's CLI check. It's honest in the meantime only if no reply implies search over uploads (CXO's line). |
| **C. Uploads are never indexed; search stays Notion's** | Delete the unreached index readers, or keep them operator-only. Chat's "search documents" says where it searched. | Smallest. It closes the gap between the person's belief and the build by words, not by building. It forecloses "find the file where I wrote about pricing". |

**Arch's read of the build:** A and B are the same build at different times. The real choice is B or C. A only ships a feature that fails for most keys.

### 3.2 Does a document belong to a project?

| Option | What it means in code | Cost and risk |
|---|---|---|
| **A. An optional `project_id` on the upload** | One nullable FK on `uploaded_files`, set by the person ("add this to Launch"), the way #2297 put a project on todos. The project page lists it the way #2455 lists todos. | Small, and the pattern is proven: the same attach, lookup and confirm as #2297, and the same page section shape as #2455. One document has one project. |
| **B. Many to many (a link table)** | `project_documents (project_id, uploaded_file_id)`, like `project_repository_links`. | A document in several projects. More UI ("which projects"), more purge rows (the erase plan gains a table, which the ratchet enforces). |
| **C. Through the Artifact lens** | The project relation lives on `artifacts` (an upload "becomes" an artifact when it's added to a project). | It matches the vision's File and Document split most closely, but it's the largest build, and it puts the upload-to-document step (claim 2) on the critical path. |
| **D. Conversation-bound** | `source_conversation_id` on uploads, as artifacts already have. | CXO advises against binding silently, because "a document that vanishes when the conversation ends reads as lost". It's useful as provenance, not as ownership. |

**Arch's read of the build:** A is the least-perturbing step that matches the person's words, and it doesn't block C later. A nullable project on an upload can become the File side of a C-style Document without a migration that throws data away. B is only worth it if xian expects one file in several projects.

## 4. What doesn't wait on the discussion

- **#2443** (`.docx` read) and **#2444** (say how much the summary read): true whatever the answers. Only "read long files in pieces" waits.
- **#2465** (erase must keep chunks another owner reads): needed before 3.1 A or B ships.
- **Naming in replies:** one word, "document", meaning the file the person uploaded (CXO's question 1), whatever is chosen above.

## 5. Facts to have in the room

- Upload types today are `.txt .pdf .docx .md .json` (`files.py`), up to 10 MB. Only PDF reaches the index.
- The summary reads the first 3,000 characters, and a question reads the first 4,000 (map 2.6).
- `/documents` redirects to `/files`, whose nav label is "Documents". The old Documents page is dead code (map section 4).
- The erase engine (`scripts/erase_user.py`, #2064) already covers uploads, the index (through the anchor) and artifacts. 2158 promotes it into the product. Any new table from 3.1 or 3.2 must join its plan, or the architecture ratchet fails.

**Verified how:** the vision documents named above, read for their Document, File and Artifact statements; `services/database/models.py` `ArtifactDB` (columns read); `document-implementation-map.md` (my own, 11-26, unchanged since); CXO's page, read whole; `scripts/erase_user.py`'s docstring and plan helpers. No served read and nothing run.
