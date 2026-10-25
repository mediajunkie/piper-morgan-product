"""
User API Key Management Service

Handles per-user API keys with OS keychain storage.
Stores metadata in database, actual keys in OS keychain.

Issue #228 CORE-USERS-API Phase 1C
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.config.llm_config_service import (
    KEY_CHECK_UNAVAILABLE,
    KEY_CHECK_UNAVAILABLE_MESSAGE,
    KeyCheckUnavailable,
    LLMConfigService,
    humanize_validation_result,
)
from services.database.models import UserAPIKey
from services.infrastructure.keychain_service import KeychainService
from services.security.api_key_validator import APIKeyValidator
from services.security.audit_logger import Action, audit_logger
from services.security.field_encryption import DecryptionError, FieldEncryptionService

logger = logging.getLogger(__name__)

# #358: the one HKDF context every provider's secret used to share.
USER_SECRET_CONTEXT = "user_api_keys.secret"
# #1982 (Arch, 2026-10-11): GitHub credentials get their OWN context so the MCP app can
# be handed a decrypt-only subkey for exactly these rows and nothing else. ``github`` is
# the user's own PAT (Settings → GitHub); ``github_mcp_oauth`` is the OAuth grant
# (ConnectorGrantStore). Every other provider stays on USER_SECRET_CONTEXT.
GITHUB_SECRET_CONTEXT = "user_api_keys.secret.github"
GITHUB_PROVIDERS = frozenset({"github", "github_mcp_oauth"})
# Reads of a GitHub row use GITHUB_SECRET_CONTEXT only. The legacy-shared-context
# fallback was live until scripts/reencrypt_github_secrets_1982.py reported zero
# legacy rows on alpha: 2026-10-13 16:36 PT, PM's hand, total=2 rewritten=2
# verified_new=2 legacy=0 failed=0 (HOST's condition 2; #1982). Flipped to False in
# the commit that records that count. The branch stays as code so a future context
# split can reuse it; a scoped process (the MCP app) never holds the legacy subkey, so
# the fallback is skipped there by construction (``supports`` is False), not by this flag.
GITHUB_LEGACY_CONTEXT_FALLBACK = False


def secret_context(provider: str) -> str:
    """The HKDF context a provider's secret is encrypted under (#1982)."""
    return GITHUB_SECRET_CONTEXT if provider in GITHUB_PROVIDERS else USER_SECRET_CONTEXT


class UserKeyReadFailed(Exception):
    """#2151 (Arch 10-24 16:49): an active key row exists but its secret couldn't be read.

    A row that exists is not absence: ``retrieve_user_key_strict`` raises this where
    ``retrieve_user_key`` answers None."""


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
        *,
        security_check: bool = True,
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
            security_check: (keyword-only) Run the #268 format/strength/leak
                validator first (default). #1982: False ONLY for a key the caller has just
                verified live with its provider (the GitHub PAT dual write,
                and the backfill of PATs that were accepted that way): a live
                acceptance outranks a regex, and a rejection here would land
                AFTER the keychain write, as a half-save. The callers allowed to
                pass False are a CLOSED LIST enforced by
                tests/test_architecture_enforcement.py::TestSecurityCheckBypassCallers1982.

        Returns:
            UserAPIKey database record, or None if store=False. When
            provider-API validation failed but the key was stored anyway
            (validate=True, store=True), the returned record carries a
            transient (non-persisted) `.validation_message` attribute with
            the honest cause (rejected credential vs. no credits/billing,
            #1718) — None when validation passed or wasn't attempted.

        Raises:
            ValueError: If validation fails or key invalid (store=False only;
                the ValueError's message is the honest #1718 cause)

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
        if security_check:  # #1982: see the docstring before passing False
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
                        error_messages.append(
                            f"Key too weak: entropy {entropy_pct}% (required: 70%)"
                        )
                    if not validation_report.leak_safe:
                        source = validation_report.leak_result.source or "known_leak_database"
                        error_messages.append(f"Key found in breach database: {source}")

                    error_detail = (
                        " | ".join(error_messages)
                        if error_messages
                        else "Security validation failed"
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
        validation_message: Optional[str] = None
        if validate:
            try:
                # #1718: use the DETAILED result (is_valid + error_code +
                # provider error_message), not the bare bool — so the specific
                # cause (rejected credential vs. no credits/billing) survives
                # to the caller instead of collapsing to flat "invalid".
                validation_result = await self._llm_config.validate_api_key_detailed(
                    provider, api_key
                )
                is_valid = validation_result.is_valid
                # #2125: an unrun check is not a verdict; never let a route read it
                # as "invalid". Validation-only callers get the typed error; a store
                # proceeds as before with is_valid False and the cause in the log.
                if validation_result.error_code == KEY_CHECK_UNAVAILABLE and not store:
                    raise KeyCheckUnavailable(KEY_CHECK_UNAVAILABLE_MESSAGE)
                if not is_valid:
                    validation_message = humanize_validation_result(validation_result)
                    logger.warning(f"Provider API validation failed for {provider}")
                    # Issue #485: For validation-only mode, raise error on invalid key
                    if not store:
                        raise ValueError(validation_message)
                logger.info(f"Provider API validation result for {provider}: {is_valid}")
            except (ValueError, KeyCheckUnavailable):
                # Re-raise validation errors and the typed unavailable error
                raise
            except Exception as e:
                logger.warning(f"Provider API validation error for {provider}: {type(e).__name__}")
                # #2125: a fault of ours during the check is not a verdict on the key
                if not store:
                    raise KeyCheckUnavailable(KEY_CHECK_UNAVAILABLE_MESSAGE) from e

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
            self._encryptor.encrypt(api_key, secret_context(provider)) if self._encryptor else None
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
            # #1718: transient, non-persisted attribute — the honest cause
            # (rejected credential vs. no credits/billing) for the immediate
            # caller (the /keys/store route) to surface, WITHOUT changing the
            # "store even if unvalidated" behavior (#485) or the return type
            # every other caller already depends on.
            setattr(
                existing_key, "validation_message", validation_message
            )  # transient, read via getattr
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
            # #1718: see the identical comment on the update branch above.
            setattr(
                user_key, "validation_message", validation_message
            )  # transient, read via getattr
            return user_key

    def _decrypt_secret(self, token: str, provider: str) -> Optional[str]:
        """Decrypt a stored secret under the provider's context; ``None`` on failure.

        #1982: a GitHub row written before the context split still sits under the
        legacy shared context. Try the provider's own context first, then the legacy
        one — only while GITHUB_LEGACY_CONTEXT_FALLBACK holds AND this process holds
        that subkey (a scoped MCP process does not, and must not: the fallback stays
        off its path by construction). Never logs the token or the plaintext.
        """
        assert self._encryptor is not None
        context = secret_context(provider)
        try:
            return self._encryptor.decrypt(token, context)
        except DecryptionError:
            pass
        legacy_applies = (
            context != USER_SECRET_CONTEXT
            and GITHUB_LEGACY_CONTEXT_FALLBACK
            and self._encryptor.supports(USER_SECRET_CONTEXT)
        )
        if not legacy_applies:
            return None
        try:
            return self._encryptor.decrypt(token, USER_SECRET_CONTEXT)
        except DecryptionError:
            return None

    async def retrieve_user_key_strict(
        self, session: AsyncSession, user_id: str, provider: str
    ) -> Optional[str]:
        """``retrieve_user_key`` that tells absence from failure (#2151, Arch 10-24 16:49).

        None only when no active row exists. An active row whose secret can't be read
        (the decrypt fails and the keychain has nothing, or the keychain store fails)
        raises ``UserKeyReadFailed``. A database error propagates. ``retrieve_user_key``
        keeps its None-on-failure contract for callers that only try a key."""
        try:
            row_user = uuid.UUID(str(user_id))
        except ValueError:
            return None  # the column is a UUID: no row can exist for this principal
        result = await session.execute(
            select(UserAPIKey).where(
                and_(
                    UserAPIKey.user_id == row_user,
                    UserAPIKey.provider == provider,
                    UserAPIKey.is_active == True,
                )
            )
        )
        user_key = result.scalar_one_or_none()
        if not user_key:
            return None
        if user_key.encrypted_secret and self._encryptor:
            secret = self._decrypt_secret(user_key.encrypted_secret, provider)
            if secret is not None:
                return secret
        read = await self._keychain.aread_secret(provider, username=user_id)
        if read.is_present and read.value:
            return read.value
        raise UserKeyReadFailed(
            f"an active {provider} key row could not be read ({read.provenance.value})"
        )

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
            secret = self._decrypt_secret(user_key.encrypted_secret, provider)
            if secret is not None:
                return secret
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

        #1870: internally uses `validate_api_key_detailed()` (not the bare-bool
        `validate_api_key()`) so the specific cause survives — same #1718 pattern
        as `store_user_key`. Return type stays `bool` (existing callers —
        web/api/routes/api_keys.py's `/validate` route, cli/commands/keys.py,
        scripts/status_checker.py — all consume a bare bool and are unaffected).
        The honest reason is exposed the SAME way `store_user_key` exposes it: a
        transient (non-persisted) `.validation_message` attribute set on the
        `UserAPIKey` DB record this method already fetches/updates — None when
        valid or no record exists.

        ⚠️ Unlike `store_user_key` (which hands its caller the SAME object it
        just annotated, in the same call), this method returns a bare bool, so
        a caller can only see `.validation_message` by already holding a live
        Python reference to that same `UserAPIKey` row in the same session
        (e.g. having fetched it themselves earlier). SQLAlchemy's identity map
        holds session objects by WEAK reference; an unreferenced row can be
        garbage-collected between calls, and a caller who queries fresh
        AFTER calling this method with no reference held in between may get a
        newly-hydrated instance without the attribute (confirmed empirically,
        #1870). Not a bug in this method — it's the nature of a side-channel
        attribute on a return value the method doesn't hand back. A future
        caller that needs this reliably should hold its own reference (fetch
        the row before or keep the one from `store_user_key`), not assume a
        fresh query will see it.
        """
        # Retrieve key
        api_key = await self.retrieve_user_key(session, user_id, provider)
        if not api_key:
            logger.warning(f"No key found to validate for {user_id}/{provider}")
            return False

        # Validate with provider
        try:
            validation_result = await self._llm_config.validate_api_key_detailed(provider, api_key)
            is_valid = validation_result.is_valid
            validation_message = None if is_valid else humanize_validation_result(validation_result)

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
                # #1870: transient attribute, same pattern as store_user_key.
                setattr(
                    user_key, "validation_message", validation_message
                )  # transient, read via getattr

            return is_valid

        except Exception as e:
            logger.error(f"Validation failed for {user_id}/{provider}: {e}")
            return False

    # NOTE (#1436 Tier-3 rider): the orphaned KeyRotationService was deleted;
    # its documented intent — a future PER-USER bulk-rotation mode — lives on
    # here as the natural home if that need materializes. This rotates ONE key.
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
        # #1870: use the DETAILED result (same #1718 pattern as store_user_key)
        # so a rejected-credential vs. no-credits/billing rotation failure
        # surfaces the honest reason instead of a flat "validation failed".
        validation_message: Optional[str] = None
        if validate:
            try:
                validation_result = await self._llm_config.validate_api_key_detailed(
                    provider, new_api_key
                )
                if not validation_result.is_valid:
                    validation_message = humanize_validation_result(validation_result)
                    raise ValueError(validation_message)
                logger.info(f"New API key validated successfully for {provider}")
            except ValueError:
                raise
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
            self._encryptor.encrypt(new_api_key, secret_context(provider))
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

        # #1870: transient (non-persisted) attribute, same pattern as
        # store_user_key — always None here since a validation failure above
        # raises ValueError(validation_message) before this point is reached;
        # kept for parity/future callers that inspect the returned record.
        setattr(
            existing_key, "validation_message", validation_message
        )  # transient, read via getattr
        return existing_key

    def _generate_key_reference(self, user_id: str, provider: str) -> str:
        """Generate keychain reference identifier"""
        return f"piper_{user_id}_{provider}"
