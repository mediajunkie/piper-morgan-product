"""Radar (Layer-2 entities-surfacing) domain — #1236 / #1090.

Value objects + view for the Radar surface (the history-sidebar slot-swap). The
vocabulary (entity types, lifecycle states) is ultimately PPM's entity-model lane
(#706); this module models the *surface* domain and renders whatever entity sources
provide. Built to the CXO mockup (radar-entities-surfacing-mockup-2026-06-14.html).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class EntityType(str, Enum):
    CONVERSATION = "Conversation"
    WORK_ITEM = "Work item"
    PERSON = "Person"
    DOCUMENT = "Document"


class Provenance(str, Enum):
    """Honest provenance (#1214/#1216). Only OBSERVED renders in the default view;
    EXAMPLE is the empty-state teaching card; SEED/dev data never claims to be real."""

    OBSERVED = "observed"  # ● real — Piper actually observed it
    EXAMPLE = "example"    # ○ illustrative — empty state only
    SEED = "seed"          # dev/seed — never rendered as observed


@dataclass(frozen=True)
class RadarEntity:
    """One card on the Radar. Value object — immutable."""

    entity_type: EntityType
    title: str
    lifecycle_state: str          # free-form for v1; vocabulary is PPM's (#706)
    provenance: Provenance
    meta: str = ""                # short context line ("last activity … · 5 turns")
    attention: float = 0.0        # ordering signal; higher = more attention (sorts first)
    ref: str | None = None        # link/target id


@dataclass(frozen=True)
class RadarView:
    """What the surface renders: a state + the cards for it."""

    state: str                    # "populated" | "empty"
    entities: list[RadarEntity] = field(default_factory=list)
