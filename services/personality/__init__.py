"""
Personality Enhancement Module

Provides personality enhancement for responses across all interfaces.
Built on DDD principles with ResponsePersonalityEnhancer as aggregate root.

Core Components:
- ResponsePersonalityEnhancer: Aggregate root for response enhancement
- PersonalityProfile: User personality preferences entity
- TransformationService: Content transformation domain service

Grammar Components (Issue #627):
- PersonalityGrammarContext: Rich context for grammar-conscious responses
- PersonalityGrammarBridge: Transform context into phrases
- Grammar helpers: apply_personality, get_greeting, etc.

Performance: <100ms enhancement constraint with circuit breaker protection
"""

from .grammar_bridge import PersonalityGrammarBridge

# Issue #627: Grammar-conscious response components
from .grammar_context import GrammarLens, PersonalityGrammarContext, SituationType
from .grammar_helpers import (
    apply_personality,
    get_closing,
    get_confidence_phrase,
    get_error_phrase,
    get_formality,
    get_greeting,
    get_situation_tone,
    is_warm_user,
)
from .personality_profile import EnhancedResponse, PersonalityProfile, ResponseContext
from .response_enhancer import ResponsePersonalityEnhancer
from .transformations import TransformationService

__all__ = [
    # Core personality
    "ResponsePersonalityEnhancer",
    "PersonalityProfile",
    "ResponseContext",
    "EnhancedResponse",
    "TransformationService",
    # Grammar context
    "PersonalityGrammarContext",
    "SituationType",
    "GrammarLens",
    "PersonalityGrammarBridge",
    # Grammar helpers
    "apply_personality",
    "get_greeting",
    "get_error_phrase",
    "get_closing",
    "get_confidence_phrase",
    "get_situation_tone",
    "get_formality",
    "is_warm_user",
]
