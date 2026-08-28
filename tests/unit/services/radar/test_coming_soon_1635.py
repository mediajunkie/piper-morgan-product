"""#1635 — ambient-presence "coming soon" placeholder as a Radar card.

Pins CXO's two binding rules (design memo 2026-08-27) and the copy VERBATIM as
string literals (grep-able copy-drift protection, per the 8/21 lesson):

Rule 1 — placement: the placeholder renders at the BOTTOM of the Radar feed, below
every real entity, never pinned, never attention-ordered — and is SUPPRESSED
entirely when Radar has zero real entities (the FTUX/empty-state path owns the
empty moment; a placeholder faking fullness would be display-side fabrication).

Rule 2 — copy claims the FUTURE, never the present. "not watching anything yet"
is load-bearing: the card is self-honest on its face, in copy.

Layer note (m-43): these tests cover the domain assembly (RadarFeed) and the API
serialization (get_radar) — the layers that decide placement, suppression, and
copy. The JS renderer's example-class mapping is asserted through the template
render path in tests/unit/templates/test_history_sidebar.py (#1635 class there).

No OLD ambient-presence placeholder copy exists to assert against — grepped
templates/, web/, services/ 2026-08-28; the surface had zero prior ambient-
presence signal (that absence is what #1635 fixes).
"""

from __future__ import annotations

from types import SimpleNamespace

from services.radar import EntityType, Provenance, RadarEntity, RadarFeed

# CXO's strings, verbatim — the memo is BINDING on copy. Do not edit these
# literals without a new CXO ruling; the whole point is that drift fails here.
TITLE_1635 = "Piper will be able to watch for changes and bring you what matters"
META_1635 = (
    "Coming soon — not watching anything yet. "
    "Briefings when something needs you, not notification noise."
)
PILL_1635 = "coming soon"
LIFECYCLE_1635 = "preview"


def _obs(title: str, attention: float, pinned: bool = False) -> RadarEntity:
    return RadarEntity(
        entity_type=EntityType.WORK_ITEM,
        title=title,
        lifecycle_state="active",
        provenance=Provenance.OBSERVED,
        attention=attention,
        pinned=pinned,
    )


class _FakeSource:
    def __init__(self, entities):
        self._entities = entities

    async def fetch(self, user_id):
        return self._entities


def _is_placeholder(e: RadarEntity) -> bool:
    return e.entity_type == EntityType.COMING_SOON


# --- Rule 1: suppression pinned BOTH ways ---


async def test_zero_real_entities_suppresses_placeholder_entirely():
    """Empty Radar → empty state only (the teaching example), NO coming-soon card."""
    view = await RadarFeed([_FakeSource([])]).assemble("u1")
    assert view.state == "empty"
    assert not any(_is_placeholder(e) for e in view.entities)
    # and none of the empty-state copy is the 1635 copy
    assert all(e.title != TITLE_1635 for e in view.entities)


async def test_zero_observed_entities_also_suppresses_placeholder():
    """Seed/dev entities don't count as real — still the empty state, no placeholder."""
    seed = RadarEntity(EntityType.WORK_ITEM, "seed", "active", Provenance.SEED, attention=9.0)
    view = await RadarFeed([_FakeSource([seed])]).assemble("u1")
    assert view.state == "empty"
    assert not any(_is_placeholder(e) for e in view.entities)


async def test_one_real_entity_renders_placeholder_last():
    """≥1 real entity → placeholder present, exactly once, LAST."""
    view = await RadarFeed([_FakeSource([_obs("real thing", 1.0)])]).assemble("u1")
    assert view.state == "populated"
    assert [_is_placeholder(e) for e in view.entities] == [False, True]


async def test_placeholder_is_below_every_real_entity_never_attention_ordered():
    """Even zero-attention real entities sort ABOVE it; pinned entities stay at top."""
    entities = [_obs("cold", 0.0), _obs("hot", 9.0), _obs("reminder", 0.0, pinned=True)]
    view = await RadarFeed([_FakeSource(entities)]).assemble("u1")
    assert view.state == "populated"
    assert [e.title for e in view.entities[:-1]] == ["reminder", "hot", "cold"]
    last = view.entities[-1]
    assert _is_placeholder(last)
    assert last.pinned is False
    assert sum(_is_placeholder(e) for e in view.entities) == 1


async def test_placeholder_is_example_provenance_and_not_clickable():
    """EXAMPLE provenance drives the dashed radar-card--example style (visually
    distinct from real held state); no ref → the JS never makes it clickable."""
    view = await RadarFeed([_FakeSource([_obs("real", 1.0)])]).assemble("u1")
    last = view.entities[-1]
    assert last.provenance == Provenance.EXAMPLE
    assert last.ref is None


# --- Rule 2: the copy, verbatim, through the domain ---


async def test_placeholder_copy_is_cxo_strings_verbatim():
    view = await RadarFeed([_FakeSource([_obs("real", 1.0)])]).assemble("u1")
    last = view.entities[-1]
    assert last.title == TITLE_1635
    assert last.meta == META_1635
    assert last.entity_type.value == PILL_1635
    assert last.lifecycle_state == LIFECYCLE_1635
    # The future-tense honesty clauses, load-bearing per CXO:
    assert "will be able to" in last.title
    assert "not watching anything yet" in last.meta
    # No present-tense capability claim anywhere on the card:
    assert "is watching" not in (last.title + last.meta)


# --- Rule 2 through the API serialization (what the JS actually receives) ---


def _summary(cid, title, last_activity):
    return SimpleNamespace(
        conversation_id=cid,
        title=title,
        last_activity=last_activity,
        turn_count=2,
        topics=[],
        preview="...",
        is_private=False,
    )


class _FakeHistoryService:
    def __init__(self, conversations):
        self._conversations = conversations

    async def get_history(self, user_id, page, page_size, include_private):
        return SimpleNamespace(
            conversations=self._conversations,
            total_count=len(self._conversations),
            page=page,
            page_size=page_size,
            has_more=False,
        )


async def test_route_serializes_placeholder_last_with_exact_strings():
    from datetime import datetime, timezone

    from web.api.routes.radar import get_radar

    now = datetime.now(timezone.utc)
    svc = _FakeHistoryService([_summary("c1", "a real chat", now)])
    view = await get_radar(current_user=SimpleNamespace(sub="u1"), service=svc)
    assert view.state == "populated"
    last = view.entities[-1]
    assert last.entity_type == PILL_1635  # serialized enum .value — the pill text
    assert last.title == TITLE_1635
    assert last.meta == META_1635
    assert last.lifecycle_state == LIFECYCLE_1635
    assert last.provenance == "example"  # → radar-card--example (dashed) in the JS
    assert last.pinned is False
    assert last.ref is None
    # every entity above it is real/observed
    assert all(e.provenance == "observed" for e in view.entities[:-1])


async def test_route_empty_state_has_no_placeholder():
    from web.api.routes.radar import get_radar

    view = await get_radar(current_user=SimpleNamespace(sub="u1"), service=_FakeHistoryService([]))
    assert view.state == "empty"
    assert all(e.entity_type != PILL_1635 for e in view.entities)
    assert all(e.title != TITLE_1635 for e in view.entities)
