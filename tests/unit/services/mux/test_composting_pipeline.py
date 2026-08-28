"""
Tests for CompostingPipeline - wires Extractor to InsightJournal.

Part of #667 COMPOSTING-PIPELINE (child of #436 MUX-TECH-PHASE4-COMPOSTING).
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List

import pytest

from services.mux.composting_models import (
    CompostingTrigger,
    ExtractedLearning,
    create_insight_learning,
)
from services.mux.composting_pipeline import CompostingPipeline, InsightJournal, SurfaceableInsight
from services.mux.lifecycle import LifecycleState

# #1035: InsightJournal is now repository-backed and async; tests use the
# in-memory FakeInsightJournal as a test double for testing OTHER classes
# (CompostingPipeline) without a DB. The InsightJournal contract itself is
# verified by InsightRepository tests at test_insight_repository_1035.py.
from tests.unit.services.mux._fake_insight_journal import FakeInsightJournal

# =============================================================================
# Test Fixtures
# =============================================================================


@dataclass
class MockObjectWithLifecycle:
    """Mock object for testing."""

    id: str
    title: str
    created_at: datetime = field(default_factory=datetime.now)
    lifecycle_state: LifecycleState = LifecycleState.EMERGENT
    lifecycle_history: List = field(default_factory=list)


# =============================================================================
# SurfaceableInsight Tests
# =============================================================================


class TestSurfaceableInsight:
    """Tests for SurfaceableInsight model."""

    def test_basic_creation(self):
        """Test basic insight creation."""
        insight = SurfaceableInsight(
            object_id="obj-123",
            user_id="user-456",
        )
        assert insight.id is not None
        assert insight.object_id == "obj-123"
        assert insight.user_id == "user-456"
        assert insight.surfaced_count == 0

    def test_with_learning(self):
        """Test insight with ExtractedLearning."""
        learning = create_insight_learning(
            description="User prefers mornings",
            derived_from=["pattern-1"],
            confidence=0.8,
        )
        insight = SurfaceableInsight(
            object_id="obj-123",
            learning=learning,
        )
        assert insight.learning is not None
        assert insight.learning_type == "insight"
        assert insight.is_high_confidence is True  # 0.8 >= 0.75

    def test_is_surfaceable_with_trust(self):
        """Test surfaceability check with trust levels."""
        insight = SurfaceableInsight(
            min_trust_stage=3,
        )

        # Below trust threshold
        assert insight.is_surfaceable(trust_stage=1) is False
        assert insight.is_surfaceable(trust_stage=2) is False

        # At or above threshold
        assert insight.is_surfaceable(trust_stage=3) is True
        assert insight.is_surfaceable(trust_stage=4) is True

    def test_is_surfaceable_cooldown(self):
        """Test that recently surfaced insights have cooldown."""
        insight = SurfaceableInsight(
            last_surfaced=datetime.now(),  # Just surfaced
        )

        # Should not be surfaceable due to 24h cooldown
        assert insight.is_surfaceable(trust_stage=4) is False

    def test_is_surfaceable_dismissed(self):
        """Test that dismissed insights are not surfaceable."""
        insight = SurfaceableInsight(
            user_response="dismissed",
        )

        assert insight.is_surfaceable(trust_stage=4) is False

    def test_to_dict_and_from_dict(self):
        """Test serialization roundtrip."""
        learning = create_insight_learning(
            description="Test insight",
            derived_from=[],
            confidence=0.7,
        )
        original = SurfaceableInsight(
            object_id="obj-1",
            user_id="user-1",
            learning=learning,
            min_trust_stage=2,
            context_tags=["scheduling"],
        )

        restored = SurfaceableInsight.from_dict(original.to_dict())

        assert restored.object_id == original.object_id
        assert restored.user_id == original.user_id
        assert restored.min_trust_stage == original.min_trust_stage
        assert restored.context_tags == original.context_tags
        assert restored.learning is not None
        assert restored.learning.description == "Test insight"


# =============================================================================
# InsightJournal Tests
# =============================================================================


@pytest.mark.asyncio
class TestInsightJournalInterface:
    """Interface contract tests using FakeInsightJournal test double.

    Production InsightJournal (repository-backed) semantics are verified
    by InsightRepository tests in test_insight_repository_1035.py. This
    class verifies the journal interface contract that both production and
    fake implementations honor.
    """

    async def test_add_and_get(self):
        journal = FakeInsightJournal()

        insight = SurfaceableInsight(
            id="insight-1",
            object_id="obj-1",
            user_id="user-1",
        )
        await journal.add(insight)

        retrieved = await journal.get("insight-1")
        assert retrieved is not None
        assert retrieved.object_id == "obj-1"

    async def test_count(self):
        journal = FakeInsightJournal()

        assert await journal.count() == 0

        await journal.add(SurfaceableInsight(id="i1"))
        await journal.add(SurfaceableInsight(id="i2"))
        await journal.add(SurfaceableInsight(id="i3"))

        assert await journal.count() == 3

    async def test_clear_per_user(self):
        """Per-user clear (#1035 Q6: clear is per-user only, not system-wide)."""
        journal = FakeInsightJournal()
        await journal.add(SurfaceableInsight(id="i1", user_id="alice"))
        await journal.add(SurfaceableInsight(id="i2", user_id="alice"))
        await journal.add(SurfaceableInsight(id="i3", user_id="bob"))

        cleared = await journal.clear(user_id="alice")

        assert cleared == 2
        assert await journal.count(user_id="alice") == 0
        # Bob's data is preserved
        assert await journal.count(user_id="bob") == 1

    async def test_get_unsurfaced(self):
        journal = FakeInsightJournal()

        high_confidence = SurfaceableInsight(
            id="high",
            user_id="user-1",
            learning=create_insight_learning(
                description="High confidence",
                derived_from=[],
                confidence=0.9,
            ),
        )
        low_confidence = SurfaceableInsight(
            id="low",
            user_id="user-1",
            learning=create_insight_learning(
                description="Low confidence",
                derived_from=[],
                confidence=0.5,
            ),
        )
        already_surfaced = SurfaceableInsight(
            id="surfaced",
            user_id="user-1",
            learning=create_insight_learning(
                description="Already surfaced",
                derived_from=[],
                confidence=0.9,
            ),
            surfaced_count=1,
        )

        await journal.add(high_confidence)
        await journal.add(low_confidence)
        await journal.add(already_surfaced)

        results = await journal.get_unsurfaced(
            user_id="user-1",
            min_confidence=0.75,
        )

        assert len(results) == 1
        assert results[0].id == "high"

    async def test_get_unsurfaced_respects_trust(self):
        journal = FakeInsightJournal()

        insight = SurfaceableInsight(
            id="high-trust",
            user_id="user-1",
            min_trust_stage=3,
            learning=create_insight_learning(
                description="Needs high trust",
                derived_from=[],
                confidence=0.9,
            ),
        )
        await journal.add(insight)

        results = await journal.get_unsurfaced(
            user_id="user-1",
            trust_stage=2,
        )
        assert len(results) == 0

        results = await journal.get_unsurfaced(
            user_id="user-1",
            trust_stage=3,
        )
        assert len(results) == 1

    async def test_get_for_context(self):
        journal = FakeInsightJournal()

        scheduling_insight = SurfaceableInsight(
            id="scheduling",
            user_id="user-1",
            learning=create_insight_learning(
                description="Morning meetings preferred",
                derived_from=[],
                confidence=0.8,
            ),
        )
        scheduling_insight.learning.topic_tags = ["scheduling", "meetings"]
        scheduling_insight.learning.applies_to_entities = ["calendar"]

        comms_insight = SurfaceableInsight(
            id="comms",
            user_id="user-1",
            learning=create_insight_learning(
                description="Prefers Slack",
                derived_from=[],
                confidence=0.8,
            ),
        )
        comms_insight.learning.topic_tags = ["communication"]
        comms_insight.learning.applies_to_entities = ["slack"]

        await journal.add(scheduling_insight)
        await journal.add(comms_insight)

        results = await journal.get_for_context(
            user_id="user-1",
            context_entities=["calendar"],
            context_topics=["meetings"],
        )

        assert len(results) >= 1
        assert results[0].id == "scheduling"

    async def test_mark_surfaced(self):
        journal = FakeInsightJournal()

        insight = SurfaceableInsight(
            id="insight-1",
            user_id="user-1",
        )
        await journal.add(insight)

        updated = await journal.mark_surfaced("insight-1", "engaged")

        assert updated is not None
        assert updated.surfaced_count == 1
        assert updated.last_surfaced is not None
        assert updated.user_response == "engaged"

    async def test_get_for_object(self):
        journal = FakeInsightJournal()

        await journal.add(SurfaceableInsight(id="i1", object_id="obj-1"))
        await journal.add(SurfaceableInsight(id="i2", object_id="obj-1"))
        await journal.add(SurfaceableInsight(id="i3", object_id="obj-2"))

        results = await journal.get_for_object("obj-1")

        assert len(results) == 2
        assert all(i.object_id == "obj-1" for i in results)


# =============================================================================
# CompostingPipeline Tests
# =============================================================================


class TestCompostingPipeline:
    """Tests for CompostingPipeline orchestration."""

    def test_creation_with_defaults(self):
        """Test pipeline creation with default components."""
        pipeline = CompostingPipeline()

        assert pipeline.extractor is not None
        assert pipeline.journal is not None

    @pytest.mark.asyncio
    async def test_process_simple_object(self):
        """Test processing a simple object."""
        # #1035: pass FakeInsightJournal so test doesn't require DB
        fake_journal = FakeInsightJournal()
        pipeline = CompostingPipeline(journal=fake_journal)

        obj = MockObjectWithLifecycle(
            id="task-1",
            title="Test Task",
            lifecycle_state=LifecycleState.ARCHIVED,
        )

        learnings = await pipeline.process(obj, user_id="user-1")

        # Should extract at least one learning
        assert len(learnings) >= 1

        # Should store in journal
        assert await fake_journal.count() >= 1

    @pytest.mark.asyncio
    async def test_process_stores_with_user_id(self):
        """Test that processed insights are stored with user_id."""
        fake_journal = FakeInsightJournal()
        pipeline = CompostingPipeline(journal=fake_journal)

        obj = MockObjectWithLifecycle(
            id="task-1",
            title="Test",
        )

        await pipeline.process(obj, user_id="user-123")

        insights = await fake_journal.get_for_object("task-1")
        assert len(insights) >= 1
        assert all(i.user_id == "user-123" for i in insights)

    @pytest.mark.asyncio
    async def test_process_calculates_confidence(self):
        """Test that confidence is calculated from journey."""
        from services.mux.lifecycle import LifecycleTransition

        pipeline = CompostingPipeline(journal=FakeInsightJournal())

        # Object with long journey including RATIFIED
        obj = MockObjectWithLifecycle(
            id="task-1",
            title="Well-traveled",
            lifecycle_state=LifecycleState.ARCHIVED,
            lifecycle_history=[
                LifecycleTransition(
                    from_state=LifecycleState.EMERGENT,
                    to_state=LifecycleState.DERIVED,
                ),
                LifecycleTransition(
                    from_state=LifecycleState.DERIVED,
                    to_state=LifecycleState.NOTICED,
                ),
                LifecycleTransition(
                    from_state=LifecycleState.NOTICED,
                    to_state=LifecycleState.PROPOSED,
                ),
                LifecycleTransition(
                    from_state=LifecycleState.PROPOSED,
                    to_state=LifecycleState.RATIFIED,
                ),
            ],
        )

        learnings = await pipeline.process(obj, user_id="user-1")

        # With RATIFIED in journey, confidence should be boosted
        assert len(learnings) >= 1
        # Confidence should be higher due to journey + RATIFIED bonus
        assert learnings[0].confidence >= 0.7

    @pytest.mark.asyncio
    async def test_process_extracts_topic_tags(self):
        """Test that topic tags are extracted from object summary."""
        pipeline = CompostingPipeline(journal=FakeInsightJournal())

        obj = MockObjectWithLifecycle(
            id="task-1",
            title="Test",
        )
        # Add type for topic extraction
        obj.type = "feature"
        obj.category = "planning"

        learnings = await pipeline.process(obj, user_id="user-1")

        # Should have extracted topic tags
        assert len(learnings) >= 1


class TestCompostingPipelineLessonClassification:
    """Tests for lesson to learning type classification."""

    @pytest.mark.asyncio
    async def test_correction_detection(self):
        """Test that correction signals create Correction learnings."""
        pipeline = CompostingPipeline()

        # Create mock result with correction-like lesson
        from services.mux.lifecycle import CompostResult

        mock_result = CompostResult(
            object_summary={"id": "obj-1"},
            journey=[LifecycleState.EMERGENT],
            lessons=["This was wrong - user actually prefers afternoon meetings"],
            composted_at=datetime.now(),
        )

        learnings = pipeline._to_extracted_learnings(mock_result, None)

        assert len(learnings) == 1
        assert learnings[0].learning_type == "correction"

    @pytest.mark.asyncio
    async def test_pattern_detection(self):
        """Test that pattern signals create Pattern learnings."""
        pipeline = CompostingPipeline()

        from services.mux.lifecycle import CompostResult

        mock_result = CompostResult(
            object_summary={"id": "obj-1"},
            journey=[LifecycleState.EMERGENT],
            lessons=["This object completed a full lifecycle - patterns are worth studying"],
            composted_at=datetime.now(),
        )

        learnings = pipeline._to_extracted_learnings(mock_result, None)

        assert len(learnings) == 1
        assert learnings[0].learning_type == "pattern"

    @pytest.mark.asyncio
    async def test_default_to_insight(self):
        """Test that generic lessons become Insight learnings."""
        pipeline = CompostingPipeline()

        from services.mux.lifecycle import CompostResult

        mock_result = CompostResult(
            object_summary={"id": "obj-1"},
            journey=[LifecycleState.EMERGENT],
            lessons=["Every object teaches something through its existence"],
            composted_at=datetime.now(),
        )

        learnings = pipeline._to_extracted_learnings(mock_result, None)

        assert len(learnings) == 1
        assert learnings[0].learning_type == "insight"


class TestCompostingPipelineTrustStages:
    """Tests for trust stage determination."""

    def test_correction_requires_high_trust(self):
        """Test that corrections require trust stage 3."""
        pipeline = CompostingPipeline()

        from services.mux.composting_models import create_correction_learning

        learning = create_correction_learning(
            previous_understanding="Old",
            new_understanding="New",
            evidence=[],
        )

        trust = pipeline._determine_trust_stage(learning)
        assert trust == 3

    def test_high_confidence_allows_push(self):
        """Test that high confidence insights get stage 2."""
        pipeline = CompostingPipeline()

        learning = create_insight_learning(
            description="High confidence insight",
            derived_from=[],
            confidence=0.9,
        )

        trust = pipeline._determine_trust_stage(learning)
        assert trust == 2

    def test_low_confidence_pull_only(self):
        """Test that low confidence insights are stage 1."""
        pipeline = CompostingPipeline()

        learning = create_insight_learning(
            description="Low confidence insight",
            derived_from=[],
            confidence=0.5,
        )

        trust = pipeline._determine_trust_stage(learning)
        assert trust == 1
