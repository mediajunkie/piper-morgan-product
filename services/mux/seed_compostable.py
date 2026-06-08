"""Synthetic lifecycle-bearing object for exercising the composting path on demand.

Issue #1143 slice 2 (COMPOSTING-DEV-TRIGGER seed affordance). The compost bin is
in-memory and, on a fresh process, empty — so a ``/trigger`` cycle has nothing to
compost and #1033 (MUX-COMPOSTED-EXPERIENCE) / #1035 (MUX-COMPOSTING-ACTIVATION)
can't be observed in a UAT-style smoke test.

This module builds a synthetic object satisfying the composting extractor's
expected surface (the ``HasLifecycle`` protocol — ``lifecycle_state`` +
``lifecycle_history`` — plus the summary attributes the extractor preserves) with
a *full* journey (EMERGENT → … → RATIFIED → DEPRECATED → ARCHIVED). That journey
yields the extractor's "completed a full lifecycle" + "successfully ratified"
lessons at high confidence, so a composting cycle produces a real
``SurfaceableInsight`` the surfacing path can later frame.

DEV/TEST infrastructure only — not wired into any production trigger.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List

from services.mux.lifecycle import LifecycleState, LifecycleTransition

# A realistic maturation-then-retirement journey: an idea that emerged, was
# derived/noticed, formally proposed, ratified into active use, then deprecated
# and archived as it aged out — exactly the kind of object ready to compost.
# Length 7 (>= the extractor's "full lifecycle" threshold) and passes through
# RATIFIED (the extractor's "validated" bonus).
_SEED_JOURNEY: List[LifecycleState] = [
    LifecycleState.EMERGENT,
    LifecycleState.DERIVED,
    LifecycleState.NOTICED,
    LifecycleState.PROPOSED,
    LifecycleState.RATIFIED,
    LifecycleState.DEPRECATED,
    LifecycleState.ARCHIVED,
]


@dataclass
class SeedCompostable:
    """Minimal object implementing the composting extractor's expected surface.

    Carries the ``CompostingExtractor.SUMMARY_ATTRIBUTES`` it preserves
    (id/title/description/type/category/created_at/updated_at) plus the lifecycle
    surface it reads (``lifecycle_state`` + ``lifecycle_history``).
    """

    id: str
    title: str
    description: str = (
        "Synthetic seed object for composting UAT (#1143 slice 2). Walks a full "
        "lifecycle so the extractor has wisdom to compost."
    )
    type: str = "seed_demo_object"
    category: str = "dev_seed"
    created_at: datetime = field(
        default_factory=lambda: datetime.now() - timedelta(days=120)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now() - timedelta(days=35)
    )
    lifecycle_state: LifecycleState = LifecycleState.ARCHIVED
    lifecycle_history: List[LifecycleTransition] = field(default_factory=list)


def make_seed_compostable(
    object_id: str, title: str = "Alpha testing approach"
) -> SeedCompostable:
    """Build a synthetic full-journey compostable object.

    The history walks the canonical maturation-then-retirement path so the
    extractor yields the "completed a full lifecycle" + "successfully ratified"
    lessons at high confidence — enough to produce a surfaceable insight.

    Args:
        object_id: Unique id for the seeded object (also the insight's source id).
        title: Human-readable title preserved in the object summary.

    Returns:
        A ``SeedCompostable`` ready to drop into a ``CompostBin``.
    """
    history = [
        LifecycleTransition(
            from_state=_SEED_JOURNEY[i],
            to_state=_SEED_JOURNEY[i + 1],
            reason="seed-demo synthetic transition",
        )
        for i in range(len(_SEED_JOURNEY) - 1)
    ]
    return SeedCompostable(
        id=object_id,
        title=title,
        lifecycle_history=history,
        lifecycle_state=_SEED_JOURNEY[-1],
    )
