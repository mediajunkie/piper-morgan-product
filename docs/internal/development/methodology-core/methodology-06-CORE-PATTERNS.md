---
type: methodology
title: "MANDATORY: Piper Morgan Development Methodology"
valid_from: "2025-09-21"
last_updated: "2025-09-21"
---

# MANDATORY: Piper Morgan Development Methodology

## CRITICAL: This Document Supersedes All Other Approaches

### ❌ NEVER Do These Things (Automatic Session Failure)
- **NEVER create implementation artifacts** - We use agent coordination, not handoffs
- **NEVER write code without verification first** - Always check existing patterns
- **NEVER skip systematic agent coordination** - This is our primary approach
- **NEVER assume without checking** - Verify everything with grep/find/cat
- **NEVER work outside GitHub issues** - All work must be tracked

### ✅ ALWAYS Follow This Process (No Exceptions)

#### 1. Verification First
```bash

# ALWAYS start with these commands:
find . -name "*.py" | grep [relevant_pattern]
grep -r "pattern" services/ --include="*.py"
cat services/domain/models.py  # Domain models drive everything
```

#### 2. Agent Coordination Excellence

* **Claude Code:** Multi-file systematic changes, test creation, infrastructure
* **Cursor:** Targeted debugging, UI testing, quick fixes
* **GitHub Issues:** Authoritative coordination and tracking
* **Principal Architect:** Strategic decisions only, NO implementation

#### 3. Systematic Handoffs

```
Step X: [Clear Task Name]

VERIFY FIRST:
- [Specific verification commands]

OBJECTIVE:
- [Single clear goal]

SUCCESS CRITERIA:
- [Measurable outcome]

REPORT BACK:
- [What to show on completion]
```

#### 4. End-to-End Validation

### ❌ NEVER Claim "Production Ready" Without E2E Validation
- **NEVER skip user journey testing** - Components working ≠ User experience working
- **NEVER assume integration works** - Test actual UI/API paths users take
- **NEVER declare complete without lifecycle verification** - Test intent → execution → completion
- **NEVER skip persistence testing** - Verify data survives system operations

### ✅ MANDATORY End-to-End Validation Requirements

Before any "production ready" declaration, systematically verify:

#### **1. User Journey Validation**
```bash
# Test actual user paths through real UI/API endpoints
python scripts/test_user_journeys.py --all-workflows
python scripts/test_ui_integration.py --comprehensive
```

**Required Coverage:**
- [ ] Every workflow type tested through actual UI endpoints
- [ ] Complete user input → system response cycles verified
- [ ] Error scenarios tested with realistic user inputs
- [ ] Response times measured under normal conditions

#### **2. Complete Workflow Lifecycle Testing**
```bash
# Verify end-to-end workflow execution pipeline
python scripts/test_workflow_lifecycle.py --all-types
python scripts/verify_orchestration_engine.py --persistence
```

**Required Verification:**
- [ ] **Intent Recognition** → **Workflow Creation** → **Task Execution** → **Completion**
- [ ] Workflow state persistence across system operations
- [ ] Task handler implementations actually execute (not just exist)
- [ ] Workflow results properly stored and retrievable

#### **3. Real-World Integration Validation**
```bash
# Test with realistic scenarios, not just unit test fixtures
python scripts/integration_reality_check.py --user-scenarios
```

**Required Testing:**
- [ ] External API integrations work (GitHub, databases, etc.)
- [ ] File operations complete successfully
- [ ] Network timeouts and retries function properly
- [ ] Configuration and environment variables properly loaded

#### **4. System Reliability Verification**
```bash
# Test system behavior under realistic conditions
python scripts/test_system_reliability.py --production-simulation
```

**Required Validation:**
- [ ] System handles concurrent user requests
- [ ] Database connections and queries perform adequately
- [ ] Memory usage remains stable during operation
- [ ] Error recovery mechanisms function correctly

### **E2E Validation Success Criteria**

**Before claiming "production ready", ALL must be verified:**

#### **Functional Completeness**
- [ ] Every user workflow completes successfully end-to-end
- [ ] All workflow types execute their intended tasks
- [ ] System state persists correctly across operations
- [ ] Error handling provides meaningful user feedback

#### **Integration Reliability**
- [ ] UI → Backend → Database → External APIs flow works
- [ ] Configuration loading and feature flags function properly
- [ ] File system operations complete successfully
- [ ] Network operations handle timeouts and failures gracefully

#### **User Experience Quality**
- [ ] Response times meet usability standards (<3 seconds typical)
- [ ] Error messages provide actionable guidance to users
- [ ] System recovers gracefully from common failure scenarios
- [ ] Data integrity maintained throughout user operations

### **Implementation Protocol**

#### **Agent Assignment for E2E Validation**
- **Cursor**: User journey testing, UI integration verification
- **Claude Code**: Workflow lifecycle testing, system reliability verification
- **Coordination**: GitHub issues track E2E validation status

#### **Validation Sequence**
1. **Deploy E2E validation agents** after component development complete
2. **Execute comprehensive user journey testing**
3. **Verify complete workflow lifecycles** through actual system paths
4. **Test system reliability** under realistic load conditions
5. **Document all gaps** before any "production ready" claims
6. **Fix identified issues** using systematic methodology
7. **Re-validate** until all E2E criteria met

#### **Documentation Requirements**
- [ ] E2E test results documented with specific pass/fail status
- [ ] User journey coverage map showing tested paths
- [ ] Performance benchmarks under realistic conditions
- [ ] Gap analysis with specific remediation plans

### **Quality Gate Enforcement**

#### **"Production Ready" Criteria (ALL Required)**
1. ✅ All unit tests pass
2. ✅ All integration tests pass
3. ✅ All component interfaces verified
4. ✅ **All E2E user journeys complete successfully** ← **NEW REQUIREMENT**
5. ✅ **Complete workflow lifecycles verified** ← **NEW REQUIREMENT**
6. ✅ **System reliability validated** ← **NEW REQUIREMENT**

#### **Failure Conditions (Automatic "Not Production Ready")**
- Any user workflow fails to complete end-to-end
- Any workflow type lacks proper task handler implementation
- System state persistence fails under normal operations
- User journey testing reveals broken integration paths
- Performance falls below acceptable thresholds

### **Strategic Value**

**Prevents Common Failures:**
- "Components work but user experience is broken"
- "Tests pass but real workflows don't complete"
- "Individual services work but integration fails"
- "Development environment works but production fails"

**Ensures Quality Claims Are Accurate:**
- "Production ready" means users can actually accomplish their goals
- Component quality verified AND user experience validated
- Integration reliability confirmed through systematic testing
- Performance and reliability validated under realistic conditions

This methodology addition ensures systematic development includes complete user experience validation, preventing the gap between development claims and user reality.

## Acceptance Criteria Discipline (MANDATORY)

Before ANY implementation:
1. Copy ALL acceptance criteria from GitHub issue
2. Create checklist in session log
3. Verify current completion state

Every 30 minutes:
- Check: "Am I building what was specified?"
- If exciting tangent appears: Document it, but stay on target

Before marking complete:
- Every criterion has evidence
- Screenshots/test results documented
- No assumptions about "probably done"

# Our Proven Patterns

1. Multi-Agent Orchestration: Strategic division based on agent strengths
2. GitHub-First Coordination: Issues are source of truth
3. Compound Productivity: Each success builds on previous
4. Excellence Flywheel: Quality creates velocity creates quality
5. Systematic Verification: Never assume, always verify

# Session Failure Conditions
If ANY of these occur, the session has failed our standards:

* Architect creates implementation artifacts
* Agents proceed without verification
* Work happens outside GitHub tracking
* Multiple fixes without architectural review
* Assumptions made without checking
