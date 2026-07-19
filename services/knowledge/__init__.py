"""
Knowledge Services Module
Cross-project pattern recognition and knowledge graph services
"""

from .pattern_recognition_service import PatternRecognitionService, get_pattern_recognition_service

__all__ = [
    "PatternRecognitionService",
    "get_pattern_recognition_service",
]
