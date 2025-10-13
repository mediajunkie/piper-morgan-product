# Phase 0: Infrastructure Verification for LLM Config Refactoring

**Issue**: #217 - CORE-LLM-CONFIG (Refactoring)
**Agent**: Code Agent
**Task Type**: Investigation (Phase 0)
**Date**: October 9, 2025, 5:13 PM
**Time Estimate**: 15-20 minutes

---

## Mission

Verify current infrastructure state before LLM configuration refactoring. NO GUESSING - check everything with terminal commands.

---

## Context

We're about to refactor LLM configuration from web-layer-only to proper DDD domain service pattern. Need to understand:
1. Current main.py structure and startup flow
2. Where LLM is currently accessed
3. What consumers exist
4. Test infrastructure

---

## Verification Tasks

### Task 1: Main Entry Point Structure (5 min)

**Check main.py**:
```bash
# Show main.py structure
ls -la main.py
wc -l main.py

# Show key sections (first 50 lines)
head -50 main.py

# Check for existing service initialization
grep -n "initialize\|startup\|bootstrap" main.py

# Check imports
head -20 main.py | grep "^import\|^from"
```

**Report**:
- Total lines in main.py
- Current startup/initialization pattern
- Existing service initialization (if any)
- Import structure

---

### Task 2: Current LLM Access Pattern (5 min)

**Find all LLM usage**:
```bash
# Find LLMConfigService usage
grep -r "LLMConfigService" --include="*.py" . | grep -v "test" | grep -v "__pycache__"

# Find where clients.py is used
grep -r "from services.llm.clients import\|from services.llm import clients" --include="*.py" . | grep -v "test" | grep -v "__pycache__"

# Check web/app.py LLM validation
grep -n "validate_llm\|LLMConfig" web/app.py
```

**Report**:
- List all files currently accessing LLMConfigService
- List all files importing from services.llm.clients
- Current validation location in web/app.py

---

### Task 3: Identify All Consumers (5 min)

**Check for potential LLM consumers**:
```bash
# Check if CLI exists and structure
ls -la cli/ 2>/dev/null || echo "No cli/ directory"
find cli/ -name "*.py" 2>/dev/null | head -10

# Check Slack integration structure
ls -la services/integrations/slack/ 2>/dev/null || echo "No slack integration"

# Check for any existing domain services
ls -la services/domain/ 2>/dev/null || echo "No domain/ directory yet"

# Check for service registry pattern
grep -r "ServiceRegistry\|service_registry" --include="*.py" . | head -5
```

**Report**:
- Does CLI exist? Structure?
- Does Slack integration exist? Where?
- Does services/domain/ exist?
- Any existing ServiceRegistry pattern?

---

### Task 4: Test Infrastructure (3 min)

**Check test structure**:
```bash
# Check test directories
ls -la tests/

# Check for domain tests
ls -la tests/domain/ 2>/dev/null || echo "No tests/domain/ yet"

# Count existing config tests
ls -la tests/config/
find tests/config/ -name "*.py" -type f | wc -l

# Check test runner
grep -n "pytest" pytest.ini 2>/dev/null || echo "No pytest.ini"
```

**Report**:
- Test directory structure
- Does tests/domain/ exist?
- Current config tests count
- Test configuration

---

### Task 5: Current Startup Flow (2 min)

**Check how server starts**:
```bash
# Check start script
ls -la start.sh stop.sh 2>/dev/null || echo "No start/stop scripts"
head -20 start.sh 2>/dev/null

# Check main.py startup
grep -A 10 "def main\|if __name__" main.py
```

**Report**:
- How is server started?
- What does main.py do at startup?
- Any existing initialization hooks?

---

## Expected Findings

Based on briefing, we expect:
- main.py: 141 lines (microservice entry)
- web/app.py: 467 lines
- services/integrations/[service]/: Router pattern
- services/plugins/: New foundation
- Port: 8001

**Verify these assumptions with actual filesystem evidence.**

---

## Report Format

```markdown
# Phase 0 Verification Report: LLM Config Refactoring

## 1. Main Entry Point
- Lines: [actual count]
- Startup pattern: [describe]
- Existing initialization: [yes/no, details]

## 2. Current LLM Access
**Files accessing LLMConfigService**:
- [file path]: [line numbers]
- [file path]: [line numbers]

**Files importing clients**:
- [file path]: [what they import]

**Current validation**: web/app.py lines [X-Y]

## 3. Consumers
- CLI: [exists/not found] - [structure if exists]
- Slack: [location] - [structure]
- Domain services: [exists/not yet]
- ServiceRegistry: [exists/not found]

## 4. Test Infrastructure
- tests/ structure: [directories found]
- tests/domain/: [exists/not yet]
- Config tests: [count] files
- Test runner: [pytest.ini status]

## 5. Startup Flow
- Start method: [script/direct]
- main.py entry: [pattern]
- Initialization hooks: [describe]

## 6. Blockers/Issues Found
- [Any issues that would block refactoring]
- [Any unexpected patterns]
- [Any missing infrastructure]

## 7. Ready For Refactoring?
- [ ] Infrastructure verified
- [ ] No blockers found
- [ ] Clear refactoring path
OR
- [ ] Issues found - [list issues]
```

---

## Success Criteria

- [ ] All 5 tasks completed with terminal evidence
- [ ] No guessing - everything verified
- [ ] Clear picture of current state
- [ ] Any blockers identified
- [ ] Report complete with facts

---

## Time Limit

**15-20 minutes maximum**

If verification takes longer, STOP and report what's taking time.

---

**This is Phase -1 verification before refactoring begins.**
