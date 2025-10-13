# Phase 1.5 Sub-Phase A: Keyring Library Setup & Testing

**Issue**: #217 - CORE-LLM-CONFIG
**Phase**: 1.5A of 4 - Secure Storage Foundation
**Agent**: Code Agent
**Date**: October 9, 2025, 7:52 PM
**Time Estimate**: 45-60 minutes
**Priority**: HIGH - Security concern (plaintext API keys)

---

## Mission

Set up Python `keyring` library for secure OS keychain storage, verify it works on macOS, and create wrapper service for API key storage/retrieval.

---

## Context

**Security Problem**: API keys currently stored in plaintext `.env` file
**Solution**: Move to encrypted OS keychain (macOS Keychain)
**Approach**: Use `keyring` library with proper abstraction layer

**Current Architecture** (from Phases 1-3):
```
LLMDomainService → LLMConfigService → os.environ (plaintext .env)
                                      ↓
                                   INSECURE ❌
```

**Target Architecture**:
```
LLMDomainService → LLMConfigService → KeychainService → OS Keychain
                                                         ↓
                                                      SECURE ✅
```

---

## Sub-Phase A Tasks

### Task 1: Install and Verify Keyring Library (10 min)

**Install keyring**:
```bash
# Install with macOS backend support
pip install keyring --break-system-packages

# Verify installation
python -c "import keyring; print(keyring.get_keyring())"
# Expected output: macOS keychain backend

# Check version
pip show keyring
```

**Test basic functionality**:
```bash
# Create test script
cat > /tmp/test_keyring.py << 'EOF'
import keyring

# Test set
keyring.set_password("piper-test", "test-key", "test-value")
print("✅ Set test password")

# Test get
value = keyring.get_password("piper-test", "test-key")
assert value == "test-value", f"Expected 'test-value', got '{value}'"
print(f"✅ Retrieved: {value}")

# Test delete
keyring.delete_password("piper-test", "test-key")
print("✅ Deleted test password")

# Verify deleted
value = keyring.get_password("piper-test", "test-key")
assert value is None, f"Expected None, got '{value}'"
print("✅ Verified deletion")

print("\n🎉 Keyring library working correctly!")
EOF

python /tmp/test_keyring.py
```

**Acceptance Criteria**:
- [ ] keyring library installed
- [ ] macOS backend detected
- [ ] Can set passwords
- [ ] Can retrieve passwords
- [ ] Can delete passwords
- [ ] Test script passes completely

---

### Task 2: Create KeychainService (30 min)

**File**: `services/infrastructure/keychain_service.py` (NEW)

**Implementation**:
```python
"""
Keychain Service for Secure API Key Storage

Provides abstraction over OS keychain for secure storage of API keys
and other sensitive credentials. Uses Python keyring library with
macOS Keychain backend.

Security Features:
- Encrypted storage via OS keychain
- No plaintext credentials in memory longer than necessary
- Automatic fallback to environment variables during migration
- Comprehensive error handling and logging
"""

from typing import Optional, Dict, List
import keyring
import structlog
from dataclasses import dataclass

logger = structlog.get_logger(__name__)

# Service name for keychain entries
SERVICE_NAME = "piper-morgan"


@dataclass
class KeychainEntry:
    """Represents a keychain entry"""
    key: str
    exists_in_keychain: bool
    exists_in_env: bool


class KeychainService:
    """
    Service for secure API key storage in OS keychain

    Provides high-level interface for storing and retrieving
    API keys securely. Handles migration from environment
    variables to keychain storage.

    Usage:
        keychain = KeychainService()

        # Store API key
        keychain.store_api_key("openai", "sk-...")

        # Retrieve API key
        key = keychain.get_api_key("openai")
    """

    def __init__(self, service_name: str = SERVICE_NAME):
        """
        Initialize keychain service

        Args:
            service_name: Service identifier for keychain entries
        """
        self.service_name = service_name
        self._verify_keyring_backend()

    def _verify_keyring_backend(self) -> None:
        """Verify keyring backend is available"""
        try:
            backend = keyring.get_keyring()
            logger.info(
                "Keychain service initialized",
                backend=backend.__class__.__name__,
                service_name=self.service_name
            )
        except Exception as e:
            logger.error(f"Failed to initialize keyring: {e}")
            raise RuntimeError(f"Keyring initialization failed: {e}")

    def store_api_key(self, provider: str, api_key: str) -> None:
        """
        Store API key securely in keychain

        Args:
            provider: Provider name (e.g., "openai", "anthropic")
            api_key: API key to store

        Raises:
            ValueError: If provider or api_key is empty
            RuntimeError: If storage fails
        """
        if not provider:
            raise ValueError("Provider name cannot be empty")
        if not api_key:
            raise ValueError("API key cannot be empty")

        try:
            keyring.set_password(
                self.service_name,
                self._get_key_name(provider),
                api_key
            )
            logger.info(f"Stored API key for {provider} in keychain")
        except Exception as e:
            logger.error(f"Failed to store API key for {provider}: {e}")
            raise RuntimeError(f"Failed to store API key: {e}")

    def get_api_key(self, provider: str) -> Optional[str]:
        """
        Retrieve API key from keychain

        Args:
            provider: Provider name (e.g., "openai", "anthropic")

        Returns:
            API key if found, None otherwise
        """
        if not provider:
            return None

        try:
            key = keyring.get_password(
                self.service_name,
                self._get_key_name(provider)
            )
            if key:
                logger.debug(f"Retrieved API key for {provider} from keychain")
            return key
        except Exception as e:
            logger.error(f"Failed to retrieve API key for {provider}: {e}")
            return None

    def delete_api_key(self, provider: str) -> bool:
        """
        Delete API key from keychain

        Args:
            provider: Provider name

        Returns:
            True if deleted, False if not found or error
        """
        if not provider:
            return False

        try:
            keyring.delete_password(
                self.service_name,
                self._get_key_name(provider)
            )
            logger.info(f"Deleted API key for {provider} from keychain")
            return True
        except keyring.errors.PasswordDeleteError:
            logger.debug(f"No API key found for {provider} to delete")
            return False
        except Exception as e:
            logger.error(f"Failed to delete API key for {provider}: {e}")
            return False

    def list_stored_keys(self) -> List[str]:
        """
        List all providers with keys stored in keychain

        Note: keyring doesn't provide a list API, so this returns
        known providers that we check for.

        Returns:
            List of provider names with stored keys
        """
        known_providers = ["openai", "anthropic", "gemini", "perplexity"]
        stored = []

        for provider in known_providers:
            if self.get_api_key(provider) is not None:
                stored.append(provider)

        return stored

    def check_migration_status(self, providers: List[str]) -> Dict[str, KeychainEntry]:
        """
        Check migration status for given providers

        Checks both keychain and environment variables to determine
        which keys need to be migrated.

        Args:
            providers: List of provider names to check

        Returns:
            Dict mapping provider to KeychainEntry status
        """
        import os

        status = {}
        for provider in providers:
            keychain_key = self.get_api_key(provider)
            env_key = os.getenv(self._get_env_var_name(provider))

            status[provider] = KeychainEntry(
                key=provider,
                exists_in_keychain=keychain_key is not None,
                exists_in_env=env_key is not None
            )

        return status

    def _get_key_name(self, provider: str) -> str:
        """
        Get keychain entry name for provider

        Args:
            provider: Provider name

        Returns:
            Keychain entry name
        """
        return f"{provider}_api_key"

    def _get_env_var_name(self, provider: str) -> str:
        """
        Get environment variable name for provider

        Args:
            provider: Provider name

        Returns:
            Environment variable name
        """
        return f"{provider.upper()}_API_KEY"


# Convenience instance for global access
_keychain_service = None


def get_keychain_service() -> KeychainService:
    """
    Get global keychain service instance

    Returns:
        KeychainService instance
    """
    global _keychain_service
    if _keychain_service is None:
        _keychain_service = KeychainService()
    return _keychain_service
```

**Acceptance Criteria**:
- [ ] File created at services/infrastructure/keychain_service.py
- [ ] All methods implemented
- [ ] Comprehensive docstrings
- [ ] Type hints throughout
- [ ] Error handling robust
- [ ] Logging included

---

### Task 3: Create Keychain Service Tests (20 min)

**File**: `tests/infrastructure/test_keychain_service.py` (NEW)

**Create test directory if needed**:
```bash
mkdir -p tests/infrastructure
touch tests/infrastructure/__init__.py
```

**Implementation**:
```python
"""Tests for KeychainService"""

import pytest
import keyring
from unittest.mock import Mock, patch
from services.infrastructure.keychain_service import (
    KeychainService,
    KeychainEntry,
    get_keychain_service
)


class TestKeychainService:
    """Test keychain service functionality"""

    @pytest.fixture
    def service(self):
        """Create keychain service for testing"""
        return KeychainService(service_name="piper-test")

    @pytest.fixture(autouse=True)
    def cleanup(self, service):
        """Clean up test keys after each test"""
        yield
        # Clean up any test keys
        for provider in ["test-provider", "openai", "anthropic"]:
            try:
                service.delete_api_key(provider)
            except:
                pass

    def test_store_and_retrieve_api_key(self, service):
        """Can store and retrieve API key"""
        service.store_api_key("test-provider", "test-key-123")

        retrieved = service.get_api_key("test-provider")
        assert retrieved == "test-key-123"

    def test_retrieve_nonexistent_key(self, service):
        """Returns None for nonexistent key"""
        result = service.get_api_key("nonexistent-provider")
        assert result is None

    def test_delete_api_key(self, service):
        """Can delete API key"""
        service.store_api_key("test-provider", "test-key")
        assert service.get_api_key("test-provider") == "test-key"

        deleted = service.delete_api_key("test-provider")
        assert deleted is True
        assert service.get_api_key("test-provider") is None

    def test_delete_nonexistent_key(self, service):
        """Deleting nonexistent key returns False"""
        result = service.delete_api_key("nonexistent-provider")
        assert result is False

    def test_store_empty_provider_raises_error(self, service):
        """Empty provider name raises ValueError"""
        with pytest.raises(ValueError, match="Provider name cannot be empty"):
            service.store_api_key("", "test-key")

    def test_store_empty_key_raises_error(self, service):
        """Empty API key raises ValueError"""
        with pytest.raises(ValueError, match="API key cannot be empty"):
            service.store_api_key("test-provider", "")

    def test_list_stored_keys(self, service):
        """Lists providers with stored keys"""
        service.store_api_key("openai", "test-key-1")
        service.store_api_key("anthropic", "test-key-2")

        stored = service.list_stored_keys()
        assert "openai" in stored
        assert "anthropic" in stored

    def test_check_migration_status(self, service):
        """Checks migration status correctly"""
        # Store one key in keychain
        service.store_api_key("openai", "test-key")

        # Mock environment variable for another
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'env-key'}):
            status = service.check_migration_status(["openai", "anthropic", "gemini"])

        assert status["openai"].exists_in_keychain is True
        assert status["openai"].exists_in_env is False

        assert status["anthropic"].exists_in_keychain is False
        assert status["anthropic"].exists_in_env is True

        assert status["gemini"].exists_in_keychain is False
        assert status["gemini"].exists_in_env is False

    def test_get_keychain_service_singleton(self):
        """Global keychain service is singleton"""
        service1 = get_keychain_service()
        service2 = get_keychain_service()
        assert service1 is service2


class TestKeychainIntegration:
    """Integration tests with actual keychain"""

    def test_real_keychain_roundtrip(self):
        """Can store and retrieve from real macOS keychain"""
        service = KeychainService(service_name="piper-test-integration")

        # Store
        service.store_api_key("integration-test", "secret-key-123")

        # Retrieve
        retrieved = service.get_api_key("integration-test")
        assert retrieved == "secret-key-123"

        # Clean up
        service.delete_api_key("integration-test")
        assert service.get_api_key("integration-test") is None
```

**Acceptance Criteria**:
- [ ] Test file created
- [ ] All unit tests implemented (10+ tests)
- [ ] Integration test with real keychain
- [ ] Proper cleanup after tests
- [ ] All tests passing

---

## Verification Commands

### After Task 1 (Library Setup)
```bash
# Verify installation
pip show keyring

# Run test script
python /tmp/test_keyring.py
# Expected: ✅ All checks passing
```

### After Task 2 (Service Creation)
```bash
# Verify import
python -c "from services.infrastructure.keychain_service import KeychainService; print('✅ Import works')"

# Quick functionality test
python -c "
from services.infrastructure.keychain_service import KeychainService
ks = KeychainService(service_name='piper-test-quick')
ks.store_api_key('test', 'value')
assert ks.get_api_key('test') == 'value'
ks.delete_api_key('test')
print('✅ KeychainService works')
"
```

### After Task 3 (Tests)
```bash
# Run keychain service tests
pytest tests/infrastructure/test_keychain_service.py -v

# Expected: 11+ tests passing
```

---

## Success Criteria

Sub-Phase A complete when:
- [ ] keyring library installed and verified
- [ ] KeychainService implemented (200+ lines)
- [ ] All methods working (store, get, delete, list, check_migration)
- [ ] 11+ tests created
- [ ] All tests passing
- [ ] Integration test with real keychain passing
- [ ] Service can be imported and used

---

## Evidence Format

```markdown
# Sub-Phase A Completion Report

## Task 1: Library Setup ✅

### Installation
```bash
$ pip install keyring --break-system-packages
Successfully installed keyring-24.x.x

$ python -c "import keyring; print(keyring.get_keyring())"
<keyring.backends.macOS.Keyring object at 0x...>
```

### Functionality Test
```bash
$ python /tmp/test_keyring.py
✅ Set test password
✅ Retrieved: test-value
✅ Deleted test password
✅ Verified deletion
🎉 Keyring library working correctly!
```

## Task 2: KeychainService ✅

**File Created**: services/infrastructure/keychain_service.py (248 lines)

**Methods Implemented**:
- store_api_key() - ✅ Working
- get_api_key() - ✅ Working
- delete_api_key() - ✅ Working
- list_stored_keys() - ✅ Working
- check_migration_status() - ✅ Working

**Quick Test**:
```bash
$ python -c "from services.infrastructure.keychain_service import KeychainService; ..."
✅ KeychainService works
```

## Task 3: Tests ✅

**File Created**: tests/infrastructure/test_keychain_service.py (150+ lines)

**Test Results**:
```bash
$ pytest tests/infrastructure/test_keychain_service.py -v
=========== 11 passed in 1.23s ===========
```

**Tests Created**:
- test_store_and_retrieve_api_key ✅
- test_retrieve_nonexistent_key ✅
- test_delete_api_key ✅
- test_delete_nonexistent_key ✅
- test_store_empty_provider_raises_error ✅
- test_store_empty_key_raises_error ✅
- test_list_stored_keys ✅
- test_check_migration_status ✅
- test_get_keychain_service_singleton ✅
- test_real_keychain_roundtrip ✅ (integration)

## Success Criteria: 9/9 ✅

All criteria met - Ready for Sub-Phase B
```

---

## Important Notes

1. **macOS Keychain**: First access will prompt for keychain password
2. **Test Cleanup**: Always clean up test entries
3. **Service Name**: Use "piper-morgan" in production, "piper-test" in tests
4. **Error Handling**: Robust error handling for all keyring operations
5. **Logging**: Use structlog for consistency

---

## Time Breakdown

| Task | Description | Time |
|------|-------------|------|
| 1 | Install and verify keyring | 10 min |
| 2 | Create KeychainService | 30 min |
| 3 | Create tests | 20 min |

**Total**: 60 minutes

---

**After completion, we'll proceed to Sub-Phase B (LLMConfigService integration)**

---

*Sub-Phase 1.5A - October 9, 2025, 7:52 PM*
