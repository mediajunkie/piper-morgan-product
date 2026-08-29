"""#1517 capability-gaslighting guards — the floor must not deny wired
capabilities and must never fabricate retractions of prior turns.

Incident (PM live, 2026-08-08): turn 1 "remind me at 3pm tomorrow…" EXECUTED
(create_reminder, row stored). Turn 2 "remind me at 9:41 today to…" fell to the
LLM floor, which replied "I can't actually set reminders from chat — I should
have been upfront about that earlier rather than implying the 3pm one was
saved" — a false capability denial PLUS a fabricated retraction of a real prior
success, then recommended Slack /remind.

LAYER HONESTY (m-43): every test here is a derivation test or a PROMPT-CONTENT
test. They verify (a) the wired-capability manifest derives correctly from the
dispatch surfaces and (b) the exact text the floor assembles into its system
prompt. They do NOT verify live LLM behavior — a model can still disobey its
prompt; that verification is a live chat/behavioral test, out of scope here.
"""

import asyncio
import re

from services.intent_service.conversational_floor import (
    FLOOR_SYSTEM_PROMPT_ADDENDUM,
    ConversationalFloor,
    FloorContext,
    capability_manifest_block,
)
from services.intent_service.unwired_writes import UNWIRED_WRITE_DECLINES
from services.intent_service.workflow_dispatcher import wired_chat_actions


def _norm(text: str) -> str:
    """Collapse line-wrapping so phrase assertions span newlines+indent."""
    return re.sub(r"\s+", " ", text).lower()


class TestWiredChatActionsDerivation:
    """wired_chat_actions() — the manifest's source set.

    Layer: pure derivation. Sources (never hand-maintained): the workflow
    registry's action_triggered WorkflowEntries (effect-classified, #1124/
    PDR-006) plus the legacy _handle_execution_intent dispatch targets as
    enumerated by ActionMapper.ACTION_MAPPING values (#284).
    """

    def test_includes_the_incident_capability_create_reminder(self):
        # create_reminder is wired via the legacy EXECUTION elif chain
        # (intent_service.py _handle_execution_intent) AND, since #1560, the
        # rail — the derivation must cover both surfaces (and dedup them, see
        # test_create_reminder_rail_1560) or it re-opens exactly the #1517 gap.
        assert "create_reminder" in wired_chat_actions()

    def test_includes_registry_rail_actions(self):
        wired = wired_chat_actions()
        # registry-wired, action_triggered=True (#1521 / #1411)
        assert "list_reminders_query" in wired
        assert "update_issue" in wired

    def test_includes_legacy_elif_actions(self):
        wired = wired_chat_actions()
        for action in ("create_todo", "list_todos", "complete_todo", "delete_todo"):
            assert action in wired, f"legacy-wired action missing: {action}"

    def test_excludes_offer_only_and_sentinel_entries(self):
        wired = wired_chat_actions()
        # "meeting" is offer-only (action_triggered=False) — the rail never
        # dispatches it by classified action, so the floor must not be told
        # it's an ask-able chat action.
        assert "meeting" not in wired
        # ActionMapper's fallback sentinel is not a capability.
        assert "unknown_intent" not in wired

    def test_disjoint_from_unwired_write_declines(self):
        # The #1426/#1433 freshness invariant, asserted at the manifest layer:
        # nothing the product honest-declines as unwired may be presented to
        # the floor as a capability it HAS (that would be the inverse lie).
        overlap = set(wired_chat_actions()) & set(UNWIRED_WRITE_DECLINES)
        assert not overlap, f"manifest claims unwired capabilities: {sorted(overlap)}"

    def test_derivation_not_vacuous(self):
        # Vacuity guard (m-44): the set is DERIVED; a tiny result means the
        # derivation broke, not that Piper lost its capabilities.
        assert len(wired_chat_actions()) >= 20


class TestCapabilityManifestBlock:
    """capability_manifest_block() — the rendered prompt block.

    Layer: prompt content (verifies the prompt text, not live LLM behavior).
    """

    def test_names_wired_capabilities(self):
        block = capability_manifest_block()
        assert "create_reminder" in block
        assert "list_reminders_query" in block

    def test_forbids_denying_wired_capabilities(self):
        block = _norm(capability_manifest_block())
        assert "never tell the user you can't do" in block
        # the recover-path instruction: wired-but-unrouted asks get a
        # re-phrase request, not a denial or an external-tool redirect
        assert "restate" in block
        assert "do not recommend external tools" in block

    def test_static_prose_is_capability_name_free(self):
        # The derived list is the ONLY carrier of capability names — static
        # prose naming a capability would be the hand-maintained list this
        # design exists to avoid, and would go stale silently.
        static_prose = capability_manifest_block.__wrapped_static__
        for token in wired_chat_actions():
            assert (
                token not in static_prose
            ), f"hand-written capability name '{token}' in static manifest prose"


class TestSystemPromptCarriesManifest:
    """The assembled floor system prompt — every non-denial floor turn.

    Layer: prompt assembly (verifies _get_system_prompt output, not live
    LLM behavior).
    """

    def _prompt_for(self, **ctx_kwargs) -> str:
        floor = ConversationalFloor(system_prompt_base="BASE-IDENTITY")
        ctx = FloorContext(
            user_message="remind me at 9:41 today to tell the Lead Developer how testing is going.",
            session_id="s-1517",
            **ctx_kwargs,
        )
        return asyncio.run(floor._get_system_prompt(ctx))

    def test_manifest_present_on_normal_floor_turn(self):
        # The incident turn was TEMPORAL-classified — the manifest must ride
        # EVERY floor turn, not just IDENTITY/DISCOVERY context assembly.
        prompt = self._prompt_for(intent_category="TEMPORAL")
        assert "create_reminder" in prompt
        assert "never tell the user you can't do" in _norm(prompt)

    def test_manifest_absent_in_denial_mode(self):
        # Boundary declines (#992) swap the addendum; a capability list would
        # be noise (and an invitation to redirect into it).
        prompt = self._prompt_for(denial_mode=True)
        assert "create_reminder" not in prompt


class TestAntiRetraction:
    """The anti-retraction instruction in FLOOR_SYSTEM_PROMPT_ADDENDUM.

    Layer: prompt content (verifies the addendum text, not live LLM behavior).
    """

    def test_floor_forbids_fabricated_retractions(self):
        p = _norm(FLOOR_SYSTEM_PROMPT_ADDENDUM)
        assert "never retract" in p, "floor must carry the #1517 anti-retraction rule"
        assert "fabricated retraction" in p, (
            "floor must name the failure mode: inventing that a prior "
            "confirmed action failed / was never saved"
        )
        # the neutral middle: can't confirm ≠ didn't happen
        assert "stay neutral" in p

    def test_anti_retraction_coexists_with_no_reassertion_rule(self):
        # #1331's rule (don't TRUST prior '✓' claims) and #1517's rule (don't
        # DENY them) are duals; both must be present simultaneously.
        p = _norm(FLOOR_SYSTEM_PROMPT_ADDENDUM)
        assert "past claim of success is not proof" in p
        assert "never retract" in p
