# Always Use Serena First - Critical Workflow Rule

## Problem Observed (2025-11-13)

Agent wasted significant tokens and nearly created a rogue parallel system by:
1. Misreading bash `ls` output (confused `web/api/` with `web/api/routes/`)
2. Making increasingly nonsensical explanations instead of verifying facts
3. Not checking what already exists before starting to build

## Solution: Serena-First Workflow

### ALWAYS Use Serena For:

1. **File/Directory Structure**:
   ```python
   mcp__serena__list_dir("path", recursive=true)
   ```
   - More reliable than `ls`
   - Token-efficient
   - Unambiguous output

2. **Finding Existing Code**:
   ```python
   mcp__serena__find_symbol("ClassName", depth=1)
   ```
   - Before creating new classes/functions
   - Check if functionality already exists

3. **Understanding System Structure**:
   ```python
   mcp__serena__get_symbols_overview("file/path.py")
   ```
   - Before modifying files
   - Understand what's already there

### Investigation Protocol (Before Building Anything)

**Phase -1 (MANDATORY)**: Verify existing system
1. Use Serena to map current structure
2. Find existing related functionality
3. Check domain models (services/domain/models.py)
4. Review relevant patterns (docs/internal/architecture/patterns/)
5. Check ADRs for architectural decisions

**Phase 0**: Design integration
1. Identify extension points
2. Follow DDD principles
3. Ensure consistency with existing patterns

**Phase 1**: Implement with evidence
1. Extend, don't replace
2. Maintain architectural consistency
3. Provide evidence for all claims

## Token Efficiency

- Serena queries: ~1K tokens
- Bash confusion + corrections: ~5K tokens
- Building parallel system then refactoring: ~20K tokens

**Savings**: 4-20x by using Serena first!

## DDD Principle Adherence

From CLAUDE.md and methodology:
- "Verify everything, assume nothing"
- "Complete existing work before creating new"
- "The 75% pattern is everywhere - find it, report it, complete it"

Using Serena enforces these principles by making it easy to:
- Find existing code
- Understand current state
- Avoid duplication

## When NOT to Use Serena

- Running actual commands (git, pytest, alembic)
- Making HTTP requests
- Checking process status
- Database queries (use appropriate tool)

## Example: Correct Workflow

**BAD** (what I did):
```bash
ls -la web/api/routes/  # Misread output
# Start building without checking
```

**GOOD** (what I should have done):
```python
mcp__serena__list_dir("web/api", recursive=true)
# See: web/api/routes/learning.py exists
mcp__serena__get_symbols_overview("web/api/routes/learning.py")
# Check what endpoints already exist
# THEN decide what needs to be added
```

## Escalation Path

If unclear about:
- Architectural patterns → Read ADRs
- Domain models → Read services/domain/models.py
- Methodology → Read BRIEFING-METHODOLOGY
- Still unclear → Ask PM for architectural guidance

## Remember

"Part of a cathedral, not just a random brick shed"

Always check what's already built before adding new bricks!
