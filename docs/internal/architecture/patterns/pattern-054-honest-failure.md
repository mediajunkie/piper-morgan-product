# Pattern-054: Honest Failure with Suggestion

**Status**: Proven
**Category**: Grammar Application
**First Documented**: January 20, 2026
**Ratified**: January 20, 2026 (Grammar Implementation)

---

## Problem Statement

Integrations and external services fail unpredictably, but users need to understand what happened and what they can do about it. Common anti-patterns:

- Silent failures (pretend everything worked)
- Generic error messages ("Something went wrong")
- Technical jargon ("HTTP 401 Unauthorized")
- No actionable guidance for recovery
- Blame-shifting ("GitHub is down")

This erodes user trust and creates support burden when users don't know how to resolve issues.

---

## Solution

Implement **Honest Failure with Suggestion** where failures are:

1. **Acknowledged explicitly** - "I couldn't reach GitHub" (not hidden)
2. **Explained clearly** - Use plain language, not technical codes
3. **Contextualized** - Why this matters to user's current task
4. **Actionable** - Provide specific recovery suggestion
5. **Warm** - Maintain Piper's supportive tone even in failure

---

## Pattern Description

**Honest Failure with Suggestion** is an error communication pattern that preserves user trust through transparency and helpfulness. The pattern emphasizes:

- **Entity integrity**: Piper admits limitations honestly (self-awareness)
- **Moment acknowledgment**: Failure is a Moment that matters
- **Place specificity**: Identify which integration failed (GitHub vs Calendar)
- **Recovery guidance**: Suggest concrete next steps
- **Warmth preservation**: Supportive tone, not cold error reporting

### Key Characteristics

1. **Three-part structure**:
   - **What failed**: "I couldn't reach [integration]"
   - **Why it matters**: "This means I can't show [capability]"
   - **What to do**: "Suggestion: [actionable step]"

2. **Failure diagnosis**:
   - Pattern match on error type
   - Map to user-facing explanation
   - Generate contextual suggestion

3. **Graceful degradation annotation**:
   - When partial failure, annotate what's missing
   - Show best available data
   - Acknowledge limitation inline

4. **Custom exception types**:
   - Feature-specific exceptions (e.g., `StandupIntegrationError`)
   - Carry suggestion field
   - Enable structured error handling

---

## Implementation

### Structure

```python
class [Feature]IntegrationError(Exception):
    """
    Raised when [feature] integrations fail.

    Carries diagnostic information for user-facing error messages.
    """

    def __init__(self, message: str, service: str = None, suggestion: str = None):
        """
        Initialize integration error.

        Args:
            message: User-facing error description
            service: Which integration failed (e.g., "github", "calendar")
            suggestion: Actionable recovery suggestion
        """
        self.service = service
        self.suggestion = suggestion
        super().__init__(message)


class FeatureService:
    async def execute_with_integration(self, user_id: str):
        """Execute feature with honest failure handling."""

        try:
            result = await self._call_integration()
            return result

        except IntegrationError as e:
            # Diagnose failure and generate suggestion
            error_msg = self._explain_failure(e)
            suggestion = self._diagnose_failure(e)

            # Raise with both explanation and suggestion
            raise [Feature]IntegrationError(
                f"{error_msg}\nSuggestion: {suggestion}",
                service=self._identify_service(e),
                suggestion=suggestion
            )

    def _diagnose_failure(self, error: Exception) -> str:
        """
        Diagnose integration failure and suggest recovery.

        Args:
            error: Original exception

        Returns:
            User-facing suggestion for recovery
        """
        error_str = str(error).lower()

        if "401" in error_str or "unauthorized" in error_str:
            return "Check API token in PIPER.user.md configuration"
        elif "403" in error_str or "forbidden" in error_str:
            return "Verify API permissions for this resource"
        elif "404" in error_str or "not found" in error_str:
            return "Confirm resource exists and is accessible"
        elif "timeout" in error_str or "timed out" in error_str:
            return "Check network connectivity and try again"
        elif "rate limit" in error_str:
            return "Wait a few minutes and try again (rate limit exceeded)"
        else:
            return "Check service logs for integration details"

    def _explain_failure(self, error: Exception) -> str:
        """
        Convert technical error to user-facing explanation.

        Args:
            error: Original exception

        Returns:
            Plain language explanation
        """
        error_str = str(error).lower()

        if "401" in error_str or "unauthorized" in error_str:
            return "I couldn't authenticate with the integration"
        elif "403" in error_str:
            return "I don't have permission to access that resource"
        elif "404" in error_str:
            return "I couldn't find the requested resource"
        elif "timeout" in error_str:
            return "The integration took too long to respond"
        else:
            return f"I encountered an issue: {str(error)}"
```

### Example from Morning Standup

**File**: `services/features/morning_standup.py:25-31`

```python
class StandupIntegrationError(Exception):
    """Raised when standup integrations fail and cannot provide real data"""

    def __init__(self, message: str, service: str = None, suggestion: str = None):
        self.service = service
        self.suggestion = suggestion
        super().__init__(message)
```

**File**: `services/features/morning_standup.py:140-152`

```python
except Exception as e:
    # No fallbacks - fail honestly
    error_msg = f"Morning standup generation failed: {str(e)}"

    # Diagnose failure and provide suggestion
    if "github" in str(e).lower():
        suggestion = "Check GitHub token in PIPER.user.md configuration"
    elif "session" in str(e).lower():
        suggestion = "Verify session persistence service is running"
    else:
        suggestion = "Check service logs for integration details"

    raise StandupIntegrationError(
        f"{error_msg}\nSuggestion: {suggestion}",
        service="standup",
        suggestion=suggestion
    )
```

**File**: `services/features/morning_standup.py:188-201`

```python
async def _get_github_activity(self) -> Dict[str, Any]:
    """Get GitHub activity from last 24 hours"""
    try:
        recent_issues = await self.github_domain_service.get_recent_issues(limit=5)
        return {"commits": [], "issues": recent_issues}
    except StandupIntegrationError:
        raise  # Re-raise our own errors
    except Exception as e:
        raise StandupIntegrationError(
            f"GitHub integration failed: {str(e)}",
            service="github",
            suggestion="Check GitHub token and network connectivity",
        )
```

**Evidence of honest failure**:

Instead of:
```
Error: HTTP 401
```

User sees:
```
Morning standup generation failed: GitHub integration failed: Authentication failed

Suggestion: Check GitHub token in PIPER.user.md configuration
```

### Graceful Degradation Pattern

**File**: `services/features/morning_standup.py:351-353`

```python
except Exception as e:
    # Graceful degradation - add error note but continue
    base_standup.today_priorities.append(f"⚠️ Document memory unavailable: {str(e)[:50]}...")
```

**Evidence of graceful degradation**:

When document service fails, standup continues with annotation:

```
Today's focus:
• Continue work on piper-morgan
• Complete authentication refactoring
• ⚠️ Document memory unavailable: Connection timeout

No critical blockers - ready to execute!
```

User sees:
- What worked (base standup)
- What didn't work (document memory)
- Why (connection timeout)
- Can still use feature (degraded, not broken)

---

## Consequences

### Benefits

- **User trust**: Honesty builds credibility vs hiding failures
- **Reduced support burden**: Users can self-diagnose with suggestions
- **Clear attribution**: User knows which integration failed
- **Actionable guidance**: Specific recovery steps, not generic advice
- **Graceful degradation**: Feature remains useful with partial data
- **Entity integrity**: Piper's self-awareness strengthened (knows limitations)

### Trade-offs

- **Verbosity**: More code than generic error handling
- **Maintenance**: Error diagnosis logic needs updating
- **Exposure**: Users see system internals (must be carefully worded)
- **Testing complexity**: Need to test each failure mode

---

## Related Patterns

### Complements

- **[Pattern-051: Parallel Place Gathering](pattern-051-parallel-place-gathering.md)** - Per-place error handling enables graceful degradation
- **[Pattern-052: Personality Bridge](pattern-052-personality-bridge.md)** - Bridge presents failures warmly
- **[Pattern-053: Warmth Calibration](pattern-053-warmth-calibration.md)** - Maintain warmth even in failure

### Alternatives

- **Silent failure** - Hides problems but erodes trust
- **Generic errors** - Simpler but not actionable
- **Retry logic** - Complement, not alternative (retry then fail honestly)

### Dependencies

- **Structured logging** - For debugging failures
- **Custom exceptions** - For carrying suggestion metadata

---

## Usage Guidelines

### When to Use

✅ **Use Honest Failure with Suggestion when:**

- Integration can fail unpredictably
- User needs to understand what happened
- Recovery action exists (check token, verify config)
- Failure blocks feature functionality
- Want to build user trust through transparency

### When NOT to Use

❌ **Don't use when:**

- **Expected failures**: Validation errors (use validation pattern)
- **Internal errors**: Programming bugs (use crash reporting)
- **User errors**: Wrong input (use friendly validation)
- **Silent degradation**: Better to work with defaults than fail

### Best Practices

1. **Three-part structure**: What + Why + Suggestion
2. **Plain language**: Avoid technical jargon in user-facing message
3. **Specific suggestions**: "Check GitHub token" not "Fix configuration"
4. **Blame-free**: "I couldn't reach" not "GitHub failed"
5. **Maintain warmth**: Use Piper's supportive tone
6. **Diagnose intelligently**: Pattern match on error types
7. **Test each failure mode**: Auth, network, rate limit, not found
8. **Log technical details**: User sees friendly message, logs have full trace
9. **Graceful degradation**: Prefer partial success to total failure
10. **Document recovery**: Link to configuration docs in suggestion

---

## Examples in Codebase

### Primary Usage

- `services/features/morning_standup.py` - StandupIntegrationError with diagnosis (reference)

### Applicable To (from audit)

**High Priority** (all integrations):
- Intent Classification - Honest about low confidence or ambiguity
- Todo Management - Clear about missing list/project context
- Slack Integration - Explain when Slack API unreachable
- GitHub Integration - Diagnose auth, permissions, network issues
- Calendar Integration - Clear about missing calendar access

**Medium Priority**:
- Feedback System - Acknowledge if feedback can't be persisted
- Conversation Handler - Clear about missing conversation context
- Onboarding - Honest about setup step failures

---

## Implementation Checklist

- [ ] Create `[Feature]IntegrationError` exception class
- [ ] Add `service` and `suggestion` fields to exception
- [ ] Implement `_diagnose_failure()` with error pattern matching
- [ ] Implement `_explain_failure()` for user-facing messages
- [ ] Wrap integration calls in try/except
- [ ] Generate specific suggestions for each failure mode
- [ ] Test auth failure (401/403) - expect token suggestion
- [ ] Test network failure (timeout) - expect connectivity suggestion
- [ ] Test not found (404) - expect resource verification suggestion
- [ ] Test rate limit - expect wait suggestion
- [ ] Log technical details for debugging
- [ ] Verify user-facing message is plain language
- [ ] Consider graceful degradation (continue with partial data)

---

## Evidence

**Proven Pattern** - Successfully implemented in:

1. **Morning Standup Honest Failure** (reference implementation)
   - Location: `services/features/morning_standup.py`
   - Status: Production, tested failure modes
   - Exception: `StandupIntegrationError` with suggestion field
   - Diagnosis: Pattern matching on error strings
   - Result: Users self-resolve GitHub token issues

**P0 Analysis Evidence**:
- Pattern identified as "Pattern E: Honest Failure with Suggestion"
- Demonstrates Entity self-awareness (Piper knows limitations)
- Builds user trust through transparency

**Grammar Audit Evidence**:
- Graceful degradation observed in trifecta methods
- Failures annotated inline (⚠️ prefix)
- User sees best available data, not binary success/failure

**User Impact**:
- Support tickets reduced (users fix token issues themselves)
- Trust increased (transparency valued over pretense)
- Feature feels more reliable (honest about limitations)

---

_Pattern Identified: January 19, 2026 (P0 Morning Standup Analysis)_
_Ratified: January 20, 2026_
_Category: Grammar Application_
