"""Integration tests for OutputFilter audit envelope (Issue #1017 Phase 2.5).

Exercises round-trip persistence of OutputFilterDecision through the real
Postgres ethics_audit_log table (introduced by #1018 Phase 2 May 2 2026).

Verifies:
- log_output_filter_decision() writes a row reachable via
  EthicsAuditRepository.find_by_session()
- event_type="output_filter_decision" distinguishes from other audit kinds
- Hashes survive the round-trip; raw content never lands in the DB
- LLMClient end-to-end (mock _complete_raw + real DB write) produces an
  auditable record per call

Requires local Postgres on port 5433 per CLAUDE.md Quick Reference.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.database.repositories import EthicsAuditRepository
from services.database.session_factory import AsyncSessionFactory
from services.ethics.audit_transparency import audit_transparency
from services.ethics.output_filter import (
    Action,
    OutputFilter,
    OutputFilterDecision,
    Profile,
    Severity,
)

pytestmark = pytest.mark.integration


@pytest.fixture
async def db_session():
    async with AsyncSessionFactory.session_scope() as session:
        yield session


def _decision(
    surface: str = "conversation",
    action: str = Action.REDACT_IN_PLACE,
    severity: str = Severity.MEDIUM,
    matched_rules: list[str] | None = None,
    session_id: str = None,
) -> OutputFilterDecision:
    return OutputFilterDecision(
        timestamp=datetime.now(timezone.utc),
        user_id=str(uuid4()),
        session_id=session_id or f"sess-{uuid4().hex[:12]}",
        surface=surface,
        profile_applied=Profile.USER_VISIBLE,
        matched_rules=matched_rules or ["pii:email"],
        severity=severity,
        redactions_count=1,
        action_taken=action,
        original_content_hash="a" * 64,
        filtered_content_hash="b" * 64,
    )


@pytest.mark.asyncio
async def test_log_output_filter_decision_round_trip(db_session):
    """Write a decision via log_output_filter_decision; read it back via
    EthicsAuditRepository; verify event_type + details round-trip."""
    session_id = f"test-1017-sess-{uuid4().hex[:12]}"
    decision = _decision(session_id=session_id)

    await audit_transparency.log_output_filter_decision(decision)

    # Fresh repo on the test session to query the row.
    repo = EthicsAuditRepository(db_session)
    entries = await repo.find_by_session(session_id, limit=10)

    assert len(entries) == 1
    entry = entries[0]
    assert entry.event_type == "output_filter_decision"
    assert entry.session_id == session_id
    assert entry.details["surface"] == "conversation"
    assert entry.details["action_taken"] == Action.REDACT_IN_PLACE
    assert entry.details["severity"] == Severity.MEDIUM
    assert entry.details["redactions_count"] == 1
    # Hashes survive the round-trip; raw content fields absent.
    assert entry.details["original_content_hash"] == "a" * 64
    assert entry.details["filtered_content_hash"] == "b" * 64


@pytest.mark.asyncio
async def test_canned_substitute_decision_records_critical_severity(db_session):
    """A boundary-violation decision (severity=critical, action=canned)
    persists with the full decision shape preserved."""
    session_id = f"test-1017-sess-{uuid4().hex[:12]}"
    decision = _decision(
        session_id=session_id,
        action=Action.CANNED_SUBSTITUTE,
        severity=Severity.CRITICAL,
        matched_rules=["boundary:harassment"],
    )

    await audit_transparency.log_output_filter_decision(decision)

    repo = EthicsAuditRepository(db_session)
    entries = await repo.find_by_session(session_id, limit=10)

    assert len(entries) == 1
    entry = entries[0]
    assert entry.details["action_taken"] == Action.CANNED_SUBSTITUTE
    assert entry.details["severity"] == Severity.CRITICAL
    assert "boundary:harassment" in entry.details["matched_rules"]


@pytest.mark.asyncio
async def test_regenerate_chain_persists_both_attempts(db_session):
    """Both attempts in the regenerate flow write distinct rows with
    attempt_number + prior_attempt_decision_id linking them."""
    session_id = f"test-1017-sess-{uuid4().hex[:12]}"

    first = _decision(
        session_id=session_id,
        action=Action.CANNED_SUBSTITUTE,
        severity=Severity.CRITICAL,
        matched_rules=["boundary:harassment"],
    )
    first.attempt_number = 1
    first.prior_attempt_decision_id = None
    await audit_transparency.log_output_filter_decision(first)

    second = _decision(
        session_id=session_id,
        action=Action.PASSTHROUGH,
        severity=Severity.LOW,
        matched_rules=[],
    )
    second.attempt_number = 2
    second.prior_attempt_decision_id = first.decision_id
    await audit_transparency.log_output_filter_decision(second)

    repo = EthicsAuditRepository(db_session)
    entries = await repo.find_by_session(session_id, limit=10)
    # Sort newest-first per repository default; second attempt should be first.
    assert len(entries) == 2
    attempts = sorted(entries, key=lambda e: e.details["attempt_number"])
    assert attempts[0].details["attempt_number"] == 1
    assert attempts[0].details["prior_attempt_decision_id"] is None
    assert attempts[1].details["attempt_number"] == 2
    assert attempts[1].details["prior_attempt_decision_id"] == first.decision_id


@pytest.mark.asyncio
async def test_llm_client_end_to_end_writes_audit_row(db_session):
    """Round-trip through LLMClient.complete() with mocked _complete_raw,
    real OutputFilter, real audit envelope. Verifies the full integration
    of Phase 2.1 + 2.2 + 2.3."""
    from services.llm.clients import LLMClient

    session_id = f"test-1017-e2e-{uuid4().hex[:12]}"
    user_id = str(uuid4())

    output_filter = OutputFilter()  # No boundary enforcer; PII rules only.

    with patch.object(LLMClient, "_init_clients", lambda self: None):
        client = LLMClient(output_filter=output_filter)
    client._complete_raw = AsyncMock(return_value="Contact alice@example.com for help.")

    result = await client.complete(
        task_type="conversation",
        prompt="hi",
        user_id=user_id,
        session_id=session_id,
    )

    # Filter redacted in place:
    assert "alice@example.com" not in result
    assert "[REDACTED]" in result

    # Audit row landed in the DB:
    repo = EthicsAuditRepository(db_session)
    entries = await repo.find_by_session(session_id, limit=10)
    assert len(entries) == 1
    entry = entries[0]
    assert entry.event_type == "output_filter_decision"
    assert entry.details["surface"] == "conversation"
    assert entry.details["action_taken"] == Action.REDACT_IN_PLACE
    assert "pii:email" in entry.details["matched_rules"]
    # Critical invariant — raw PII NEVER reaches the DB:
    assert "alice@example.com" not in str(entry.details)
