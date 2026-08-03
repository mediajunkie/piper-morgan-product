"""#1124 Phase 4 re-land (#1432, 2026-08-02): verb-canonicalization on the LIVE classifier.

Port of the deleted reference tests (fba6452f0) to the live seam: the prompt flip
now lives in classifier.py::_classify_with_reasoning, which parses verb+source_type
from the LLM JSON and canonicalizes intent.action via verb_sourcetype_to_legacy_action,
keeping the free-form action as the zero-regression fallback.

No live LLM — self.llm.complete and the personalization resolver are patched;
crafted JSON exercises the parse boundary exactly as the resilient path sees it.
"""

import json
from unittest.mock import AsyncMock, patch

import pytest

from services.intent_service.classifier import IntentClassifier


def _clf():
    return IntentClassifier()


def _llm_json(**over):
    base = {
        "category": "synthesis",
        "action": "free_form_action",
        "confidence": 0.9,
        "reasoning": "r",
    }
    base.update(over)
    return json.dumps(base)


async def _classify(clf, llm_response, message="summarize issue 42"):
    with patch.object(clf, "_llm", create=True), \
         patch(
             "services.configuration.personalization_service.personalization_service"
             ".resolve_system_prompt_standalone",
             new=AsyncMock(return_value="sys"),
         ):
        clf._llm = AsyncMock()
        clf._llm.complete = AsyncMock(return_value=llm_response)
        intent, reasoning = await clf._classify_with_reasoning(message)
    return intent


class TestVerbCanonicalizationLive:
    @pytest.mark.asyncio
    async def test_mappable_verb_canonicalizes_action_and_stores_source_type(self):
        # Table-driven: pick a verb that maps TODAY (the reference test hardcoded
        # summarize, whose row was later deliberately removed — summaries floor
        # per #1158; a hardcoded verb makes the test assert a stale table).
        from services.intent_service.action_registry import (
            Verb,
            verb_sourcetype_to_legacy_action,
        )
        mapped = [(v, verb_sourcetype_to_legacy_action(v, None)) for v in Verb
                  if verb_sourcetype_to_legacy_action(v, None)]
        assert mapped, "precondition: shim table must map at least one verb"
        verb, expected = mapped[0]
        intent = await _classify(
            _clf(),
            _llm_json(verb=verb.value, source_type="github_issue",
                      action="improvised_free_form_name"),
        )
        assert intent.action == expected
        assert intent.context["source_type"] == "github_issue"
        # #1332/#1459 discipline: BOTH surfaces populated
        assert intent.original_message == "summarize issue 42"
        assert intent.context["original_message"] == "summarize issue 42"

    @pytest.mark.asyncio
    async def test_no_verb_keeps_free_form_action(self):
        intent = await _classify(_clf(), _llm_json())
        assert intent.action == "free_form_action"
        assert "source_type" not in intent.context

    @pytest.mark.asyncio
    async def test_invalid_verb_keeps_free_form_action(self):
        intent = await _classify(_clf(), _llm_json(verb="not_a_verb"))
        assert intent.action == "free_form_action"

    @pytest.mark.asyncio
    async def test_null_and_na_source_types_normalize_to_absent(self):
        for st in ("null", "None", "N/A", "  "):
            intent = await _classify(_clf(), _llm_json(verb="summarize", source_type=st))
            assert "source_type" not in intent.context, f"source_type {st!r} leaked"

    @pytest.mark.asyncio
    async def test_unmappable_verb_combo_keeps_free_form(self):
        # A verb that parses but has no shim row at all would fall through;
        # simulate via a mappable verb whose shim result is None only if absent —
        # guard: if every Verb maps, this test asserts the fallback shape instead.
        from services.intent_service.action_registry import (
            Verb,
            verb_sourcetype_to_legacy_action,
        )
        unmapped = [v for v in Verb if verb_sourcetype_to_legacy_action(v, None) is None]
        if not unmapped:
            pytest.skip("every Verb currently maps; fallback covered by invalid-verb test")
        intent = await _classify(_clf(), _llm_json(verb=unmapped[0].value))
        assert intent.action == "free_form_action"
