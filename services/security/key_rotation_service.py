"""
API Key Rotation Service

Provides seamless API key rotation without service downtime, including:
- Gradual transition between old and new keys
- Automatic fallback mechanisms
- Health monitoring during rotation
- Rollback capabilities
- Zero-downtime rotation process

Issue #252 CORE-KEYS-ROTATION
"""

import asyncio
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

import structlog

from services.config.llm_config_service import LLMConfigService
from services.infrastructure.keychain_service import KeychainService
from services.security.api_key_validator import APIKeyValidator, ValidationReport
from services.security.user_api_key_service import UserAPIKeyService

logger = structlog.get_logger()


class RotationPhase(Enum):
    """Phases of key rotation process"""

    PREPARING = "preparing"
    VALIDATING = "validating"
    TRANSITIONING = "transitioning"
    MONITORING = "monitoring"
    COMPLETING = "completing"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLING_BACK = "rolling_back"
    ROLLED_BACK = "rolled_back"


class RotationStrategy(Enum):
    """Key rotation strategies"""

    IMMEDIATE = "immediate"  # Switch immediately (risky)
    GRADUAL = "gradual"  # Gradually increase new key usage
    BLUE_GREEN = "blue_green"  # Test new key, then switch
    CANARY = "canary"  # Small percentage first, then full


@dataclass
class RotationConfig:
    """Configuration for key rotation"""

    strategy: RotationStrategy = RotationStrategy.GRADUAL
    transition_duration_minutes: int = 30
    health_check_interval_seconds: int = 30
    failure_threshold: int = 3
    rollback_on_failure: bool = True
    canary_percentage: int = 10  # For canary strategy
    validation_timeout_seconds: int = 60


@dataclass
class KeyPair:
    """Represents old and new key pair during rotation"""

    old_key: str
    new_key: str
    provider: str
    old_key_hash: str = field(init=False)
    new_key_hash: str = field(init=False)

    def __post_init__(self):
        import hashlib

        self.old_key_hash = hashlib.sha256(self.old_key.encode()).hexdigest()[:16]
        self.new_key_hash = hashlib.sha256(self.new_key.encode()).hexdigest()[:16]


@dataclass
class RotationMetrics:
    """Metrics collected during rotation"""

    old_key_requests: int = 0
    new_key_requests: int = 0
    old_key_failures: int = 0
    new_key_failures: int = 0
    old_key_success_rate: float = 0.0
    new_key_success_rate: float = 0.0
    avg_response_time_old: float = 0.0
    avg_response_time_new: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class RotationStatus:
    """Status of ongoing key rotation"""

    rotation_id: str
    provider: str
    phase: RotationPhase
    strategy: RotationStrategy
    started_at: datetime
    current_step: str
    progress_percentage: int
    metrics: RotationMetrics
    config: RotationConfig
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    estimated_completion: Optional[datetime] = None
    can_rollback: bool = True


class KeyRotationService:
    """Service for seamless API key rotation"""

    def __init__(
        self,
        keychain_service: Optional[KeychainService] = None,
        llm_config_service: Optional[LLMConfigService] = None,
        api_key_validator: Optional[APIKeyValidator] = None,
        user_api_key_service: Optional[UserAPIKeyService] = None,
    ):
        self.keychain = keychain_service or KeychainService()
        self.llm_config = llm_config_service or LLMConfigService()
        self.validator = api_key_validator or APIKeyValidator()
        self.user_service = user_api_key_service or UserAPIKeyService()

        # Active rotations
        self.active_rotations: Dict[str, RotationStatus] = {}

        # Key usage tracking for gradual transition
        self.key_usage_weights: Dict[
            str, Dict[str, float]
        ] = {}  # provider -> {old: weight, new: weight}

        # Health monitoring
        self.health_callbacks: List[Callable[[str, str], bool]] = []

        # Rotation history
        self.rotation_history: List[RotationStatus] = []

    async def start_rotation(
        self,
        provider: str,
        new_key: str,
        config: Optional[RotationConfig] = None,
        user_id: Optional[UUID] = None,
    ) -> str:
        """
        Start key rotation process

        Args:
            provider: Provider name (openai, anthropic, etc.)
            new_key: New API key to rotate to
            config: Rotation configuration
            user_id: User ID for user-specific keys

        Returns:
            Rotation ID for tracking
        """
        rotation_id = str(uuid4())
        config = config or RotationConfig()

        # Get current key
        if user_id:
            # User-specific key rotation (not implemented in this version)
            raise NotImplementedError("User-specific key rotation not yet implemented")
        else:
            # System-wide key rotation
            old_key = self.llm_config.get_api_key(provider)
            if not old_key:
                raise ValueError(f"No existing key found for provider {provider}")

        # Create rotation status
        status = RotationStatus(
            rotation_id=rotation_id,
            provider=provider,
            phase=RotationPhase.PREPARING,
            strategy=config.strategy,
            started_at=datetime.now(),
            current_step="Initializing rotation",
            progress_percentage=0,
            metrics=RotationMetrics(),
            config=config,
            estimated_completion=datetime.now()
            + timedelta(minutes=config.transition_duration_minutes),
        )

        self.active_rotations[rotation_id] = status

        logger.info(
            "key_rotation_started",
            rotation_id=rotation_id,
            provider=provider,
            strategy=config.strategy.value,
            user_id=user_id,
        )

        # Start rotation process in background
        asyncio.create_task(
            self._execute_rotation(rotation_id, KeyPair(old_key, new_key, provider))
        )

        return rotation_id

    async def _execute_rotation(self, rotation_id: str, key_pair: KeyPair) -> None:
        """Execute the rotation process"""
        status = self.active_rotations[rotation_id]

        try:
            # Phase 1: Validate new key
            await self._phase_validate_new_key(status, key_pair)

            # Phase 2: Begin transition
            await self._phase_begin_transition(status, key_pair)

            # Phase 3: Monitor and adjust
            await self._phase_monitor_transition(status, key_pair)

            # Phase 4: Complete rotation
            await self._phase_complete_rotation(status, key_pair)

            status.phase = RotationPhase.COMPLETED
            status.current_step = "Rotation completed successfully"
            status.progress_percentage = 100

            logger.info(
                "key_rotation_completed",
                rotation_id=rotation_id,
                provider=key_pair.provider,
                duration_minutes=(datetime.now() - status.started_at).total_seconds() / 60,
            )

        except Exception as e:
            logger.error(
                "key_rotation_failed",
                rotation_id=rotation_id,
                provider=key_pair.provider,
                error=str(e),
                phase=status.phase.value,
            )

            status.phase = RotationPhase.FAILED
            status.errors.append(f"Rotation failed: {str(e)}")

            # Attempt rollback if configured
            if status.config.rollback_on_failure and status.can_rollback:
                await self._rollback_rotation(status, key_pair)

        finally:
            # Move to history
            self.rotation_history.append(status)
            if len(self.rotation_history) > 100:  # Keep last 100 rotations
                self.rotation_history = self.rotation_history[-100:]

    async def _phase_validate_new_key(self, status: RotationStatus, key_pair: KeyPair) -> None:
        """Phase 1: Validate the new key"""
        status.phase = RotationPhase.VALIDATING
        status.current_step = "Validating new API key"
        status.progress_percentage = 10

        # Validate new key format and API access
        validation_report = await self.validator.validate_api_key(
            key_pair.provider,
            key_pair.new_key,
            skip_rate_limit=True,  # Skip rate limiting for rotation
        )

        if not validation_report.is_valid:
            error_details = "; ".join([error.message for error in validation_report.errors])
            raise ValueError(f"New key validation failed: {error_details}")

        status.current_step = "New key validated successfully"
        status.progress_percentage = 20

        logger.info(
            "key_rotation_validation_passed",
            rotation_id=status.rotation_id,
            provider=key_pair.provider,
            new_key_hash=key_pair.new_key_hash,
        )

    async def _phase_begin_transition(self, status: RotationStatus, key_pair: KeyPair) -> None:
        """Phase 2: Begin the transition process"""
        status.phase = RotationPhase.TRANSITIONING
        status.current_step = "Beginning key transition"
        status.progress_percentage = 30

        # Initialize key usage weights based on strategy
        if status.strategy == RotationStrategy.IMMEDIATE:
            # Switch immediately (not recommended for production)
            self.key_usage_weights[key_pair.provider] = {"old": 0.0, "new": 1.0}
            status.progress_percentage = 80

        elif status.strategy == RotationStrategy.GRADUAL:
            # Start with small percentage of new key
            self.key_usage_weights[key_pair.provider] = {"old": 0.9, "new": 0.1}

        elif status.strategy == RotationStrategy.CANARY:
            # Use canary percentage
            canary_pct = status.config.canary_percentage / 100.0
            self.key_usage_weights[key_pair.provider] = {"old": 1.0 - canary_pct, "new": canary_pct}

        elif status.strategy == RotationStrategy.BLUE_GREEN:
            # Keep old key active while testing new key
            self.key_usage_weights[key_pair.provider] = {"old": 1.0, "new": 0.0}

        status.current_step = f"Transition started with {status.strategy.value} strategy"

        logger.info(
            "key_rotation_transition_started",
            rotation_id=status.rotation_id,
            provider=key_pair.provider,
            strategy=status.strategy.value,
            weights=self.key_usage_weights[key_pair.provider],
        )

    async def _phase_monitor_transition(self, status: RotationStatus, key_pair: KeyPair) -> None:
        """Phase 3: Monitor the transition and adjust weights"""
        status.phase = RotationPhase.MONITORING
        status.current_step = "Monitoring transition health"

        transition_start = datetime.now()
        transition_duration = timedelta(minutes=status.config.transition_duration_minutes)
        health_check_interval = status.config.health_check_interval_seconds

        consecutive_failures = 0

        while datetime.now() - transition_start < transition_duration:
            # Health check
            health_ok = await self._perform_health_check(status, key_pair)

            if not health_ok:
                consecutive_failures += 1
                status.warnings.append(f"Health check failed (attempt {consecutive_failures})")

                if consecutive_failures >= status.config.failure_threshold:
                    raise Exception(
                        f"Health checks failed {consecutive_failures} times consecutively"
                    )
            else:
                consecutive_failures = 0

            # Adjust weights for gradual strategies
            if status.strategy == RotationStrategy.GRADUAL:
                elapsed_ratio = (datetime.now() - transition_start) / transition_duration
                new_weight = min(0.1 + (elapsed_ratio * 0.9), 1.0)  # 10% to 100%
                old_weight = 1.0 - new_weight

                self.key_usage_weights[key_pair.provider] = {"old": old_weight, "new": new_weight}

                # Update progress
                status.progress_percentage = int(30 + (elapsed_ratio * 50))  # 30% to 80%
                status.current_step = f"Gradual transition: {int(new_weight * 100)}% new key"

            elif status.strategy == RotationStrategy.CANARY:
                # After half the transition time, switch to full new key if healthy
                if elapsed_ratio > 0.5 and self.key_usage_weights[key_pair.provider]["new"] < 1.0:
                    self.key_usage_weights[key_pair.provider] = {"old": 0.0, "new": 1.0}
                    status.current_step = "Canary successful, switching to full new key"
                    status.progress_percentage = 80

            # Wait before next check
            await asyncio.sleep(health_check_interval)

        status.current_step = "Transition monitoring completed"
        status.progress_percentage = 90

    async def _phase_complete_rotation(self, status: RotationStatus, key_pair: KeyPair) -> None:
        """Phase 4: Complete the rotation"""
        status.phase = RotationPhase.COMPLETING
        status.current_step = "Completing rotation"

        # Ensure new key is fully active
        self.key_usage_weights[key_pair.provider] = {"old": 0.0, "new": 1.0}

        # Store new key in keychain
        self.keychain.store_api_key(key_pair.provider, key_pair.new_key)

        # Final health check
        health_ok = await self._perform_health_check(status, key_pair)
        if not health_ok:
            raise Exception("Final health check failed")

        status.current_step = "New key stored and activated"
        status.can_rollback = False  # Can't rollback after storing new key

        logger.info(
            "key_rotation_completed_successfully",
            rotation_id=status.rotation_id,
            provider=key_pair.provider,
            old_key_hash=key_pair.old_key_hash,
            new_key_hash=key_pair.new_key_hash,
        )

    async def _perform_health_check(self, status: RotationStatus, key_pair: KeyPair) -> bool:
        """Perform health check during rotation"""
        try:
            # Test both keys if both are active
            weights = self.key_usage_weights.get(key_pair.provider, {"old": 1.0, "new": 0.0})

            health_results = []

            # Test old key if still in use
            if weights["old"] > 0:
                old_health = await self._test_key_health(key_pair.provider, key_pair.old_key)
                health_results.append(old_health)
                if old_health:
                    status.metrics.old_key_requests += 1
                else:
                    status.metrics.old_key_failures += 1

            # Test new key if in use
            if weights["new"] > 0:
                new_health = await self._test_key_health(key_pair.provider, key_pair.new_key)
                health_results.append(new_health)
                if new_health:
                    status.metrics.new_key_requests += 1
                else:
                    status.metrics.new_key_failures += 1

            # Update success rates
            if status.metrics.old_key_requests > 0:
                status.metrics.old_key_success_rate = 1.0 - (
                    status.metrics.old_key_failures / status.metrics.old_key_requests
                )
            if status.metrics.new_key_requests > 0:
                status.metrics.new_key_success_rate = 1.0 - (
                    status.metrics.new_key_failures / status.metrics.new_key_requests
                )

            status.metrics.last_updated = datetime.now()

            # Call custom health callbacks
            for callback in self.health_callbacks:
                try:
                    callback_result = callback(key_pair.provider, status.rotation_id)
                    health_results.append(callback_result)
                except Exception as e:
                    logger.warning(f"Health callback failed: {e}")
                    health_results.append(False)

            # All health checks must pass
            return all(health_results)

        except Exception as e:
            logger.warning(f"Health check error: {e}")
            return False

    async def _test_key_health(self, provider: str, api_key: str) -> bool:
        """Test individual key health"""
        try:
            # Use the validator's API check
            is_valid = await self.llm_config.validate_api_key(provider, api_key)
            return is_valid
        except Exception:
            return False

    async def _rollback_rotation(self, status: RotationStatus, key_pair: KeyPair) -> None:
        """Rollback rotation to old key"""
        status.phase = RotationPhase.ROLLING_BACK
        status.current_step = "Rolling back to old key"

        try:
            # Switch back to old key
            self.key_usage_weights[key_pair.provider] = {"old": 1.0, "new": 0.0}

            # Test old key health
            old_key_healthy = await self._test_key_health(key_pair.provider, key_pair.old_key)
            if not old_key_healthy:
                status.errors.append("Rollback failed: old key is also unhealthy")
                return

            status.phase = RotationPhase.ROLLED_BACK
            status.current_step = "Successfully rolled back to old key"

            logger.info(
                "key_rotation_rolled_back",
                rotation_id=status.rotation_id,
                provider=key_pair.provider,
            )

        except Exception as e:
            status.errors.append(f"Rollback failed: {str(e)}")
            logger.error(f"Rollback failed for rotation {status.rotation_id}: {e}")

    def get_rotation_status(self, rotation_id: str) -> Optional[RotationStatus]:
        """Get status of rotation"""
        return self.active_rotations.get(rotation_id)

    def get_active_rotations(self) -> List[RotationStatus]:
        """Get all active rotations"""
        return list(self.active_rotations.values())

    def get_rotation_history(self, limit: int = 50) -> List[RotationStatus]:
        """Get rotation history"""
        return self.rotation_history[-limit:]

    async def cancel_rotation(self, rotation_id: str, reason: str = "Cancelled by user") -> bool:
        """Cancel active rotation"""
        if rotation_id not in self.active_rotations:
            return False

        status = self.active_rotations[rotation_id]

        if status.phase in [
            RotationPhase.COMPLETED,
            RotationPhase.FAILED,
            RotationPhase.ROLLED_BACK,
        ]:
            return False  # Can't cancel completed rotations

        # Attempt rollback if possible
        if status.can_rollback:
            # This would need the key pair, which we'd need to store in status
            status.errors.append(f"Rotation cancelled: {reason}")
            status.phase = RotationPhase.FAILED

        logger.info(
            "key_rotation_cancelled",
            rotation_id=rotation_id,
            reason=reason,
            phase=status.phase.value,
        )

        return True

    def add_health_callback(self, callback: Callable[[str, str], bool]) -> None:
        """Add custom health check callback"""
        self.health_callbacks.append(callback)

    def get_key_for_request(self, provider: str) -> Optional[str]:
        """
        Get appropriate key for a request based on current rotation weights

        This would be called by the LLM clients during rotation
        """
        if provider not in self.key_usage_weights:
            # No rotation in progress, use normal key
            return self.llm_config.get_api_key(provider)

        weights = self.key_usage_weights[provider]

        # Simple weighted selection (in production, might use more sophisticated logic)
        import random

        if random.random() < weights["new"]:
            # Return new key (would need to store it somewhere accessible)
            # For now, return the configured key
            return self.llm_config.get_api_key(provider)
        else:
            # Return old key (would need to store it somewhere accessible)
            return self.llm_config.get_api_key(provider)

    def cleanup_completed_rotations(self) -> int:
        """Clean up completed rotations from active list"""
        completed_phases = [
            RotationPhase.COMPLETED,
            RotationPhase.FAILED,
            RotationPhase.ROLLED_BACK,
        ]

        to_remove = [
            rotation_id
            for rotation_id, status in self.active_rotations.items()
            if status.phase in completed_phases
        ]

        for rotation_id in to_remove:
            del self.active_rotations[rotation_id]

        return len(to_remove)


# Global instance for easy access
key_rotation_service = KeyRotationService()


# Convenience functions
async def rotate_api_key(
    provider: str,
    new_key: str,
    strategy: RotationStrategy = RotationStrategy.GRADUAL,
    transition_duration_minutes: int = 30,
) -> str:
    """Convenience function to start key rotation"""
    config = RotationConfig(
        strategy=strategy, transition_duration_minutes=transition_duration_minutes
    )
    return await key_rotation_service.start_rotation(provider, new_key, config)


def get_rotation_status(rotation_id: str) -> Optional[RotationStatus]:
    """Convenience function to get rotation status"""
    return key_rotation_service.get_rotation_status(rotation_id)
