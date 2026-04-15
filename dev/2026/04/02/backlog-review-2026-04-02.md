# Backlog Review — April 2, 2026

**Author**: Piper Alpha (PA)
**Status**: SUPERSEDED by `backlog-deep-review-2026-04-07.md` and `roadmap-restructure-proposal-2026-04-08.md`
**Note**: This initial review led to a deeper analysis (Apr 7) which informed the roadmap restructure (Apr 8). The closure/revision recommendations below are now captured with full rationale in the deep review. The MVP scope triage recommendations evolved into the differentiator-stack-based sprint restructure. Refer to the later documents for current thinking.
**Source**: GitHub issues via `gh` CLI, cross-referenced with roadmap and BRIEFING-CURRENT-STATE

---

## Summary

**119 open issues** across 4 milestones + 1 un-milestoned. The backlog is well-milestoned and reflects the project's anticipatory planning style. Main concerns: MVP milestone carries 89 issues targeting May 27, and 6-8 issues appear superseded by intervening work.

| Milestone | Open | Closed | Completion | Due |
|-----------|------|--------|------------|-----|
| MVP | 89 | 578 | 87% | May 27, 2026 |
| Fast Follow | 13 | 0 | 0% | Jul 31, 2026 |
| Post-MVP | 5 | 0 | 0% | Oct 30, 2026 |
| Enterprise | 13 | 0 | 0% | Apr 15, 2027 |
| None | 1 (#938) | — | — | — |

---

## Recommended Closures (Superseded)

These issues have been overtaken by more specific, recent work:

| # | Title | Superseded By | Recommendation |
|---|-------|--------------|----------------|
| 167 | INFR-TEST: Review regression testing | #927-930 (E2E/AAXT track) | Close |
| 191 | POST-TEST-E2E: Web UI E2E Testing | #927-930 | Close |
| 273 | TEST-SMOKE: Smoke test coverage | #927-930 | Close |
| 276 | TEST-SMOKE-CI: Smoke test CI | #930 (CI integration) | Close |
| 241 | CORE-ETHICS-TUNE: Post-Alpha Ethics | ADR-060, CXO boundary work, floor-first routing | Review & likely close |
| 310 | CONV-UX-QUICK: Settings quick wins | Significant UX shipped since Nov 2025 | Audit remaining scope; likely close |

---

## Worth Reviewing (May Be Outdated)

| # | Title | Last Updated | Question |
|---|-------|-------------|----------|
| 146/147/148 | FLY-VERIFY trilogy | Nov 15, 2025 | Superseded by audit-cascade + CLAUDE.md framework? |
| 302/309/315 | CONV-MCP series | Nov 15, 2025 | MCP strategy has evolved — still the right decomposition? |
| 312/313 | CONV-UX-DESIGN/DOCS | Nov 15, 2025 | MUX work may have absorbed some of this |
| 355 | DOCS-STOPGAP | Nov 21, 2025 | Canonical handler work (#904/903/902) may cover this |
| 463/465 | FLY-COORD-TREES | Dec 31, 2025 | Git worktree approach — still intended? |
| 118 | INFR-AGENT: Multi-Agent Coordinator | Old | Agent architecture has evolved significantly |
| 272 | RESEARCH-TOKENS-THINKING | Oct 25, 2025 | Model strategy may have changed |

---

## Duplicate/Overlapping Clusters

| Cluster | Issues | Note |
|---------|--------|------|
| Testing strategy | #167, #191, #273, #276 vs #927-930 | Old set should close in favor of new |
| In-memory storage | #935, #936, #760, #746 | Same root problem — cross-reference |
| MUX lifecycle UI | #703, #704, #712, #713, #714 | Well-decomposed but verify against shipped MUX work |
| Epic trackers | #470, #471, #472 | Review whether these are adding value as roll-ups |

---

## MVP Scope Concern

89 open issues targeting May 27 is nominally alarming. However:
- ~30 are DIST, CONV-FEAT, and MUX clusters that are likely Fast Follow candidates
- ~15 are WIRE stubs that depend on unbuilt features
- The sprint-level work (M2 issues #927-930, #934; M5 issues #921, #932-936) is well-defined and actionable

**Recommendation**: A triage pass to move non-essential MVP items to Fast Follow would reduce noise and make the MVP milestone more honest. Prime deferral candidates:
- DIST epic (#828-837) — 10 issues, entire distribution packaging sprint
- CONV-FEAT cluster (#100-106) — ambitious AI features
- MUX lifecycle UI cluster (#703-714) — UI polish
- Heavy infrastructure (#371, #372, #463, #465, #557)

---

## Un-Milestoned

Only #938 (Q2 Maintenance Sweep) — assign to MVP or leave as standing process artifact. Non-issue.

---

## Sprint Readiness (M2)

The M2-assigned issues are well-defined and actionable:
- #927-930: E2E/AAXT testing track (clear scope, dependencies documented)
- #934: Orphaned stub investigation (small, bounded)

Additional MVP issues that are sprint-ready but not yet assigned to a specific sprint:
- #925: Floor inversion Phase 3-4
- #900: Standup 3-part collection
- #869: Project configuration IA
- #864-865: Intent coverage + setup wizard refactor

---

*This review is intentionally conservative about closure recommendations. Per project convention, stale issues are anticipatory drafts that get audit-cascaded when their sprint arrives. Only issues clearly superseded by specific newer work are recommended for closure.*
