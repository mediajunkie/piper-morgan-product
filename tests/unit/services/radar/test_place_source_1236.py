"""#1236 — PlaceEntitySource maps Places → WorkItem RadarEntities (CXO mapping 2026-06-19).

The home "what i'm seeing" (Places) module is retired into the Radar. CXO's final call:
Places map onto the existing ``work_item`` type (no schema expansion for beta) with a
fixed ``active`` lifecycle, OBSERVED provenance (PlaceService only yields real connected
sources). Mirrors test_document_source_1238.py.
"""

from __future__ import annotations

from datetime import datetime, timezone

from services.radar import EntityType, PlaceEntitySource, Provenance, RadarFeed


class _FakePlaces:
    def __init__(self, rows):
        self._rows = rows

    async def list_for_user(self, user_id):
        return self._rows


async def test_place_source_maps_place_as_observed_work_item():
    now_iso = datetime.now(timezone.utc).isoformat()
    rows = [
        {
            "id": "github-acme/repo",
            "name": "acme/repo repository",
            "summary": "I see 3 open issues and 2 PRs waiting for review",
            "source_url": "https://github.com/acme/repo",
            "last_fetched": now_iso,
        }
    ]
    entities = await PlaceEntitySource(_FakePlaces(rows)).fetch("u1")
    assert len(entities) == 1
    e = entities[0]
    assert e.entity_type == EntityType.WORK_ITEM  # CXO: Places → work_item (no new type)
    assert e.title == "acme/repo repository"
    assert e.lifecycle_state == "active"  # CXO: fixed active/neutral
    assert e.provenance == Provenance.OBSERVED  # a real connected source
    assert "open issues" in e.meta  # the Place summary carries the context
    assert e.ref == "https://github.com/acme/repo"


async def test_place_source_untitled_fallback_ref_to_id_and_empty():
    e = (
        await PlaceEntitySource(
            _FakePlaces(
                [{"id": "calendar-today", "name": None, "summary": None, "source_url": None}]
            )
        ).fetch("u1")
    )[0]
    assert e.title == "(unnamed place)"
    assert e.ref == "calendar-today"  # falls back to id when no source_url
    assert await PlaceEntitySource(_FakePlaces([])).fetch("u1") == []


async def test_place_composes_into_radar_attention_first():
    now_iso = datetime.now(timezone.utc).isoformat()
    places = PlaceEntitySource(
        _FakePlaces(
            [
                {
                    "id": "p1",
                    "name": "your calendar",
                    "summary": "1 meeting today",
                    "last_fetched": now_iso,
                }
            ]
        )
    )
    view = await RadarFeed([places]).assemble("u1")
    assert view.state == "populated"
    assert view.entities[0].title == "your calendar"
    assert view.entities[0].entity_type == EntityType.WORK_ITEM
