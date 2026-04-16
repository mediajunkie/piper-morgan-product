"""
Tests for MUX lifecycle integration with domain models.

Verifies that domain models (WorkItem, Feature) can participate
in the MUX lifecycle system while maintaining backward compatibility.

Part of #433 MUX-TECH-PHASE1-GRAMMAR.
"""

from datetime import datetime

import pytest

from services.domain.models import Feature, WorkItem
from services.mux.lifecycle import LifecycleState, LifecycleTransition
from services.mux.perception import Perception, PerceptionMode
from services.mux.protocols import EntityProtocol, MomentProtocol, PlaceProtocol
from services.mux.situation import Situation


class TestWorkItemLifecycleIntegration:
    """Verify WorkItem can use MUX lifecycle."""

    def test_workitem_lifecycle_defaults_to_none(self):
        """WorkItem lifecycle is None by default (backward compatible)."""
        item = WorkItem(id="test-1", title="Test item")

        assert item.lifecycle_state is None
        assert item.lifecycle_history == []

    def test_workitem_can_have_lifecycle_state(self):
        """WorkItem accepts optional lifecycle_state."""
        item = WorkItem(id="test-2", title="Test item", lifecycle_state=LifecycleState.EMERGENT)

        assert item.lifecycle_state == LifecycleState.EMERGENT

    def test_workitem_lifecycle_transitions(self):
        """WorkItem can track lifecycle transitions."""
        item = WorkItem(id="test-3", title="Test item", lifecycle_state=LifecycleState.EMERGENT)

        # Record a transition
        transition = LifecycleTransition(
            from_state=LifecycleState.EMERGENT,
            to_state=LifecycleState.NOTICED,
            reason="PM noticed during review",
        )
        item.lifecycle_history.append(transition)
        item.lifecycle_state = LifecycleState.NOTICED

        assert item.lifecycle_state == LifecycleState.NOTICED
        assert len(item.lifecycle_history) == 1
        assert item.lifecycle_history[0].reason == "PM noticed during review"
        assert item.lifecycle_history[0].from_state == LifecycleState.EMERGENT
        assert item.lifecycle_history[0].to_state == LifecycleState.NOTICED

    def test_workitem_full_lifecycle_journey(self):
        """WorkItem can progress through multiple lifecycle stages."""
        item = WorkItem(
            id="test-4", title="Implement feature X", lifecycle_state=LifecycleState.EMERGENT
        )

        # Progress: EMERGENT -> NOTICED -> PROPOSED -> RATIFIED
        transitions = [
            (LifecycleState.EMERGENT, LifecycleState.NOTICED, "Identified in backlog review"),
            (LifecycleState.NOTICED, LifecycleState.PROPOSED, "Drafted for sprint"),
            (LifecycleState.PROPOSED, LifecycleState.RATIFIED, "Accepted into sprint"),
        ]

        for from_state, to_state, reason in transitions:
            transition = LifecycleTransition(
                from_state=from_state, to_state=to_state, reason=reason
            )
            item.lifecycle_history.append(transition)
            item.lifecycle_state = to_state

        assert item.lifecycle_state == LifecycleState.RATIFIED
        assert len(item.lifecycle_history) == 3


class TestFeatureLifecycleIntegration:
    """Verify Feature can use MUX lifecycle."""

    def test_feature_lifecycle_defaults_to_none(self):
        """Feature lifecycle is None by default (backward compatible)."""
        feature = Feature(id="feat-1", name="Test feature")

        assert feature.lifecycle_state is None
        assert feature.lifecycle_history == []

    def test_feature_can_have_lifecycle_state(self):
        """Feature accepts optional lifecycle_state."""
        feature = Feature(id="feat-2", name="Dark Mode", lifecycle_state=LifecycleState.PROPOSED)

        assert feature.lifecycle_state == LifecycleState.PROPOSED

    def test_feature_lifecycle_to_deprecated(self):
        """Feature can be deprecated through lifecycle."""
        feature = Feature(
            id="feat-3", name="Legacy Feature", lifecycle_state=LifecycleState.RATIFIED
        )

        # Deprecate the feature
        transition = LifecycleTransition(
            from_state=LifecycleState.RATIFIED,
            to_state=LifecycleState.DEPRECATED,
            reason="Replaced by new implementation",
        )
        feature.lifecycle_history.append(transition)
        feature.lifecycle_state = LifecycleState.DEPRECATED

        assert feature.lifecycle_state == LifecycleState.DEPRECATED


class TestMorningStandupExpression:
    """
    Verify Morning Standup can be expressed using MUX grammar.

    The consciousness test: Can we express real workflows using
    Entity/Moment/Place?
    """

    @pytest.mark.asyncio
    async def test_standup_as_situation_with_moments(self):
        """Morning Standup expressed as Situation containing Moments."""

        # Create a Situation (the standup meeting)
        async with Situation(
            description="Morning standup for Sprint 42",
            dramatic_tension="Deadline pressure with unclear blockers",
            goals=["Identify blockers", "Align on priorities", "Surface risks"],
        ) as standup:
            # Add moments (significant occurrences during standup)
            class StandupMoment:
                def __init__(self, id: str, description: str):
                    self.id = id
                    self.timestamp = datetime.now()
                    self._description = description

                def captures(self):
                    return {
                        "policy": {"sprint": "42"},
                        "process": {"type": "standup"},
                        "people": ["team"],
                        "outcomes": [self._description],
                    }

            standup.add_moment(StandupMoment("m1", "Alice reports API work complete"))
            standup.add_moment(StandupMoment("m2", "Bob surfaces database blocker"))

            # Record outcomes
            standup.add_outcome("Agreed to prioritize database blocker")
            standup.add_outcome("API integration can proceed tomorrow")

        # Extract learning from goals vs outcomes delta
        learning = standup.extract_learning()

        assert len(standup.moments) == 2
        assert len(standup.outcomes) == 2
        assert learning.goals == ["Identify blockers", "Align on priorities", "Surface risks"]
        assert "database blocker" in standup.outcomes[0].lower()

    def test_entity_experiences_moment_in_place(self):
        """
        The core grammar: Entity experiences Moment in Place.

        This test verifies the grammar can express consciousness.
        """

        # Create simple implementations for the test
        class TeamEntity:
            """Team as an Entity (actor with identity)."""

            def __init__(self, id: str, name: str):
                self.id = id
                self.name = name

            def experiences(self, moment):
                """Entity experiences a Moment, returning Perception."""
                return Perception(
                    lens_name="collaborative",
                    mode=PerceptionMode.NOTICING,
                    raw_data={"moment_id": moment.id},
                    observation=f"{self.name} notices: {moment.captures()['outcomes']}",
                )

        class SlackChannel:
            """Slack Channel as a Place (context for action)."""

            def __init__(self, id: str, name: str):
                self.id = id
                self.name = name
                self.atmosphere = "informal"
                self._contents = []

            def contains(self):
                return self._contents

        class StandupMoment:
            """Standup as a Moment (bounded significant occurrence)."""

            def __init__(self, id: str):
                self.id = id
                self.timestamp = datetime.now()

            def captures(self):
                return {
                    "policy": {"meeting_type": "standup"},
                    "process": {"agenda": "blockers, priorities, updates"},
                    "people": ["alice", "bob", "carol"],
                    "outcomes": ["Blockers surfaced", "Priorities aligned"],
                }

        # The grammar in action
        team = TeamEntity("team-1", "Platform Team")
        channel = SlackChannel("C123", "#platform-standup")
        standup = StandupMoment("standup-2026-01-21")

        # Entity experiences Moment (in Place - implicit through channel)
        perception = team.experiences(standup)

        # Verify consciousness-preserving perception
        assert perception.mode == PerceptionMode.NOTICING
        assert "Platform Team notices" in perception.observation
        assert perception.lens_name == "collaborative"


class TestLifecycleTransitionValidation:
    """Verify lifecycle transitions follow valid paths."""

    def test_valid_transition_emergent_to_noticed(self):
        """EMERGENT -> NOTICED is a valid transition."""
        transition = LifecycleTransition(
            from_state=LifecycleState.EMERGENT, to_state=LifecycleState.NOTICED
        )
        assert transition.is_valid()

    def test_invalid_transition_ratified_to_emergent(self):
        """RATIFIED -> EMERGENT is invalid (no backward)."""
        transition = LifecycleTransition(
            from_state=LifecycleState.RATIFIED, to_state=LifecycleState.EMERGENT
        )
        assert not transition.is_valid()

    def test_composted_is_terminal(self):
        """COMPOSTED has no valid transitions (terminal state)."""
        for state in LifecycleState:
            if state != LifecycleState.COMPOSTED:
                transition = LifecycleTransition(
                    from_state=LifecycleState.COMPOSTED, to_state=state
                )
                assert not transition.is_valid(), f"COMPOSTED -> {state} should be invalid"
