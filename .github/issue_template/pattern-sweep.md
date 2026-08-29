---
name: Pattern Sweep 2.0
about: Recurring multi-lens pattern analysis to detect true emergence vs pattern usage
title: 'PATTERN-SWEEP: [Date Range]'
labels: 'process, patterns'
assignees: ''
---

# Pattern Sweep 2.0 - [Date Range]

**Generated**: [Date]
**Lead**: Lead Developer
**Framework**: `dev/active/pattern-sweep-2.0-framework.md`

---

## Scope

**Analysis Period**: [Start Date] - [End Date]
**Pattern Library**: `docs/internal/architecture/patterns/` (check count)

---

## Pre-Sweep Checklist

- [ ] Pattern library index exists or needs regeneration
- [ ] Data sources available for analysis period:
  - [ ] `docs/omnibus-logs/` for the period
  - [ ] `dev/YYYY/MM/` session logs
  - [ ] Git history accessible

---

## Phase 1: Pattern Library Index (Agent A - Haiku)

**Task**: Create/update `dev/active/pattern-library-index.json`

**Acceptance Criteria**:
- [ ] All patterns in catalog indexed
- [ ] Each pattern has signature terms
- [ ] Valid JSON output
- [ ] Categories assigned

---

## Phase 2: Multi-Lens Analysis (Agents B-E in parallel)

### Agent B: Usage Analyst (Haiku)
- [ ] Create `dev/active/pattern-usage-analysis.md`
- [ ] Frequency counts per pattern
- [ ] Top 10 most-used identified
- [ ] Unusual applications flagged

### Agent C: Novelty Detector (Sonnet)
- [ ] Create `dev/active/pattern-novelty-candidates.md`
- [ ] Candidates verified against library
- [ ] FALSE POSITIVE TEST passed
- [ ] 5-tier classification applied

### Agent D: Evolution Tracker (Sonnet)
- [ ] Create `dev/active/pattern-evolution-report.md`
- [ ] Variations documented
- [ ] Anti-patterns identified
- [ ] **Anti-pattern index updated** (`docs/internal/architecture/current/anti-pattern-index.md`)
- [ ] Lifecycle stages assigned

### Agent E: Meta-Pattern Synthesizer (Opus)
- [ ] Create `dev/active/pattern-meta-synthesis.md`
- [ ] Meta-patterns identified
- [ ] Pattern-045 connections explored
- [ ] Process recommendations made

---

## Phase 3: Anti-Pattern Index Update

**New for 2026**: Update the anti-pattern index as part of each sweep.

- [ ] Scan new/modified patterns for anti-patterns
- [ ] Scan new/modified ADRs for anti-patterns
- [ ] Add new entries with stable IDs (G-xx, T-xx, A-xx, P-xx, I-xx)
- [ ] Update reverse index (Pattern → Anti-patterns)
- [ ] Update "Last Scan" date in index

**Reference**: `docs/internal/architecture/current/anti-pattern-index.md`

---

## Phase 3a: Emergent Anti-Pattern Scan

**Automated Detection** (validated in Phase 2 experiment - 63% precision):

Run the extraction scripts and classify candidates:

```bash
# Best strategy (60% precision) - session log lessons learned
./scripts/extract-session-lessons.sh [start_date] [end_date]

# Code comment mining (50% precision)
./scripts/extract-code-comments.sh services/

# ADR rejected alternatives (28% precision, highest volume)
./scripts/extract-adr-rejected.sh
```

**Classification Workflow**:
- [ ] Run `extract-session-lessons.sh` for analysis period
- [ ] Run `extract-code-comments.sh` against changed directories
- [ ] Run `extract-adr-rejected.sh` for new/modified ADRs
- [ ] Review candidates and classify: TRUE EMERGENT / VARIATION / FALSE POSITIVE
- [ ] Document all candidates in `dev/active/emergent-anti-pattern-candidates.md`

**⚠️ HUMAN REVIEW GATE** (Required):
- [ ] **Chief Architect or PM reviews** `emergent-anti-pattern-candidates.md`
- [ ] Human approves which TRUE EMERGENT candidates merge to index
- [ ] Only after approval: Add approved entries to anti-pattern-index.md with stable IDs

**Why**: ~37% false positive rate in automated detection. Anti-patterns are traps, bad habits, and seductive fake patterns - not pattern negation. Human judgment required to distinguish genuine anti-patterns from noise.

**Expected Outcomes**: 5-15 candidates per sweep, ~60% precision (based on Phase 2 experiment)

---

## Phase 4: Synthesis & Validation

- [ ] Final report created in `docs/internal/development/reports/`
- [ ] All validation test cases pass:
  - [ ] Known patterns NOT flagged as new
  - [ ] TRUE EMERGENCE has evidence trail
- [ ] DRAFT-pattern files created for any TRUE EMERGENCE

---

## Classification Tiers

1. **TRUE EMERGENCE** - Genuinely new pattern
2. **PATTERN EVOLUTION** - Variation of existing
3. **PATTERN COMBINATION** - Novel mixing of known patterns
4. **PATTERN USAGE** - Standard application
5. **ANTI-PATTERN** - Degradation or misuse

---

## Phase 5: Skill Formalization Review

**New for 2026**: Evaluate skill candidates for formalization during each sweep.

**Reference**: `.claude/skills/SKILLS.md` (rubric and candidates)

### Rubric (Score ≥ 3 to formalize)

| Criterion | Signal |
|-----------|--------|
| Frequency | Happens 3+ times/week across agents |
| Friction | Agents doing it inconsistently |
| Error Cost | Mistakes cause rework/PM intervention |
| Docs Exist | Procedure written somewhere (not yet skill) |
| Cross-Role | Multiple roles need it |

### Checklist

- [ ] Review `dev/active/skill-harvest-candidates.md`
- [ ] Score top 3-5 candidates against rubric
- [ ] Formalize any scoring ≥ 3 (spec → draft → audit → pilot)
- [ ] Add new candidates discovered during sweep
- [ ] Update `.claude/skills/SKILLS.md` adoption status

**Expected Outcomes**: 1-2 new skills formalized per sweep

---

## Expected Outcomes

Based on previous sweeps:
- TRUE EMERGENCE: 0-2 patterns per 6 weeks
- PATTERN EVOLUTION: 5-10 refinements
- PATTERN USAGE: 40+ applications
- SKILL FORMALIZATION: 1-2 new skills per sweep

---

## Deliverables Checklist

- [ ] `dev/active/pattern-library-index.json`
- [ ] `dev/active/pattern-usage-analysis.md`
- [ ] `dev/active/pattern-novelty-candidates.md`
- [ ] `dev/active/pattern-evolution-report.md`
- [ ] `dev/active/pattern-meta-synthesis.md`
- [ ] `docs/internal/development/reports/pattern-sweep-2.0-results-YYYY-MM-DD.md`
- [ ] `docs/internal/architecture/current/anti-pattern-index.md` (updated)
- [ ] `dev/active/emergent-anti-pattern-candidates.md` (Phase 3a output)
- [ ] DRAFT-pattern files (if TRUE EMERGENCE found)
- [ ] `.claude/skills/SKILLS.md` (updated if skills formalized)

---

## Success Criteria

- [ ] FALSE POSITIVE TEST passed (known patterns not flagged as new)
- [ ] All 5 agent deliverables complete
- [ ] Anti-pattern index updated with new entries
- [ ] Final report in reports directory
- [ ] GitHub issue updated with results
- [ ] Session log completed
- [ ] Skill candidates evaluated (Phase 5)

---

## Notes

[Add any specific focus areas or context for this sweep]

---

**Methodology**: Pattern Sweep 2.0 (#524)
**Template Version**: 1.4 (January 21, 2026) - Added Phase 5 skill formalization review
