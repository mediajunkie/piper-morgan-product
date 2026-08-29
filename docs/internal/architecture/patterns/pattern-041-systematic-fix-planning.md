# Pattern-041: Systematic Fix Planning

## Status

**Proven** (Evidence from Nov 18, 2025 Alpha Testing session)

---

## Context

When facing multiple related issues (bugs, refactoring needs, infrastructure improvements), teams often resort to reactive, piecemeal fixes. Each issue is addressed independently, leading to:

- **Quality degradation**: Individual fixes miss shared root causes
- **Documentation debt**: Changes not systematically documented
- **Rework risk**: Same underlying issue fixed multiple times
- **Testing gaps**: Individual fixes tested in isolation, not as system
- **Team coordination loss**: Parallel work on related issues creates conflicts

The Systematic Fix Planning Pattern ensures quality and coordination by grouping related issues into phases before executing fixes.

**Real-world Example**: Nov 18, 2025 - Wizard cleanup issues.
- **Reactive approach**: 7 separate bug fixes, scattered across codebase
- **Systematic approach**: 5-phase plan (migrations → keychain → username → status → polish), all fixes committed individually with test verification
- **Outcome**: Higher quality, better documented, completed faster

---

## Pattern Description

Systematic Fix Planning groups related issues into **phases based on issue type**, executes each phase completely before moving to the next, and verifies all fixes before integration.

**Core Principle**: "Multiple related issues → shared root causes → group by type → fix by phase → verify systematically"

**Pattern Structure**:

1. **Issue Analysis Phase** (Understanding)
   - Inventory all related issues
   - Categorize by type (fixtures, imports, syntax, architecture, etc.)
   - Identify shared root causes

2. **Phase Planning** (Organizing)
   - Group issues by category
   - Determine dependency order
   - Estimate effort per phase

3. **Execution Phase** (Implementation)
   - Execute one phase at a time
   - Fix all issues of that type
   - Commit each fix individually (enables rollback)

4. **Verification Phase** (Quality)
   - Test each fix independently
   - Verify no regressions
   - Run full suite after each phase

5. **Documentation Phase** (Cleanup)
   - Polish and final documentation
   - Update related docs
   - Create reusable templates for this issue class

---

## Implementation

### Structure

```python
class SystematicFixPlanner:
    """Orchestrates systematic fix planning."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.issues = []
        self.phases = []

    def analyze_issues(self, issues: List[Issue]) -> Dict[str, List[Issue]]:
        """Categorize issues by type."""
        categorized = defaultdict(list)
        for issue in issues:
            category = self._determine_category(issue)
            categorized[category].append(issue)
        return dict(categorized)

    def plan_phases(self, categorized_issues: Dict) -> List[Phase]:
        """Create execution phases from categorized issues."""
        phases = []
        for category, issues in categorized_issues.items():
            phase = Phase(
                name=category,
                issues=issues,
                order=self._determine_phase_order(category),
                verification_criteria=self._criteria_for_category(category)
            )
            phases.append(phase)
        return sorted(phases, key=lambda p: p.order)

    def execute_phase(self, phase: Phase) -> PhaseResult:
        """Execute all fixes for a single phase."""
        results = []
        for issue in phase.issues:
            try:
                # Fix the issue
                fix = self._apply_fix(issue)

                # Commit individually
                commit = self._commit_fix(issue, fix)

                # Verify
                verification = self._verify_fix(issue, fix)

                results.append({
                    "issue": issue,
                    "fix": fix,
                    "commit": commit,
                    "verified": verification.passed
                })

                if not verification.passed:
                    raise FixVerificationError(verification.failures)

            except Exception as e:
                logger.error(f"Phase execution failed on {issue}: {e}")
                # Can rollback individual commits
                raise

        return PhaseResult(phase=phase, results=results)
```

### Code Example

```python
# Actual implementation from Nov 18 Alpha Testing session

wizard_issues = [
    Issue("Database migrations not running", type="infrastructure"),
    Issue("Keychain checks invisible", type="ux"),
    Issue("Cannot reclaim username", type="feature"),
    Issue("dict has no attribute is_active", type="bug"),
    Issue("Duplicate logging", type="bug"),
    Issue("SQLAlchemy import unclear", type="docs"),
    Issue("Doc links broken", type="docs"),
]

planner = SystematicFixPlanner(project_root)

# Phase 1: Categorize
categorized = planner.analyze_issues(wizard_issues)
# Result:
# {
#   "infrastructure": [migrations],
#   "ux": [keychain],
#   "feature": [username reclaim],
#   "bug": [dict attribute, duplicate logging],
#   "docs": [imports, links]
# }

# Phase 2: Plan
phases = planner.plan_phases(categorized)
# Result:
# [
#   Phase(infrastructure),  # Foundation - run first
#   Phase(ux),              # User experience - run second
#   Phase(feature),         # Features - run third
#   Phase(bug),             # Bugs - run fourth
#   Phase(docs),            # Documentation - run last
# ]

# Phase 3: Execute
for phase in phases:
    result = planner.execute_phase(phase)
    print(f"Phase {phase.name}: {len(result.verified)} fixed, {len(result.failed)} failed")
    if result.failed:
        raise PhaseFailedError(result.failed)

# Result: 115 minutes, all 7 issues fixed, no regressions, 5 commits

# Phase 4: Verify
test_result = run_full_test_suite()
assert test_result.passed, "Full suite must pass"

# Phase 5: Document
create_reusable_wizard_fix_template(phases)
```

### Configuration

```yaml
# Systematic Fix Planning Configuration
systematic_fix_planning:
  enabled: true

  phase_categories:
    - name: "infrastructure"
      priority: 1
      examples:
        - "database migrations"
        - "service initialization"
        - "environment setup"

    - name: "ux"
      priority: 2
      examples:
        - "user-facing messages"
        - "progress indicators"
        - "error visibility"

    - name: "feature"
      priority: 3
      examples:
        - "new capabilities"
        - "user flows"
        - "edge case handling"

    - name: "bug"
      priority: 4
      examples:
        - "logic errors"
        - "incorrect attribute access"
        - "duplicate operations"

    - name: "docs"
      priority: 5
      examples:
        - "documentation clarity"
        - "link validity"
        - "example accuracy"

  verification:
    per_fix: true  # Test after each individual fix
    per_phase: true  # Test after each phase
    full_suite: true  # Test after all phases

  commit_strategy: "individual"  # One commit per fix
  documentation: "comprehensive"  # All changes documented
```

---

## Benefits

| Benefit | Impact | Evidence |
|---------|--------|----------|
| **Root cause discovery** | Identifies shared underlying issues | Duplicate logging found to be service initialization problem |
| **Quality assurance** | Each fix tested independently + full suite | 45 tests passing, 0 regressions |
| **Documentation** | All fixes documented for future reference | Became template for similar issues |
| **Efficiency** | Shared root cause fix prevents future rework | Single fix solves multiple surface issues |
| **Team coordination** | Clear phases enable parallel work in future | Blueprint for similar multi-issue cleanup |
| **Rollback capability** | Individual commits enable precise rollback | Can revert specific fix if needed |

---

## When to Use

✅ **Use Systematic Fix Planning when**:
- Facing 4+ related issues
- Issues likely share root causes
- Quality is higher priority than speed
- Team needs to learn from the issues
- Similar issues likely to appear in future

❌ **Don't use when**:
- Single critical issue needs immediate fix
- Time constraint more important than learning
- Issues completely unrelated
- Prototype/throwaway code

---

## Related Patterns

- **Pattern-006: Verification-First** - Each phase verification gate
- **Pattern-031: Phase -1 Planning** - Planning before implementation
- **Pattern-037: Cross-Context Validation** - Verify fix in multiple contexts
- **Pattern-041: Investigation-Only Protocol** - Understand before fixing

---

## References

- **Evidence**: Nov 18, 2025 Alpha Testing session
  - Wizard cleanup: 7 issues → 5 phases → 115 minutes → all fixed
  - Commit log: 5 commits (d4dff6dc, 8103e6a0, 23c5d059, 14252139, 6bcaa313)
  - Test results: 45 passed, 8 skipped, 0 regressions

- **Previous Usage**:
  - Nov 19: Test infrastructure cleanup (14 collection errors → 8 files → 8 individual commits)
  - Pattern proven effective for multi-issue resolution

---

**Pattern Contributed**: Nov 21, 2025
**Pattern Authority**: Methodology-Core
**Maturity Level**: Proven (Evidence from 2 independent applications)
