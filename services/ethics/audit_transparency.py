"""
PM-087 Audit Transparency System
User-visible audit logs with security redactions for transparency

Leverages existing infrastructure:
- services/infrastructure/monitoring/ethics_metrics.py
- services/infrastructure/logging/config.py
- services/domain/models.py patterns

Issue #1018 Phase 2 (2026-05-02): replaced in-memory storage with durable
PostgreSQL backing via EthicsAuditRepository. Transaction-boundary semantic
is deliberate: an audit-write failure must NOT roll back the ethics decision
(per Architect Q2 ratification 2026-04-30). Each write opens its own session
via AsyncSessionFactory, isolating audit failures from the request transaction.
Closes #1006 (datetime offset, now TIMESTAMPTZ throughout), #1007 (PII
redaction still runs before DB write — SecurityRedactor unchanged), #1008
(read endpoints fully async with proper session usage).
"""

import hashlib
import json
import re
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from services.domain.models import BoundaryViolation, EthicalDecision
from services.infrastructure.logging.config import get_ethics_logger
from services.infrastructure.monitoring.ethics_metrics import ethics_metrics


class SecurityRedactor:
    """Security redaction for sensitive data in audit logs"""

    def __init__(self):
        # Patterns for sensitive data.
        # Issue #1007 fix (2026-05-02): added the 3-3-4-digit phone-number
        # pattern (e.g., "555-123-4567"). Pre-fix, only the 9-digit SSN
        # pattern (3-2-4) was present, so canonical phone-number-shaped
        # PII (the most common) was not redacted.
        self.sensitive_patterns = [
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN (3-2-4)
            r"\b\d{3}-\d{3}-\d{4}\b",  # Phone number (3-3-4) — #1007 fix
            r"\b\(\d{3}\)\s*\d{3}-\d{4}\b",  # Phone number ((NNN) NNN-NNNN)
            r"\b\d{4}-\d{4}-\d{4}-\d{4}\b",  # Credit card
            r"\b\d{10,11}\b",  # Phone numbers (digit-only)
        ]

        # Redaction replacement
        self.redaction_replacement = "[REDACTED]"

    def redact_sensitive_data(self, text: str) -> str:
        """Redact sensitive data from text"""
        redacted_text = text

        for pattern in self.sensitive_patterns:
            redacted_text = re.sub(pattern, self.redaction_replacement, redacted_text)

        return redacted_text

    def redact_content_preview(self, content: str, max_length: int = 100) -> str:
        """Create redacted content preview"""
        if not content:
            return ""

        # Redact sensitive data
        redacted_content = self.redact_sensitive_data(content)

        # Truncate if too long. Off-by-3 fix (#1018 sweep, 2026-05-02):
        # the prior code did `text[:max_length] + "..."` which produced
        # max_length+3 chars; tests asserting `<= max_length` failed.
        # Reserve space for the ellipsis so total stays within max_length.
        if len(redacted_content) > max_length:
            ellipsis = "..."
            cutoff = max(0, max_length - len(ellipsis))
            redacted_content = redacted_content[:cutoff] + ellipsis

        return redacted_content


class AuditLogEntry:
    """Individual audit log entry for transparency"""

    def __init__(
        self,
        entry_id: str,
        event_type: str,
        timestamp: datetime,
        session_id: Optional[str] = None,
        user_id: Optional[UUID] = None,
        details: Dict[str, Any] = None,
        redacted: bool = True,
    ):
        self.entry_id = entry_id
        self.event_type = event_type
        self.timestamp = timestamp
        self.session_id = session_id
        self.user_id = user_id
        self.details = details or {}
        self.redacted = redacted

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response"""
        return {
            "entry_id": self.entry_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "session_id": self.session_id,
            "user_id": self.user_id,
            "details": self.details,
            "redacted": self.redacted,
        }


class AuditTransparency:
    """Audit transparency system for user-visible audit logs.

    Backed by PostgreSQL via `EthicsAuditRepository` (Issue #1018 Phase 2,
    2026-05-02). Pre-#1018 this stored entries in an in-memory list, lost on
    every restart. The transparency endpoints could lie. Now they don't.
    """

    def __init__(self):
        self.ethics_logger = get_ethics_logger(__name__)
        self.metrics = ethics_metrics
        self.redactor = SecurityRedactor()

        # Retention policy (90 days). Enforced by `EthicsAuditCleanupJob`
        # scheduled task (sibling of BlacklistCleanupJob); cleanup_old_entries
        # method below also exposes it for the manual /transparency/cleanup
        # endpoint.
        self.log_retention_days = 90

        # Transparency metrics — these are process-lifetime counters for ops
        # observability (NOT user-facing audit data). Reset on restart is fine.
        self.transparency_requests = 0
        self.audit_log_entries_total = 0
        self.redaction_operations = 0

    async def log_ethics_decision(self, decision: EthicalDecision) -> None:
        """Log ethics decision for transparency.

        Persists via `EthicsAuditRepository` in a fresh DB session opened
        for this call. Transaction-boundary is deliberate: write failures
        here MUST NOT propagate up the request transaction (per Architect
        Q2 ratification 2026-04-30) — losing a single audit entry is a
        smaller failure than rolling back the ethics decision itself.
        """
        try:
            # Create audit log entry. SecurityRedactor still runs BEFORE
            # the DB write — closes #1007 (PII redaction not applied).
            entry = AuditLogEntry(
                entry_id=f"audit_{uuid.uuid4().hex[:24]}",
                event_type="ethics_decision",
                timestamp=decision.timestamp,
                session_id=decision.session_id,
                details={
                    "boundary_type": decision.boundary_type,
                    "violation_detected": decision.violation_detected,
                    "explanation": decision.explanation,
                    "audit_data": self._redact_audit_data(decision.audit_data),
                },
            )

            # Persist via repository. Lazy import keeps services/database
            # out of import chain at module load time.
            from services.database.repositories import EthicsAuditRepository
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as session:
                repo = EthicsAuditRepository(session)
                await repo.add(entry)
                await session.commit()

            # Record metrics
            self.audit_log_entries_total += 1
            self.metrics.record_audit_trail_entry(success=True)

            # Log transparency event
            self.ethics_logger.log_behavior_pattern(
                "audit_log_entry",
                {
                    "entry_id": entry.entry_id,
                    "event_type": entry.event_type,
                    "session_id": entry.session_id,
                },
            )

        except Exception as e:
            self.metrics.record_audit_trail_entry(success=False)

            # Log error
            self.ethics_logger.log_boundary_violation(
                "audit_log_error", {"error": str(e), "decision_id": decision.decision_id}
            )

    async def log_boundary_violation(self, violation: BoundaryViolation) -> None:
        """Log boundary violation for transparency.

        Same transaction-boundary semantic as `log_ethics_decision`:
        per-call session, audit-write failure does NOT propagate up.
        """
        try:
            # SecurityRedactor runs BEFORE DB write (closes #1007).
            entry = AuditLogEntry(
                entry_id=f"audit_{uuid.uuid4().hex[:24]}",
                event_type="boundary_violation",
                timestamp=violation.timestamp,
                session_id=violation.session_id,
                details={
                    "violation_type": violation.violation_type,
                    "severity": violation.severity,
                    "context_preview": self.redactor.redact_content_preview(violation.context),
                    "audit_data": self._redact_audit_data(violation.audit_data),
                },
            )

            from services.database.repositories import EthicsAuditRepository
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as session:
                repo = EthicsAuditRepository(session)
                await repo.add(entry)
                await session.commit()

            # Record metrics
            self.audit_log_entries_total += 1
            self.metrics.record_audit_trail_entry(success=True)

            # Log transparency event
            self.ethics_logger.log_behavior_pattern(
                "audit_log_entry",
                {
                    "entry_id": entry.entry_id,
                    "event_type": entry.event_type,
                    "session_id": entry.session_id,
                },
            )

        except Exception as e:
            self.metrics.record_audit_trail_entry(success=False)

            # Log error
            self.ethics_logger.log_boundary_violation(
                "audit_log_error", {"error": str(e), "violation_id": violation.violation_id}
            )

    async def log_output_filter_decision(self, decision: Any) -> None:
        """Log a post-generation OutputFilter decision (Issue #1017 Phase 2.3).

        Sibling of `log_ethics_decision` per Architect Q4 ratification —
        the OutputFilterDecision shape differs enough from BoundaryDecision
        that overloading the existing entry point would muddy semantics at
        the call sites. Same Postgres table (`ethics_audit_log`) via the
        flexible `details` JSONB column; `event_type="output_filter_decision"`
        distinguishes the records.

        Architectural invariant (Pattern-064-adjacent): the audit envelope
        carries **hashes only** — never raw filtered content. The
        OutputFilterDecision dataclass enforces this at construction time
        (only hash fields are populated, not raw content); this function
        treats the decision's `to_dict()` output as already-safe.

        Transaction-boundary semantic matches `log_ethics_decision`:
        per-call session_scope, write failures swallowed (audit-write
        failure must not propagate up the LLM call's transaction).

        Args:
            decision: OutputFilterDecision (from services.ethics.output_filter).
                Typed as Any to avoid an import cycle (output_filter imports
                from audit_transparency for the redactor pattern source).
        """
        try:
            details = decision.to_dict()
            # Sanity check the hash-only invariant — never serialize raw
            # filtered_content or original_content into the audit log.
            # to_dict() already returns hashes, but if a future caller
            # mutates audit_metadata with raw text this catches it on
            # the next read.
            for k, v in list(details.get("audit_metadata", {}).items()):
                if isinstance(v, str) and len(v) > 256:
                    # Suspiciously long string in audit_metadata — likely raw
                    # content leaked through. Truncate + flag.
                    details["audit_metadata"][k] = v[:64] + "...[TRUNCATED]"
                    details.setdefault("invariant_violations", []).append(
                        f"audit_metadata.{k} truncated (exceeded 256 chars)"
                    )

            user_id_str = details.get("user_id")
            user_id_uuid: Optional[UUID] = None
            if user_id_str:
                try:
                    user_id_uuid = UUID(user_id_str)
                except (ValueError, TypeError):
                    # user_id is a string identifier, not UUID — pass through.
                    user_id_uuid = None

            entry = AuditLogEntry(
                entry_id=f"audit_{uuid.uuid4().hex[:24]}",
                event_type="output_filter_decision",
                timestamp=decision.timestamp,
                session_id=details.get("session_id"),
                user_id=user_id_uuid,
                details=details,
            )

            from services.database.repositories import EthicsAuditRepository
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as session:
                repo = EthicsAuditRepository(session)
                await repo.add(entry)
                await session.commit()

            self.audit_log_entries_total += 1
            self.metrics.record_audit_trail_entry(success=True)

            self.ethics_logger.log_behavior_pattern(
                "audit_log_entry",
                {
                    "entry_id": entry.entry_id,
                    "event_type": entry.event_type,
                    "session_id": entry.session_id,
                    "decision_id": details.get("decision_id"),
                    "action_taken": details.get("action_taken"),
                    "severity": details.get("severity"),
                },
            )

        except Exception as e:
            self.metrics.record_audit_trail_entry(success=False)
            self.ethics_logger.log_boundary_violation(
                "audit_log_error",
                {
                    "error": str(e),
                    "decision_id": getattr(decision, "decision_id", "unknown"),
                    "event_type": "output_filter_decision",
                },
            )

    async def get_user_audit_log(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's audit log entries (read path; queries DB).

        Closes #1008: end-to-end async, awaits session.execute through the
        repository, no list-as-awaitable mistake.
        """
        try:
            self.transparency_requests += 1

            from services.database.repositories import EthicsAuditRepository
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as session:
                repo = EthicsAuditRepository(session)
                entries = await repo.find_by_session(session_id, limit=limit)

            # Convert to dictionary format
            audit_log = [entry.to_dict() for entry in entries]

            # Log transparency request
            self.ethics_logger.log_behavior_pattern(
                "transparency_request",
                {
                    "session_id": session_id,
                    "entries_returned": len(audit_log),
                    "request_limit": limit,
                },
            )

            return audit_log

        except Exception as e:
            # Log error
            self.ethics_logger.log_boundary_violation(
                "transparency_request_error", {"error": str(e), "session_id": session_id}
            )

            return []

    async def get_system_audit_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get system-wide audit summary (admin only). Queries DB."""
        try:
            from services.database.repositories import EthicsAuditRepository
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as session:
                repo = EthicsAuditRepository(session)
                summary = await repo.summarize_recent(days=days)

            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
            # Augment with response-shape compatibility for the existing endpoint
            return {
                "total_entries": summary["total_entries"],
                "unique_sessions": None,  # NOTE: legacy field; would require COUNT(DISTINCT session_id)
                "event_type_breakdown": summary["events_by_type"],
                "boundary_breakdown": summary["boundary_breakdown"],
                "date_range": {
                    "start": cutoff_date.isoformat(),
                    "end": datetime.now(timezone.utc).isoformat(),
                },
            }

        except Exception as e:
            # Log error
            self.ethics_logger.log_boundary_violation("audit_summary_error", {"error": str(e)})

            return {"error": "Failed to generate audit summary"}

    async def cleanup_old_entries(self) -> int:
        """Clean up old audit log entries. Returns count deleted.

        Used by both the manual `POST /transparency/cleanup` endpoint
        and the scheduled `EthicsAuditCleanupJob` (24h cadence).
        Closes #1006: TIMESTAMPTZ throughout, no naive-datetime comparisons.
        """
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=self.log_retention_days)

        try:
            from services.database.repositories import EthicsAuditRepository
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as session:
                repo = EthicsAuditRepository(session)
                cleaned_count = await repo.delete_older_than(cutoff_date)
                await session.commit()

            if cleaned_count > 0:
                self.ethics_logger.log_behavior_pattern(
                    "audit_log_cleanup",
                    {
                        "entries_removed": cleaned_count,
                        "retention_days": self.log_retention_days,
                    },
                )

            return cleaned_count
        except Exception as e:
            self.ethics_logger.log_boundary_violation(
                "audit_cleanup_error", {"error": str(e)}
            )
            return 0

    def _redact_audit_data(self, audit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Redact sensitive data from audit data"""
        if not audit_data:
            return {}

        redacted_data = {}

        for key, value in audit_data.items():
            if isinstance(value, str):
                # Redact sensitive strings
                redacted_data[key] = self.redactor.redact_sensitive_data(value)
            elif isinstance(value, dict):
                # Recursively redact nested dictionaries
                redacted_data[key] = self._redact_audit_data(value)
            else:
                # Keep non-string values as-is
                redacted_data[key] = value

        self.redaction_operations += 1
        return redacted_data

    async def get_transparency_stats(self) -> Dict[str, Any]:
        """Get transparency system statistics. Now async because total
        + recent counts come from DB queries (Issue #1018 Phase 2)."""
        try:
            from services.database.repositories import EthicsAuditRepository
            from services.database.session_factory import AsyncSessionFactory
            from sqlalchemy import func, select
            from services.database.models import EthicsAuditLogDB

            async with AsyncSessionFactory.session_scope() as session:
                repo = EthicsAuditRepository(session)
                total = await repo.count()

                # 24h recent count via direct query (no repository helper
                # since this is the only caller and it's a simple count).
                cutoff_24h = datetime.now(timezone.utc) - timedelta(days=1)
                recent_result = await session.execute(
                    select(func.count(EthicsAuditLogDB.entry_id)).where(
                        EthicsAuditLogDB.timestamp >= cutoff_24h
                    )
                )
                recent_24h = recent_result.scalar_one() or 0
        except Exception as e:
            self.ethics_logger.log_boundary_violation(
                "transparency_stats_error", {"error": str(e)}
            )
            total = -1  # sentinel: stats unavailable
            recent_24h = -1

        return {
            "total_audit_entries": total,
            "transparency_requests": self.transparency_requests,
            "audit_log_entries_total": self.audit_log_entries_total,
            "redaction_operations": self.redaction_operations,
            "log_retention_days": self.log_retention_days,
            "recent_entries_24h": recent_24h,
        }


# Singleton instance
audit_transparency = AuditTransparency()
