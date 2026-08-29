# Pattern-000: Template for Pattern Documentation

## Status

**Template** | Proven | Emerging | Experimental | Deprecated

## Product Relevance

**Process-only** | Portable | Converged

- **Process-only**: Useful for building Piper, not applicable to Piper's users
- **Portable**: Methodology that could become user-facing capability
- **Converged**: Pattern already implemented as product feature

## Context

Brief description of the problem or situation that this pattern addresses. Include:

- What challenges does this solve?
- When should this pattern be considered?
- What are the typical scenarios where this applies?

## Pattern Description

Clear, concise description of the pattern itself:

- Core concept and approach
- Key components or elements
- How it works conceptually

## Implementation

### Structure

```
# Language-specific implementation structure
# Show key classes, interfaces, or components
```

### Code Example

```python
# Concrete implementation example
# Focus on the essential elements that demonstrate the pattern
class PatternExample:
    """Example implementation of this pattern."""

    def __init__(self):
        # Initialization logic
        pass

    def core_method(self):
        """Core pattern functionality."""
        # Implementation details
        pass
```

### Configuration

```yaml
# Configuration examples if applicable
pattern_config:
  enabled: true
  parameters:
    - setting: value
```

## Usage Guidelines

### When to Use

- Specific scenarios where this pattern is recommended
- Conditions that make this pattern appropriate
- Benefits gained from using this pattern

### When NOT to Use

- Situations where this pattern should be avoided
- Potential drawbacks or limitations
- Alternative approaches to consider

### Best Practices

- Implementation recommendations
- Common pitfalls to avoid
- Performance considerations

## Examples in Codebase

### Primary Usage

- `path/to/primary/example.py` - Main implementation
- `path/to/another/example.py` - Alternative usage

### Test Examples

- `tests/path/to/test_example.py` - How this pattern is tested

## Related Patterns

### Complements

- [Pattern-XXX: Related Pattern](pattern-xxx-related.md) - How they work together

### Alternatives

- [Pattern-YYY: Alternative Pattern](pattern-yyy-alternative.md) - When to choose one over the other

### Dependencies

- [Pattern-ZZZ: Required Pattern](pattern-zzz-required.md) - Patterns this one depends on

## Migration Notes

_If consolidating from existing documentation_

### From pattern-catalog.md

- Section reference: `pattern-catalog.md#original-section`
- Key information preserved: [list what was migrated]

### From PATTERN-INDEX.md

- Section reference: `PATTERN-INDEX.md#original-section`
- Key information preserved: [list what was migrated]

## References

### Documentation

- Original source: [Link to original documentation]
- Related ADRs: [Link to relevant architectural decisions]
- External references: [Links to external resources]

### Usage Analysis

- Current usage count: X files
- Last updated: [Date]
- Maintenance status: Active | Stable | Legacy

---

## Template Usage Instructions

### For Consolidation (Agents A & B)

1. **Status**: Set to "Proven" for established patterns, "Emerging" for new ones
2. **Context**: Merge context from both pattern-catalog.md and PATTERN-INDEX.md
3. **Implementation**: Prioritize working code examples from codebase
4. **Migration Notes**: Document what was consolidated from each source
5. **References**: Include links back to original sources

### For New Patterns

1. **Status**: Start with "Experimental" or "Emerging"
2. **Context**: Clearly define the problem space
3. **Implementation**: Provide working, tested examples
4. **Usage Guidelines**: Be explicit about when to use/avoid
5. **References**: Link to supporting documentation and decisions

### Quality Checklist

- [ ] Status is appropriate for pattern maturity
- [ ] Product Relevance is classified (Process-only, Portable, or Converged)
- [ ] Context clearly explains when/why to use
- [ ] Implementation includes working code examples
- [ ] Usage guidelines are explicit and actionable
- [ ] Related patterns are properly linked
- [ ] Migration notes document consolidation sources
- [ ] References are complete and accurate

---

_Template created: September 15, 2025_
_For use in Pattern Catalog Consolidation project_
_Agent coordination: Template by Agent B (Cursor), Implementation by Agent A (Code)_
