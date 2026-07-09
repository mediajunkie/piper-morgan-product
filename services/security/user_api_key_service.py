"""
User API Key Management Service

Handles per-user API keys with OS keychain storage.
Stores metadata in database, actual keys in OS keychain.

Issue #228 CORE-USERS-API Phase 1C
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.config.llm_config_service import LLMConfigService
from services.database.models import UserAPIKey
from services.infrastructure.keychain_service import KeychainService
from services.security.api_key_validator import APIKeyValidator
from services.security.audit_logger import Action, audit_logger
from services.security.field_encryption import DecryptionError, FieldEncryptionService

logger = logging.getLogger(__name__)


class UserAPIKeyService:
    """Service for managing user-specific API keys with keychain storage"""

    def __init__(
        self,
        keychain_service: Optional[KeychainService] = None,
        field_encryption_service: Optional[FieldEncryptionService] = None,
    ):
        """
        Initialize user API key service.

        Args:
            keychain_service: Optional keychain service for testing
            field_encryption_service: Optional encryptor for at-rest DB storage (#358).
                None (no ENCRYPTION_MASTER_KEY) → keychain-only (today's local-dev path).
        """
        self._keychain = keychain_service or KeychainService()
        self._llm_config = LLMConfigService()
        self._validator = APIKeyValidator()
        # #358: encrypt-at-rest store, portable off the OS keychain to the hosted DB.
        self._encryptor = field_encryption_service or FieldEncryptionService.from_env()

    async def store_user_key(
        self,
        session: AsyncSession,
        user_id: str,
        provider: str,
        api_key: str,
        validate: bool = True,
        store: bool = True,
        audit_context: Optional[Dict[str, Any]] = None,
    ) -> Optional[UserAPIKey]:
        """
        Store API key for user in keychain with database metadata.

        Args:
            session: Database session
            user_id: User identifier
            provider: Service provider (openai, anthropic, github, etc)
            api_key: API key to store
            validate: Whether to validate key with provider API
            store: Whether to actually store the key (False for validation-only)
            audit_context: Optional request context for audit logging

        Returns:
            UserAPIKey database record, or None if store=False

        Raises:
            ValueError: If validation fails or key invalid

        Issue #249: Added audit logging
        Issue #485: Added store parameter for validation-only mode
        """
        logger.info(f"Storing API key for user {user_id}, provider {provider}")

        # Validate key security before storage (Issue #268).
        # #933 (May 9 2026): re-enabled. The original bypass was added for
        # "format validator issues" — those were fixed Oct 30 2025 in commit
        # 214f4afe (OpenAI sk-proj-* / service-account key support). The
        # bypass remained in place but the cause was gone. #932 made
        # leak_safe informational (confidence=0.0 doesn't gate overall_valid),
        # so the validator no longer falsely-blocks on a leak check we
        # didn't actually perform. Format + strength still gate; the leak
        # quick-checks (known test keys, weak patterns, obvious fakes)
        # also gate when they fire with high confidence.
        try:
            validation_report = await self._validator.validate_api_key(provider, api_key)
            if not validation_report.overall_valid:
                # Build detailed error message from validation report
                error_messages = []

                if not validation_report.format_valid:
                    error_messages.append(
                        f"Key format invalid for {provider}: {validation_report.format_result.message}"
                    )
                if not validation_report.strength_acceptable:
                    entropy_score = validation_report.strength_result.entropy_score
                    entropy_pct = int(entropy_score * 100)
                    error_messages.append(f"Key too weak: entropy {entropy_pct}% (required: 70%)")
                if not validation_report.leak_safe:
                    source = validation_report.leak_result.source or "known_leak_database"
                    error_messages.append(f"Key found in breach database: {source}")

                error_detail = (
                    " | ".join(error_messages) if error_messages else "Security validation failed"
                )
                logger.warning(f"API key validation failed for {provider}: {error_detail}")

                # #1071: Audit-log validation failures. Security-relevant event
                # (someone attempted to store a key that failed format/strength/leak
                # checks). Captures provider, key_preview (first 8 chars), failure
                # reason, and the failed check categories. NEVER logs the full key.
                # Non-blocking: any error here should not prevent the ValueError.
                try:
                    key_preview = f"{api_key[:8]}..." if len(api_key) > 8 else "<too_short>"
                    failed_checks = []
                    if not validation_report.format_valid:
                        failed_checks.append("format")
                    if not validation_report.strength_acceptable:
                        failed_checks.append("strength")
                    if not validation_report.leak_safe:
                        failed_checks.append("leak")

                    await audit_logger.log_api_key_event(
                        action=Action.KEY_VALIDATION_FAILED,
                        provider=provider,
                        status="failed",
                        message=f"API key validation rejected for {provider}",
                        session=session,
                        user_id=user_id,
                        details={
                            "key_preview": key_preview,
                            "failure_reason": error_detail,
                            "failed_checks": failed_checks,
                        },
                        audit_context=audit_context,
                    )
                except Exception as audit_err:
                    # Non-blocking — don't let audit-log failure prevent the
                    # primary ValueError signal to the caller.
                    logger.error(f"Failed to write validation-failure audit log: {audit_err}")

                raise ValueError(f"API key validation failed: {error_detail}")

            logger.info(
                f"API key security validation passed for {provider} (security level: {validation_report.security_level})"
            )
        except ValueError:
            # Re-raise validation errors as-is
            raise
        except Exception as e:
            logger.error(f"Unexpected error during key validation: {e}")
            raise ValueError(f"Failed to validate API key: {e}")

        # Validate key with provider API if requested (existing validation)
        is_valid = False
        if validate:
            try:
                is_valid = await self._llm_config.validate_api_key(provider, api_key)
                if not is_valid:
                    logger.warning(f"Provider API validation failed for {provider}")
                    # Issue #485: For validation-only mode, raise error on invalid key
                    if not store:
                        raise ValueError(f"API key validation failed for {provider}")
                logger.info(f"Provider API validation result for {provider}: {is_valid}")
            except ValueError:
                # Re-raise validation errors
                raise
            except Exception as e:
                logger.warning(f"Provider API validation error for {provider}: {e}")
                # Issue #485: For validation-only mode, raise error on validation failure
                if not store:
                    raise ValueError(f"API key validation error for {provider}: {e}")

        # Issue #485: If store=False, return early after validation (no DB writes)
        if not store:
            logger.info(f"Validation-only mode: key validated for {provider}, not storing")
            return None

        # Generate keychain reference
        key_reference = self._generate_key_reference(user_id, provider)

        # Store in keychain — best-effort WHEN the encrypted-DB store is available (#1382).
        # On hosted Linux the container has no keyring backend, so this write always
        # fails there; raising here meant the #358 encrypted_secret write below never
        # ran and every tester's wizard key save died (found live on alpha 2026-07-08).
        # With an encryptor, encrypted_secret is the durable store and the read path
        # already prefers it; without one (local keychain-only mode), keychain failure
        # is still fatal — nothing else would hold the key.
        try:
            self._keychain.store_api_key(provider, api_key, username=user_id)
            logger.info(f"Stored key in keychain: {key_reference}")
        except Exception as e:
            if self._encryptor is None:
                logger.error(f"Failed to store key in keychain: {e}")
                raise ValueError(f"Keychain storage failed: {e}")
            logger.warning(
                f"Keychain unavailable ({e}); relying on encrypted-at-rest DB store (#1382)"
            )

        # #358: also encrypt-at-rest in the DB (portable to the hosted box, which has no
        # OS keychain). None encryptor (no master key) → skip; the keychain remains the store.
        encrypted_secret = (
            self._encryptor.encrypt(api_key, "user_api_keys.secret") if self._encryptor else None
        )

        # Check if key record exists
        result = await session.execute(
            select(UserAPIKey).where(
                and_(UserAPIKey.user_id == user_id, UserAPIKey.provider == provider)
            )
        )
        existing_key = result.scalar_one_or_none()

        if existing_key:
            # Update existing record
            existing_key.key_reference = key_reference
            existing_key.is_active = True
            existing_key.is_validated = is_valid
            existing_key.last_validated_at = datetime.now(timezone.utc) if is_valid else None
            existing_key.updated_at = datetime.now(timezone.utc)
            existing_key.encrypted_secret = encrypted_secret  # #358

            # Audit log (Issue #249)
            await audit_logger.log_api_key_event(
                action=Action.KEY_STORED,
                provider=provider,
                status="success",
                message=f"API key updated for {provider}",
                session=session,
                user_id=user_id,
                details={
                    "keychain_ref": key_reference,
                    "validated": is_valid,
                    "operation": "update",
                },
                audit_context=audit_context,
            )

            await session.commit()
            logger.info(f"Updated existing key record for {user_id}/{provider}")
            return existing_key
        else:
            # Create new record
            user_key = UserAPIKey(
                user_id=user_id,
                provider=provider,
                key_reference=key_reference,
                is_active=True,
                is_validated=is_valid,
                last_validated_at=datetime.now(timezone.utc) if is_valid else None,
                created_by=str(user_id),
                encrypted_secret=encrypted_secret,  # #358
            )
            session.add(user_key)

            # Audit log (Issue #249)
            await audit_logger.log_api_key_event(
                action=Action.KEY_STORED,
                provider=provider,
                status="success",
                message=f"API key stored for {provider}",
                session=session,
                user_id=user_id,
                details={
                    "keychain_ref": key_reference,
                    "validated": is_valid,
                    "operation": "create",
                },
                audit_context=audit_context,
            )

            await session.commit()
            logger.info(f"Created new key record for {user_id}/{provider}")
            return user_key

    async def retrieve_user_key(
        self, session: AsyncSession, user_id: str, provider: str
    ) -> Optional[str]:
        """
        Retrieve API key for user from keychain.

        Args:
            session: Database session
            user_id: User identifier
            provider: Service provider

        Returns:
            API key if found, None otherwise
        """
        # Check database for key metadata
        result = await session.execute(
            select(UserAPIKey).where(
                and_(
                    UserAPIKey.user_id == user_id,
                    UserAPIKey.provider == provider,
                    UserAPIKey.is_active == True,
                )
            )
        )
        user_key = result.scalar_one_or_none()

        if not user_key:
            logger.debug(f"No key record found for {user_id}/{provider}")
            return None

        # #358: prefer the encrypted-at-rest secret (works on the hosted box, which has no
        # OS keychain). Fall back to the keychain for legacy / pre-migration / local rows.
        if user_key.encrypted_secret and self._encryptor:
            try:
                return self._encryptor.decrypt(user_key.encrypted_secret, "user_api_keys.secret")
            except DecryptionError:
                logger.error(
                    f"Failed to decrypt stored secret for {user_id}/{provider}; "
                    "falling back to keychain"
                )

        # Retrieve from keychain
        try:
            api_key = self._keychain.get_api_key(provider, username=user_id)
            if api_key:
                logger.debug(f"Retrieved key from keychain for {user_id}/{provider}")
                return api_key
            else:
                logger.warning(
                    f"Key reference exists but keychain returned None: {user_id}/{provider}"
                )
                return None
        except Exception as e:
            logger.error(f"Failed to retrieve key from keychain: {e}")
            return None

    async def delete_user_key(
        self,
        session: AsyncSession,
        user_id: str,
        provider: str,
        audit_context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Delete API key for user from keychain and database.

        Args:
            session: Database session
            user_id: User identifier
            provider: Service provider
            audit_context: Optional request context for audit logging

        Returns:
            True if deleted, False if not found

        Issue #249: Added audit logging
        """
        logger.info(f"Deleting API key for {user_id}/{provider}")

        # Get database record
        result = await session.execute(
            select(UserAPIKey).where(
                and_(UserAPIKey.user_id == user_id, UserAPIKey.provider == provider)
            )
        )
        user_key = result.scalar_one_or_none()

        if not user_key:
            logger.debug(f"No key record to delete for {user_id}/{provider}")
            return False

        # Store old value for audit
        old_value = {
            "keychain_ref": user_key.key_reference,
            "created_at": user_key.created_at.isoformat() if user_key.created_at else None,
            "last_validated_at": (
                user_key.last_validated_at.isoformat() if user_key.last_validated_at else None
            ),
        }

        # Delete from keychain
        try:
            self._keychain.delete_api_key(provider, username=user_id)
            logger.info(f"Deleted key from keychain: {user_id}/{provider}")
        except Exception as e:
            logger.warning(f"Failed to delete from keychain (continuing): {e}")

        # Delete database record
        await session.delete(user_key)

        # Audit log (Issue #249)
        await audit_logger.log_api_key_event(
            action=Action.KEY_DELETED,
            provider=provider,
            status="success",
            message=f"API key deleted for {provider}",
            session=session,
            user_id=user_id,
            old_value=old_value,
            audit_context=audit_context,
        )

        await session.commit()
        logger.info(f"Deleted key database record for {user_id}/{provider}")

        return True

    async def list_user_keys(
        self, session: AsyncSession, user_id: str, active_only: bool = True
    ) -> List[Dict[str, Any]]:
        """
        List all API keys for user.

        Args:
            session: Database session
            user_id: User identifier
            active_only: Only return active keys

        Returns:
            List of key metadata (no actual keys)
        """
        query = select(UserAPIKey).where(UserAPIKey.user_id == user_id)

        if active_only:
            query = query.where(UserAPIKey.is_active == True)

        result = await session.execute(query)
        user_keys = result.scalars().all()

        return [
            {
                "id": key.id,
                "provider": key.provider,
                "is_active": key.is_active,
                "is_validated": key.is_validated,
                "last_validated_at": (
                    key.last_validated_at.isoformat() if key.last_validated_at else None
                ),
                "created_at": key.created_at.isoformat(),
                "rotated_at": key.rotated_at.isoformat() if key.rotated_at else None,
            }
            for key in user_keys
        ]

    async def validate_user_key(self, session: AsyncSession, user_id: str, provider: str) -> bool:
        """
        Validate user's API key by testing with provider API.

        Args:
            session: Database session
            user_id: User identifier
            provider: Service provider

        Returns:
            True if valid, False otherwise
        """
        # Retrieve key
        api_key = await self.retrieve_user_key(session, user_id, provider)
        if not api_key:
            logger.warning(f"No key found to validate for {user_id}/{provider}")
            return False

        # Validate with provider
        try:
            is_valid = await self._llm_config.validate_api_key(provider, api_key)

            # Update validation status in database
            result = await session.execute(
                select(UserAPIKey).where(
                    and_(UserAPIKey.user_id == user_id, UserAPIKey.provider == provider)
                )
            )
            user_key = result.scalar_one_or_none()

            if user_key:
                user_key.is_validated = is_valid
                user_key.last_validated_at = datetime.now(timezone.utc)
                await session.commit()

            return is_valid

        except Exception as e:
            logger.error(f"Validation failed for {user_id}/{provider}: {e}")
            return False

    async def rotate_user_key(
        self,
        session: AsyncSession,
        user_id: str,
        provider: str,
        new_api_key: str,
        validate: bool = True,
        audit_context: Optional[Dict[str, Any]] = None,
    ) -> UserAPIKey:
        """
        Rotate API key for user with zero-downtime strategy.

        Process:
        1. Validate new key
        2. Store old key reference
        3. Store new key in keychain
        4. Update database with rotation info
        5. Delete old key from keychain

        Args:
            session: Database session
            user_id: User identifier
            provider: Service provider
            new_api_key: New API key to rotate to
            validate: Whether to validate new key before rotation
            audit_context: Optional request context for audit logging

        Returns:
            Updated UserAPIKey database record

        Raises:
            ValueError: If no existing key found or validation fails

        Issue #228 CORE-USERS-API Phase 2A - Key rotation
        Issue #249: Added audit logging
        """
        logger.info(f"Rotating API key for {user_id}/{provider}")

        # Get existing key record
        result = await session.execute(
            select(UserAPIKey).where(
                and_(
                    UserAPIKey.user_id == user_id,
                    UserAPIKey.provider == provider,
                    UserAPIKey.is_active == True,
                )
            )
        )
        existing_key = result.scalar_one_or_none()

        if not existing_key:
            raise ValueError(f"No existing key found for {user_id}/{provider}")

        # Store old key reference for rollback capability
        old_key_reference = existing_key.key_reference

        # Validate new key if requested
        if validate:
            try:
                is_valid = await self._llm_config.validate_api_key(provider, new_api_key)
                if not is_valid:
                    raise ValueError(f"New API key validation failed for {provider}")
                logger.info(f"New API key validated successfully for {provider}")
            except Exception as e:
                logger.error(f"New API key validation error: {e}")
                raise ValueError(f"Failed to validate new API key: {e}")

        # Generate new key reference (same format, but represents the new key)
        new_key_reference = self._generate_key_reference(user_id, provider)

        # Store new key in keychain (overwrites old key) — best-effort when the
        # encrypted-DB store is available; same #1382 hosted-Linux reasoning as store.
        try:
            self._keychain.store_api_key(provider, new_api_key, username=user_id)
            logger.info(f"Stored new key in keychain: {new_key_reference}")
        except Exception as e:
            if self._encryptor is None:
                logger.error(f"Failed to store new key in keychain: {e}")
                raise ValueError(f"Keychain storage failed: {e}")
            logger.warning(
                f"Keychain unavailable ({e}); relying on encrypted-at-rest DB store (#1382)"
            )

        # #1382 (found during the same trace): rotation previously never refreshed
        # encrypted_secret, so the read path — which PREFERS the encrypted column —
        # would keep serving the OLD key after every rotation. Refresh it with the
        # new key (or clear it if no encryptor, keeping column and keychain in step).
        existing_key.encrypted_secret = (
            self._encryptor.encrypt(new_api_key, "user_api_keys.secret")
            if self._encryptor
            else None
        )

        # Update database record with rotation info
        existing_key.key_reference = new_key_reference
        existing_key.previous_key_reference = old_key_reference
        existing_key.rotated_at = datetime.now(timezone.utc)
        existing_key.is_validated = validate
        existing_key.last_validated_at = datetime.now(timezone.utc) if validate else None
        existing_key.updated_at = datetime.now(timezone.utc)

        # Audit log (Issue #249)
        await audit_logger.log_api_key_event(
            action=Action.KEY_ROTATED,
            provider=provider,
            status="success",
            message=f"API key rotated for {provider}",
            session=session,
            user_id=user_id,
            old_value={
                "keychain_ref": old_key_reference,
                "rotated_at": (
                    existing_key.rotated_at.isoformat() if existing_key.rotated_at else None
                ),
            },
            new_value={
                "keychain_ref": new_key_reference,
                "validated": validate,
            },
            details={"zero_downtime": True},
            audit_context=audit_context,
        )

        await session.commit()

        logger.info(
            f"Key rotation complete for {user_id}/{provider}. "
            f"Old: {old_key_reference}, New: {new_key_reference}"
        )

        return existing_key

    def _generate_key_reference(self, user_id: str, provider: str) -> str:
        """Generate keychain reference identifier"""
        return f"piper_{user_id}_{provider}"
