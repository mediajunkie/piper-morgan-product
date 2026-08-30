"""
Feedback Service
Captures and processes user corrections for learning
"""

from .capture import FeedbackCapture

# The Issue-623 grammar-conscious triplet (narrative_bridge / narrative_helpers /
# response_context) was disposed 2026-08-30 in the Batch-2 census-dead-family
# disposal — loaded-only, zero call sites. Retrievable by commit hash via the
# disposal record in decisions.log. The pattern's in-tree exemplar lives on in
# services/onboarding/narrative_bridge.py.

# Note: We'll create the global instance in main.py after Redis is initialized
# since FeedbackCapture requires a Redis connection

__all__ = [
    # Capture
    "FeedbackCapture",
]
