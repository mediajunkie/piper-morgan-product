"""Phase 4 (#1124): classifier-prompt verb-canonicalization boundary wiring.

The LLM classifier prompt now asks for a canonical Verb + source_type alongside
the (still-emitted) free-form action. This verifies the boundary wiring in
``_validate_confidence``:

- When the parsed result carries a *mappable* verb, ``intent.action`` is
  canonicalized via the shim (``verb_sourcetype_to_legacy_action``) and
  ``source_type`` is stored in ``intent.context`` (where ``_handle_summarize``
  reads it).
- When the verb is absent / unmappable / invalid, the free-form ``action`` is
  preserved unchanged — the zero-regression fallback that lets the prompt flip
  ship behind the canonical-retest gate without touching the ~40 consumers.

No live LLM — exercises ``_validate_confidence`` with crafted classification
dicts (the shape the resilient parser produces).
"""

import pytest

from services.api.errors import LowConfidenceIntentError
from services.intent_service.llm_classifier import LLMIntentClassifier


def _clf():
    # _validate_confidence only reads confidence_threshold / knowledge_graph
    # (None) / enable_learning (False) — no LLM or KG needed.
    return LLMIntentClassifier(
        knowledge_graph_service=None,
        enable_learning=False,
        confidence_threshold=0.75,
    )


def _result(**over):
    base = {
        "category": "synthesis",
        "action": "free_form_action",
        "confidence": 0.9,
        "reasoning": "r",
    }
    base.update(over)
    return base


class TestVerbCanonicalizationWiring:
    @pytest.mark.asyncio
    async def test_mappable_verb_canonicalizes_action_and_stores_source_type(self):
        # CLOSE is a still-mapped cohort verb: verb -> shim -> legacy `_query` action.
        clf = _clf()
        intent = await clf._validate_confidence(
            _result(category="execution", verb="close", action="close_the_issue"),
            "close issue 42",
        )
        assert intent.action == "close_issue_query"

    @pytest.mark.asyncio
    async def test_summarize_verb_is_unmapped_floors_but_stores_source_type(self):
        """SUMMARIZE-TAXONOMY (#1158): summarize is deliberately NOT shimmed — PPM
        ruled summary output is ALWAYS floor-rendered. So the free-form action is
        preserved (the SYNTHESIS `summarize`/`create_summary` elif is never hit →
        the request floors), while source_type still rides into intent.context for
        observability + the future fetch-augmentation pipeline."""
        clf = _clf()
        intent = await clf._validate_confidence(
            _result(
                category="synthesis",
                verb="summarize",
                source_type="github_issue",
                action="summarize_github_issue",  # the old improvised name, preserved
            ),
            "summarize issue 42",
        )
        # NOT canonicalized to "summarize" → synthesis elif misses → floors.
        assert intent.action == "summarize_github_issue"
        assert intent.action not in ("summarize", "create_summary")
        # source_type still captured for observability / future fetch-augmentation.
        assert intent.context.get("source_type") == "github_issue"

    @pytest.mark.asyncio
    async def test_mutation_verb_maps_to_query_action(self):
        clf = _clf()
        intent = await clf._validate_confidence(
            _result(category="execution", verb="close", action="close_the_issue"),
            "close issue 42",
        )
        assert intent.action == "close_issue_query"

    @pytest.mark.asyncio
    async def test_no_verb_preserves_freeform_action(self):
        clf = _clf()
        intent = await clf._validate_confidence(
            _result(category="analysis", action="analyze_document"),  # no verb key
            "analyze this",
        )
        assert intent.action == "analyze_document"
        assert "source_type" not in intent.context

    @pytest.mark.asyncio
    async def test_valid_but_unmapped_verb_preserves_freeform_action(self):
        clf = _clf()
        # ANALYZE is a real Verb but has no shim entry -> keep the free-form action.
        intent = await clf._validate_confidence(
            _result(category="analysis", verb="analyze", action="analyze_blockers"),
            "what's blocking us",
        )
        assert intent.action == "analyze_blockers"

    @pytest.mark.asyncio
    async def test_invalid_verb_string_does_not_crash(self):
        clf = _clf()
        intent = await clf._validate_confidence(
            _result(category="query", verb="not_a_real_verb", action="search_documents"),
            "find docs",
        )
        assert intent.action == "search_documents"  # graceful fallback, no raise

    @pytest.mark.asyncio
    async def test_null_source_type_string_is_normalized(self):
        clf = _clf()
        intent = await clf._validate_confidence(
            _result(
                category="synthesis",
                verb="summarize",
                source_type="null",  # LLM sometimes emits the string "null"
                action="summarize",
            ),
            "summarize",
        )
        assert intent.context.get("source_type") is None

    @pytest.mark.asyncio
    async def test_low_confidence_still_raises_even_with_verb(self):
        clf = _clf()
        with pytest.raises(LowConfidenceIntentError):
            await clf._validate_confidence(
                _result(verb="summarize", confidence=0.1),
                "summarize",
            )


class TestSourceTypeVocabularyPrompt:
    """SUMMARIZE-TAXONOMY (#1158): the classifier prompt advertises the canonical
    source_type vocabulary (PPM 5-set) + explicit anti-improvisation guidance so the
    LLM emits verb=summarize + source_type instead of inventing summarize_github_issue."""

    def test_prompt_advertises_canonical_source_type_vocabulary(self):
        prompt = _clf()._build_classification_prompt("summarize issue 42", {})
        for src in ("text", "conversation", "github_issue", "commit_range", "document"):
            assert src in prompt, f"source_type '{src}' missing from classifier prompt"

    def test_prompt_steers_summary_to_verb_plus_source_slot(self):
        prompt = _clf()._build_classification_prompt("summarize issue 42", {})
        # Guidance present and names the anti-pattern it replaces.
        assert "summarize_github_issue" in prompt  # called out as the thing NOT to do
        assert "source_type" in prompt
