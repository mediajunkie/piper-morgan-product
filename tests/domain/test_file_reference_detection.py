from datetime import datetime, timezone

import pytest

from services.intent_service.classifier import IntentClassifier
from services.intent_service.pre_classifier import PreClassifier
from services.session.session_manager import SessionManager


class TestFileReferenceDetection:
    """Test file reference detection functionality"""

    @pytest.fixture
    def session_manager(self):
        """Create a fresh session manager for each test"""
        return SessionManager(ttl_minutes=30)

    @pytest.fixture
    def classifier(self):
        """Create a classifier instance"""
        return IntentClassifier()

    def test_file_reference_patterns(self):
        """Test that file reference patterns are correctly detected"""
        patterns = [
            ("analyze the file I uploaded", True),
            ("create a ticket from that document", True),
            ("what's in the csv", True),
            ("summarize the pdf", True),
            ("the spreadsheet shows", True),
            ("my report contains", True),
            ("the data indicates", False),  # System is correct: not a file reference
            ("that upload has", True),
            ("the excel file shows", True),
        ]

        for message, expected in patterns:
            assert (
                PreClassifier.detect_file_reference(message) == expected
            ), f"Failed to detect file reference in: {message}"

    def test_non_file_references(self):
        """Test that non-file references are not detected"""
        # Test messages that should NOT be detected as file references
        non_file_references = [
            "hello there",
            "create a ticket",
            "list all projects",
            "how are you",
            "thanks for the help",
            "goodbye",
            "analyze the data",
            "the project is ready",
        ]

        for message in non_file_references:
            assert not PreClassifier.detect_file_reference(
                message
            ), f"Incorrectly detected file reference in: {message}"

    @pytest.mark.llm  # #1452: drives the LIVE classifier (category/action/confidence asserts)
    @pytest.mark.asyncio
    async def test_classification_with_file_context(self, session_manager, classifier):
        """Test that file context is included in classification"""
        session_id = "test_file_context"
        session = session_manager.get_or_create_session(session_id)

        # Add a file to the session
        session.add_uploaded_file(
            file_id="test_file_123",
            filename="data.csv",
            file_type="text/csv",
            upload_time=datetime.now(timezone.utc),
        )

        # Test classification with file reference
        intent = await classifier.classify(message="analyze the file I uploaded", session=session)

        # Should be classified as analysis intent
        assert intent.category.value == "analysis"
        assert intent.action == "analyze_data"
        assert intent.confidence > 0.7

    @pytest.mark.llm  # #1452: drives the LIVE classifier (category/action/confidence asserts)
    @pytest.mark.asyncio
    async def test_classification_without_file_context(self, session_manager, classifier):
        """Test that classification works without file context"""
        session_id = "test_no_file_context"
        session = session_manager.get_or_create_session(session_id)

        # Test classification without file reference
        intent = await classifier.classify(message="list all projects", session=session)

        # Should be classified as query intent
        assert intent.category.value == "query"
        assert intent.action == "list_projects"
        assert intent.confidence > 0.7

    @pytest.mark.llm  # #1452: drives the LIVE classifier (category/action/confidence asserts)
    @pytest.mark.asyncio
    async def test_file_reference_with_multiple_files(self, session_manager, classifier):
        """Test file reference when multiple files are uploaded"""
        session_id = "test_multiple_files"
        session = session_manager.get_or_create_session(session_id)

        # Add multiple files
        session.add_uploaded_file(
            "file1", "report.pdf", "application/pdf", datetime.now(timezone.utc)
        )
        session.add_uploaded_file("file2", "data.csv", "text/csv", datetime.now(timezone.utc))

        # Test classification with ambiguous file reference
        intent = await classifier.classify(message="analyze the document", session=session)

        # Should still be classified as analysis, but may need clarification
        assert intent.category.value in ["analysis", "conversation"]
        if intent.category.value == "conversation":
            assert intent.action == "clarification_needed"

    def test_file_reference_edge_cases(self):
        """Test edge cases for file reference detection"""
        edge_cases = [
            ("THE FILE", True),  # Case insensitive
            ("that document!", True),  # With punctuation
            ("my file and stuff", True),  # With additional words
            ("file the report", False),  # Verb usage of 'file', not a file reference
            ("the file is ready", True),  # Complete sentence
            ("", False),  # Empty string
            ("   the file   ", True),  # With whitespace
        ]

        for message, expected in edge_cases:
            result = PreClassifier.detect_file_reference(message)
            assert result == expected, f"Expected {expected} for '{message}', got {result}"

    def test_file_the_report_verb_usage(self):
        """Test that verb usage of 'file' is not detected as a file reference"""
        # This was previously a known limitation, now resolved
        assert PreClassifier.detect_file_reference("file the report") is False
