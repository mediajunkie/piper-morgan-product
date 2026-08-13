"""#1509 TRUST-CONSENT — capability legibility (the other half of the one feature).

The derivation-chain tests: registry (declared effect) -> decide_consent
(the ONE decision function) -> copy; chat_pointers POINTER rows (ratchet-
verified routable utterances) -> example asks. NOTHING hand-written per
capability — a hand list would drift exactly like the ones #1333/#1517
retired.

Layer honesty (m-43): these test the DERIVATION and its outputs, not live
LLM behavior. Routability of example asks is inherited from the #1433
reachability ratchet (every POINTER utterance is resolution-asserted on
every build) — asserted here as set membership, not re-resolved.
"""

import pytest

from services.intent_service import capability_legibility as legibility
from services.intent_service.chat_pointers import pointer_utterances
from services.intent_service.collaboration_gate import (
    FRAMING_AMBIGUOUS,
    WorkingMode,
)
from services.intent_service.consent_gate import ConsentDecision, decide_consent
from services.intent_service.workflow_dispatcher import (
    get_action_workflows,
    wired_chat_actions,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import EffectClass


class TestEffectPhrases:
    def test_every_effect_tier_has_a_phrase(self):
        """Denominator: all len(EffectClass) tiers covered — a new tier fails
        here (and in describe_effect's KeyError) until it gets a phrase."""
        for effect in EffectClass:
            assert legibility.describe_effect(effect)

    def test_phrases_distinguish_the_tiers(self):
        phrases = {legibility.describe_effect(e) for e in EffectClass}
        assert len(phrases) == len(EffectClass)

    def test_write_phrase_names_the_boundary(self):
        """The #1509 boundary in user words: WRITE is 'outside our
        conversation' — the reason the consent check exists."""
        assert "outside our conversation" in legibility.describe_effect(EffectClass.WRITE)


class TestConsentLineDerivation:
    """consent_behavior_line is COMPUTED from decide_consent — the copy can't
    drift from the gate because it is derived from the gate."""

    @pytest.mark.parametrize(
        "effect,decision,fragment",
        [
            (EffectClass.READ, ConsentDecision.PROCEED, "right away"),
            (EffectClass.WRITE, ConsentDecision.COLLABORATE, "check with you"),
            (EffectClass.DESTRUCTIVE, ConsentDecision.CONFIRM, "explicit yes"),
        ],
    )
    def test_line_matches_the_gates_verdict(self, effect, decision, fragment):
        assert (
            decide_consent(effect, FRAMING_AMBIGUOUS, WorkingMode.COLLABORATE) is decision
        )
        assert fragment in legibility.consent_behavior_line(effect)


class TestCatalogDerivation:
    def test_every_catalog_action_is_a_registry_rail_key(self):
        """No hand-written capability names: the catalog's actions ARE
        registry keys (membership by existing — the #1428 discipline)."""
        register_default_workflows()
        rail_keys = set(get_action_workflows())
        catalog = legibility.capability_catalog()
        assert catalog, "catalog must not be empty"
        for entry in catalog:
            assert entry.action in rail_keys

    def test_one_entry_per_unique_rail_entry(self):
        """Alias dedup mirrors wired_chat_actions (#1517): aliases share
        their canonical's single description."""
        catalog = legibility.capability_catalog()
        actions = [d.action for d in catalog]
        assert len(actions) == len(set(actions))
        assert len(catalog) == len(legibility._unique_rail_entries())

    def test_fields_are_derived_not_stored(self):
        for entry in legibility.capability_catalog():
            assert entry.effect_phrase == legibility.describe_effect(entry.effect)
            assert entry.consent_line == legibility.consent_behavior_line(entry.effect)

    def test_example_asks_come_only_from_the_verified_ledger(self):
        """#1571: never teach a phrase that doesn't route. Every example ask
        is a POINTER utterance — routability inherited from the #1433
        ratchet, and absence of a pointer yields None, never an invention."""
        utterances = set(pointer_utterances())
        examples = [d.example_ask for d in legibility.capability_catalog() if d.example_ask]
        assert examples, "at least one rail capability has a verified example ask"
        for ask in examples:
            assert ask in utterances

    def test_known_pointer_backed_capability_carries_its_ask(self):
        by_action = {d.action: d for d in legibility.capability_catalog()}
        assert by_action["list_reminders_query"].example_ask == "what reminders do I have?"


class TestCoverageDenominator:
    def test_coverage_names_what_it_covers(self):
        """m-44: any claim built on the catalog carries its denominator —
        covered + uncovered == wired_total, and the uncovered remainder is
        the legacy (undeclared-effect) chain, not silently 'clear'."""
        cov = legibility.catalog_coverage()
        assert cov["covered"] + cov["uncovered"] == cov["wired_total"]
        assert cov["covered"] > 0

    def test_legacy_chain_actions_are_outside_not_clear(self):
        """The known boundary: wired-but-uncatalogued actions exist (the
        legacy _handle_execution_intent chain, e.g. the todo family) and are
        reported as uncovered — their consent + legibility ride their rail
        migration (#1605/#1569 lane). If this ever reaches 0, delete this
        test and the module-docstring caveat in the same commit."""
        covered = {d.action for d in legibility.capability_catalog()}
        uncovered = set(wired_chat_actions()) - covered
        assert uncovered, "legacy chain drained — update the catalog docstring"
        # The named example the report cites:
        assert any(a.endswith("_todo") or a.startswith("complete") for a in uncovered) or (
            "delete_todo" in uncovered or "complete_todo" in uncovered
        )


class TestGatePromptIsALegibilitySurface:
    def test_check_copy_carries_the_derived_effect_phrase(self):
        """The chain's last link: the consent check's copy embeds
        describe_effect output — the gate's own prompt is capability
        legibility (the synthesis's 'while intent forms' surface)."""
        from services.domain.models import Intent
        from services.intent_service.consent_gate import build_consent_check_offer
        from services.shared_types import IntentCategory

        intent = Intent(
            category=IntentCategory.QUERY,
            action="update_issue",
            confidence=0.9,
            original_message="the title of issue #108 ought to say Q3 roadmap",
            context={},
        )
        offer = build_consent_check_offer(intent, EffectClass.WRITE)
        assert legibility.describe_effect(EffectClass.WRITE) in offer.question
