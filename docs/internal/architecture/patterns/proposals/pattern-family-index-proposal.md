# Proposal: Pattern Family Index Format

**Author**: Docs Agent
**Date**: February 5, 2026
**Requested by**: CIO (memo-cio-pattern-sweep-response-2026-02-04)
**Timeline**: Proposal due by February 19, 2026 — this is the initial draft for CIO review

---

## Problem Statement

The pattern catalog has grown to 61 patterns. Pattern Sweep 2.0 identified that patterns work best in family units, not individually. However, the catalog currently organizes patterns by *category* (Core Architecture, Data & Query, etc.) rather than by *family* (Completion Theater, Grammar Application, etc.).

Categories describe *what* a pattern is about; families describe *how* patterns work together. Both views are needed.

The CIO approved a 3-tier approach (established / emerging / unaffiliated) and recommended embedding family references in skills and gameplan templates rather than requiring memorization.

---

## Proposed Format

### Pattern Family Index (New File)

A new `PATTERN-FAMILIES.md` alongside the existing `README.md` (category index) and `META-PATTERNS.md`:

```markdown
# Pattern Family Index

## Tier 1: Established Families
_Proven pattern groups with documented co-occurrence and reinforcing effects._

### Completion Theater Family
**Patterns**: 045, 046, 047, 049
**Health**: Excellent
**Use when**: Multi-phase work, closing issues, preventing premature completion
**Quick reference**: 045 diagnoses → 046 enforces → 047 enables pause → 049 audits

### Investigation & Root Cause Family
**Patterns**: 006, 041, 042, 043, 060
**Health**: Excellent
**Use when**: Bug fixing, incident response, security investigation
**Quick reference**: 006 verifies → 042 investigates → 060 cascades → 041 plans → 043 prevents

### Grammar Application Family
**Patterns**: 050-058
**Health**: Strong
**Use when**: New feature development, UX work, intent classification
**Quick reference**: Apply all 9 for "Conscious" rating on features

## Tier 2: Emerging Families
_Pattern groups with initial evidence but not yet proven across multiple contexts._

### Multi-Agent Coordination Family
**Patterns**: 029, 059, 021, 010, 037
**Health**: Medium
**Use when**: Cross-domain decisions, parallel agent work
**Note**: 059 (leadership alignment) and 029 (technical execution) are complementary, not competing

### Analysis & Discovery Family
**Patterns**: 036, 037, 038, 039
**Health**: Experimental
**Use when**: System analysis, pattern detection, feature prioritization

## Tier 3: Unaffiliated Patterns
_Patterns not yet assigned to a family. May join existing families or form new ones._

### Architecture & Data Patterns
001-008, 013-017, 023, 025, 026, 034 — HEALTH CHECK NEEDED

### Integration & Platform Patterns
018, 027, 030, 031, 033, 035, 040, 044, 048

### AI & Intelligence Patterns
012, 019, 020, 022, 028, 032

### Standalone Process Patterns
009, 011, 024
```

### Key Design Decisions

1. **Two indexes, not one**: The category index (README.md) stays for "find a pattern by topic." The family index adds "find patterns that work together." Neither replaces the other.

2. **Tier classification**:
   - **Established**: 3+ co-occurrence instances documented, reinforcing effects proven
   - **Emerging**: Initial co-occurrence observed, still building evidence
   - **Unaffiliated**: Not yet grouped — either standalone or awaiting evidence

3. **Quick reference lines**: One-sentence operational guide for each family. Designed for embedding in skills/templates without requiring full pattern knowledge.

4. **Health status**: Carried forward from sweep analysis. Triggers health checks when status is "Unknown."

---

## Integration Points

### Skills (`.claude/skills/`)

Add family references to relevant skills. Example for `close-issue-properly`:

```markdown
## Relevant Pattern Families
- **Completion Theater** (045/046/047/049): Verify completion is real, not theatrical
- **Investigation** (006/041-043/060): If issue involved bug investigation
```

### Gameplan Templates

Add a "Pattern Families" section to gameplan templates:

```markdown
## Applicable Pattern Families
- [ ] Completion Theater (multi-phase work)
- [ ] Investigation (bug-related work)
- [ ] Grammar Application (feature development)
- [ ] Multi-Agent Coordination (cross-domain decisions)
```

### Session Log Templates

Add a one-liner at session start:

```markdown
**Active pattern families this session**: [Completion Theater, Investigation]
```

---

## Maintenance Plan

### During Pattern Sweeps (Every 6 Weeks)

1. Review family assignments — any patterns that should move?
2. Review tier classifications — any emerging families that should be established?
3. Update health status based on usage analysis
4. Check unaffiliated patterns for new family candidates

### Between Sweeps

- New patterns automatically start as unaffiliated
- Proto-patterns (PROTO-PATTERNS.md) include provisional family suggestions
- Family assignment happens during next sweep, not ad-hoc

---

## Scalability Considerations

The CIO flagged concern about sweep complexity growing with catalog size. The family index helps by:

1. **Grouping reduces cognitive load**: 8 families are easier to reason about than 61 patterns
2. **Tiered review**: Sweeps can focus on established families (health check) vs. emerging (evidence review) vs. unaffiliated (grouping)
3. **Quick references enable delegation**: Skills and templates carry family knowledge, reducing need for agents to memorize the catalog

### Scaling thresholds

| Catalog Size | Approach |
|-------------|----------|
| <100 patterns | Current: Full sweep every 6 weeks |
| 100-200 patterns | Rotate: Full sweep annually, family-level review every 6 weeks |
| 200+ patterns | Delegate: Each family has an "owner" pattern, sweep by family |

---

## Open Questions for CIO

1. **Should the family index live in the patterns directory or at the architecture level?** Proposed: patterns directory alongside README.md.

2. **Should families have explicit "lead patterns"?** E.g., Pattern-045 as the diagnostic entry point for Completion Theater. This could simplify references but adds maintenance.

3. **How formal should skill/template integration be?** Options range from "add a comment" to "structured checklist." Proposed: structured checklist in gameplans, comment-level in skills.

4. **Should the Architecture & Data patterns (Tier 3) be split into sub-families or kept as one large unaffiliated group?** The health check (Lead Dev assignment, before Feb 17) may inform this.

---

## Recommendation

Create `PATTERN-FAMILIES.md` with the format above. Start with the 8 families identified in Pattern Sweep 2.0. Add family references to 3 high-traffic skills (`close-issue-properly`, `create-session-log`, `audit-cascade`) as a pilot. Evaluate adoption during March 17 sweep.

---

_Proposal submitted: February 5, 2026_
_For CIO review per assignment timeline (2 weeks from Feb 4)_
