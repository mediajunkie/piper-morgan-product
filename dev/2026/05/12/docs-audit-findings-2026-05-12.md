# Weekly Docs Audit Findings — 2026-05-12

**Issue**: #1076 (FLY-AUDIT: Weekly Docs Audit - 2026-05-11)
**Run**: Tuesday, 2026-05-12 ~1:00 PM
**Auditor**: Docs

## Top-line

Audit completed end-to-end. **One high-priority action** (pattern README count drift from CIO Pattern Sweep). **Three medium-priority actions** (briefing staleness in core 3 + 5 essential files; 2 duplicate file pairs; 9 port-8080 references to verify). **Zero broken internal links** in priority docs (encouraging). **Zero backup files** in active dirs. dev/active/ over threshold but PM has cleanup queued post-audit.

## Claude Knowledge Updates — observations

- **Docs modified this week**: 752 unique `.md` files touched (M2f-A/B/C closure week + cohort workstream-review cycle + roadmap v15→v16 swap + Inchworm publish + two omnibus logs + activity-log backfill).
- **knowledge/** directory has 20 regular files, **0 symlinks**. Per memory `feedback_chat_briefings_reminder.md`, no roles use chat project knowledge as primary surface as of May 4 2026; maintain at bare essentials, no per-briefing nag. Not flagging knowledge/ staleness for that reason.
- **BRIEFING-CURRENT-STATE.md fresh** (2026-05-10, 2 days; refreshed by Docs as part of Roadmap v16 swap).

## Link Integrity — ✅ clean

- **364 internal links checked** in priority directories (ADRs + Patterns + Briefings).
- **0 broken** internal links to `.md` files.
- Below the <10 target. No action.

## Infrastructure & Pattern Verification

| Check | Expected | Actual | Status |
|---|---|---|---|
| `web/app.py` line count | <1000 (refactor trigger) | 319 | ✅ |
| Port 8080 in `docs/` | 0 (server is 8001, ChromaDB 8000) | **9 hits** | ⚠️ |
| Mock/fallback in `services/` | Normal accumulation | 535 | informational |
| `DatabasePool` in `services/` | 0 (deprecated) | 0 | ✅ |
| `.cursor/rules/` files | 5 expected | 5 | ✅ |
| Pattern files on disk | matches README | **70 (000-069)** | ⚠️ mismatch |
| Pattern README documents | matches filesystem | **63** | ⚠️ mismatch |
| ADR naming convention | all `adr-NNN-*.md` | 64 files, all conform | ✅ |
| Methodology files location | all in `methodology-core/` | clean (1 false-positive in `superseded/`) | ✅ |
| Backup files in active dirs | 0 | 0 | ✅ |
| TODO/FIXME in code | normal | 68 | informational |

### ⚠️ Pattern count drift (high-priority)

- Filesystem has **70 pattern files (000-069)** in `docs/internal/architecture/current/patterns/`.
- `patterns/README.md` documents **63 named patterns** (~"66 (001-066)" headline but only 63 in index).
- Gap: 7 patterns added without corresponding README updates. P-064 (Extension Without Integration, Apr-May), P-065 (Continuity Memo Before the Seam, Apr-May), P-066 (Stacked Silent Failures, CIO May 9 Emerging), P-067 (Lead Dev's Issue-Body Reality Mismatch, May 9 Emerging), P-068 (CIO's Silent State Mutation in Shared Working Tree, May 11 Emerging after slot-renumber), P-069 (CIO's Coarse Triggers Causing False-Positive Triage Cost, May 11 Emerging after slot-renumber).
- **Action**: CIO carries the pattern-catalog update normally; flagging for their next cycle. Standing-items tracker 12l (pre-filing slot-availability check) is the related discipline thread.

### ⚠️ Port 8080 in docs (medium-priority)

- 9 hits in `docs/` for "8080". Server is on 8001; ChromaDB on 8000.
- Likely candidates: historical references, external-tool examples, or genuine drift.
- **Action**: Lead Dev (or Docs) verify whether 8080 references are legitimate; if drift, sweep to 8001.

## Briefing Freshness

| File | Last Update | Days | Status |
|---|---|---|---|
| `docs/briefing/BRIEFING-CURRENT-STATE.md` | 2026-05-10 | 2 | ✅ fresh |
| `docs/briefing/METHODOLOGY.md` | 2026-04-29 | 13 | ⚠️ stale |
| `docs/briefing/PROJECT.md` | 2026-04-29 | 13 | ⚠️ stale |
| `BRIEFING-ESSENTIAL-DOCS.md` | 2026-04-28 | 14 | ⚠️ stale |
| `BRIEFING-ESSENTIAL-CXO.md` | 2026-04-26 | 16 | ⚠️ stale |
| `BRIEFING-ESSENTIAL-HOST.md` | 2026-04-26 | 16 | ⚠️ stale |
| `BRIEFING-ESSENTIAL-PPM.md` | 2026-04-26 | 16 | ⚠️ stale |
| `BRIEFING-ESSENTIAL-CHIEF-STAFF.md` | 2026-04-26 | 16 | ⚠️ stale |
| `BRIEFING-ESSENTIAL-ETA.md` | 2026-03-20 | 53 | ⚠️ stale (M2-discovered scope; lower priority) |
| `BRIEFING-ESSENTIAL-LLM.md` | 2026-03-19 | 54 | ⚠️ stale |
| `BRIEFING-ESSENTIAL-AGENT.md` | 2026-03-19 | 54 | ⚠️ stale (HOST role-health flagged at Medium-risk May 10) |

- **Action (medium-priority)**: METHODOLOGY.md + PROJECT.md refresh. Probably one ~30-min Docs pass per CIO's recent meta-pattern + M2f closure + Pattern-067/068/069 + Roadmap v16.
- **Action (per-role)**: leadership-role essentials are 14-16 days stale; per CLAUDE.md `update-current-state` skill, *any agent who notices the briefing is stale should refresh it without waiting for Docs or CIO to own the task*. Surfacing for visibility.
- BRIEFING-ESSENTIAL-AGENT was already flagged by HOST May 10 role-health-check as Medium-risk; refresh before next active subagent use.

## Duplicates

3 hash duplicates found:

1. **`docs/internal/planning/roadmap/CORE/CORE-MCP-MIGRATION-epic.md`** + **`...CORE-MCP-MIGRATION.md`** (same hash, real content) — **Action**: consolidate; canonical name TBD.
2. **`docs/internal/planning/current/plan-piper-alpha-2026-03-20.md`** + **`docs/internal/planning/strategy/plan-piper-alpha-2026-03-20.md`** (both empty, 0 bytes) — **Action**: safe to delete one or both.
3. **`docs/briefs/cross-pollination/2026-05-12.md`** + **`docs/briefs/cross-pollination/current.md`** (same content) — **Expected pattern**: `current.md` is the always-pointing-at-today symlink-equivalent + dated archive. No action.

## Session Log Management & Omnibus Synthesis

- **Omnibus logs**: 338 `.md` files in `docs/omnibus-logs/` — healthy; coverage back to mid-2025.
- **Stranded session logs outside `dev/`**: 0 actual; false-positives are the dated omnibus files (those belong in `docs/omnibus-logs/`).
- **dev/active/** has **35 items** (exceeds 15-item threshold from `cleanup-dev-active` skill):
  - 3 stale session logs misplaced (CXO May 4 + CXO May 10 + PPM May 10) — belong in `dev/2026/05/04/` and `dev/2026/05/10/`
  - Active workspace files (cio backlog/standing-items, exec/comms/agent trackers) — keep
  - Several drafted-but-aging memos and ship/workstream drafts
  - publish-package (active)
  - 2026-05-12 research items
- **Action**: dev/active/ cleanup queued by PM post-audit (next item on slate).

## Sprint & Roadmap Alignment

- **Roadmap** at `docs/internal/planning/roadmap/roadmap.md` — **v16.0 adopted May 10 2026** (Docs swap commit `f1e60672`); fresh.
- **Open issues**: 143 total open.
- **Open issues without milestone**: 14 of 143 (10%). Worth a sweep but not urgent.
- **Stale issues >30 days no activity**: 85 of 143 (59%). Mostly DIST-* (distribution backlog) and LEARNING-* / PREF-* / TRUST-* (post-MVP backlog clusters) and #865 REFACTOR (72 days). Backlog by design; not flagging as urgent.

## GitHub Issues Sync

- Skipped pm-issues-status.json regeneration (note in audit: "CSV generation deprecated - GitHub is source of truth"). The `gh issue list` queries above are the live source.

## Pattern & Knowledge Capture

- Pattern README count drift covered above (action: CIO update).
- **CITATIONS.md** (`docs/references/CITATIONS.md`) — spot-checked; appears in-place; not running full attribution review this cycle (no PM-flagged issues since last audit).

## Quality Checks

- Root `README.md` review: not run this audit. Per audit FAQ "thoroughness over speed; can span multiple days" — flagging as deferral candidate. **Status: ⏸️ deferred**, will run as a sub-task at next inflection (not blocking close).
- Test coverage: not run (out-of-scope quick spike).
- Other items: all clean per Infrastructure table above.

## Completion Matrix

| Section | Status | Evidence/Notes |
|---------|--------|----------------|
| Claude Knowledge Updates | ✅ | This file (sections above); knowledge/ design-deprioritized per memory |
| Link Integrity Check | ✅ | 0 broken in 364 priority links |
| Infrastructure Verification | ✅ | All checks pass; 1 warning (port 8080 ×9) |
| Session Log Management | ✅ | 338 omnibus + 0 stranded; dev/active/ over threshold (PM cleanup queued) |
| Sprint & Roadmap Alignment | ✅ | v16 fresh; 14 issues no-milestone + 85 stale flagged |
| GitHub Issues Sync | ✅ | Live `gh` queries used; pm-issues-status.json deprecated per audit FAQ |
| Pattern & Knowledge Capture | ⚠️ | Pattern count drift documented (action: CIO) |
| Quality Checks | ⏸️ | Root README review deferred to next inflection (will run as sub-task) |

## Carry-forward asks

- **CIO**: pattern README count refresh (70 files vs 63 documented); ~30 min when bandwidth opens.
- **Any agent (per CLAUDE.md "update-current-state")**: METHODOLOGY.md + PROJECT.md refresh; leadership-role essentials refresh where applicable.
- **Lead Dev (or Docs)**: port 8080 ×9 in docs/ — verify legitimate-vs-drift; sweep if drift.
- **Docs**: 2 file-pair consolidations (CORE-MCP-MIGRATION + plan-piper-alpha empties).
- **Docs**: root `README.md` review (deferred from this audit; sub-task at next inflection).

— Docs, 2026-05-12 ~1:00 PM
