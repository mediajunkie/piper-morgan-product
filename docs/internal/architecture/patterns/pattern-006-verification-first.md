# Pattern-006: Verification-First Pattern

## Status

**Absorbed** — absorbed into `methodology-07-VERIFICATION-FIRST.md`, ruled canonical 2026-09-01 by
Arch's B3 synthesis motion (`docs/internal/architecture/reviews/2026-08-architectural-review/`):
verification-first is a practice, and practices live in methodology-core; CLAUDE.md's "Evidence
Required" section is its enforcement surface. This was the first cross-corpus absorb identified
during the review — Docs and CIO independently found the same principle living in both the
patterns and methodology-core corpora and flagged it upward rather than resolving it unilaterally.
`methodology-30-CONSUMER-TRACE-VERIFICATION.md` stays independent of this absorption — it
specializes m-07 (consumer-trace is a specific technique), a healthy relationship, not redundancy.
Pattern content preserved below for historical reference.

## Context

AI-assisted development introduces unique risks where generated solutions may appear correct but contain subtle errors, security vulnerabilities, or logical flaws. Traditional development assumes human-generated code has been reasoned through, but AI-generated solutions require systematic verification. The Verification-First Pattern addresses:

- Preventing execution of unverified AI-generated solutions
- Establishing systematic validation gates for critical operations
- Reducing production errors from AI-generated code
- Building trust in AI-assisted development workflows
- Creating accountability in multi-agent development scenarios

## Pattern Description

The Verification-First Pattern ensures reliability by implementing systematic verification gates before executing AI-generated solutions. The pattern establishes a four-step process:

**Core Principle**: "Never assume AI-generated solutions are correct. Implement systematic verification."

**Pattern Structure**:

1. **Generate Solution** (AI/LLM)
2. **Verify Solution** (Human/System)
3. **Execute Solution** (Only if verified)
4. **Validate Results** (Post-execution)

## Implementation

### Structure

```python
class VerificationGate:
    """Systematic verification for AI-generated solutions."""

    def __init__(self, verification_criteria: Dict[str, Any]):
        self.criteria = verification_criteria
        self.verification_log = []

    def verify_solution(self, solution: Any) -> VerificationResult:
        """Apply verification criteria to solution."""
        # Implementation details
        pass

    def execute_if_verified(self, solution: Any, executor: Callable) -> Result:
        """Execute only verified solutions."""
        verification = self.verify_solution(solution)
        if verification.passed:
            return executor(solution)
        else:
            raise VerificationFailedError(verification.failures)
```

### Code Example

```python
# GitHub Issue Creation with Verification-First
class GitHubIssueCreator:
    def __init__(self):
        self.verification_gate = VerificationGate({
            "required_fields": ["title", "description", "repository"],
            "format_validation": ["title_length", "markdown_syntax"],
            "security_checks": ["repository_access", "token_validity"],
            "business_rules": ["project_context", "priority_mapping"]
        })

    def create_issue_with_verification(self, ai_generated_issue: Dict) -> Issue:
        """Create GitHub issue with verification-first approach."""

        # Step 1: AI has already generated the issue

        # Step 2: Verify the solution
        verification = self.verification_gate.verify_solution(ai_generated_issue)

        if not verification.passed:
            logger.error(f"Issue creation failed verification: {verification.failures}")
            raise VerificationFailedError(verification.failures)

        # Step 3: Execute only if verified
        issue = self.github_client.create_issue(ai_generated_issue)

        # Step 4: Validate results
        if not self.validate_created_issue(issue):
            logger.error("Post-execution validation failed")
            # Implement rollback if necessary

        return issue
```

### Configuration

```yaml
# Verification-First Configuration
verification_gates:
  enabled: true
  strict_mode: true
  verification_levels:
    - basic: ["syntax", "required_fields"]
    - enhanced: ["security", "business_rules"]
    - comprehensive: ["integration", "performance"]

logging:
  verification_failures: true
  execution_tracking: true
  post_validation: true
```

## Usage Guidelines

### When to Use

- **AI-Generated Code**: All code, configurations, or solutions from LLMs
- **Critical Operations**: Database changes, API integrations, security configurations
- **User-Facing Features**: UI changes, workflow modifications, data transformations
- **Multi-Agent Coordination**: When multiple AI agents collaborate on solutions
- **Production Deployments**: Any change affecting production systems

### When NOT to Use

- **Simple, Low-Risk Operations**: Basic logging, trivial utility functions
- **Development/Testing Environments**: Where failure has minimal impact
- **Well-Tested Patterns**: Established patterns with extensive test coverage
- **Human-Generated Solutions**: Code written and reasoned through by humans

### Best Practices

- **Define Criteria Upfront**: Establish verification criteria before solution generation
- **Automate Where Possible**: Use automated checks for syntax, security, format validation
- **Log All Verifications**: Maintain audit trail of verification decisions
- **Implement Rollback**: Have rollback mechanisms for post-execution validation failures
- **Gradual Verification**: Start with basic checks, add comprehensive validation over time

## Examples in Codebase

### Primary Usage

- `services/github/issue_creator.py` - GitHub issue creation with verification gates
- `services/orchestration/workflow_validator.py` - Workflow execution verification
- `cli/commands/deploy.py` - Deployment verification before execution

### Test Examples

- `tests/patterns/test_verification_first.py` - Pattern implementation tests
- `tests/integration/test_verified_workflows.py` - End-to-end verification testing

## Related Patterns

### Complements

- [Pattern-009: GitHub Issue Tracking](pattern-009-github-issue-tracking.md) - Uses verification for issue operations
- [Pattern-010: Cross-Validation Protocol](pattern-010-cross-validation-protocol.md) - Multi-agent verification approach

### Alternatives

- **Trust-First Pattern**: Assumes AI solutions are correct (not recommended for production)
- **Post-Execution Validation**: Validates after execution (higher risk, faster execution)

### Dependencies

- **Logging Infrastructure**: Required for verification audit trails
- **Error Handling Framework**: Needed for verification failure management

## Migration Notes

_Consolidated from multiple sources_

### From decision-patterns/emergent/verification-first-pattern.md

- **Pattern Strength**: 15/16 (Critical Strength) - indicates high reliability
- **Core Implementation**: Four-step verification process (Generate → Verify → Execute → Validate)
- **Discovery Context**: Emerged from AI-assisted development challenges in July 2025
- **Production Status**: Proven effective in production environments

### From methodology documentation

- **Excellence Flywheel Integration**: Verification-first as core component of systematic development
- **Multi-Agent Coordination**: Essential for coordinating multiple AI agents safely

## References

### Documentation

- **Original source**: `docs/internal/archive/piper-education-2025/decision-patterns/emergent/verification-first-pattern.md` (archived Feb 2026)
- **Related patterns**: Human-AI Collaboration Referee, Session Log Pattern
- **Methodology integration**: Excellence Flywheel methodology

### Usage Analysis

- **Current usage**: Core pattern across GitHub operations, workflow management, deployment processes
- **Pattern strength**: 15/16 critical strength rating
- **Status**: Production ready, actively maintained
- **Last updated**: September 15, 2025

---

_Pattern extracted and consolidated: September 15, 2025_
_Agent B (Cursor) - Pattern Catalog Consolidation Project_
