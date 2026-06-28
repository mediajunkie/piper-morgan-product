"""Tests for log_output_filter_decision (Issue #1017 Phase 2.3).

Verifies the durable audit envelope for OutputFilter decisions:
- Writes an AuditLogEntry with event_type="output_filter_decision"
- Hash-only invariant preserved (raw content never serialized)
- Oversized audit_metadata strings truncated + flagged
- Write failures swallowed (audit must not propagate)
- User-ID string identifiers handled (not just UUIDs)
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.ethics.audit_transparency import AuditTransparency
from services.ethics.output_filter import (
    Action,
    OutputFilterDecision,
    Profile,
    Severity,
)


def _build_decision(**overrides) -> OutputFilterDecision:
    """Test fixture: a sensible OutputFilterDecision."""
    defaults = dict(
        decision_id="test-decision-1",
        timestamp=datetime.now(timezone.utc),
        user_id="user-1",
        session_id="sess-1",
        surface="conversation",
        profile_applied=Profile.USER_VISIBLE,
        matched_rules=["pii:email"],
        severity=Severity.MEDIUM,
        redactions_count=1,
        action_taken=Action.REDACT_IN_PLACE,
        original_content_hash="a" * 64,
        filtered_content_hash="b" * 64,
        attempt_number=1,
        prior_attempt_decision_id=None,
    )
    defaults.update(overrides)
    return OutputFilterDecision(**defaults)


class TestLogOutputFilterDecision:
    @pytest.mark.asyncio
    async def test_writes_entry_with_correct_event_type(self):
        at = AuditTransparency()
        decision = _build_decision()

        captured_entry = {}

        class _FakeRepo:
            def __init__(self, session):
                pass

            async def add(self, entry):
                captured_entry["entry"] = entry

        class _FakeSession:
            async def commit(self):
                pass

        class _FakeFactory:
            @staticmethod
            def session_scope():
                class _Ctx:
                    async def __aenter__(self_inner):
                        return _FakeSession()

                    async def __aexit__(self_inner, *args):
                        return None

                return _Ctx()

        with (
            patch("services.database.repositories.EthicsAuditRepository", _FakeRepo),
            patch("services.database.session_factory.AsyncSessionFactory", _FakeFactory),
        ):
            await at.log_output_filter_decision(decision)

        entry = captured_entry.get("entry")
        assert entry is not None
        assert entry.event_type == "output_filter_decision"
        assert entry.session_id == "sess-1"
        assert entry.details["decision_id"] == "test-decision-1"
        assert entry.details["action_taken"] == Action.REDACT_IN_PLACE
        assert entry.details["severity"] == Severity.MEDIUM

    @pytest.mark.asyncio
    async def test_hash_only_invariant_no_raw_content_in_entry(self):
        """The entry's details must contain hashes only — never raw content."""
        at = AuditTransparency()
        decision = _build_decision(
            original_content_hash="hash-of-PII-bearing-content",
            filtered_content_hash="hash-of-redacted-content",
        )

        captured = {}

        class _FakeRepo:
            def __init__(self, session):
                pass

            async def add(self, entry):
                captured["entry"] = entry

        class _FakeSession:
            async def commit(self):
                pass

        class _FakeFactory:
            @staticmethod
            def session_scope():
                class _Ctx:
                    async def __aenter__(self_inner):
                        return _FakeSession()

                    async def __aexit__(self_inner, *args):
                        return None

                return _Ctx()

        with (
            patch("services.database.repositories.EthicsAuditRepository", _FakeRepo),
            patch("services.database.session_factory.AsyncSessionFactory", _FakeFactory),
        ):
            await at.log_output_filter_decision(decision)

        entry = captured["entry"]
        # Hashes present:
        assert entry.details["original_content_hash"] == "hash-of-PII-bearing-content"
        assert entry.details["filtered_content_hash"] == "hash-of-redacted-content"
        # Raw-content fields absent:
        assert "filtered_content" not in entry.details
        assert "raw_content" not in entry.details
        assert "original_content" not in entry.details

    @pytest.mark.asyncio
    async def test_oversized_audit_metadata_string_truncated(self):
        """audit_metadata strings >256 chars get truncated + flagged.

        Belt-and-braces invariant guard: if a future caller mutates
        audit_metadata with raw content, the audit-log layer catches it.
        """
        at = AuditTransparency()
        raw_leak = "Email leak: alice@example.com " * 50  # >256 chars
        decision = _build_decision()
        decision.audit_metadata["leaked_raw_content"] = raw_leak

        captured = {}

        class _FakeRepo:
            def __init__(self, session):
                pass

            async def add(self, entry):
                captured["entry"] = entry

        class _FakeSession:
            async def commit(self):
                pass

        class _FakeFactory:
            @staticmethod
            def session_scope():
                class _Ctx:
                    async def __aenter__(self_inner):
                        return _FakeSession()

                    async def __aexit__(self_inner, *args):
                        return None

                return _Ctx()

        with (
            patch("services.database.repositories.EthicsAuditRepository", _FakeRepo),
            patch("services.database.session_factory.AsyncSessionFactory", _FakeFactory),
        ):
            await at.log_output_filter_decision(decision)

        details = captured["entry"].details
        stored = details["audit_metadata"]["leaked_raw_content"]
        assert len(stored) < len(raw_leak)
        assert "[TRUNCATED]" in stored
        assert "invariant_violations" in details

    @pytest.mark.asyncio
    async def test_write_failure_swallowed(self):
        """Audit-write failures must not propagate (LLM call must not break)."""
        at = AuditTransparency()
        decision = _build_decision()

        class _FailingRepo:
            def __init__(self, session):
                pass

            async def add(self, entry):
                raise RuntimeError("DB unavailable")

        class _FakeSession:
            async def commit(self):
                pass

        class _FakeFactory:
            @staticmethod
            def session_scope():
                class _Ctx:
                    async def __aenter__(self_inner):
                        return _FakeSession()

                    async def __aexit__(self_inner, *args):
                        return None

                return _Ctx()

        with (
            patch("services.database.repositories.EthicsAuditRepository", _FailingRepo),
            patch("services.database.session_factory.AsyncSessionFactory", _FakeFactory),
        ):
            # No exception should escape:
            await at.log_output_filter_decision(decision)

    @pytest.mark.asyncio
    async def test_string_user_id_does_not_break(self):
        """user_id may be a string identifier (not a UUID); audit should pass."""
        at = AuditTransparency()
        decision = _build_decision(user_id="not-a-uuid-just-a-string")

        captured = {}

        class _FakeRepo:
            def __init__(self, session):
                pass

            async def add(self, entry):
                captured["entry"] = entry

        class _FakeSession:
            async def commit(self):
                pass

        class _FakeFactory:
            @staticmethod
            def session_scope():
                class _Ctx:
                    async def __aenter__(self_inner):
                        return _FakeSession()

                    async def __aexit__(self_inner, *args):
                        return None

                return _Ctx()

        with (
            patch("services.database.repositories.EthicsAuditRepository", _FakeRepo),
            patch("services.database.session_factory.AsyncSessionFactory", _FakeFactory),
        ):
            await at.log_output_filter_decision(decision)

        entry = captured["entry"]
        assert entry.user_id is None  # String non-UUID → None at the entry layer
        assert entry.details["user_id"] == "not-a-uuid-just-a-string"  # preserved in details
