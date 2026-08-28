"""#1238 RADAR-DOC-SOURCE — DocumentEntitySource + per-source isolation + compose (TDD).

Covers: DocumentService rows → Document RadarEntities (observed, recency lifecycle,
honest meta, ref=base_id); per-source isolation (a failing source never blanks Radar);
and Conversation + Document composing attention-first. Mirrors test_radar_domain.py.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from services.radar import (
    ConversationEntitySource,
    DocumentEntitySource,
    EntityType,
    Provenance,
    RadarEntity,
    RadarFeed,
)


def _obs(title: str, attention: float) -> RadarEntity:
    return RadarEntity(
        entity_type=EntityType.WORK_ITEM,
        title=title,
        lifecycle_state="active",
        provenance=Provenance.OBSERVED,
        attention=attention,
    )


class _FakeSource:
    def __init__(self, entities):
        self._entities = entities

    async def fetch(self, user_id):
        return self._entities


class _BoomSource:
    async def fetch(self, user_id):
        raise RuntimeError("source down")


class _FakeDocs:
    def __init__(self, rows):
        self._rows = rows

    async def list_for_user(self, user_id):
        return self._rows


class _FakeHistory:
    def __init__(self, summaries):
        self._summaries = summaries

    async def list_summaries(self, user_id):
        return self._summaries


# --- DocumentEntitySource mapping ---


async def test_document_source_maps_doc_as_observed():
    now_iso = datetime.now(timezone.utc).isoformat()
    rows = [
        {
            "chromadb_base_id": "pdf_1",
            "title": "Spec",
            "source": "/docs/spec.pdf",
            "created_at": now_iso,
            "updated_at": now_iso,
        }
    ]
    entities = await DocumentEntitySource(_FakeDocs(rows)).fetch("u1")
    assert len(entities) == 1
    e = entities[0]
    assert e.entity_type == EntityType.DOCUMENT
    assert e.title == "Spec"
    assert e.provenance == Provenance.OBSERVED  # a user's real document
    assert e.lifecycle_state == "new"  # recent updated_at
    assert e.ref == "pdf_1"
    assert "spec.pdf" in e.meta  # filename, not full path


async def test_document_source_recent_then_stale():
    recent = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
    old = "2020-01-01T00:00:00+00:00"
    recent_e = (
        await DocumentEntitySource(
            _FakeDocs([{"chromadb_base_id": "r", "title": "R", "updated_at": recent}])
        ).fetch("u1")
    )[0]
    old_e = (
        await DocumentEntitySource(
            _FakeDocs([{"chromadb_base_id": "o", "title": "O", "updated_at": old}])
        ).fetch("u1")
    )[0]
    assert recent_e.lifecycle_state == "recent"
    assert old_e.lifecycle_state == "stale"


async def test_document_source_untitled_fallback_and_empty():
    e = (
        await DocumentEntitySource(
            _FakeDocs([{"chromadb_base_id": "x", "title": None, "updated_at": None}])
        ).fetch("u1")
    )[0]
    assert e.title == "(untitled document)"
    assert await DocumentEntitySource(_FakeDocs([])).fetch("u1") == []


# --- per-source isolation (AC: a failing source never blanks Radar) ---


async def test_failing_source_does_not_blank_radar():
    view = await RadarFeed([_BoomSource(), _FakeSource([_obs("survivor", 5.0)])]).assemble("u1")
    assert view.state == "populated"
    # [:-1]: the populated view ends with the #1635 coming-soon placeholder
    assert [e.title for e in view.entities[:-1]] == ["survivor"]


async def test_all_sources_failing_falls_back_to_empty_example():
    view = await RadarFeed([_BoomSource(), _BoomSource()]).assemble("u1")
    assert view.state == "empty"
    assert view.entities[0].provenance == Provenance.EXAMPLE


# --- multi-source compose (Conversation + Document, attention-first) ---


async def test_conversation_and_document_compose_attention_first():
    now_iso = datetime.now(timezone.utc).isoformat()
    older_iso = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
    conv = ConversationEntitySource(
        _FakeHistory(
            [
                {
                    "conversation_id": "c1",
                    "title": "chat",
                    "last_activity": older_iso,
                    "turn_count": 2,
                }
            ]
        )
    )
    docs = DocumentEntitySource(
        _FakeDocs(
            [
                {
                    "chromadb_base_id": "pdf_1",
                    "title": "fresh doc",
                    "source": None,
                    "updated_at": now_iso,
                }
            ]
        )
    )
    view = await RadarFeed([conv, docs]).assemble("u1")
    assert view.state == "populated"
    types = {e.entity_type for e in view.entities}
    assert {EntityType.CONVERSATION, EntityType.DOCUMENT} <= types
    # the more-recently-touched document sorts ahead of the older conversation
    assert view.entities[0].entity_type == EntityType.DOCUMENT
    assert view.entities[0].title == "fresh doc"
