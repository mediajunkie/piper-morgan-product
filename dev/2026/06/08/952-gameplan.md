# Gameplan — #952 ARTIFACT-MODEL (Artifact data model with lifecycle states)

**Author**: Lead Developer · **Date**: 2026-06-08 · **Template**: gameplan-template v9.3
**Status**: DRAFT — awaiting PM sanity-check (then audit-cascade gate → build)
**Prereq audit**: `dev/2026/06/08/M3-artifact-spine-audit-cascade-2026-06-08.md` (#952 = formalize/unify existing primitives, ~330 LOC + doc; NOT a blocker — persistence already works piecemeal)

---

## Phase -1: Infrastructure Verification (verified, not assumed)

- **DB**: PostgreSQL (5433), SQLAlchemy + Alembic. ✅
- **Lifecycle primitive**: `services/mux/lifecycle.py` — `LifecycleState` (8-state enum), `LifecycleTransition`, `LifecycleManager`. Already used as `Optional[LifecycleState]` on `Feature` (models.py:248), `WorkItem` (318), `Project` (472), `Todo` (1482). ✅
- **Ownership primitive**: `services/mux/ownership.py` — `OwnershipMetadata` (NATIVE/FEDERATED/SYNTHETIC; MUX epistemology, distinct from SEC `owner_id`). ✅
- **Persistence pattern to mirror**: `InsightDB` + `InsightRepository` (#1035); `UploadedFileDB` + `FileRepository` (owner-scoped, #470). ✅
- **Adjacent content models** (the design fork): `Document` (models.py:784 — content/title/tags/analysis; **no** lifecycle, **no** owner_id, **not** DB-persisted — Notion-backed); `UploadedFile` (owner_id + `UploadedFileDB` persistence, but file-on-disk, **no** inline content, **no** lifecycle); `SurfaceableInsight` (composted learning; has object_id + min_trust_stage; persisted via InsightDB).
- **Gap (verified)**: no top-level `Artifact` / `ArtifactDB` class.

Template phases **0.5 (frontend-backend), 0.7 (conversation design)** → skipped per the template's own "when to apply" gates (this is a backend data-model + persistence change; no UI, no conversation flow). Flagging rather than self-marking N/A.

## Phase 0: Issue verification

#952 ACs (from issue body): (1) Artifact model w/ id, content, type, state, created_at, updated_at, source(conversation/session), owner(user); (2) lifecycle state field (the 8-state enum); (3) basic state transitions; (4) documented in architecture/current/; (5) storage layer; (6) read/write persistence API. Drift: primitives for 2/3/5/6 exist; what's missing is the unified model (1) + the doc (4).

## THE DESIGN DECISION (the crux of the sanity-check)

**What is an "Artifact" vs the models we already have?** Three options:

| Option | What | Pro | Con |
|--------|------|-----|-----|
| **A — standalone `Artifact` (RECOMMENDED)** | New `Artifact` dataclass (id, content, content_type, `lifecycle_state: Optional[LifecycleState]`, created_at, updated_at, source_conversation_id, owner_id, + optional `mux_ownership`) + `ArtifactDB` (mirror UploadedFileDB) + `ArtifactRepository` (owner-scoped, mirror FileRepository) + arch doc. **Reuses** LifecycleState + OwnershipMetadata + the persistence pattern. Files/Documents/Insights stay sibling types. | Matches ACs literally; **additive — zero touch to shipped code**; serves #355 (save chat output → Artifact); smallest honest scope (~330 LOC). | A 4th content-ish model (but each is genuinely distinct: *generated* content vs *analyzed* doc vs *uploaded* file vs *composted* insight). |
| **B — unify all under an `Artifact` base/protocol** | Make Document/UploadedFile/Insight all *kinds of* Artifact via a shared base + lifecycle. | Conceptually elegant; one abstraction. | **Big refactor of shipped, in-use code** (high risk); models have genuinely different fields; not needed for MVP. The "unify everything" over-reach. |
| **C — extend `Document`** | Add lifecycle_state + owner_id + source_conversation_id to `Document` + a new DocumentDB. | Reuses a model. | `Document` is the *analyzed-doc* model (analysis_metadata/key_findings); conflates "generated artifact" w/ "analyzed doc"; Document isn't DB-persisted today → ~same effort as A but with semantic baggage. |

**Recommendation: Option A.** Distinct `Artifact` model for *generated/saved content* (the thing #355 saves from chat, #1179 composts) — distinct from uploaded files (on-disk) and analyzed docs. Reuse the primitives; explicitly **defer** the "unify all content models" question (Option B) to a post-MVP architectural decision (note for Arch).

**Sanity-check question for PM** (the one that changes the plan): *Is a distinct `Artifact` model warranted, or should "saved chat outputs" just reuse the existing `UploadedFile` persistence?* My view: distinct is warranted — generated artifacts carry semantics uploaded files don't (inline content, `lifecycle_state`, `source_conversation_id` provenance). But this is the call to confirm before ~330 LOC.

## Phases 1-N (Option A build, if confirmed)

- **Phase 1**: `Artifact` domain dataclass in `services/domain/models.py` (reuse LifecycleState/OwnershipMetadata) + unit tests.
- **Phase 2**: `ArtifactDB` SQLAlchemy model (mirror UploadedFileDB: owner_id + index) + Alembic migration.
- **Phase 3**: `ArtifactRepository` (CRUD, owner-scoped + is_admin bypass per #470 pattern) + unit tests against in-memory SQLite (the #1035 repo-test pattern).
- **Phase 4**: Architecture doc `docs/internal/architecture/current/` (the artifact model + the deferred-unification decision); flag to Arch for awareness/ratification (non-blocking — consolidates ratified primitives). AC#4.
- **Phase Z**: evidence, close per close-issue-properly (PM approval).

## Test strategy
- **Unit**: Artifact dataclass (lifecycle transitions via LifecycleManager; ownership defaults). ArtifactRepository CRUD + owner-scoping + admin-bypass (in-memory SQLite, no live DB — #1035 pattern).
- **Wiring**: repository ↔ DB model round-trip (from_domain/to_domain).
- No e2e gate needed (no routing/UI). No integration deps.

## Rollback
Pure additive (new model + table + repo + doc). Rollback = revert + drop the (new, empty) table via down-migration. Zero risk to shipped code.

## Dependencies / sequencing
- Unblocks the *clean* versions of #355 (save → Artifact) + #313 (browse artifacts) + #1179 (composted-learning corpus is a sibling). But **not a hard blocker** — those work against existing persistence today.
- Adjacent: #953 (next in build order) is independent (conversation-context persistence).

## Self-audit (gameplan vs template v9.3) — to run AFTER PM sanity-check
Will produce the audit matrix (problem/root-cause/success/test/wiring-tests/rollback/deps/evidence) as the cascade's gameplan gate before any build. Template UI/conversation phases gated-out per their own "when to apply"; will confirm with PM that gating (not self-N/A).
