# Phase 1 Part C: Integration - Wire Up LLMConfigService

**Issue**: #217 - CORE-LLM-CONFIG
**Phase**: 1 Part C (Final integration)
**Agent**: Code Agent
**Estimated Time**: 30-45 minutes
**Date**: October 9, 2025, 1:35 PM

---

## Mission

Integrate the fully-tested LLMConfigService into existing LLM client initialization and add startup validation.

---

## Context

**What We Have**:
- ✅ LLMConfigService fully implemented and tested (26/26 tests passing)
- ✅ Real API validation for all 4 providers (OpenAI, Anthropic, Gemini, Perplexity)
- ✅ Clear error messages for missing/invalid keys

**What We Need**:
- Update existing LLM client code to use LLMConfigService
- Add startup validation to catch key issues early
- Verify end-to-end functionality

---

## Part C Tasks

### Task 1: Update LLM Client Initialization (20 minutes)

**From Phase 0 Investigation**:
Current LLM clients are initialized in `services/llm/clients.py` around lines 20-42.

**Current pattern** (from investigation):
```python
# Direct environment variable access
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Client initialization
openai_client = OpenAI(api_key=openai_api_key)
anthropic_client = Anthropic(api_key=anthropic_api_key)
```

**New pattern** (using LLMConfigService):
```python
from services.config.llm_config_service import LLMConfigService

# Create config service (singleton pattern recommended)
_config_service = LLMConfigService()

# Get keys through service
openai_api_key = _config_service.get_api_key("openai")
anthropic_api_key = _config_service.get_api_key("anthropic")

# Client initialization (same as before)
openai_client = OpenAI(api_key=openai_api_key)
anthropic_client = Anthropic(api_key=anthropic_api_key)
```

**Files to update**:
1. **`services/llm/clients.py`** - Main client initialization
   - Import LLMConfigService
   - Replace direct `os.getenv()` calls with `config_service.get_api_key()`
   - Keep existing client initialization logic

**Important**:
- Don't change how clients are used elsewhere
- Only change how API keys are retrieved
- Preserve the existing global client variables if they exist
- Maintain backward compatibility

### Task 2: Add Startup Validation (15 minutes)

**File**: `main.py`

Add validation at application startup to catch key issues early.

**Find startup events**:
Look for FastAPI lifespan or `@app.on_event("startup")` handlers.

**Add validation**:
```python
from services.config.llm_config_service import LLMConfigService
import structlog

logger = structlog.get_logger(__name__)

@app.on_event("startup")
async def validate_llm_configuration():
    """Validate LLM API keys at startup"""
    logger.info("Validating LLM API keys...")

    try:
        config_service = LLMConfigService()
        results = await config_service.validate_all_providers()

        # Log results
        for provider, result in results.items():
            if result.is_valid:
                logger.info(f"✅ {provider}: Valid")
            else:
                logger.warning(f"⚠️ {provider}: {result.error_message}")

        # Count valid providers
        valid_count = sum(1 for r in results.values() if r.is_valid)
        logger.info(f"LLM configuration: {valid_count}/{len(results)} providers valid")

    except Exception as e:
        logger.error(f"LLM configuration validation failed: {e}")
        # Don't crash startup, but log the error
```

**Note**: We don't want to crash the server if optional providers fail, but we want to know about it.

### Task 3: Verify Integration (10 minutes)

**Step 3.1: Run Tests**
```bash
# Run LLM config tests
PYTHONPATH=. python -m pytest tests/config/test_llm_config_service.py -v
# Expected: 26/26 PASSING

# Run any tests that use LLM clients
PYTHONPATH=. python -m pytest tests/llm/ -v
# Expected: Tests still pass (backward compatible)
```

**Step 3.2: Start Server**
```bash
# Start server and watch for validation messages
PYTHONPATH=. python main.py
```

**Expected startup logs**:
```
INFO     Validating LLM API keys...
INFO     ✅ openai: Valid
INFO     ✅ anthropic: Valid
INFO     ✅ gemini: Valid
INFO     ✅ perplexity: Valid
INFO     LLM configuration: 4/4 providers valid
```

**Step 3.3: Test with Invalid Key** (optional but recommended)
```bash
# Temporarily break one key in .env
OPENAI_API_KEY=sk-invalid

# Start server
PYTHONPATH=. python main.py
```

**Expected behavior**:
- Server logs: "❌ openai: Invalid API key (401 Unauthorized)"
- Server still starts (doesn't crash)
- Or server refuses to start if OpenAI is required (check service logic)

---

## Implementation Details

### Singleton Pattern for Config Service

Consider making LLMConfigService a singleton to avoid reloading configuration:

```python
# services/config/llm_config_service.py

class LLMConfigService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        # ... existing initialization ...
        self._initialized = True
```

This ensures configuration is loaded once and reused.

### Error Handling Strategy

**For required providers** (OpenAI):
- Raise exception if key missing/invalid
- Server refuses to start

**For optional providers** (Anthropic, Gemini, Perplexity):
- Log warning if key missing/invalid
- Server starts anyway
- Provider just won't be available

This is already implemented in `validate_all_providers()` based on the `required` flag.

---

## Acceptance Criteria

- [ ] LLM clients use LLMConfigService for API keys
- [ ] No direct `os.getenv()` calls for LLM keys in client code
- [ ] Startup validation runs and logs results
- [ ] Server starts successfully with valid keys
- [ ] All existing tests still pass (backward compatible)
- [ ] Startup logs show validation status for each provider
- [ ] Invalid key produces clear error message

---

## Testing Validation

```bash
# 1. Run config service tests
python -m pytest tests/config/test_llm_config_service.py -v
# Expected: 26/26 PASSING

# 2. Run LLM client tests (if they exist)
python -m pytest tests/llm/ -v
# Expected: All passing

# 3. Run integration tests
python -m pytest tests/integration/ -v
# Expected: All passing

# 4. Start server
python main.py
# Expected: Clean startup with validation messages

# 5. Test API endpoint (if accessible)
curl http://localhost:8001/health
# Expected: 200 OK
```

---

## Files to Modify

Based on Phase 0 investigation:

1. **`services/llm/clients.py`** (lines ~20-42)
   - Import LLMConfigService
   - Replace direct env var access
   - Maintain existing client variables

2. **`main.py`** (startup section)
   - Add validation event handler
   - Log validation results

**Files NOT to modify**:
- Don't change how clients are used in other services
- Don't change existing API contracts
- Don't modify test files (except conftest if needed)

---

## STOP Conditions

- If client initialization is more complex than expected
- If startup validation causes circular dependencies
- If existing tests break (indicates breaking change)
- If integration reveals architecture issues

If STOP condition hit: Document findings and escalate.

---

## Success Metrics

After Part C completion:
- ✅ LLMConfigService integrated into production code
- ✅ Startup validation working
- ✅ All tests passing (26 config tests + existing tests)
- ✅ Clear validation messages in logs
- ✅ No breaking changes to existing code

---

## Deliverable

**Updated files**:
- `services/llm/clients.py` - Using config service
- `main.py` - Startup validation added

**Verification**:
- Server starts with validation messages
- All tests passing
- API keys properly managed through service

---

**Time Estimate**: 30-45 minutes

**This completes Phase 1** - After this, we have secure key management with validation!

Then we move to Phase 2: Provider exclusion logic to stop burning Anthropic credits.
