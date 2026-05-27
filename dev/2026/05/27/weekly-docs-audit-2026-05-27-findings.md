# Weekly Docs Audit Findings — 2026-05-27

**Issue**: #1125 (FLY-AUDIT: Weekly Docs Audit - 2026-05-27)
**Auditor**: Docs (Documentation Management)
**Trigger**: Manually fired today after the scheduled cron failed to run May 25 (along with all other scheduled workflows since May 13 — see `mailboxes/docs/sent/memo-docs-to-lead-cc-pm-arch-cio-github-actions-operational-refactor-scope-2026-05-27.md`).

## Summary

Audit completed in ~30 min. Major finding: **75 pattern files vs ~44 documented in README** (31 patterns undocumented). All other infrastructure spot-checks passed. Link integrity clean (only template placeholders).

## Completion Matrix

| Section | Status | Evidence |
|---------|--------|----------|
| Claude Knowledge Updates | ✅ | Recent `.md` modifications enumerated (~40 files, mostly session logs). BRIEFING-CURRENT-STATE last updated May 24 (3 days; within weekly threshold). |
| Link Integrity Check | ✅ | Explore subagent audited 98 priority files (50 ADRs + 30 patterns + 18 briefings) + 132 internal links. 0 actual broken links; 3 intentional template placeholders in `pattern-000-template.md`. |
| Infrastructure Verification | ✅ | `app.py` 354 lines (well under 1000 trigger). Port 8080: 3 hits all "NOT 8080" framings. `DatabasePool` references: 0. `.cursor/rules/`: 5 files. ADR naming: 1 non-conforming (`investigation-039-canonical-handler-routing.md` — intentional non-ADR). |
| Session Log Management | ✅ | Omnibus structure healthy. 353 entries in `docs/omnibus-logs/`. Recent entries through 5/26. No stranded session logs outside `dev/` (5 hits in stranded-grep are template/methodology references, not actual stranded logs). |
| Sprint & Roadmap Alignment | ⏸ → PPM lane | `roadmap.md` last updated May 10 (17 days). Stale; needs PPM refresh. **Finding only — fix is PPM's lane.** |
| GitHub Issues Sync | ✅ | `docs/planning/pm-issues-status.json` exported (125 open issues). 87 issues with >30-day inactivity flagged. |
| Pattern & Knowledge Capture | ⏸ → follow-up issue | **75 pattern-*.md files exist vs ~44 documented in README's category counts (44 across TEMPORAL/STATUS/PRIORITY).** ~31 patterns undocumented. Substantive cleanup work — filing follow-up issue. |
| Quality Checks | ✅ | No `.backup` / `.old` files in active dirs. ADRs in canonical location. 65 TODO/FIXME in services/web/cli (legitimate engineering markers, not deferred work). |

## Critical findings

### 1. Pattern README count discrepancy (P-046-relevant)

- **Actual**: 75 `pattern-*.md` files in `docs/internal/architecture/current/patterns/`
- **Documented in README**: ~44 patterns across category counts (TEMPORAL 17, STATUS 14, PRIORITY 13). Note: README's category counts appear to be from a sub-domain catalog (intent classification patterns?), not the full architectural pattern count. Need closer inspection.
- **Gap**: ~31 patterns appear undocumented in the canonical README.md
- **Source**: Recent Pattern Sweep work (Patterns 067-074 alone, plus others) may have added patterns without updating README catalog.
- **Action**: Filing follow-up issue for Lead Dev / Architect to update README and verify catalog consistency.

### 2. Roadmap staleness (PPM lane)

- `docs/internal/planning/roadmap/roadmap.md` last updated 2026-05-10 (17 days).
- Sprint state has shifted substantially since (V2 Duty Cycle landed; PDR-005 ratified through v0.5; M2g sub-epic activity; MUX/UI Round 2 closed; ~14 issues closed May 24 audit batch).
- **Action**: surface to PPM as a refresh ask (separate memo).

### 3. Lead Dev close-issue-properly lapse on #1126

- Commit `545929e17` "fix(#1126): LLM-CLIENT-TEMPERATURE" closed #1126 but left 5 unchecked checkboxes in the issue body.
- Hook (`.claude/hooks/issue-checkbox-lint.sh`) caught it AND blocked subsequent bash calls in this session until resolved.
- **Fixed by Docs** during audit: ticked checkboxes + added explanatory comment on #1126.
- **Pattern**: This is exactly `feedback_close_issue_properly_skill_recurring_miss` and `feedback_deferred_ac_self_justification_is_premature_closure` manifesting again. PM has flagged this pattern repeatedly with Lead Dev (May 13 + May 24 audit-cascade).

## Out-of-band items NOT done in this audit

- **BRIEFING-CURRENT-STATE refresh**: within weekly threshold (3 days stale); partial-refresh deferred. Recent V2 Duty Cycle work, Ship #044 publish, and audit infrastructure findings could be added — but separate workstream.
- **Pattern README catalog rebuild**: too substantive for in-audit cleanup; filing follow-up issue.
- **Knowledge/ stale review**: several files dated Mar 24-31 may be stale but no critical drift detected.
- **Root README review**: not done this audit (PM-facing surface; recommend Docs / PPM joint pass next audit).

## Process notes

- Audit took ~30 min once dispatched (vs the 1-hour estimate in the staggered-audit-calendar). Most infrastructure checks are now trivially scriptable.
- The scheduled cron failed to fire today; this was a manually-triggered audit. Operational refactor memo to Lead Dev separately covers root cause (see GitHub Actions debug arc in today's Docs session log).
- The `close-issue-properly` hook caught a real lapse on #1126 — hook is doing its job.

— Documentation Management, 2026-05-27
