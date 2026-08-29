# ADR-064: Project-Scope Search Index Architecture — Pre-1.0 Commitment for Surface 5

**Status**: **v0.1 (drafted 2026-05-16)** — pre-1.0 Architect-lane ADR per MUX/UI Round 2 (Surface 5 user-facing search is post-1.0; this ADR commits to the index architecture before 1.0 so new surfaces have known indexing shape)
**Date**: 2026-05-16 (v0.1 — third ADR in the MUX/UI Round 2 sequence: ADR-062 (e2e suite) → ADR-063 (audit-envelope read) → ADR-064 (search index))
**Supersedes**: None (extends existing fragmented search surfaces with a coherent project-wide architecture)
**Issues**: #786 (GLUE-HISTORY-DIFF — existing conversation search via title; predecessor); #1090 (MUX/UI gap — Round 2 ratified Surface 5 deferral with pre-1.0 index ADR commitment)
**Related**: ADR-054 (Cross-Session Memory Architecture — Layer 3 User History uses a similar text-search shape and is a prior reference instance), ADR-062 (Project-Scope E2E Suite — Phase 5 cross-host extension informs BYOC-distributed indexing), ADR-063 (User-Facing Audit Envelope Read Surface — audit envelope searchability is a forward-question this ADR scopes), Pattern-072 (Registries that Grow into Architectural Shapes, Proven — per-surface indexing declarations are same-shape registry pattern)
**Deciders**: Chief Architect (drafted); Lead Developer (implementation refinement when Surface 5 ships); CIO (methodology shelf consideration for per-surface indexing declarations)

---

## Context and Problem Statement

The project has accumulated **fragmented search surfaces** across multiple domains:

| Surface | Current implementation | Index type |
|---------|----------------------|-----------|
| Conversation list filter | `web/api/routes/conversations.py:262` — `search: str` query param; Postgres LIKE on title | Text (title only) |
| User history search | `web/api/routes/user_history.py:109` — `/api/v1/users/me/history/search` (title/preview/topics) | Text (multi-field) |
| Knowledge graph query | `web/api/routes/knowledge_graph.py:266` — `search_term` on node names/descriptions | Text (graph nodes) |
| Document ingestion | `services/knowledge_graph/ingestion.py` — ChromaDB vector store + Postgres FTS for metadata | Vector + Text |
| Editorial draft/calendar | `services/editorial/{draft,calendar}.py` — Postgres FTS | Text |

Each surface chose its own indexing shape based on local needs. **No project-wide commitment exists for**:
- Whether a new surface SHOULD be searchable
- Where its index lives (Postgres FTS / ChromaDB / both / neither)
- How fresh the index is (sync-on-write / async batch / eager-vs-lazy)
- How access control composes with search results
- How BYOC distribution interacts with indexing (server-side vs per-host)

MUX/UI Round 2 ratified Surface 5 (user-facing search interface) as **post-1.0** because the unified-search UX is its own project. **The architect-lane commitment that lands pre-1.0** is what this ADR provides: the index architecture, so when new surfaces ship between now and 1.0, they have a known indexing shape to follow rather than each surface negotiating an ad-hoc indexing decision at filing time.

### Why pre-1.0 commitment matters even though Surface 5 is post-1.0

Three reasons the index decision can't wait:

1. **New surfaces ship between now and 1.0** — every new surface that touches user-visible data has an implicit search question. Without commitment, each surface either skips indexing (cumulative drift; post-1.0 search shows uneven coverage) or invents its own (cumulative fragmentation; post-1.0 search has to bridge inconsistencies)
2. **BYOC distribution model coupling** — PDR-005 BYOC implies cross-host coordination; "where does the search index live" has a different answer when the user is on Claude Desktop vs. Slack vs. the FastAPI surface. The architectural commitment now keeps 1.0 from boxing us into a single-host index assumption
3. **Pattern-072 (Proven) recognition** — per-surface indexing declarations are the same-shape registry pattern (`task_type`, `safe_surface()`, probe registry). Naming the registry shape pre-1.0 means new declarations land in a consistent place rather than re-discovering the shape per surface

---

## Decision

### Principle

**Search index architecture is a per-surface declaration following a project-wide registry, layered across Postgres FTS (text-structured) + ChromaDB (vector-semantic), with query-time access control filtering and synchronous-text-async-vector freshness model.** Cross-host search distribution is deferred to BYOC Phase 5 (per ADR-062's cross-host trigger) but the architecture is forward-compatible.

The principle is a synthesis of three commitments: layered storage, declarative registry, and access control discipline.

### Three-Layer Decision Tree (Per-Surface)

When a new surface ships, three questions decide its indexing:

**Q1 — Should this surface be searchable?**

Default: **NO** (every surface added to the search index adds maintenance + freshness + access-control cost). Surfacing requires explicit decision based on three criteria:
- **User benefit**: would users routinely scan or query this surface? (Existing conversation list filter is a strong yes; internal request_ids are a strong no)
- **Cross-surface value**: would users search ACROSS surfaces (e.g., "find that conversation where I asked about Q3 deadlines")? Cross-surface value is the strong argument for inclusion
- **Privacy posture**: does indexing create attack surface? (Audit envelopes are sensitive per Pattern-071; indexing them increases the existence-leak attack surface — likely keep audit envelopes out of unified search even though they're user-visible at the read surface)

Surfaces NOT searched: internal request IDs, audit envelopes (Pattern-071 defensive posture), system telemetry, transient state.

**Q2 — Which index type does this surface use?**

Two layers, chosen by data shape:

- **Postgres FTS** (text-structured): when content is short, structured, mostly title-like or metadata. Examples: conversation titles, user history topics, knowledge graph node names, editorial calendar entries, todo list items. Index lives in the source table via `tsvector` columns; queries via `to_tsquery` with ranking
- **ChromaDB** (vector-semantic): when content is long-form, semantic, or requires similarity (not just keyword match). Examples: document body content, conversation embeddings for "find similar conversations", long-form knowledge graph descriptions
- **Both layers** (text + vector): rare; reserved for surfaces where exact-match and semantic-similarity have distinct user value. Documents have both today

Default to Postgres FTS unless semantic similarity is the use case.

**Q3 — Freshness model for this surface?**

Two models, chosen by index type:

- **Synchronous-on-write** for Postgres FTS: `tsvector` columns regenerated in the same transaction as the write (via Postgres trigger or service-layer code). Query consistency: immediate
- **Async-batch** for ChromaDB: embeddings generated post-commit via a background job (per Pattern-070's cleanup-job-with-cancellation-hygiene shape). Query consistency: eventually consistent (typically <30s in production)
- **Eager-vs-lazy choice within async-batch**: write-time queues an embedding job (eager) vs. query-time triggers embedding-if-missing (lazy). Default eager for high-write surfaces; lazy for low-write surfaces.

### Per-Surface Index Declaration Registry (Pattern-072 Shape)

Following Pattern-072 (Registries that Grow into Architectural Shapes, Proven via #1094), each searchable surface declares its index shape in a central registry. Proposed location: `services/search/index_declarations.py` (or analogous).

```python
@dataclass
class IndexDeclaration:
    surface: str  # the surface name (e.g., "conversations", "user_history", "knowledge_graph_nodes")
    enabled: bool  # whether this surface is in the project-wide search index
    index_type: Literal["postgres_fts", "chromadb_vector", "both"]
    freshness: Literal["sync_on_write", "async_eager", "async_lazy"]
    access_control: Callable  # query-time filter; takes (user_id, raw_results) → filtered_results
    notes: str  # rationale for inclusion / exclusion / configuration choices
```

The registry serves as:
- **Single source of truth** for "is X searchable?" — new surfaces add a declaration explicitly (default-disabled)
- **Cross-surface query coordinator** when Surface 5 ships (the UI iterates the registry to assemble unified search results)
- **Audit surface for the indexing decision-tree** — the `notes` field records the Q1/Q2/Q3 reasoning so future-author confidence has a reference

The registry is third+ application of the Pattern-072 shape (after `task_type` registry and probe registry from ADR-062). Pattern recognition trigger for promotion of the registry shape to "standard architectural primitive" has fired multiple times across distinct surface domains.

### Access Control: Query-Time Filtering, Never Index-Time-Only

**Search results are post-filtered by JWT user authorization at query time, not at index time alone.**

Rationale:
- Index-time-only authorization tags can become stale (user permission changes, content access revoked, content moved)
- Query-time filtering keeps the JWT-bound authorization rule (per ADR-063) as the load-bearing surface
- Performance cost is acceptable: post-filtering a small result set (Top-K query) is cheap; the alternative is per-user-stored indices which doesn't scale

Each surface's `access_control: Callable` in the registry takes raw results and filters per user. Common shape: rejoin results against the source table with user-ownership check; drop entries the user can't access.

**Exception** (acceptable index-time filtering): partition indices by user_id when the data is **structurally** per-user (e.g., user history is naturally user-scoped; the index is queryable only with user_id key). Cross-user-shared indices (knowledge graph nodes; document corpus) require query-time filtering.

### BYOC Posture (Forward-Compatible)

**Server-side indexing remains canonical**; cross-host search distribution is deferred to BYOC Phase 5 per ADR-062's cross-host trigger.

When BYOC MCP server packaging ships:
- The MCP server adapter exposes search via the existing registry-based query mechanism
- Per-host clients (Claude Desktop / ChatGPT / Slack) call the MCP server's search endpoint rather than maintaining local indices
- Cross-host search results unify at the server side; client-side concerns are presentation only (per host UI conventions)

This keeps the server as single-source-of-truth for index state; clients are stateless consumers. Per-host content (e.g., Slack messages that haven't been mirrored to server-side substrate) is not in the unified search until the substrate-sync question is resolved (separate ADR or BYOC-side decision).

### Out of Scope

- **Search UI shape** (Surface 5 itself, post-1.0): typeahead vs. dedicated search page; result ranking visualization; per-surface filtering chips. Surface 5 MUX doc work at Phase 2 of 1.0+; this ADR commits to architecture, not to UI
- **Query language** (advanced operators, faceting, boolean logic): post-1.0 design work; this ADR commits to the index shape, not to the query interface
- **Specific Postgres FTS configuration parameters** (which language stemmer, which weight per-field, which rank_normalization): per-surface Phase 2 implementation decisions
- **Audit envelope searchability** (currently default exclude per Q1 privacy posture): can be revisited if a clear user-benefit case emerges; current default keeps Pattern-071 defensive posture
- **Federated cross-host search** (search across multi-host accounts; e.g., "find this message across my Slack + Claude Desktop conversations"): BYOC-deep-future; not Phase 5 scope; separate ADR if it surfaces

---

## Consequences

### Positive

- **Project-wide search index architecture commitment lands before 1.0** — new surfaces have a known indexing shape; cumulative coverage drift is bounded by explicit declarations
- **Fragmented search surfaces have a unification path** — Surface 5 ships post-1.0 against a stable registry; existing per-domain searches (conversations / user history / knowledge graph) become first-class surfaces in the registry rather than ad-hoc implementations
- **BYOC distribution forward-compatible** — server-side canonicalization keeps the index assumption stable across BYOC scenarios; Phase 5 cross-host extension via ADR-062 has a stable target
- **Access control discipline codified** — query-time filtering keeps JWT authorization (per ADR-063) load-bearing; index-time-only-authorization gotchas avoided
- **Pattern-072 registry shape applied** — `IndexDeclaration` is third+ application of the same architectural primitive; Pattern-072 (Proven) recognition reinforces
- **Layered storage matches data shape** — Postgres FTS for text-structured + ChromaDB for vector-semantic; surfaces choose by content shape rather than retrofitting into a single substrate

### Negative / Tradeoffs

- **Per-surface declaration cost** — each new searchable surface adds a registry entry. Mitigated by `enabled=False` default; declaration is a one-line entry. Cost is non-zero but bounded.
- **Two-substrate operational cost** — both Postgres FTS and ChromaDB need monitoring + freshness checks + backup. Existing infrastructure includes both; this ADR doesn't add substrates, it commits to using them coherently
- **Async vector freshness** is eventually consistent (typically <30s). For high-value semantic queries with strict-freshness needs, this is a cost. Mitigation: surface declaration can override to `sync_on_write` if needed (most surfaces don't need it)
- **Query-time filtering performance** — post-filtering Top-K results is cheap, but if pre-filter result set is very large (10K+ candidates pre-filter), performance degrades. Mitigation: per-surface optimization at Phase 2 implementation (partition by user_id where possible)

### Non-Consequences (explicitly out of scope)

- **Not committing to specific Postgres FTS language stemmer or weight configuration** — per-surface implementation decisions
- **Not committing to ChromaDB-specific embedding model** — separate ADR if model choice matters at architectural level; current Anthropic Claude embeddings adequate
- **Not requiring all existing search surfaces to migrate to the registry immediately** — Phase 2 implementation work; backward-compat with existing per-domain searches preserved
- **Not addressing audit envelope searchability** — current default exclude per Pattern-071; revisit if user-benefit case emerges

---

## Validation

### Existing Reference Instances

The architecture is grounded by five existing search-adjacent implementations, each demonstrating one aspect of the principle:

| Instance | Validates |
|----------|-----------|
| Conversation list filter (`conversations.py:262`) | Postgres LIKE → upgrade path to Postgres FTS; per-user partitioning works |
| User history search (`user_history.py:109`) | Multi-field Postgres-based text search; per-user query-time filtering |
| Knowledge graph node query (`knowledge_graph.py:266`) | Cross-entity text search; query-time access control |
| Document ingestion (`knowledge_graph/ingestion.py`) | ChromaDB vector store + Postgres FTS for metadata; layered storage in production |
| Editorial draft + calendar (`editorial/{draft,calendar}.py`) | Postgres FTS for structured text content |

Phase 2 implementation (when Surface 5 ships) folds these into the IndexDeclaration registry as the first five entries.

### Pattern-072 (Proven) Recognition Trigger

The IndexDeclaration registry is the third+ application of the registry-as-architectural-shape primitive Pattern-072 names (Proven via #1094 close-out 2026-05-15):

| Instance | Surface |
|----------|---------|
| 1 | `task_type` registry → model + handler dispatch |
| 2 | `safe_surface()` registry → permission-gating |
| 3 | Probe registry (ADR-062 Layer 1) → e2e suite |
| 4 | **IndexDeclaration registry (this ADR)** → search corpus management |

Pattern-072's recognition discipline (typed enum, documented consumer set, explicit default policy, register-time validation) applies cleanly: `IndexDeclaration` is a dataclass (typed); the registry is a single file (documented consumers); `enabled=False` is the explicit default; registry-time validation at Phase 2 confirms required fields present.

### ADR-054 (Cross-Session Memory) Reference Instance

ADR-054 Layer 3 (User History) uses the same text-search shape this ADR generalizes. The User History search at `user_history.py:109` is one of the five reference instances above; ADR-054's Layer 3 commitment to per-user text search is the structural precedent for ADR-064's per-surface declarative approach.

---

## Cross-references

- **ADR-054** (Cross-Session Memory; Layer 3 User History as precedent): `docs/internal/architecture/current/adrs/adr-054-cross-session-memory-architecture.md`
- **ADR-062** (Project-Scope E2E Suite; Pattern-072 registry-shape reuse): `docs/internal/architecture/current/adrs/adr-062-project-scope-e2e-suite.md`
- **ADR-063** (Audit Envelope Read Surface; access control template): `docs/internal/architecture/current/adrs/adr-063-user-facing-audit-envelope-read-surface.md`
- **Pattern-072** (Registries that Grow into Architectural Shapes, Proven): `docs/internal/architecture/current/patterns/pattern-072-registries-that-grow-into-architectural-shapes.md`
- **Pattern-070** (Cleanup-Job-with-Cancellation-Hygiene, Emerging — async-batch freshness model uses Pattern-070 invariants): `docs/internal/architecture/current/patterns/pattern-070-cleanup-job-with-cancellation-hygiene.md`
- **MUX/UI Round 2 synthesis** (Surface 5 deferral + pre-1.0 index ADR commitment): `mailboxes/{cohort}/inbox/mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md`
- **MUX/UI Round 2 CEO ratification**: `mailboxes/arch/sent/memo-arch-to-cxo-lead-comms-ppm-cc-ceo-pa-exec-mux-ui-round-2-ceo-ratification-2026-05-16.md`
- **Existing search surfaces**:
  - `web/api/routes/conversations.py:262` (search param)
  - `web/api/routes/user_history.py:109` (history search)
  - `web/api/routes/knowledge_graph.py:266` (node query)
  - `services/knowledge_graph/ingestion.py` (ChromaDB + Postgres FTS)
  - `services/editorial/{draft,calendar}.py` (Postgres FTS)

---

## Open Items (Phase 2+ work, post-1.0 or surface-specific; not gated by this ADR)

- **Surface 5 MUX doc drafting** — post-1.0; CXO + Comms lane when Surface 5 itself reaches the build queue
- **IndexDeclaration registry implementation** — Phase 2 of Surface 5 (post-1.0): file location, dataclass shape, registry-time validation, migration of existing surfaces (conversation / user history / knowledge graph / documents / editorial)
- **Audit envelope searchability decision** — currently default-excluded per Pattern-071 defensive posture; revisit if user-benefit case surfaces
- **Cross-host search via BYOC Phase 5** — gated by BYOC MCP server ship per ADR-062; the MCP server adapter exposes the registry-based query when this surfaces
- **Per-surface freshness tuning** — most surfaces will be `sync_on_write` for text + `async_eager` for vector; high-write surfaces may need `async_lazy` for cost reduction. Phase 2 per-surface decisions.

— Chief Architect, 2026-05-16 v0.1 (Pre-1.0 Architect-lane ADR per MUX/UI Round 2 Surface 5 ratification; commits to project-wide search index architecture before Surface 5 user-facing search ships post-1.0)
