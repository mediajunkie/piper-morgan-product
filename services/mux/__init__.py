# mux module - MUX-VISION Object Model Implementation
# Core grammar abstractions: Entity, Moment, Place protocols and perceptual lenses
#
# This module provides:
# - Protocols: EntityProtocol, MomentProtocol, PlaceProtocol (role-fluid substrates)
# - Situation: Async context manager for framing sequences of Moments
# - Perception: Result of perceiving through lenses (consciousness-preserving)
# - Lenses: 8 perceptual lenses mapping to 8D spatial dimensions
# - Ownership: 3-category model (NATIVE/FEDERATED/SYNTHETIC)
# - Lifecycle: 8-stage state machine with composting
#
# References:
# - ADR-045: Object Model Specification
# - ADR-055: Object Model Implementation
# - ADR-038: Spatial Intelligence Patterns

from .compost_bin import (
    CompostBin,
    CompostBinEntry,
    determine_trigger,
    meets_composting_criteria,
    on_lifecycle_archived,
    on_lifecycle_deprecated,
)
from .composting_models import (
    CompostingTrigger,
    Correction,
    ExtractedLearning,
    Insight,
    Pattern,
    create_correction_learning,
    create_insight_learning,
    create_pattern_learning,
)
from .composting_pipeline import CompostingPipeline, InsightJournal, SurfaceableInsight
from .composting_scheduler import (
    COMPOSTING_FRAMES,
    CompostingRunResult,
    CompostingSchedule,
    CompostingScheduler,
    frame_learning,
)
from .consciousness import (
    AwarenessLevel,
    Capability,
    ConsciousnessAttributes,
    ConsciousnessExpression,
    EmotionalState,
    EntityContext,
    EntityRole,
    PiperEntity,
    TrustLevel,
)
from .lifecycle import (
    VALID_TRANSITIONS,
    CompostingExtractor,
    CompostResult,
    HasLifecycle,
    InvalidTransitionError,
    LifecycleManager,
    LifecycleState,
    LifecycleTransition,
)
from .ownership import (
    HasOwnership,
    OwnershipCategory,
    OwnershipMetadata,
    OwnershipResolution,
    OwnershipResolver,
    OwnershipTransformation,
)
from .perception import Perception, PerceptionMode
from .premonition import (
    SURFACING_FRAMES,
    InsightReadiness,
    PremonitionService,
    SurfacingContext,
    frame_insight_for_surfacing,
    score_relevance,
)
from .protocols import EntityProtocol, MomentProtocol, PlaceProtocol, Target
from .situation import Situation, SituationLearning

__all__ = [
    # Protocols (substrates)
    "EntityProtocol",
    "MomentProtocol",
    "PlaceProtocol",
    "Target",
    # Situation (frame)
    "Situation",
    "SituationLearning",
    # Perception
    "Perception",
    "PerceptionMode",
    # Consciousness (#434)
    "AwarenessLevel",
    "Capability",
    "ConsciousnessAttributes",
    "ConsciousnessExpression",
    "EmotionalState",
    "EntityContext",
    "EntityRole",
    "PiperEntity",
    "TrustLevel",
    # Ownership (#435)
    "HasOwnership",
    "OwnershipCategory",
    "OwnershipMetadata",
    "OwnershipResolution",
    "OwnershipResolver",
    "OwnershipTransformation",
    # Lifecycle (P3)
    "CompostingExtractor",
    "CompostResult",
    "HasLifecycle",
    "InvalidTransitionError",
    "LifecycleManager",
    "LifecycleState",
    "LifecycleTransition",
    "VALID_TRANSITIONS",
    # Workspace Detection (#658)
    # Workspace Navigation (#659)
    # Workspace Isolation (#660)
    # Workspace Memory (#661)
    # Composting Models (#665)
    "CompostingTrigger",
    "Correction",
    "ExtractedLearning",
    "Insight",
    "Pattern",
    "create_correction_learning",
    "create_insight_learning",
    "create_pattern_learning",
    # Compost Bin (#666)
    "CompostBin",
    "CompostBinEntry",
    "determine_trigger",
    "meets_composting_criteria",
    "on_lifecycle_archived",
    "on_lifecycle_deprecated",
    # Composting Pipeline (#667)
    "CompostingPipeline",
    "InsightJournal",
    "SurfaceableInsight",
    # Composting Scheduler (#668)
    "COMPOSTING_FRAMES",
    "CompostingRunResult",
    "CompostingSchedule",
    "CompostingScheduler",
    "frame_learning",
    # Premonition (#415)
    "InsightReadiness",
    "PremonitionService",
    "SURFACING_FRAMES",
    "SurfacingContext",
    "frame_insight_for_surfacing",
    "score_relevance",
    # Moment UI (#418)
]
