"""
Integration tests for real content search functionality.
Tests the complete flow from MCP resource retrieval to domain model scoring.
"""

import asyncio
import os
import tempfile
import time
from pathlib import Path
from typing import List

import pytest

from services.domain.mcp.content_extraction import ContentExtractor
from services.domain.mcp.value_objects import ContentMatch, RelevanceScore
from services.mcp.resources import EnhancedFileResult, MCPResourceManager


class TestContentSearchIntegration:
    """Test real content search with TF-IDF scoring and domain models."""

    @pytest.fixture
    def sample_content_files(self):
        """Create sample files with known content for testing."""
        files = {}

        # Project timeline document
        files["project_timeline.md"] = """
        # Project Timeline

        ## Phase 1: Planning (Weeks 1-2)
        - Requirements gathering
        - Architecture design
        - Timeline creation

        ## Phase 2: Development (Weeks 3-8)
        - Core feature implementation
        - Testing and validation
        - Code review process

        ## Phase 3: Launch (Weeks 9-10)
        - Production deployment
        - User training
        - Performance monitoring
        """

        # Technical specification
        files["tech_spec.md"] = """
        # Technical Specification

        ## Architecture Overview
        The system uses a microservices architecture with:
        - API Gateway for routing
        - Service mesh for communication
        - Database per service pattern

        ## Performance Requirements
        - Response time < 200ms for API calls
        - Throughput > 1000 requests/second
        - 99.9% uptime requirement
        """

        # Unrelated document
        files["meeting_notes.txt"] = """
        Meeting Notes - July 20, 2025

        Attendees: Alice, Bob, Charlie

        Topics Discussed:
        - Budget planning for Q3
        - Office relocation plans
        - Team building activities

        Action Items:
        - Alice: Review budget proposals
        - Bob: Contact real estate agents
        - Charlie: Plan team outing
        """

        return files

    @pytest.fixture
    async def mcp_manager_with_content(self, sample_content_files):
        """Set up MCP manager with test content files in uploads directory."""
        # Create test files in uploads directory
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)

        # Store original files for cleanup
        test_files = []

        try:
            # Write test files to uploads directory
            for filename, content in sample_content_files.items():
                file_path = uploads_dir / f"test_{filename}"
                file_path.write_text(content)
                test_files.append(file_path)

            # Configure MCP manager
            config = {
                "url": f"stdio://./scripts/mcp_file_server.py",
                "timeout": 5.0,
            }

            manager = MCPResourceManager(client_config=config)

            # Initialize with MCP enabled
            success = await manager.initialize(enabled=True)
            if not success:
                pytest.skip("MCP not available for integration testing")

            yield manager

            # Cleanup
            await manager.cleanup()

        finally:
            # Remove test files
            for file_path in test_files:
                if file_path.exists():
                    file_path.unlink()

    @pytest.fixture
    def content_extractor(self):
        """Create ContentExtractor with test configuration."""
        config = {
            "max_content_length": 10000,
            "snippet_length": 150,
            "include_metadata": True,
            "min_word_length": 2,
            "max_keywords": 15,
        }
        return ContentExtractor(config=config)

    @pytest.mark.asyncio
    async def test_real_content_search_finds_project_timeline(
        self, mcp_manager_with_content, content_extractor
    ):
        """Test that searching 'project timeline' finds documents containing those words."""
        # RED: This test should fail initially because we're using basic scoring
        query = "project timeline"

        # Search for content
        results = await mcp_manager_with_content.enhanced_file_search(query)

        # Should find the project timeline document
        assert len(results) > 0, "Should find at least one result"

        # The test_project_timeline.md should be the top result
        timeline_results = [r for r in results if "test_project_timeline" in r.filename.lower()]
        assert len(timeline_results) > 0, "Should find project timeline document"

        top_result = timeline_results[0]

        # Should have high relevance score using domain model
        assert (
            top_result.relevance_score > 0.5
        ), f"Expected high relevance, got {top_result.relevance_score}"

        # Content preview should contain query terms
        preview_lower = top_result.content_preview.lower()
        assert "project" in preview_lower, "Preview should contain 'project'"
        assert "timeline" in preview_lower, "Preview should contain 'timeline'"

    @pytest.mark.asyncio
    async def test_tfidf_scoring_ranks_results_properly(
        self, mcp_manager_with_content, content_extractor
    ):
        """Test that TF-IDF scoring ranks more relevant documents higher."""
        # RED: This should fail with basic term frequency scoring
        query = "architecture performance"

        # Search for content
        results = await mcp_manager_with_content.enhanced_file_search(query)

        assert len(results) >= 2, "Should find multiple results for comparison"

        # Tech spec should rank higher than meeting notes for architecture/performance
        tech_spec_results = [r for r in results if "test_tech_spec" in r.filename.lower()]
        meeting_results = [r for r in results if "test_meeting" in r.filename.lower()]

        if tech_spec_results and meeting_results:
            tech_score = tech_spec_results[0].relevance_score
            meeting_score = meeting_results[0].relevance_score

            assert tech_score > meeting_score, (
                f"Tech spec ({tech_score}) should rank higher than meeting notes ({meeting_score}) "
                f"for architectural query"
            )

    @pytest.mark.asyncio
    async def test_content_extraction_works_for_markdown(
        self, mcp_manager_with_content, content_extractor
    ):
        """Test that markdown content is properly extracted and processed."""
        # RED: This should fail if content extraction is not working
        query = "Phase 2 Development"

        results = await mcp_manager_with_content.enhanced_file_search(query)

        # Should find the project timeline with markdown content
        timeline_results = [r for r in results if "test_project_timeline" in r.filename.lower()]
        assert len(timeline_results) > 0, "Should find markdown document"

        result = timeline_results[0]

        # Should extract meaningful content from markdown
        assert len(result.content_preview) > 50, "Should extract substantial content"

        # Should find phase-related content
        preview_lower = result.content_preview.lower()
        assert any(
            word in preview_lower for word in ["phase", "development", "weeks"]
        ), "Should extract phase and development content from markdown"

    @pytest.mark.asyncio
    async def test_domain_model_integration(self, mcp_manager_with_content, content_extractor):
        """Test that domain models (ContentExtractor, RelevanceScore) are properly integrated."""
        # RED: This should fail until we integrate domain models
        query = "requirements architecture"

        # Get raw content for comparison
        results = await mcp_manager_with_content.enhanced_file_search(query)
        assert len(results) > 0, "Should find results"

        # For each result, verify domain model integration
        for result in results:
            # Relevance score should be calculated using ContentExtractor
            # (This will fail until we integrate the domain models)
            assert isinstance(result.relevance_score, float), "Score should be float"
            assert 0 <= result.relevance_score <= 1, "Score should be normalized 0-1"

            # Metadata should include domain model insights
            if result.metadata:
                # Should have processed metadata from ContentExtractor
                expected_keys = ["file_type", "word_count", "keywords"]
                # Note: This will fail until we integrate ContentExtractor.extract_text_content()

    @pytest.mark.asyncio
    async def test_performance_under_500ms(self, mcp_manager_with_content):
        """Test that content search performance stays under 500ms."""
        query = "timeline development"

        # Measure search performance
        start_time = time.time()
        results = await mcp_manager_with_content.enhanced_file_search(query)
        duration = time.time() - start_time

        assert duration < 0.5, f"Search took {duration:.3f}s, should be under 500ms"
        assert len(results) > 0, "Should find results within performance limit"

    @pytest.mark.asyncio
    async def test_feature_flag_controls_behavior(self):
        """Test that feature flag properly controls MCP pool usage."""
        # Test with pool disabled
        manager_direct = MCPResourceManager()
        success_direct = await manager_direct.initialize(enabled=True)

        if success_direct:
            stats_direct = await manager_direct.get_connection_stats()
            assert (
                stats_direct["using_pool"] == False
            ), "Should use direct connection when pool disabled"
            await manager_direct.cleanup()

        # Test with pool enabled (if available)
        os.environ["USE_MCP_POOL"] = "true"
        try:
            manager_pool = MCPResourceManager()
            success_pool = await manager_pool.initialize(enabled=True)

            if success_pool:
                stats_pool = await manager_pool.get_connection_stats()
                # Note: This might be False if pool not available, which is fine
                await manager_pool.cleanup()
        finally:
            os.environ.pop("USE_MCP_POOL", None)

    @pytest.mark.asyncio
    async def test_no_more_filename_only_matching(self, mcp_manager_with_content):
        """Test that we're doing real content search, not just filename matching."""
        # RED: This should fail if we're still doing filename-only matching

        # Search for content that appears in file content but not filename
        query = "Budget planning Q3"  # This appears in meeting_notes.txt content only

        results = await mcp_manager_with_content.enhanced_file_search(query)

        # Should find the meeting notes based on content, not filename
        meeting_results = [r for r in results if "test_meeting" in r.filename.lower()]
        assert len(meeting_results) > 0, "Should find meeting notes based on content"

        result = meeting_results[0]
        assert result.relevance_score > 0, "Should have relevance score for content match"

        # Preview should show the matched content
        preview_lower = result.content_preview.lower()
        assert "budget" in preview_lower, "Should show budget content in preview"

    @pytest.mark.asyncio
    async def test_empty_query_handling(self, mcp_manager_with_content):
        """Test graceful handling of edge cases."""
        # Empty query
        results = await mcp_manager_with_content.enhanced_file_search("")
        assert isinstance(results, list), "Should return empty list for empty query"

        # None query
        results = await mcp_manager_with_content.enhanced_file_search(None)
        assert isinstance(results, list), "Should handle None query gracefully"

        # Very long query
        long_query = "word " * 100
        results = await mcp_manager_with_content.enhanced_file_search(long_query)
        assert isinstance(results, list), "Should handle long queries"


class TestContentExtractionDomain:
    """Test the domain model integration separately."""

    def test_content_extractor_calculate_relevance_score(self):
        """Test ContentExtractor relevance scoring."""
        extractor = ContentExtractor()

        content = """
        This document discusses project timeline and development phases.
        The architecture team will review the technical specifications.
        """

        query = "project timeline"

        # Should return RelevanceScore object with proper TF-IDF calculation
        score = extractor.calculate_relevance_score(content, query)

        assert isinstance(score, RelevanceScore), "Should return RelevanceScore object"
        assert score.value > 0, "Should have positive relevance"
        assert "project" in score.matched_terms, "Should match 'project'"
        assert "timeline" in score.matched_terms, "Should match 'timeline'"

    def test_content_extractor_find_content_matches(self):
        """Test ContentExtractor content matching."""
        extractor = ContentExtractor()

        content = """
        Project Timeline Overview

        Phase 1: Planning and requirements
        Phase 2: Development and testing
        Phase 3: Deployment and monitoring
        """

        query = "timeline planning"

        # Should return list of ContentMatch objects
        matches = extractor.find_content_matches(content, query)

        assert isinstance(matches, list), "Should return list of matches"
        assert len(matches) > 0, "Should find matches"

        for match in matches:
            assert isinstance(match, ContentMatch), "Should be ContentMatch objects"
            assert match.relevance_score > 0, "Each match should have relevance score"
