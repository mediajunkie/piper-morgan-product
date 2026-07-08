# Weekly Docs Audit — #1375 Findings (in progress)

**Auditor**: Docs (scheduled-task fire, 2026-07-08 ~05:40 PDT)
**Issue**: #1375 "FLY-AUDIT: Weekly Docs Audit - 2026-07-07" (OPEN, overdue Jul-7 EOD)
**Status**: PARTIAL — mechanical/cheap checks done this fire; heavier subagent sweeps + README reviews remain (audit spans multiple days per its own FAQ). Issue left OPEN.

---

## Section results

| Section | Status | Evidence |
|---|---|---|
| **Briefing Freshness (PRIORITY)** | ✅ DONE | `BRIEFING-CURRENT-STATE.md` refreshed today — Jul-7 cross-cohort attest appended; `last_updated`/`last_verified` → 2026-07-08 (same fire). |
| **Omnibus Coverage** | ✅ PASS | Continuous Jul-1 → Jul-7, no gap >2 days (Jul-7 built this fire). No stranded session logs in `dev/active/`. |
| **Link Integrity (ADRs)** | ✅ PASS | `0` broken internal ADR links (portable python check). |
| **Quality Checks (backup/old files)** | ✅ PASS | No `*.backup`/`*.old` in `docs/ services/ web/ cli/`. |
| **Pattern & Knowledge Capture (count)** | ⚠️ FINDING | **README count stale.** `ls pattern-*.md` = **75 files**; README says "74 patterns" and also carries a stale "62 patterns" reference. README needs a reconciliation pass (which pattern # is undocumented + fix both stale counts). |
| **Sprint & Roadmap Alignment** | ⚠️ MINOR | `roadmap.md` last updated 2026-07-05 (3 days). Could reflect recent Beta Blockers closes (Epic A/#1304, #1317, #1105, #1279). Not stale-critical; flag for a sprint-completion update. |
| **GitHub Issues Sync** | ⏳ NOT RUN | Heavier — deferred to a later fire this week (not closing). |
| **Subagent sweeps** (stale >30d content, duplicate files, methodology cross-refs, NAVIGATION↔INDEX) | ⏳ NOT RUN | Token-efficiency: batch these into a single later fire with Haiku subagents. |
| **Root README.md review** | ⏳ NOT RUN | Judgment review — later fire. |
| **docs/README.md (pmorgan.tech) review** | ⏳ NOT RUN | Judgment review — later fire. |
| **CITATIONS.md completeness** | ⏳ NOT RUN | Later fire. |

## Findings to action

1. **Pattern README count drift** (75 actual vs 74/62 documented) — real discrepancy; the README carries two different stale counts. Needs a proper reconciliation (identify undocumented pattern, correct headline count). Flagged here per discovered-work discipline; candidate for a focused fix on a later Docs fire.
2. **Roadmap sprint-completion update** — reflect Jul-7 Beta Blocker closes.

## Note on completion discipline

No checklist item is being marked "deferred" at close (deferral policy requires PM approval). The issue stays **OPEN** and in-progress; the ⏳ sections are scheduled for a later fire this week, which is explicitly allowed ("Thoroughness over speed… can span multiple days"). No silent skipping — every section is accounted for above.
