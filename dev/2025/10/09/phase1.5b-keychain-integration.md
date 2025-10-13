# Phase 1.5 Sub-Phase B: Keychain Integration with LLMConfigService

**Issue**: #217 - CORE-LLM-CONFIG
**Phase**: 1.5B of 4 - Keychain Integration
**Agent**: Code Agent
**Date**: October 9, 2025, 8:09 PM
**Time Estimate**: 45-60 minutes
**Priority**: HIGH - Security implementation

---

## Mission

Integrate KeychainService with LLMConfigService to enable secure API key storage with automatic fallback to environment variables during migration.

---

## Context from Sub-Phase A

**✅ Completed**:
- KeychainService created (241 lines)
- 10/10 tests passing
- Real macOS Keychain integration verified

**Now**: Update LLMConfigService to use KeychainService as primary storage, with env vars as fallback.

---

## Architecture Design

### Current Flow (Insecure)
```
LLMConfigService → os.environ → .env file (plaintext) ❌
```

### Target Flow (Secure)
```
LLMConfigService → KeychainService → macOS Keychain (encrypted) ✅
                   ↓ (if not found)
                   → os.environ → .env file (migration fallback)
```

### Fallback Strategy
```python
def get_api_key(provider: str) -> Optional[str]:
    # Priority 1: Try keychain (secure)
    key = keychain_service.get_api_key(provider)
    if key:
        return key

    # Priority 2: Try environment (migration fallback)
    key = os.getenv(f"{provider.upper()}_API_KEY")
    if key:
        logger.warning(f"{provider} key from ENV - migrate to keychain")
        return key

    return None
```

---

## Sub-Phase B Tasks

### Task 1: Update LLMConfigService (30 min)

**File**: `services/config/llm_config_service.py` (MODIFY)

**Changes Required**:

#### 1.1 Add KeychainService Import
```python
from services.infrastructure.keychain_service import KeychainService
```

#### 1.2 Add KeychainService to __init__
```python
def __init__(self, keychain_service: Optional[KeychainService] = None):
    """
    Initialize LLM configuration service

    Args:
        keychain_service: Optional KeychainService for testing
    """
    self._keychain_service = keychain_service or KeychainService()
    # ... existing code ...
```

#### 1.3 Update get_api_key Method
**Find existing get_api_key method** and replace with:

```python
def get_api_key(self, provider: str) -> Optional[str]:
    """
    Get API key for provider with keychain-first fallback

    Tries keychain first (secure), falls back to environment
    variables for migration support.

    Args:
        provider: Provider name (openai, anthropic, gemini, perplexity)

    Returns:
        API key if found, None otherwise
    """
    # Priority 1: Try keychain (secure storage)
    key = self._keychain_service.get_api_key(provider)
    if key:
        logger.debug(f"Retrieved {provider} key from keychain (secure)")
        return key

    # Priority 2: Try environment (migration fallback)
    env_var = f"{provider.upper()}_API_KEY"
    key = os.getenv(env_var)
    if key:
        logger.warning(
            f"{provider} key retrieved from environment variable",
            env_var=env_var,
            recommendation="Migrate to keychain for security"
        )
        return key

    # Not found in either location
    logger.debug(f"No API key found for {provider}")
    return None
```

#### 1.4 Add Migration Helper Method
**Add new method** to LLMConfigService:

```python
def get_migration_status(self) -> Dict[str, Any]:
    """
    Get migration status for all providers

    Shows which keys are in keychain vs environment to help
    with migration planning.

    Returns:
        Dict with migration status for each provider
    """
    providers = ["openai", "anthropic", "gemini", "perplexity"]
    status = self._keychain_service.check_migration_status(providers)

    summary = {
        "total_providers": len(providers),
        "in_keychain": sum(1 for s in status.values() if s.exists_in_keychain),
        "in_env": sum(1 for s in status.values() if s.exists_in_env),
        "missing": sum(1 for s in status.values() if not s.exists_in_keychain and not s.exists_in_env),
        "needs_migration": sum(1 for s in status.values() if s.exists_in_env and not s.exists_in_keychain),
        "providers": status
    }

    return summary

def migrate_key_to_keychain(self, provider: str) -> bool:
    """
    Migrate API key from environment to keychain

    Reads key from environment variable and stores it securely
    in keychain. Does not delete from environment (manual step).

    Args:
        provider: Provider name to migrate

    Returns:
        True if migration successful, False otherwise
    """
    # Get key from environment
    env_var = f"{provider.upper()}_API_KEY"
    key = os.getenv(env_var)

    if not key:
        logger.warning(f"No {provider} key in environment to migrate")
        return False

    # Store in keychain
    try:
        self._keychain_service.store_api_key(provider, key)
        logger.info(
            f"Migrated {provider} key to keychain",
            provider=provider,
            recommendation=f"Remove {env_var} from .env file"
        )
        return True
    except Exception as e:
        logger.error(f"Failed to migrate {provider} key: {e}")
        return False
```

**Acceptance Criteria**:
- [ ] KeychainService imported
- [ ] KeychainService injected in __init__
- [ ] get_api_key updated with fallback logic
- [ ] get_migration_status method added
- [ ] migrate_key_to_keychain method added
- [ ] All logging statements updated

---

### Task 2: Update LLMConfigService Tests (20 min)

**File**: `tests/config/test_llm_config_service.py` (MODIFY)

#### 2.1 Add Keychain Mocking
**At top of file**, add:
```python
from unittest.mock import Mock, patch, MagicMock
from services.infrastructure.keychain_service import KeychainService
```

#### 2.2 Add Keychain Fixture
**Add new fixture**:
```python
@pytest.fixture
def mock_keychain_service():
    """Mock KeychainService for testing"""
    mock = Mock(spec=KeychainService)
    mock.get_api_key.return_value = None  # Default: nothing in keychain
    mock.store_api_key.return_value = None
    mock.check_migration_status.return_value = {}
    return mock
```

#### 2.3 Update Existing Tests to Use Mock
**Update existing config_service fixture** to inject mock keychain:
```python
@pytest.fixture
def config_service(mock_keychain_service):
    """Create LLMConfigService with mocked keychain"""
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "ANTHROPIC_API_KEY": "test-anthropic-key",
    }):
        service = LLMConfigService(keychain_service=mock_keychain_service)
        yield service
```

#### 2.4 Add New Tests for Keychain Integration
**Add these new test methods**:

```python
class TestKeychainIntegration:
    """Test keychain integration with LLMConfigService"""

    def test_get_api_key_from_keychain(self, mock_keychain_service):
        """Retrieves key from keychain when available"""
        mock_keychain_service.get_api_key.return_value = "keychain-key"

        service = LLMConfigService(keychain_service=mock_keychain_service)
        key = service.get_api_key("openai")

        assert key == "keychain-key"
        mock_keychain_service.get_api_key.assert_called_once_with("openai")

    def test_get_api_key_falls_back_to_env(self, mock_keychain_service):
        """Falls back to environment when not in keychain"""
        mock_keychain_service.get_api_key.return_value = None

        with patch.dict(os.environ, {"OPENAI_API_KEY": "env-key"}):
            service = LLMConfigService(keychain_service=mock_keychain_service)
            key = service.get_api_key("openai")

        assert key == "env-key"

    def test_keychain_preferred_over_env(self, mock_keychain_service):
        """Keychain takes priority over environment"""
        mock_keychain_service.get_api_key.return_value = "keychain-key"

        with patch.dict(os.environ, {"OPENAI_API_KEY": "env-key"}):
            service = LLMConfigService(keychain_service=mock_keychain_service)
            key = service.get_api_key("openai")

        # Should get keychain version, not env
        assert key == "keychain-key"

    def test_get_migration_status(self, mock_keychain_service):
        """Returns migration status for all providers"""
        from services.infrastructure.keychain_service import KeychainEntry

        mock_keychain_service.check_migration_status.return_value = {
            "openai": KeychainEntry("openai", True, False),
            "anthropic": KeychainEntry("anthropic", False, True),
            "gemini": KeychainEntry("gemini", False, False),
        }

        service = LLMConfigService(keychain_service=mock_keychain_service)
        status = service.get_migration_status()

        assert status["in_keychain"] == 1
        assert status["in_env"] == 1
        assert status["missing"] == 1

    def test_migrate_key_to_keychain_success(self, mock_keychain_service):
        """Can migrate key from environment to keychain"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "env-key"}):
            service = LLMConfigService(keychain_service=mock_keychain_service)
            result = service.migrate_key_to_keychain("openai")

        assert result is True
        mock_keychain_service.store_api_key.assert_called_once_with(
            "openai", "env-key"
        )

    def test_migrate_key_no_env_key(self, mock_keychain_service):
        """Migration fails gracefully when no env key"""
        service = LLMConfigService(keychain_service=mock_keychain_service)
        result = service.migrate_key_to_keychain("nonexistent")

        assert result is False
        mock_keychain_service.store_api_key.assert_not_called()
```

**Acceptance Criteria**:
- [ ] Mock keychain service fixture created
- [ ] Existing tests updated to use mock
- [ ] 6+ new keychain integration tests added
- [ ] All tests passing

---

### Task 3: Update LLMDomainService Tests (10 min)

**File**: `tests/domain/test_llm_domain_service.py` (MODIFY)

**Update mock_config_service fixture** to include keychain:
```python
@pytest.fixture
def mock_config_service():
    """Mock LLMConfigService"""
    mock = Mock()
    mock.get_available_providers.return_value = ["openai", "gemini"]
    mock.get_default_provider.return_value = "openai"
    mock.get_api_key.return_value = "test-key"  # Now comes from keychain or env
    mock.validate_all_providers = AsyncMock(return_value={
        "openai": Mock(is_valid=True),
        "gemini": Mock(is_valid=True)
    })
    return mock
```

**No other changes needed** - mocking hides the keychain complexity.

**Acceptance Criteria**:
- [ ] Mock updated to reflect keychain integration
- [ ] All 15 domain tests still passing

---

## Verification Commands

### After Task 1 (Service Update)
```bash
# Verify import works
python -c "
from services.config.llm_config_service import LLMConfigService
from services.infrastructure.keychain_service import KeychainService
print('✅ Imports work')
"

# Quick integration test
python -c "
from services.config.llm_config_service import LLMConfigService
import os
os.environ['OPENAI_API_KEY'] = 'test-key'
service = LLMConfigService()
key = service.get_api_key('openai')
assert key == 'test-key', 'Fallback to env failed'
print('✅ Fallback logic works')
"

# Test migration status
python -c "
from services.config.llm_config_service import LLMConfigService
service = LLMConfigService()
status = service.get_migration_status()
print(f'✅ Migration status: {status}')
"
```

### After Task 2 (Config Tests)
```bash
# Run config service tests
pytest tests/config/test_llm_config_service.py -v

# Should see 35 existing + 6 new = 41 tests passing
```

### After Task 3 (Domain Tests)
```bash
# Run domain service tests
pytest tests/domain/test_llm_domain_service.py -v

# Should see 15 tests still passing
```

### Full Test Suite
```bash
# Run all tests
pytest tests/ -v

# Expected: 66+ tests passing (58 existing + 6 new keychain + infrastructure)
```

---

## Success Criteria

Sub-Phase B complete when:
- [ ] LLMConfigService uses KeychainService
- [ ] Fallback to environment variables working
- [ ] Migration helper methods implemented
- [ ] 6+ new integration tests added
- [ ] All existing tests updated and passing
- [ ] All domain tests still passing
- [ ] Total: 66+ tests passing

---

## Evidence Format

```markdown
# Sub-Phase B Completion Report

## Task 1: LLMConfigService Integration ✅

**Changes Made**:
- Added KeychainService import
- Injected KeychainService in __init__
- Updated get_api_key with fallback logic
- Added get_migration_status method
- Added migrate_key_to_keychain method

**Verification**:
```bash
$ python -c "from services.config.llm_config_service import LLMConfigService; ..."
✅ Imports work
✅ Fallback logic works
✅ Migration status: {...}
```

## Task 2: Config Tests Updated ✅

**Tests Added**:
- test_get_api_key_from_keychain ✅
- test_get_api_key_falls_back_to_env ✅
- test_keychain_preferred_over_env ✅
- test_get_migration_status ✅
- test_migrate_key_to_keychain_success ✅
- test_migrate_key_no_env_key ✅

**Results**:
```bash
$ pytest tests/config/test_llm_config_service.py -v
=========== 41 passed in 2.13s ===========
```

## Task 3: Domain Tests Updated ✅

**Changes Made**:
- Updated mock_config_service fixture

**Results**:
```bash
$ pytest tests/domain/test_llm_domain_service.py -v
=========== 15 passed in 0.45s ===========
```

## Full Test Suite ✅

```bash
$ pytest tests/ -v
=========== 66 passed in 4.28s ===========
```

## Success Criteria: 7/7 ✅

All criteria met - Ready for Sub-Phase C (Migration CLI)
```

---

## Important Notes

1. **Backwards Compatible**: Environment variables still work (migration period)
2. **Security Priority**: Keychain checked first, env is fallback
3. **Migration Helpers**: Tools to move from env to keychain
4. **No Breaking Changes**: All existing code continues working
5. **Warning Logs**: Clear indication when using env vars (migrate!)

---

## Time Breakdown

| Task | Description | Time |
|------|-------------|------|
| 1 | Update LLMConfigService | 30 min |
| 2 | Update config tests | 20 min |
| 3 | Update domain tests | 10 min |

**Total**: 60 minutes

---

**After completion, we'll proceed to Sub-Phase C (Migration CLI)**

---

*Sub-Phase 1.5B - October 9, 2025, 8:09 PM*
