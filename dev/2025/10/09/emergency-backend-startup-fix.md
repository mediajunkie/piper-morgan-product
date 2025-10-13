# Emergency: Backend Startup Hang Investigation

**Issue**: Backend hangs on startup after keychain migration
**Agent**: Code Agent
**Date**: October 9, 2025, 9:41 PM
**Priority**: CRITICAL - Blocks verification
**Time Estimate**: 15-30 minutes

---

## Problem Statement

PM reports: "When I try to start piper the backend seems to hang"

**Context**: Just migrated API keys from .env to macOS Keychain. Need to verify backend can:
1. Initialize LLMDomainService
2. Access keys from keychain
3. Start successfully

---

## Investigation Tasks

### Task 1: Reproduce the Hang (5 min)

**Try to start backend**:
```bash
# Check if anything is running
ps aux | grep python | grep main

# Kill any existing processes
pkill -f "python main.py"

# Try to start
python main.py

# Watch for where it hangs
# Let it run for 30 seconds, then Ctrl+C if hung
```

**Capture**:
- Last log message before hang
- Any error messages
- Where in main.py it stops

---

### Task 2: Check Keychain Access (5 min)

**Test keychain access directly**:
```bash
# Test if Python can access keychain
python -c "
from services.infrastructure.keychain_service import KeychainService
ks = KeychainService()
key = ks.get_api_key('openai')
print(f'OpenAI key retrieved: {key[:10] if key else None}...')
"
```

**If this hangs**: Keychain permission issue
**If this works**: Issue is elsewhere in startup

---

### Task 3: Check LLMDomainService Initialization (5 min)

**Test domain service initialization**:
```bash
# Test if LLMDomainService initializes
python -c "
import asyncio
from services.domain.llm_domain_service import LLMDomainService

async def test():
    service = LLMDomainService()
    print('Created service')
    await service.initialize()
    print('Initialized successfully')

asyncio.run(test())
"
```

**Look for**:
- Where it hangs in initialization
- Any validation that takes too long
- Network timeouts

---

### Task 4: Check Main.py Startup Sequence (5 min)

**Use Serena to examine main.py initialization**:
```python
mcp__serena__find_symbol(
    name_path="initialize_domain_services",
    relative_path="main.py",
    include_body=True
)
```

**Look for**:
- What happens at line 102 (where we added domain service init)
- Any blocking operations
- Order of initialization

---

### Task 5: Test Without Domain Service Init (5 min)

**Temporarily comment out domain service initialization**:

In `main.py`, find and comment out:
```python
# async def initialize_domain_services():
#     ...
# asyncio.run(initialize_domain_services())
```

**Then try**:
```bash
python main.py
```

**If this works**: Issue is in domain service initialization
**If still hangs**: Issue elsewhere

---

## Common Issues to Check

### Issue 1: Keychain Password Prompt
**Symptom**: Hangs waiting for keychain password
**Solution**: Run with input available or pre-authorize

### Issue 2: API Validation Timeout
**Symptom**: Hangs during `validate_all_providers()`
**Solution**: Network timeout or slow API

### Issue 3: Async/Await Issue
**Symptom**: Hangs in async initialization
**Solution**: Missing await or event loop issue

### Issue 4: Import Cycle
**Symptom**: Hangs on import
**Solution**: Circular dependency in imports

---

## Quick Fixes to Try

### Fix 1: Skip Validation on Startup
```python
# In LLMDomainService.initialize()
# Comment out validation temporarily:
# validation_results = await self._config_service.validate_all_providers()
```

### Fix 2: Add Timeouts
```python
# Add timeout to validation
import asyncio
try:
    await asyncio.wait_for(
        self._config_service.validate_all_providers(),
        timeout=10.0
    )
except asyncio.TimeoutError:
    logger.warning("Validation timed out, skipping")
```

### Fix 3: Make Validation Optional
```python
# Add flag to skip validation
async def initialize(self, skip_validation: bool = False):
    if not skip_validation:
        await self._config_service.validate_all_providers()
```

---

## Expected Findings

Report in this format:

```markdown
# Backend Startup Investigation

## Reproduction
- Startup command: python main.py
- Hangs at: [log message / line number]
- Duration: [how long before hang]

## Root Cause
[What's causing the hang]

## Evidence
```bash
[Terminal output showing the issue]
```

## Solution
[What needs to be fixed]

## Fix Applied
[Code changes made]

## Verification
```bash
$ python main.py
[Startup logs showing success]
```

## Status
- [ ] Backend starts successfully
- [ ] Keys retrieved from keychain
- [ ] No hangs or timeouts
- [ ] Ready for production
```

---

## Time Limit

**30 minutes maximum**

If not resolved in 30 minutes:
1. Document findings
2. Implement quick workaround (skip validation)
3. Note for tomorrow's fix

---

## Success Criteria

- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Backend starts successfully
- [ ] Keys accessed from keychain
- [ ] No hangs or delays
- [ ] Evidence provided

---

**CRITICAL: We need backend working to verify Phase 3 complete!**

---

*Emergency troubleshooting - October 9, 2025, 9:41 PM*
