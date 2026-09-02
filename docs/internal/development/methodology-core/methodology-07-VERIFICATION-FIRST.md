# Verification-First Methodology

> **Cross-corpus note (2026-09-01)**: ruled canonical for this principle by Arch's B3 synthesis
> motion — `pattern-006-verification-first.md` described the same practice independently in the
> patterns catalog and has been absorbed into this file (content preserved there for historical
> reference). `methodology-30-CONSUMER-TRACE-VERIFICATION.md` stays independent — it specializes
> this methodology for consumer-relationship claims specifically, a healthy relationship, not
> redundancy.

## Overview

The **Verification-First Methodology** is a systematic approach to development that prioritizes understanding existing systems before implementing changes. This methodology prevents integration issues and ensures robust, production-ready implementations.

## Core Principles

### 1. VERIFY FIRST (Mandatory)

**❌ NEVER assume** method names, response structures, or API patterns exist
**✅ ALWAYS verify** existing implementations FIRST using verification commands
**✅ CHECK before implementing, implement after verifying**
**✅ When uncertain, verify rather than guess**

### 2. Excellence Flywheel Guardrails

- **Systematic Discovery**: Use verification commands to understand existing patterns
- **Integration Awareness**: Always test at the integration level, not just unit level
- **Backward Compatibility**: Maintain existing response structures and patterns
- **User Experience**: Ensure graceful degradation provides helpful, actionable messages

## Verification Commands

### API Response Structure Verification

```bash
# Find response models and validation patterns
grep -r "response.*model\|Response.*Model" services/ --include="*.py"

# Check existing error handling in API layer
grep -r "try.*except" services/api/routes/ --include="*.py"

# Find validation error patterns
find . -name "*.py" -exec grep -l "ValidationError\|ResponseValidationError" {} \;
```

### Integration Point Verification

```bash
# Check current API response structure expectations
grep -r "QueryRouter" services/api/ --include="*.py" -A5 -B5

# Find response models and validation patterns
find services/api/ -name "*.py" -exec grep -l "response.*model\|Response.*Model" {} \;

# Check existing error handling in API layer
grep -r "try.*except" services/api/routes/ --include="*.py"
```

### System Architecture Verification

```bash
# Check current location and confirm project structure
find services/ -name "*query*router*" -type f

# Map dependencies and usage patterns
grep -rn "QueryRouter" services/ --include="*.py"

# Analyze existing graceful degradation patterns
grep -rn "test_mode" services/ --include="*.py"
```

## Methodology Application Example

### Session: August 1, 2025 - QueryRouter Degradation Implementation

**Problem**: Unit tests passed (11/11) but integration tests failed (5/7) with 500 errors

**Verification-First Approach Applied**:

1. **✅ VERIFY API Response Structure**:

   ```bash
   grep -r "response.*model\|Response.*Model" services/ --include="*.py"
   ```

   - Found: `IntentResponse` model expects structured responses
   - Found: `@app.post("/api/v1/intent", response_model=IntentResponse)`

2. **✅ VERIFY Integration Points**:

   ```bash
   grep -r "QueryRouter" services/api/ --include="*.py" -A5 -B5
   ```

   - Found: QueryRouter called in `main.py` lines 310-330
   - Found: Missing return statement in normal flow

3. **✅ VERIFY Error Patterns**:
   ```bash
   find . -name "*.py" -exec grep -l "ValidationError\|ResponseValidationError" {} \;
   ```
   - Found: FastAPI validation errors in integration tests

**Critical Discovery**: Normal flow calls `query_router.route_query()` but doesn't return anything, causing `None` to be returned to FastAPI, triggering `ResponseValidationError`.

## Success Criteria

### Verification Success

- ✅ **API Response Structure Identified**: `IntentResponse` model requirements
- ✅ **Integration Points Mapped**: QueryRouter integration in main.py
- ✅ **Error Patterns Understood**: FastAPI validation error root cause
- ✅ **Backward Compatibility Maintained**: Existing response patterns preserved

### Implementation Success

- ✅ **Unit Tests**: All 11 degradation tests passing
- ✅ **Integration Tests**: API properly handles degradation responses
- ✅ **User Experience**: Graceful degradation with helpful messages
- ✅ **System Resilience**: Circuit breaker patterns working correctly

## Best Practices

### 1. Always Start with Verification

```bash
# BEFORE implementing any feature, run verification commands
grep -r "response.*model\|Response.*Model" services/ --include="*.py"
find . -name "*.py" -exec grep -l "ValidationError\|ResponseValidationError" {} \;
```

### 2. Test at Integration Level

- Unit tests verify method-level functionality
- Integration tests verify API-level behavior
- Always run both before considering implementation complete

### 3. Maintain Response Structure Consistency

- API expects structured responses (not strings)
- Degradation responses must fit existing response models
- User-friendly messages within structured format

### 4. Document Verification Commands

- Record all verification commands used
- Document discoveries and patterns found
- Share verification-first approach with team

## Common Pitfalls Avoided

### ❌ Assumption-Based Development

- **Pitfall**: Assuming API response structure without verification
- **Solution**: Always verify existing patterns first

### ❌ Unit-Only Testing

- **Pitfall**: Passing unit tests but failing integration
- **Solution**: Test at both unit and integration levels

### ❌ Breaking Response Structure

- **Pitfall**: Returning strings when API expects structured objects
- **Solution**: Maintain existing response model compatibility

### ❌ Ignoring Error Patterns

- **Pitfall**: Not understanding validation error root causes
- **Solution**: Use verification commands to understand error patterns

## Methodology Checklist

### Before Implementation

- [ ] Run verification commands to understand existing patterns
- [ ] Map integration points and dependencies
- [ ] Identify response structure requirements
- [ ] Document existing error handling patterns

### During Implementation

- [ ] Maintain backward compatibility
- [ ] Test at both unit and integration levels
- [ ] Verify response structure consistency
- [ ] Ensure graceful degradation patterns

### After Implementation

- [ ] Run comprehensive integration tests
- [ ] Verify user experience quality
- [ ] Document verification-first approach used
- [ ] Share methodology with team

## Conclusion

The Verification-First Methodology ensures robust, production-ready implementations by systematically understanding existing systems before making changes. This approach prevents integration issues and maintains system reliability while enabling graceful degradation and excellent user experience.

**Key Takeaway**: Always verify before implementing, test at integration level, and maintain existing response structure compatibility.

## Relationship to Anthropic Outcomes (May 2026 productization)

Methodology-07 covers **code-verification-before-implementation** — the discipline of reading existing code before writing new code. Anthropic's Outcomes API (shipped 2026-05-06) covers **artifact-output-verification** — rubric + grader + retry against a produced artifact. The two disciplines are complementary, not competing:

- **methodology-07 (this entry)**: verify the codebase you're extending. Grep for patterns, read existing implementations, check integration points. Verification happens **before** you write code.
- **Outcomes API**: verify the artifact you've produced. Define a rubric, let an auto-provisioned grader score the output, iterate up to N times on `needs_revision`. Verification happens **after** you write code (or after the agent writes an artifact).

Both compose in any disciplined workflow. methodology-07 prevents code-archaeology drift (e.g., adding endpoints that don't match existing response patterns); Outcomes prevents output-quality drift (e.g., shipping artifacts that don't satisfy success criteria). Neither replaces the other.

See `methodology-15 (Testing & Validation)` and `methodology-17 (Cross-Validation Protocol)` for the verification disciplines that compose with Outcomes more directly. methodology-07 stays in the code-archaeology lane.

CIO Outcomes platform-productization disposition memo (2026-05-18) covers the broader climb-up framing.
