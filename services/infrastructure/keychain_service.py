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

from dataclasses import dataclass
from typing import Dict, List, Optional

import os

import keyring
import structlog

logger = structlog.get_logger(__name__)

# Service name for keychain entries
SERVICE_NAME = "piper-morgan"

# CLI session token provider name (Issue #397)
CLI_SESSION_PROVIDER = "cli_session"


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
        # #1382: the encrypted-DB fallback store, active when the OS keyring has no
        # real backend (hosted Linux resolves to keyring.backends.fail.Keyring —
        # init "succeeds" there while every operation raises; found live on alpha
        # 2026-07-08). None = OS keychain in use (the local-dev/Mac path, unchanged).
        self._db_store = None
        # #1382: when NO secure store exists (dead OS backend + no ENCRYPTION_MASTER_KEY),
        # this holds the reason string. Construction must not raise — module-level
        # singletons (services/llm/clients.py) construct this at import, so a raise
        # here detonates test collection on any keyring-less machine. Fail-closed
        # moves to the operations: writes raise, reads return None (truthfully empty).
        self._no_secure_store: Optional[str] = None
        self._verify_keyring_backend()

    def _verify_keyring_backend(self) -> None:
        """Verify keyring backend availability and select the credential store.

        Selection (#1382): env PIPER_CREDENTIAL_STORE=db forces the encrypted-DB
        store; =keychain forces the OS keyring (legacy behavior incl. its failure
        mode); unset → auto: a dead/fail backend with a field encryptor available
        routes to the DB store. Dead backend AND no encryptor → hard error (fail
        closed — there is nowhere secure to put a secret).
        """
        forced = os.getenv("PIPER_CREDENTIAL_STORE", "").strip().lower()
        try:
            backend = keyring.get_keyring()
            backend_name = backend.__class__.__name__
            backend_dead = "fail" in backend.__class__.__module__ or forced == "db"
        except Exception as e:
            if forced == "keychain":
                logger.error(f"Failed to initialize keyring: {e}")
                raise RuntimeError(f"Keyring initialization failed: {e}")
            backend_name, backend_dead = "unavailable", True

        if forced == "keychain":
            logger.info(
                "Keychain service initialized",
                backend=backend_name,
                service_name=self.service_name,
            )
            return

        if backend_dead:
            try:
                from services.infrastructure.secure_credential_store import (
                    EncryptedDBCredentialStore,
                )

                self._db_store = EncryptedDBCredentialStore()
                logger.info(
                    "Keychain service initialized",
                    backend="EncryptedDBCredentialStore (#1382 hosted fallback)",
                    os_backend=backend_name,
                    service_name=self.service_name,
                )
                return
            except Exception as e:
                self._no_secure_store = (
                    "No OS keyring backend AND the encrypted-DB fallback is "
                    f"unavailable ({e}) — no secure credential store; refusing "
                    "the operation (#1382)."
                )
                logger.error(
                    "keychain_no_secure_store",
                    os_backend=backend_name,
                    fallback_error=str(e),
                    effect="credential writes will raise; reads return None",
                )
                return

        logger.info(
            "Keychain service initialized",
            backend=backend_name,
            service_name=self.service_name,
        )

    def store_api_key(self, provider: str, api_key: str, username: Optional[str] = None) -> None:
        """
        Store API key securely in keychain

        Args:
            provider: Provider name (e.g., "openai", "anthropic")
            api_key: API key to store
            username: Optional username for multi-user support (uses provider as default)

        Raises:
            ValueError: If provider or api_key is empty
            RuntimeError: If storage fails
        """
        if not provider:
            raise ValueError("Provider name cannot be empty")
        if not api_key:
            raise ValueError("API key cannot be empty")
        if self._no_secure_store:
            raise RuntimeError(self._no_secure_store)

        try:
            if self._db_store is not None:
                self._db_store.store(self._get_key_name(provider, username), api_key)
            else:
                keyring.set_password(
                    self.service_name, self._get_key_name(provider, username), api_key
                )
            log_identifier = f"{username}/{provider}" if username else provider
            logger.info(f"Stored API key for {log_identifier} in keychain")
        except Exception as e:
            log_identifier = f"{username}/{provider}" if username else provider
            logger.error(f"Failed to store API key for {log_identifier}: {e}")
            raise RuntimeError(f"Failed to store API key: {e}")

    def get_api_key(self, provider: str, username: Optional[str] = None) -> Optional[str]:
        """
        Retrieve API key from keychain

        Args:
            provider: Provider name (e.g., "openai", "anthropic")
            username: Optional username for multi-user support (uses provider as default)

        Returns:
            API key if found, None otherwise (including when no secure store
            exists — the degraded state is error-logged once at construction)
        """
        if not provider:
            return None
        if self._no_secure_store:
            return None

        try:
            if self._db_store is not None:
                key = self._db_store.get(self._get_key_name(provider, username))
            else:
                key = keyring.get_password(
                    self.service_name, self._get_key_name(provider, username)
                )
            if key:
                log_identifier = f"{username}/{provider}" if username else provider
                logger.debug(f"Retrieved API key for {log_identifier} from keychain")
            return key
        except Exception as e:
            log_identifier = f"{username}/{provider}" if username else provider
            logger.error(f"Failed to retrieve API key for {log_identifier}: {e}")
            return None

    def delete_api_key(self, provider: str, username: Optional[str] = None) -> bool:
        """
        Delete API key from keychain

        Args:
            provider: Provider name
            username: Optional username for multi-user support (uses provider as default)

        Returns:
            True if deleted, False if not found or error
        """
        if not provider:
            return False
        if self._no_secure_store:
            return False

        try:
            if self._db_store is not None:
                found = self._db_store.delete(self._get_key_name(provider, username))
                if not found:
                    return False
            else:
                keyring.delete_password(
                    self.service_name, self._get_key_name(provider, username)
                )
            log_identifier = f"{username}/{provider}" if username else provider
            logger.info(f"Deleted API key for {log_identifier} from keychain")
            return True
        except keyring.errors.PasswordDeleteError:
            log_identifier = f"{username}/{provider}" if username else provider
            logger.debug(f"No API key found for {log_identifier} to delete")
            return False
        except Exception as e:
            log_identifier = f"{username}/{provider}" if username else provider
            logger.error(f"Failed to delete API key for {log_identifier}: {e}")
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
                exists_in_env=env_key is not None,
            )

        return status

    def _get_key_name(self, provider: str, username: Optional[str] = None) -> str:
        """
        Get keychain entry name for provider

        Args:
            provider: Provider name
            username: Optional username for multi-user support

        Returns:
            Keychain entry name (e.g., "openai_api_key" or "user123_openai_api_key")
        """
        if username:
            return f"{username}_{provider}_api_key"
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

    # CLI Session Token Methods (Issue #397)

    def store_cli_token(self, user_id: str, token: str) -> None:
        """
        Store CLI session token in keychain (Issue #397).

        Args:
            user_id: User identifier for scoping
            token: JWT session token for CLI authentication

        Raises:
            ValueError: If user_id or token is empty
            RuntimeError: If storage fails
        """
        if not user_id:
            raise ValueError("User ID cannot be empty")
        if not token:
            raise ValueError("Token cannot be empty")

        self.store_api_key(CLI_SESSION_PROVIDER, token, username=user_id)
        logger.info(f"Stored CLI session token for user {user_id}")

    def get_cli_token(self, user_id: str) -> Optional[str]:
        """
        Retrieve CLI session token from keychain (Issue #397).

        Args:
            user_id: User identifier for scoping

        Returns:
            Token string if found, None otherwise
        """
        if not user_id:
            return None
        return self.get_api_key(CLI_SESSION_PROVIDER, username=user_id)

    def delete_cli_token(self, user_id: str) -> bool:
        """
        Delete CLI session token from keychain (Issue #397).

        Args:
            user_id: User identifier for scoping

        Returns:
            True if deleted, False if not found
        """
        if not user_id:
            return False
        return self.delete_api_key(CLI_SESSION_PROVIDER, username=user_id)


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
