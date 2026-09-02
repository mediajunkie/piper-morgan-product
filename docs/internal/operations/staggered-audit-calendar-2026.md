# Staggered Audit Calendar 2026

**Proposed**: January 3, 2026
**Purpose**: Prevent "audit week" clustering by offsetting recurring reviews
**Owner**: Chief of Staff (tracking), respective owners (execution)

---

## Audit Types & Cadences

| Audit Type | Cadence | Duration | Owner | Methodology |
|------------|---------|----------|-------|-------------|
| Pattern Sweep | 6 weeks | ~1 day | Lead Dev + specialized agents | `dev/active/pattern-sweep-2.0-framework.md` |
| Methodology Audit | Trigger-based (within 2 weeks of sprint gate closure, 8-week max interval) | ~2 hours | CIO | `methodology-audit-policy-updates-2026-03-16.md` |
| Documentation Audit (quality/accuracy) | **Weekly** | ~1 hour | Docs | `.github/workflows/weekly-docs-audit.yml` |
| Documentation Audit (housekeeping/infra) | **Monthly** (1st Mon) | ~1 hour | Docs | `.github/workflows/monthly-housekeeping-audit.yml` |
| Workstream Review | Weekly | ~1 hour | CoS + PM | N/A (informal) |
| Role Health Check | 4 weeks | ~30 min | HOST | `docs/internal/operations/role-health-check-methodology.md` |
| Skill-Candidates Review | **Monthly (1st Tue)** | ~20 min | PM + Exec (CIO/HOST triage input) | `docs/internal/operations/skill-candidates-review.md` |

**Cadence split ratified 2026-07-04** (HOST + CIO input, PM-authorized): weekly = quality/accuracy (briefing freshness, link integrity, README reviews, sprint alignment); monthly = housekeeping/infra (agent infra, dev/active cleanup, metrics, workflow improvement). HOST runs a separate 4-weekly welfare-lens pass on agent infrastructure.

**Skill-Candidates Review slotted 2026-07-09** (CIO, confirming HOST's proposal): every other row in this table is Monday-anchored (Doc Audit weekly + monthly, Role Health, Pattern Sweep all fire on Mondays per their GH workflow crons below) — 1st Tuesday is a genuinely clean offset, not just adjacent-day cosmetics. One real wrinkle: 1st-Tuesday usually falls the same week as Doc Audit's 1st-Monday housekeeping pass, which is within the "≤2 heavy audits/week" limit but worth naming — if a third heavy audit (Methodology, trigger-based) ever lands the same week, that's the one combination to watch.

---

## 2026 Calendar (Staggered)

### Q1 2026

| Week | Mon | Pattern Sweep | Methodology | Doc Audit | Role Health |
|------|-----|---------------|-------------|-----------|-------------|
| 1 | Jan 6 | | | ✓ | |
| 2 | Jan 13 | | | ✓ | |
| 3 | Jan 20 | | | ✓ | ✓ |
| 4 | Jan 27 | | | ✓ | |
| 5 | Feb 3 | ✓ | | ✓ | |
| 6 | Feb 10 | | | ✓ | |
| 7 | Feb 17 | | ✓ | ✓ | ✓ |
| 8 | Feb 24 | | | ✓ | |
| 9 | Mar 3 | | | ✓ | |
| 10 | Mar 10 | | | ✓ | |
| 11 | Mar 17 | ✓ | | ✓ | ✓ |
| 12 | Mar 24 | | | ✓ | |
| 13 | Mar 31 | | | ✓ | |

### Q2 2026

| Week | Mon | Pattern Sweep | Methodology | Doc Audit | Role Health |
|------|-----|---------------|-------------|-----------|-------------|
| 14 | Apr 6 | | ✓ | ✓ | |
| 15 | Apr 13 | | | ✓ | ✓ |
| 16 | Apr 20 | | | ✓ | |
| 17 | Apr 27 | ✓ | | ✓ | |
| 18 | May 4 | | | ✓ | |
| 19 | May 11 | | | ✓ | ✓ |
| 20 | May 18 | | | ✓ | |
| 21 | May 25 | | ✓ | ✓ | |
| 22 | Jun 1 | | | ✓ | |
| 23 | Jun 8 | ✓ | | ✓ | ✓ |
| 24 | Jun 15 | | | ✓ | |
| 25 | Jun 22 | | | ✓ | |
| 26 | Jun 29 | | | ✓ | |

---

## Offset Logic

**Pattern Sweep** (anchor): Weeks 5, 11, 17, 23, 29, 35, 41, 47
- 6-week intervals starting Feb 3

**Methodology Audit**: Weeks 7, 14, 21, 28, 35, 42, 49
- ~7-week intervals, offset 2 weeks from Pattern Sweep
- Never same week as Pattern Sweep

**Documentation Audit**: Every week (weekly)
- Runs every Monday via `.github/workflows/weekly-docs-audit.yml`
- ~1 hour per audit, lightweight but consistent
- Critical for project knowledge currency and agent reliability

**Role Health Check**: Weeks 3, 7, 11, 15, 19, 23...
- 4-week intervals
- Offset 1 week from Doc Audit
- Critical for HOST function

---

## Maximum Audit Load Per Week

**Design Principle**: No more than 2 *heavy* audits in any given week. Doc Audit is weekly and doesn't count toward the heavy audit limit.

**Worst Case**: Doc Audit + Pattern Sweep + Role Health (Week 11, 23 — ~3 hours total)

**Typical Case**: Doc Audit alone (~1 hour), or Doc Audit + one other (~2 hours)

---

## GitHub Workflow Implementation

### Pattern Sweep Workflow
```yaml
# .github/workflows/pattern-sweep-reminder.yml
name: Pattern Sweep Reminder
on:
  schedule:
    # Every 6 weeks on Monday at 9am UTC
    # Starting Feb 3, 2026
    - cron: '0 9 3 2 *'   # Feb 3
    - cron: '0 9 17 3 *'  # Mar 17
    - cron: '0 9 27 4 *'  # Apr 27
    - cron: '0 9 8 6 *'   # Jun 8
    # ... continue for year
```

### Documentation Audit Workflow
```yaml
# .github/workflows/weekly-docs-audit.yml
name: Weekly Documentation Audit
on:
  schedule:
    # Every Monday at 9am UTC
    - cron: '0 9 * * 1'
```

### Role Health Check Workflow
```yaml
# .github/workflows/role-health-reminder.yml
name: Role Health Check Reminder
on:
  schedule:
    # Every 4 weeks on Monday at 9am UTC
    - cron: '0 9 20 1 *'  # Jan 20
    - cron: '0 9 17 2 *'  # Feb 17
    - cron: '0 9 17 3 *'  # Mar 17
    # ... continue for year
```

---

## Issue Templates for Each Audit

### Pattern Sweep Issue Template
```markdown
---
name: Pattern Sweep
about: 6-week pattern analysis
labels: pattern-sweep, methodology
---

## Pattern Sweep: [Date Range]

**Period**: [Start] - [End]
**Lead**: Lead Developer (Specialist Instance)

### Checklist
- [ ] Pattern library index updated
- [ ] Usage analysis complete
- [ ] Novelty candidates identified
- [ ] Evolution tracking complete
- [ ] Meta-synthesis complete
- [ ] FALSE POSITIVE test passed
- [ ] Leadership summary prepared
- [ ] Ratification decisions documented

### Deliverables
- [ ] pattern-sweep-results-YYYY-MM-DD.md
- [ ] pattern-sweep-leadership-summary.md
- [ ] DRAFT-pattern-XXX.md (if any)
```

### Documentation Audit Issue Template
```markdown
---
name: Documentation Audit
about: Monthly documentation health check
labels: documentation, audit
---

## Documentation Audit: [Date]

**Owner**: Chief of Staff / Doc Manager

### Checklist

**🔗 Link Integrity (Priority)** - Added Feb 2026 per Ted Nadeau feedback
- [ ] ADR link audit: Check all `docs/internal/architecture/adrs/adr-*.md` for broken internal refs
- [ ] Pattern link audit: Check `pattern-*.md` for broken cross-references
- [ ] Briefing link audit: Check `docs/briefing/*.md` and `knowledge/BRIEFING-*.md`
- [ ] Document broken links found with file:line format
- [ ] Fix or file issues for broken links

**📊 Standard Checks**
- [ ] Stale documents identified (>90 days unchanged)
- [ ] README coverage verified (target: 100%)
- [ ] Navigation docs current
- [ ] Knowledge folder aligned with filesystem

### Metrics
- Broken internal links: ___ (target: <10 in priority files)
- Stale docs: ___
- Coverage: ___%

### Link Audit Notes
Files with broken links discovered:
- [ ] [file] line [N]: [broken link] → [resolution]

### Completion Matrix (REQUIRED)
| Section | Status | Evidence |
|---------|--------|----------|
| Link Integrity | ✅/⏸️/❌ | |
| Stale Docs | ✅/⏸️/❌ | |
| README Coverage | ✅/⏸️/❌ | |
| Navigation Docs | ✅/⏸️/❌ | |
| Knowledge Folder | ✅/⏸️/❌ | |

**⚠️ Deferral requires PM approval comment link. No silent skipping.**
```

### Role Health Check Issue Template
```markdown
---
name: Role Health Check
about: Monthly agent role health assessment
labels: sapient-trust, audit
---

## Role Health Check: [Date]

**Owner**: HOST / Chief of Staff (interim)

### Active Roles Assessed
| Role | Last Session | Drift Risk | Notes |
|------|--------------|------------|-------|
| Chief of Staff | | Low/Med/High | |
| Chief Architect | | | |
| Lead Developer | | | |
| Communications Director | | | |

### Checklist
- [ ] All active roles had session in past 2 weeks
- [ ] Briefing documents current
- [ ] No role drift detected
- [ ] Succession plans documented
- [ ] Prompt templates current
```

---

## Tracking Dashboard

CoS to maintain simple tracking:

| Audit Type | Last Completed | Next Due | Status |
|------------|----------------|----------|--------|
| Pattern Sweep | Feb 3, 2026 | Mar 17, 2026 | ✅ Complete |
| Methodology | Mar 15, 2026 | Trigger: next sprint gate | ✅ Complete (trigger-based per CIO policy) |
| Documentation (weekly — quality/accuracy) | Aug 24, 2026 | Aug 31, 2026 | ✅ Complete (#1681; full 8-section pass. 2 real fixes shipped: NAVIGATION.md missing Piper Alpha entry (`acd0e40e7`); a genuine 3-day omnibus gap (08-21/22/23) found + backfilled via 3 sequential subagent dispatches, chain continuous through 08-23. 1 significant finding escalated (2nd flag, zero movement since #1643's first): BRIEFING-CURRENT-STATE substantive content ~5-6 weeks stale despite a misleadingly-recent meta-date — mailed directly to Lead Dev + PPM. roadmap.md header-date discrepancy (from #1644) confirmed still unresolved, escalated same memo. `last_verified` bulk-stamp cluster down to 20 of 26 (from 23, modest progress, still cohort-wide unowned). #1475 (orphaned Aug 3 audit) closed as superseded. 3 minor findings consolidated in #1682 (stray test file, stray ADR-dir file, CITATIONS.md 5mo stale). Findings: closing comment on #1681. Prior: Aug 17 (#1643). |
| Documentation (monthly — housekeeping/infra) | Sep 2, 2026 | Sep 7, 2026 (1st Mon) | ✅ Complete (#1486, generated 2026-08-05, worked 2026-09-02 — 6+ weeks after generation, itself found + fixed by #1713's GH-Actions-scheduled-workflow investigation). All 7 sections done: Agent Infrastructure (37 skills verified, 10 hooks executable, mailbox delivery clean, 1 real gap fixed — `spec` role missing from ROSTER.md Tier 3); Infrastructure & Pattern Verification (app.py 401 lines, port-8080 refs clean, pattern/ADR counts match, ADR-067/068 gap confirmed already-tracked by Arch's own review); `dev/active/` Cleanup (183→33 files — 116 archived, 33 gitignored ephemeral `delta-*.md` deleted per a pre-established 2026-06-05 disposition, 2 held as <3-days-old; broke 22 live references across CLAUDE.md/briefings/operations docs, all repaired; filed **#1719** for the recurring "file moved, cross-refs not updated" structural pattern, now confirmed 4th instance); Session Log Archive Check (clean, omnibus chain current through the last Friday, on cadence); Metrics Snapshot (1923 docs, 75 patterns, 80 ADRs, 37 skills, 0 stranded session logs; test count not run — no Python env in this worktree); Workflow Improvement (this row + #1719 filed). Prior: Jul 2, 2026 (absorbed into #1341 quarterly sweep). |
| Role Health | Aug 31, 2026 | Sep 28, 2026 (4 weeks) | ✅ Complete (#1714). Period Aug 3–31. 11 roles assessed (10 cycling + Web off-cycle), Ted Nadeau explicitly marked unassessed (visibility gap, not guessed). Summary: 8 Low, 3 Medium (Comms briefing ~2.5mo stale; Arch's own portfolio predates the review Arch authored this same week; PA's portfolio the stalest `last_updated` found despite strong current self-awareness), 0 High/Critical. Session-log liveness 29/29 for every cycling role; all 11 carry-forwards ≤1 day old. Actual cadence ran ~3.5 weeks after #1478 (Aug 7 → Aug 31), earlier than the Sep 4 prediction — self-polling mechanism (fixed same-day in #1478) held. Prior: Aug 7 (#1478), Apr 16 + May 10 (#978). |
| Skill-Candidates Review | *(none yet)* | Aug 4, 2026 (1st Tue) | Ratified 2026-07-08 (PM); slot confirmed 2026-07-09 (CIO/HOST). First review not yet held. |

**Note**: Role Health Check methodology formalized Jan 31, 2026. First formal audit Feb 17, 2026.
HOSR provided informal baseline assessment Jan 31 showing all roles Low/Medium risk.

Apr 16 audit (Q2 Week 15) by predecessor HOST instance covered Mar 17 → Apr 16 window. May 10 audit (Q2 Week 19, closing #978) covered Apr 13 → May 10 window and absorbed the migration arc; full artifact at `dev/2026/05/10/host-role-health-check-2026-05-10.md`. Findings: 8 roles Low, 4 Medium findings, 1 High (team-structure.md 4-month staleness), 0 Critical.

---

## Adjustment Protocol

If an audit needs to slip:
1. Move by 1 week maximum
2. Don't create collision with other audits
3. Document reason in tracking dashboard
4. Don't skip entirely - defer to next slot

If project phase requires pause (e.g., major release):
1. PM can suspend non-critical audits (Doc, Role Health)
2. Pattern Sweep and Methodology should still run
3. Document suspension and resume date

---

## Success Metrics

**After 3 months**:
- No week with >2 audits
- All audits completed within 1 week of scheduled date
- Pattern library growing (target: 50+ patterns by Q2)
- Documentation health: <30 broken links sustained
- Role drift incidents: <2 per quarter

---

*Calendar proposed by Chief of Staff*
*January 3, 2026*
*For implementation via GitHub Actions*
