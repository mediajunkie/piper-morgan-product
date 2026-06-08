"""Tests for the #1143 slice-2 composting seed affordance.

The dev seed endpoint (web/routers/dev_composting.py ``POST /seed``) relies on a
synthetic full-journey object flowing all the way through the composting path:

    make_seed_compostable() -> CompostBin.add() -> CompostingScheduler.run(force=True)
        -> CompostingExtractor.extract() -> learnings -> InsightJournal.add()

These tests verify that path without HTTP or a DB (using the FakeInsightJournal
test double), so a regression in the seed object's shape — or in the extractor's
expectations of it — fails loudly rather than silently writing zero insights.
"""

import pytest

from services.mux.compost_bin import CompostBin
from services.mux.composting_models import CompostingTrigger
from services.mux.composting_pipeline import CompostingPipeline
from services.mux.lifecycle import (
    CompostingExtractor,
    LifecycleState,
)
from services.mux.seed_compostable import make_seed_compostable
from tests.unit.services.mux._fake_insight_journal import FakeInsightJournal


class TestSeedCompostableShape:
    """The synthetic object must satisfy the extractor's expected surface."""

    def test_full_journey_reaches_ratified_then_archived(self):
        obj = make_seed_compostable("seed-1", title="Alpha testing approach")
        assert obj.id == "seed-1"
        assert obj.title == "Alpha testing approach"
        # Current state is the end of the maturation-then-retirement walk.
        assert obj.lifecycle_state == LifecycleState.ARCHIVED
        # 7-state journey => 6 transitions.
        assert len(obj.lifecycle_history) == 6
        # Summary attributes the extractor preserves are present.
        for attr in ("id", "title", "description", "type", "category"):
            assert hasattr(obj, attr)

    def test_extractor_yields_full_lifecycle_and_ratified_lessons(self):
        obj = make_seed_compostable("seed-2")
        result = CompostingExtractor().extract(obj)

        # Journey rebuilt from history: 7 states, passing through RATIFIED.
        assert len(result.journey) == 7
        assert LifecycleState.RATIFIED in result.journey

        joined = " ".join(result.lessons).lower()
        # The two lessons the seed is designed to trigger:
        assert "full lifecycle" in joined
        assert "ratified" in joined or "validated" in joined


class TestSeedComposteEndToEnd:
    """seed -> bin -> scheduler.run(force=True) -> journal write path."""

    @pytest.mark.asyncio
    async def test_seeded_object_composts_and_writes_insight(self):
        journal = FakeInsightJournal()
        pipeline = CompostingPipeline(journal=journal)

        # Build the scheduler the same way startup.py does, but with the fake
        # journal so no DB session is needed.
        from services.mux.composting_scheduler import (
            CompostingSchedule,
            CompostingScheduler,
        )

        bin_ = CompostBin()
        scheduler = CompostingScheduler(
            compost_bin=bin_,
            pipeline=pipeline,
            schedule=CompostingSchedule(),
        )

        seed = make_seed_compostable("seed-e2e-1")
        bin_.add(
            seed,
            CompostingTrigger.MANUAL,
            object_type="seed_demo_object",
            priority=5,
        )
        assert len(bin_.pending) == 1

        result = await scheduler.run(force=True, user_id="u-test")

        # Cycle processed the seed and wrote learnings.
        assert result.processed_count == 1
        assert result.learnings_extracted >= 1
        assert result.errors == []
        # Bin drained after successful processing.
        assert len(bin_.pending) == 0

        # The insight is retrievable by the seed's object_id and carries framed,
        # non-empty learning text (frame_learning runs in the cycle).
        insights = await journal.get_for_object("seed-e2e-1")
        assert len(insights) >= 1
        first = insights[0]
        assert first.user_id == "u-test"
        assert first.learning is not None
        assert isinstance(first.learning.expression, str)
        assert first.learning.expression.strip() != ""

    @pytest.mark.asyncio
    async def test_empty_bin_force_run_writes_nothing(self):
        """Control: force-run with an empty bin writes no insights (so a positive
        result in the test above is attributable to the seed, not ambient state)."""
        journal = FakeInsightJournal()
        from services.mux.composting_scheduler import (
            CompostingSchedule,
            CompostingScheduler,
        )

        scheduler = CompostingScheduler(
            compost_bin=CompostBin(),
            pipeline=CompostingPipeline(journal=journal),
            schedule=CompostingSchedule(),
        )

        result = await scheduler.run(force=True, user_id="u-test")
        assert result.processed_count == 0
        assert result.learnings_extracted == 0
