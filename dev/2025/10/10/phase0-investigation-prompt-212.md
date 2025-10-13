# Phase 0: Investigation & Baseline - CORE-INTENT-ENHANCE #212

**Issue**: #212 - CORE-INTENT-ENHANCE: Classification Accuracy & Pre-Classifier Optimization  
**Phase**: 0 - Investigation & Baseline  
**Agent**: Code Agent  
**Date**: October 10, 2025, 12:47 PM  
**Time Estimate**: 30-45 minutes  
**Context**: This work also closes GREAT-4A gap (75% gap in intent classification)

---

## Mission

Understand the current intent classification system, establish accuracy baseline, and identify specific improvements needed for IDENTITY and GUIDANCE categories, plus pre-classifier pattern expansion opportunities.

**Critical Context**: We recently discovered that GREAT-4A has a 75% gap with 76% test failure rate in intent classification. This work addresses that gap while completing Sprint A1.

---

## New Verification Standards (Applied to All Phases)

Every deliverable must include:
1. **Serena structural audit** ✅ - Use Serena to verify code structure
2. **Functional demonstration** ✅ - Show it actually works (not just exists)
3. **Evidence** ✅ - Terminal output, not summaries

**NO sophisticated placeholders.** If something doesn't work, document why and what's needed.

---

## Architecture Context (ADR-032)

### Dual-Path Design
```
User Input → Intent Classifier → Router → Handler → Response
                  ↓                       ↓
           Pre-Classifier          Canonical Handlers
           (Fast Path ~1ms)        or Workflow Orchestration
```

**Fast Path** (Canonical Handlers):
- Categories: IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE
- Pre-classifier recognizes patterns instantly (~1ms)
- Direct route to canonical handlers

**Workflow Path** (Orchestrated):
- Categories: EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, LEARNING, UNKNOWN, QUERY, CONVERSATION
- Full LLM classification (2000-3000ms)
- Multi-step orchestration

**Current Performance** (from GREAT-4E):
- Pre-classifier: ~1ms
- LLM classification: 2000-3000ms
- Cache hit rate: 84.6%
- Test suite: 126 tests passing

---

## Task 0.1: Locate and Review Current Code (15 min)

### Use Serena Efficiently

**Step 1**: Find intent classification files
```python
# Search for intent service files
mcp__serena__search_for_pattern(
    substring_pattern="intent",
    relative_path="services/intent_service",
    restrict_search_to_code_files=True
)
```

**Step 2**: Examine classifier structure
```python
# Get overview of LLM classifier
mcp__serena__get_symbols_overview("services/intent_service/llm_classifier.py")

# Find the classify method
mcp__serena__find_symbol(
    name_path="LLMClassifier/classify",
    relative_path="services/intent_service/llm_classifier.py",
    include_body=True
)
```

**Step 3**: Examine pre-classifier patterns
```python
# Get overview of pre-classifier
mcp__serena__get_symbols_overview("services/intent_service/pre_classifier.py")

# Find pattern definitions
mcp__serena__find_symbol(
    name_path="PreClassifier",
    relative_path="services/intent_service/pre_classifier.py",
    include_body=True
)
```

**Step 4**: Find test files
```python
# Search for classification test files
mcp__serena__search_for_pattern(
    substring_pattern="test_classification",
    relative_path="tests/intent",
    restrict_search_to_code_files=True
)
```

### Questions to Answer

1. **Where are LLM classifier prompts defined?**
   - In separate file? Embedded in code?
   - What's the structure?
   - How are categories defined?

2. **What patterns does pre-classifier currently use?**
   - How many patterns?
   - Which categories covered?
   - What's the matching logic?

3. **How are classification tests structured?**
   - Test file organization?
   - How many test queries per category?
   - How is accuracy calculated?

4. **Where are the 50+ test query sets?**
   - Existing test data?
   - Need to create new?
   - What format?

### STOP Conditions

**STOP and ask PM if**:
- Files are not in expected locations
- Architecture differs significantly from ADR-032
- Test structure is unclear
- Can't find prompt definitions

### Deliverable for Task 0.1

```markdown
## Task 0.1: Code Location Report

### Files Located
- **LLM Classifier**: [path]
  - Size: [lines]
  - Key methods: [list]
- **Pre-Classifier**: [path]
  - Size: [lines]
  - Current patterns: [count]
- **Prompts**: [location - file or embedded]
  - Structure: [description]
- **Tests**: [path]
  - Test files: [list]
  - Test structure: [description]

### Current Architecture
[Brief description of how classification works]

### Prompt Structure
- Location: [where prompts are defined]
- Format: [how categories and examples are structured]
- IDENTITY section: [exists? how detailed?]
- GUIDANCE section: [exists? how detailed?]

### Pre-Classifier Patterns
- Total patterns: [count]
- Categories covered: [list]
- Pattern type: [regex? keywords?]

### Test Structure
- Test queries per category: [typical count]
- Accuracy calculation: [how it's done]
- Test query format: [structure]

### Evidence
```bash
[Terminal output from Serena searches]
```
```

---

## Task 0.2: Run Current Accuracy Baseline (15 min)

### Run Tests and Capture Output

```bash
# Run full accuracy test suite
pytest tests/intent/test_classification_accuracy.py -v

# Capture output showing:
# - Overall accuracy
# - Per-category accuracy
# - Number of test queries per category
# - Which queries are failing
```

### Expected Results (from issue #212)
- PRIORITY: 100% accuracy ✅
- TEMPORAL: 96.7% accuracy ✅
- STATUS: 96.7% accuracy ✅
- IDENTITY: ~76% accuracy ⚠️
- GUIDANCE: ~76.7% accuracy ⚠️
- Pre-classifier: ~1% hit rate ⚠️

### Also Run Pre-Classifier Tests

```bash
# Test pre-classifier
pytest tests/intent/test_pre_classifier.py -v

# Look for hit rate metric
# Or run benchmark if exists:
python scripts/benchmark_pre_classifier.py  # if this exists
```

### Capture Evidence

**CRITICAL**: Include **full terminal output**, not summaries!

```bash
# Example of what to capture:
$ pytest tests/intent/test_classification_accuracy.py -v
=========== test session starts ===========
platform darwin -- Python 3.x.x
collected 13 items

tests/intent/test_classification_accuracy.py::test_priority_accuracy PASSED [ 7%]
tests/intent/test_classification_accuracy.py::test_temporal_accuracy PASSED [15%]
tests/intent/test_classification_accuracy.py::test_status_accuracy PASSED [23%]
tests/intent/test_classification_accuracy.py::test_identity_accuracy FAILED [30%]
...

[Include FULL output here]
```

### STOP Conditions

**STOP and ask PM if**:
- Tests don't exist or are in different format
- Can't run tests (missing dependencies)
- Accuracy is significantly different from expected
- Test failures indicate broken system (not just low accuracy)

### Deliverable for Task 0.2

```markdown
## Task 0.2: Baseline Accuracy Report

### Test Execution
```bash
[FULL terminal output from pytest]
```

### Current Accuracy by Category

| Category | Accuracy | Test Queries | Status |
|----------|----------|--------------|--------|
| PRIORITY | X% | Y queries | ✅/⚠️ |
| TEMPORAL | X% | Y queries | ✅/⚠️ |
| STATUS | X% | Y queries | ✅/⚠️ |
| IDENTITY | X% | Y queries | ⚠️ |
| GUIDANCE | X% | Y queries | ⚠️ |
| EXECUTION | X% | Y queries | ✅/⚠️ |
| ANALYSIS | X% | Y queries | ✅/⚠️ |
| SYNTHESIS | X% | Y queries | ✅/⚠️ |
| STRATEGY | X% | Y queries | ✅/⚠️ |
| LEARNING | X% | Y queries | ✅/⚠️ |
| QUERY | X% | Y queries | ✅/⚠️ |
| CONVERSATION | X% | Y queries | ✅/⚠️ |
| UNKNOWN | X% | Y queries | ✅/⚠️ |

### Pre-Classifier Performance
```bash
[Output from pre-classifier tests]
```
- Current hit rate: X%
- Categories with patterns: [list]
- Total patterns: [count]

### Overall Assessment
- Overall accuracy: X%
- Target categories (IDENTITY, GUIDANCE): X%, X%
- Improvement needed: [specific gaps]
```

---

## Task 0.3: Analyze IDENTITY Mis-classifications (10 min)

### Run with Verbose Output

```bash
# Get detailed failure information
pytest tests/intent/test_classification_accuracy.py::test_identity_accuracy -vv

# This should show:
# - Which queries failed
# - What they were classified as
# - Expected vs actual
```

### Manual Analysis

If tests don't show details, examine test file and run individual queries:

```python
# If needed, create quick analysis script
from services.intent_service.llm_classifier import LLMClassifier

classifier = LLMClassifier()

identity_queries = [
    "What can you do?",
    "What are your features?",
    "Tell me about yourself",
    # ... more from test file
]

for query in identity_queries:
    result = classifier.classify(query)
    if result.intent != "IDENTITY":
        print(f"FAIL: '{query}' → {result.intent} (expected IDENTITY)")
```

### Look for Patterns

1. **What are they mis-classifying as?**
   - QUERY?
   - CONVERSATION?
   - Other?

2. **What keywords are missing?**
   - "can you"
   - "features"
   - "capabilities"
   - "tell me about yourself"

3. **Are there consistent patterns?**
   - All capability questions → QUERY?
   - Self-referential questions → CONVERSATION?

### STOP Conditions

**STOP and ask PM if**:
- Can't determine what queries are failing
- Test structure doesn't provide failure details
- Unclear how to improve (need guidance)

### Deliverable for Task 0.3

```markdown
## Task 0.3: IDENTITY Mis-classification Analysis

### Failed Queries
[Table of: Query | Classified As | Should Be | Why It Failed]

### Pattern Analysis

**Common Mis-classifications**:
- X queries → QUERY (should be IDENTITY)
- Y queries → CONVERSATION (should be IDENTITY)

**Keywords Missing in Prompts**:
- "can you" phrases
- "features" / "capabilities"
- "tell me about yourself"
- [other patterns]

**Root Cause**:
[Explanation of why these queries fail]

### Recommendations for Phase 1
1. Add [specific keywords/patterns]
2. Enhance [specific disambiguation]
3. Include [specific examples]

### Evidence
```bash
[Terminal output showing failures]
```
```

---

## Task 0.4: Analyze GUIDANCE Mis-classifications (10 min)

### Run with Verbose Output

```bash
# Get detailed failure information
pytest tests/intent/test_classification_accuracy.py::test_guidance_accuracy -vv
```

### Manual Analysis (if needed)

```python
# Quick analysis script
from services.intent_service.llm_classifier import LLMClassifier

classifier = LLMClassifier()

guidance_queries = [
    "How should I approach this?",
    "What's the best way to...",
    "Can you guide me...",
    # ... more from test file
]

for query in guidance_queries:
    result = classifier.classify(query)
    if result.intent != "GUIDANCE":
        print(f"FAIL: '{query}' → {result.intent} (expected GUIDANCE)")
```

### Look for Patterns

1. **What are they mis-classifying as?**
   - STRATEGY?
   - CONVERSATION?
   - QUERY?

2. **What distinguishes GUIDANCE from STRATEGY?**
   - GUIDANCE: "How to do X" (tactical advice)
   - STRATEGY: "Should I do X or Y" (strategic decision)

3. **What keywords are missing?**
   - "how should I"
   - "best way to"
   - "guide me"
   - "help me"

### STOP Conditions

**STOP and ask PM if**:
- GUIDANCE vs STRATEGY boundary seems inherently ambiguous
- Can't determine clear patterns
- Need clarification on category definitions

### Deliverable for Task 0.4

```markdown
## Task 0.4: GUIDANCE Mis-classification Analysis

### Failed Queries
[Table of: Query | Classified As | Should Be | Why It Failed]

### Pattern Analysis

**Common Mis-classifications**:
- X queries → STRATEGY (should be GUIDANCE)
- Y queries → CONVERSATION (should be GUIDANCE)
- Z queries → QUERY (should be GUIDANCE)

**GUIDANCE vs STRATEGY Confusion**:
[Specific examples of ambiguous queries]

**Keywords Missing in Prompts**:
- "how should I" phrases
- "best way to" patterns
- "guide me" / "help me"
- [other patterns]

**Root Cause**:
[Explanation of why these queries fail]

### Recommendations for Phase 2
1. Strengthen [specific disambiguation]
2. Add [specific keywords/patterns]
3. Include [specific examples]

### Evidence
```bash
[Terminal output showing failures]
```
```

---

## Phase 0 Final Deliverable

**Create**: `dev/2025/10/10/phase0-baseline-report.md`

Combine all tasks into comprehensive report:

```markdown
# Phase 0: Investigation & Baseline Complete

**Date**: October 10, 2025  
**Issue**: #212 (also closes GREAT-4A gap)  
**Agent**: Code Agent  
**Time**: [actual time taken]

---

## Executive Summary

[2-3 sentence summary of current state and what needs to be done]

---

## Task 0.1: Code Location

[Include Task 0.1 deliverable content]

---

## Task 0.2: Baseline Accuracy

[Include Task 0.2 deliverable content]

---

## Task 0.3: IDENTITY Analysis

[Include Task 0.3 deliverable content]

---

## Task 0.4: GUIDANCE Analysis

[Include Task 0.4 deliverable content]

---

## Recommendations

### Phase 1: IDENTITY Enhancement
[List specific changes needed with confidence level]

### Phase 2: GUIDANCE Enhancement
[List specific changes needed with confidence level]

### Phase 3: Pre-Classifier Expansion
[List patterns to add based on current structure]

---

## STOP Conditions Evaluation

- [ ] Current accuracy acceptable as-is?
- [ ] Achieving 90% requires fundamental redesign?
- [ ] Architecture significantly different from ADR-032?
- [ ] Other blockers identified?

**Decision**: Proceed to Phase 1 / Stop and discuss with PM

---

## Evidence Appendix

### Full Test Output
```bash
[Complete terminal output from all test runs]
```

### Serena Audit Trail
```bash
[All Serena commands and outputs used]
```

---

**Verification Checklist**:
- ✅ Serena structural audit completed
- ✅ Functional tests executed (not just reviewed)
- ✅ Full terminal output captured (evidence)
- ✅ Specific recommendations with examples
- ✅ STOP conditions evaluated

**Status**: Ready for Phase 1 / Need PM guidance
```

---

## Success Criteria for Phase 0

- [ ] All files located and structure understood
- [ ] Baseline accuracy established with evidence
- [ ] IDENTITY mis-classification patterns identified
- [ ] GUIDANCE mis-classification patterns identified
- [ ] Specific recommendations for each phase
- [ ] Full terminal output captured (not summaries)
- [ ] STOP conditions evaluated
- [ ] Report created in `dev/2025/10/10/phase0-baseline-report.md`

---

## Important Notes

### On Evidence
**DO**: Capture full terminal output
```bash
$ pytest tests/intent/test_classification_accuracy.py -v
=========== test session starts ===========
[FULL OUTPUT HERE]
===========  X passed, Y failed in Z.ZZs ===========
```

**DON'T**: Summarize output
```
Tests ran and showed 76% accuracy for IDENTITY.
```

### On Serena Usage
Use Serena to navigate codebase efficiently, but also **read the actual code** to understand implementation details. Serena helps you find things, but you still need to understand them.

### On Functional Demonstration
This is investigation phase, so "functional demonstration" means:
- Actually running tests (not just reading test files)
- Actually executing queries (if doing manual analysis)
- Actually examining failure output (not inferring)

### On STOP Conditions
**Don't hesitate to stop and ask** if:
- Architecture is confusing
- Test structure is unclear
- Can't determine root cause
- Need clarification on category definitions

Better to ask than to proceed on wrong assumptions.

---

## After Phase 0 Completion

1. **Notify PM**: Phase 0 complete, report ready for review
2. **Wait for approval**: Don't proceed to Phase 1 without green light
3. **Be ready to discuss**: Findings, recommendations, approach

**PM will review and approve** Phase 1 prompt based on Phase 0 findings.

---

*Phase 0 prompt created: October 10, 2025, 12:47 PM*  
*Time estimate: 30-45 minutes*  
*Next: Phase 1 (IDENTITY enhancement) after Phase 0 review*
