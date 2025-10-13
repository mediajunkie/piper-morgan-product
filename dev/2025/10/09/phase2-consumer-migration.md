# Phase 2: Consumer Migration to ServiceRegistry

**Issue**: #217 - CORE-LLM-CONFIG (Refactoring)
**Phase**: 2 of 3 - Consumer Updates
**Agent**: Code Agent
**Date**: October 9, 2025, 6:48 PM
**Time Estimate**: 45-60 minutes
**Anti-80% Protocol**: ENFORCED

---

## Mission

Update all 13 LLM consumers to use `ServiceRegistry.get_llm()` instead of direct imports. Verify EACH consumer with evidence. 100% completion required.

---

## Context from Phase 1

**✅ Phase 1 Complete**:
- ServiceRegistry created
- LLMDomainService created
- Initialization in main.py working
- 58/58 tests passing

**Now**: Update all consumers to use the new architecture

---

## Anti-80% Success Criteria

### Consumer Migration Checklist

**CRITICAL**: Each consumer must have ALL 4 checkboxes marked:

```
Consumer                              | Updated | Imports | Tested | Works
------------------------------------- | ------- | ------- | ------ | -----
web/app.py                            | [ ]     | [ ]     | [ ]    | [ ]
services/intent/intent_service.py     | [ ]     | [ ]     | [ ]    | [ ]
services/intent/classification.py     | [ ]     | [ ]     | [ ]    | [ ]
services/knowledge_graph.py           | [ ]     | [ ]     | [ ]    | [ ]
services/integrations/github/X.py     | [ ]     | [ ]     | [ ]    | [ ]
services/integrations/github/Y.py     | [ ]     | [ ]     | [ ]    | [ ]
services/orchestration/engine.py      | [ ]     | [ ]     | [ ]    | [ ]
services/domain/work_item_extractor   | [ ]     | [ ]     | [ ]    | [ ]
[Consumer 9]                          | [ ]     | [ ]     | [ ]    | [ ]
[Consumer 10]                         | [ ]     | [ ]    | [ ]
[Consumer 11]                         | [ ]     | [ ]     | [ ]    | [ ]
[Consumer 12]                         | [ ]     | [ ]     | [ ]    | [ ]
[Consumer 13]                         | [ ]     | [ ]     | [ ]    | [ ]
------------------------------------- | ------- | ------- | ------ | -----
TOTAL: 0/52 checkmarks = 0% complete
```

**Each Column Means**:
- **Updated**: File modified to use ServiceRegistry
- **Imports**: Correct imports added, old imports removed
- **Tested**: Individual verification command run
- **Works**: Evidence provided (output, no errors)

**100% = 52/52 checkmarks**

---

## Phase 2 Tasks

### Task 1: Identify All 13 Consumers (5 min)

**Use Serena** to find all consumers:
```python
# Find all imports of llm_client or LLMConfigService
mcp__serena__search_for_pattern(
    substring_pattern="from services.llm",
    relative_path="services",
    restrict_search_to_code_files=True
)

mcp__serena__search_for_pattern(
    substring_pattern="from services.llm",
    relative_path="web",
    restrict_search_to_code_files=True
)
```

**Create Complete List**:
```markdown
## All 13 Consumers Found

1. [file path] - Line [X]: imports [what]
2. [file path] - Line [X]: imports [what]
...
13. [file path] - Line [X]: imports [what]
```

**Acceptance**:
- [ ] All 13 consumers identified with exact file paths
- [ ] Line numbers for each import statement
- [ ] What each file currently imports

---

### Task 2: Update Each Consumer (30-40 min)

**For EACH of the 13 consumers, execute this pattern**:

#### Step 1: Read Current Usage
```python
# Use Serena to understand current usage
mcp__serena__get_symbols_overview("[consumer_file].py")

# Find the specific usage
mcp__serena__find_symbol(
    name_path="ClassName/method_using_llm",
    relative_path="[consumer_file].py",
    include_body=True
)
```

#### Step 2: Update Import
```python
# Use Serena to replace import
mcp__serena__replace_symbol_body(
    name_path="[old_import]",
    new_body="""from services.service_registry import ServiceRegistry"""
)
```

**Old Pattern** (remove):
```python
from services.llm.clients import llm_client
# or
from services.config.llm_config_service import LLMConfigService
```

**New Pattern** (add):
```python
from services.service_registry import ServiceRegistry
```

#### Step 3: Update Usage Pattern

**Old usage patterns to replace**:
```python
# Pattern 1: Direct llm_client
result = await llm_client.complete(prompt)

# Pattern 2: Direct config service
config = LLMConfigService()
key = config.get_api_key("openai")
```

**New usage pattern**:
```python
# Get LLM service from registry
llm_service = ServiceRegistry.get_llm()

# Use domain service
result = await llm_service.generate(
    prompt=prompt,
    task_type="general"  # or "coding", "research"
)
```

#### Step 4: Verify Each Consumer

**After updating each file, verify**:
```bash
# Test 1: Import works
python -c "from [consumer_module] import [ClassName]; print('✅ Import works')"

# Test 2: File has no old imports
grep -n "from services.llm" [consumer_file].py
# Expected: No output (or only comments)

# Test 3: File has new import
grep -n "ServiceRegistry" [consumer_file].py
# Expected: Import line found

# Test 4: Usage updated
grep -n "ServiceRegistry.get_llm()" [consumer_file].py
# Expected: At least one usage found
```

#### Step 5: Mark Checkboxes

After each consumer verified, update the checklist:
```
services/intent/intent_service.py     | [✓]     | [✓]     | [✓]    | [✓]
```

---

### Task 3: Integration Testing (10 min)

**After ALL 13 consumers updated**:

```bash
# Test 1: All unit tests still pass
pytest tests/ -v
# Expected: 58/58 passing (no regressions)

# Test 2: Server starts
python main.py &
sleep 5
# Expected: No errors, validation messages appear

# Test 3: Health check
curl http://localhost:8001/health
# Expected: 200 OK

# Kill server
pkill -f "python main.py"

# Test 4: No old imports remain
grep -r "from services.llm.clients import" services/ web/ --include="*.py"
# Expected: No output (all removed)

grep -r "from services.config.llm_config_service import" services/ web/ --include="*.py" | grep -v test | grep -v "services/domain/llm_domain_service"
# Expected: Only in domain service and tests
```

---

## Evidence Format (MANDATORY)

### For Each Consumer

```markdown
### Consumer X: [file path]

**Old Pattern Found**:
Line [X]: `from services.llm.clients import llm_client`
Line [Y]: `result = await llm_client.complete(prompt)`

**New Pattern Applied**:
Line [X]: `from services.service_registry import ServiceRegistry`
Line [Y]: `llm = ServiceRegistry.get_llm()`
Line [Z]: `result = await llm.generate(prompt, task_type="general")`

**Verification**:
```bash
$ python -c "from services.intent.intent_service import IntentService; print('✅')"
✅

$ grep -n "from services.llm" services/intent/intent_service.py
# No output ✅

$ grep -n "ServiceRegistry" services/intent/intent_service.py
12: from services.service_registry import ServiceRegistry
45:     llm = ServiceRegistry.get_llm()
```

**Checklist**:
- [✓] Updated
- [✓] Imports correct
- [✓] Tested
- [✓] Works
```

**Repeat this for ALL 13 consumers**

---

## Final Evidence Report

At the end, provide:

```markdown
# Phase 2 Completion Report

## Consumer Migration: 52/52 Checkmarks (100%)

Consumer                              | Updated | Imports | Tested | Works
------------------------------------- | ------- | ------- | ------ | -----
web/app.py                            | [✓]     | [✓]     | [✓]    | [✓]
services/intent/intent_service.py     | [✓]     | [✓]     | [✓]    | [✓]
[... all 13 consumers ...]
------------------------------------- | ------- | ------- | ------ | -----
TOTAL: 52/52 checkmarks = 100% ✅

## Integration Test Results

```bash
$ pytest tests/ -v
===== 58 passed in 2.34s =====

$ python main.py
[startup logs showing initialization]
✅ Server started successfully

$ curl http://localhost:8001/health
{"status": "healthy"}

$ grep -r "from services.llm.clients import" services/ web/
# No output ✅ (all migrations complete)
```

## Files Modified

1. [file path] - [lines changed]
2. [file path] - [lines changed]
...
13. [file path] - [lines changed]

## Breaking Changes: NONE

- All existing functionality preserved
- All tests passing
- No API changes
- Zero regression

## Ready for Phase 3: YES ✅
```

---

## Success Criteria

**Phase 2 is NOT complete unless**:
- [ ] All 13 consumers identified with evidence
- [ ] All 13 consumers updated (13/13)
- [ ] All 13 consumers verified individually (13/13)
- [ ] All 52 checkboxes marked (52/52 = 100%)
- [ ] Integration tests pass (58/58)
- [ ] Server starts successfully
- [ ] No old imports remain anywhere
- [ ] Evidence report provided for EACH consumer

**Anti-80% Enforcement**: 99% = FAILURE. Only 100% = SUCCESS.

---

## STOP Conditions

If you encounter:
- Consumer with complex LLM usage pattern
- Circular import issues
- Test failures
- Unclear usage pattern

**STOP and document** - do not skip, do not assume, do not approximate.

---

## Time Breakdown

| Task | Description | Time |
|------|-------------|------|
| 1 | Identify all consumers | 5 min |
| 2 | Update 13 consumers (4 min each) | 40 min |
| 3 | Integration testing | 10 min |
| Final | Evidence report | 5 min |

**Total**: 60 minutes with rigorous verification

---

## Tips for Efficiency

1. **Use Serena** for all code operations
2. **Verify continuously** - after each consumer
3. **Use parallel sub-agents** if beneficial
4. **Document evidence** as you go (not at end)
5. **Be thorough** - this is foundational infrastructure

---

**100% completion required. No shortcuts. Anti-80% protocol enforced.**

---

*Phase 2 implementation - October 9, 2025, 6:48 PM*
