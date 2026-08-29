# Pattern-037: Cross-Context Validation

**Category**: Development & Process Patterns (META-PATTERN)
**Status**: Active
**Created**: 2025-11-04
**Meta-Level**: Pattern about validating patterns across contexts
**Related**: Pattern-036 (Signal Convergence), Pattern-038 (Temporal Clustering)

## Intent

Validate concept emergence and terminology evolution by tracking appearances across multiple independent contexts (ADR, code, omnibus, tests) rather than single-source validation.

## Problem

New concepts/terminology can appear in documentation but never materialize in code, or vice versa:
- **Documentation drift**: ADRs describe patterns not actually implemented
- **Undocumented patterns**: Code patterns exist without architectural documentation
- **False positives**: Concepts mentioned once then abandoned
- **No validation metric**: Can't quantify how "real" a concept is

Manual validation requires checking multiple locations, which is time-consuming and error-prone.

## Solution

Track concept appearances across **independent contexts** and calculate validation score:

### Context Types
```python
KEY_CONTEXTS = {
    "adr",       # Architecture Decision Records
    "omnibus",   # Omnibus synthesis logs
    "code",      # Production code (services/, web/)
    "test",      # Test files
    "doc",       # General documentation
    "session_log" # Session logs
}
```

### Validation Scoring
```python
def calculate_validation_score(contexts: Dict[str, int]) -> float:
    """
    Score based on cross-context appearances.

    Returns:
        0.0-1.0 where higher = more validated
    """
    key_contexts = {"adr", "omnibus", "code"}
    present_contexts = set(contexts.keys()) & key_contexts

    return len(present_contexts) / len(key_contexts)
```

### Validation Tiers

- **100% validated** (3/3): ADR + code + omnibus
  - Concept documented architecturally
  - Implemented in production code
  - Validated in synthesis/review
  - Example: `AsyncSessionFactory`, `EnhancedErrorMiddleware`

- **67% validated** (2/3): Any 2 of {ADR, code, omnibus}
  - Concept partially validated
  - May be in progress
  - Example: Concept in ADR + code but not yet in omnibus

- **33% validated** (1/3): Single context only
  - Concept mentioned but not validated
  - May be abandoned or exploratory
  - Example: Concept in session log only

## Example

**ActionHumanizer Pattern** (Nov 3, 2025):
```python
contexts = {
    "session_log": 3,  # Discussed in 3 session logs
    "omnibus": 1,      # Captured in omnibus log
    "code": 2,         # Implemented in 2 files
}

validation_score = 2/3 = 0.67  # ADR context missing
```

After ADR-042 created:
```python
contexts = {
    "adr": 1,          # ADR-042 documents pattern
    "session_log": 3,
    "omnibus": 1,
    "code": 2,
}

validation_score = 3/3 = 1.00  # Fully validated!
```

## Structure

```
SemanticAnalyzer
├── _build_term_timeline()
│   ├── Scan ADR files (docs/internal/architecture/current/adrs/)
│   ├── Scan omnibus logs (docs/omnibus-logs/)
│   ├── Scan code files (services/, web/)
│   └── Scan session logs (dev/2025/)
│
├── _classify_file_context()
│   └── Determine context type from file path
│
├── _classify_term_contexts()
│   └── Count term appearances by context
│
└── _calculate_validation_scores()
    └── Score = present_contexts / total_key_contexts
```

## Benefits

1. **Objective Validation**: Quantifiable 0.0-1.0 score
2. **Drift Detection**: Finds documentation-code mismatches
3. **Pattern Maturity**: Tracks concept evolution from idea → implementation → documentation
4. **False Positive Reduction**: Single-context concepts filtered out
5. **Prioritization**: High-validation concepts are more important

## Implementation

```python
class SemanticAnalyzer:
    def _classify_term_contexts(
        self, term_timeline: Dict[str, List[Dict]]
    ) -> Dict[str, Dict[str, int]]:
        """Count term appearances by context type"""
        classification = {}

        for term, occurrences in term_timeline.items():
            context_counts = Counter(occ["context"] for occ in occurrences)
            classification[term] = dict(context_counts)

        return classification

    def _calculate_validation_scores(
        self, context_classification: Dict[str, Dict[str, int]]
    ) -> Dict[str, float]:
        """Calculate validation scores (0.0-1.0)"""
        scores = {}
        key_contexts = {"adr", "omnibus", "code"}

        for term, contexts in context_classification.items():
            present_contexts = set(contexts.keys()) & key_contexts
            score = len(present_contexts) / len(key_contexts)
            scores[term] = score

        return scores
```

## Consequences

**Positive:**
- Detects documentation drift automatically
- Validates architectural decisions with implementation evidence
- Identifies abandoned concepts early
- Provides metric for pattern maturity
- Enables "architectural insight" breakthrough signal

**Negative:**
- Requires scanning multiple file types
- Context classification may be ambiguous
- Doesn't detect semantic equivalence (e.g., "session factory" vs "AsyncSessionFactory")
- May miss concepts in unconventional locations

## Validation Evidence

**Nov 3, 2025 Concepts**:
- `ActionHumanizer`: 67% validation (code + omnibus, ADR pending)
- `75% pattern`: 67% validation (session_log + omnibus)
- `EnhancedErrorMiddleware`: 67% validation (code + session_log)

**High-validation concepts** triggered `ARCHITECTURAL_INSIGHT` breakthrough signal.

## Related Patterns

- **Pattern-036**: Signal Convergence - Also uses multi-source validation
- **Pattern-038**: Temporal Clustering - Groups validation events by date
- **Pattern-034**: Error Handling Standards - Validated across ADR + code + tests

## Notes

This pattern emerged from Enhanced Pattern Sweep implementation (2025-11-04). Key insight: **Concepts appearing in multiple independent contexts are more "real"** than single-source concepts.

The pattern enables detecting:
- When architectural decisions (ADRs) are actually implemented
- When code patterns need architectural documentation
- When concepts are abandoned vs evolving

Cross-context validation is a form of **empirical validation** - the concept proves itself by appearing in independent sources, not by declaration.
