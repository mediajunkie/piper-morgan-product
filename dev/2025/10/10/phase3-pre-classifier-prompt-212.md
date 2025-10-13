# Phase 3: Pre-Classifier Pattern Expansion - CORE-INTENT-ENHANCE #212

**Issue**: #212 - CORE-INTENT-ENHANCE: Classification Accuracy & Pre-Classifier Optimization  
**Phase**: 3 - Pre-Classifier Pattern Expansion  
**Agent**: Code Agent  
**Date**: October 10, 2025, 1:53 PM  
**Time Estimate**: 1-2 hours  
**Prerequisites**: Phase 1 ✅ (IDENTITY 100%), Phase 2 ✅ (GUIDANCE 93.3%)

---

## Mission

Expand pre-classifier pattern coverage from ~60 patterns to 100+ patterns, improving hit rate from ~1% to 10%+. This enables fast-path routing (1ms vs 2-3s) for common queries.

**Success Criteria**:
- Hit rate ≥ 10% on representative query set
- No false positives detected
- Performance maintained (<100ms for 10k queries)
- Patterns added for TEMPORAL, STATUS, PRIORITY categories

---

## Context: Pre-Classifier Purpose

**Architecture** (from ADR-032):
```
User Input → Pre-Classifier (regex patterns)
                 ↓
           Hit? → Canonical Handler (1ms)
                 ↓
           Miss? → LLM Classifier (2-3s)
```

**Why This Matters**:
- **Speed**: 1ms vs 2000-3000ms (2000x faster)
- **Cost**: No LLM API call for pattern matches
- **Experience**: Instant responses for common queries

**Safety**: False positives worse than misses (falls back to LLM)

**Current State** (from Phase 0):
- ~60 existing patterns
- ~1% hit rate (very conservative)
- Mostly TEMPORAL patterns

---

## Task 3.1: Review Current Pre-Classifier (15 min)

### Use Serena to Understand Structure

```python
# Get overview of pre-classifier
mcp__serena__get_symbols_overview("services/intent_service/pre_classifier.py")

# Find the PreClassifier class
mcp__serena__find_symbol(
    name_path="PreClassifier",
    relative_path="services/intent_service/pre_classifier.py",
    include_body=True
)

# Look for pattern definitions
mcp__serena__search_for_pattern(
    substring_pattern="PATTERN",
    relative_path="services/intent_service/pre_classifier.py",
    restrict_search_to_code_files=True
)
```

### Questions to Answer

1. **How are patterns defined?**
   - Regex? Keywords? Both?
   - Where are they stored?
   - How are they organized?

2. **What's the matching logic?**
   - Case-sensitive? Case-insensitive?
   - Word boundaries enforced?
   - Pattern precedence?

3. **Current pattern coverage?**
   - Which categories have patterns?
   - How many patterns per category?
   - Any notable gaps?

4. **How is hit rate measured?**
   - Existing tests?
   - Benchmark script?
   - Metrics collected?

### Deliverable

```markdown
## Task 3.1: Pre-Classifier Structure Analysis

### Current Architecture
- File: [path]
- Pattern format: [regex/keywords/both]
- Matching logic: [description]
- Case handling: [sensitive/insensitive]

### Current Pattern Coverage
- Total patterns: ~60
- TEMPORAL: X patterns
- STATUS: Y patterns (if any)
- PRIORITY: Z patterns (if any)
- IDENTITY: A patterns (if any)
- GUIDANCE: B patterns (if any)

### Pattern Organization
[How patterns are defined - constants? dict? class variables?]

### Hit Rate Measurement
[How hit rate is currently measured]

### Evidence
```bash
[Serena commands and outputs]
```
```

---

## Task 3.2: Add TEMPORAL Patterns (20 min)

**Goal**: Comprehensive TEMPORAL pattern coverage for instant time/calendar queries

### Pattern Categories to Add

**Time Queries**:
```python
TEMPORAL_TIME_PATTERNS = [
    r'\b(what|when).{0,10}(time|hour|minute)\b',
    r'\bwhat.{0,10}(time is it|the time)\b',
    r'\bcurrent time\b',
    r'\btime now\b',
    r'\btime is\b',
]
```

**Date Queries**:
```python
TEMPORAL_DATE_PATTERNS = [
    r'\b(what|when).{0,10}(day|date|month|year)\b',
    r'\bwhat day (is it|today)\b',
    r'\bwhat.{0,10}date\b',
    r'\btoday.{0,10}date\b',
    r'\bcurrent date\b',
]
```

**Calendar/Schedule Queries**:
```python
TEMPORAL_CALENDAR_PATTERNS = [
    r'\b(calendar|schedule|appointment|meeting)s?\b',
    r'\b(next|upcoming|today|tomorrow).{0,10}(meeting|appointment|event)\b',
    r'\bmy (calendar|schedule)\b',
    r'\bwhen (is|am) (my|i)\b',
    r'\bshow.{0,10}(calendar|schedule)\b',
]
```

**Relative Time**:
```python
TEMPORAL_RELATIVE_PATTERNS = [
    r'\b(today|tomorrow|yesterday)\b',
    r'\b(this|next|last) (week|month|year)\b',
    r'\b(tonight|this morning|this afternoon)\b',
]
```

### Implementation Approach

1. **Find where patterns are defined** (from Task 3.1)
2. **Add new pattern sets** following existing format
3. **Ensure case-insensitive matching** (likely `re.IGNORECASE`)
4. **Test with sample queries**:
   ```python
   test_queries = [
       "what time is it",
       "what's the date today",
       "show me my calendar",
       "when is my next meeting",
       "what day is it",
   ]
   ```

### STOP Conditions

**STOP and ask if**:
- Pattern format is complex or unclear
- False positives detected in testing
- Existing TEMPORAL patterns are comprehensive already
- Pattern matching logic needs modification

### Deliverable

```markdown
## Task 3.2: TEMPORAL Patterns Added

### Patterns Added
- Time queries: X patterns
- Date queries: Y patterns
- Calendar/schedule: Z patterns
- Relative time: A patterns
- **Total new TEMPORAL patterns**: B

### Test Results
```python
# Test each pattern category
[Show test code and results]
```

### Sample Matches
- "what time is it" → TEMPORAL ✅
- "what's the date" → TEMPORAL ✅
- "show my calendar" → TEMPORAL ✅
- [etc.]

### False Positive Check
[Any queries that shouldn't match but do?]

### Evidence
```bash
[Terminal output showing tests]
```
```

---

## Task 3.3: Add STATUS Patterns (20 min)

**Goal**: Comprehensive STATUS pattern coverage for instant work status queries

### Pattern Categories to Add

**Work Status**:
```python
STATUS_WORK_PATTERNS = [
    r'\b(standup|stand-up|stand up)\b',
    r'\bstatus (update|report)\b',
    r'\b(working on|working with)\b',
    r'\bcurrent (task|work|project)\b',
    r'\bmy (work|tasks|projects)\b',
    r'\bwhat am i (working|doing)\b',
]
```

**Progress Queries**:
```python
STATUS_PROGRESS_PATTERNS = [
    r'\bmy progress\b',
    r'\bprogress (on|report|update)\b',
    r'\bhow.{0,10}(going|progressing)\b',
    r'\bstatus of\b',
]
```

**Current Work**:
```python
STATUS_CURRENT_PATTERNS = [
    r'\bcurrent (issue|ticket|task|pr|pull request)\b',
    r'\bworking on (issue|ticket|pr)\b',
    r'\bwhat.{0,10}working on\b',
]
```

### Implementation Approach

Same as Task 3.2:
1. Add pattern sets following existing format
2. Test with sample queries
3. Check for false positives

**Test queries**:
```python
test_queries = [
    "standup",
    "what am i working on",
    "my progress",
    "current task",
    "status update",
]
```

### Deliverable

```markdown
## Task 3.3: STATUS Patterns Added

### Patterns Added
- Work status: X patterns
- Progress queries: Y patterns
- Current work: Z patterns
- **Total new STATUS patterns**: A

### Test Results
[Sample matches and results]

### False Positive Check
[Any issues?]

### Evidence
```bash
[Terminal output]
```
```

---

## Task 3.4: Add PRIORITY Patterns (20 min)

**Goal**: Comprehensive PRIORITY pattern coverage for instant priority/focus queries

### Pattern Categories to Add

**Priority Queries**:
```python
PRIORITY_BASIC_PATTERNS = [
    r'\b(priority|priorities)\b',
    r'\b(top|highest|urgent|important|critical) (priority|task|item)\b',
    r'\bhighest priority\b',
    r'\btop (priority|priorities|task|tasks)\b',
]
```

**Focus Queries**:
```python
PRIORITY_FOCUS_PATTERNS = [
    r'\bfocus on\b',
    r'\bwhat should i (focus|work on|do|prioritize)\b',
    r'\bwhere should i (start|begin|focus)\b',
    r'\bwhat.{0,10}next\b',
]
```

**Urgent Items**:
```python
PRIORITY_URGENT_PATTERNS = [
    r'\b(urgent|critical|important) (items?|tasks?|work)\b',
    r'\bwhat.{0,10}(urgent|critical)\b',
    r'\bmost (important|urgent|critical)\b',
]
```

### Test Queries

```python
test_queries = [
    "what are my priorities",
    "top priority",
    "what should i focus on",
    "urgent items",
    "what's most important",
]
```

### Deliverable

```markdown
## Task 3.4: PRIORITY Patterns Added

### Patterns Added
- Priority queries: X patterns
- Focus queries: Y patterns
- Urgent items: Z patterns
- **Total new PRIORITY patterns**: A

### Test Results
[Sample matches and results]

### False Positive Check
[Any issues?]

### Evidence
```bash
[Terminal output]
```
```

---

## Task 3.5: Measure Hit Rate Improvement (20 min)

**Goal**: Verify hit rate has improved from ~1% to ≥10%

### Create or Update Benchmark

**If benchmark script exists**, run it:
```bash
python scripts/benchmark_pre_classifier.py
```

**If not**, create simple benchmark:
```python
# benchmark_pre_classifier.py
from services.intent_service.pre_classifier import PreClassifier

pre_classifier = PreClassifier()

# Representative common queries (100+ queries covering all categories)
common_queries = [
    # TEMPORAL
    "what time is it",
    "what's the date",
    "show my calendar",
    "when is my next meeting",
    
    # STATUS
    "standup",
    "what am i working on",
    "my progress",
    
    # PRIORITY
    "what are my priorities",
    "what should i focus on",
    
    # IDENTITY
    "what can you do",
    
    # GUIDANCE
    "how do i create an issue",
    
    # Should NOT match (workflow categories)
    "create an issue for bug",
    "analyze these commits",
    "generate a report",
    # ... add 80+ more diverse queries
]

hits = 0
total = len(common_queries)
hit_details = []

for query in common_queries:
    result = pre_classifier.classify(query)
    if result is not None:  # Hit
        hits += 1
        hit_details.append(f"✓ '{query}' → {result}")
    else:
        hit_details.append(f"✗ '{query}' → (LLM fallback)")

hit_rate = (hits / total) * 100

print(f"\n{'='*60}")
print(f"Pre-Classifier Hit Rate Benchmark")
print(f"{'='*60}")
print(f"Total queries: {total}")
print(f"Pattern hits: {hits}")
print(f"LLM fallback: {total - hits}")
print(f"Hit rate: {hit_rate:.1f}%")
print(f"{'='*60}\n")

# Show first 20 results
print("Sample results:")
for detail in hit_details[:20]:
    print(detail)

# Target check
if hit_rate >= 10.0:
    print(f"\n✅ SUCCESS: Hit rate {hit_rate:.1f}% exceeds 10% target")
else:
    print(f"\n⚠️  NEEDS WORK: Hit rate {hit_rate:.1f}% below 10% target")
```

### Representative Query Set

**Critical**: Use realistic, diverse queries that represent actual usage:
- 20-30% TEMPORAL queries (common)
- 15-20% STATUS queries (common in standup)
- 10-15% PRIORITY queries (common in planning)
- 10% IDENTITY queries
- 10% GUIDANCE queries
- 30-35% workflow queries that should NOT match (EXECUTION, ANALYSIS, etc.)

### Target

**Hit rate ≥ 10%** on representative query set

### STOP Conditions

**STOP and ask if**:
- Hit rate still below 5% after pattern additions
- False positives detected (workflow queries matching)
- Need guidance on representative query selection

### Deliverable

```markdown
## Task 3.5: Hit Rate Improvement Measurement

### Benchmark Script
[Created new? Used existing? Location?]

### Test Query Set
- Total queries: X
- TEMPORAL: Y queries
- STATUS: Z queries
- PRIORITY: A queries
- Other categories: B queries
- Workflow (should not match): C queries

### Results

```bash
[FULL terminal output from benchmark]
```

### Hit Rate Analysis
- Before: ~1%
- After: X%
- Improvement: +Y percentage points
- Target: ≥10% ✅/⚠️

### Hit Distribution
- TEMPORAL hits: X
- STATUS hits: Y
- PRIORITY hits: Z
- Other: A
- False positives: B (should be 0)

### Sample Matches
[Show 10-15 example queries with their classifications]

### Status
- ✅ Hit rate target met (≥10%)
- ✅ No false positives detected
- Ready for Phase 4 validation
```

---

## Task 3.6: Performance Verification (15 min)

**Goal**: Verify pre-classifier maintains <100ms performance for 10k queries

### Performance Test

```python
# benchmark_performance.py
import time
from services.intent_service.pre_classifier import PreClassifier

pre_classifier = PreClassifier()

# Sample queries (mix of matches and misses)
queries = [
    "what time is it",
    "standup",
    "priorities",
    "create an issue",  # should miss
    # ... more queries
] * 1000  # Repeat to get 10k+ queries

start = time.time()
for query in queries:
    pre_classifier.classify(query)
end = time.time()

total_time_ms = (end - start) * 1000
avg_time_ms = total_time_ms / len(queries)

print(f"Performance Test Results:")
print(f"Total queries: {len(queries)}")
print(f"Total time: {total_time_ms:.2f}ms")
print(f"Average per query: {avg_time_ms:.4f}ms")
print(f"Target: <100ms total for 10k queries")

if total_time_ms < 100:
    print(f"✅ PASS: {total_time_ms:.2f}ms (target: <100ms)")
else:
    print(f"⚠️  SLOW: {total_time_ms:.2f}ms (target: <100ms)")
```

### Target

**<100ms for 10,000 queries** (or <0.01ms per query)

### STOP Conditions

**STOP and ask if**:
- Performance degrades beyond 100ms
- Pattern matching causing slowdown
- Need optimization guidance

### Deliverable

```markdown
## Task 3.6: Performance Verification

### Performance Test Results

```bash
[Terminal output from performance test]
```

### Metrics
- Test queries: 10,000
- Total time: Xms
- Average per query: Xms
- Target: <100ms ✅/⚠️

### Analysis
[Performance acceptable? Any concerns?]

### Evidence
Performance maintained within acceptable bounds for production use.
```

---

## Phase 3 Final Deliverable

**Create**: `dev/2025/10/10/phase3-pre-classifier-complete.md`

```markdown
# Phase 3: Pre-Classifier Expansion Complete

**Date**: October 10, 2025  
**Issue**: #212 (also closes GREAT-4A gap)  
**Agent**: Code Agent  
**Duration**: [actual time]

---

## Summary

Expanded pre-classifier pattern coverage from ~60 to X patterns, improving hit rate from ~1% to Y%.

---

## Patterns Added

### TEMPORAL Patterns
[Task 3.2 content]

### STATUS Patterns
[Task 3.3 content]

### PRIORITY Patterns
[Task 3.4 content]

### Total Pattern Growth
- Before: ~60 patterns
- After: X patterns
- Growth: +Y patterns (+Z%)

---

## Hit Rate Improvement

[Task 3.5 content]

---

## Performance

[Task 3.6 content]

---

## Files Modified

- `services/intent_service/pre_classifier.py`
- `scripts/benchmark_pre_classifier.py` (if created)
- `scripts/benchmark_performance.py` (if created)

---

## Verification Checklist

- ✅ TEMPORAL patterns added and tested
- ✅ STATUS patterns added and tested
- ✅ PRIORITY patterns added and tested
- ✅ Hit rate ≥10% achieved
- ✅ No false positives detected
- ✅ Performance <100ms for 10k queries
- ✅ Full terminal evidence captured

---

## Next Steps

Phase 4: System validation
- Full regression testing
- Documentation updates
- Final accuracy report

---

**Status**: ✅ Phase 3 complete, ready for Phase 4
```

---

## Success Criteria

- [ ] TEMPORAL patterns added (comprehensive coverage)
- [ ] STATUS patterns added (comprehensive coverage)
- [ ] PRIORITY patterns added (comprehensive coverage)
- [ ] Hit rate ≥ 10% on representative queries
- [ ] No false positives detected
- [ ] Performance maintained (<100ms for 10k queries)
- [ ] Full evidence captured (terminal output)
- [ ] Completion report created

---

## Important Notes

### On Pattern Design

**Good patterns** (specific, low false positive risk):
- `r'\bwhat time is it\b'` ✅
- `r'\bstandup\b'` ✅
- `r'\bpriorities\b'` ✅

**Risky patterns** (too broad, high false positive risk):
- `r'\bwhat\b'` ❌ (matches everything)
- `r'\bdo\b'` ❌ (matches too much)
- `r'\bhelp\b'` ⚠️ (might match help requests for other things)

**Principle**: Conservative patterns are better than risky ones. Miss → LLM fallback (acceptable). False positive → wrong handler (bad).

### On False Positives

**Critical**: A false positive is worse than a miss.
- Miss: User waits 2-3s for LLM (acceptable)
- False positive: User gets wrong response (bad UX)

**Always test** workflow queries (EXECUTION, ANALYSIS, SYNTHESIS) to ensure they DON'T match.

### On Evidence

**Capture full terminal output**, not summaries:
```bash
$ python scripts/benchmark_pre_classifier.py
[COMPLETE OUTPUT HERE]
```

---

## After Phase 3 Completion

1. **Create completion report** ✅
2. **Update session log** ✅
3. **STOP and await authorization** ⏸️
4. **Do NOT proceed to Phase 4** without approval

---

*Phase 3 prompt created: October 10, 2025, 1:53 PM*  
*Time estimate: 1-2 hours*  
*Next: Phase 4 (validation) after Phase 3 approval*
