# Debug Task: Fix Perplexity API Validation

**Issue**: Perplexity validation returning 400 error
**Agent**: Code Agent
**Task Type**: Debug and fix
**Date**: October 9, 2025, 1:13 PM
**Philosophy**: Inchworm - Fix the issue completely before moving forward

---

## Problem Statement

Perplexity API validation is failing with 400 error:
```
ValidationResult(provider='perplexity', is_valid=False,
                error_message='Validation failed: 400',
                error_code='VALIDATION_ERROR')
```

**Other providers work fine:**
- ✅ OpenAI: Passing with real API call
- ✅ Anthropic: Passing with real API call
- ✅ Gemini: Passing with real API call

**Root Cause**: Our Perplexity API request format is incorrect.

---

## Investigation Steps

### Step 1: Check Current Implementation

**File**: `services/config/llm_config_service.py`

Find the `_validate_perplexity()` method and show:
1. What endpoint are we calling?
2. What HTTP method? (GET/POST)
3. What headers are we sending?
4. What request body (if any)?
5. How are we passing the API key?

### Step 2: Research Perplexity API

**Check Perplexity documentation** for:
1. What's the correct endpoint for a lightweight validation call?
2. Is there a `/models` endpoint like OpenAI?
3. Or should we use `/chat/completions` with a minimal request?
4. How does authentication work? (Header? Query param?)
5. What's the minimum valid request structure?

**Perplexity API endpoints to try:**
- `https://api.perplexity.ai/models` - Does this exist?
- `https://api.perplexity.ai/chat/completions` - Minimal request
- Check their docs: https://docs.perplexity.ai/

### Step 3: Compare with Working Providers

Look at how we validate other providers:
- **OpenAI**: Uses GET `/v1/models`
- **Anthropic**: Uses POST `/v1/messages`
- **Gemini**: Uses GET `/v1/models`

What pattern does Perplexity follow?

### Step 4: Test Different Approaches

Try these approaches in order:

#### Approach A: GET /models (if exists)
```python
async def _validate_perplexity(self, config: ProviderConfig) -> ValidationResult:
    """Validate Perplexity API key"""
    import httpx

    headers = {
        "Authorization": f"Bearer {config.api_key}"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.perplexity.ai/models",
                headers=headers,
                timeout=10.0
            )

            if response.status_code == 200:
                return ValidationResult(provider="perplexity", is_valid=True)
            elif response.status_code == 401:
                return ValidationResult(
                    provider="perplexity",
                    is_valid=False,
                    error_message="Invalid API key (401 Unauthorized)",
                    error_code="INVALID_KEY"
                )
            else:
                return ValidationResult(
                    provider="perplexity",
                    is_valid=False,
                    error_message=f"Validation failed: {response.status_code}",
                    error_code="VALIDATION_ERROR"
                )
    except Exception as e:
        return ValidationResult(
            provider="perplexity",
            is_valid=False,
            error_message=f"Network error: {str(e)}",
            error_code="NETWORK_ERROR"
        )
```

#### Approach B: POST /chat/completions (minimal request)
```python
async def _validate_perplexity(self, config: ProviderConfig) -> ValidationResult:
    """Validate Perplexity API key with minimal chat request"""
    import httpx

    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json"
    }

    # Minimal valid request
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",  # or whatever model exists
        "messages": [
            {"role": "user", "content": "test"}
        ],
        "max_tokens": 1  # Minimal response
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=payload,
                timeout=10.0
            )

            if response.status_code in [200, 201]:
                return ValidationResult(provider="perplexity", is_valid=True)
            elif response.status_code == 401:
                return ValidationResult(
                    provider="perplexity",
                    is_valid=False,
                    error_message="Invalid API key (401 Unauthorized)",
                    error_code="INVALID_KEY"
                )
            elif response.status_code == 400:
                # Log the actual error for debugging
                error_detail = response.text
                return ValidationResult(
                    provider="perplexity",
                    is_valid=False,
                    error_message=f"Request format error (400): {error_detail}",
                    error_code="INVALID_REQUEST"
                )
            else:
                return ValidationResult(
                    provider="perplexity",
                    is_valid=False,
                    error_message=f"Validation failed: {response.status_code}",
                    error_code="VALIDATION_ERROR"
                )
    except Exception as e:
        return ValidationResult(
            provider="perplexity",
            is_valid=False,
            error_message=f"Network error: {str(e)}",
            error_code="NETWORK_ERROR"
        )
```

### Step 5: Debug Current 400 Error

If still getting 400, capture the full response:
```python
# Add detailed logging
print(f"Request URL: {url}")
print(f"Request headers: {headers}")
print(f"Request body: {payload}")
print(f"Response status: {response.status_code}")
print(f"Response body: {response.text}")
```

This will tell us exactly what Perplexity's API is complaining about.

---

## Implementation Strategy

1. **Check Perplexity docs** for correct API format
2. **Try Approach A first** (GET /models) - simplest
3. **If A fails, try Approach B** (POST /chat/completions)
4. **Capture detailed error** to understand what's wrong
5. **Fix the implementation** based on findings
6. **Re-run test** until it passes

---

## Acceptance Criteria

- [ ] Perplexity API validation working (200 response)
- [ ] Test passes: `test_validate_perplexity_key_success`
- [ ] Clear error messages for invalid key vs bad request
- [ ] Implementation matches Perplexity's actual API spec
- [ ] No @pytest.mark.skip on Perplexity test

---

## Success Validation

```bash
# Run Perplexity-specific test
PYTHONPATH=. python -m pytest tests/config/test_llm_config_service.py::TestProviderValidation::test_validate_perplexity_key_success -v

# Should see: PASSED

# Run all provider validation tests
PYTHONPATH=. python -m pytest tests/config/test_llm_config_service.py::TestProviderValidation -v

# Should see: 4/4 PASSING (OpenAI, Anthropic, Gemini, Perplexity)
```

---

## Expected Outcome

After this debug session:
- ✅ All 4 providers validate successfully
- ✅ Real API calls to all providers working
- ✅ 26/26 tests passing (no skips)
- ✅ Ready to proceed to Part C with confidence

---

## STOP Conditions

- If Perplexity API is down/unreachable
- If Perplexity API key is actually invalid (not a format issue)
- If Perplexity API requires features we can't implement quickly

If STOP condition hit: Document findings and we can make Perplexity optional (not required provider).

---

**Time Estimate**: 30-45 minutes to research, fix, and validate

**This is classic debugging - investigate, hypothesis, test, fix. Inchworm style.** 🐛
