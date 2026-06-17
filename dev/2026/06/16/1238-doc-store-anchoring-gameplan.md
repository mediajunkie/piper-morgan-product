# Gameplan — #1238 Doc-Store User-Auth Anchoring (ADR-071 P2)

**Issue**: #1238 (RADAR-ENTITY-SOURCES Document source / doc-store anchoring)
**Parent**: #1252 (ADR-071 consolidating refactor), P2 doc-store
**Arch ruling**: `mailboxes/lead/read/memo-arch-to-lead-cc-cio-pm-1238-doc-store-disposition-synthesis-confirmed-2026-06-16.md`
**Author**: Lead Developer · 2026-06-16
**Gameplan template**: v9.6
**Execution model**: SOLO (Lead Dev, no subagent fan-out) → the audit-cascade **Prompts gate is inapplicable-by-absence** (no agent prompts are authored); gates run Issue (done, #1238 well-formed) → Gameplan (this doc + audit) → Execute (TDD).

---

## The ruling in one line

Synthesis (Arch CONCUR): **`owner_id` = configured-PM `users.id`** at ingest + backfill existing → PM (provenance) **AND** `is_global_pm_domain = true` (D1 exemption — preserves shared-reasoning-context reads). Marker location: **DB-row column, NOT ChromaDB metadata** (AST-guard sees ORM fields, not vector-store blobs; queryability). Doc store has **no DB row backing each ChromaDB entry → introduce a `documents` table** (ADR-071 D2 catch-up: the owner-anchored row must exist somewhere; this makes its home explicit).

---

## Phase -1: Infrastructure Verification (completed via Phase-0 investigation, no PM gate needed — facts verified empirically)

| Item | Verified state |
|---|---|
| Web framework | FastAPI (`web/app.py`) |
| CLI | Click (`cli/commands/documents.py`) |
| Relational DB | PostgreSQL 5433 (`piper_morgan`, user `piper`); SQLAlchemy async + Alembic |
| Vector store | ChromaDB `pm_knowledge` collection (`data/chromadb`), OpenAI embeddings |
| Testing | pytest (asyncio_mode=auto; in-memory SQLite for repo tests via `__table__.create`; Postgres for integration) |
| Doc-store backing | **ChromaDB-only** — `ingest_pdf` → `collection.add()`; NO relational row, NO owner field |
| Existing docs | **1** document (`pdf_88388894`, 8 chunks, source `tests/fixtures/chapter.pdf` — test fixture) |
| Configured PM | `a25db09c-6d79-41e4-8d82-87b6a005bbb0` (username `xian`, email `xian@pobox.com`) — primary web account, github_preferences-mapped |

**Worktree**: ephemeral `interesting-beaver-7ee19c` (Option B). Write to worktree paths.

---

## Phase 0: GitHub + Codebase Investigation (done)

- `gh issue view 1238` — exists; Phase-0 findings already posted (comment 4719098084).
- **Ingest path**: `cli/commands/documents.py:95` (`add` cmd) → `DocumentService.upload_pdf` (`document_service.py:27`) → `DocumentIngester.ingest_pdf` (`ingestion.py:149`) → `collection.add()`. No DB write.
- **3 reads** (all query `self.ingester.collection` directly, none scoped): `find_decisions` (`document_service.py:70`), `get_relevant_context` (`:176`), `suggest_documents` (`:259`).
- **Real read-callers** (m-40 caller-analysis):
  - `services/intent_service/document_handlers.py:329` — `find_decisions(topic=query)`; `handle_search_documents(query, user_id)` **already receives `user_id`** (line 306); lines 319-322 explicitly flag this work as the planned follow-up.
  - `services/features/morning_standup.py:520-522` + `:702-704` — all 3 reads (global-reasoning-context).
  - `cli/commands/documents.py` — CLI ops (operator = configured PM).
  - **`classifier.py:1389` is a FALSE POSITIVE** — it calls `knowledge_graph_service.get_relevant_context(user_query, user_id, max_nodes)`, a different already-scoped method. NOT in #1238 scope. *(Corrects Arch's memo, which listed "classifier" as a caller.)*

### STOP-condition check
- Issue exists ✓ · Feature not already implemented ✓ (no documents table; reads unscoped) · Problem matches description ✓.

---

## Phase 0.5: Frontend-Backend Contract — **SKIP** (justified)
Backend-only change (new table, repo, service-layer threading, migration, backfill). No new API endpoints, no JS/template work. Per template: "Backend-only changes (skip this phase)."

---

## Phase 0.6: Data Flow & Integration Verification — **APPLIES** (the load-bearing section)

### Part A: User-context propagation (owner_id, the principal)

| Layer | Needs owner_id? | Source of value |
|---|---|---|
| CLI command (`documents.py`) | Yes (write + read) | `resolve_pm_owner_id(session)` (operator = configured PM) |
| `document_handlers.handle_search_documents` | Yes (read) | **already has `user_id` param** (line 306) — pass through |
| `morning_standup` reads | Yes (read) | `self.user_id` (standup config principal) |
| `DocumentService` methods | Yes — **new optional `owner_id` param** | Parameter from caller (m-40: scope-when-provided, WARN-graceful-when-None) |
| `DocumentRepository` | Yes | Parameter from service |

**State persistence**: new `documents` table (Postgres). Lookup key: `chromadb_base_id` (links row ↔ ChromaDB chunks). Read-authorization key: `owner_id` + `is_global_pm_domain`.

### Part B: Integration points

| Caller | Callee | Import verified | Method | Params available |
|---|---|---|---|---|
| CLI `add` | `DocumentService.upload_pdf(file, metadata, owner_id)` | ✓ | upload_pdf (extend sig) | owner_id from resolver |
| `DocumentService.upload_pdf` | `DocumentIngester.ingest_pdf` | ✓ | returns `document_id`=base_id | base_id from result |
| `DocumentService.upload_pdf` | `DocumentRepository.upsert_document` | new | upsert by base_id | session acquired per-call |
| `DocumentService.<read>` | `DocumentRepository.get_readable_base_ids` | new | filter set | owner_id param |
| `document_handlers:329` | `DocumentService.find_decisions(topic, owner_id)` | ✓ | extend sig | user_id (have it) |
| `morning_standup` | `DocumentService.<read>(..., owner_id)` | ✓ | extend sig | self.user_id |

**Session acquisition**: `DocumentService` is currently session-less. Each read/write acquires an async session per-call (`async with <session factory>() as session: repo = DocumentRepository(session)`). Confirm the canonical session factory in Phase 2 (mirror `repositories.py` consumers).

### Part C: Pattern adaptation (m-40 layer-then-migrate — proven on artifacts/conversations/insights)

| Aspect | Source pattern (insights a,3) | This implementation | Why different |
|---|---|---|---|
| Scope mechanism | filter in SQL SELECT | **post-ChromaDB-query filter** via `get_readable_base_ids` | authoritative scope lives in the relational row, not the vector store (Arch: marker not in ChromaDB) |
| None-principal | WARN-shim, return unscoped | WARN + **global-only** (return only `is_global_pm_domain` docs) | safe default; un-anchored content not surfaced |
| Readability | owner == principal | owner == principal **OR is_global_pm_domain** | D1 exemption preserves shared-reasoning-context |

**Pitfalls + mitigation**:
- *A doc chunk with no `documents` row* → excluded from reads (fail-safe). Mitigated by backfill (Phase 4) covering all existing base_ids + ingest wiring (Phase 3) creating rows for all new docs. Post-deploy, every doc has a row. Documented as deliberate.
- *ChromaDB `query` returns `ids`* — verified: `search_with_context` already uses `results["ids"][0][i]`; `ids` are always returned. base_id = `id.rsplit("_chunk_",1)[0]`.

### STOP conditions (Phase 0.6)
All import paths exist ✓ · method sigs extend cleanly ✓ · owner_id available at every call site ✓ · pattern difference documented ✓.

---

## Phase 0.7: Conversation Design — **SKIP** (justified)
Not a conversational feature (no multi-turn flow). Per template: applies only to onboarding/wizard/multi-turn.

---

## Phase 0.8: Post-Completion Integration

Creates DB records (documents rows). Completion side-effects:

| Side effect | Table/field | Value | Verify |
|---|---|---|---|
| Document row created at ingest | `documents` | 1 row/doc, owner=PM, is_global_pm_domain=true | repo test + manual |
| Existing docs backfilled | `documents` | 1 row (`pdf_88388894`) | SQL count after backfill |

Downstream behavior change:

| Feature | Before | After |
|---|---|---|
| `find_decisions`/`get_relevant_context`/`suggest_documents` | return ALL ChromaDB matches (unscoped — (c,3) leak surface) | return only readable docs (owner OR global); all current docs are global → **behavior preserved**, leak surface closed |

---

## DDD Domain Model

A **Document** is a PM-domain knowledge artifact ingested into the vector store. It carries **provenance** (`owner_id` — who ingested) and a **readability policy** (`is_global_pm_domain`). The relational `documents` row is the canonical anchor ADR-071 D2 mandates; ChromaDB is the downstream vector index keyed by `chromadb_base_id`.

`DocumentDB` (services/database/models.py):
- `id` UUID PK (default uuid4)
- `chromadb_base_id` String, unique, indexed, nullable=False — link to ChromaDB chunks (e.g. `pdf_88388894`)
- `owner_id` `CrossDialectUUID()` + `ForeignKey("users.id")`, nullable=True, index — provenance (D2 canonical owner)
- `is_global_pm_domain` Boolean, nullable=False, `server_default="false"`, default=False — D1 exemption marker
- `title` String, nullable=True
- `source` String, nullable=True (file path)
- `created_at` DateTime(timezone=True), default now

---

## Phases 1–5 (implementation; Inchworm — 100% + green + commit + push per phase)

### Phase 1 — `DocumentDB` model + additive Alembic table (TDD)
- Add `DocumentDB` to `models.py` (CrossDialectUUID for SQLite-testability).
- Alembic migration `a1238documents_create_documents_table` (additive create_table; reversible drop). Apply + verify on dev DB; downgrade-test.
- Test: model imports, table creates in SQLite, columns/defaults correct.
- **Green gate**: model + migration tests pass; `alembic upgrade head` + `downgrade -1` clean.

### Phase 2 — `DocumentRepository` (TDD)
- `repositories.py` (or `services/repositories/`): `upsert_document(chromadb_base_id, owner_id=None, is_global_pm_domain=False, title=None, source=None)` (idempotent by base_id); `get_readable_base_ids(principal_owner_id) -> set[str]` (`is_global_pm_domain==True OR owner_id==principal`; None principal → global-only); `get_by_base_id`.
- Confirm canonical async session factory.
- Test (in-memory SQLite): upsert insert + update; readable-set for owner / other-owner / None / global vs private.
- **Green gate**: repo tests pass.

### Phase 3 — Ingest wiring + PM-owner resolution
- `resolve_pm_owner_id(session)` helper — order: (1) env `PIPER_PM_USER_ID` if set, (2) `username='xian'` lookup (alpha-scoped fallback), (3) None. Documented as alpha-scoped, evolves with ADR-071 D7 tenant_id. *(owner_id is provenance; reads work via is_global_pm_domain → imperfect resolution is low-risk.)*
- `DocumentService.upload_pdf(file, metadata, owner_id=None)` → after `ingest_pdf` returns, `upsert_document(base_id, owner_id, is_global_pm_domain=True, title, source)`.
- CLI `add` resolves owner via helper + passes it.
- Test: upload writes a documents row (mock ingester or real base_id) with owner + global flag.
- **Green gate**: ingest-wiring test passes.

### Phase 4 — Backfill existing doc(s)
- Idempotent `scripts/backfill_documents_1238.py`: enumerate distinct ChromaDB `pm_knowledge` base_ids → `upsert_document(base_id, owner=resolve_pm_owner_id, is_global_pm_domain=True, title, source)`.
- Run on dev DB; verify 1 row (`pdf_88388894`), owner=xian, global=true. Re-run = no dup (idempotent).
- **Green gate**: backfill verified by SQL.

### Phase 5 — Thread the 3 reads + callers + cross-owner test (the (c,3) close)
- `find_decisions(topic, timeframe, owner_id=None)`, `get_relevant_context(timeframe, owner_id=None)`, `suggest_documents(focus_area, owner_id=None)`: after ChromaDB query, compute base_id per result, filter to `get_readable_base_ids(owner_id)`. None → WARN + global-only.
- Thread callers: `document_handlers:329` (pass existing `user_id`), `morning_standup` ×2 (`self.user_id`), CLI (resolved PM).
- **TDD cross-owner test** (the close): seed doc A owned by user-A `is_global_pm_domain=false` + doc B `is_global_pm_domain=true`; assert principal-B reads B not A; principal-A reads both; None reads only B. Plus a **wiring test** (real import chain: caller → DocumentService → repo, owner_id propagates — no mocked internals, per #490 learning).
- **Green gate**: read-threading + cross-owner + wiring tests pass; existing doc-service/standup/document-handler suites green (no regression).

---

## Test Scope (acceptance)
- [ ] Unit: DocumentDB model; DocumentRepository (upsert + readable-set); resolve_pm_owner_id.
- [ ] Integration: ingest writes row; reads filter by readable-set (cross-owner).
- [ ] **Wiring**: real import chain caller → DocumentService → DocumentRepository with owner_id propagating (no mocked internals).
- [ ] **Performance**: the read-filter adds exactly **one index-backed query** per read (`get_readable_base_ids`). Metric = O(1) extra round-trip; the **index on `owner_id` + `is_global_pm_domain` is the guard** (asserted by the migration/model having those indexes). A timing-assertion test is test-theatre at alpha scale (1 doc) — the metric + index requirement is the disposition, not an omission.
- [ ] Regression: existing document_service / morning_standup / document_handlers suites green.
- [ ] Migration: upgrade + downgrade clean on dev DB.

## STOP conditions (throughout)
Standard + : session factory not found at expected import → trace before wiring; ChromaDB `ids` absent from a read's results → verify include before filtering; FK type mismatch documents.owner_id ↔ users.id → reconcile before migration.

## Success criteria
- [ ] `documents` table live (additive, reversible).
- [ ] Ingest stamps owner_id + is_global_pm_domain=true.
- [ ] Existing doc backfilled.
- [ ] 3 reads scoped behind the marker; callers threaded.
- [ ] Cross-owner + wiring tests green; no regressions.
- [ ] #1238 closed-properly (description checkboxes first, evidence, PM-validate); decisions.log appended.

## Phase Z: Handoff
- Per-phase: commit + push to origin/main; gh issue progress comment.
- Final: evidence summary on #1238; decisions.log entry (Arch ruling); refresh carry-forward; ack Arch process memo.
- **Follow-up to consider filing**: formal PM-identity config (replace the `username='xian'` alpha-fallback in `resolve_pm_owner_id`) — ties to ADR-071 D7 tenant_id evolution.
