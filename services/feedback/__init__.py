"""
Feedback Service
The feedback a person sends from the app: ``models`` and ``feedback_service``.
"""

# The Issue-623 grammar-conscious triplet (narrative_bridge / narrative_helpers /
# response_context) was disposed 2026-08-30 in the Batch-2 census-dead-family
# disposal — loaded-only, zero call sites. Retrievable by commit hash via the
# disposal record in decisions.log. The pattern's in-tree exemplar lives on in
# services/onboarding/narrative_bridge.py.

# ``capture.FeedbackCapture`` (a Redis-backed correction capture that was never
# constructed) was deleted 2026-11-12, #2347, on Arch's ruling; see decisions.log.

__all__: list = []
