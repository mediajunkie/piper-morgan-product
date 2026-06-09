# M3 Artifact-Persistence Spine — Audit-Cascade (verify-before-extend)

**Date**: 2026-06-08 · **Author**: Lead Developer · **Discipline**: audit-cascade (Pattern-049), code-reality vs issue-claim
**Method**: 4 parallel read-only Explore audits (issue body + codebase, file:line evidence) → Lead-Dev spot-verification of all load-bearing claims → this synthesis.
**Scope**: the artifact-persistence cluster PM flagged — #952, #355, #1060, #953, #371, #470, #313 (spine) + #976, #669 (composting, PM connected #669/#952/#953 to artifacts).

---

## Headline

**The artifact-persistence theme is far more built than the 16-open count implies.** Persistence already works *piecemeal*: files persist (UploadedFileDB + FileRepository + owner_id), conversations persist (ConversationRepository + ConversationTurnDB, R4), insights persist (InsightDB + InsightJournal). Of the 9 audited:

- **3 are already done** (verify → close): **#1060**, **#470**, **#976** (mostly)
- **4 are near-done / small solo gaps**: **#355** (UI button), **#669** (~50 LOC), **#953** (lens/offer persist), **#952** (consolidate existing primitives)
- **2 are big / not-M3-critical**: **#371** (descope/defer — months, blocks only post-alpha #366), **#313** (L, multi-sprint, overlaps #355)

## Audit matrix (verified)

| # | Title | Code reality (evidence) | Gap | Size | Recommendation |
|---|-------|------------------------|-----|------|----------------|
| **1060** | INFRA-CONVERSATION-REPO | ConversationRepository fully impl (`repositories.py:1167`, 8 methods) + wired (`conversation_manager.py:298`, R4/#1030). Placeholder body ("ACs to be authored"). | none | — | **VERIFY → CLOSE** w/ evidence |
| **470** | SEC-RBAC Phases 4-5 | owner_id + `is_admin` enforced: ProjectRepository (`repositories.py:268`), FileRepository (`file_repository.py:59`); APIs pass `owner_id=current_user.sub`; project sharing model wired. MUX `OwnershipMetadata` is orthogonal (epistemology, not access control). | none (4-5 complete) | — | **VERIFY → CLOSE** w/ evidence (or confirm no Phase 6) |
| **976** | MEM-COMPOSTING | Pipeline/scheduler/bin/journal/persistence/framing/dev-trigger all shipped (#1035/#1033/#1143). `CompostingPipeline`, `CompostingScheduler`, `InsightJournal` present. | "consolidate duplicates" + "expire outdated facts" NOT built — but **not in the issue body's core ACs** (only alluded). ADR-054 labeling drift (ADR-054 = memory layers; composting spec is a separate doc). | S–M if gaps real | **AUDIT ACs → likely CLOSE** (file sub-task if dedup/expiry truly required) |
| **355** | DOCS-STOPGAP | File infra fully wired: `UploadedFileDB`, `FileRepository`, `/files` UI (`ui.py:386` + `files.html`), upload/list/download/delete APIs. | "Save as artifact" chat button (UI wiring to existing upload API) + filename edit. NOT a DB problem. | **S** (UI) | Build (small; template-render verifiable) |
| **669** | COMPOSTING-HYBRID-TRIGGER | Scheduler has quiet-hours gate + `force=True` path; `last_run` tracked. `max_hours_since_last_run` **absent** (verified). | Add field + force-bypass in `_should_run()` (insomniac case) + tests. | **S** (~50 LOC) | Build (small, solo, no integration) |
| **953** | CONTEXT-PERSIST | Turns + turn_provenance persist (R4). lens_stack + last_offer live in in-memory `_conversation_contexts` dict (`conversation_context.py:494`). | Persist lens_stack + last_offer to DB (ConversationDB.metadata sufficient — no Redis decision pending) + load on resume. | **M** (~2-3d) | Build (real Layer-4 gap) |
| **952** | ARTIFACT-MODEL | All primitives exist: `LifecycleState` (8 states, `lifecycle.py`), `LifecycleManager`, `OwnershipMetadata`, `InsightDB`/`UploadedFileDB`/`ConversationTurnDB`. **No top-level `Artifact`/`ArtifactDB` class** (verified). | Unified `Artifact` dataclass + `ArtifactDB` + `ArtifactRepository` + 1 ADR — *reusing* the primitives. | **M** (~330 LOC + ADR) | Build — but **consolidation, not a blocker** (persistence works piecemeal without it) |
| **313** | CONV-UX-DOCS | File ops backend complete; UI ~60% (list/upload/download/delete in `files.html`). Missing: search/preview/bulk/artifacts/sharing. | Search + preview + bulk + artifact-classification + version + share. Overlaps #355 (which is a subset). | **L** (5-7d), XL w/ version+share | Slice or defer; sequence after #355 |
| **371** | INFRA-TIMESERIES | Nothing exists. Blocks only **#366 SLACK-MEMORY (post-alpha)**; **#365 closed without it** (used LearnedPatternDB). Not a dep of #953/#1060/#952. | Full TS infra (ingestion/analysis/retention). | **XL** (~months) | **DESCOPE / defer to M4+** (PM call) — independent infra that landed in the sprint |

## Build-order for the spine (given the drift)

Because persistence already works piecemeal, **#952 is NOT a foundational blocker** — it's conceptual consolidation. Honest sequence:

1. **Clear the noise** — verify→close the already-done: **#1060**, **#470**, **#976** (after AC check). Drops M3 open count by ~3 with zero build.
2. **Small solo gaps** (no integration / configured-env needed):
   - **#669** hybrid trigger (~50 LOC + tests) — self-contained.
   - **#952** Artifact-model consolidation (~330 LOC + ADR) — makes the piecemeal coherent; unblocks a clean #313/#953 story.
   - **#953** lens_stack + last_offer persistence (~2-3d) — closes the real Layer-4 hole.
3. **User-facing** — **#355** (chat save button, small) then **#313** (file-UI slices: search/preview first). #355 ⊂ #313.
4. **Defer** — **#371** to M4+ (PM call).

## Recommended immediate actions (for PM)

- **A. Authorize verify→close of #1060 + #470** (clearest already-done; I'll paste the file:line evidence into each + close per close-issue-properly). #976 needs a quick AC read first.
- **B. Solo-buildable now** (configured-env not needed): #669, #952, #953. I can take these in order.
- **C. PM decisions**: #371 descope to M4? · #313 slice vs defer? · #355 — wire now or fold into #313?

---
*This audit is the issue-phase gate of the cascade. Next phase per item that proceeds to build: write gameplan → AUDIT → prompts → AUDIT → execute.*
