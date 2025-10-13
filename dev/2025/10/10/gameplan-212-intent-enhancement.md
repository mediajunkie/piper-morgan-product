# CORE-INTENT-ENHANCE #212: Classification Accuracy & Pre-Classifier Optimization

**Gameplan Version**: 1.0  
**Created**: October 10, 2025, 10:04 AM  
**Issue**: #212  
**Priority**: Medium (optimization, not blocking)  
**Time Estimate**: 4-6 hours  
**Context**: Post-GREAT-4F enhancement, ADR-032 production system

---

## Executive Summary

**Goal**: Improve intent classification accuracy for IDENTITY and GUIDANCE categories, and expand pre-classifier pattern coverage for faster common query handling.

**Current State**:
- ✅ PRIORITY: 100% accuracy
- ✅ TEMPORAL: 96.7% accuracy
- ✅ STATUS: 96.7% accuracy
- ⚠️ IDENTITY: 76% accuracy → Target: 90%+
- ⚠️ GUIDANCE: 76.7% accuracy → Target: 90%+
- ⚠️ Pre-classifier: ~1% hit rate → Target: 10%+

**Success Criteria**:
- IDENTITY accuracy ≥ 90% (50+ test queries)
- GUIDANCE accuracy ≥ 90% (50+ test queries)
- Pre-classifier hit rate ≥ 10%
- No regression in other categories (all stay >75%)
- Performance maintained (<100ms for pre-classifier)

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

### Files Involved
- **Classifier**: `services/intent_service/llm_classifier.py`
- **Pre-classifier**: `services/intent_service/pre_classifier.py`
- **Prompts**: Embedded in classifier or `services/llm/prompts/intent_classifier.py`
- **Tests**: `tests/intent/test_classification_accuracy.py`
- **Canonical Handlers**: `services/intent_service/canonical_handlers.py`

---

## Anti-80% Discipline

### What We Will NOT Do
- ❌ Chase 100% accuracy (diminishing returns)
- ❌ Over-engineer pattern matching (complexity creep)
- ❌ Add categories without clear use case
- ❌ Optimize beyond user-noticeable improvements
- ❌ Build complex ML training pipelines (out of scope)

### What We WILL Do
- ✅ Target 90% accuracy (good enough for production)
- ✅ Use simple regex patterns (maintainable)
- ✅ Test with real-world queries
- ✅ Stop when criteria met
- ✅ Document patterns for future maintenance

### STOP Conditions
1. If investigation shows current accuracy is actually acceptable
2. If achieving 90% requires fundamental redesign
3. If pattern expansion causes false positive issues
4. If testing reveals regression in other categories
5. If performance degrades below acceptable thresholds

**In any STOP condition**: Document findings, explain trade-offs, recommend next steps or deferral.

---

## Phase 0: Investigation & Baseline (30-45 minutes)

**Agent**: Code Agent  
**Goal**: Understand current system and establish baseline

### Task 0.1: Locate and Review Current Code (15 min)

**Use Serena** to efficiently explore:

```python
# Find intent classification files
mcp__serena__search_for_pattern(
    substring_pattern="intent",
    relative_path="services/intent_service",
    restrict_search_to_code_files=True
)

# Examine classifier structure
mcp__serena__get_symbols_overview("services/intent_service/llm_classifier.py")

# Examine pre-classifier patterns
mcp__serena__get_symbols_overview("services/intent_service/pre_classifier.py")

# Find test files
mcp__serena__search_for_pattern(
    substring_pattern="test_classification",
    relative_path="tests/intent",
    restrict_search_to_code_files=True
)
```

**Questions to Answer**:
1. Where are LLM classifier prompts defined?
2. What patterns does pre-classifier currently use?
3. How are classification tests structured?
4. Where are the 50+ test query sets?

**STOP if**: Files are not where expected, or architecture differs significantly from ADR-032.

---

### Task 0.2: Run Current Accuracy Baseline (15 min)

```bash
# Run accuracy tests
pytest tests/intent/test_classification_accuracy.py -v

# Expected output:
# - Overall accuracy: ~89.3%
# - IDENTITY: ~76%
# - GUIDANCE: ~76.7%
# - Other categories: >90%

# Check pre-classifier hit rate
pytest tests/intent/test_pre_classifier.py -v
# Expected: ~1% hit rate
```

**Capture**:
- Exact current accuracy for each category
- Number of test queries per category
- Pre-classifier hit rate
- Any unexpected failures

**Document in**: `dev/2025/10/10/phase0-baseline-report.md`

---

### Task 0.3: Analyze IDENTITY Mis-classifications (10 min)

**Review test failures**:
```bash
# Run IDENTITY tests with verbose output
pytest tests/intent/test_classification_accuracy.py::test_identity_accuracy -vv

# Capture which queries are mis-classifying
# Look for patterns in failures
```

**Questions**:
1. Which IDENTITY queries classify as QUERY?
2. What keywords are missing in prompts?
3. Are there consistent patterns in failures?

---

### Task 0.4: Analyze GUIDANCE Mis-classifications (10 min)

**Review test failures**:
```bash
# Run GUIDANCE tests with verbose output
pytest tests/intent/test_classification_accuracy.py::test_guidance_accuracy -vv

# Capture which queries are mis-classifying
# Look for patterns in failures
```

**Questions**:
1. Which GUIDANCE queries classify as CONVERSATION/STRATEGY?
2. What distinguishes advice from strategic planning?
3. Are there consistent patterns in failures?

---

### Phase 0 Deliverable

**Report**: `dev/2025/10/10/phase0-baseline-report.md`

```markdown
# Phase 0: Investigation & Baseline

## Current System

### Files Located
- Classifier: [path]
- Pre-classifier: [path]
- Prompts: [path]
- Tests: [path]

### Current Accuracy
- IDENTITY: X% (Y/Z queries)
- GUIDANCE: X% (Y/Z queries)
- Pre-classifier: X% hit rate
- Other categories: [list with %]

### IDENTITY Mis-classifications
[Table of query → wrong classification → reason]

### GUIDANCE Mis-classifications
[Table of query → wrong classification → reason]

## Recommendations

### IDENTITY Enhancement
[List specific prompt changes needed]

### GUIDANCE Enhancement
[List specific prompt changes needed]

### Pre-classifier Patterns
[List patterns to add]

## STOP Conditions Evaluation
- [ ] Current accuracy acceptable as-is?
- [ ] Achieving 90% requires redesign?
- [ ] Other blockers?

**Decision**: Proceed to Phase 1 / Stop and document why
```

---

## Phase 1: IDENTITY Enhancement (1-2 hours)

**Agent**: Code Agent  
**Goal**: Improve IDENTITY accuracy from 76% to 90%+  
**Prerequisites**: Phase 0 complete with clear recommendations

### Context for Agent

**IDENTITY Intent**: Questions about Piper's capabilities, features, identity, and what it can do.

**Current Problem** (from issue):
- "What can you do?" → Mis-classifies as QUERY
- "What are your features?" → Mis-classifies as QUERY
- "Tell me about yourself" → Sometimes CONVERSATION

**Why This Matters**:
- Users need to discover Piper's capabilities
- IDENTITY has fast canonical handler (~1ms)
- Mis-classification to QUERY causes slower response

---

### Task 1.1: Review Current IDENTITY Prompt (15 min)

**Use Serena** to examine current prompt:

```python
# Find IDENTITY in classifier prompt
mcp__serena__search_for_pattern(
    substring_pattern="IDENTITY",
    relative_path="services/intent_service",
    restrict_search_to_code_files=True
)

# Read the full prompt definition
mcp__serena__find_symbol(
    name_path="IDENTITY",
    relative_path="[path from search]",
    include_body=True
)
```

**Understand**:
1. What examples are currently in the prompt?
2. What keywords are emphasized?
3. What disambiguation guidance exists?

---

### Task 1.2: Enhance IDENTITY Prompt (30 min)

**Add to classifier prompt**:

**Capability Keywords**:
- "what can you", "what do you", "what are you capable of"
- "your features", "your capabilities", "your skills"
- "tell me about yourself", "who are you", "what are you"
- "how do you work", "what can you help with"

**Disambiguation Guidance**:
```
IDENTITY vs QUERY:
- IDENTITY: Questions about Piper's own capabilities/features
- QUERY: Questions about external information or user's data

Examples:
- "What can you do?" → IDENTITY (asking about Piper)
- "What can I do today?" → QUERY (asking about user's data)
- "What are your features?" → IDENTITY (asking about Piper)
- "What are my features?" → QUERY (asking about user's system)
```

**Examples to Add**:
```
IDENTITY examples:
- "What can you help me with?"
- "What are your capabilities?"
- "Tell me about yourself"
- "What features do you have?"
- "How do you work?"
- "What do you do?"
- "Can you explain what you are?"
- "What's your purpose?"
```

**STOP if**: 
- Prompt is already comprehensive and well-structured
- Current examples are sufficient and clear
- Changes would require major prompt redesign

---

### Task 1.3: Test IDENTITY Enhancement (30 min)

**Create test queries** (if not already existing):
```python
IDENTITY_TEST_QUERIES = [
    "What can you do?",
    "What are your features?",
    "Tell me about yourself",
    "What are your capabilities?",
    "How do you work?",
    "What can you help me with?",
    "What's your purpose?",
    "Can you explain what you are?",
    "What do you do?",
    "What are you capable of?",
    # ... add 40+ more variants
]
```

**Run tests**:
```bash
# Test IDENTITY accuracy
pytest tests/intent/test_classification_accuracy.py::test_identity_accuracy -v

# Target: ≥90% accuracy
```

**If accuracy < 90%**:
1. Review which queries still fail
2. Identify common patterns
3. Enhance prompt further
4. Re-test

**If accuracy ≥ 90%**: Proceed to Phase 2

---

### Task 1.4: Verify No Regression (15 min)

```bash
# Run full test suite
pytest tests/intent/test_classification_accuracy.py -v

# Ensure all categories maintain >75% accuracy
# Especially check:
# - QUERY (shouldn't absorb former IDENTITY queries)
# - CONVERSATION (shouldn't be affected)
# - Other canonical handlers (should remain stable)
```

**STOP if**: Any category drops below 75% accuracy.

---

### Phase 1 Deliverable

**Report**: `dev/2025/10/10/phase1-identity-complete.md`

```markdown
# Phase 1: IDENTITY Enhancement Complete

## Prompt Changes
[Show before/after of prompt sections]

## Test Results

### IDENTITY Accuracy
- Before: 76% (X/Y queries)
- After: Z% (X/Y queries)
- Target: ≥90% ✅/❌

### Regression Check
[Table of all categories with before/after %]

## Mis-classifications Resolved
[List of queries that now classify correctly]

## Remaining Issues
[List any queries still mis-classifying, if <90%]

## Evidence
```bash
$ pytest tests/intent/test_classification_accuracy.py::test_identity_accuracy -v
[test output]
```

## Status
- ✅ IDENTITY accuracy ≥90%
- ✅ No regression in other categories
- Ready for Phase 2
```

---

## Phase 2: GUIDANCE Enhancement (1-2 hours)

**Agent**: Code Agent  
**Goal**: Improve GUIDANCE accuracy from 76.7% to 90%+  
**Prerequisites**: Phase 1 complete

### Context for Agent

**GUIDANCE Intent**: Questions asking for advice, recommendations, how-to instructions, or guidance on approaching something.

**Current Problem** (from issue):
- "How should I approach this?" → Varies unpredictably
- "What's the best way to..." → Sometimes STRATEGY
- "Can you guide me..." → Sometimes CONVERSATION

**Why This Matters**:
- Users need help with workflows
- GUIDANCE has fast canonical handler (~1ms)
- Mis-classification to STRATEGY causes slower orchestrated response

---

### Task 2.1: Review Current GUIDANCE Prompt (15 min)

**Use Serena** to examine current prompt:

```python
# Find GUIDANCE in classifier prompt
mcp__serena__search_for_pattern(
    substring_pattern="GUIDANCE",
    relative_path="services/intent_service",
    restrict_search_to_code_files=True
)
```

**Understand**:
1. Current examples for GUIDANCE
2. Current disambiguation vs STRATEGY
3. Keywords emphasized

---

### Task 2.2: Enhance GUIDANCE Prompt (30 min)

**Add to classifier prompt**:

**Advice/Recommendation Keywords**:
- "how should I", "what's the best way", "how do I"
- "can you guide me", "can you help me", "show me how"
- "what do you recommend", "what would you suggest"
- "how to", "best practices", "advice"

**Disambiguation Guidance**:
```
GUIDANCE vs STRATEGY:
- GUIDANCE: Asking for instructions/advice on HOW to do something
- STRATEGY: Asking for high-level planning or WHAT to prioritize

Examples:
- "How should I create an issue?" → GUIDANCE (asking how-to)
- "Should I focus on bugs or features?" → STRATEGY (asking what to prioritize)
- "What's the best way to write a PR?" → GUIDANCE (asking for advice on execution)
- "What's the best strategy for Q4?" → STRATEGY (asking for strategic planning)

GUIDANCE vs CONVERSATION:
- GUIDANCE: Specific request for help/advice on a task
- CONVERSATION: General chat or clarification

Examples:
- "Can you guide me through this?" → GUIDANCE (asking for help)
- "Can you explain that?" → CONVERSATION (asking for clarification)
```

**Examples to Add**:
```
GUIDANCE examples:
- "How should I approach this?"
- "What's the best way to do X?"
- "Can you guide me through Y?"
- "Show me how to Z"
- "What do you recommend for this?"
- "How do I get started with A?"
- "What are best practices for B?"
- "Can you help me with C?"
```

**STOP if**: 
- Prompt already has comprehensive disambiguation
- GUIDANCE vs STRATEGY boundary is inherently ambiguous
- Achieving 90% requires restructuring category definitions

---

### Task 2.3: Test GUIDANCE Enhancement (30 min)

**Create test queries** (if not already existing):
```python
GUIDANCE_TEST_QUERIES = [
    "How should I approach this?",
    "What's the best way to create an issue?",
    "Can you guide me through the workflow?",
    "Show me how to write a PR",
    "What do you recommend for testing?",
    "How do I get started?",
    "What are best practices?",
    "Can you help me with this task?",
    # ... add 40+ more variants
]
```

**Run tests**:
```bash
# Test GUIDANCE accuracy
pytest tests/intent/test_classification_accuracy.py::test_guidance_accuracy -v

# Target: ≥90% accuracy
```

**If accuracy < 90%**:
1. Review which queries still fail
2. Check if mis-classifying to STRATEGY or CONVERSATION
3. Enhance disambiguation further
4. Re-test

**If accuracy ≥ 90%**: Proceed to Phase 3

---

### Task 2.4: Verify No Regression (15 min)

```bash
# Run full test suite
pytest tests/intent/test_classification_accuracy.py -v

# Ensure all categories maintain >75% accuracy
# Especially check:
# - STRATEGY (shouldn't lose legitimate strategic queries)
# - CONVERSATION (shouldn't be affected)
# - IDENTITY (should remain at Phase 1 level)
```

**STOP if**: Any category drops below 75% accuracy.

---

### Phase 2 Deliverable

**Report**: `dev/2025/10/10/phase2-guidance-complete.md`

```markdown
# Phase 2: GUIDANCE Enhancement Complete

## Prompt Changes
[Show before/after of prompt sections]

## Test Results

### GUIDANCE Accuracy
- Before: 76.7% (X/Y queries)
- After: Z% (X/Y queries)
- Target: ≥90% ✅/❌

### Regression Check
[Table of all categories with before/after %]

## Mis-classifications Resolved
[List of queries that now classify correctly]

## Remaining Issues
[List any queries still mis-classifying, if <90%]

## Evidence
```bash
$ pytest tests/intent/test_classification_accuracy.py::test_guidance_accuracy -v
[test output]
```

## Status
- ✅ GUIDANCE accuracy ≥90%
- ✅ No regression in other categories
- Ready for Phase 3
```

---

## Phase 3: Pre-Classifier Expansion (1-2 hours)

**Agent**: Code Agent  
**Goal**: Expand pre-classifier patterns from ~1% to 10%+ hit rate  
**Prerequisites**: Phases 1-2 complete

### Context for Agent

**Pre-Classifier Purpose**: Fast-path pattern matching (~1ms) to route common queries directly to canonical handlers without LLM classification.

**Current State**: 
- Hit rate: ~1% (mostly just "help")
- Canonical handlers: IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE

**Why This Matters**:
- 1ms vs 2000-3000ms response time
- Reduces LLM API costs
- Better user experience for common queries

**Architecture Note**: Pre-classifier is a **pattern-based fast path**, not a replacement for LLM classification. False positives are worse than misses (just falls back to LLM).

---

### Task 3.1: Review Current Pre-Classifier (15 min)

**Use Serena**:
```python
# Examine pre-classifier patterns
mcp__serena__get_symbols_overview("services/intent_service/pre_classifier.py")

# Find pattern definitions
mcp__serena__find_symbol(
    name_path="PreClassifier",
    relative_path="services/intent_service/pre_classifier.py",
    include_body=True
)
```

**Understand**:
1. How patterns are defined (regex? keywords?)
2. Current pattern sets
3. Pattern matching logic
4. False positive prevention

---

### Task 3.2: Add TEMPORAL Patterns (20 min)

**Add pattern set**:
```python
TEMPORAL_PATTERNS = [
    # Time queries
    r'\b(what|when).{0,10}(time|day|date)\b',
    r'\bwhat.{0,10}today\b',
    r'\bwhat.{0,10}tomorrow\b',
    
    # Calendar/schedule
    r'\b(calendar|schedule|appointment|meeting)s?\b',
    r'\btoday.{0,10}(schedule|meeting|appointment)\b',
    r'\bthis week\b',
    r'\bnext week\b',
    
    # Date-specific
    r'\bwhen is\b',
    r'\bwhat day\b',
    r'\bwhat date\b',
]
```

**Test patterns**:
```python
test_queries = [
    "What time is it?",
    "What's the date today?",
    "When is my next meeting?",
    "Show me my calendar",
    "What day is it?",
    # ... add more
]

for query in test_queries:
    result = pre_classifier.classify(query)
    assert result == "TEMPORAL", f"Failed: {query} → {result}"
```

**STOP if**: 
- Patterns cause false positives (e.g., "what time did you suggest?" → TEMPORAL but should be CONVERSATION)
- Performance degrades (test with 10,000 queries should still be <100ms total)

---

### Task 3.3: Add STATUS Patterns (20 min)

**Add pattern set**:
```python
STATUS_PATTERNS = [
    # Work status
    r'\b(standup|stand-up|status)\b',
    r'\bworking on\b',
    r'\bcurrent (task|project|work)\b',
    r'\bmy (progress|status)\b',
    r'\bwhat am i\b',
    
    # Project queries
    r'\bproject status\b',
    r'\btask status\b',
    r'\bwork status\b',
]
```

**Test patterns**: Similar to 3.2

---

### Task 3.4: Add PRIORITY Patterns (20 min)

**Add pattern set**:
```python
PRIORITY_PATTERNS = [
    # Priority queries
    r'\b(priority|priorities)\b',
    r'\b(urgent|important|critical)\b',
    r'\bfocus on\b',
    r'\btop (item|task|priority)\b',
    r'\bhighest priority\b',
    
    # What should I
    r'\bwhat should i (do|work on|focus)\b',
    r'\bwhere should i start\b',
]
```

**Test patterns**: Similar to 3.2

---

### Task 3.5: Measure Hit Rate Improvement (15 min)

**Create benchmark**:
```python
# Script: benchmark_pre_classifier.py
common_queries = [
    # 100+ real-world common queries
    # Mix of TEMPORAL, STATUS, PRIORITY, and others
]

hits = 0
total = len(common_queries)

for query in common_queries:
    result = pre_classifier.classify(query)
    if result is not None:  # Hit (pattern matched)
        hits += 1

hit_rate = (hits / total) * 100
print(f"Pre-classifier hit rate: {hit_rate:.1f}%")

# Target: ≥10%
```

**Run benchmark**:
```bash
python benchmark_pre_classifier.py

# Expected output:
# Pre-classifier hit rate: 10%+ ✅
```

**STOP if**: Hit rate doesn't improve significantly (still <5%) - patterns may not be matching real queries.

---

### Task 3.6: Verify Performance (10 min)

**Performance test**:
```python
import time

queries = common_queries * 100  # 10,000 queries

start = time.time()
for query in queries:
    pre_classifier.classify(query)
end = time.time()

total_time_ms = (end - start) * 1000
avg_time_ms = total_time_ms / len(queries)

print(f"Total: {total_time_ms:.2f}ms for {len(queries)} queries")
print(f"Average: {avg_time_ms:.4f}ms per query")

# Target: <0.01ms per query (100ms total for 10k queries)
```

**STOP if**: Performance degrades beyond acceptable (<100ms for 10k queries).

---

### Phase 3 Deliverable

**Report**: `dev/2025/10/10/phase3-pre-classifier-complete.md`

```markdown
# Phase 3: Pre-Classifier Expansion Complete

## Patterns Added

### TEMPORAL Patterns
[List patterns with examples]

### STATUS Patterns
[List patterns with examples]

### PRIORITY Patterns
[List patterns with examples]

## Hit Rate Improvement
- Before: ~1%
- After: X%
- Target: ≥10% ✅/❌

## Performance
- 10,000 queries in Xms
- Average: Xms per query
- Target: <100ms total ✅/❌

## False Positive Check
[Any patterns causing false positives?]

## Evidence
```bash
$ python benchmark_pre_classifier.py
Pre-classifier hit rate: X%
```

## Status
- ✅ Hit rate ≥10%
- ✅ Performance <100ms
- ✅ No false positives
- Ready for Phase 4
```

---

## Phase 4: Validation & Testing (1 hour)

**Agent**: Code Agent  
**Goal**: Comprehensive validation of all enhancements  
**Prerequisites**: Phases 1-3 complete

### Task 4.1: Full Test Suite (20 min)

```bash
# Run complete intent test suite
pytest tests/intent/ -v

# Should include:
# - Classification accuracy tests (all 13 categories)
# - Pre-classifier tests
# - Canonical handler tests
# - Integration tests
```

**Capture**:
- Total tests passing/failing
- Accuracy per category
- Any unexpected failures

**STOP if**: 
- Any category drops below 75% accuracy
- Regressions in non-targeted categories
- Integration tests failing

---

### Task 4.2: Accuracy Report (20 min)

**Generate comprehensive report**:

```markdown
# Final Accuracy Report - CORE-INTENT-ENHANCE #212

## Category Accuracy (Before → After)

| Category | Before | After | Target | Status |
|----------|--------|-------|--------|--------|
| IDENTITY | 76% | X% | ≥90% | ✅/❌ |
| GUIDANCE | 76.7% | X% | ≥90% | ✅/❌ |
| TEMPORAL | 96.7% | X% | ≥75% | ✅/❌ |
| STATUS | 96.7% | X% | ≥75% | ✅/❌ |
| PRIORITY | 100% | X% | ≥75% | ✅/❌ |
| EXECUTION | X% | X% | ≥75% | ✅/❌ |
| ANALYSIS | X% | X% | ≥75% | ✅/❌ |
| SYNTHESIS | X% | X% | ≥75% | ✅/❌ |
| STRATEGY | X% | X% | ≥75% | ✅/❌ |
| LEARNING | X% | X% | ≥75% | ✅/❌ |
| QUERY | X% | X% | ≥75% | ✅/❌ |
| CONVERSATION | X% | X% | ≥75% | ✅/❌ |
| UNKNOWN | X% | X% | ≥75% | ✅/❌ |

## Pre-Classifier Performance
- Hit rate: Before ~1% → After X%
- Target: ≥10% ✅/❌
- Performance: Xms for 10k queries ✅/❌

## Success Criteria Achievement
- ✅/❌ IDENTITY ≥90%
- ✅/❌ GUIDANCE ≥90%
- ✅/❌ Pre-classifier ≥10%
- ✅/❌ No regression (all >75%)
- ✅/❌ Performance maintained

## Overall Assessment
[Summary of improvements and remaining issues]
```

**Save as**: `dev/2025/10/10/phase4-final-accuracy-report.md`

---

### Task 4.3: Update Documentation (20 min)

**Update files**:

1. **Intent Classification Guide** (`docs/guides/intent-classification-guide.md`):
   - Add improved IDENTITY examples
   - Add improved GUIDANCE examples
   - Document new pre-classifier patterns
   - Update accuracy metrics

2. **ADR-032 Addendum** (if needed):
   - Note accuracy improvements
   - Document pattern additions
   - Update performance metrics

**Create**: `docs/guides/pre-classifier-patterns.md` (new)
```markdown
# Pre-Classifier Pattern Guide

## Purpose
Fast-path pattern matching for common queries to bypass LLM classification.

## Pattern Sets

### TEMPORAL Patterns
[List patterns with examples and reasoning]

### STATUS Patterns
[List patterns with examples and reasoning]

### PRIORITY Patterns
[List patterns with examples and reasoning]

## Adding New Patterns

### Guidelines
1. High-confidence patterns only (false positives worse than misses)
2. Test with 50+ variants
3. Check for false positives
4. Verify performance impact
5. Document reasoning

### Testing Patterns
[Code example for testing new patterns]

## Maintenance
- Review patterns monthly
- Remove patterns with high false positive rate
- Add patterns based on user query logs
```

---

### Phase 4 Deliverable

**Summary Report**: `dev/2025/10/10/phase4-validation-complete.md`

```markdown
# Phase 4: Validation Complete

## Test Results
- Total tests: X
- Passing: X
- Failing: X (if any, with analysis)

## Accuracy Achievements
- ✅ IDENTITY: X% (target ≥90%)
- ✅ GUIDANCE: X% (target ≥90%)
- ✅ Pre-classifier: X% hit rate (target ≥10%)

## Regression Check
[All categories maintaining >75%? ✅/❌]

## Documentation Updated
- ✅ Intent classification guide
- ✅ Pre-classifier pattern guide
- ✅ ADR-032 addendum (if needed)

## Ready for Phase Z
All acceptance criteria met, ready for commit and close.
```

---

## Phase Z: Commit, Push & Issue Closure (30 minutes)

**Agent**: Code Agent (commits) → Cursor Agent (push & issue update)  
**Goal**: Commit all changes, push to repository, update issue with evidence

### Task Z.1: Review All Changes (5 min)

**Code Agent**:
```bash
# Check what changed
git status

# Review diffs
git diff

# Expected changes:
# - services/intent_service/llm_classifier.py (or prompt files)
# - services/intent_service/pre_classifier.py
# - tests/intent/test_classification_accuracy.py (if new tests added)
# - docs/guides/intent-classification-guide.md
# - docs/guides/pre-classifier-patterns.md (new)
# - dev/2025/10/10/*.md (phase reports)
```

**Ensure**:
- All intended changes present
- No unintended changes
- Tests passing

**STOP if**: 
- Unexpected files changed
- Tests not passing
- Unclear what was modified

---

### Task Z.2: Create Commit (10 min)

**Code Agent**:

```bash
# Stage changes
git add services/intent_service/llm_classifier.py
git add services/intent_service/pre_classifier.py
git add tests/intent/test_classification_accuracy.py
git add docs/guides/intent-classification-guide.md
git add docs/guides/pre-classifier-patterns.md

# Create commit
git commit -m "feat(intent): improve IDENTITY/GUIDANCE accuracy and expand pre-classifier patterns

Classification Improvements:
- Enhance IDENTITY classifier from 76% to X% accuracy
- Enhance GUIDANCE classifier from 76.7% to X% accuracy
- Add capability/feature keyword patterns for IDENTITY
- Strengthen GUIDANCE vs STRATEGY disambiguation
- Add 50+ test queries per category

Pre-Classifier Expansion:
- Add TEMPORAL pattern set (calendar, time, schedule queries)
- Add STATUS pattern set (standup, progress, current work)
- Add PRIORITY pattern set (priority, urgent, focus queries)
- Improve hit rate from ~1% to X%
- Maintain <100ms performance for 10k queries

Testing:
- 50+ IDENTITY test queries (X% accuracy)
- 50+ GUIDANCE test queries (X% accuracy)
- Pre-classifier benchmark (X% hit rate)
- Full regression suite (all categories >75%)

Documentation:
- Update intent classification guide
- Add pre-classifier pattern guide
- Document pattern addition guidelines

Performance:
- Pre-classifier: <0.01ms per query
- No regression in LLM classification time
- No false positives detected

Fixes #212

Duration: ~X hours
Status: All acceptance criteria met
Follow-up to: GREAT-4F (ADR-032 production system)"
```

**Verify commit**:
```bash
git log -1 --stat
git log -1 --pretty=format:"%B"
```

---

### Task Z.3: Push Changes (5 min)

**Cursor Agent**:

```bash
# Verify tests before push
pytest tests/intent/ -v
# All tests must pass

# Push to remote
git push origin main

# Verify push
git log origin/main --oneline -1
```

**Evidence**:
```bash
$ git push origin main
Enumerating objects: X, done.
...
To github.com:username/piper-morgan.git
   abc1234..def5678  main -> main
```

---

### Task Z.4: Update Issue #212 (10 min)

**Cursor Agent** - Add completion comment to GitHub issue:

```markdown
## ✅ CORE-INTENT-ENHANCE Complete

**Completion Date**: October 10, 2025  
**Total Time**: ~X hours  
**Status**: All Acceptance Criteria Met

---

### Improvements Delivered

#### IDENTITY Classification
- **Before**: 76% accuracy
- **After**: X% accuracy
- **Target**: ≥90% ✅
- **Test Coverage**: 50+ capability question variants

**Changes**:
- Added capability/feature keyword patterns
- Enhanced IDENTITY vs QUERY disambiguation
- Added examples: "What can you do?", "What are your features?", etc.

**Evidence**:
```bash
$ pytest tests/intent/test_classification_accuracy.py::test_identity_accuracy -v
=========== X/Y passing (X% accuracy) ===========
```

#### GUIDANCE Classification
- **Before**: 76.7% accuracy
- **After**: X% accuracy
- **Target**: ≥90% ✅
- **Test Coverage**: 50+ advice/guidance query variants

**Changes**:
- Strengthened GUIDANCE vs STRATEGY disambiguation
- Added how-to/advice keyword patterns
- Added examples: "How should I...", "What's the best way...", etc.

**Evidence**:
```bash
$ pytest tests/intent/test_classification_accuracy.py::test_guidance_accuracy -v
=========== X/Y passing (X% accuracy) ===========
```

#### Pre-Classifier Expansion
- **Before**: ~1% hit rate
- **After**: X% hit rate
- **Target**: ≥10% ✅
- **Performance**: <100ms for 10k queries ✅

**Patterns Added**:
- **TEMPORAL**: Time, date, calendar, schedule queries
- **STATUS**: Standup, progress, current work queries
- **PRIORITY**: Priority, urgent, focus queries

**Evidence**:
```bash
$ python benchmark_pre_classifier.py
Pre-classifier hit rate: X%
Performance: Xms for 10,000 queries (Xms avg per query)
```

---

### Regression Testing

**All categories maintain >75% accuracy** ✅

| Category | Before | After | Status |
|----------|--------|-------|--------|
| IDENTITY | 76% | X% | ✅ |
| GUIDANCE | 76.7% | X% | ✅ |
| TEMPORAL | 96.7% | X% | ✅ |
| STATUS | 96.7% | X% | ✅ |
| PRIORITY | 100% | X% | ✅ |
| [Other categories...] | | | ✅ |

**Evidence**:
```bash
$ pytest tests/intent/test_classification_accuracy.py -v
=========== All X tests passing ===========
```

---

### Documentation Updated

- ✅ Intent Classification Guide (`docs/guides/intent-classification-guide.md`)
  - Added IDENTITY improvements
  - Added GUIDANCE improvements
  - Updated accuracy metrics

- ✅ Pre-Classifier Pattern Guide (`docs/guides/pre-classifier-patterns.md`)
  - NEW: Comprehensive pattern documentation
  - Pattern addition guidelines
  - Testing and maintenance procedures

---

### Acceptance Criteria

- ✅ IDENTITY accuracy ≥ 90% (50+ test queries)
- ✅ GUIDANCE accuracy ≥ 90% (50+ test queries)
- ✅ Pre-classifier hit rate ≥ 10%
- ✅ Pre-classifier patterns for TEMPORAL working
- ✅ Pre-classifier patterns for STATUS working
- ✅ Pre-classifier patterns for PRIORITY working
- ✅ No regression in other categories (all stay >75%)
- ✅ Performance maintained (<100ms for pre-classifier)
- ✅ Documentation updated with new patterns

---

### Files Modified

**Classification**:
- `services/intent_service/llm_classifier.py` (prompt enhancements)
- `services/intent_service/pre_classifier.py` (pattern additions)

**Testing**:
- `tests/intent/test_classification_accuracy.py` (if new tests added)

**Documentation**:
- `docs/guides/intent-classification-guide.md` (updated)
- `docs/guides/pre-classifier-patterns.md` (NEW)

**Reports**:
- `dev/2025/10/10/phase0-baseline-report.md`
- `dev/2025/10/10/phase1-identity-complete.md`
- `dev/2025/10/10/phase2-guidance-complete.md`
- `dev/2025/10/10/phase3-pre-classifier-complete.md`
- `dev/2025/10/10/phase4-final-accuracy-report.md`

---

### Impact

**User Experience**:
- ✅ Fewer mis-classifications for capability and advice questions
- ✅ Faster responses for common queries (1ms vs 2-3s)
- ✅ Better discovery of Piper's capabilities

**System Performance**:
- ✅ 10x improvement in pre-classifier hit rate
- ✅ Reduced LLM API calls for common queries
- ✅ Maintained fast response times (<100ms for patterns)

**Overall Quality**:
- Before: 89.3% overall canonical accuracy
- After: X% overall canonical accuracy
- Improvement: +X percentage points

---

### Ready For

- ✅ Sprint A1 completion
- ✅ Production deployment
- ✅ Alpha user testing

---

**Issue can be closed.** All acceptance criteria met, all tests passing, documentation complete.

---

*Completed: October 10, 2025*  
*Session Log: dev/2025/10/10/2025-10-10-0936-lead-sonnet-log.md*
```

---

### Task Z.5: Close Issue (2 min)

**Cursor Agent**:
- Add completion comment (from Z.4)
- Add label: `status: complete`
- Close issue

---

### Phase Z Deliverable

**Completion Summary**: `dev/2025/10/10/phaseZ-deployment-complete.md`

```markdown
# Phase Z: Deployment Complete

## Git Commit
- Commit hash: [hash]
- Files changed: X
- Lines added: +X
- Lines removed: -X

## Git Push
- Branch: main
- Remote: origin
- Status: ✅ Pushed successfully

## Issue Update
- Issue: #212
- Status: Closed
- Completion comment added: ✅
- All evidence linked: ✅

## Sprint A1 Status
- ✅ #145: Slack asyncio bug
- ✅ #216: Test caching (deferred)
- ✅ #217: LLM config & keychain
- ✅ #212: Intent classification accuracy

**Sprint A1: COMPLETE** 🎉

---

*Deployment completed: October 10, 2025*
```

---

## Summary & Anti-80% Checklist

### What We Built
- ✅ Improved IDENTITY classification (76% → 90%+)
- ✅ Improved GUIDANCE classification (76.7% → 90%+)
- ✅ Expanded pre-classifier patterns (1% → 10%+ hit rate)
- ✅ Maintained performance (<100ms)
- ✅ No regression in other categories

### What We Did NOT Build (Anti-80%)
- ❌ 100% accuracy (diminishing returns)
- ❌ Complex ML training pipelines (out of scope)
- ❌ New intent categories (not needed)
- ❌ Over-engineered pattern matching (maintainability risk)

### Time Estimate Validation
- Phase 0: 30-45 min (investigation)
- Phase 1: 1-2 hours (IDENTITY)
- Phase 2: 1-2 hours (GUIDANCE)
- Phase 3: 1-2 hours (pre-classifier)
- Phase 4: 1 hour (validation)
- Phase Z: 30 min (deployment)
- **Total**: 4.5-6.5 hours ✅ (matches estimate)

### Success Criteria
- [x] IDENTITY accuracy ≥ 90%
- [x] GUIDANCE accuracy ≥ 90%
- [x] Pre-classifier hit rate ≥ 10%
- [x] No regression (all >75%)
- [x] Performance maintained
- [x] Documentation complete

---

## Appendix: Agent Guidance

### When to STOP and Ask
1. **Architecture unclear**: If ADR-032 doesn't match actual code
2. **Files not found**: If expected files are in different locations
3. **Accuracy plateaus**: If 90% seems unachievable with current approach
4. **False positives**: If patterns cause mis-classifications
5. **Performance issues**: If pattern matching becomes slow
6. **Test failures**: If regression detected in other categories
7. **Ambiguous requirements**: If GUIDANCE vs STRATEGY boundary is unclear

### Context Check Questions
- "Is the classifier prompt in a separate file or embedded?"
- "Are there existing test query sets for IDENTITY/GUIDANCE?"
- "What's the current pre-classifier architecture?"
- "Should I add tests or use existing ones?"
- "Is the disambiguation guidance clear enough?"

### Evidence Standards
- Always provide terminal output (not summaries)
- Always show before/after metrics
- Always verify with actual test runs
- Always capture regression check results
- Always document reasoning for changes

---

**This gameplan follows yesterday's successful pattern**: Investigation → Phase work → Validation → Deployment, with anti-80% discipline and clear STOP conditions.

---

*Gameplan v1.0 - October 10, 2025, 10:04 AM*
