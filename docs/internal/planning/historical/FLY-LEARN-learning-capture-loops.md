# FLY-LEARN: Formalize learning capture loops from session logs

**Labels**: enhancement, fly-methodology, patterns

## Description

Currently we capture patterns informally in pattern-catalog.md. We need a systematic process to extract learnings from our work and prevent repeating mistakes.

## Current State

- Patterns discovered ad-hoc during sessions
- Manual updates to pattern-catalog.md
- No systematic review process
- Learning often lost in session logs

## Desired State

- Automated pattern extraction from session logs
- Weekly pattern review during audits
- Categorized pattern library
- Integration with methodology docs

## Success Criteria

- [ ] Pattern extraction script/process defined
- [ ] Categories established (verification, coordination, error-handling, etc.)
- [ ] Weekly review integrated into FLY-AUDIT process
- [ ] Pattern-catalog.md auto-updated with discoveries
- [ ] Anti-patterns documented (what NOT to do)

## Examples to Capture

- Mock data fallbacks causing validation theater
- Infrastructure verification preventing wrong gameplans
- Multi-agent coordination patterns
- Evidence requirements preventing false claims

**Estimated**: 4 hours
**Priority**: Medium (supports continuous improvement)

## Implementation Notes

### Pattern Categories

- **Verification Patterns**: How to validate work properly
- **Coordination Patterns**: Multi-agent collaboration
- **Error Handling**: Graceful degradation vs honest failure
- **Anti-Patterns**: What NOT to do (validation theater, etc.)

### Integration Points

- Weekly FLY-AUDIT process
- Session log analysis
- Pattern-catalog.md maintenance
- Methodology documentation updates

### Technical Approach

1. Create pattern extraction script for session logs
2. Define pattern taxonomy and templates
3. Integrate with existing audit workflow
4. Build pattern library with search/filter capabilities
