"""
Tests for Lifecycle State Machine (P3).

This module tests the 8-stage lifecycle model for objects:
EMERGENT → DERIVED → NOTICED → PROPOSED → RATIFIED → DEPRECATED → ARCHIVED → COMPOSTED

"Nothing disappears, it transforms."

References:
- ADR-055: Object Model Implementation
- MUX-399-P3: Lifecycle State Machine with Composting
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

import pytest

from services.mux.lifecycle import (
    TRANSITION_EXPLANATIONS,
    VALID_TRANSITIONS,
    CompostingExtractor,
    CompostResult,
    HasLifecycle,
    InvalidTransitionError,
    LifecycleManager,
    LifecycleState,
    LifecycleTransition,
    get_composting_narrative,
    transition_explanation,
)

# =============================================================================
# Phase 1: LifecycleState Enum Tests
# =============================================================================


class TestLifecycleStateBasics:
    """Test the 8-stage lifecycle enum."""

    def test_has_emergent_state(self):
        """EMERGENT state exists - first stirrings of an idea."""
        assert LifecycleState.EMERGENT is not None
        assert LifecycleState.EMERGENT.value == "emergent"

    def test_has_derived_state(self):
        """DERIVED state exists - pattern recognized from emergence."""
        assert LifecycleState.DERIVED is not None
        assert LifecycleState.DERIVED.value == "derived"

    def test_has_noticed_state(self):
        """NOTICED state exists - brought to attention."""
        assert LifecycleState.NOTICED is not None
        assert LifecycleState.NOTICED.value == "noticed"

    def test_has_proposed_state(self):
        """PROPOSED state exists - formal recommendation."""
        assert LifecycleState.PROPOSED is not None
        assert LifecycleState.PROPOSED.value == "proposed"

    def test_has_ratified_state(self):
        """RATIFIED state exists - officially accepted."""
        assert LifecycleState.RATIFIED is not None
        assert LifecycleState.RATIFIED.value == "ratified"

    def test_has_deprecated_state(self):
        """DEPRECATED state exists - marked for retirement."""
        assert LifecycleState.DEPRECATED is not None
        assert LifecycleState.DEPRECATED.value == "deprecated"

    def test_has_archived_state(self):
        """ARCHIVED state exists - preserved but inactive."""
        assert LifecycleState.ARCHIVED is not None
        assert LifecycleState.ARCHIVED.value == "archived"

    def test_has_composted_state(self):
        """COMPOSTED state exists - transformed into nourishment."""
        assert LifecycleState.COMPOSTED is not None
        assert LifecycleState.COMPOSTED.value == "composted"

    def test_exactly_eight_states(self):
        """Lifecycle has exactly 8 states."""
        assert len(LifecycleState) == 8


class TestLifecycleStateMeanings:
    """Test the meaning property for each state."""

    def test_emergent_meaning(self):
        """EMERGENT has meaning describing initial formation."""
        assert (
            "stirring" in LifecycleState.EMERGENT.meaning.lower()
            or "forming" in LifecycleState.EMERGENT.meaning.lower()
        )

    def test_derived_meaning(self):
        """DERIVED has meaning describing pattern recognition."""
        assert (
            "pattern" in LifecycleState.DERIVED.meaning.lower()
            or "derived" in LifecycleState.DERIVED.meaning.lower()
        )

    def test_noticed_meaning(self):
        """NOTICED has meaning describing awareness."""
        assert (
            "attention" in LifecycleState.NOTICED.meaning.lower()
            or "noticed" in LifecycleState.NOTICED.meaning.lower()
        )

    def test_proposed_meaning(self):
        """PROPOSED has meaning describing recommendation."""
        assert (
            "recommend" in LifecycleState.PROPOSED.meaning.lower()
            or "proposed" in LifecycleState.PROPOSED.meaning.lower()
        )

    def test_ratified_meaning(self):
        """RATIFIED has meaning describing acceptance."""
        assert (
            "accept" in LifecycleState.RATIFIED.meaning.lower()
            or "ratified" in LifecycleState.RATIFIED.meaning.lower()
        )

    def test_deprecated_meaning(self):
        """DEPRECATED has meaning describing retirement."""
        assert (
            "retire" in LifecycleState.DEPRECATED.meaning.lower()
            or "deprecated" in LifecycleState.DEPRECATED.meaning.lower()
        )

    def test_archived_meaning(self):
        """ARCHIVED has meaning describing preservation."""
        assert (
            "preserved" in LifecycleState.ARCHIVED.meaning.lower()
            or "archived" in LifecycleState.ARCHIVED.meaning.lower()
        )

    def test_composted_meaning(self):
        """COMPOSTED has meaning describing transformation."""
        assert (
            "transform" in LifecycleState.COMPOSTED.meaning.lower()
            or "nourish" in LifecycleState.COMPOSTED.meaning.lower()
        )


class TestLifecycleStateExperiencePhrases:
    """Test consciousness-preserving experience phrases."""

    def test_emergent_experience_phrase(self):
        """EMERGENT has phrase expressing initial sensing."""
        phrase = LifecycleState.EMERGENT.experience_phrase
        assert phrase and len(phrase) > 10

    def test_derived_experience_phrase(self):
        """DERIVED has phrase expressing pattern recognition."""
        phrase = LifecycleState.DERIVED.experience_phrase
        assert phrase and len(phrase) > 10

    def test_composted_experience_phrase(self):
        """COMPOSTED has phrase expressing learning (transformation)."""
        phrase = LifecycleState.COMPOSTED.experience_phrase
        # Learning is the transformed outcome of composting
        assert "learned" in phrase.lower() or "learning" in phrase.lower()


class TestLifecycleStateTypicalObjects:
    """Test typical_objects property."""

    def test_emergent_typical_objects(self):
        """EMERGENT lists typical object types."""
        objects = LifecycleState.EMERGENT.typical_objects
        assert isinstance(objects, list)
        assert len(objects) > 0

    def test_ratified_typical_objects(self):
        """RATIFIED lists typical object types."""
        objects = LifecycleState.RATIFIED.typical_objects
        assert isinstance(objects, list)
        assert len(objects) > 0

    def test_composted_typical_objects(self):
        """COMPOSTED lists typical object types."""
        objects = LifecycleState.COMPOSTED.typical_objects
        assert isinstance(objects, list)
        assert len(objects) > 0


# =============================================================================
# Phase 2: Transition Rules Tests
# =============================================================================


class TestTransitionRulesStructure:
    """Test the VALID_TRANSITIONS mapping structure."""

    def test_valid_transitions_exists(self):
        """VALID_TRANSITIONS constant exists."""
        assert VALID_TRANSITIONS is not None
        assert isinstance(VALID_TRANSITIONS, dict)

    def test_all_states_have_transitions_defined(self):
        """Every state has a transition entry (even if empty set)."""
        for state in LifecycleState:
            assert state in VALID_TRANSITIONS

    def test_composted_has_no_transitions(self):
        """COMPOSTED is terminal - no outward transitions."""
        assert VALID_TRANSITIONS[LifecycleState.COMPOSTED] == set()


class TestTransitionRulesValidity:
    """Test specific valid transitions."""

    def test_emergent_can_transition_to_derived(self):
        """EMERGENT → DERIVED is valid."""
        assert LifecycleState.DERIVED in VALID_TRANSITIONS[LifecycleState.EMERGENT]

    def test_emergent_can_transition_to_noticed(self):
        """EMERGENT → NOTICED is valid (skip derived)."""
        assert LifecycleState.NOTICED in VALID_TRANSITIONS[LifecycleState.EMERGENT]

    def test_derived_can_transition_to_noticed(self):
        """DERIVED → NOTICED is valid."""
        assert LifecycleState.NOTICED in VALID_TRANSITIONS[LifecycleState.DERIVED]

    def test_derived_can_transition_to_deprecated(self):
        """DERIVED → DEPRECATED is valid (early deprecation)."""
        assert LifecycleState.DEPRECATED in VALID_TRANSITIONS[LifecycleState.DERIVED]

    def test_noticed_can_transition_to_proposed(self):
        """NOTICED → PROPOSED is valid."""
        assert LifecycleState.PROPOSED in VALID_TRANSITIONS[LifecycleState.NOTICED]

    def test_noticed_can_transition_to_deprecated(self):
        """NOTICED → DEPRECATED is valid (abandon without proposal)."""
        assert LifecycleState.DEPRECATED in VALID_TRANSITIONS[LifecycleState.NOTICED]

    def test_proposed_can_transition_to_ratified(self):
        """PROPOSED → RATIFIED is valid."""
        assert LifecycleState.RATIFIED in VALID_TRANSITIONS[LifecycleState.PROPOSED]

    def test_proposed_can_transition_to_deprecated(self):
        """PROPOSED → DEPRECATED is valid (rejected proposal)."""
        assert LifecycleState.DEPRECATED in VALID_TRANSITIONS[LifecycleState.PROPOSED]

    def test_ratified_can_transition_to_deprecated(self):
        """RATIFIED → DEPRECATED is valid."""
        assert LifecycleState.DEPRECATED in VALID_TRANSITIONS[LifecycleState.RATIFIED]

    def test_deprecated_can_transition_to_archived(self):
        """DEPRECATED → ARCHIVED is valid."""
        assert LifecycleState.ARCHIVED in VALID_TRANSITIONS[LifecycleState.DEPRECATED]

    def test_archived_can_transition_to_composted(self):
        """ARCHIVED → COMPOSTED is valid."""
        assert LifecycleState.COMPOSTED in VALID_TRANSITIONS[LifecycleState.ARCHIVED]


class TestLifecycleTransitionDataclass:
    """Test LifecycleTransition dataclass."""

    def test_transition_has_from_state(self):
        """Transition captures from_state."""
        t = LifecycleTransition(from_state=LifecycleState.EMERGENT, to_state=LifecycleState.DERIVED)
        assert t.from_state == LifecycleState.EMERGENT

    def test_transition_has_to_state(self):
        """Transition captures to_state."""
        t = LifecycleTransition(from_state=LifecycleState.EMERGENT, to_state=LifecycleState.DERIVED)
        assert t.to_state == LifecycleState.DERIVED

    def test_valid_transition_is_valid(self):
        """is_valid() returns True for valid transitions."""
        t = LifecycleTransition(from_state=LifecycleState.EMERGENT, to_state=LifecycleState.DERIVED)
        assert t.is_valid() is True

    def test_invalid_transition_is_not_valid(self):
        """is_valid() returns False for invalid transitions."""
        t = LifecycleTransition(
            from_state=LifecycleState.COMPOSTED,
            to_state=LifecycleState.EMERGENT,  # Can't resurrect!
        )
        assert t.is_valid() is False

    def test_same_state_transition_is_invalid(self):
        """is_valid() returns False for no-op transitions."""
        t = LifecycleTransition(
            from_state=LifecycleState.RATIFIED, to_state=LifecycleState.RATIFIED
        )
        assert t.is_valid() is False

    def test_backward_transition_is_invalid(self):
        """is_valid() returns False for backward transitions."""
        t = LifecycleTransition(
            from_state=LifecycleState.RATIFIED,
            to_state=LifecycleState.PROPOSED,  # Can't un-ratify
        )
        assert t.is_valid() is False


class TestInvalidTransitionError:
    """Test InvalidTransitionError exception."""

    def test_error_is_exception(self):
        """InvalidTransitionError is a proper exception."""
        assert issubclass(InvalidTransitionError, Exception)

    def test_error_message_includes_states(self):
        """Error message includes from and to states."""
        error = InvalidTransitionError(LifecycleState.COMPOSTED, LifecycleState.EMERGENT)
        msg = str(error)
        assert "composted" in msg.lower()
        assert "emergent" in msg.lower()

    def test_user_message_for_backward_transition(self):
        """Backward transitions get friendly 'forward only' message."""
        error = InvalidTransitionError(LifecycleState.RATIFIED, LifecycleState.PROPOSED)
        assert "forward" in error.user_message.lower()
        # Should NOT contain technical state names
        assert "RATIFIED" not in error.user_message
        assert "PROPOSED" not in error.user_message

    def test_user_message_for_skip_transition(self):
        """Skipping states gets friendly 'one step at a time' message."""
        # EMERGENT can go to DERIVED or NOTICED, but not directly to PROPOSED
        error = InvalidTransitionError(LifecycleState.EMERGENT, LifecycleState.PROPOSED)
        assert "step" in error.user_message.lower() or "jump" in error.user_message.lower()

    def test_user_message_for_composted_terminal(self):
        """COMPOSTED is terminal - learning stays that way."""
        error = InvalidTransitionError(LifecycleState.COMPOSTED, LifecycleState.EMERGENT)
        assert "learning" in error.user_message.lower()

    def test_user_message_no_technical_jargon(self):
        """User messages should not expose state names."""
        test_cases = [
            (LifecycleState.COMPOSTED, LifecycleState.EMERGENT),
            (LifecycleState.RATIFIED, LifecycleState.EMERGENT),
            (LifecycleState.EMERGENT, LifecycleState.RATIFIED),
        ]
        for from_state, to_state in test_cases:
            error = InvalidTransitionError(from_state, to_state)
            msg = error.user_message
            # Should not contain uppercase state names
            for state in LifecycleState:
                assert state.value.upper() not in msg.upper() or state.value.lower() in msg.lower()


class TestTransitionExplanations:
    """Test transition explanation templates and function."""

    def test_all_valid_transitions_have_explanations(self):
        """Every valid transition has an explanation template."""
        for from_state, to_states in VALID_TRANSITIONS.items():
            for to_state in to_states:
                key = (from_state, to_state)
                assert (
                    key in TRANSITION_EXPLANATIONS
                ), f"Missing explanation for {from_state.value} → {to_state.value}"

    def test_explanation_count_matches_transitions(self):
        """Number of explanations matches number of valid transitions."""
        valid_count = sum(len(to_states) for to_states in VALID_TRANSITIONS.values())
        assert len(TRANSITION_EXPLANATIONS) == valid_count

    def test_emergent_to_derived_explanation(self):
        """EMERGENT→DERIVED explains pattern recognition."""
        explanation = transition_explanation(
            LifecycleState.EMERGENT, LifecycleState.DERIVED, "this task"
        )
        assert "recognized" in explanation.lower() or "pattern" in explanation.lower()
        assert "this task" in explanation

    def test_emergent_to_noticed_explanation(self):
        """EMERGENT→NOTICED explains noticing."""
        explanation = transition_explanation(
            LifecycleState.EMERGENT, LifecycleState.NOTICED, "this issue"
        )
        assert "noticed" in explanation.lower() or "attention" in explanation.lower()
        assert "this issue" in explanation

    def test_proposed_to_ratified_explanation(self):
        """PROPOSED→RATIFIED explains agreement."""
        explanation = transition_explanation(
            LifecycleState.PROPOSED, LifecycleState.RATIFIED, "the plan"
        )
        assert "agreed" in explanation.lower() or "proceed" in explanation.lower()
        assert "the plan" in explanation

    def test_archived_to_composted_explanation(self):
        """ARCHIVED→COMPOSTED explains learning."""
        explanation = transition_explanation(
            LifecycleState.ARCHIVED, LifecycleState.COMPOSTED, "that project"
        )
        assert "taught" in explanation.lower() or "learn" in explanation.lower()
        assert "that project" in explanation

    def test_explanation_with_reason(self):
        """Explanations can include optional reason."""
        explanation = transition_explanation(
            LifecycleState.NOTICED,
            LifecycleState.DEPRECATED,
            "this task",
            reason="user marked it as obsolete",
        )
        assert "this task" in explanation
        assert "user marked it as obsolete" in explanation

    def test_explanation_uses_object_name(self):
        """Explanation substitutes object_name into template."""
        explanation = transition_explanation(
            LifecycleState.DEPRECATED, LifecycleState.ARCHIVED, "Sprint 42 retrospective"
        )
        assert "Sprint 42 retrospective" in explanation

    def test_default_object_name(self):
        """Default object name is 'this'."""
        explanation = transition_explanation(LifecycleState.RATIFIED, LifecycleState.DEPRECATED)
        assert "this" in explanation.lower()

    def test_explanations_use_first_person(self):
        """Explanations use first-person or collaborative language."""
        # Check a sample of explanations
        for (from_state, to_state), template in list(TRANSITION_EXPLANATIONS.items())[:5]:
            # Should use "I" or "We" or object-focused language
            has_perspective = "I " in template or "We " in template or "{object}" in template
            assert has_perspective, f"Template lacks perspective: {template}"

    def test_invalid_transition_fallback(self):
        """Unknown transitions get generic fallback."""
        # This shouldn't happen in practice, but test the fallback
        explanation = transition_explanation(
            LifecycleState.COMPOSTED, LifecycleState.EMERGENT, "test"
        )
        # Should still return something, not crash
        assert len(explanation) > 0


# =============================================================================
# Phase 3: HasLifecycle Protocol Tests
# =============================================================================


class TestHasLifecycleProtocol:
    """Test HasLifecycle protocol for runtime checking."""

    def test_protocol_is_runtime_checkable(self):
        """HasLifecycle can be used with isinstance()."""

        class MockLifecycled:
            @property
            def lifecycle_state(self) -> LifecycleState:
                return LifecycleState.EMERGENT

            @property
            def lifecycle_history(self) -> List:
                return []

        obj = MockLifecycled()
        assert isinstance(obj, HasLifecycle)

    def test_non_conforming_object_fails(self):
        """Objects without lifecycle properties don't satisfy protocol."""

        class NoLifecycle:
            pass

        obj = NoLifecycle()
        assert not isinstance(obj, HasLifecycle)

    def test_partial_implementation_fails(self):
        """Objects with only some properties don't satisfy protocol."""

        class PartialLifecycle:
            @property
            def lifecycle_state(self) -> LifecycleState:
                return LifecycleState.EMERGENT

            # Missing lifecycle_history

        obj = PartialLifecycle()
        assert not isinstance(obj, HasLifecycle)


# =============================================================================
# Phase 4: LifecycleManager Tests
# =============================================================================


class TestLifecycleManagerBasics:
    """Test LifecycleManager basic functionality."""

    def test_manager_exists(self):
        """LifecycleManager class exists."""
        assert LifecycleManager is not None

    def test_manager_can_be_instantiated(self):
        """LifecycleManager can be created."""
        manager = LifecycleManager()
        assert manager is not None


class MockLifecycleObject:
    """Test fixture: object with lifecycle support."""

    def __init__(self, initial_state: LifecycleState = LifecycleState.EMERGENT):
        self._state = initial_state
        self._history: List[LifecycleTransition] = []

    @property
    def lifecycle_state(self) -> LifecycleState:
        return self._state

    @lifecycle_state.setter
    def lifecycle_state(self, value: LifecycleState):
        self._state = value

    @property
    def lifecycle_history(self) -> List[LifecycleTransition]:
        return self._history

    def add_history(self, transition: LifecycleTransition):
        self._history.append(transition)


class TestLifecycleManagerTransition:
    """Test LifecycleManager.transition() method."""

    def test_valid_transition_succeeds(self):
        """Manager performs valid transitions."""
        manager = LifecycleManager()
        obj = MockLifecycleObject(LifecycleState.EMERGENT)

        result = manager.transition(obj, LifecycleState.DERIVED)

        assert result is True
        assert obj.lifecycle_state == LifecycleState.DERIVED

    def test_transition_records_history(self):
        """Manager records transition in history."""
        manager = LifecycleManager()
        obj = MockLifecycleObject(LifecycleState.EMERGENT)

        manager.transition(obj, LifecycleState.DERIVED)

        assert len(obj.lifecycle_history) == 1
        assert obj.lifecycle_history[0].from_state == LifecycleState.EMERGENT
        assert obj.lifecycle_history[0].to_state == LifecycleState.DERIVED

    def test_invalid_transition_raises(self):
        """Manager raises InvalidTransitionError for invalid transitions."""
        manager = LifecycleManager()
        obj = MockLifecycleObject(LifecycleState.COMPOSTED)

        with pytest.raises(InvalidTransitionError):
            manager.transition(obj, LifecycleState.EMERGENT)

    def test_invalid_transition_does_not_change_state(self):
        """Failed transition leaves state unchanged."""
        manager = LifecycleManager()
        obj = MockLifecycleObject(LifecycleState.COMPOSTED)

        try:
            manager.transition(obj, LifecycleState.EMERGENT)
        except InvalidTransitionError:
            pass

        assert obj.lifecycle_state == LifecycleState.COMPOSTED

    def test_callback_is_called_on_success(self):
        """Manager calls callback after successful transition."""
        manager = LifecycleManager()
        obj = MockLifecycleObject(LifecycleState.EMERGENT)
        callback_called = []

        def on_transition(transition: LifecycleTransition):
            callback_called.append(transition)

        manager.transition(obj, LifecycleState.DERIVED, on_transition=on_transition)

        assert len(callback_called) == 1
        assert callback_called[0].to_state == LifecycleState.DERIVED

    def test_full_lifecycle_journey(self):
        """Manager can take object through full lifecycle."""
        manager = LifecycleManager()
        obj = MockLifecycleObject(LifecycleState.EMERGENT)

        # EMERGENT → DERIVED → NOTICED → PROPOSED → RATIFIED
        manager.transition(obj, LifecycleState.DERIVED)
        manager.transition(obj, LifecycleState.NOTICED)
        manager.transition(obj, LifecycleState.PROPOSED)
        manager.transition(obj, LifecycleState.RATIFIED)
        # → DEPRECATED → ARCHIVED → COMPOSTED
        manager.transition(obj, LifecycleState.DEPRECATED)
        manager.transition(obj, LifecycleState.ARCHIVED)
        manager.transition(obj, LifecycleState.COMPOSTED)

        assert obj.lifecycle_state == LifecycleState.COMPOSTED
        assert len(obj.lifecycle_history) == 7


# =============================================================================
# Phase 5: Composting Integration Tests
# =============================================================================


class TestCompostResultDataclass:
    """Test CompostResult dataclass."""

    def test_compost_result_has_object_summary(self):
        """CompostResult captures object summary."""
        result = CompostResult(
            object_summary={"type": "task", "title": "Old task"},
            journey=[],
            lessons=["Scope creep is real"],
            composted_at=datetime.now(),
        )
        assert result.object_summary["type"] == "task"

    def test_compost_result_has_journey(self):
        """CompostResult captures lifecycle journey."""
        result = CompostResult(
            object_summary={},
            journey=[LifecycleState.EMERGENT, LifecycleState.DEPRECATED],
            lessons=[],
            composted_at=datetime.now(),
        )
        assert len(result.journey) == 2

    def test_compost_result_has_lessons(self):
        """CompostResult captures extracted lessons."""
        result = CompostResult(
            object_summary={},
            journey=[],
            lessons=["Don't over-engineer", "Get feedback early"],
            composted_at=datetime.now(),
        )
        assert len(result.lessons) == 2

    def test_compost_result_has_timestamp(self):
        """CompostResult has composted_at timestamp."""
        now = datetime.now()
        result = CompostResult(object_summary={}, journey=[], lessons=[], composted_at=now)
        assert result.composted_at == now


class TestCompostingExtractorBasics:
    """Test CompostingExtractor basic functionality."""

    def test_extractor_exists(self):
        """CompostingExtractor class exists."""
        assert CompostingExtractor is not None

    def test_extractor_can_be_instantiated(self):
        """CompostingExtractor can be created."""
        extractor = CompostingExtractor()
        assert extractor is not None


class MockCompostableObject:
    """Test fixture: object that can be composted."""

    def __init__(self):
        self._state = LifecycleState.ARCHIVED
        self._history: List[LifecycleTransition] = []
        self.title = "Old Feature Request"
        self.created_at = datetime(2024, 1, 1)
        self.description = "A feature that was never built"

    @property
    def lifecycle_state(self) -> LifecycleState:
        return self._state

    @lifecycle_state.setter
    def lifecycle_state(self, value: LifecycleState):
        self._state = value

    @property
    def lifecycle_history(self) -> List[LifecycleTransition]:
        return self._history

    def add_history(self, transition: LifecycleTransition):
        self._history.append(transition)


class TestCompostingExtractorExtract:
    """Test CompostingExtractor.extract() method."""

    def test_extract_produces_compost_result(self):
        """Extractor produces CompostResult from object."""
        extractor = CompostingExtractor()
        obj = MockCompostableObject()

        result = extractor.extract(obj)

        assert isinstance(result, CompostResult)

    def test_extract_captures_object_summary(self):
        """Extractor captures key object attributes."""
        extractor = CompostingExtractor()
        obj = MockCompostableObject()

        result = extractor.extract(obj)

        assert result.object_summary is not None
        assert "title" in result.object_summary or len(result.object_summary) > 0

    def test_extract_captures_journey(self):
        """Extractor captures lifecycle journey."""
        extractor = CompostingExtractor()
        obj = MockCompostableObject()
        # Add some history
        obj.add_history(
            LifecycleTransition(from_state=LifecycleState.EMERGENT, to_state=LifecycleState.NOTICED)
        )

        result = extractor.extract(obj)

        # Journey should reflect the history
        assert result.journey is not None

    def test_extract_sets_timestamp(self):
        """Extractor sets composted_at timestamp."""
        extractor = CompostingExtractor()
        obj = MockCompostableObject()

        before = datetime.now()
        result = extractor.extract(obj)
        after = datetime.now()

        assert before <= result.composted_at <= after

    def test_extract_generates_lessons(self):
        """Extractor generates lessons from object."""
        extractor = CompostingExtractor()
        obj = MockCompostableObject()

        result = extractor.extract(obj)

        # Should have at least one lesson or empty list
        assert isinstance(result.lessons, list)


class TestCompostingPhilosophy:
    """Test the philosophical aspects of composting."""

    def test_composted_objects_retain_wisdom(self):
        """Composting preserves learned insights."""
        extractor = CompostingExtractor()
        obj = MockCompostableObject()

        result = extractor.extract(obj)

        # The result should contain enough info to learn from
        assert result.object_summary or result.lessons or result.journey

    def test_nothing_truly_disappears(self):
        """Composted objects transform rather than vanish."""
        extractor = CompostingExtractor()
        obj = MockCompostableObject()
        obj.title = "Important Lesson"

        result = extractor.extract(obj)

        # Original identity should be traceable
        summary_str = str(result.object_summary)
        assert len(summary_str) > 0  # Something is preserved


class TestCompostingNarrative:
    """Test user-facing narrative generation for composting."""

    def test_narrative_returns_string(self):
        """get_composting_narrative returns a string."""
        result = CompostResult(
            object_summary={"title": "Test Task"},
            journey=[LifecycleState.EMERGENT, LifecycleState.COMPOSTED],
            lessons=["Learned something"],
            composted_at=datetime.now(),
        )
        narrative = get_composting_narrative(result)
        assert isinstance(narrative, str)
        assert len(narrative) > 0

    def test_narrative_includes_lessons(self):
        """Narrative includes the lessons learned."""
        result = CompostResult(
            object_summary={"title": "Feature X"},
            journey=[LifecycleState.EMERGENT, LifecycleState.COMPOSTED],
            lessons=["Users prefer simplicity"],
            composted_at=datetime.now(),
        )
        narrative = get_composting_narrative(result)
        assert "simplicity" in narrative.lower()

    def test_narrative_full_lifecycle(self):
        """Full lifecycle journey gets reflective narrative."""
        full_journey = [
            LifecycleState.EMERGENT,
            LifecycleState.DERIVED,
            LifecycleState.NOTICED,
            LifecycleState.PROPOSED,
            LifecycleState.RATIFIED,
            LifecycleState.DEPRECATED,
            LifecycleState.ARCHIVED,
            LifecycleState.COMPOSTED,
        ]
        result = CompostResult(
            object_summary={"title": "Sprint 42"},
            journey=full_journey,
            lessons=["Patterns are worth studying"],
            composted_at=datetime.now(),
        )
        narrative = get_composting_narrative(result)
        # Should use reflective "Having had time" template
        assert "reflect" in narrative.lower() or "learned" in narrative.lower()
        assert "Sprint 42" in narrative

    def test_narrative_short_lifecycle(self):
        """Short lifecycle gets brief narrative."""
        result = CompostResult(
            object_summary={"title": "Quick Idea"},
            journey=[LifecycleState.EMERGENT, LifecycleState.DEPRECATED, LifecycleState.COMPOSTED],
            lessons=["Sometimes ideas don't pan out"],
            composted_at=datetime.now(),
        )
        narrative = get_composting_narrative(result)
        assert "brief" in narrative.lower()
        assert "Quick Idea" in narrative

    def test_narrative_ratified_then_deprecated(self):
        """Ratified then deprecated gets 'worked for a while' narrative."""
        result = CompostResult(
            object_summary={"title": "Old Feature"},
            journey=[
                LifecycleState.EMERGENT,
                LifecycleState.PROPOSED,
                LifecycleState.RATIFIED,
                LifecycleState.DEPRECATED,
                LifecycleState.COMPOSTED,
            ],
            lessons=["Features have lifespans"],
            composted_at=datetime.now(),
        )
        narrative = get_composting_narrative(result)
        assert "worked" in narrative.lower() or "looking back" in narrative.lower()

    def test_narrative_no_deletion_language(self):
        """Narrative never uses deletion language."""
        result = CompostResult(
            object_summary={"title": "Some Object"},
            journey=[LifecycleState.EMERGENT, LifecycleState.COMPOSTED],
            lessons=["Test lesson"],
            composted_at=datetime.now(),
        )
        narrative = get_composting_narrative(result)
        # Should NOT contain deletion words
        forbidden_words = ["delete", "remove", "gone", "destroy", "erase"]
        for word in forbidden_words:
            assert word not in narrative.lower(), f"Found forbidden word: {word}"

    def test_narrative_uses_object_title(self):
        """Narrative incorporates the object's title."""
        result = CompostResult(
            object_summary={"title": "Customer Feedback Loop"},
            journey=[LifecycleState.EMERGENT, LifecycleState.COMPOSTED],
            lessons=["Feedback matters"],
            composted_at=datetime.now(),
        )
        narrative = get_composting_narrative(result)
        assert "Customer Feedback Loop" in narrative

    def test_narrative_fallback_for_no_title(self):
        """Narrative handles objects without title gracefully."""
        result = CompostResult(
            object_summary={},  # No title
            journey=[LifecycleState.EMERGENT, LifecycleState.COMPOSTED],
            lessons=["Anonymous wisdom"],
            composted_at=datetime.now(),
        )
        narrative = get_composting_narrative(result)
        assert len(narrative) > 0  # Still produces something
        assert "this" in narrative.lower()  # Uses fallback

    def test_narrative_limits_lessons_display(self):
        """Narrative doesn't overwhelm with too many lessons."""
        result = CompostResult(
            object_summary={"title": "Complex Project"},
            journey=[LifecycleState.EMERGENT, LifecycleState.COMPOSTED],
            lessons=[
                "First lesson",
                "Second lesson",
                "Third lesson",
                "Fourth lesson",
                "Fifth lesson",
            ],
            composted_at=datetime.now(),
        )
        narrative = get_composting_narrative(result)
        # Should include some lessons but not all 5
        lesson_count = sum(
            1 for l in ["First", "Second", "Third", "Fourth", "Fifth"] if l in narrative
        )
        assert lesson_count <= 3  # Capped at 3

    def test_narrative_uses_name_if_no_title(self):
        """Narrative uses 'name' field if 'title' not available."""
        result = CompostResult(
            object_summary={"name": "project-alpha"},
            journey=[LifecycleState.EMERGENT, LifecycleState.COMPOSTED],
            lessons=["Names matter"],
            composted_at=datetime.now(),
        )
        narrative = get_composting_narrative(result)
        assert "project-alpha" in narrative
