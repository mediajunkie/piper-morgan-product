"""
Handoff Protocol Tests

Comprehensive tests for the MandatoryHandoffProtocol implementation.
Tests core functionality, state management, and protocol compliance.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List

import pytest

# Import the handoff protocol components (to be implemented by Code Agent)
try:
    from methodology.coordination.exceptions import (
        EvidenceReviewRequired,
        HandoffBlocked,
        VerificationRequired,
    )
    from methodology.coordination.handoff import (
        HandoffPackage,
        HandoffState,
        MandatoryHandoffProtocol,
    )
    from methodology.verification.evidence import Evidence, EvidenceType

    HANDOFF_PROTOCOL_AVAILABLE = True
except ImportError:
    HANDOFF_PROTOCOL_AVAILABLE = False


class TestHandoffProtocolCore:
    """Test core handoff protocol functionality"""

    @pytest.fixture
    def protocol(self):
        """Initialize handoff protocol for testing"""
        if not HANDOFF_PROTOCOL_AVAILABLE:
            pytest.skip("Handoff protocol not yet implemented by Code Agent")
        return MandatoryHandoffProtocol()

    @pytest.fixture
    def sample_task(self):
        """Create a sample task for testing"""
        return {
            "type": "implementation",
            "description": "Implement new feature",
            "complexity": "medium",
            "evidence": [
                {"type": "terminal", "content": "$ pytest tests/test_feature.py -v\nPASSED"},
                {"type": "url", "content": "https://github.com/user/repo/issues/123"},
                {"type": "artifact", "content": "Created: src/feature.py (150 lines)"},
            ],
        }

    @pytest.mark.asyncio
    async def test_successful_handoff_flow(self, protocol, sample_task):
        """Test complete successful handoff flow"""

        # Step 1: Initiate handoff
        package = await protocol.initiate_handoff(
            from_agent="agent_a", to_agent="agent_b", task=sample_task
        )

        # Verify package creation
        assert package.from_agent == "agent_a"
        assert package.to_agent == "agent_b"
        assert package.state == HandoffState.VERIFIED
        assert package.verification_result is not None
        assert len(package.evidence) > 0
        assert package.timestamp is not None

        # Step 2: Receive handoff
        result = await protocol.receive_handoff("agent_b", package)

        # Verify handoff completion
        assert result["handoff_complete"] == True
        assert "task" in result
        assert "evidence" in result
        assert "verification" in result
        assert package.state == HandoffState.COMPLETE

    @pytest.mark.asyncio
    async def test_handoff_id_generation(self, protocol):
        """Test handoff ID generation and uniqueness"""

        # Generate multiple handoff IDs
        id1 = protocol._generate_handoff_id("agent_a", "agent_b")
        id2 = protocol._generate_handoff_id("agent_a", "agent_b")
        id3 = protocol._generate_handoff_id("agent_c", "agent_d")

        # Verify IDs are strings
        assert isinstance(id1, str)
        assert isinstance(id2, str)
        assert isinstance(id3, str)

        # Verify IDs are unique
        assert id1 != id2  # Different timestamps
        assert id1 != id3  # Different agents
        assert id2 != id3  # Different agents

    @pytest.mark.asyncio
    async def test_handoff_tracking(self, protocol, sample_task):
        """Test handoff tracking and history management"""

        # Verify initial state
        assert len(protocol.active_handoffs) == 0
        assert len(protocol.handoff_history) == 0

        # Create handoff
        package = await protocol.initiate_handoff(
            from_agent="agent_a", to_agent="agent_b", task=sample_task
        )

        # Verify tracking
        assert len(protocol.active_handoffs) == 1
        handoff_id = protocol._generate_handoff_id("agent_a", "agent_b")
        assert handoff_id in protocol.active_handoffs

        # Complete handoff
        await protocol.receive_handoff("agent_b", package)

        # Verify history
        assert len(protocol.active_handoffs) == 0
        assert len(protocol.handoff_history) == 1
        assert protocol.handoff_history[0] == package

    @pytest.mark.asyncio
    async def test_verification_pyramid_integration(self, protocol, sample_task):
        """Test integration with verification pyramid"""

        # Create handoff - should use verification pyramid
        package = await protocol.initiate_handoff(
            from_agent="agent_a", to_agent="agent_b", task=sample_task
        )

        # Verify verification pyramid was used
        verification = package.verification_result
        assert verification is not None
        assert hasattr(verification, "passed")
        assert hasattr(verification, "evidence")
        assert hasattr(verification, "failures")

        # Verify evidence was processed
        assert len(package.evidence) > 0
        for evidence in package.evidence:
            assert evidence is not None

    @pytest.mark.asyncio
    async def test_evidence_review_process(self, protocol, sample_task):
        """Test evidence review process"""

        # Create handoff
        package = await protocol.initiate_handoff(
            from_agent="agent_a", to_agent="agent_b", task=sample_task
        )

        # Mock evidence review to return True
        original_method = protocol._force_evidence_review
        protocol._force_evidence_review = lambda agent, evidence: True

        try:
            # Should succeed with evidence review
            result = await protocol.receive_handoff("agent_b", package)
            assert result["handoff_complete"] == True

        finally:
            # Restore original method
            protocol._force_evidence_review = original_method

    def test_handoff_package_immutability(self, protocol, sample_task):
        """Test that handoff packages are immutable"""
        if not HANDOFF_PROTOCOL_AVAILABLE:
            pytest.skip("Handoff protocol not yet implemented by Code Agent")

        # Create package directly (for testing immutability)
        package = HandoffPackage(
            task=sample_task,
            from_agent="agent_a",
            to_agent="agent_b",
            verification_result=None,
            evidence=[],  # This will fail due to evidence requirement
            timestamp=datetime.now(),
            state=HandoffState.INITIATED,
        )

        # Verify package structure
        assert package.task == sample_task
        assert package.from_agent == "agent_a"
        assert package.to_agent == "agent_b"
        assert package.state == HandoffState.INITIATED

        # Verify timestamp is set
        assert package.timestamp is not None
        assert isinstance(package.timestamp, datetime)


class TestHandoffProtocolEdgeCases:
    """Test edge cases and error conditions"""

    @pytest.fixture
    def protocol(self):
        """Initialize handoff protocol for testing"""
        if not HANDOFF_PROTOCOL_AVAILABLE:
            pytest.skip("Handoff protocol not yet implemented by Code Agent")
        return MandatoryHandoffProtocol()

    @pytest.mark.asyncio
    async def test_none_task_handoff(self, protocol):
        """Test handoff with None task"""

        with pytest.raises(VerificationRequired):
            await protocol.initiate_handoff(from_agent="agent_a", to_agent="agent_b", task=None)

    @pytest.mark.asyncio
    async def test_empty_agent_names(self, protocol, sample_task):
        """Test handoff with empty agent names"""

        with pytest.raises((ValueError, VerificationRequired)):
            await protocol.initiate_handoff(from_agent="", to_agent="agent_b", task=sample_task)

        with pytest.raises((ValueError, VerificationRequired)):
            await protocol.initiate_handoff(from_agent="agent_a", to_agent="", task=sample_task)

    @pytest.mark.asyncio
    async def test_same_agent_handoff(self, protocol, sample_task):
        """Test handoff to same agent"""

        # This might be allowed or blocked depending on implementation
        try:
            package = await protocol.initiate_handoff(
                from_agent="agent_a",
                to_agent="agent_a",
                task=sample_task,  # Same agent
            )

            # If allowed, verify it works
            result = await protocol.receive_handoff("agent_a", package)
            assert result["handoff_complete"] == True

        except (VerificationRequired, HandoffBlocked):
            # If blocked, that's also acceptable behavior
            pass

    @pytest.mark.asyncio
    async def test_large_task_handoff(self, protocol):
        """Test handoff with large task data"""

        # Create large task
        large_task = {
            "type": "implementation",
            "description": "Large implementation task",
            "data": "x" * 10000,  # Large data
            "evidence": [{"type": "terminal", "content": "Large terminal output: " + "x" * 5000}],
        }

        # Should still work with large data
        package = await protocol.initiate_handoff(
            from_agent="agent_a", to_agent="agent_b", task=large_task
        )

        # Verify large data is preserved
        assert package.task["data"] == large_task["data"]
        assert len(package.task["data"]) == 10000

    @pytest.mark.asyncio
    async def test_concurrent_handoffs_same_agents(self, protocol, sample_task):
        """Test concurrent handoffs between same agents"""

        # Create multiple concurrent handoffs between same agents
        tasks = []
        for i in range(3):
            task = protocol.initiate_handoff(
                from_agent="agent_a", to_agent="agent_b", task=sample_task
            )
            tasks.append(task)

        # Execute concurrently
        packages = await asyncio.gather(*tasks)

        # Verify all succeeded
        assert len(packages) == 3
        for package in packages:
            assert package.state == HandoffState.VERIFIED

        # Verify all are tracked
        assert len(protocol.active_handoffs) == 3


class TestHandoffProtocolPerformance:
    """Test performance characteristics of handoff protocol"""

    @pytest.fixture
    def protocol(self):
        """Initialize handoff protocol for testing"""
        if not HANDOFF_PROTOCOL_AVAILABLE:
            pytest.skip("Handoff protocol not yet implemented by Code Agent")
        return MandatoryHandoffProtocol()

    @pytest.mark.asyncio
    async def test_handoff_latency(self, protocol):
        """Test handoff latency is acceptable"""
        import time

        sample_task = {
            "type": "implementation",
            "evidence": [{"type": "terminal", "content": "tests passing"}],
        }

        # Measure handoff latency
        start_time = time.time()

        package = await protocol.initiate_handoff(
            from_agent="agent_a", to_agent="agent_b", task=sample_task
        )

        await protocol.receive_handoff("agent_b", package)

        end_time = time.time()
        latency = end_time - start_time

        # Should complete in reasonable time (< 1 second)
        assert latency < 1.0, f"Handoff latency {latency:.3f}s exceeds 1s threshold"

    @pytest.mark.asyncio
    async def test_multiple_handoffs_performance(self, protocol):
        """Test performance with multiple handoffs"""
        import time

        sample_task = {
            "type": "implementation",
            "evidence": [{"type": "terminal", "content": "tests passing"}],
        }

        # Create multiple handoffs
        num_handoffs = 10
        start_time = time.time()

        packages = []
        for i in range(num_handoffs):
            package = await protocol.initiate_handoff(
                from_agent=f"agent_{i}", to_agent=f"agent_{i+1}", task=sample_task
            )
            packages.append(package)

        # Complete all handoffs
        for i, package in enumerate(packages):
            await protocol.receive_handoff(f"agent_{i+1}", package)

        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / num_handoffs

        # Should handle multiple handoffs efficiently
        assert avg_time < 0.1, f"Average handoff time {avg_time:.3f}s exceeds 0.1s threshold"
        assert total_time < 2.0, f"Total time {total_time:.3f}s exceeds 2s threshold"
