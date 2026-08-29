# CORE-GREAT-1B: Orchestration Connection & Integration

## Context
Part 2 of CORE-GREAT-1 epic. After QueryRouter is fixed and enabled (GREAT-1A), we need to properly connect it to the OrchestrationEngine and ensure the full orchestration pipeline works end-to-end.

## Acceptance Criteria

### Connection Phase
- [ ] OrchestrationEngine properly initializes QueryRouter
- [ ] QueryRouter receives queries from OrchestrationEngine
- [ ] Orchestration pipeline flows: Intent → Orchestration → QueryRouter
- [ ] All connection points use proper async/await patterns
- [ ] Session management works correctly

### Integration Phase
- [ ] GitHub issue creation works through chat interface
- [ ] Performance meets target (<500ms for standard operations)
- [ ] Error handling provides meaningful feedback
- [ ] All orchestration services communicate properly
- [ ] Bug #166 (UI hang on multiple prompts) is resolved

### Verification Phase
- [ ] "Create GitHub issue about X" works end-to-end (North Star test)
- [ ] No "None" objects or uninitialized services
- [ ] Logging confirms proper initialization sequence
- [ ] Multiple rapid requests don't cause hangs

## Evidence Required
- Terminal output showing initialization sequence
- Successful GitHub issue creation through chat
- Performance metrics showing <500ms response
- Multiple request test without UI hang
- Log output confirming all services connected

## Dependencies
- CORE-GREAT-1A must be complete (QueryRouter enabled)
- GitHub integration service must be accessible
- Intent classifier must be operational

## STOP Conditions
- If QueryRouter can't be initialized by OrchestrationEngine
- If architectural conflicts prevent connection
- If performance cannot meet targets without major refactor
- If Bug #166 requires separate architectural changes

## Definition of Done
- OrchestrationEngine initializes with QueryRouter
- GitHub issue creation works through chat interface
- Performance validated at <500ms
- Bug #166 resolved (no UI hang)
- All integration tests passing
- Evidence provided for all connections

## Technical Notes
- Check `services/orchestration/engine.py` for initialization
- Verify session factory pattern is used correctly
- Ensure async patterns are consistent
- May need to update `web/app.py` connection points

## Related
- Parent: CORE-GREAT-1 (#180)
- Depends on: CORE-GREAT-1A completion
- Fixes: Bug #166 (UI hang)
