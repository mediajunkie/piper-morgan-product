"""
LLM Configuration Service - Secure key management and validation

Responsibilities:
- Load API keys from environment variables
- Validate keys with real API calls
- Provide clear error messages
- Provider selection and exclusion logic (Phase 2)

Architecture:
- Single source of truth for LLM configuration
- Environment variable storage (Phase 1)
- Intelligent provider selection with fallbacks (Phase 2)
- OS keychain support (Phase 3)
"""

import asyncio
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

import structlog

from services.infrastructure.keychain_service import KeychainService

try:
    import httpx
except ImportError:
    httpx = None
    # Will raise clear error if validation attempted

logger = structlog.get_logger()


@dataclass
class ValidationResult:
    """Result of provider key validation"""

    provider: str
    is_valid: bool
    error_message: Optional[str] = None
    error_code: Optional[str] = None


@dataclass
class ProviderConfig:
    """Configuration for a single LLM provider"""

    name: str
    env_var: str
    api_key: Optional[str]
    validation_endpoint: str
    required: bool = False


class LLMProvider(Enum):
    """Supported LLM providers"""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    PERPLEXITY = "perplexity"


class Environment(Enum):
    """Deployment environment"""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LLMConfigService:
    """
    Central service for LLM configuration management

    Usage:
        service = LLMConfigService()
        await service.validate_all_providers()

        # Get provider API key
        openai_key = service.get_api_key("openai")
    """

    def __init__(self, keychain_service: Optional[KeychainService] = None):
        """
        Initialize service and load configuration from environment

        Args:
            keychain_service: Optional KeychainService for testing (uses default if None)
        """
        self._keychain_service = keychain_service or KeychainService()
        self._load_provider_configs()
        self._load_selection_config()

    def _load_provider_configs(self) -> None:
        """Load provider configurations from environment variables"""
        # Define provider configurations
        self._providers: Dict[str, ProviderConfig] = {
            "openai": ProviderConfig(
                name="openai",
                env_var="OPENAI_API_KEY",
                api_key=os.getenv("OPENAI_API_KEY"),
                validation_endpoint="https://api.openai.com/v1/models",
                required=False,  # #940: No single provider is required
            ),
            "anthropic": ProviderConfig(
                name="anthropic",
                env_var="ANTHROPIC_API_KEY",
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                validation_endpoint="https://api.anthropic.com/v1/messages",
                required=False,
            ),
            "gemini": ProviderConfig(
                name="gemini",
                env_var="GEMINI_API_KEY",
                api_key=os.getenv("GEMINI_API_KEY"),
                validation_endpoint="https://generativelanguage.googleapis.com/v1/models",
                required=False,
            ),
            "perplexity": ProviderConfig(
                name="perplexity",
                env_var="PERPLEXITY_API_KEY",
                api_key=os.getenv("PERPLEXITY_API_KEY"),
                validation_endpoint="https://api.perplexity.ai/chat/completions",
                required=False,
            ),
        }

    def _load_selection_config(self) -> None:
        """Load provider selection configuration from environment"""

        # Current environment
        env_value = os.getenv("PIPER_ENVIRONMENT", "development")
        try:
            self._environment = Environment(env_value)
        except ValueError:
            logger.warning(f"Invalid PIPER_ENVIRONMENT: {env_value}, defaulting to development")
            self._environment = Environment.DEVELOPMENT

        # Excluded providers (comma-separated list)
        excluded = os.getenv("PIPER_EXCLUDED_PROVIDERS", "")
        self._excluded_providers = [p.strip() for p in excluded.split(",") if p.strip()]

        # Default provider
        self._default_provider = os.getenv("PIPER_DEFAULT_PROVIDER", "openai")  # Safe default

        # Fallback chain (comma-separated, in priority order)
        fallback = os.getenv(
            "PIPER_FALLBACK_PROVIDERS",
            "openai,gemini,anthropic,perplexity",  # Default order
        )
        self._fallback_chain = [p.strip() for p in fallback.split(",") if p.strip()]

        logger.debug(
            f"Selection config loaded: env={self._environment.value}, "
            f"excluded={self._excluded_providers}, default={self._default_provider}"
        )

    def get_configured_providers(self, user_id: Optional[str] = None) -> List[str]:
        """Return providers with API keys configured AND authorized for the caller.

        #946: setup stores an 'authorized_llm_providers' consent list. Only
        providers on that list are returned — stale keys from previous installs
        are filtered out.

        #1415: the consent list resolves PER USER (the acting principal's list
        first, then the server/global list, else legacy all-configured), and a
        consent-read failure now FAILS CLOSED to the server-default provider
        only — the old behavior failed OPEN to everything configured, silently
        disabling the consent boundary (census F1).
        """
        from services.llm.provider_selection import resolve_authorized_providers

        # Check which providers have keys available
        all_configured = [
            name for name in self._providers.keys() if self.get_api_key(name) is not None
        ]

        filtered = resolve_authorized_providers(
            user_id,
            all_configured,
            server_default=self._default_provider,
            keychain=self._keychain_service,
        )
        if filtered != all_configured:
            logger.debug(
                "provider_consent_filter",
                all_configured=all_configured,
                filtered=filtered,
                user_scoped=bool(user_id),
            )
        return filtered

    def get_available_providers(self, user_id: Optional[str] = None) -> List[str]:
        """
        Return list of providers that are:
        1. Configured (have valid API keys)
        2. Authorized for the acting principal (#946/#1415 consent filter)
        3. Not excluded
        4. Available in current environment
        """
        configured = self.get_configured_providers(user_id)

        # Filter out excluded providers
        available = [
            provider for provider in configured if provider not in self._excluded_providers
        ]

        return available

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
        if provider not in self._providers:
            logger.debug(f"Unknown provider: {provider}")
            return None

        # Priority 1: Try keychain (secure storage)
        key = self._keychain_service.get_api_key(provider)
        if key:
            # Note: keychain_service already logs the retrieval
            return key

        # Priority 2: Try environment (migration fallback)
        env_var = f"{provider.upper()}_API_KEY"
        key = os.getenv(env_var)
        if key:
            logger.warning(
                f"{provider} key retrieved from environment variable",
                env_var=env_var,
                recommendation="Migrate to keychain for security",
            )
            return key

        # Not found in either location
        logger.debug(f"No API key found for {provider}")
        return None

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
            "missing": sum(
                1 for s in status.values() if not s.exists_in_keychain and not s.exists_in_env
            ),
            "needs_migration": sum(
                1 for s in status.values() if s.exists_in_env and not s.exists_in_keychain
            ),
            "providers": status,
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
                recommendation=f"Remove {env_var} from .env file",
            )
            return True
        except Exception as e:
            logger.error(f"Failed to migrate {provider} key: {e}")
            return False

    def get_default_provider(self, user_id: Optional[str] = None) -> str:
        """
        Get the default provider to use for the acting principal.

        Priority (#1415 — resolved statelessly per call, never cached):
        1. The ACTING USER's setup choice (username-scoped keychain slot)
        2. The server/global setup choice (legacy single-user slot)
        3. PIPER_DEFAULT_PROVIDER env var
        4. First available provider

        Every step is validated against the caller's consent-filtered available
        set, so one user's choice can never pin another user's provider, and a
        stored choice pointing at an unavailable provider falls through instead
        of locking the user out.

        Raises:
            ValueError: If no providers available
        """
        from services.llm.provider_selection import resolve_default_provider

        available = self.get_available_providers(user_id)

        choice = resolve_default_provider(
            user_id,
            available,
            env_default=self._default_provider,
            keychain=self._keychain_service,
        )
        if choice is None:
            raise ValueError("No LLM providers available. Check configuration.")
        if choice != self._default_provider and self._default_provider not in available:
            logger.warning(
                f"Default provider {self._default_provider} not available, using {choice}"
            )
        return choice

    def get_provider_with_fallback(self, preferred: Optional[str] = None) -> str:
        """
        Get provider with fallback logic

        Args:
            preferred: Preferred provider (optional)

        Returns:
            Provider name to use

        Logic:
        1. If preferred specified and available, use it
        2. Otherwise use default provider
        3. If default not available, use first in fallback chain
        """
        available = self.get_available_providers()

        if not available:
            raise ValueError("No LLM providers available")

        # Try preferred provider first
        if preferred and preferred in available:
            return preferred

        # Try default provider
        if self._default_provider in available:
            return self._default_provider

        # Try fallback chain in order
        for provider in self._fallback_chain:
            if provider in available:
                logger.info(f"Using fallback provider: {provider}")
                return provider

        # Last resort: first available
        logger.warning(f"All fallbacks exhausted, using {available[0]}")
        return available[0]

    def is_provider_excluded(self, provider: str) -> bool:
        """Check if provider is excluded"""
        return provider in self._excluded_providers

    def get_environment(self) -> Environment:
        """Get current environment"""
        return self._environment

    async def validate_provider(self, provider: str) -> ValidationResult:
        """
        Validate provider API key with real API call

        Makes lightweight API call to verify key works.
        """
        if provider not in self._providers:
            return ValidationResult(
                provider=provider,
                is_valid=False,
                error_message=f"Unknown provider: {provider}",
            )

        config = self._providers[provider]

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

        # Validate with provider-specific logic
        if provider == "openai":
            return await self._validate_openai(config)
        elif provider == "anthropic":
            return await self._validate_anthropic(config)
        elif provider == "gemini":
            return await self._validate_gemini(config)
        elif provider == "perplexity":
            return await self._validate_perplexity(config)

        return ValidationResult(
            provider=provider,
            is_valid=False,
            error_message=f"No validation implemented for {provider}",
        )

    async def validate_api_key(self, provider: str, api_key: str) -> bool:
        """
        Validate a specific API key for a provider.

        This method validates any given API key, not just the configured one.
        Used for user-provided API key validation in multi-user scenarios.

        Args:
            provider: Provider name (openai, anthropic, gemini, perplexity)
            api_key: API key to validate

        Returns:
            True if valid, False otherwise

        Issue #228 CORE-USERS-API - User key validation
        """
        if provider not in self._providers:
            return False

        # Create temporary config with the provided key
        config = self._providers[provider]
        temp_config = ProviderConfig(
            name=config.name,
            env_var=config.env_var,
            api_key=api_key,  # Use provided key
            validation_endpoint=config.validation_endpoint,
            required=False,
        )

        # Validate with provider-specific logic
        try:
            if provider == "openai":
                result = await self._validate_openai(temp_config)
            elif provider == "anthropic":
                result = await self._validate_anthropic(temp_config)
            elif provider == "gemini":
                result = await self._validate_gemini(temp_config)
            elif provider == "perplexity":
                result = await self._validate_perplexity(temp_config)
            else:
                return False

            return result.is_valid
        except Exception:
            return False

    async def _validate_openai(self, config: ProviderConfig) -> ValidationResult:
        """Validate OpenAI API key"""
        if httpx is None:
            return ValidationResult(
                provider=config.name,
                is_valid=False,
                error_message="httpx library not installed",
                error_code="MISSING_DEPENDENCY",
            )

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    config.validation_endpoint,
                    headers={"Authorization": f"Bearer {config.api_key}"},
                )

                if response.status_code == 200:
                    return ValidationResult(provider=config.name, is_valid=True)
                else:
                    return ValidationResult(
                        provider=config.name,
                        is_valid=False,
                        error_message=f"Invalid API key: {response.status_code} {response.reason_phrase}",
                        error_code="AUTH_ERROR",
                    )

        except httpx.TimeoutException:
            return ValidationResult(
                provider=config.name,
                is_valid=False,
                error_message="Network error: Connection timeout",
                error_code="NETWORK_ERROR",
            )
        except Exception as e:
            return ValidationResult(
                provider=config.name,
                is_valid=False,
                error_message=f"Validation error: {str(e)}",
                error_code="VALIDATION_ERROR",
            )

    async def _validate_anthropic(self, config: ProviderConfig) -> ValidationResult:
        """Validate Anthropic API key"""
        if httpx is None:
            return ValidationResult(
                provider=config.name,
                is_valid=False,
                error_message="httpx library not installed",
                error_code="MISSING_DEPENDENCY",
            )

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Minimal request to check auth
                response = await client.post(
                    config.validation_endpoint,
                    headers={
                        "x-api-key": config.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": "claude-haiku-4-5-20251001",
                        "max_tokens": 1,
                        "messages": [{"role": "user", "content": "Hi"}],
                    },
                )

                if response.status_code in [200, 201]:
                    return ValidationResult(provider=config.name, is_valid=True)
                elif response.status_code in [401, 403]:
                    return ValidationResult(
                        provider=config.name,
                        is_valid=False,
                        error_message=f"Invalid API key: {response.status_code} Unauthorized",
                        error_code="AUTH_ERROR",
                    )
                else:
                    return ValidationResult(
                        provider=config.name,
                        is_valid=False,
                        error_message=f"Validation failed: {response.status_code} {response.reason_phrase}",
                        error_code="VALIDATION_ERROR",
                    )

        except httpx.TimeoutException:
            return ValidationResult(
                provider=config.name,
                is_valid=False,
                error_message="Network error: Connection timeout",
                error_code="NETWORK_ERROR",
            )
        except Exception as e:
            return ValidationResult(
                provider=config.name,
                is_valid=False,
                error_message=f"Validation error: {str(e)}",
                error_code="VALIDATION_ERROR",
            )

    async def _validate_gemini(self, config: ProviderConfig) -> ValidationResult:
        """Validate Gemini API key"""
        if httpx is None:
            return ValidationResult(
                provider=config.name,
                is_valid=False,
                error_message="httpx library not installed",
                error_code="MISSING_DEPENDENCY",
            )

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{config.validation_endpoint}?key={config.api_key}",
                )

                if response.status_code == 200:
                    return ValidationResult(provider=config.name, is_valid=True)
                elif response.status_code in [400, 401, 403]:
                    return ValidationResult(
                        provider=config.name,
                        is_valid=False,
                        error_message=f"Invalid API key: {response.status_code}",
                        error_code="AUTH_ERROR",
                    )
                else:
                    return ValidationResult(
                        provider=config.name,
                        is_valid=False,
                        error_message=f"Validation failed: {response.status_code}",
                        error_code="VALIDATION_ERROR",
                    )

        except httpx.TimeoutException:
            return ValidationResult(
                provider=config.name,
                is_valid=False,
                error_message="Network error: Connection timeout",
                error_code="NETWORK_ERROR",
            )
        except Exception as e:
            return ValidationResult(
                provider=config.name,
                is_valid=False,
                error_message=f"Validation error: {str(e)}",
                error_code="VALIDATION_ERROR",
            )

    async def _validate_perplexity(self, config: ProviderConfig) -> ValidationResult:
        """Validate Perplexity API key"""
        if httpx is None:
            return ValidationResult(
                provider=config.name,
                is_valid=False,
                error_message="httpx library not installed",
                error_code="MISSING_DEPENDENCY",
            )

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Minimal request to check auth
                # Note: Correct model name is just "sonar" (not llama-3.1-sonar-small-128k-online)
                response = await client.post(
                    config.validation_endpoint,
                    headers={
                        "Authorization": f"Bearer {config.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "sonar",  # Fixed: Use correct Perplexity model name
                        "messages": [{"role": "user", "content": "test"}],
                        "max_tokens": 1,
                    },
                )

                if response.status_code in [200, 201]:
                    return ValidationResult(provider=config.name, is_valid=True)
                elif response.status_code in [401, 403]:
                    return ValidationResult(
                        provider=config.name,
                        is_valid=False,
                        error_message=f"Invalid API key: {response.status_code} Unauthorized",
                        error_code="AUTH_ERROR",
                    )
                else:
                    return ValidationResult(
                        provider=config.name,
                        is_valid=False,
                        error_message=f"Validation failed: {response.status_code}",
                        error_code="VALIDATION_ERROR",
                    )

        except httpx.TimeoutException:
            return ValidationResult(
                provider=config.name,
                is_valid=False,
                error_message="Network error: Connection timeout",
                error_code="NETWORK_ERROR",
            )
        except Exception as e:
            return ValidationResult(
                provider=config.name,
                is_valid=False,
                error_message=f"Validation error: {str(e)}",
                error_code="VALIDATION_ERROR",
            )

    async def validate_all_providers(self) -> Dict[str, ValidationResult]:
        """
        Validate all configured providers

        Returns dict of provider -> ValidationResult
        Logs results and raises if required provider fails
        """
        configured = self.get_configured_providers()

        if not configured:
            logger.warning("No LLM providers configured")
            return {}

        # Validate all providers concurrently
        tasks = [self.validate_provider(provider) for provider in configured]
        results = await asyncio.gather(*tasks)

        # Create results dict
        validation_results = {result.provider: result for result in results}

        # Log results
        for provider, result in validation_results.items():
            if result.is_valid:
                logger.info(f"✅ {provider}: Valid")
            else:
                logger.warning(f"❌ {provider}: {result.error_message}")

        # Check required providers
        for provider, config in self._providers.items():
            if config.required and provider in validation_results:
                result = validation_results[provider]
                if not result.is_valid:
                    raise ValueError(
                        f"Required provider {provider} validation failed: "
                        f"{result.error_message}"
                    )

        return validation_results
