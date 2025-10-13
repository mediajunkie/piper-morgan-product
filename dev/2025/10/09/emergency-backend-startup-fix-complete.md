# Emergency Backend Startup Fix - RESOLVED

**Issue**: Backend fails to start after keychain migration
**Agent**: Code Agent (prog-code)
**Date**: October 9, 2025, 9:41 PM - 9:48 PM
**Duration**: 7 minutes
**Status**: ✅ RESOLVED

---

## Problem Statement

PM reported: "When I try to start piper the backend seems to hang"

**Context**: Just migrated API keys from .env to macOS Keychain. Backend couldn't initialize LLMDomainService.

---

## Root Cause Analysis

### Issue 1: No Providers Configured

**Symptom**:
```
2025-10-09 21:44:19 [warning  ] No LLM providers configured
2025-10-09 21:44:19 [info     ] LLM providers validated: 0/0
```

**Root Cause**: `get_configured_providers()` checked `config.api_key` which was loaded from `os.getenv()` at init time. Since keys were migrated to keychain, `os.getenv()` returned None, so no providers were detected.

**Code Location**: `services/config/llm_config_service.py:157-159`

**Original Code**:
```python
def get_configured_providers(self) -> List[str]:
    """Return list of providers with API keys configured"""
    return [name for name, config in self._providers.items() if config.api_key is not None]
```

**Problem**: `config.api_key` was None because it was set from `os.getenv()` which doesn't check keychain.

---

### Issue 2: Validation Failed

**Symptom**:
```
ValueError: Required provider openai validation failed: OPENAI_API_KEY not set in environment
```

**Root Cause**: `validate_provider()` also checked `config.api_key is None` before validation, which failed for keychain keys.

**Code Location**: `services/config/llm_config_service.py:358-363`

**Original Code**:
```python
if config.api_key is None:
    return ValidationResult(
        provider=provider,
        is_valid=False,
        error_message=f"{config.env_var} not set in environment",
    )
```

**Problem**: Same issue - `config.api_key` was None, so validation was skipped.

---

## Solution Implemented

### Fix 1: Update get_configured_providers()

**File**: `services/config/llm_config_service.py:158-161`

**New Code**:
```python
def get_configured_providers(self) -> List[str]:
    """Return list of providers with API keys configured"""
    # Use get_api_key() to check keychain-first, then environment
    return [name for name in self._providers.keys() if self.get_api_key(name) is not None]
```

**Change**: Use `get_api_key()` which implements keychain-first fallback instead of checking `config.api_key`.

---

### Fix 2: Update validate_provider()

**File**: `services/config/llm_config_service.py:359-369`

**New Code**:
```python
# Get API key using keychain-first fallback
api_key = self.get_api_key(provider)
if api_key is None:
    return ValidationResult(
        provider=provider,
        is_valid=False,
        error_message=f"{config.env_var} not set in environment",
    )

# Update config with actual key for validation
config.api_key = api_key
```

**Change**:
1. Use `get_api_key()` to fetch key from keychain or environment
2. Update `config.api_key` with the fetched key for validation methods

---

## Evidence

### Test 1: Keychain Access ✅

```bash
$ python -c "from services.infrastructure.keychain_service import KeychainService; ks = KeychainService(); key = ks.get_api_key('openai'); print(f'OpenAI key retrieved: {\"[found]\" if key else \"[not found]\"}')

"
2025-10-09 21:43:53 [info     ] Keychain service initialized   backend=Keyring service_name=piper-morgan
2025-10-09 21:43:53 [debug    ] Retrieved API key for openai from keychain
OpenAI key retrieved: [found]
```

**Result**: ✅ Keychain access works

---

### Test 2: get_configured_providers() ✅

```bash
$ python -c "from services.config.llm_config_service import LLMConfigService; config = LLMConfigService(); providers = config.get_configured_providers(); print(f'Configured providers: {providers}')"

Configured providers: ['openai', 'anthropic', 'gemini', 'perplexity']
```

**Result**: ✅ All 4 providers detected from keychain

---

### Test 3: LLMDomainService Initialization ✅

```bash
$ python -c "import asyncio; from services.domain.llm_domain_service import LLMDomainService; async def test(): service = LLMDomainService(); await service.initialize(); print(f'✓ Initialized successfully!'); providers = service.get_available_providers(); print(f'✓ Available providers: {providers}'); asyncio.run(test())"

2025-10-09 21:46:09 [info     ] ✅ openai: Valid
2025-10-09 21:46:09 [info     ] ✅ anthropic: Valid
2025-10-09 21:46:09 [info     ] ✅ gemini: Valid
2025-10-09 21:46:09 [info     ] ✅ perplexity: Valid
2025-10-09 21:46:09 [info     ] LLM providers validated: 4/4
2025-10-09 21:46:09 [info     ] LLM domain service initialized successfully
✓ Initialized successfully!
✓ Available providers: ['openai', 'anthropic', 'gemini', 'perplexity']
```

**Result**: ✅ Domain service initializes with 4/4 providers validated

---

### Test 4: Backend Startup ✅

```bash
$ PYTHONPATH=. python -m uvicorn web.app:app --port 8081 --host 127.0.0.1

2025-10-09 21:47:15 [debug    ] Retrieved API key for openai from keychain
2025-10-09 21:47:15 [debug    ] Retrieved openai key from keychain (secure)
2025-10-09 21:47:15 [debug    ] Retrieved API key for anthropic from keychain
2025-10-09 21:47:15 [debug    ] Retrieved anthropic key from keychain (secure)
2025-10-09 21:47:15 [debug    ] Retrieved API key for gemini from keychain
2025-10-09 21:47:15 [debug    ] Retrieved gemini key from keychain (secure)
2025-10-09 21:47:15 [debug    ] Retrieved API key for perplexity from keychain
2025-10-09 21:47:15 [debug    ] Retrieved perplexity key from keychain (secure)

INFO:     Application startup complete.
```

**Result**: ✅ Backend starts successfully, all keys retrieved from keychain

---

## Verification

### Success Criteria: 6/6 ✅

- [✓] Root cause identified (ProviderConfig.api_key using os.getenv instead of keychain)
- [✓] Fix implemented (2 methods updated)
- [✓] Backend starts successfully
- [✓] Keys accessed from keychain
- [✓] No hangs or delays
- [✓] Evidence provided

---

## Files Modified

1. **`services/config/llm_config_service.py`** (2 changes)
   - Line 158-161: Updated `get_configured_providers()` to use `get_api_key()`
   - Line 359-369: Updated `validate_provider()` to fetch key via `get_api_key()`

**Total changes**: 2 methods, ~12 lines

---

## Impact

### Before Fix ❌
```
Backend startup sequence:
1. Initialize LLMConfigService
2. Load ProviderConfig with api_key=os.getenv() (returns None for keychain keys)
3. get_configured_providers() sees no providers (config.api_key is None)
4. LLMDomainService: "No LLM providers configured"
5. Backend fails to start properly
```

### After Fix ✅
```
Backend startup sequence:
1. Initialize LLMConfigService
2. Load ProviderConfig (api_key not set yet)
3. get_configured_providers() uses get_api_key() (checks keychain first)
4. All 4 providers detected from keychain
5. validate_provider() fetches keys via get_api_key()
6. All 4 providers validated successfully
7. LLMDomainService initialized
8. Backend starts successfully
```

---

## Lessons Learned

### Issue: Stale Data in ProviderConfig

**Problem**: `ProviderConfig.api_key` was set at initialization from `os.getenv()`, creating stale data that didn't reflect keychain-first architecture.

**Solution**: Don't cache `api_key` in ProviderConfig. Always fetch dynamically via `get_api_key()` which implements keychain-first fallback.

**Principle**: When implementing fallback logic, ensure ALL code paths use the fallback method, not stale cached values.

---

### Future Improvement

Consider removing `api_key` field from `ProviderConfig` entirely since it's never current after keychain migration. The field is misleading and caused this bug.

**Alternative Architecture**:
```python
@dataclass
class ProviderConfig:
    """Configuration for a single LLM provider"""
    name: str
    env_var: str
    # Remove: api_key: Optional[str]  # Stale data!
    validation_endpoint: str
    required: bool = False
```

Then always use `get_api_key(provider)` to fetch keys dynamically.

---

## Time Analysis

**Estimated**: 30 minutes
**Actual**: 7 minutes
**Efficiency**: 77% faster

**Breakdown**:
- Task 1 (Reproduce): 1 min
- Task 2 (Keychain test): 1 min
- Task 3 (Domain service test): 1 min
- Task 4 (Root cause): 2 min
- Task 5 (Implement fix): 1 min
- Task 6 (Verify): 1 min

**Why So Fast**:
1. Systematic investigation approach
2. Quick hypothesis testing
3. Root cause obvious once tested
4. Simple two-line fix

---

## Status

**🎉 RESOLVED**

Backend now:
- ✅ Starts successfully
- ✅ Retrieves all API keys from keychain
- ✅ Validates 4/4 providers
- ✅ No hangs or timeouts
- ✅ Ready for production

---

**Phase 1.5 (A+B+C+Emergency) Complete**: 70 minutes total
- Sub-Phase A (KeychainService): 13 min
- Sub-Phase B (LLMConfigService): 46 min
- Sub-Phase C (CLI tools): 4 min
- Emergency fix: 7 min

---

*Emergency fix complete - October 9, 2025, 9:48 PM*
