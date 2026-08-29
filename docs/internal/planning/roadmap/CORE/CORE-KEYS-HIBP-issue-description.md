# CORE-KEYS-HIBP: Have I Been Pwned API Integration

**Sprint**: TBD (A8 or later)
**Priority**: Medium
**Effort**: 30-45 minutes
**Impact**: High (security enhancement)

---

## Problem

Issue #252 (CORE-KEYS-STRENGTH-VALIDATION) created the **structure** for leak detection but did not implement actual integration with the Have I Been Pwned (HIBP) API. Currently, the `KeyLeakDetector` service only performs local checks for:
- Test/demo keys
- Weak patterns (e.g., "test", "demo", "fake")
- Obviously invalid keys

This provides basic protection but doesn't detect keys that have been compromised and leaked in actual data breaches.

---

## Current State

**What Exists** (from #252):
```python
# services/security/leak_detector.py

class KeyLeakDetector:
    """Detects if API keys have been leaked or compromised"""

    async def check_key_leaked(
        self,
        key: str,
        provider: str
    ) -> KeyLeakStatus:
        """
        Check if a key has been leaked

        TODO: Implement actual HIBP integration
        Currently only checks for obvious test/demo keys
        """
        # Local checks only (test keys, weak patterns)
        # NO actual HIBP API calls
```

**Security Framework Ready**:
- ✅ SHA-256 hashing method implemented
- ✅ `KeyLeakStatus` data model defined
- ✅ Error handling structure in place
- ✅ Rate limiting hooks ready

---

## Proposed Solution

Implement actual integration with the Have I Been Pwned Pwned Passwords API to check if API keys (or their hashes) appear in known data breaches.

### HIBP Pwned Passwords API

**Endpoint**: `https://api.pwnedpasswords.com/range/{hash-prefix}`

**How it works**:
1. Hash the API key with SHA-1 (HIBP requirement)
2. Send first 5 characters of hash to HIBP
3. HIBP returns all hash suffixes that match
4. Check if our full hash appears in the results
5. Report leak status with occurrence count

**Privacy**: API key never sent to HIBP - only first 5 chars of hash (k-anonymity model)

---

## Implementation

### Updated KeyLeakDetector

```python
import hashlib
import aiohttp
from typing import Optional

class KeyLeakDetector:
    """Detects if API keys have been leaked or compromised"""

    HIBP_API_URL = "https://api.pwnedpasswords.com/range"

    async def check_key_leaked(
        self,
        key: str,
        provider: str
    ) -> KeyLeakStatus:
        """
        Check if a key has been leaked using HIBP API

        Uses k-anonymity model - only sends first 5 chars of hash
        """
        # Step 1: Local checks (fast, no API call)
        local_result = self._check_local_patterns(key)
        if local_result.is_leaked:
            return local_result

        # Step 2: HIBP API check
        try:
            hibp_result = await self._check_hibp_api(key)
            return hibp_result
        except Exception as e:
            logger.warning(f"HIBP check failed: {e}")
            # Return non-leaked status if HIBP unavailable
            return KeyLeakStatus(
                is_leaked=False,
                confidence="low",
                source="local-only",
                message="Could not verify against breach database"
            )

    async def _check_hibp_api(self, key: str) -> KeyLeakStatus:
        """Check key against HIBP Pwned Passwords API"""

        # Hash the key with SHA-1 (HIBP requirement)
        sha1_hash = hashlib.sha1(key.encode('utf-8')).hexdigest().upper()
        hash_prefix = sha1_hash[:5]
        hash_suffix = sha1_hash[5:]

        # Query HIBP API
        url = f"{self.HIBP_API_URL}/{hash_prefix}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                if response.status != 200:
                    raise Exception(f"HIBP API returned {response.status}")

                # Parse response (format: "SUFFIX:COUNT\r\n")
                content = await response.text()

                for line in content.split('\r\n'):
                    if not line:
                        continue

                    suffix, count = line.split(':')
                    if suffix == hash_suffix:
                        # Key found in breach database!
                        return KeyLeakStatus(
                            is_leaked=True,
                            confidence="high",
                            source="haveibeenpwned",
                            message=f"Key found in {count} breaches",
                            occurrences=int(count)
                        )

        # Key not found in breach database
        return KeyLeakStatus(
            is_leaked=False,
            confidence="high",
            source="haveibeenpwned",
            message="No known breaches detected"
        )

    def _check_local_patterns(self, key: str) -> KeyLeakStatus:
        """Fast local checks for obvious test/demo keys"""
        # Existing implementation from #252
        ...
```

---

## Configuration

### Environment Variables

```bash
# Optional: HIBP API key for higher rate limits
HIBP_API_KEY=your-api-key-here  # Optional, for enterprise use

# Rate limiting
HIBP_MAX_REQUESTS_PER_MINUTE=60  # Default: 60 (anonymous)
HIBP_REQUEST_TIMEOUT_SECONDS=5   # Default: 5
```

### Rate Limiting Strategy

**Anonymous usage**: 60 requests per minute (sufficient for most use cases)
**With API key**: Higher limits available

**Implementation**:
```python
class HIBPRateLimiter:
    """Rate limiter for HIBP API calls"""

    def __init__(self, max_per_minute: int = 60):
        self.max_per_minute = max_per_minute
        self.requests: list[float] = []

    async def acquire(self):
        """Wait if necessary to stay within rate limits"""
        now = time.time()

        # Remove requests older than 1 minute
        self.requests = [t for t in self.requests if now - t < 60]

        # Wait if at limit
        if len(self.requests) >= self.max_per_minute:
            wait_time = 60 - (now - self.requests[0])
            await asyncio.sleep(wait_time)

        self.requests.append(now)
```

---

## Security Considerations

### Why This Is Safe

1. **k-anonymity model**: Only 5 chars of hash sent to HIBP
2. **SHA-1 hashing**: API key never transmitted in plain text
3. **No key storage**: HIBP doesn't store or log queries
4. **Privacy-preserving**: Cannot reverse-engineer key from hash prefix

### Additional Protections

```python
class KeyLeakDetector:

    async def check_key_leaked(self, key: str, provider: str) -> KeyLeakStatus:
        # Validate key before hashing
        if len(key) < 8:
            return KeyLeakStatus(
                is_leaked=False,
                confidence="low",
                source="validation",
                message="Key too short to validate"
            )

        # Don't check certain key types (e.g., JWT tokens)
        if self._is_jwt_token(key):
            return KeyLeakStatus(
                is_leaked=False,
                confidence="low",
                source="validation",
                message="JWT tokens not checked against HIBP"
            )

        # Proceed with HIBP check
        ...
```

---

## Error Handling

### Graceful Degradation

```python
async def _check_hibp_api(self, key: str) -> KeyLeakStatus:
    """Check key against HIBP API with comprehensive error handling"""

    try:
        # HIBP API call
        result = await self._perform_hibp_check(key)
        return result

    except aiohttp.ClientTimeout:
        logger.warning("HIBP API timeout")
        return KeyLeakStatus(
            is_leaked=False,
            confidence="low",
            source="timeout",
            message="Breach check timed out - try again later"
        )

    except aiohttp.ClientError as e:
        logger.warning(f"HIBP API error: {e}")
        return KeyLeakStatus(
            is_leaked=False,
            confidence="low",
            source="error",
            message="Breach database temporarily unavailable"
        )

    except Exception as e:
        logger.error(f"Unexpected error in HIBP check: {e}")
        return KeyLeakStatus(
            is_leaked=False,
            confidence="low",
            source="error",
            message="Could not complete breach check"
        )
```

**Key principle**: If HIBP is unavailable, **don't block the user** - return non-leaked status with low confidence.

---

## Testing

### Unit Tests

```python
async def test_hibp_api_integration():
    """Test actual HIBP API calls"""
    detector = KeyLeakDetector()

    # Test with known leaked password
    result = await detector.check_key_leaked("password123", "test")
    assert result.is_leaked is True
    assert result.source == "haveibeenpwned"
    assert result.occurrences > 0

async def test_hibp_rate_limiting():
    """Test rate limiting doesn't block legitimate requests"""
    detector = KeyLeakDetector()
    limiter = HIBPRateLimiter(max_per_minute=5)

    # Make 10 requests
    start = time.time()
    for i in range(10):
        await limiter.acquire()
        # Should take ~60 seconds for 10 requests at 5/min

    duration = time.time() - start
    assert duration >= 60  # Rate limiting working

async def test_hibp_timeout_handling():
    """Test graceful handling of timeouts"""
    detector = KeyLeakDetector()

    # Mock slow HIBP response
    with mock_slow_response():
        result = await detector.check_key_leaked("test-key", "test")
        assert result.is_leaked is False
        assert result.confidence == "low"
        assert "timeout" in result.message.lower()
```

### Integration Tests

```python
async def test_key_validation_with_hibp():
    """Test full key validation including HIBP"""
    validator = KeyValidator()

    # Test with API key that's definitely not leaked
    secure_key = "sk-" + secrets.token_urlsafe(32)
    report = await validator.validate_key(secure_key, "openai")

    assert report.leak_check.is_leaked is False
    assert report.leak_check.confidence == "high"

async def test_leaked_key_detection():
    """Test detection of actually leaked keys"""
    validator = KeyValidator()

    # Use a known weak/test key
    weak_key = "test-key-12345"
    report = await validator.validate_key(weak_key, "openai")

    # Should be caught by local checks OR HIBP
    assert report.leak_check.is_leaked is True
```

---

## Acceptance Criteria

### Functional Requirements
- [ ] Actual HIBP API integration implemented
- [ ] SHA-1 hashing for k-anonymity
- [ ] Rate limiting respects HIBP limits (60/min)
- [ ] Graceful degradation if HIBP unavailable
- [ ] Local checks run first (fast path)
- [ ] Breach count reported when key found

### Security Requirements
- [ ] No plain-text keys sent to HIBP
- [ ] Only 5 chars of hash transmitted
- [ ] Request timeout configured (5 seconds)
- [ ] No key material logged
- [ ] JWT tokens excluded from checks

### User Experience
- [ ] Fast response (<1 second typical)
- [ ] Clear messaging if HIBP unavailable
- [ ] Leak count shown when detected
- [ ] Integration with existing validation flow

### Testing Requirements
- [ ] Unit tests for HIBP API calls
- [ ] Mock tests for error scenarios
- [ ] Rate limiting tests
- [ ] Integration with KeyValidator tests

---

## Performance Considerations

### Expected Performance

- **Local checks**: <1ms
- **HIBP API call**: 100-500ms typical
- **Rate limit wait**: 0-60 seconds (rare)
- **Total validation**: <1 second typical

### Optimization Strategy

1. **Local checks first**: Catch obvious issues without API call
2. **Caching**: Consider caching negative results (key not leaked) for 24 hours
3. **Batch checking**: For multiple keys, respect rate limits
4. **Async operations**: Don't block other validations

---

## Integration Points

### With Existing Services

**KeyValidator** (from #252):
```python
class KeyValidator:
    async def validate_key(self, key: str, provider: str) -> ValidationReport:
        # Format check
        format_result = await self.format_checker.check(...)

        # Strength check
        strength_result = await self.strength_checker.check(...)

        # Leak check (NOW WITH HIBP!)
        leak_result = await self.leak_detector.check_key_leaked(key, provider)

        return ValidationReport(
            format_check=format_result,
            strength_check=strength_result,
            leak_check=leak_result  # Now includes HIBP results
        )
```

**Status Checker** (from #255):
```python
async def check_key_security():
    """Enhanced status check with HIBP integration"""
    for key in user_keys:
        validation = await validator.validate_key(key.value, key.provider)

        if validation.leak_check.is_leaked:
            print(f"⚠️  {key.provider}: Key found in {validation.leak_check.occurrences} breaches!")
        else:
            print(f"✅ {key.provider}: No known leaks detected")
```

---

## Future Enhancements

### Phase 2 (Later)
- Automatic key rotation when leak detected
- Webhook notifications for leaked keys
- Dashboard showing leak check history
- Batch checking for all keys

### Phase 3 (MVP)
- HIBP API key for higher rate limits
- Cache negative results (24-hour TTL)
- Breach notification timeline
- Key compromise response workflow

---

## Related Issues

- **#252: CORE-KEYS-STRENGTH-VALIDATION** - Created the framework for leak detection
- **#250: CORE-KEYS-ROTATION-REMINDERS** - Could trigger rotation on leak detection
- **#253: CORE-KEYS-COST-ANALYTICS** - Could track HIBP API usage

---

## Documentation Requirements

### User Documentation
- How HIBP integration works (k-anonymity model)
- Why it's safe (privacy-preserving)
- What happens if key is leaked
- How to respond to leak detection

### Developer Documentation
- HIBP API integration guide
- Rate limiting implementation
- Error handling patterns
- Testing with HIBP API

---

## Deployment Considerations

### Configuration
```yaml
# config/security.yaml
hibp:
  enabled: true  # Can be disabled if needed
  api_key: ${HIBP_API_KEY}  # Optional
  rate_limit: 60  # Requests per minute
  timeout: 5  # Seconds
  cache_ttl: 86400  # 24 hours (for negative results)
```

### Monitoring
- Track HIBP API success/failure rates
- Monitor rate limiting delays
- Alert on detected leaks
- Log HIBP availability

---

## Success Metrics

- HIBP API calls successful >95% of time
- Average response time <1 second
- Zero false positives on leak detection
- User confidence in key security increased

---

**Sprint**: TBD
**Milestone**: TBD (A8 or later)
**Labels**: security, enhancement, api-integration, keys
**Estimated Effort**: 30-45 minutes
