"""
PM-087 Phase 3 Integration Tests
Comprehensive testing of advanced ethics features and user transparency
"""

import asyncio
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from services.api.transparency import transparency_router
from services.domain.models import BoundaryViolation, EthicalDecision
from services.ethics.adaptive_boundaries import AdaptiveBoundaries, PatternMetadata
from services.ethics.audit_transparency import AuditLogEntry, AuditTransparency, SecurityRedactor
from services.ethics.boundary_enforcer import BoundaryDecision, BoundaryEnforcer, BoundaryType
from services.infrastructure.monitoring.ethics_metrics import ethics_metrics


class TestAdaptiveBoundaries:
    """Test adaptive boundaries system"""

    @pytest.fixture
    def adaptive_boundaries(self):
        """Provide AdaptiveBoundaries instance for tests"""
        return AdaptiveBoundaries()

    @pytest.mark.asyncio
    async def test_learn_from_decision(self, adaptive_boundaries):
        """Test learning from ethics decision"""
        # Create test decision
        decision = EthicalDecision(
            decision_id="test_decision_123",
            boundary_type="harassment",
            violation_detected=True,
            explanation="Test harassment violation",
            audit_data={"content_length": 100, "response_time_ms": 50},
            session_id="test_session",
        )

        # Learn from decision
        await adaptive_boundaries.learn_from_decision(decision)

        # Verify learning occurred
        assert adaptive_boundaries.learning_operations_total > 0
        assert len(adaptive_boundaries.learned_patterns) > 0

        # Check that pattern was learned
        pattern_found = False
        for pattern_hash, metadata in adaptive_boundaries.learned_patterns.items():
            if metadata.boundary_type == "harassment":
                pattern_found = True
                break

        assert pattern_found

    @pytest.mark.asyncio
    async def test_learn_from_violation(self, adaptive_boundaries):
        """Test learning from boundary violation"""
        # Create test violation
        violation = BoundaryViolation(
            violation_id="test_violation_123",
            violation_type="harassment",
            context="Test harassment content",
            session_id="test_session",
            severity="high",
        )

        # Learn from violation
        await adaptive_boundaries.learn_from_violation(violation)

        # Verify learning occurred
        assert adaptive_boundaries.learning_operations_total > 0

        # Check that pattern was learned
        pattern_found = False
        for pattern_hash, metadata in adaptive_boundaries.learned_patterns.items():
            if metadata.boundary_type == "harassment":
                pattern_found = True
                break

        assert pattern_found

    @pytest.mark.asyncio
    async def test_get_adaptive_patterns(self, adaptive_boundaries):
        """Test getting adaptive patterns"""
        # Learn some patterns first
        decision = EthicalDecision(
            decision_id="test_decision_456",
            boundary_type="professional",
            violation_detected=True,
            explanation="Test professional violation",
            audit_data={"content_length": 200},
            session_id="test_session",
        )

        await adaptive_boundaries.learn_from_decision(decision)

        # Get patterns for professional boundary
        patterns = await adaptive_boundaries.get_adaptive_patterns("professional")

        # Should have patterns if confidence threshold is met
        assert isinstance(patterns, list)

    @pytest.mark.asyncio
    async def test_update_confidence_scores(self, adaptive_boundaries):
        """Test confidence score updates"""
        # Create and learn a pattern
        decision = EthicalDecision(
            decision_id="test_decision_789",
            boundary_type="inappropriate",
            violation_detected=True,
            explanation="Test inappropriate content",
            audit_data={"content_length": 150},
            session_id="test_session",
        )

        await adaptive_boundaries.learn_from_decision(decision)

        # Update confidence scores
        await adaptive_boundaries.update_confidence_scores()

        # Check that confidence scores were updated
        for metadata in adaptive_boundaries.learned_patterns.values():
            assert 0 <= metadata.confidence_score <= 1

    @pytest.mark.asyncio
    async def test_cleanup_old_patterns(self, adaptive_boundaries):
        """Test cleanup of old patterns"""
        # Create old pattern
        old_pattern = PatternMetadata(
            pattern_hash="old_pattern_123",
            frequency=1,
            first_seen=datetime.now(timezone.utc) - timedelta(days=40),
            last_seen=datetime.now(timezone.utc) - timedelta(days=35),
        )
        old_pattern.boundary_type = "test"

        adaptive_boundaries.learned_patterns["old_pattern_123"] = old_pattern

        # Perform cleanup
        await adaptive_boundaries.cleanup_old_patterns()

        # Check that old pattern was removed
        assert "old_pattern_123" not in adaptive_boundaries.learned_patterns

    def test_get_learning_stats(self, adaptive_boundaries):
        """Test learning statistics"""
        stats = adaptive_boundaries.get_learning_stats()

        # Verify stats structure
        assert "total_patterns" in stats
        assert "learning_operations" in stats
        assert "learning_errors" in stats
        assert "patterns_by_type" in stats
        assert "high_confidence_patterns" in stats
        assert "active_patterns" in stats


class TestAuditTransparency:
    """Test audit transparency system"""

    @pytest.fixture
    def audit_transparency(self):
        """Provide AuditTransparency instance for tests"""
        return AuditTransparency()

    @pytest.fixture
    def security_redactor(self):
        """Provide SecurityRedactor instance for tests"""
        return SecurityRedactor()

    @pytest.mark.asyncio
    async def test_log_ethics_decision(self, audit_transparency):
        """Test logging ethics decision.

        Updated for #1018 Phase 2 (2026-05-02): `audit_logs` in-memory list
        is gone. Test now mocks the repository to capture what would be
        persisted and asserts on that.
        """
        captured = []

        class _CapturingRepo:
            def __init__(self, session):
                pass

            async def add(self, entry):
                captured.append(entry)

        decision = EthicalDecision(
            decision_id="test_decision_123",
            boundary_type="harassment",
            violation_detected=True,
            explanation="Test harassment violation",
            audit_data={"content_length": 100, "response_time_ms": 50},
            session_id="test_session",
        )

        with patch(
            "services.database.repositories.EthicsAuditRepository", _CapturingRepo
        ):
            with patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope"
            ) as mock_scope:
                mock_session = Mock()
                mock_session.commit = AsyncMock()

                class _Ctx:
                    async def __aenter__(self):
                        return mock_session

                    async def __aexit__(self, *args):
                        return False

                mock_scope.return_value = _Ctx()
                await audit_transparency.log_ethics_decision(decision)

        # Verify entry was passed to the repository
        assert len(captured) == 1
        entry = captured[0]
        assert entry.event_type == "ethics_decision"
        assert entry.session_id == "test_session"
        assert entry.details["boundary_type"] == "harassment"
        assert entry.details["violation_detected"] is True

    @pytest.mark.asyncio
    async def test_log_boundary_violation(self, audit_transparency):
        """Test logging boundary violation.

        Updated for #1018 Phase 2 (2026-05-02): same shape as
        test_log_ethics_decision — mock the repository, capture entry.
        """
        captured = []

        class _CapturingRepo:
            def __init__(self, session):
                pass

            async def add(self, entry):
                captured.append(entry)

        violation = BoundaryViolation(
            violation_id="test_violation_123",
            violation_type="harassment",
            context="Test harassment content with email@example.com",
            session_id="test_session",
            severity="high",
        )

        with patch(
            "services.database.repositories.EthicsAuditRepository", _CapturingRepo
        ):
            with patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope"
            ) as mock_scope:
                mock_session = Mock()
                mock_session.commit = AsyncMock()

                class _Ctx:
                    async def __aenter__(self):
                        return mock_session

                    async def __aexit__(self, *args):
                        return False

                mock_scope.return_value = _Ctx()
                await audit_transparency.log_boundary_violation(violation)

        assert len(captured) == 1
        entry = captured[0]
        assert entry.event_type == "boundary_violation"
        assert entry.session_id == "test_session"
        assert entry.details["violation_type"] == "harassment"
        assert entry.details["severity"] == "high"

    @pytest.mark.asyncio
    async def test_get_user_audit_log(self, audit_transparency):
        """Test getting user audit log.

        Updated for #1018 Phase 2 (2026-05-02): pre-fix, this test wrote
        to an in-memory list and read back from the same list. Post-fix,
        write/read both go through the repository — so we mock the repo
        to return canned entries on read.
        """
        from datetime import datetime, timezone
        from services.ethics.audit_transparency import AuditLogEntry

        canned_entry = AuditLogEntry(
            entry_id="audit_test_1",
            event_type="ethics_decision",
            timestamp=datetime.now(timezone.utc),
            session_id="test_session",
            details={"boundary_type": "harassment", "violation_detected": True},
            redacted=True,
        )

        with patch(
            "services.database.repositories.EthicsAuditRepository"
        ) as MockRepo:
            mock_repo_instance = MockRepo.return_value
            mock_repo_instance.find_by_session = AsyncMock(return_value=[canned_entry])

            with patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope"
            ) as mock_scope:
                class _Ctx:
                    async def __aenter__(self):
                        return Mock()

                    async def __aexit__(self, *args):
                        return False

                mock_scope.return_value = _Ctx()
                audit_log = await audit_transparency.get_user_audit_log(
                    "test_session", limit=10
                )

        assert len(audit_log) == 1
        assert audit_log[0]["session_id"] == "test_session"
        assert audit_log[0]["event_type"] == "ethics_decision"

    @pytest.mark.asyncio
    async def test_get_system_audit_summary(self, audit_transparency):
        """Test getting system audit summary.

        #1006 fix (#1018 Phase 2, 2026-05-02): the original failure was
        "can't compare offset-naive and offset-aware datetimes" inside the
        in-memory list comparison path. That code is gone — `get_system_
        audit_summary` now queries `EthicsAuditRepository.summarize_recent`
        which uses TIMESTAMPTZ throughout (no naive-vs-aware mixing).
        Repository-layer datetime handling is covered separately in
        `tests/unit/services/test_ethics_audit_repository_1018.py`.

        This test mocks the repository so it doesn't need a live DB —
        verifies the response shape and that summarize_recent is called.
        """
        from datetime import datetime, timezone

        with patch(
            "services.database.repositories.EthicsAuditRepository"
        ) as MockRepo:
            mock_repo_instance = MockRepo.return_value
            mock_repo_instance.summarize_recent = AsyncMock(
                return_value={
                    "period_days": 30,
                    "total_entries": 1,
                    "events_by_type": {"ethics_decision": 1},
                    "boundary_breakdown": {"harassment": 1},
                }
            )
            with patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope"
            ) as mock_scope:
                class _Ctx:
                    async def __aenter__(self):
                        return Mock()

                    async def __aexit__(self, *args):
                        return False

                mock_scope.return_value = _Ctx()

                summary = await audit_transparency.get_system_audit_summary(days=30)

        assert "total_entries" in summary
        assert "unique_sessions" in summary
        assert "event_type_breakdown" in summary
        assert summary["total_entries"] == 1
        assert summary["event_type_breakdown"] == {"ethics_decision": 1}

    def test_security_redaction(self, security_redactor):
        """Test security redaction"""
        # Test email redaction
        text_with_email = "Contact me at user@example.com for details"
        redacted_text = security_redactor.redact_sensitive_data(text_with_email)

        assert "[REDACTED]" in redacted_text
        assert "user@example.com" not in redacted_text

        # Test phone number redaction
        text_with_phone = "Call me at 555-123-4567"
        redacted_text = security_redactor.redact_sensitive_data(text_with_phone)

        assert "[REDACTED]" in redacted_text
        assert "555-123-4567" not in redacted_text

    def test_content_preview_redaction(self, security_redactor):
        """Test content preview redaction"""
        content = "This is test content with email@example.com and phone 555-123-4567"

        preview = security_redactor.redact_content_preview(content, max_length=50)

        assert "[REDACTED]" in preview
        assert len(preview) <= 50
        assert "email@example.com" not in preview
        assert "555-123-4567" not in preview

    @pytest.mark.asyncio
    async def test_get_transparency_stats(self, audit_transparency):
        """Test transparency statistics.

        Updated for #1018 Phase 2 (2026-05-02): get_transparency_stats is
        now async (queries DB for total + 24h count). Mock the repo so
        no DB connection is required. `max_log_entries` removed from the
        response (no longer applicable — DB has retention not size cap).
        """
        with patch(
            "services.database.repositories.EthicsAuditRepository"
        ) as MockRepo:
            mock_repo_instance = MockRepo.return_value
            mock_repo_instance.count = AsyncMock(return_value=100)

            with patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope"
            ) as mock_scope:
                mock_session = Mock()
                mock_session.execute = AsyncMock()
                mock_result = Mock()
                mock_result.scalar_one = Mock(return_value=10)
                mock_session.execute.return_value = mock_result

                class _Ctx:
                    async def __aenter__(self):
                        return mock_session

                    async def __aexit__(self, *args):
                        return False

                mock_scope.return_value = _Ctx()
                stats = await audit_transparency.get_transparency_stats()

        assert "total_audit_entries" in stats
        assert "transparency_requests" in stats
        assert "audit_log_entries_total" in stats
        assert "redaction_operations" in stats
        assert "log_retention_days" in stats
        assert "recent_entries_24h" in stats


class TestTransparencyAPI:
    """Test transparency API endpoints"""

    @pytest.fixture
    def app(self):
        """Provide FastAPI app for testing"""
        app = FastAPI()
        app.include_router(transparency_router)
        return app

    @pytest.fixture
    def client(self, app):
        """Provide test client"""
        return TestClient(app)

    def test_get_user_audit_log_endpoint(self, client):
        """Test user audit log endpoint.

        #1008 fix (2026-05-02): switched the mock from `Mock.return_value`
        to `AsyncMock` so the mocked `get_user_audit_log` returns an
        awaitable. Pre-fix, awaiting a `Mock(return_value=[...])` produced
        TypeError "object list can't be used in 'await' expression". The
        production code was correct; the test mock was wrong.
        """
        with patch("services.api.transparency.audit_transparency") as mock_transparency:
            mock_transparency.get_user_audit_log = AsyncMock(
                return_value=[
                    {
                        "entry_id": "test_entry_123",
                        "event_type": "ethics_decision",
                        "timestamp": "2025-08-03T10:00:00Z",
                        "session_id": "test_session",
                        "details": {"boundary_type": "harassment"},
                    }
                ]
            )

            # Make request
            response = client.get("/transparency/audit-log/test_session?limit=10")

            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert data["total_entries"] == 1
            assert data["session_id"] == "test_session"
            assert len(data["entries"]) == 1

    def test_get_user_audit_summary_endpoint(self, client):
        """Test user audit summary endpoint.

        #1018 Phase 2 fix (2026-05-02): switched mock to AsyncMock so the
        production `await audit_transparency.get_user_audit_log(...)` call
        gets an awaitable.
        """
        with patch("services.api.transparency.audit_transparency") as mock_transparency:
            mock_transparency.get_user_audit_log = AsyncMock(
                return_value=[
                    {
                        "entry_id": "test_entry_123",
                        "event_type": "ethics_decision",
                        "timestamp": "2025-08-03T10:00:00Z",
                        "session_id": "test_session",
                        "details": {"boundary_type": "harassment"},
                    }
                ]
            )

            # Make request
            response = client.get("/transparency/audit-summary/test_session")

            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert "summary" in data
            assert data["summary"]["total_entries"] == 1

    def test_get_transparency_stats_endpoint(self, client):
        """Test transparency stats endpoint"""
        # Mock audit transparency
        with patch("services.api.transparency.audit_transparency") as mock_transparency:
            mock_transparency.get_transparency_stats = AsyncMock(
                return_value={
                    "total_audit_entries": 100,
                    "transparency_requests": 50,
                    "redaction_operations": 200,
                }
            )

            # Make request
            response = client.get("/transparency/stats")

            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert "stats" in data
            assert data["stats"]["total_audit_entries"] == 100

    def test_transparency_health_check_endpoint(self, client):
        """Test transparency health check endpoint"""
        # Mock audit transparency
        with patch("services.api.transparency.audit_transparency") as mock_transparency:
            mock_transparency.get_transparency_stats = AsyncMock(
                return_value={
                    "total_audit_entries": 100,
                    "transparency_requests": 50,
                    "redaction_operations": 200,
                }
            )

            # Make request
            response = client.get("/transparency/health")

            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "transparency_system" in data


class TestPhase3Integration:
    """Integration tests for Phase 3 components"""

    @pytest.mark.asyncio
    async def test_boundary_enforcer_with_adaptive_learning(self):
        """Test BoundaryEnforcer integration with adaptive learning"""
        # Create boundary enforcer
        enforcer = BoundaryEnforcer()

        # Create mock request
        request = Mock(spec=Request)
        request.body = AsyncMock(return_value=b"This is harassment content")
        request.headers = {"X-Session-ID": "test_session"}
        request.url.path = "/api/test"
        request.method = "POST"

        # Perform boundary enforcement
        decision = await enforcer.enforce_boundaries(request)

        # Verify decision
        assert isinstance(decision, BoundaryDecision)
        assert decision.violation_detected is True
        assert decision.boundary_type == BoundaryType.HARASSMENT

        # Verify adaptive learning occurred
        adaptive_stats = enforcer.adaptive_boundaries.get_learning_stats()
        assert adaptive_stats["learning_operations"] > 0

    @pytest.mark.asyncio
    async def test_boundary_enforcer_with_audit_transparency(self):
        """Test BoundaryEnforcer integration with audit transparency"""
        # Create boundary enforcer
        enforcer = BoundaryEnforcer()

        # Create mock request
        request = Mock(spec=Request)
        request.body = AsyncMock(return_value=b"Normal content")
        request.headers = {"X-Session-ID": "test_session"}
        request.url.path = "/api/test"
        request.method = "POST"

        # Perform boundary enforcement
        decision = await enforcer.enforce_boundaries(request)

        # Verify audit transparency occurred
        transparency_stats = enforcer.audit_transparency.get_transparency_stats()
        assert transparency_stats["audit_log_entries_total"] > 0

    @pytest.mark.asyncio
    async def test_end_to_end_phase3_workflow(self):
        """Test complete Phase 3 workflow"""
        # Create components
        enforcer = BoundaryEnforcer()
        adaptive = AdaptiveBoundaries()
        transparency = AuditTransparency()

        # Create test decision
        decision = EthicalDecision(
            decision_id="test_decision_123",
            boundary_type="harassment",
            violation_detected=True,
            explanation="Test violation",
            audit_data={"content_length": 100},
            session_id="test_session",
        )

        # Test adaptive learning
        await adaptive.learn_from_decision(decision)
        assert adaptive.learning_operations_total > 0

        # Test audit transparency
        await transparency.log_ethics_decision(decision)
        assert transparency.audit_log_entries_total > 0

        # Test user audit log access
        audit_log = await transparency.get_user_audit_log("test_session")
        assert len(audit_log) > 0

        # Test security redaction
        redactor = SecurityRedactor()
        redacted_content = redactor.redact_sensitive_data("Contact me at user@example.com")
        assert "[REDACTED]" in redacted_content

        # Verify all components working together
        assert adaptive.get_learning_stats()["total_patterns"] > 0
        assert transparency.get_transparency_stats()["total_audit_entries"] > 0
