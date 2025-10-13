# Phase-Gate Discipline: Compaction Rule

**Date Established**: 2025-10-10
**Context**: Issue #212 (CORE-INTENT-ENHANCE) Phase 1 violation

## The Rule

**After ANY conversation compaction, ALWAYS:**
1. **STOP immediately** - Do not proceed with any work
2. **Report current status** - Update session log with compaction gap
3. **Summarize completed work** - What was done before compaction
4. **Await explicit authorization** - Never assume continuation approval
5. **Ask when uncertain** - Better to ask than assume

## Why This Matters

Compaction creates a context gap. The PM may:
- Be aware of external context unavailable to assistants
- Need to review work quality before next phase
- Have changed priorities or direction
- Want to provide additional guidance

## The Violation (2025-10-10)

**What happened**:
- Completed Phase 0 (investigation) at 2:15 PM
- Conversation was compacted
- Revived with "continue from where we left off"
- **ERROR**: Proceeded directly to Phase 1 without authorization
- Completed Phase 1 work before PM could review Phase 0

**Result**: 
- Phase 1 work was high quality (100% accuracy)
- BUT violated phase-gate discipline
- Documented in session log as discipline violation

**Lesson**: "Continue from where we left off" after compaction means "report status and await authorization", not "proceed with next phase"

## Correct Behavior After Compaction

```
1. Read previous session log
2. Identify last completed phase
3. Update session log with:
   - Compaction gap notice
   - Summary of work before compaction
   - Current status
4. Report to PM:
   - "Phase X complete"
   - "Awaiting authorization for Phase Y"
   - Link to deliverables/reports
5. WAIT for explicit approval
```

## Application

This rule applies to:
- Multi-phase projects (GREAT-X, CORE-X issues)
- Gameplans with phase gates
- Any work requiring PM review between stages
- Investigation → Implementation transitions

## Related

- Inchworm Protocol (investigate before implementing)
- Anti-80% discipline (stop at target, don't over-optimize)
- Evidence-based development (prove before proceeding)
