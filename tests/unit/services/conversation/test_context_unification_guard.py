"""#1207 conversation-context unification guard (m-41: mechanism beats vigilance).

Pins the single-source-of-truth architecture so the dual-implementation
drift (ADR-005's pattern) can't silently regrow:

- The domain owns Conversation + ConversationTurn; the manager exposes
  persisted turns as domain objects (no manager-local context aggregate).
- Exactly ONE in-process working-state class exists
  (services.intent_service.conversation_context.ConversationContext),
  and exactly one domain→working-state mapping point (hydrate_turns_from_db)
  plus one prompt-shaped reader (build_recent_history).
- intent_service builds floor/slot-filling history ONLY via the shared
  builder — no inline turn-iteration copies (the 7-copies regression that
  produced #1122).
"""

import re
from pathlib import Path

import services.conversation.conversation_manager as manager_mod
from services.conversation.conversation_manager import ConversationManager

REPO_ROOT = Path(__file__).resolve().parents[4]


class TestManagerHasNoContextAggregate:
    def test_manager_module_does_not_define_conversation_context(self):
        """The anemic manager-local ConversationContext was eliminated
        (#1207); the domain Conversation + turn lists express the concept.
        If this fails, a duplicate aggregate is being reintroduced —
        extend the domain model or the working state instead."""
        assert not hasattr(manager_mod, "ConversationContext")

    def test_manager_read_api_is_get_recent_turns(self):
        assert hasattr(ConversationManager, "get_recent_turns")
        assert not hasattr(ConversationManager, "get_conversation_context")


class TestSingleWorkingStateMappingPoint:
    def test_working_state_module_exposes_the_two_sanctioned_entrypoints(self):
        from services.intent_service.conversation_context import (
            build_recent_history,
            hydrate_turns_from_db,
        )

        assert callable(build_recent_history)
        assert callable(hydrate_turns_from_db)

    def test_no_inline_history_building_in_intent_service(self):
        """The #1122 regression shape: hand-copied `for turn in
        conv_context.turns` history builders drifting apart (7 copies at
        peak, two with the [:-1] bug). All history reads go through
        build_recent_history."""
        src = (REPO_ROOT / "services" / "intent" / "intent_service.py").read_text()
        inline_builders = re.findall(r"for\s+turn\s+in\s+\w*conv\w*\.turns\[", src)
        assert inline_builders == [], (
            "Inline conversation-history builder(s) found in intent_service.py — "
            f"{inline_builders}. Use build_recent_history() "
            "(services/intent_service/conversation_context.py) instead."
        )

    def test_no_other_module_maps_domain_turns_into_working_state(self):
        """hydrate_turns_from_db is THE domain→working-state mapping point.
        Catch new callers of get_recent_turns that hand-build working-state
        turns (the mapping must stay in one place)."""
        ws_src = (REPO_ROOT / "services" / "intent_service" / "conversation_context.py").read_text()
        assert "get_recent_turns" in ws_src  # the sanctioned mapping point exists

        intent_src = (REPO_ROOT / "services" / "intent" / "intent_service.py").read_text()
        # intent_service may call hydrate_turns_from_db, but must not call
        # the manager's read API directly and hand-map turns itself.
        assert ".get_recent_turns(" not in intent_src, (
            "intent_service.py calls ConversationManager.get_recent_turns "
            "directly — route through hydrate_turns_from_db / "
            "build_recent_history so the mapping stays single-sourced."
        )
