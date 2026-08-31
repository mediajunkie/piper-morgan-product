"""
Learning Module

Database-backed, per-user learning (Issue #300) lives in
``services.learning.learning_handler`` (imported directly, not re-exported
here). ``ContextMatcher`` provides context-similarity scoring for it.

1613: the former cross-feature pooled pattern system (QueryLearningLoop,
CrossFeatureKnowledgeService — patterns keyed by source_feature, NOT by user)
was removed per PM ruling 2026-08-31. It implemented exactly the cross-user
data pooling our published privacy claims disclaim, and was superseded by the
user-scoped #300 system.
"""

from .context_matcher import ContextMatcher

__version__ = "1.0.0"
__all__ = [
    "ContextMatcher",
]
