# docs/ Tree Audit + Cleanup Plan

**Authored**: 2026-07-13 by Docs  
**Status**: DRAFT — awaiting PM approval before any execution  
**Requested by**: PM (relayed by PPM, Jul 12)

---

## Summary

The `docs/` tree has accumulated three distinct cleanup problems over ~18 months of growth:
1. **"MOVED" stub directories** — navigational tombstones pointing at `docs/internal/`; the redirect message is helpful but the empty shell directories add confusion
2. **Legacy external-facing docs structure** — ~12 top-level directories (`docs/guides/`, `docs/installation/`, `docs/api/`, etc.) from an earlier developer-documentation phase; most are Nov 2025 vintage, some updated mechanically in 2026
3. **Alpha-era working documents** — `docs/internal/planning/roadmap/CORE/` (23 files) and `docs/refactor/` (22 files) were active planning surfaces in late 2025 and are now effectively historical

The main docbase (`docs/internal/`) is in reasonable shape. This is a perimeter cleanup, not a restructure of the core.

---

## What I Found

### Tier 1: "MOVED" stub directories

These contain only a `README.md` saying "this content moved to docs/internal/" — they are navigational tombstones with no other content:

| Directory | README says | Real content |
|-----------|-------------|--------------|
| `docs/architecture/` | "MOVED → docs/internal/architecture/" | `docs/internal/architecture/` |
| `docs/planning/` | "MOVED → docs/internal/planning/" | `docs/internal/planning/` |
| `docs/development/` | likely same pattern | `docs/internal/development/` |

`docs/planning/` also has `pm-issues-status.json` — needs one-time check if it's live or stale before removal.

**Risk**: Low. The redirects are informational only; no CI or code reads from these paths. Removing the stubs eliminates the confusion without losing anything.

### Tier 2: Legacy external-facing docs

~12 top-level directories that look like they were for an old developer-facing documentation site. Most were last meaningfully committed in Nov 2025; some have Jun 2026 commits that appear to be mechanical (link placeholder fills, not content updates).

| Directory | Files | Last real commit |
|-----------|-------|-----------------|
| `docs/refactor/` | 22 | Nov 2025 |
| `docs/guides/` | 15 | Jun 2026 (mech.) |
| `docs/installation/` | 7 | Nov 2025 |
| `docs/dev-tips/` | 5 | Feb 2026 |
| `docs/features/` | 5 | Jun 2026 (mech.) |
| `docs/alpha/` | 2 | Apr 2026 |
| `docs/api/` | 3 | Nov 2025 |
| `docs/accessibility/` | 3 | Jan 2026 |
| `docs/configuration/` | 2 | Jun 2026 (mech.) |
| `docs/integrations/` | 3 | Jun 2026 (mech.) |
| `docs/processes/` | 3 | Nov 2025 |
| `docs/references/` | 2 | Jun 2026 (mech.) |
| `docs/research/` | 1 | Mar 2026 |
| `docs/security/` | 1 | Jun 2026 |
| `docs/setup/` | 2 | Nov 2025 |
| `docs/troubleshooting/` | 2 | Oct 2025 |
| `docs/migration/` | 3 | Jul 2026 |

`docs/migration/` has a Jul 2026 date — needs a closer look before any action.

None of these appear in CLAUDE.md's Progressive Loading table or `docs/NAVIGATION.md`. They're not agent-facing references. They may have been intended for a user-facing docs site that was never launched.

**Risk**: Medium. Before archiving, need to confirm nothing in the live app or external links points to these paths. `docs/migration/` in particular has a recent date and warrants review.

### Tier 3: CORE/ directory

`docs/internal/planning/roadmap/CORE/` — 23 files (Alpha-era per-epic working documents, plus some cryptic single-word entries: `ALPHA`, `AUTH`, `CRAFT`, `GREAT`, `KEYS`, `KNOW`).

Last substantive commit: January 2026 (v0.8.4.3 doc updates). The June 2026 commit was a mass mechanical fill (`107 content-gap links → '(proposed; doc TBD)'`) — the content wasn't refreshed, just marked as stale.

PPM described these as "candidate for archival if nothing currently links to them." Quick link scan shows none appear in CLAUDE.md or NAVIGATION.md. These are historical Alpha-phase design docs, now effectively read-only artifacts.

**Risk**: Low-medium. Archive to `docs/internal/planning/historical/` or similar; no deletion until confirmed nothing links.

### Tier 4: Dual-structure areas (needs PM decision, not just cleanup)

Two areas have parallel content at both `docs/X/` and `docs/internal/X/` with different (not duplicate) content:

**Testing**:  
- `docs/testing/` — strategy and architecture docs (7 files: enforcement-system-overview, integration-test-strategy, etc.)
- `docs/internal/testing/` — canonical query matrices, test history, colleague rubrics (10+ files)

**Operations**:  
- `docs/operations/` — external-ish operational guides (startup-routines, alpha-onboarding, duty-cycle design, intent-monitoring-api, etc.)
- `docs/internal/operations/` — internal agent operational docs (CI/CD runbooks, deployment, environment, canonical retest history, etc.)

These aren't redundant — they're different content that ended up in parallel locations. The question is whether to merge them into `docs/internal/` or establish a clearer naming convention for the dual structure. This is a **PM decision on architecture**, not just a cleanup call.

---

## Proposed Phases

### Phase 1 — Remove "MOVED" stub shells (low risk, no PM decision needed beyond this plan)

Remove `docs/architecture/`, `docs/planning/` (after checking pm-issues-status.json), and `docs/development/` skeleton directories.  
**Expected: 3 directories, ~4 files removed.**

### Phase 2 — Archive CORE/ (PM approval before execution)

Move `docs/internal/planning/roadmap/CORE/` to `docs/internal/planning/historical/alpha-era-CORE-2025/`.  
Run link check first to confirm no active references.  
**Expected: 23 files moved, no deletions.**

### Phase 3 — Assess and archive legacy external docs (PM approval + scope decision)

Read a sample from `docs/guides/`, `docs/features/`, and `docs/migration/` to assess whether any are still live references. Archive confirmed-dead directories to `docs/_archive/` (or delete if genuinely valueless). Hold `docs/migration/` pending PM confirmation of its Jul 2026 recency.  
**Expected: 10–15 directories archived, ~60 files moved.**

### Phase 4 — Resolve testing/ and operations/ dual structure (PM decision first)

After PM decides the organizational intent (merge into docs/internal/, or establish a clear convention), execute accordingly. This is not a call Docs makes unilaterally.

---

## What Docs is NOT proposing

- Touching `docs/internal/` core content (ADRs, patterns, planning documents, omnibus logs) — that's a different and larger conversation
- Deleting anything without a link check first
- Making Phase 4 decisions without PM input

---

## Recommendation

Start with Phase 1 immediately (no PM approval gate needed beyond this plan review). Gate Phases 2–4 on PM review of this document.

---

*Next step: PM reviews this plan → Docs proceeds phase by phase.*
