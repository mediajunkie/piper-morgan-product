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
from typing import Any, Dict, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import AuditLog

logger = logging.getLogger(__name__)


class EventType:
    """Audit event type constants"""

    AUTH = "auth"  # Authentication events
    API_KEY = "api_key"  # API key operations
    DATA = "data"  # Data modifications
    SYSTEM = "system"  # System events
    SECURITY = "security"  # Security events


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


class AuditLogger:
    """Centralized audit logging service"""

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
            f"AUDIT: {event_type}.{action} | user={user_id} | status={status} | message={message}",
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
