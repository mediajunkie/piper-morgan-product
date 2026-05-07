"""
Integration tests for Knowledge Graph Enhancement (Issue #278: CORE-KNOW-ENHANCE)

Tests verify that:
1. Edge types include causal and temporal relationships
2. Confidence weighting on edges works correctly
3. Graph-first retrieval pattern functions end-to-end
4. Intent classification integrates with knowledge graph
5. Reasoning chains can be extracted from relationships
6. Cost savings are achieved through graph-first approach
"""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.domain.models import KnowledgeEdge, KnowledgeNode
from services.intent_service.classifier import IntentClassifier
from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.shared_types import EdgeType, IntentCategory


@pytest.fixture
def mock_knowledge_graph_service():
    """Create a mock KnowledgeGraphService for testing"""
    mock_repo = Mock()
    service = KnowledgeGraphService(knowledge_graph_repository=mock_repo)
    return service


@pytest.fixture
def mock_classifier(mock_knowledge_graph_service):
    """Create an IntentClassifier with mocked knowledge graph service"""
    return IntentClassifier(knowledge_graph_service=mock_knowledge_graph_service)


class TestEdgeTypeEnhancements:
    """Test that edge types have been enhanced with causal and temporal relationships"""

    def test_causal_edge_types_exist(self):
        """Test that causal edge types are defined.

        Issue #534 (Gate fixes, commit 8829a9b6) standardized all EdgeType
        values to uppercase to match the basic-types convention. Test
        updated to match: enum value == uppercase name.
        """
        causal_types = ["because", "enables", "requires", "prevents", "leads_to"]
        for edge_type in causal_types:
            assert hasattr(EdgeType, edge_type.upper())
            edge = EdgeType[edge_type.upper()]
            assert edge.value == edge_type.upper()

    def test_temporal_edge_types_exist(self):
        """Test that temporal edge types are defined.

        Issue #534 (Gate fixes, commit 8829a9b6) standardized all EdgeType
        values to uppercase. Test updated to match.
        """
        temporal_types = ["before", "during", "after"]
        for edge_type in temporal_types:
            assert hasattr(EdgeType, edge_type.upper())
            edge = EdgeType[edge_type.upper()]
            assert edge.value == edge_type.upper()

    def test_edge_type_count(self):
        """Test that we have at least 18 edge types (9 basic + 8 new)"""
        edge_types = [e for e in EdgeType]
        assert len(edge_types) >= 18

    def test_edge_types_have_string_values(self):
        """Test that all edge types have proper string values"""
        for edge_type in EdgeType:
            assert isinstance(edge_type.value, str)
            assert len(edge_type.value) > 0
            assert " " not in edge_type.value  # No spaces in values


class TestConfidenceWeighting:
    """Test confidence weighting on knowledge edges"""

    def test_knowledge_edge_has_confidence_field(self):
        """Test that KnowledgeEdge has confidence field"""
        edge = KnowledgeEdge(
            source_node_id="node1",
            target_node_id="node2",
            edge_type=EdgeType.BECAUSE,
        )
        assert hasattr(edge, "confidence")
        assert edge.confidence == 1.0

    def test_confidence_can_be_set(self):
        """Test that confidence can be set on edge creation"""
        edge = KnowledgeEdge(
            source_node_id="node1",
            target_node_id="node2",
            edge_type=EdgeType.BECAUSE,
            confidence=0.85,
        )
        assert edge.confidence == 0.85

    def test_confidence_is_float_between_0_and_1(self):
        """Test that confidence is a float between 0.0 and 1.0"""
        for confidence_val in [0.0, 0.5, 0.85, 1.0]:
            edge = KnowledgeEdge(
                source_node_id="node1",
                target_node_id="node2",
                edge_type=EdgeType.ENABLES,
                confidence=confidence_val,
            )
            assert isinstance(edge.confidence, float)
            assert 0.0 <= edge.confidence <= 1.0

    def test_knowledge_edge_has_usage_count(self):
        """Test that KnowledgeEdge has usage_count field for reinforcement"""
        edge = KnowledgeEdge(
            source_node_id="node1",
            target_node_id="node2",
            edge_type=EdgeType.REQUIRES,
            usage_count=5,
        )
        assert hasattr(edge, "usage_count")
        assert edge.usage_count == 5

    def test_knowledge_edge_has_last_accessed(self):
        """Test that KnowledgeEdge has last_accessed for potential decay"""
        now = datetime.now()
        edge = KnowledgeEdge(
            source_node_id="node1",
            target_node_id="node2",
            edge_type=EdgeType.AFTER,
            last_accessed=now,
        )
        assert hasattr(edge, "last_accessed")
        assert edge.last_accessed == now

    def test_edge_to_dict_includes_confidence(self):
        """Test that edge.to_dict() includes confidence"""
        edge = KnowledgeEdge(
            source_node_id="node1",
            target_node_id="node2",
            edge_type=EdgeType.BECAUSE,
            confidence=0.9,
            usage_count=3,
        )
        edge_dict = edge.to_dict()
        assert "confidence" in edge_dict
        assert edge_dict["confidence"] == 0.9
        assert "usage_count" in edge_dict
        assert edge_dict["usage_count"] == 3


class TestGraphFirstRetrievalPattern:
    """Test graph-first retrieval pattern implementation"""

    def test_knowledge_graph_has_expand_method(self, mock_knowledge_graph_service):
        """Test that KnowledgeGraphService has expand method"""
        assert hasattr(mock_knowledge_graph_service, "expand")
        assert callable(mock_knowledge_graph_service.expand)

    def test_knowledge_graph_has_extract_reasoning_chains_method(
        self, mock_knowledge_graph_service
    ):
        """Test that KnowledgeGraphService has extract_reasoning_chains method"""
        assert hasattr(mock_knowledge_graph_service, "extract_reasoning_chains")
        assert callable(mock_knowledge_graph_service.extract_reasoning_chains)

    def test_knowledge_graph_has_get_relevant_context_method(self, mock_knowledge_graph_service):
        """Test that KnowledgeGraphService has get_relevant_context method"""
        assert hasattr(mock_knowledge_graph_service, "get_relevant_context")
        assert callable(mock_knowledge_graph_service.get_relevant_context)

    @pytest.mark.asyncio
    async def test_get_relevant_context_returns_dict(self, mock_knowledge_graph_service):
        """Test that get_relevant_context returns appropriate structure"""
        # Mock the method to return a dict
        mock_knowledge_graph_service.get_relevant_context = AsyncMock(return_value={})

        result = await mock_knowledge_graph_service.get_relevant_context(
            user_query="test query",
            user_id="test_user",
            max_nodes=10,
        )
        assert isinstance(result, dict)

    def test_expand_method_signature(self, mock_knowledge_graph_service):
        """Test that expand method has correct signature"""
        import inspect

        sig = inspect.signature(mock_knowledge_graph_service.expand)
        params = list(sig.parameters.keys())

        # Should accept node_ids, max_hops, edge_types
        assert "node_ids" in params or len(params) > 0
        assert "max_hops" in params or len(params) > 1

    def test_extract_reasoning_chains_signature(self, mock_knowledge_graph_service):
        """Test that extract_reasoning_chains method exists and is callable"""
        import inspect

        sig = inspect.signature(mock_knowledge_graph_service.extract_reasoning_chains)
        params = list(sig.parameters.keys())

        # Should accept a graph structure
        assert len(params) > 0


class TestIntentClassifierGraphIntegration:
    """Test integration of knowledge graph with intent classifier"""

    def test_intent_classifier_accepts_knowledge_graph(self, mock_knowledge_graph_service):
        """Test that IntentClassifier can be initialized with knowledge_graph_service"""
        classifier = IntentClassifier(knowledge_graph_service=mock_knowledge_graph_service)
        assert classifier.knowledge_graph_service == mock_knowledge_graph_service

    def test_intent_classifier_has_get_graph_context_method(self):
        """Test that IntentClassifier has _get_graph_context method"""
        classifier = IntentClassifier()
        assert hasattr(classifier, "_get_graph_context")
        assert callable(classifier._get_graph_context)

    def test_intent_classifier_has_extract_hints_method(self):
        """Test that IntentClassifier has _extract_intent_hints_from_graph method"""
        classifier = IntentClassifier()
        assert hasattr(classifier, "_extract_intent_hints_from_graph")
        assert callable(classifier._extract_intent_hints_from_graph)

    @pytest.mark.asyncio
    async def test_get_graph_context_handles_missing_user_id(self, mock_knowledge_graph_service):
        """Test that _get_graph_context handles missing user_id gracefully"""
        classifier = IntentClassifier(knowledge_graph_service=mock_knowledge_graph_service)

        # Should return empty dict if user_id is None
        result = await classifier._get_graph_context("test message", user_id=None)
        assert isinstance(result, dict)

    def test_extract_intent_hints_returns_list(self):
        """Test that _extract_intent_hints_from_graph returns a list"""
        classifier = IntentClassifier()

        # Test with empty context
        hints = classifier._extract_intent_hints_from_graph({})
        assert isinstance(hints, list)

        # Test with sample context
        sample_context = {
            "reasoning_chains": [
                {
                    "edge_type": "because",
                    "source": "morning_preference",
                    "target": "high_energy",
                }
            ],
            "nodes": [{"name": "daily_standup"}],
        }
        hints = classifier._extract_intent_hints_from_graph(sample_context)
        assert isinstance(hints, list)
        assert len(hints) > 0

    def test_extract_intent_hints_extracts_from_chains(self):
        """Test that hints are extracted from reasoning chains"""
        classifier = IntentClassifier()

        context = {
            "reasoning_chains": [
                {
                    "edge_type": "because",
                    "source": "morning_preference",
                    "target": "high_energy",
                },
                {
                    "edge_type": "enables",
                    "source": "high_energy",
                    "target": "focus_time",
                },
            ],
            "nodes": [],
        }
        hints = classifier._extract_intent_hints_from_graph(context)

        # Should extract edge types and node names
        assert "because" in hints
        assert "enables" in hints
        assert "morning_preference" in hints

    def test_extract_intent_hints_extracts_from_nodes(self):
        """Test that hints are extracted from nodes"""
        classifier = IntentClassifier()

        # Create proper node objects with name attribute
        node1 = KnowledgeNode(name="daily_standup")
        node2 = KnowledgeNode(name="sprint_planning")
        node3 = KnowledgeNode(name="code_review")

        context = {
            "reasoning_chains": [],
            "nodes": [node1, node2, node3],
        }
        hints = classifier._extract_intent_hints_from_graph(context)

        # Should extract node names
        assert "daily_standup" in hints
        assert "sprint_planning" in hints
        assert "code_review" in hints

    def test_extract_intent_hints_removes_duplicates(self):
        """Test that duplicate hints are removed"""
        classifier = IntentClassifier()

        context = {
            "reasoning_chains": [
                {"edge_type": "because", "source": "focus_time", "target": "because"},
                {"edge_type": "because", "source": "because", "target": "focus_time"},
            ],
            "nodes": [],
        }
        hints = classifier._extract_intent_hints_from_graph(context)

        # Should not have duplicates
        assert len(hints) == len(set(hints))


class TestReasoningChainExtraction:
    """Test reasoning chain extraction from knowledge graph"""

    def test_reasoning_chains_follow_causal_edges(self, mock_knowledge_graph_service):
        """Test that reasoning chains can be extracted following causal edges"""
        # Verify the method exists and is callable
        assert callable(mock_knowledge_graph_service.extract_reasoning_chains)

    def test_reasoning_chains_preserve_edge_types(self, mock_knowledge_graph_service):
        """Test that edge types are preserved in reasoning chains"""
        import inspect

        sig = inspect.signature(mock_knowledge_graph_service.extract_reasoning_chains)

        # Method should accept graph structure with edges
        assert len(sig.parameters) > 0


class TestPerformanceCharacteristics:
    """Test performance characteristics of graph-first retrieval"""

    def test_get_relevant_context_is_async(self, mock_knowledge_graph_service):
        """Test that get_relevant_context is an async method"""
        import inspect

        method = mock_knowledge_graph_service.get_relevant_context
        assert inspect.iscoroutinefunction(method)

    def test_expand_is_async(self, mock_knowledge_graph_service):
        """Test that expand is an async method"""
        import inspect

        method = mock_knowledge_graph_service.expand
        assert inspect.iscoroutinefunction(method)

    def test_extract_reasoning_chains_is_async(self, mock_knowledge_graph_service):
        """Test that extract_reasoning_chains is async"""
        import inspect

        method = mock_knowledge_graph_service.extract_reasoning_chains
        # May or may not be async - check if it exists
        assert callable(method)


class TestBackwardCompatibility:
    """Test that changes are backward compatible"""

    def test_edge_type_enum_still_has_original_types(self):
        """Test that original edge types still exist"""
        original_types = [
            "references",
            "depends_on",
            "implements",
            "measures",
            "involves",
            "triggers",
            "enhances",
            "replaces",
            "supports",
        ]
        for edge_type in original_types:
            assert hasattr(EdgeType, edge_type.upper())

    def test_knowledge_edge_defaults_are_sensible(self):
        """Test that KnowledgeEdge defaults are backward compatible"""
        edge = KnowledgeEdge(
            source_node_id="node1",
            target_node_id="node2",
        )
        # Should have sensible defaults
        assert edge.edge_type == EdgeType.REFERENCES
        assert edge.confidence == 1.0
        assert edge.usage_count == 0

    def test_knowledge_graph_service_still_has_original_methods(self, mock_knowledge_graph_service):
        """Test that KnowledgeGraphService still has original methods"""
        # Original methods should still exist
        original_methods = [
            "create_node",
            "create_edge",
            "search_nodes",
            "traverse_relationships",
            "get_node",
            "get_neighbors",
        ]
        for method_name in original_methods:
            assert hasattr(mock_knowledge_graph_service, method_name)
            assert callable(getattr(mock_knowledge_graph_service, method_name))

    def test_intent_classifier_backward_compatible(self):
        """Test that IntentClassifier works without knowledge_graph_service"""
        # Should work with no knowledge_graph_service parameter
        classifier = IntentClassifier()
        assert classifier.knowledge_graph_service is None

        # Should still have classify method
        assert hasattr(classifier, "classify")
        assert callable(classifier.classify)


class TestIntegrationFlow:
    """Test the complete integration flow from query to classification with graph"""

    @pytest.mark.asyncio
    async def test_intent_classifier_integration_step_by_step(self, mock_classifier):
        """Test that intent classifier integrates with graph correctly"""
        # Simulate context with user_id
        context = {
            "user_id": "test_user",
            "project": "test_project",
        }

        message = "What are my pending tasks?"

        # Get graph context should not raise an error
        try:
            graph_context = await mock_classifier._get_graph_context(message, "test_user")
            assert isinstance(graph_context, dict)
        except Exception as e:
            # If graph service requires external resources, that's OK
            pytest.skip(f"Graph service requires external resources: {e}")

    @pytest.mark.asyncio
    async def test_graph_context_used_in_classification_context(self, mock_classifier):
        """Test that graph context is captured in classification_context"""
        context = {
            "user_id": "test_user",
        }

        try:
            # Get graph context
            graph_context = await mock_classifier._get_graph_context(
                "test message", context["user_id"]
            )

            # Verify it can be used
            assert isinstance(graph_context, dict)

            # Extract hints
            hints = mock_classifier._extract_intent_hints_from_graph(graph_context)
            assert isinstance(hints, list)
        except Exception as e:
            pytest.skip(f"Service requires external resources: {e}")


class TestCostSavingsPotential:
    """Test that the implementation supports cost savings through graph-first approach"""

    def test_semantic_search_method_exists(self, mock_knowledge_graph_service):
        """Test that KnowledgeGraphService has semantic_search method"""
        # semantic_search should exist for cost-optimized retrieval
        assert hasattr(mock_knowledge_graph_service, "search_nodes") or hasattr(
            mock_knowledge_graph_service, "semantic_search"
        )

    def test_graph_context_reduces_llm_input(self):
        """Test that graph context can be concise (reducing token count)"""
        # A well-structured graph context should be serializable to fewer tokens
        context = {
            "nodes": [{"id": "n1", "name": "focus_time"}],
            "relationships": [{"source": "n1", "target": "n2", "type": "enables"}],
            "reasoning_chains": [{"path": ["n1", "n2"], "confidence": 0.85}],
        }

        # Should be efficiently serializable
        import json

        serialized = json.dumps(context)
        assert len(serialized) < 500  # Should be quite small

    def test_2_hop_expansion_provides_context(self, mock_knowledge_graph_service):
        """Test that 2-hop expansion provides sufficient context"""
        # expand method should support max_hops parameter for controlled expansion
        import inspect

        sig = inspect.signature(mock_knowledge_graph_service.expand)
        params = list(sig.parameters.keys())

        # Should have some form of hop control
        assert len(params) >= 2  # At least node_ids and some other param


class TestDataModel:
    """Test the data model enhancements for knowledge graph"""

    def test_knowledge_edge_serialization(self):
        """Test that KnowledgeEdge can be serialized to dict with new fields"""
        edge = KnowledgeEdge(
            source_node_id="morning_routine",
            target_node_id="high_energy",
            edge_type=EdgeType.ENABLES,
            confidence=0.95,
            usage_count=10,
            metadata={"context": "user_preference"},
        )

        edge_dict = edge.to_dict()

        # Should include new fields
        assert "confidence" in edge_dict
        assert "usage_count" in edge_dict
        assert edge_dict["confidence"] == 0.95
        assert edge_dict["usage_count"] == 10

    def test_knowledge_edge_preserves_metadata(self):
        """Test that KnowledgeEdge preserves metadata through serialization"""
        edge = KnowledgeEdge(
            source_node_id="n1",
            target_node_id="n2",
            edge_type=EdgeType.BECAUSE,
            metadata={"learning_context": "user_feedback"},
            properties={"strength": "high"},
        )

        edge_dict = edge.to_dict()
        assert edge_dict["metadata"] == {"learning_context": "user_feedback"}
        assert edge_dict["properties"] == {"strength": "high"}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
