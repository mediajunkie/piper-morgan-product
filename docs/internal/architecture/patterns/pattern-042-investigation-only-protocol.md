# Pattern-042: Investigation-Only Protocol

## Status

**Proven** (Evidence from Nov 18, 2025 E2E Bug Testing session)

---

## Context

End-to-end testing often reveals multiple bugs that demand immediate fixes. Traditional approaches allow agents to implement fixes during investigation, leading to:

- **Symptom fixing**: Fixes the surface issue without understanding root cause
- **Repeated fixes**: Same underlying issue fixed multiple times in different ways
- **Rework accumulation**: Partial fixes create technical debt requiring refactoring
- **Missed patterns**: Individual bug fixes prevent pattern recognition across issues
- **Process violations**: Bypasses DDD/TDD/Verification-First methodology due to time pressure

The Investigation-Only Protocol ensures rigorous understanding before implementation by strictly separating investigation from fixing into distinct phases with different teams/agents.

**Real-world Example**: Nov 18, 2025 - E2E Bug Protocol Creation
- When PM requested systematic approach to E2E bugs, decision made to prevent agents from fixing during investigation
- Created 3-phase protocol: Capture → Investigate (NO FIXES) → Fix (based on patterns)
- Result: Discovered that 53 failures shared common root cause (async_transaction fixture), prevented fixing each individually

---

## Pattern Description

The Investigation-Only Protocol enforces a strict separation between bug investigation and bug fixing into three distinct phases, each with different agents/roles and explicit constraints.

**Core Principle**: "Never fix a bug you don't understand. Investigate first, fix strategically."

**Pattern Structure**:

1. **Phase 1: Bug Capture & Categorization** (PM/QA)
   - Document bug with reproduction steps
   - Categorize by domain (Database, Integration, UI, etc.)
   - Create GitHub issue from template
   - NO investigation yet, NO fixes

2. **Phase 2: Investigation-Only** (Agents - STRICT NO-FIX RULE)
   - Root cause investigation only
   - Pattern analysis across multiple bugs
   - Domain model verification
   - Comprehensive investigation report
   - **EXPLICIT CONSTRAINT**: No fixes allowed in this phase
   - **Completion Criteria**: Investigation report submitted

3. **Phase 3: Strategic Fix Planning** (PM Review)
   - Analyze investigation reports for patterns
   - Determine fix strategy (isolated fix vs. refactoring vs. domain change)
   - Assign fixes with TDD/DDD requirements
   - Execute fixes with high confidence in root cause

---

## Implementation

### Structure

```python
class InvestigationOnlyProtocol:
    """
    Enforces investigation-only constraint during E2E bug analysis.
    Prevents premature fixing while enabling pattern recognition.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.bugs = []
        self.investigations = []
        self.phase = "capture"  # phase tracking

    def phase_1_capture_bug(self, bug: Bug) -> CaptureResult:
        """Phase 1: Document bug without investigation."""
        if self.phase not in ["capture", "planning"]:
            raise ProtocolViolationError("Can only capture bugs in Phase 1")

        result = CaptureResult(
            issue_id=self._create_github_issue(bug),
            category=bug.category,
            reproduction_steps=bug.reproduction_steps,
            timestamp=datetime.now()
        )
        self.bugs.append(result)
        return result

    def phase_2_investigate_bug(self, bug_id: str) -> InvestigationReport:
        """
        Phase 2: Investigate bug - INVESTIGATION ONLY.

        Strict constraint: NO FIXES allowed in this phase.
        This phase focuses on understanding root cause.
        """
        if self.phase != "investigation":
            raise ProtocolViolationError("Must transition to Phase 2 before investigating")

        investigation = InvestigationReport(
            bug_id=bug_id,
            root_cause_hypothesis="",  # Will be filled during investigation
            pattern_analysis={},  # Will be filled during investigation
            domain_impact="",  # Will be filled during investigation
            fix_recommendation=""  # Will be filled during investigation
        )

        # Step 1: Root cause investigation
        investigation.root_cause_hypothesis = self._investigate_root_cause(bug_id)

        # Step 2: Pattern analysis
        investigation.pattern_analysis = self._analyze_patterns_across_bugs()

        # Step 3: Domain model verification
        investigation.domain_impact = self._verify_domain_model_compliance(
            investigation.root_cause_hypothesis
        )

        # Step 4: Recommendations (NOT FIXES)
        investigation.fix_recommendation = self._recommend_fix_strategy(
            investigation.root_cause_hypothesis,
            investigation.pattern_analysis
        )

        # STOP - Do NOT implement fixes
        # Report is submitted to PM for Phase 3 review

        self.investigations.append(investigation)
        return investigation

    def phase_3_plan_strategic_fixes(
        self,
        investigations: List[InvestigationReport]
    ) -> List[FixPlan]:
        """
        Phase 3: After investigation complete, plan strategic fixes.

        Only executed AFTER Phase 2 investigations are complete.
        Uses investigation findings to group fixes by pattern.
        """
        if self.phase != "planning":
            raise ProtocolViolationError("Phase 3 only after Phase 2 complete")

        # Analyze investigation reports for patterns
        patterns = self._find_patterns_across_investigations(investigations)

        # Group bugs by pattern
        grouped_fixes = self._group_by_pattern(patterns)

        # Create fix plans
        fix_plans = []
        for pattern, bugs in grouped_fixes.items():
            plan = FixPlan(
                pattern=pattern,
                bugs=bugs,
                strategy=self._determine_strategy(pattern),  # isolated/refactoring/domain
                priority=self._calculate_priority(pattern),
                tdd_requirements=self._generate_tdd_spec(pattern)
            )
            fix_plans.append(plan)

        return fix_plans

    def verify_protocol_compliance(self, session_log: str) -> ComplianceReport:
        """Verify that investigation phase had NO fix attempts."""
        fixes_attempted = self._search_for_fix_keywords(session_log)
        if fixes_attempted:
            raise ProtocolViolationError(
                f"Investigation phase contained {len(fixes_attempted)} fix attempts. "
                "Violations: " + ", ".join(fixes_attempted)
            )
        return ComplianceReport(compliant=True)
```

### Code Example

```python
# E2E Bug Protocol Implementation from Nov 18, 2025

protocol = InvestigationOnlyProtocol(project_root)

# ============================================
# PHASE 1: CAPTURE (PM)
# ============================================

e2e_bugs = [
    Bug(
        title="Database migrations not running",
        category="infrastructure",
        reproduction="Run wizard, check migrations"
    ),
    Bug(
        title="Keychain checks invisible",
        category="ux",
        reproduction="Run wizard, no progress messages"
    ),
    # ... 5 more bugs captured
]

for bug in e2e_bugs:
    protocol.phase_1_capture_bug(bug)

# Result: 7 bugs documented, categorized, GitHub issues created

# ============================================
# PHASE 2: INVESTIGATE ONLY (Code Agent)
# ============================================

protocol.phase = "investigation"  # Transition to Phase 2

investigations = []
for bug in protocol.bugs:
    # STRICT NO-FIX CONSTRAINT
    investigation = protocol.phase_2_investigate_bug(bug.issue_id)

    # Agent performs:
    # - Root cause analysis (WHY is this happening?)
    # - Pattern analysis (Do other bugs share root cause?)
    # - Domain impact assessment (Does this violate domain rules?)
    # - Fix recommendation (WHAT strategy should fix this?)

    # Agent does NOT:
    # - Implement any fixes
    # - Make code changes
    # - Execute fixes even if obvious

    investigations.append(investigation)

# Result: 7 investigation reports, root causes understood
# Key discovery: 53 test failures from async_transaction fixture
# would have been fixed individually (rework)
# Instead: Pattern identified for ONE systematic fix

# ============================================
# PHASE 3: PLAN STRATEGIC FIXES (PM)
# ============================================

protocol.phase = "planning"  # Transition to Phase 3

fix_plans = protocol.phase_3_plan_strategic_fixes(investigations)

# PM reviews investigations:
# - "Database migrations": infrastructure fix
# - "Keychain visible": UX + messaging
# - "Username reclaim": feature addition
# - "Duplicate logging": service initialization
# - "Doc links": documentation

# PM creates 5-phase fix plan (same as pattern-041)
# Assignments made with full understanding of root causes
```

### Documentation Example

```markdown
# E2E Bug Investigation Report Template

## Bug Summary
- Issue: #XXX
- Category: [Domain/Integration/UI/Infrastructure/Data]
- Reproduction: [steps]

## Phase 2: Investigation (NO FIXES)

### 1. Root Cause Investigation
**Question**: Why does this bug occur?
**Analysis**: [Investigation findings]
**Hypothesis**: [Root cause statement]
**Evidence**: [Code references, log excerpts]

### 2. Pattern Analysis
**Question**: Do other bugs share this root cause?
**Analysis**: [Cross-bug comparison]
**Pattern**: [Systemic issue identified]
**Impact**: [How many bugs affected by this pattern?]

### 3. Domain Model Verification
**Question**: Does root cause violate domain invariants?
**Check**: [Domain rules relevant to bug]
**Compliance**: [Domain impact assessment]

### 4. Fix Recommendation (NOT Implementation)
**Strategy**: [isolated/refactoring/domain/architectural]
**Rationale**: [Why this strategy?]
**TDD Spec**: [What test should verify fix?]
**Effort**: [Estimated complexity]

---

**Report Complete**: Investigation ready for Phase 3 review
**No Fixes Implemented**: Per protocol, all implementation deferred
```

---

## Benefits

| Benefit | Impact | Evidence |
|---------|--------|----------|
| **Root cause mastery** | Each bug understood deeply | 7 bugs → 5 distinct patterns |
| **Pattern recognition** | Find systemic issues | 53 failing tests from single fixture root cause |
| **Prevent rework** | Don't fix same issue multiple ways | Would have fixed 53 tests individually |
| **Domain compliance** | Fixes respect architecture | Verified domain invariants before fixing |
| **Process discipline** | Enforces DDD/TDD/Excellence | Prevents reactive patching under time pressure |
| **Documentation** | Investigation reports become knowledge base | Reference for similar issues in future |

---

## When to Use

✅ **Use Investigation-Only Protocol when**:
- E2E testing reveals multiple bugs
- Time available for investigation
- Want to prevent repeated fixes of same issue
- Domain compliance important
- Building institutional knowledge
- Multiple agents involved

❌ **Don't use when**:
- Single critical production bug needs immediate fix
- Time constraint doesn't allow investigation phase
- Cause already known
- No pattern recognition benefit

---

## Related Patterns

- **Pattern-041: Systematic Fix Planning** - Used after Phase 2 to plan fixes
- **Pattern-006: Verification-First** - Verification gate for Phase 3 fixes
- **Pattern-037: Cross-Context Validation** - Domain validation in Phase 2

---

## References

- **Evidence**: Nov 18, 2025 E2E Bug Testing session
  - Created 6 documentation files for protocol
  - CLAUDE.md updated with explicit "NO FIXES in Phase 2" rule
  - Prevents agents from implementing during investigation
  - Result: More rigorous analysis, better root cause understanding

- **Protocol Documentation**:
  - `.github/ISSUE_TEMPLATE/e2e-bug.md` - Bug capture template
  - `docs/internal/development/testing/e2e-bug-investigation-report-template.md`
  - `docs/internal/development/testing/e2e-bug-pm-review-process.md`

---

**Pattern Contributed**: Nov 21, 2025
**Pattern Authority**: Process-Core
**Maturity Level**: Proven (Implemented in protocol, ready for first full use)
