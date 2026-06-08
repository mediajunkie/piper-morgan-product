# Artifact Model — Design Proposal (#952)

**Status**: PROPOSED — awaiting Chief Architect ratification (MUX object-model domain). Candidate for an ADR (ADR-067?) at Arch's discretion.
**Author**: Lead Developer · **Date**: 2026-06-08 · **Issue**: #952 ARTIFACT-MODEL (M3 Artifact Persistence)
**PM sanity-check**: 2026-06-08 — Option "standalone Artifact" approved *with the lossless round-trip requirement*; "flatten everything into one model" (extend-Document / reuse-UploadedFile) rejected as MUX flattening; full structural unification affirmed as "the real goal," postpone-able past MVP.
**Grounding**: `dev/2026/06/08/M3-artifact-spine-audit-cascade-2026-06-08.md` (audit-cascade), `dev/2026/06/08/952-gameplan.md` (gameplan).

---

## 1. Problem

The "Artifact Persistence" sprint theme has no top-level `Artifact` model, yet the system already persists several *kinds* of artifact piecemeal, each with its own model + repository:

| Existing entity | Model / persistence | Distinct identity |
|-----------------|---------------------|-------------------|
| **Uploaded file** | `UploadedFile` + `UploadedFileDB` + `FileRepository` (owner-scoped) | bytes on disk; owner; reference-counted |
| **Analyzed document** | `Document` (Notion-backed, not DB-persisted) | external content + analysis_metadata/key_findings |
| **Composted insight** | `SurfaceableInsight` + `InsightDB` + `InsightRepository` | learning extracted from a composted object; trust-gated |
| **Generated content** (chat output to save — #355) | *(none today)* | inline content produced in-conversation; needs lifecycle + provenance |

#952 asks for an `Artifact` with `id, content, type, lifecycle_state, created_at, updated_at, source(conversation/session), owner(user)`. The primitives exist — `LifecycleState` (8-state enum, `services/mux/lifecycle.py`), `OwnershipMetadata` (`services/mux/ownership.py`), the DB-model+repository pattern — but no unifying model ties them together.

## 2. The MUX-flattening trap (what we are NOT doing)

The tempting shortcuts both *flatten* the MUX object model and are rejected:
- **Reuse `UploadedFile`** for saved chat outputs → conflates on-disk files with inline generated content; loses lifecycle + source-conversation provenance.
- **Extend `Document`** → conflates *generated* artifacts with *analyzed* documents (analysis_metadata/key_findings are doc-specific).

Each existing entity has a genuine, distinct identity. Collapsing them loses information. The design must **preserve each type's identity** while providing a unifying lens.

## 3. Proposed design — Artifact as a *unifying lens* with lossless round-trip

Introduce a standalone `Artifact` that is the **unifying projection** of the MUX entities — not a fourth silo, and not a flattening.

### 3.1 Domain model (`services/domain/models.py`)
```
@dataclass
class Artifact:
    id: str
    content: str                                   # inline content (generated) or pointer/summary
    source_type: ArtifactSourceType                # document | uploaded_file | insight | generated
    lifecycle_state: Optional[LifecycleState] = None        # reuse the 8-state enum
    lifecycle_history: List[LifecycleTransition] = []        # reuse
    owner_id: str = ""                             # SEC ownership (matches #470 pattern)
    source_conversation_id: Optional[str] = None   # provenance
    mux_ownership: Optional[OwnershipMetadata] = None        # MUX epistemology (orthogonal to owner_id)
    payload: Dict[str, Any] = {}                   # type-specific fields preserved verbatim (no flattening)
    created_at / updated_at: datetime
```
- `source_type` discriminator + `payload` is the **anti-flattening mechanism**: each origin type's specific fields ride in `payload` untouched, so a round-trip is lossless.

### 3.2 Lossless round-trip converters (the load-bearing requirement)
Additive classmethods + instance methods — **no change to the shipped types/repos**:
- `Artifact.from_document(doc) -> Artifact` / `.to_document() -> Document`
- `Artifact.from_uploaded_file(f) -> Artifact` / `.to_uploaded_file() -> UploadedFile`
- `Artifact.from_insight(ins) -> Artifact` / `.to_insight() -> SurfaceableInsight`

**Invariant (tested):** `X == to_X(from_X(X))` for each type — the round-trip preserves identity. `payload` holds whatever the Artifact's flat fields don't natively carry.

### 3.3 Persistence (mirror the established pattern)
- `ArtifactDB` (SQLAlchemy) — mirror `UploadedFileDB`: `owner_id` + index, `source_type`, `lifecycle_state` (string), JSON `payload`, timestamps. + Alembic migration.
- `ArtifactRepository` — CRUD, **owner-scoped + `is_admin` bypass** (the #470 pattern), in-memory-SQLite-testable (the #1035 pattern).

## 4. The unification trajectory (now vs. later) — the decision for Arch

Goal (3) — full structural unification, where `FileRepository`/`InsightRepository`/`Document` are *backed by* Artifact — is **the real goal**, and is affirmed. The proposal is to **build the round-trip foundation now and defer the structural unification to post-MVP, done incrementally.**

**Why deferral is safe here (the key argument):** with the round-trip converters in place, unification becomes an **incremental, one-consumer-at-a-time migration** (each repo becomes Artifact-backed via its existing converter) — structurally identical to the #1124 elif→action-rail migration we just executed cleanly. It is *not* a big-bang rewrite that "gets harder later." We capture the architecture now (cheap, additive) and pay the migration cost per-consumer when each is touched anyway.

**Why not full unification now:** it would refactor three shipped, in-active-use subsystems (Files, Insights, Notion-Documents) mid-MVP → real regression risk, no MVP-functional gain.

**Open question for Arch:** is the round-trip-foundation-now / incremental-unification-later split the right MUX trajectory, or does Arch want the structural unification sequenced differently (e.g., one consumer migrated now as a proof-of-trajectory)?

## 5. Scope / non-goals
- **In scope (this issue)**: the `Artifact` model + `source_type`/`payload` + the 3 lossless round-trip converter pairs + `ArtifactDB` + `ArtifactRepository` + tests + this doc.
- **Out of scope (post-MVP, incremental)**: re-backing FileRepository/InsightRepository/Document onto Artifact; UI (#313); save-from-chat wiring (#355 — consumes this).
- **Additive**: zero modification to shipped models/repositories. Rollback = revert + drop the new (empty) table.

## 6. Relationship to other issues
- **#355** (save chat output) → becomes "create a `generated` Artifact" once this lands.
- **#313** (file/doc browser) → can list across types via the Artifact lens.
- **#1179** (composted-learning dedup/expiry) → operates on insight-Artifacts; sibling.
- **#470 / ownership.py** → `owner_id` (SEC) + `mux_ownership` (MUX) both carried; consistent with the orthogonality clarified in the #470 closure.

---
*Ratification requested via memo-lead-to-arch 2026-06-08. On ratification: audit-cascade gameplan gate → build (Option-1 round-trip Artifact) → close #952 per close-issue-properly.*
