"""
PM-034 Phase 2: Anaphoric Reference Resolution Tests
Tests for 90% accuracy requirement and target capabilities
"""

from datetime import datetime, timedelta
from typing import List

import pytest

from services.conversation.reference_resolver import (
    ConversationMemoryService,
    ReferenceCandidate,
    ReferenceResolver,
    ResolvedReference,
)
from services.domain.models import ConversationTurn


class TestReferenceResolver:
    """Test suite for reference resolution accuracy"""

    @pytest.fixture
    def resolver(self):
        return ReferenceResolver(context_window_turns=10)

    @pytest.fixture
    def sample_conversation_history(self):
        """Create realistic conversation history for testing"""
        base_time = datetime.now() - timedelta(hours=1)

        turns = [
            # Turn 1: User creates GitHub issue
            ConversationTurn(
                id="turn_1",
                conversation_id="conv_123",
                turn_number=1,
                user_message="Create GitHub issue for login bug",
                assistant_response="I've created GitHub issue #85 for the login bug. The issue has been assigned to the development team.",
                entities=["#85"],
                created_at=base_time + timedelta(minutes=5),
            ),
            # Turn 2: User asks about project
            ConversationTurn(
                id="turn_2",
                conversation_id="conv_123",
                turn_number=2,
                user_message="What's the status of the main project?",
                assistant_response='The main project "Piper Morgan Platform" is currently in active development with 15 open issues.',
                entities=["Piper Morgan Platform"],
                created_at=base_time + timedelta(minutes=10),
            ),
            # Turn 3: User uploads document
            ConversationTurn(
                id="turn_3",
                conversation_id="conv_123",
                turn_number=3,
                user_message="I've uploaded the requirements document",
                assistant_response='I\'ve processed the uploaded file "requirements_v2.pdf" and extracted key requirements.',
                entities=["requirements_v2.pdf"],
                created_at=base_time + timedelta(minutes=15),
            ),
        ]

        return turns

    def test_pronoun_reference_resolution(self, resolver, sample_conversation_history):
        """Test basic pronoun resolution: 'it', 'that', 'this'"""
        test_cases = [
            ("Show me that issue again", "Show me GitHub issue #85 again"),
            ("Update it with more details", "Update GitHub issue #85 with more details"),
            ("Close this now", "Close GitHub issue #85 now"),
        ]

        correct_resolutions = 0

        for user_input, expected_output in test_cases:
            resolved_message, resolved_refs = resolver.resolve_references(
                user_input, sample_conversation_history
            )

            if "GitHub issue #85" in resolved_message:
                correct_resolutions += 1

        accuracy = correct_resolutions / len(test_cases)
        assert accuracy >= 0.9, f"Pronoun resolution accuracy {accuracy:.2%} below 90% threshold"

    def test_definite_reference_resolution(self, resolver, sample_conversation_history):
        """Test definite reference resolution: 'the issue', 'the project'"""
        test_cases = [
            # #1234: the resolver's entity_type for issues is "github_issue" (the established
            # convention — see test_target_capability_demonstration, which asserts it). The old
            # "issue" expectation was stale; the resolver correctly resolves all three.
            ("What's the status of the issue?", "github_issue"),
            ("Update the project timeline", "project"),
            ("Send me the document", "file"),
        ]

        correct_resolutions = 0

        for user_input, expected_type in test_cases:
            resolved_message, resolved_refs = resolver.resolve_references(
                user_input, sample_conversation_history
            )

            if resolved_refs and any(ref.entity_type == expected_type for ref in resolved_refs):
                correct_resolutions += 1

        accuracy = correct_resolutions / len(test_cases)
        assert accuracy >= 0.9, f"Definite reference accuracy {accuracy:.2%} below 90% threshold"

    def test_target_capability_demonstration(self, resolver, sample_conversation_history):
        """Test the exact target capability from mission brief"""

        # Simulate: User: "Create GitHub issue for login bug" -> Piper: [Creates issue #85]
        # Then: User: "Show me that issue again" -> Should resolve to specific GitHub issue #85

        user_follow_up = "Show me that issue again"
        resolved_message, resolved_refs = resolver.resolve_references(
            user_follow_up, sample_conversation_history
        )

        # Verify specific requirements
        assert (
            "GitHub issue #85" in resolved_message
        ), "Failed to resolve 'that issue' to specific GitHub issue #85"
        assert len(resolved_refs) == 1, "Should resolve exactly one reference"
        assert resolved_refs[0].resolved_entity == "#85", "Should resolve to issue #85"
        assert resolved_refs[0].entity_type == "github_issue", "Should identify as GitHub issue"
        assert resolved_refs[0].confidence >= 0.7, "Should have high confidence in resolution"

    def test_performance_under_150ms(self, resolver, sample_conversation_history):
        """Test <150ms additional latency requirement"""
        start_time = datetime.now()

        # Test multiple reference resolutions
        test_messages = [
            "Show me that issue again",
            "Update it with more details",
            "What's the status of the project?",
            "Send me the document",
            "Close this now",
        ]

        for message in test_messages:
            resolver.resolve_references(message, sample_conversation_history)

        total_time = (datetime.now() - start_time).total_seconds() * 1000
        avg_time_per_resolution = total_time / len(test_messages)

        assert (
            avg_time_per_resolution < 150
        ), f"Average resolution time {avg_time_per_resolution:.1f}ms exceeds 150ms target"

    def test_context_window_limitation(self, resolver):
        """Test that context window is properly limited to 10 turns"""
        # Create 15 conversation turns
        extended_history = []
        base_time = datetime.now() - timedelta(hours=2)

        for i in range(15):
            turn = ConversationTurn(
                id=f"turn_{i}",
                conversation_id="conv_extended",
                turn_number=i + 1,
                user_message=f"Message {i}",
                assistant_response=f"Created issue #{100 + i}",
                created_at=base_time + timedelta(minutes=i * 5),
            )
            extended_history.append(turn)

        # Test that only last 10 turns are considered
        candidates = resolver._find_candidates("that", "pronoun", extended_history)

        # Should only have candidates from turns 6-15 (last 10)
        turn_numbers = [c.source_turn.turn_number for c in candidates]
        assert max(turn_numbers) == 15, "Should include most recent turn"
        assert min(turn_numbers) >= 6, "Should not include turns older than context window"

    def test_confidence_scoring(self, resolver, sample_conversation_history):
        """Test confidence scoring algorithm"""
        candidates = resolver._find_candidates("that", "pronoun", sample_conversation_history)

        if candidates:
            best_candidate = resolver._score_candidates(candidates)

            assert best_candidate.confidence_score <= 1.0, "Confidence should not exceed 1.0"
            assert best_candidate.confidence_score >= 0.0, "Confidence should not be negative"

            # Most recent issue should have highest confidence
            assert (
                best_candidate.entity == "#85"
            ), "Most recent entity should have highest confidence"

    def test_entity_extraction_patterns(self, resolver):
        """Test entity extraction from assistant responses"""
        test_responses = [
            ("I created GitHub issue #123 for you", [("#123", "github_issue")]),
            ('Working on project "Test Project"', [("Test Project", "project")]),
            ("Uploaded requirements.pdf successfully", [("requirements.pdf", "file")]),
            (
                'Created issue #456 and updated file "data.csv"',
                [("#456", "github_issue"), ("data.csv", "file")],
            ),
        ]

        correct_extractions = 0
        total_extractions = sum(len(expected) for _, expected in test_responses)

        for response_text, expected_entities in test_responses:
            extracted = resolver._extract_entities(response_text)

            for expected_entity, expected_type in expected_entities:
                if (expected_entity, expected_type) in extracted:
                    correct_extractions += 1

        accuracy = correct_extractions / total_extractions
        assert accuracy >= 0.9, f"Entity extraction accuracy {accuracy:.2%} below 90% threshold"

    def test_multiple_references_in_single_message(self, resolver, sample_conversation_history):
        """Test handling multiple references in one message"""
        user_message = "Show me that issue and update the project status"

        resolved_message, resolved_refs = resolver.resolve_references(
            user_message, sample_conversation_history
        )

        assert len(resolved_refs) >= 2, "Should resolve multiple references in single message"

        # Check that both references were resolved appropriately
        entity_types = [ref.entity_type for ref in resolved_refs]
        assert "github_issue" in entity_types, "Should resolve issue reference"
        assert "project" in entity_types, "Should resolve project reference"


class TestConversationMemoryService:
    """Test conversation memory service integration"""

    @pytest.fixture
    def memory_service(self):
        return ConversationMemoryService()

    @pytest.mark.asyncio
    async def test_high_level_resolution_service(self, memory_service):
        """Test high-level service integration"""
        user_message = "Show me that issue again"
        conversation_id = "conv_123"

        resolved_message, resolved_refs, metadata = await memory_service.resolve_user_message(
            user_message, conversation_id
        )

        # Verify service response structure
        assert isinstance(resolved_message, str)
        assert isinstance(resolved_refs, list)
        assert isinstance(metadata, dict)

        # Verify metadata structure
        required_keys = [
            "original_message",
            "resolution_count",
            "confidence_scores",
            "context_window_size",
        ]
        for key in required_keys:
            assert key in metadata, f"Metadata missing required key: {key}"


class TestAccuracyBenchmark:
    """Comprehensive accuracy benchmark testing"""

    @pytest.fixture
    def accuracy_test_suite(self):
        """Comprehensive test cases for 90% accuracy verification"""
        base_time = datetime.now() - timedelta(hours=1)

        # Create conversation with diverse entities
        conversation_turns = [
            ConversationTurn(
                id="t1",
                conversation_id="test_conv",
                turn_number=1,
                user_message="Create issue for authentication bug",
                assistant_response="Created GitHub issue #101 for authentication bug",
                created_at=base_time + timedelta(minutes=1),
            ),
            ConversationTurn(
                id="t2",
                conversation_id="test_conv",
                turn_number=2,
                user_message="Start project planning",
                assistant_response='Initiated planning for project "Auth Redesign"',
                created_at=base_time + timedelta(minutes=5),
            ),
            ConversationTurn(
                id="t3",
                conversation_id="test_conv",
                turn_number=3,
                user_message="Upload design document",
                assistant_response='Processed uploaded file "auth_design.pdf"',
                created_at=base_time + timedelta(minutes=10),
            ),
        ]

        # Comprehensive test cases covering all reference types
        test_cases = [
            # Pronoun references
            ("Show me it", "github_issue", "#101"),
            ("Update that", "github_issue", "#101"),
            ("Close this", "github_issue", "#101"),
            # Definite references
            ("Status of the issue", "github_issue", "#101"),
            ("Update the project", "project", "Auth Redesign"),
            ("Review the document", "file", "auth_design.pdf"),
            # Implicit references
            ("Show it again", "github_issue", "#101"),
            ("Check that status", "github_issue", "#101"),
            # Complex references
            ("What's the latest on the issue?", "github_issue", "#101"),
            ("Send me that file again", "file", "auth_design.pdf"),
        ]

        return conversation_turns, test_cases

    def test_comprehensive_accuracy_benchmark(self, accuracy_test_suite):
        """Comprehensive 90% accuracy test across all reference types"""
        conversation_turns, test_cases = accuracy_test_suite
        resolver = ReferenceResolver(context_window_turns=10)

        correct_resolutions = 0
        total_tests = len(test_cases)

        results = []

        for user_input, expected_entity_type, expected_entity in test_cases:
            resolved_message, resolved_refs = resolver.resolve_references(
                user_input, conversation_turns
            )

            # Check if resolution was correct
            is_correct = False
            if resolved_refs:
                for ref in resolved_refs:
                    if (
                        ref.entity_type == expected_entity_type
                        and expected_entity in ref.resolved_entity
                    ):
                        is_correct = True
                        break

            if is_correct:
                correct_resolutions += 1

            results.append(
                {
                    "input": user_input,
                    "expected": f"{expected_entity_type}:{expected_entity}",
                    "resolved": [f"{r.entity_type}:{r.resolved_entity}" for r in resolved_refs],
                    "correct": is_correct,
                }
            )

        accuracy = correct_resolutions / total_tests

        # Print detailed results for debugging
        print(f"\nReference Resolution Accuracy Test Results:")
        print(f"Correct: {correct_resolutions}/{total_tests} ({accuracy:.1%})")

        for result in results:
            status = "✅" if result["correct"] else "❌"
            print(
                f"{status} '{result['input']}' -> Expected: {result['expected']}, Got: {result['resolved']}"
            )

        assert (
            accuracy >= 0.9
        ), f"Overall accuracy {accuracy:.1%} below 90% requirement. See detailed results above."

    def test_performance_benchmark_with_accuracy(self, accuracy_test_suite):
        """Combined performance and accuracy benchmark"""
        conversation_turns, test_cases = accuracy_test_suite
        resolver = ReferenceResolver(context_window_turns=10)

        start_time = datetime.now()

        total_correct = 0
        for user_input, expected_entity_type, expected_entity in test_cases:
            resolved_message, resolved_refs = resolver.resolve_references(
                user_input, conversation_turns
            )

            # Verify accuracy
            if resolved_refs and any(
                ref.entity_type == expected_entity_type and expected_entity in ref.resolved_entity
                for ref in resolved_refs
            ):
                total_correct += 1

        total_time = (datetime.now() - start_time).total_seconds() * 1000
        avg_time = total_time / len(test_cases)
        accuracy = total_correct / len(test_cases)

        print(f"\nPerformance & Accuracy Benchmark:")
        print(f"Average resolution time: {avg_time:.1f}ms (target: <150ms)")
        print(f"Accuracy: {accuracy:.1%} (target: ≥90%)")

        assert avg_time < 150, f"Average time {avg_time:.1f}ms exceeds 150ms target"
        assert accuracy >= 0.9, f"Accuracy {accuracy:.1%} below 90% requirement"
