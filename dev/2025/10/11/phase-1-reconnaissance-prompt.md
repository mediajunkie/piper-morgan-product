# Phase -1: Reconnaissance - CORE-CRAFT-GAP

**Date**: October 11, 2025, 8:00 AM  
**Agents**: Code Agent + Cursor Agent (working together)  
**Duration**: 1 hour  
**Purpose**: Comprehensive handler inventory and infrastructure verification

---

## Mission

Use Serena MCP to create complete inventory of handlers with placeholders, verify infrastructure readiness, and provide PM with concrete numbers for Sub-Gameplan 1 execution planning.

**Critical**: This reconnaissance determines whether we can proceed with the gameplan as written or need adjustments.

---

## Task 1: Handler Inventory (30 min)

### Step 1.1: Find All Handler Files

```python
# Use Serena to locate handler files
mcp__serena__search_for_pattern(
    substring_pattern="handler",
    relative_path="services/",
    restrict_search_to_code_files=True
)

# Get handler directory structure
mcp__serena__get_directory_structure("services/handlers/")
```

**Questions to Answer**:
1. How many handler files exist?
2. What's the file organization? (One file per category? All in one file?)
3. Are handlers organized by intent category (EXECUTION, ANALYSIS, etc.)?

---

### Step 1.2: Identify All Handler Methods

```python
# Find all _handle_* methods
mcp__serena__search_for_pattern(
    substring_pattern="_handle_",
    relative_path="services/",
    restrict_search_to_code_files=True
)

# Get detailed view of handler implementations
mcp__serena__find_symbol(
    name_regex=".*Handler$",  # Find handler classes
    relative_path="services/handlers/",
    include_body=True
)
```

**For EACH handler method found, document**:
- Method name
- Which file it's in
- Approximate line count
- Intent category (EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, LEARNING)

---

### Step 1.3: Identify Placeholder Patterns

Search for sophisticated placeholder indicators:

```python
# Search for "IMPLEMENTATION IN PROGRESS"
mcp__serena__search_for_pattern(
    substring_pattern="IMPLEMENTATION IN PROGRESS",
    relative_path="services/",
    restrict_search_to_code_files=True
)

# Search for TODO markers
mcp__serena__search_for_pattern(
    substring_pattern="TODO",
    relative_path="services/handlers/",
    restrict_search_to_code_files=True
)

# Search for placeholder comments
mcp__serena__search_for_pattern(
    substring_pattern="placeholder",
    relative_path="services/handlers/",
    restrict_search_to_code_files=True
)
```

**For EACH placeholder found, document**:
- Handler method name
- Type of placeholder (TODO, IN PROGRESS, comment-only, etc.)
- Approximate work needed (trivial/moderate/substantial)

---

### Step 1.4: Categorize Handlers

**Create comprehensive inventory table**:

```markdown
## Handler Inventory

### EXECUTION Handlers
| Handler Method | File | Status | Placeholder Type | Estimated Work |
|----------------|------|--------|------------------|----------------|
| _handle_create_issue | handlers/execution.py | PLACEHOLDER | IN PROGRESS | 2 hours |
| _handle_update_issue | handlers/execution.py | PLACEHOLDER | IN PROGRESS | 2 hours |
| ... | ... | ... | ... | ... |

**EXECUTION Total**: X handlers, Y with placeholders

### ANALYSIS Handlers
| Handler Method | File | Status | Placeholder Type | Estimated Work |
|----------------|------|--------|------------------|----------------|
| ... | ... | ... | ... | ... |

**ANALYSIS Total**: X handlers, Y with placeholders

### SYNTHESIS Handlers
[Same format]

### STRATEGY Handlers
[Same format]

### LEARNING Handlers
[Same format]

---

## Overall Summary
- **Total handlers found**: X
- **Total with placeholders**: Y (Z%)
- **EXECUTION**: A handlers (B with placeholders)
- **ANALYSIS**: C handlers (D with placeholders)
- **SYNTHESIS**: E handlers (F with placeholders)
- **STRATEGY**: G handlers (H with placeholders)
- **LEARNING**: I handlers (J with placeholders)
```

---

## Task 2: Infrastructure Verification (15 min)

### Step 2.1: Verify HandlerResult Infrastructure

```python
# Find HandlerResult class
mcp__serena__find_symbol(
    name_path="HandlerResult",
    relative_path="services/",
    include_body=True
)
```

**Questions to Answer**:
1. Does `HandlerResult` class exist?
2. Where is it defined?
3. Does it have `implemented` field?
4. If not, where should we add it?

---

### Step 2.2: Verify Service Integrations

```bash
# Check which services are configured
cat .env | grep -E "GITHUB_TOKEN|SLACK_TOKEN|NOTION_TOKEN" | wc -l

# Verify service files exist
ls -la services/integrations/github_service.py
ls -la services/integrations/slack_service.py
ls -la services/integrations/notion_service.py

# Check ServiceRegistry
grep -r "ServiceRegistry" services/ --include="*.py" | head -5
```

**Questions to Answer**:
1. Which external services are configured? (GitHub, Slack, Notion, others?)
2. Are authentication tokens present in .env?
3. Does ServiceRegistry exist and work?
4. Are service files properly structured?

---

### Step 2.3: Verify Test Infrastructure

```bash
# Find handler tests
find tests/ -name "*handler*" -type f

# Check for integration test markers
grep -r "@pytest.mark.integration" tests/ --include="*.py" | wc -l

# Verify test configuration
cat pytest.ini | grep -A5 "markers"
```

**Questions to Answer**:
1. Do handler tests exist?
2. Are integration test markers configured?
3. Can we run tests with `pytest tests/handlers/ -v`?
4. What's the current test pass rate?

---

### Step 2.4: Verify Logging Infrastructure

```bash
# Check logging configuration
cat config/logging.yaml || cat config/logging.json || echo "No logging config found"

# Verify log directory
ls -la logs/ 2>/dev/null || echo "No logs directory"

# Check logger usage in handlers
grep -r "logger" services/handlers/ --include="*.py" | head -5
```

**Questions to Answer**:
1. Is logging configured?
2. Where do logs go?
3. Are handlers using logger properly?

---

## Task 3: Identify Simplest EXECUTION Handler (15 min)

### Step 3.1: Analyze EXECUTION Handlers

For each EXECUTION handler with placeholder:
1. **Count dependencies**: How many services does it need?
2. **Check complexity**: How many steps in the workflow?
3. **Review parameters**: Simple or complex parameter validation?
4. **Check error cases**: How many error conditions?

### Step 3.2: Rank by Simplicity

Create ranking from simplest to most complex:

```markdown
## EXECUTION Handler Complexity Ranking

1. **_handle_create_task** (SIMPLEST)
   - Dependencies: 1 (task service)
   - Steps: 3 (validate, create, return)
   - Parameters: 2 (title, description)
   - Errors: 2 cases
   - Estimated time: 1.5 hours

2. **_handle_create_issue**
   - Dependencies: 1 (GitHub service)
   - Steps: 4 (validate, auth, create, return)
   - Parameters: 3 (title, body, labels)
   - Errors: 3 cases
   - Estimated time: 2 hours

[Continue for all EXECUTION handlers...]
```

**Recommendation**: Start with #1 (simplest) for pattern establishment

---

## Task 4: STOP Condition Evaluation

### Check for Blockers

**STOP and report to PM if ANY of these are true**:

- [ ] Handler files don't exist or are in unexpected location
- [ ] Handler count is significantly different from estimate (20-25)
- [ ] HandlerResult infrastructure missing and complex to add
- [ ] Service integrations not configured (no tokens in .env)
- [ ] Test infrastructure broken or missing
- [ ] Handlers are more complex than expected (need redesign)
- [ ] Can't identify a "simplest" EXECUTION handler

**If any blockers found**: Document clearly and await PM guidance before proceeding

---

## Deliverables

### Primary Deliverable: Reconnaissance Report

**Create**: `dev/2025/10/11/phase-1-reconnaissance-report.md`

```markdown
# Phase -1 Reconnaissance Report - CORE-CRAFT-GAP

**Date**: October 11, 2025  
**Agents**: Code Agent + Cursor Agent  
**Duration**: [actual time]

---

## Executive Summary

[2-3 sentence summary of findings]

---

## Handler Inventory

[Complete table from Task 1.4]

---

## Infrastructure Status

### HandlerResult
- Status: [Exists/Missing/Needs Enhancement]
- Location: [path]
- Has `implemented` field: [Yes/No]
- Action needed: [None/Add field/Create class]

### Service Integrations
- GitHub: [Configured/Not Configured]
- Slack: [Configured/Not Configured]
- Notion: [Configured/Not Configured]
- Other: [List]

### Test Infrastructure
- Handler tests: [X tests found]
- Integration markers: [Configured/Not Configured]
- Current pass rate: [X%]

### Logging
- Configuration: [Found/Missing]
- Log location: [path]
- Handler usage: [Proper/Needs Fix]

---

## Simplest EXECUTION Handler

**Recommendation**: Start with `_handle_[X]`

**Rationale**:
- Fewest dependencies (X)
- Simplest workflow (Y steps)
- Basic parameters (Z)
- Clear error cases (A)

**Estimated time**: B hours

---

## STOP Conditions

[List any blockers found, or "None - ready to proceed"]

---

## Recommendations for Sub-Gameplan 1

1. [Specific recommendation based on findings]
2. [Another recommendation]
3. [Etc.]

---

## Evidence

### Serena Audit Trail
```bash
[All Serena commands used and their outputs]
```

### File Listings
```bash
[Relevant file listings]
```

### Configuration Checks
```bash
[Environment and config verification]
```

---

**Status**: [Ready to proceed / Need PM guidance]
```

---

## Success Criteria

- [ ] Complete handler inventory created
- [ ] All placeholders identified and categorized
- [ ] Infrastructure status verified
- [ ] Simplest EXECUTION handler identified
- [ ] STOP conditions evaluated
- [ ] Reconnaissance report created
- [ ] Recommendations provided

---

## Coordination Protocol

**Code Agent**: Focus on handler inventory (Tasks 1 & 3)  
**Cursor Agent**: Focus on infrastructure (Task 2)  
**Both**: Collaborate on simplest handler identification and report creation

**Communication**: Report findings to each other as you go, compile into single report at end

---

## After Reconnaissance

1. **Report to PM**: Present reconnaissance report
2. **Wait for approval**: Don't proceed to Phase 1 without authorization
3. **Adjust gameplan if needed**: PM may modify approach based on findings
4. **Create Phase 1 prompt**: Based on actual handler found, not assumptions

---

*Phase -1 Reconnaissance prompt created: October 11, 2025, 8:00 AM*  
*Estimated duration: 1 hour*  
*Critical for accurate Sub-Gameplan 1 execution*
