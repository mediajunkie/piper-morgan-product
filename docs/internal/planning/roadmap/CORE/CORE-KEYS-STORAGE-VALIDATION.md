# CORE-KEYS-STORAGE-VALIDATION: Add Strength Validation to Key Storage Workflow

**Sprint**: TBD (A8 or MVP)
**Priority**: Medium
**Effort**: 20-30 minutes
**Impact**: High (prevent weak keys at storage time)

---

## Problem

Issue #252 (CORE-KEYS-STRENGTH-VALIDATION) created comprehensive key validation infrastructure:

```python
# What exists now:
validator = KeyValidator()
report = await validator.validate_key(key, provider)
# Returns: format check, strength check, leak detection

# What's missing:
# - Integration with key storage workflow
# - Validation BEFORE storing keys
# - Warning users about weak keys
# - Blocking storage of invalid keys
```

Currently, key validation exists but isn't integrated into the key storage process. Users can store weak or invalid keys without any warnings.

**Result**: Weak keys may be stored without users knowing there's a problem.

---

## Proposed Solution

Integrate key validation into the key storage workflow so that:
1. **Every key** is validated before storage
2. **Weak keys** trigger warnings
3. **Invalid keys** are rejected
4. **Users informed** about validation results
5. **Storage prevented** for critical failures (optional override)

---

## Current Key Storage Flow

### Existing Storage Service

```python
# services/security/key_storage.py

class KeyStorage:
    """Store API keys in macOS Keychain"""

    async def store_key(
        self,
        provider: str,
        key_value: str,
        user_id: str
    ):
        """Store key - NO validation currently"""

        # Store directly in keychain
        keyring.set_password(
            f"piper-morgan-{provider}",
            user_id,
            key_value
        )

        # Log storage event
        await self._log_storage(user_id, provider)
```

**Status**: ✅ Storage works, ⏳ No validation

---

## Enhanced Storage with Validation

### 1. Validation-First Storage

```python
# Enhanced key storage with validation

class KeyStorage:
    """Store API keys with validation"""

    def __init__(self):
        self.validator = KeyValidator()  # From #252!

    async def store_key(
        self,
        provider: str,
        key_value: str,
        user_id: str,
        force: bool = False  # Allow override for weak keys
    ) -> StorageResult:
        """
        Store key with validation

        Args:
            provider: API provider name
            key_value: The API key to store
            user_id: User ID
            force: If True, store even if validation warnings

        Returns:
            StorageResult with validation report
        """

        # Step 1: Validate key
        validation = await self.validator.validate_key(key_value, provider)

        # Step 2: Handle validation results
        if validation.has_critical_issues():
            # Critical issues - refuse to store
            return StorageResult(
                success=False,
                validation_report=validation,
                message=f"Cannot store key: {', '.join(validation.critical_issues)}"
            )

        if validation.has_warnings() and not force:
            # Warnings - ask user to confirm
            return StorageResult(
                success=False,
                validation_report=validation,
                message="Key has validation warnings. Use --force to store anyway.",
                requires_confirmation=True
            )

        # Step 3: Store key
        try:
            keyring.set_password(
                f"piper-morgan-{provider}",
                user_id,
                key_value
            )

            # Log storage with validation results
            await self._log_storage(user_id, provider, validation)

            return StorageResult(
                success=True,
                validation_report=validation,
                message="Key stored successfully"
            )

        except Exception as e:
            return StorageResult(
                success=False,
                validation_report=validation,
                message=f"Storage failed: {e}"
            )
```

---

### 2. Validation Severity Levels

```python
class ValidationReport:
    """Validation report with severity classification"""

    def has_critical_issues(self) -> bool:
        """
        Critical issues that block storage:
        - Invalid format
        - Key too short
        - Known leaked key
        """
        return (
            not self.format_check.is_valid or
            self.strength_check.entropy < 4.0 or  # Very weak
            self.leak_check.is_leaked
        )

    def has_warnings(self) -> bool:
        """
        Warnings that should prompt user confirmation:
        - Weak but acceptable key
        - Missing leak check (HIBP unavailable)
        """
        return (
            self.strength_check.entropy < 6.0 or  # Weak
            self.leak_check.confidence == "low"
        )

    def get_storage_recommendation(self) -> StorageRecommendation:
        """Get storage recommendation"""
        if self.has_critical_issues():
            return StorageRecommendation.REJECT
        elif self.has_warnings():
            return StorageRecommendation.WARN
        else:
            return StorageRecommendation.ACCEPT
```

---

### 3. Interactive Storage CLI

```python
# CLI command with validation

async def store_key_interactive(provider: str, user_id: str):
    """Interactive key storage with validation"""

    print(f"\n🔐 Store API Key: {provider.capitalize()}\n")

    # Step 1: Get key from user
    key_value = input(f"Paste your {provider} API key: ").strip()

    # Step 2: Validate key
    print("\n🔍 Validating key...")

    storage = KeyStorage()
    result = await storage.store_key(provider, key_value, user_id)

    # Step 3: Handle validation results
    if result.success:
        print("\n✅ Key stored successfully!")
        print_validation_summary(result.validation_report)
        return

    # Step 4: Handle failures
    if result.validation_report.has_critical_issues():
        print("\n❌ Cannot store key - Critical issues found:\n")
        print_validation_details(result.validation_report)
        print("\n⚠️  Please generate a new key from your provider.")
        return

    # Step 5: Handle warnings
    if result.requires_confirmation:
        print("\n⚠️  Key has validation warnings:\n")
        print_validation_details(result.validation_report)

        confirm = input("\nStore anyway? (y/n): ")
        if confirm.lower() == 'y':
            # Store with force flag
            result = await storage.store_key(
                provider,
                key_value,
                user_id,
                force=True
            )
            if result.success:
                print("\n✅ Key stored (with warnings)")
            else:
                print(f"\n❌ Storage failed: {result.message}")
        else:
            print("\n❌ Storage cancelled")


def print_validation_details(report: ValidationReport):
    """Print detailed validation results"""

    # Format check
    if report.format_check.is_valid:
        print(f"  ✅ Format: Valid {report.format_check.pattern}")
    else:
        print(f"  ❌ Format: Invalid ({report.format_check.message})")

    # Strength check
    entropy = report.strength_check.entropy
    if entropy >= 6.0:
        print(f"  ✅ Strength: Strong ({entropy:.1f} bits/char)")
    elif entropy >= 4.0:
        print(f"  ⚠️  Strength: Weak ({entropy:.1f} bits/char)")
    else:
        print(f"  ❌ Strength: Very weak ({entropy:.1f} bits/char)")

    # Leak check
    if report.leak_check.is_leaked:
        print(f"  ❌ Leak: Key found in {report.leak_check.occurrences} breaches!")
    elif report.leak_check.confidence == "high":
        print(f"  ✅ Leak: No breaches detected")
    else:
        print(f"  ⚠️  Leak: Could not verify ({report.leak_check.message})")
```

---

### 4. Programmatic Storage with Validation

```python
# For programmatic key storage (e.g., from scripts)

async def store_key_programmatic(
    provider: str,
    key_value: str,
    user_id: str,
    strict: bool = True
) -> tuple[bool, str]:
    """
    Store key programmatically with validation

    Args:
        strict: If True, reject keys with any issues
                If False, only reject critical issues

    Returns:
        (success, message)
    """
    storage = KeyStorage()

    # Validate and store
    result = await storage.store_key(
        provider,
        key_value,
        user_id,
        force=not strict  # Force if not strict
    )

    if result.success:
        return True, "Key stored successfully"

    # Build error message
    issues = []
    if result.validation_report.has_critical_issues():
        issues.append("Critical validation failures")
    if result.validation_report.has_warnings():
        issues.append("Validation warnings (use strict=False to override)")

    return False, f"Storage failed: {', '.join(issues)}"
```

---

## Integration Points

### 1. CLI Commands

```python
# main.py

async def add_key_command(provider: str):
    """Add API key with validation"""
    user_id = await get_current_user_id()
    await store_key_interactive(provider, user_id)

# Usage:
# python main.py add-key openai
# python main.py add-key anthropic
```

---

### 2. Web UI Integration (Future)

```python
# web/routes/api_keys.py

@router.post("/keys/{provider}")
async def add_api_key(
    provider: str,
    key: str = Body(...),
    force: bool = Body(False),
    user_id: str = Depends(get_current_user)
):
    """Store API key with validation (API endpoint)"""

    storage = KeyStorage()
    result = await storage.store_key(provider, key, user_id, force)

    if result.success:
        return {
            "success": True,
            "message": result.message,
            "validation": result.validation_report.to_dict()
        }

    if result.requires_confirmation:
        return JSONResponse(
            status_code=422,  # Unprocessable Entity
            content={
                "success": False,
                "message": result.message,
                "requires_confirmation": True,
                "validation": result.validation_report.to_dict()
            }
        )

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": result.message,
            "validation": result.validation_report.to_dict()
        }
    )
```

---

### 3. Rotation Workflow Integration

```python
# From CORE-KEYS-ROTATION-WORKFLOW (when implemented)

async def rotate_key_with_validation(provider: str, user_id: str):
    """Rotate key with validation"""

    # Get new key from user
    new_key = input("Paste new API key: ")

    # Validate BEFORE storing (integration!)
    storage = KeyStorage()
    result = await storage.store_key(provider, new_key, user_id)

    if not result.success:
        print(f"❌ New key validation failed: {result.message}")
        return False

    # Continue with rotation...
    return True
```

---

## Acceptance Criteria

### Functional Requirements
- [ ] All key storage validates before storing
- [ ] Critical issues block storage
- [ ] Warnings allow user override with `--force`
- [ ] Validation results logged to audit system
- [ ] CLI provides clear validation feedback
- [ ] Programmatic storage supports strict/permissive modes

### Validation Requirements
- [ ] Format validation integrated
- [ ] Strength validation integrated
- [ ] Leak detection integrated
- [ ] Severity levels properly categorized
- [ ] Recommendations actionable

### User Experience
- [ ] Clear error messages for invalid keys
- [ ] Helpful guidance for weak keys
- [ ] Easy override for warnings
- [ ] Success confirmation with summary

---

## Testing

### Unit Tests

```python
async def test_store_valid_key():
    """Test storing a valid key"""
    storage = KeyStorage()

    result = await storage.store_key(
        'openai',
        'sk-' + secrets.token_urlsafe(32),
        test_user_id
    )

    assert result.success is True
    assert not result.validation_report.has_critical_issues()

async def test_reject_invalid_key():
    """Test rejecting invalid format key"""
    storage = KeyStorage()

    result = await storage.store_key(
        'openai',
        'invalid-key',
        test_user_id
    )

    assert result.success is False
    assert result.validation_report.has_critical_issues()

async def test_warn_on_weak_key():
    """Test warning on weak key"""
    storage = KeyStorage()

    result = await storage.store_key(
        'openai',
        'sk-weakkey123',  # Weak but valid format
        test_user_id
    )

    assert result.success is False  # Without force
    assert result.requires_confirmation is True

    # Now with force
    result = await storage.store_key(
        'openai',
        'sk-weakkey123',
        test_user_id,
        force=True
    )

    assert result.success is True  # Stored with force

async def test_reject_leaked_key():
    """Test rejecting leaked key"""
    storage = KeyStorage()

    # Test with known weak pattern
    result = await storage.store_key(
        'openai',
        'sk-test-demo-key',  # Known test pattern
        test_user_id
    )

    assert result.success is False
    assert result.validation_report.leak_check.is_leaked
```

---

## Security Considerations

### Validation Before Storage

**Key principle**: Never store invalid or leaked keys

```python
CRITICAL_VALIDATIONS = [
    'format_invalid',      # Wrong format for provider
    'entropy_too_low',     # < 4.0 bits/char
    'known_leaked',        # Found in breach database
    'test_key_pattern'     # Matches test/demo patterns
]

def has_critical_issues(report: ValidationReport) -> bool:
    """Critical issues that MUST block storage"""
    for issue_type in CRITICAL_VALIDATIONS:
        if report.has_issue(issue_type):
            return True
    return False
```

---

### Audit Logging

```python
async def _log_storage(
    self,
    user_id: str,
    provider: str,
    validation: ValidationReport
):
    """Log key storage with validation results"""

    await audit_log.record_event(
        user_id=user_id,
        event_type='key_storage',
        details={
            'provider': provider,
            'format_valid': validation.format_check.is_valid,
            'strength_score': validation.strength_check.entropy,
            'leak_detected': validation.leak_check.is_leaked,
            'forced': validation.has_warnings()  # Was force flag used?
        }
    )
```

---

## Related Issues

- **#252: CORE-KEYS-STRENGTH-VALIDATION** - Key validation infrastructure
- **CORE-KEYS-ROTATION-WORKFLOW** - Will integrate with validation
- **Key storage service** - Core integration point

---

## Future Enhancements

### Phase 2
- Automatic strength improvement suggestions
- Key generation assistance
- Provider-specific security best practices

### Phase 3 (MVP)
- Batch key validation
- Periodic re-validation of stored keys
- Security score tracking over time

---

## Success Metrics

- 0% invalid keys stored (100% format validation)
- <1% weak keys stored (strong defaults)
- User satisfaction with validation feedback
- Reduced security incidents from weak keys

---

**Sprint**: TBD
**Milestone**: TBD (A8 or MVP)
**Labels**: security, enhancement, validation, key-management
**Estimated Effort**: 20-30 minutes
