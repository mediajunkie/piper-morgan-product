"""
Learning Module - Cross-Feature Pattern Learning System

Provides pattern tracking and learning capabilities between different features
of the Piper Morgan system for continuous improvement.
"""

from .context_matcher import ContextMatcher
from .cross_feature_knowledge import (
    ConfidenceLevel,
    CrossFeatureKnowledgeService,
    CrossFeaturePattern,
    KnowledgeSharingType,
    SharedKnowledge,
    get_cross_feature_service,
)
from .query_learning_loop import (
    LearnedPattern,
    PatternConfidence,
    PatternFeedback,
    PatternType,
    QueryLearningLoop,
    get_learning_loop,
    learn_query_pattern,
    learn_response_pattern,
)

__version__ = "1.0.0"
__all__ = [
    # Context Matching
    "ContextMatcher",
    # Query Learning Loop
    "QueryLearningLoop",
    "LearnedPattern",
    "PatternFeedback",
    "PatternType",
    "PatternConfidence",
    "get_learning_loop",
    "learn_query_pattern",
    "learn_response_pattern",
    # Cross-Feature Knowledge Sharing
    "CrossFeatureKnowledgeService",
    "SharedKnowledge",
    "CrossFeaturePattern",
    "KnowledgeSharingType",
    "ConfidenceLevel",
    "get_cross_feature_service",
]
