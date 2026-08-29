# CORE-KEYS-STRENGTH-VALIDATION: API Key Strength & Security Validation

## Context

Users may enter weak, leaked, or compromised API keys. The system should validate key strength and security before storage to protect users and the platform.

**Parent Issue**: #228 (API Key Management)

---

## Problem Statement

**Current State**:
- Keys validated for format correctness (via provider APIs)
- No strength checks (length, entropy, character diversity)
- No leak detection (compromised keys in public databases)
- No pattern validation (common weak keys)

**Risk**:
- Users may use weak or compromised keys
- Security vulnerabilities from poor key hygiene
- Compliance issues (some standards require key strength validation)
- Reputation risk if compromised keys used

---

## Proposed Solution

### 1. Key Strength Analysis
```python
class KeyStrengthAnalyzer:
    def analyze_key_strength(self, api_key: str) -> KeyStrength:
        """Analyze API key strength"""
        return KeyStrength(
            length_score=self._check_length(api_key),
            entropy_score=self._calculate_entropy(api_key),
            character_diversity_score=self._check_character_diversity(api_key),
            pattern_score=self._check_patterns(api_key),
            overall_score=self._calculate_overall_score()
        )

    def _check_length(self, key: str) -> float:
        """Check if key meets minimum length requirements"""
        # OpenAI: 51 chars (sk-...)
        # Anthropic: 108 chars (sk-ant-...)
        # GitHub: 40 chars (ghp_...)

    def _calculate_entropy(self, key: str) -> float:
        """Calculate Shannon entropy"""
        # High entropy = more random = stronger

    def _check_character_diversity(self, key: str) -> float:
        """Check use of different character types"""
        # Should include: uppercase, lowercase, numbers, symbols

    def _check_patterns(self, key: str) -> float:
        """Check for common weak patterns"""
        # Repeating characters, sequential patterns, etc.
```

### 2. Leak Detection
```python
class KeyLeakDetector:
    async def check_key_leaked(self, api_key: str) -> LeakCheckResult:
        """Check if key appears in public leak databases"""
        # Integration with:
        # - Have I Been Pwned (hibp.com)
        # - GitHub Secret Scanning
        # - Custom leak database

        # Use one-way hash to protect key
        key_hash = sha256(api_key).hexdigest()

        leaked = await self._check_hibp(key_hash)

        return LeakCheckResult(
            leaked=leaked,
            source="HIBP" if leaked else None,
            severity="critical" if leaked else "ok",
            recommendation="Rotate immediately" if leaked else None
        )
```

### 3. Provider-Specific Validation
```python
class ProviderKeyValidator:
    """Provider-specific key validation rules"""

    RULES = {
        "openai": {
            "prefix": "sk-",
            "min_length": 50,
            "pattern": r"^sk-[A-Za-z0-9]{48}$"
        },
        "anthropic": {
            "prefix": "sk-ant-",
            "min_length": 100,
            "pattern": r"^sk-ant-[A-Za-z0-9-_]{100,}$"
        },
        "github": {
            "prefixes": ["ghp_", "gho_", "ghu_"],
            "min_length": 40,
            "pattern": r"^gh[pou]_[A-Za-z0-9]{36}$"
        }
    }

    def validate_format(self, provider: str, api_key: str) -> ValidationResult:
        """Validate key format for provider"""
        rules = self.RULES.get(provider)
        if not rules:
            return ValidationResult(valid=True, message="Provider not configured")

        # Check prefix
        if not api_key.startswith(rules["prefix"]):
            return ValidationResult(
                valid=False,
                message=f"Key must start with {rules['prefix']}"
            )

        # Check length
        if len(api_key) < rules["min_length"]:
            return ValidationResult(
                valid=False,
                message=f"Key too short (minimum {rules['min_length']} characters)"
            )

        # Check pattern
        if not re.match(rules["pattern"], api_key):
            return ValidationResult(
                valid=False,
                message="Key format invalid for provider"
            )

        return ValidationResult(valid=True, message="Format valid")
```

### 4. Storage with Validation
```python
async def store_user_key_validated(
    self,
    user_id: str,
    provider: str,
    api_key: str,
    skip_strength_check: bool = False
) -> StorageResult:
    """Store key with comprehensive validation"""

    # 1. Format validation (fast)
    format_result = validator.validate_format(provider, api_key)
    if not format_result.valid:
        raise InvalidKeyFormatError(format_result.message)

    # 2. Strength analysis (fast)
    if not skip_strength_check:
        strength = analyzer.analyze_key_strength(api_key)
        if strength.overall_score < 0.7:
            raise WeakKeyError(
                f"Key strength too low ({strength.overall_score:.0%}). "
                f"Use a stronger key or override with skip_strength_check=True"
            )

    # 3. Leak detection (slow, async)
    leak_result = await detector.check_key_leaked(api_key)
    if leak_result.leaked:
        raise LeakedKeyError(
            f"This key appears in public leak database ({leak_result.source}). "
            f"Rotate immediately!"
        )

    # 4. Provider API validation (slow, required)
    api_valid = await self.validate_user_key(user_id, provider, api_key)
    if not api_valid:
        raise InvalidKeyError("Key rejected by provider API")

    # 5. Store if all checks pass
    return await self._store_key(user_id, provider, api_key)
```

---

## Implementation Phases

### Phase 1: Format Validation (2 hours)
- Provider-specific format rules
- Prefix validation
- Length validation
- Pattern matching
- Clear error messages

### Phase 2: Strength Analysis (3 hours)
- Length scoring
- Entropy calculation
- Character diversity checking
- Pattern detection
- Overall strength score

### Phase 3: Leak Detection (4 hours)
- HIBP integration
- GitHub Secret Scanning integration
- One-way hash protection
- Async checking (don't block storage)
- Clear leak warnings

### Phase 4: UI Integration (3 hours)
- Strength indicator in CLI/web UI
- Real-time validation feedback
- Leak warnings
- Override options for advanced users

---

## Acceptance Criteria

### Core Functionality
- [ ] Validate key format before storage
- [ ] Calculate key strength score
- [ ] Check for leaked keys
- [ ] Provider-specific validation rules
- [ ] Clear error messages for each failure type

### User Experience
- [ ] Real-time validation feedback
- [ ] Strength indicator (weak/medium/strong)
- [ ] Actionable error messages
- [ ] Override option for advanced users
- [ ] Non-blocking for strong keys

### Security
- [ ] Never log actual keys (even partial)
- [ ] Use one-way hashing for leak checks
- [ ] Secure transmission of keys
- [ ] Audit all validation results

### Quality Gates
- [ ] Unit tests for all validation logic
- [ ] Integration tests with providers
- [ ] Performance: <100ms for format + strength
- [ ] Performance: <2s for leak detection
- [ ] Documentation for validation rules

---

## Technical Design

### Validation Pipeline
```
User enters key
      ↓
1. Format validation (fast, <10ms)
   ├─ Prefix check
   ├─ Length check
   └─ Pattern match
      ↓
2. Strength analysis (fast, <50ms)
   ├─ Entropy calculation
   ├─ Character diversity
   └─ Pattern detection
      ↓
3. Leak detection (slow, <2s)
   ├─ Hash key (SHA-256)
   ├─ Check HIBP API
   └─ Check GitHub API
      ↓
4. Provider API validation (slow, <500ms)
   └─ Real API call to provider
      ↓
5. Storage (fast, <50ms)
   ├─ Keychain storage
   └─ Database metadata
      ↓
Success!
```

### Error Handling
```python
class KeyValidationError(Exception):
    """Base class for key validation errors"""

class InvalidKeyFormatError(KeyValidationError):
    """Key format doesn't match provider requirements"""

class WeakKeyError(KeyValidationError):
    """Key strength below threshold"""

class LeakedKeyError(KeyValidationError):
    """Key found in public leak database"""

class InvalidKeyError(KeyValidationError):
    """Key rejected by provider API"""
```

### New Components
```
services/security/
  key_strength_analyzer.py      # NEW - Strength analysis
  key_leak_detector.py          # NEW - Leak detection
  provider_key_validator.py     # NEW - Format validation

config/
  key_validation_rules.yaml     # NEW - Validation config
```

---

## Example User Flows

### Flow 1: Weak Key Rejected
```bash
$ piper keys store openai sk-short

✗ Error: Key too weak

  Strength Analysis:
  - Length: 8/20 (too short)
  - Entropy: 3.2/5.0 (low randomness)
  - Character Diversity: 2/4 (missing symbols)
  - Overall: 45% (threshold: 70%)

  Recommendation: Use a properly formatted OpenAI key
  OpenAI keys start with "sk-" and are 51 characters long.

  Generate new key at: https://platform.openai.com/api-keys
```

### Flow 2: Leaked Key Warning
```bash
$ piper keys store github ghp_1234567890abcdef...

⚠️  WARNING: This key appears in public leak database!

Source: Have I Been Pwned (HIBP)
Severity: CRITICAL
Risk: This key is publicly known and should be rotated immediately.

✗ Storage blocked for security

Action Required:
1. Revoke this key at: https://github.com/settings/tokens
2. Generate a new key
3. Store the new key

This protection can't be disabled - leaked keys are never stored.
```

### Flow 3: Strong Key Accepted
```bash
$ piper keys store openai sk-proj-...

Validating key...
✓ Format valid (OpenAI key detected)
✓ Strength: 95% (strong)
✓ No leaks detected
✓ Provider API confirms validity

Success! Key stored securely.
- Strength: Strong (95%)
- Entropy: High
- Provider: OpenAI (gpt-4 access confirmed)
- Stored in: macOS Keychain

Next rotation recommended: January 20, 2026
```

---

## Success Metrics

### Security
- **Target**: 100% of leaked keys rejected
- **Measure**: Leak detection accuracy
- **Success**: No leaked keys in system

### User Protection
- **Target**: 90% of stored keys are "strong"
- **Measure**: Average strength score of stored keys
- **Success**: Mean strength >80%

### User Experience
- **Target**: <5% of valid keys rejected
- **Measure**: False positive rate
- **Success**: <5% users need to override

### Performance
- **Target**: Fast validation for most keys
- **Measure**: P95 validation time
- **Success**: P95 <2 seconds

---

## Dependencies

**Required**:
- ✅ #228: API Key Management (provides infrastructure)
- ✅ KeychainService (key storage)
- ❌ External APIs: HIBP, GitHub Secret Scanning

**Optional**:
- #249: Audit logging (log validation results)
- #218: Alpha onboarding (integrate into setup wizard)

---

## Configuration

```yaml
# config/key_validation_rules.yaml
validation:
  strength:
    enabled: true
    minimum_score: 0.7  # 70%
    allow_override: true  # For advanced users

  leak_detection:
    enabled: true
    services:
      - hibp  # Have I Been Pwned
      - github_secret_scanning
    cache_results: true
    cache_ttl_hours: 24

  format:
    enabled: true
    strict_mode: false  # If true, reject unrecognized formats

  providers:
    openai:
      prefix: "sk-"
      min_length: 50
      pattern: "^sk-[A-Za-z0-9]{48}$"

    anthropic:
      prefix: "sk-ant-"
      min_length: 100
      pattern: "^sk-ant-[A-Za-z0-9-_]{100,}$"

    github:
      prefixes: ["ghp_", "gho_", "ghu_"]
      min_length: 40
      pattern: "^gh[pou]_[A-Za-z0-9]{36}$"
```

---

## Time Estimate

**Total**: 12 hours

**Breakdown**:
- Format validation: 2 hours
- Strength analysis: 3 hours
- Leak detection: 4 hours
- UI integration: 3 hours

---

## Priority

**Priority**: Medium (security enhancement, not critical)
**Milestone**: Beta (post-Alpha)
**Sprint**: A8 or later

**Rationale**: Important for security, but Alpha users can validate manually. Add after core features complete.

---

## Related Issues

- #228: API Key Management (parent - provides infrastructure)
- #249: Audit Logging (validation results should be logged)
- #218: Alpha Onboarding (validation in setup wizard)

**Epic**: CORE-USERS (Multi-user & Security)
**Labels**: enhancement, security, component: security, priority: medium
