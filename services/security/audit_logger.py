"""Audit logging service for security and compliance tracking

Provides comprehensive audit trail for:
- Authentication events (login, logout, token operations)
- API key management (store, retrieve, delete, rotate)
- Data modifications
- Security events

Usage:
    from services.security.audit_logger import audit_logger, EventType, Action, Severity

    # Log authentication event
    await audit_logger.log_auth_event(
        action=Action.LOGIN,
        status="success",
        message="User logged in successfully",
        session=session,
        user_id="user123",
        audit_context={"ip_address": "192.168.1.1", "user_agent": "Mozilla..."}
    )

    # Log API key event
    await audit_logger.log_api_key_event(
        action=Action.KEY_STORED,
        provider="openai",
        status="success",
        message="API key stored successfully",
        session=session,
        user_id="user123",
        audit_context=request_context
    )

Issue #249 CORE-AUDIT-LOGGING
"""

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Optional, Union, cast
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import AuditLog
from services.utils.utterance_log import utterance_preview

logger = logging.getLogger(__name__)


class EventType:
    """Audit event type constants"""

    AUTH = "auth"  # Authentication events
    API_KEY = "api_key"  # API key operations
    DATA = "data"  # Data modifications
    SYSTEM = "system"  # System events
    SECURITY = "security"  # Security events
    CONSEQUENTIAL = "consequential"  # #1680: external send/write by a censused site


class Action:
    """Audit action constants"""

    # Authentication
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    TOKEN_ISSUED = "token_issued"
    TOKEN_REVOKED = "token_revoked"
    TOKEN_REFRESHED = "token_refreshed"

    # API Keys
    KEY_STORED = "key_stored"
    KEY_RETRIEVED = "key_retrieved"
    KEY_DELETED = "key_deleted"
    KEY_ROTATED = "key_rotated"
    KEY_VALIDATED = "key_validated"
    KEY_VALIDATION_FAILED = "key_validation_failed"  # #1071: security-relevant failure event

    # Data Operations
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    EXPORTED = "exported"

    # Security Events
    PERMISSION_DENIED = "permission_denied"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"


class Severity:
    """Audit severity levels"""

    INFO = "info"  # Normal operations
    WARNING = "warning"  # Potential issues
    ERROR = "error"  # Errors that need attention
    CRITICAL = "critical"  # Critical security/system events


# #1680: the outcome a consequential site reports. "unconfirmed" is a call that returned
# (or raised) without a verifiable result; it is never mapped to "success".
CONSEQUENTIAL_STATUSES = frozenset({"success", "failed", "unconfirmed"})

# #1680 (Arch condition 3): a consequential row that could not be written is counted
# here, so a lost row reads as a coverage gap, never as "0 actions".
_consequential_write_failures = 0


def consequential_write_failures() -> int:
    """How many consequential audit rows failed to write in this process."""
    return _consequential_write_failures


def _coerce_principal(user_id: Union[str, UUID, None]) -> tuple[Optional[UUID], Optional[str]]:
    """(UUID for audit_logs.user_id, raw principal for details) — a non-UUID
    principal such as a Slack "U123" goes in details, never in the FK column."""
    if user_id is None:
        return None, None
    if isinstance(user_id, UUID):
        return user_id, None
    try:
        return UUID(str(user_id)), None
    except ValueError:
        return None, str(user_id)


class AuditLogger:
    """Centralized audit logging service"""

    async def log_consequential_action(
        self,
        *,
        site: str,
        status: str,
        user_id: Union[str, UUID, None],
        message: str,
        credits_spent: bool,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
    ) -> Optional[AuditLog]:
        """#1680 Criterion E: write one consequential-action row, in its own commit.

        Await it AFTER the external call returns (or raises), with ``status`` from the
        call's outcome: "success", "failed" or "unconfirmed". ``proactive``,
        ``external_message`` and ``hard_to_reverse`` come from the site's registry entry
        (services/security/consequential_sites.py); ``credits_spent`` is the site's own
        code path (did it call the LLM). Code sets every flag, never the model's words
        (ADR-080).

        The row is written in a fresh session and committed here, so the caller's
        rollback can never erase an action that already left the system. A failed write
        is logged at error level, counted (``consequential_write_failures()``) and
        returns None; it never raises into the caller. An unknown ``site`` or
        ``status`` raises ``ValueError`` (a programming error, caught by tests).
        """
        global _consequential_write_failures
        from services.security.consequential_sites import CONSEQUENTIAL_SITES

        entry = CONSEQUENTIAL_SITES.get(site)
        if entry is None:
            raise ValueError(f"#1680: unknown consequential site {site!r}; add a registry entry")
        if status not in CONSEQUENTIAL_STATUSES:
            raise ValueError(
                f"#1680: status must be one of {sorted(CONSEQUENTIAL_STATUSES)}, got {status!r}"
            )

        row_user_id, raw_principal = _coerce_principal(user_id)
        row_details: Dict[str, Any] = dict(details or {})
        if raw_principal is not None:
            row_details["principal"] = raw_principal

        try:
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope_fresh() as session:
                log = AuditLog(
                    id=str(uuid.uuid4()),
                    # the column's plugin type (_UUID_RETURN) is not uuid.UUID to mypy
                    user_id=cast(Any, row_user_id),
                    session_id=session_id,
                    event_type=EventType.CONSEQUENTIAL,
                    action=entry.key,
                    resource_type=resource_type,
                    resource_id=None if resource_id is None else str(resource_id),
                    status=status,
                    severity=Severity.INFO,
                    message=message,
                    details=row_details or None,
                    proactive=entry.proactive,
                    credits_spent=bool(credits_spent),
                    external_message=entry.external_message,
                    hard_to_reverse=entry.hard_to_reverse,
                )
                session.add(log)
                await session.commit()
        except Exception as e:  # silent-ok: #1680 write guard — counted + logged at error, never raised into the site that already acted
            _consequential_write_failures += 1
            logger.error(
                f"AUDIT: consequential row write failed | site={site} | status={status} | "
                f"error={type(e).__name__}: {e}",
                extra={"action": site, "status": status},
            )
            return None

        logger.info(
            f"AUDIT: consequential.{entry.key} | user={row_user_id} | status={status}",
            extra={"audit_log_id": log.id, "action": entry.key, "status": status},
        )
        return log

    async def log_event(
        self,
        event_type: str,
        action: str,
        status: str,
        severity: str,
        message: str,
        session: AsyncSession,
        user_id: Optional[UUID] = None,
        session_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        old_value: Optional[Dict[str, Any]] = None,
        new_value: Optional[Dict[str, Any]] = None,
        audit_context: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        """Log a comprehensive audit event

        Args:
            event_type: Type of event (auth, api_key, data, system, security)
            action: Specific action (login, key_stored, etc)
            status: Event status (success, failed, error)
            severity: Event severity (info, warning, error, critical)
            message: Human-readable message
            session: Database session
            user_id: User ID if applicable
            session_id: Session ID if applicable
            resource_type: Resource type being acted upon
            resource_id: Specific resource identifier
            details: Additional structured data
            old_value: Previous state for modifications
            new_value: New state for modifications
            audit_context: Request context (ip_address, user_agent, etc)

        Returns:
            Created AuditLog instance
        """
        # Extract request context
        context = audit_context or {}

        # Create audit log entry
        log = AuditLog(
            id=str(uuid.uuid4()),
            user_id=user_id,
            session_id=session_id,
            event_type=event_type,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            status=status,
            severity=severity,
            message=message,
            details=details,
            old_value=old_value,
            new_value=new_value,
            ip_address=context.get("ip_address"),
            user_agent=context.get("user_agent"),
            request_id=context.get("request_id"),
            request_path=context.get("request_path"),
        )

        # Store in database
        session.add(log)
        await session.flush()  # Don't commit - let caller handle transaction

        # Log to application logs as well
        logger.info(
            f"AUDIT: {event_type}.{action} | user={user_id} | status={status} | message={utterance_preview(message)}",
            extra={
                "audit_log_id": log.id,
                "event_type": event_type,
                "action": action,
                "user_id": user_id,
                "status": status,
                "severity": severity,
            },
        )

        return log

    async def log_auth_event(
        self,
        action: str,
        status: str,
        message: str,
        session: AsyncSession,
        user_id: Optional[UUID] = None,
        session_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        audit_context: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        """Convenience method for authentication events

        Args:
            action: Auth action (login, logout, token_issued, etc)
            status: Event status (success, failed)
            message: Human-readable message
            session: Database session
            user_id: User ID
            session_id: Session ID if applicable
            details: Additional data (username, reason, etc)
            audit_context: Request context

        Returns:
            Created AuditLog instance
        """
        severity = Severity.WARNING if status == "failed" else Severity.INFO

        return await self.log_event(
            event_type=EventType.AUTH,
            action=action,
            status=status,
            severity=severity,
            message=message,
            session=session,
            user_id=user_id,
            session_id=session_id,
            resource_type="auth",
            details=details,
            audit_context=audit_context,
        )

    async def log_api_key_event(
        self,
        action: str,
        provider: str,
        status: str,
        message: str,
        session: AsyncSession,
        user_id: UUID,
        details: Optional[Dict[str, Any]] = None,
        old_value: Optional[Dict[str, Any]] = None,
        new_value: Optional[Dict[str, Any]] = None,
        audit_context: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        """Convenience method for API key events

        Args:
            action: API key action (key_stored, key_rotated, etc)
            provider: Provider name (openai, anthropic, etc)
            status: Event status (success, failed)
            message: Human-readable message
            session: Database session
            user_id: User ID
            details: Additional data (keychain_ref, validation result, etc)
            old_value: Previous state for rotations
            new_value: New state for rotations
            audit_context: Request context

        Returns:
            Created AuditLog instance
        """
        # Add provider to details
        event_details = details or {}
        event_details["provider"] = provider

        return await self.log_event(
            event_type=EventType.API_KEY,
            action=action,
            status=status,
            severity=Severity.INFO,
            message=message,
            session=session,
            user_id=user_id,
            resource_type="api_key",
            resource_id=provider,
            details=event_details,
            old_value=old_value,
            new_value=new_value,
            audit_context=audit_context,
        )

    async def log_security_event(
        self,
        action: str,
        severity: str,
        message: str,
        session: AsyncSession,
        user_id: Optional[UUID] = None,
        details: Optional[Dict[str, Any]] = None,
        audit_context: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        """Convenience method for security events

        Args:
            action: Security action (permission_denied, suspicious_activity, etc)
            severity: Event severity (warning, error, critical)
            message: Human-readable message
            session: Database session
            user_id: User ID if applicable
            details: Additional data (attempted action, detection reason, etc)
            audit_context: Request context

        Returns:
            Created AuditLog instance
        """
        return await self.log_event(
            event_type=EventType.SECURITY,
            action=action,
            status="detected",
            severity=severity,
            message=message,
            session=session,
            user_id=user_id,
            resource_type="security",
            details=details,
            audit_context=audit_context,
        )


# Global instance
audit_logger = AuditLogger()
