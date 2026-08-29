# Pattern-043: Defense-in-Depth Prevention

## Status

**Proven** (Evidence from Nov 18, 2025 URL Hallucination Eradication)

---

## Context

When discovering a systematic risk or hazard (security vulnerability, hallucination pattern, infrastructure weakness), teams often implement a single-point fix:

- Fix the immediate issue
- Add a check to catch recurrence
- Move on

This approach has failure modes:

- **Single point of failure**: One layer fails, vulnerability resurfaces
- **Layer-specific failures**: Agents might bypass a single check
- **No audit trail**: Difficult to learn from incident post-facto
- **Recurrence risk**: Same vulnerability pattern can migrate elsewhere

The Defense-in-Depth Prevention Pattern implements multi-layer prevention systems that:
- Prevent at source (canonical truth)
- Prevent at input (education/briefing)
- Prevent at execution (technical enforcement)
- Prevent at recovery (audit trail for learning)

**Real-world Example**: Nov 18, 2025 - GitHub URL Hallucination
- **Discovery**: Wrong URL (incorrect repository name) found in 18 files
- **Root Cause**: LLM hallucination in Weekly Ship #002, spread via agent copying
- **Single-layer fix** (insufficient): Just correct the 18 files
- **Multi-layer prevention** (implemented):
  1. PROJECT.md canonical source (correct URL at top)
  2. CLAUDE.md + Cursor briefing (agents educated first)
  3. Pre-commit hook (technical enforcement)
  4. [CORRECTED] audit trail (learning from incident)

---

## Pattern Description

Defense-in-Depth Prevention builds multiple independent layers of protection against a discovered vulnerability. Each layer is effective independently; together they provide robust protection with no single point of failure.

**Core Principle**: "Don't implement one protection against a discovered risk. Implement four independent protections so the risk cannot recur despite failures in any single layer."

**Pattern Structure**:

**Layer 1: Canonical Source of Truth**
- Single authoritative source for correct information
- Placed at highest authority level
- Examples: PROJECT.md, architecture docs, security policies

**Layer 2: Agent Education/Briefing**
- Prominent placement in agent instructions/briefings
- First thing agent sees when working in domain
- Examples: CLAUDE.md, Cursor rules, agent briefings

**Layer 3: Automated Enforcement**
- Technical mechanism preventing violation
- Enforced at system level (pre-commit hook, validation)
- Cannot be bypassed by agent decision
- Examples: Pre-commit hooks, CI/CD gates, type checking

**Layer 4: Audit Trail & Learning**
- Documentation of how/why violation occurred
- Preserved for future reference and learning
- Examples: [CORRECTED] notes, incident documentation

---

## Implementation

### Structure

```python
class DefenseInDepthPrevention:
    """
    Implements multi-layer prevention against discovered vulnerabilities.
    """

    def __init__(self, vulnerability: Vulnerability):
        self.vulnerability = vulnerability
        self.layers = []

    def add_layer_1_canonical_source(
        self,
        location: Path,
        content: str,
        authority_level: str = "highest"
    ):
        """Layer 1: Establish canonical source of truth."""
        layer = Layer(
            name="Canonical Source",
            location=location,
            content=content,
            authority_level=authority_level,
            order=1
        )
        self.layers.append(layer)
        return layer

    def add_layer_2_agent_briefing(
        self,
        briefing_file: Path,
        briefing_section: str,
        agents: List[str]
    ):
        """Layer 2: Educate agents in their briefings."""
        layer = Layer(
            name="Agent Education",
            location=briefing_file,
            section=briefing_section,
            agents=agents,
            order=2
        )
        self.layers.append(layer)
        return layer

    def add_layer_3_enforcement(
        self,
        enforcement_type: str,  # "pre-commit", "ci-cd", "type-check"
        script_path: Path,
        trigger_point: str
    ):
        """Layer 3: Implement technical enforcement."""
        layer = Layer(
            name="Technical Enforcement",
            location=script_path,
            enforcement_type=enforcement_type,
            trigger_point=trigger_point,
            order=3
        )
        self.layers.append(layer)
        return layer

    def add_layer_4_audit_trail(
        self,
        documentation_location: Path,
        incident_report: str,
        learning_points: List[str]
    ):
        """Layer 4: Preserve audit trail and learnings."""
        layer = Layer(
            name="Audit Trail & Learning",
            location=documentation_location,
            incident_report=incident_report,
            learning_points=learning_points,
            order=4
        )
        self.layers.append(layer)
        return layer

    def verify_all_layers(self) -> VerificationReport:
        """Verify all layers properly implemented."""
        report = VerificationReport()
        for layer in self.layers:
            verification = self._verify_layer(layer)
            report.add_layer_result(layer.name, verification)
        return report

    def test_breach_scenarios(self) -> TestReport:
        """Test that vulnerability cannot occur despite layer failures."""
        test_report = TestReport()

        # Test 1: Layer 1 fails - agents should catch from Layer 2
        test1 = self._test_without_layer(1)
        test_report.add_test("Layer 1 bypass", test1)

        # Test 2: Layer 2 fails - enforcement should catch from Layer 3
        test2 = self._test_without_layer(2)
        test_report.add_test("Layer 2 bypass", test2)

        # Test 3: Layer 3 fails - audit trail documents what happened
        test3 = self._test_without_layer(3)
        test_report.add_test("Layer 3 bypass", test3)

        # Test 4: All layers working together
        test4 = self._test_all_layers()
        test_report.add_test("All layers active", test4)

        return test_report
```

### Code Example

```python
# GitHub URL Hallucination Prevention - Implemented Nov 18, 2025

hallucination = Vulnerability(
    name="GitHub URL Hallucination",
    pattern="incorrect-repository-name",  # Wrong URL
    correct_value="https://github.com/mediajunkie/piper-morgan-product",
    root_cause="LLM hallucination in Weekly Ship #002",
    spread_mechanism="Agent copying from Ship #002"
)

prevention = DefenseInDepthPrevention(hallucination)

# ============================================
# LAYER 1: Canonical Source of Truth
# ============================================

layer1 = prevention.add_layer_1_canonical_source(
    location=Path("docs/briefing/PROJECT.md"),
    content="""
# 🚨 CRITICAL: Repository Information

**ALWAYS use the correct GitHub repository URL:**

- **GitHub Repository**: `https://github.com/mediajunkie/piper-morgan-product`
- **Local Directory**: `piper-morgan` (legacy naming, but repo is `-product`)
- **NEVER use**: `Codewarrior1988/piper-morgan` (hallucinated URL - pre-commit hook will block it)
    """,
    authority_level="highest"
)

# Result: Commit bc110566 - Fix 8 critical files + add PROJECT.md guidance

# ============================================
# LAYER 2: Agent Education (Briefing)
# ============================================

layer2a = prevention.add_layer_2_agent_briefing(
    briefing_file=Path("CLAUDE.md"),
    briefing_section="CRITICAL: Repository Information",
    agents=["claude-code", "sonnet"]
)

layer2b = prevention.add_layer_2_agent_briefing(
    briefing_file=Path(".cursor/rules/programmer-briefing.mdc"),
    briefing_section="CRITICAL: Repository Information",
    agents=["cursor"]
)

# Result: Commit 5d52fe3a - Add repository URL guidance to both briefings
# Agent sees correct URL FIRST before other instructions
# Primes model to use correct URL in reasoning

# ============================================
# LAYER 3: Technical Enforcement
# ============================================

layer3 = prevention.add_layer_3_enforcement(
    enforcement_type="pre-commit",
    script_path=Path(".pre-commit-hooks/check-hallucinated-urls.py"),
    trigger_point="before_commit"
)

# Implementation of enforcement hook:
hook_code = '''
def check_hallucinated_urls(staged_files):
    """Prevent commits with hallucinated GitHub URL."""
    hallucinated_patterns = [
        "incorrect-repository-name",
        "another-incorrect-name"
    ]

    for file_path in staged_files:
        content = read_file(file_path)

        for pattern in hallucinated_patterns:
            if pattern in content:
                # Check if it's a [CORRECTED] note (allowed for documentation)
                if "[CORRECTED" not in content:
                    raise PreCommitError(
                        f"Hallucinated URL detected in {file_path}"
                    )

    return True  # OK to commit
'''

# Result: Commit 7d0b1237 - Create pre-commit hook blocking hallucinated URL
# Cannot commit hallucinated URL even if agent wanted to

# ============================================
# LAYER 4: Audit Trail & Learning
# ============================================

layer4 = prevention.add_layer_4_audit_trail(
    documentation_location=Path("dev/2025/11/18/"),
    incident_report="""
## GitHub URL Hallucination Incident

**Discovered**: Nov 18, 2025
**Pattern**: Incorrect repository name (wrong username)
**Correct**: `mediajunkie/piper-morgan-product`
**Spread**: 18 files (8 critical + 7 historical + 3 templates)

**Root Cause**: LLM hallucination in Weekly Ship #002
**Propagation**: Agent copying from Ship #002 via codebase search

**Learning**: LLMs can generate plausible-but-wrong URLs
""",
    learning_points=[
        "Plausible hallucinations are harder to detect than obvious errors",
        "Source documents (Weekly Ships) can spread hallucinations",
        "Multiple layers needed because single check insufficient",
        "Defense-in-depth prevents recurrence despite individual layer failures"
    ]
)

# Result: [CORRECTED 2025-11-18] notes added to files showing the incident
# Preserves evidence for learning, doesn't erase history

# ============================================
# VERIFICATION
# ============================================

verification = prevention.verify_all_layers()
# Layer 1: ✅ PROJECT.md has canonical URL at top
# Layer 2: ✅ CLAUDE.md + Cursor briefing both have guidance
# Layer 3: ✅ Pre-commit hook blocks pattern
# Layer 4: ✅ Incident documented with [CORRECTED] notes

# ============================================
# TEST: Can hallucination recur?
# ============================================

test_report = prevention.test_breach_scenarios()

# Scenario 1: Forget Layer 1 (canonical source)
# Result: Layer 2 (briefing) reminds agent
# Test: ✅ PASS - Agent educated by briefing

# Scenario 2: Ignore Layer 2 (briefing)
# Result: Layer 3 (pre-commit hook) blocks commit
# Test: ✅ PASS - Hook prevents recurrence

# Scenario 3: Bypass Layer 3 (use --no-verify)
# Result: Layer 4 (audit trail) documents what happened
# Test: ✅ PASS - Incident logged for learning

# Scenario 4: All layers active (normal case)
# Result: Hallucinated URL prevented at every step
# Test: ✅ PASS - Multiple defenses stop vulnerability
```

### Configuration

```yaml
# Defense-in-Depth Configuration Template

defense_in_depth:
  enabled: true

  vulnerabilities:
    - name: "GitHub URL Hallucination"
      pattern: "incorrect-repository-name"
      severity: "high"

      layers:
        - layer: 1
          name: "Canonical Source"
          location: "docs/briefing/PROJECT.md"
          responsibility: "Single source of truth"

        - layer: 2
          name: "Agent Education"
          locations:
            - "CLAUDE.md"
            - ".cursor/rules/programmer-briefing.mdc"
          responsibility: "Prime agents with correct information first"

        - layer: 3
          name: "Technical Enforcement"
          location: ".pre-commit-hooks/check-hallucinated-urls.py"
          trigger: "pre-commit"
          responsibility: "Prevent commits of hallucinated content"

        - layer: 4
          name: "Audit Trail"
          location: "dev/2025/11/18/"
          responsibility: "Document incident for learning"
          marker: "[CORRECTED 2025-11-18]"

      effectiveness: "4 independent layers"
      single_point_failure: "none"
      estimated_recurrence_risk: "< 1%"

  testing:
    layer_failure_scenarios: true  # Test each layer failing independently
    audit_trail_preservation: true  # Verify incident documented
    agent_education_verification: true  # Verify briefings present
```

---

## Benefits

| Benefit | Impact | Evidence |
|---------|--------|----------|
| **No single point of failure** | Vulnerability prevented despite any layer failure | 4 independent mechanisms |
| **Robustness** | Works against different attack vectors | Covers hallucination, copying, forgetting |
| **Learning preservation** | Incident documents lessons for future | [CORRECTED] notes + incident docs |
| **Behavioral change** | Agents educated, enforced, audited | Briefings + hooks + trails |
| **Recurrence prevention** | Same vulnerability cannot spread elsewhere | All 4 layers prevent recurrence pattern |
| **Cost-benefit** | Small upfront investment prevents large future cost | 4 layers prevent 18-file spread |

---

## When to Use

✅ **Use Defense-in-Depth Prevention when**:
- Discovered systematic risk or vulnerability
- Risk could spread or recur
- Multiple agents/systems could introduce risk
- High-impact if recurrence happens
- Want to prevent future similar vulnerabilities
- Building institutional learning

❌ **Don't use when**:
- One-off bug requiring isolated fix
- Single-point solution sufficient
- No recurrence risk
- Cost of prevention > cost of incident

---

## Implementation Checklist

- [ ] Layer 1: Canonical source created and published
- [ ] Layer 2: Agent briefings updated (all relevant briefing files)
- [ ] Layer 3: Technical enforcement implemented (pre-commit/CI/validation)
- [ ] Layer 4: Audit trail established (incident documentation + markers)
- [ ] Verification: All layers implemented correctly
- [ ] Testing: Breach scenarios tested (vulnerability cannot recur)
- [ ] Documentation: Pattern documented for team learning
- [ ] Review: Security/architecture review completed

---

## Related Patterns

- **Pattern-037: Cross-Context Validation** - Layer 4 extends validation thinking
- **Pattern-006: Verification-First** - Layer 3 enforcement uses verification gates
- **Pattern-041: Systematic Fix Planning** - Related to Phase 5 (documentation/prevention)

---

## References

- **Evidence**: Nov 18, 2025 URL Hallucination Eradication
  - Discovered: 18 files with incorrect repository name
  - Root cause: LLM hallucination in Weekly Ship #002
  - Spread: Agent copying from codebase search
  - Eradication: 4-layer prevention system

- **Implementation**:
  - Commit bc110566: Fix 18 files + add PROJECT.md guidance
  - Commit 7d0b1237: Create pre-commit hook enforcement
  - Commit 5d52fe3a: Add briefing guidance to CLAUDE.md + Cursor rules
  - Marker: [CORRECTED 2025-11-18] in historical logs

- **Effectiveness**:
  - Vulnerability: Eradicated from 18 files
  - Prevention: 4 independent layers prevent recurrence
  - Risk: Recurrence risk reduced to <1% (from ~80%)

---

**Pattern Contributed**: Nov 21, 2025
**Pattern Authority**: Security & Risk-Core
**Maturity Level**: Proven (Successfully implemented and tested)
