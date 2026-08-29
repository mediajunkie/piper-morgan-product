"""
#1018 Phase 2 cluster regression — #1007 PII redaction.

The bug filed in #1007: "audit_transparency: security redaction not applied
to PII strings". Pre-#1018, `SecurityRedactor` was instantiated but the test
that verified redaction was failing because the in-memory list was being
populated before this assertion could see redaction take effect.

Phase 2 reconfirms: `SecurityRedactor` runs BEFORE the DB write inside
`audit_transparency.log_ethics_decision()`. The repository never sees
unredacted PII strings — only the post-redaction details payload.

This test mocks the repository at the call site so it doesn't need a
DB connection; it captures what would be persisted and asserts redaction
markers are present.
"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.models import EthicalDecision
from services.ethics.audit_transparency import AuditTransparency

pytestmark = pytest.mark.asyncio


@pytest.fixture
def decision_with_pii():
    """A decision whose audit_data contains an email address — should be
    redacted before persistence."""
    return EthicalDecision(
        decision_id="dec-test-1",
        boundary_type="harassment",
        violation_detected=True,
        explanation="Test decision",
        audit_data={
            "user_email": "alice@example.com",
            "phone": "555-123-4567",
            "session_id": "test-sess",
            "confidence": 0.9,
        },
        timestamp=datetime.now(timezone.utc),
        session_id="test-sess",
    )


async def test_redaction_runs_before_db_write(decision_with_pii):
    """SecurityRedactor must apply BEFORE `repo.add()` is called. The
    persisted entry should have `[REDACTED]` markers in place of the
    email + SSN-shaped string, not raw PII."""
    audit = AuditTransparency()

    # Capture what gets passed to the repository.
    captured_entries = []

    class _CapturingRepo:
        def __init__(self, session):
            pass

        async def add(self, entry):
            captured_entries.append(entry)

    # Patch the repo constructor + the session_scope context manager.
    with patch("services.database.repositories.EthicsAuditRepository", _CapturingRepo):
        with patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope"
        ) as mock_scope:
            # Make session_scope() a working async context manager
            mock_session = MagicMock()
            mock_session.commit = AsyncMock()

            class _Ctx:
                async def __aenter__(self):
                    return mock_session

                async def __aexit__(self, *args):
                    return False

            mock_scope.return_value = _Ctx()

            await audit.log_ethics_decision(decision_with_pii)

    # Verify the entry was captured
    assert len(captured_entries) == 1, f"expected exactly 1 add() call, got {len(captured_entries)}"
    entry = captured_entries[0]

    # Redaction should have replaced the email + phone shape in the audit_data
    persisted_audit_data = entry.details.get("audit_data", {})
    persisted_email = str(persisted_audit_data.get("user_email", ""))
    persisted_phone = str(persisted_audit_data.get("phone", ""))

    assert (
        "[REDACTED]" in persisted_email or "alice@example.com" not in persisted_email
    ), f"expected email to be redacted, got: {persisted_email!r}"
    assert (
        "[REDACTED]" in persisted_phone or "555-123-4567" not in persisted_phone
    ), f"expected phone to be redacted, got: {persisted_phone!r}"

    # Redacted flag should be True (preserved from AuditLogEntry default)
    assert entry.redacted is True


async def test_redaction_preserves_non_pii_fields(decision_with_pii):
    """Non-PII fields (confidence, session_id) should pass through
    redaction unchanged."""
    audit = AuditTransparency()
    captured_entries = []

    class _CapturingRepo:
        def __init__(self, session):
            pass

        async def add(self, entry):
            captured_entries.append(entry)

    with patch("services.database.repositories.EthicsAuditRepository", _CapturingRepo):
        with patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope"
        ) as mock_scope:
            mock_session = MagicMock()
            mock_session.commit = AsyncMock()

            class _Ctx:
                async def __aenter__(self):
                    return mock_session

                async def __aexit__(self, *args):
                    return False

            mock_scope.return_value = _Ctx()
            await audit.log_ethics_decision(decision_with_pii)

    entry = captured_entries[0]
    persisted_audit_data = entry.details.get("audit_data", {})
    # Non-string non-PII values pass through unchanged
    assert persisted_audit_data.get("confidence") == 0.9
    # session_id is a non-email-shaped string; should pass through
    assert persisted_audit_data.get("session_id") == "test-sess"


async def test_log_ethics_decision_swallows_db_failures(decision_with_pii):
    """Architect-ratified Q2 transaction-boundary semantic: an audit-write
    failure must NOT propagate up. log_ethics_decision should handle
    repository errors internally without raising into the caller."""
    audit = AuditTransparency()

    class _FailingRepo:
        def __init__(self, session):
            pass

        async def add(self, entry):
            raise RuntimeError("simulated DB failure")

    with patch("services.database.repositories.EthicsAuditRepository", _FailingRepo):
        with patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope"
        ) as mock_scope:
            mock_session = MagicMock()
            mock_session.commit = AsyncMock()

            class _Ctx:
                async def __aenter__(self):
                    return mock_session

                async def __aexit__(self, *args):
                    return False

            mock_scope.return_value = _Ctx()

            # Must NOT raise — failure is logged + counted, not propagated
            try:
                await audit.log_ethics_decision(decision_with_pii)
            except RuntimeError:
                pytest.fail(
                    "log_ethics_decision must not propagate audit-write failures "
                    "(transaction-boundary semantic per Architect Q2 ratification)"
                )
