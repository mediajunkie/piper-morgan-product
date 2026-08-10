"""#1571 half 1 — the floor must never teach magic phrases.

Incident (PM live, 2026-08-10): the LLM floor shaped a great issue draft, then
taught PM to "just say 'file it in [owner/repo]' and I'll create it". That
phrase is not a canonical ask shape — it misclassified into the files family,
whose canned unwired-decline replied "I can't do that from chat yet": a FALSE
denial (create_issue is wired; PM had used it minutes earlier). The floor
invented an utterance the router doesn't speak, then the router punished the
user for trusting it.

The fix: a rule in the capability-manifest block (the region that already
carries the #1517 never-deny-wired instruction, riding EVERY non-denial floor
turn): when the floor recommends HOW to execute something, it must phrase the
ask as a plain request matching the manifest's wired capabilities — never an
invented magic phrase, trigger word, or special syntax.

LAYER HONESTY (m-43): these are PROMPT-CONTENT tests. They verify the exact
text the floor assembles into its system prompt — NOT live LLM behavior (a
model can still disobey its prompt; that's a live behavioral test, out of
scope here).
"""

import asyncio
import re

from services.intent_service.conversational_floor import (
    ConversationalFloor,
    FloorContext,
    capability_manifest_block,
)
from services.intent_service.workflow_dispatcher import wired_chat_actions


def _norm(text: str) -> str:
    """Collapse line-wrapping so phrase assertions span newlines+indent."""
    return re.sub(r"\s+", " ", text).lower()


class TestCanonicalPhrasingRule:
    """The no-magic-phrases rule in the rendered manifest block.

    Layer: prompt content (verifies prompt text, not live LLM behavior).
    """

    def test_manifest_forbids_inventing_magic_phrases(self):
        block = _norm(capability_manifest_block())
        assert "never invent" in block, (
            "manifest must carry the #1571 no-magic-phrases rule"
        )
        assert "magic phrase" in block, (
            "manifest must name the failure mode: an invented magic phrase"
        )

    def test_manifest_names_the_incident_shape(self):
        # The concrete anti-example keeps the rule grounded: "file it" is the
        # phrase the floor actually taught in the #1571 incident.
        block = _norm(capability_manifest_block())
        assert "file it" in block, (
            "manifest must carry the concrete #1571 anti-example ('file it')"
        )

    def test_manifest_requires_plain_language_recommendations(self):
        # The positive half: recommended asks must be plain one-line requests
        # that match wired capabilities — not special syntax.
        block = _norm(capability_manifest_block())
        assert "plain" in block
        assert "special" in block  # "special command syntax" / "special syntax"

    def test_static_prose_stays_capability_name_free(self):
        # The #1517 invariant must survive the #1571 addition: the derived
        # list remains the sole carrier of capability names.
        static_prose = capability_manifest_block.__wrapped_static__
        for token in wired_chat_actions():
            assert token not in static_prose, (
                f"hand-written capability name '{token}' in static manifest prose"
            )


class TestRuleRidesTheAssembledPrompt:
    """The rule reaches the actual system prompt on a normal floor turn.

    Layer: prompt assembly (verifies _get_system_prompt output, not live
    LLM behavior).
    """

    def _prompt_for(self, **ctx_kwargs) -> str:
        floor = ConversationalFloor(system_prompt_base="BASE-IDENTITY")
        ctx = FloorContext(
            user_message="draft an issue for the login timeout bug",
            session_id="s-1571",
            **ctx_kwargs,
        )
        return asyncio.run(floor._get_system_prompt(ctx))

    def test_rule_present_on_normal_floor_turn(self):
        prompt = _norm(self._prompt_for(intent_category="EXECUTION"))
        assert "never invent" in prompt
        assert "magic phrase" in prompt

    def test_rule_absent_in_denial_mode(self):
        # Denial mode (#992) swaps the addendum and drops the manifest; the
        # phrasing rule rides the manifest, so it drops with it.
        prompt = _norm(self._prompt_for(denial_mode=True))
        assert "magic phrase" not in prompt
