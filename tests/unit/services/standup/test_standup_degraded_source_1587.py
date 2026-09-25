"""#1587 — StandupAssembler/StandupSummary honestly disclose a FAILED EntitySource
read instead of rendering as if nothing happened.

Companion to test_standup_assembler_1269.py's existing per-source-isolation test
(a failing source never blanks the standup) — this file asserts the NEXT
property: a failure that #1587 makes distinguishable (EntitySourceReadFailed)
must actually be told to the user, not just swallowed into a log line. A
generic bug (plain Exception, pre-existing behavior) stays silent/isolated —
unchanged and out of scope for this issue.
"""

from __future__ import annotations

from services.domain.models import StandupSummary
from services.radar.models import EntityType, Provenance, RadarEntity
from services.radar.sources import EntitySourceReadFailed
from services.standup.assembler import StandupAssembler

NOW = 1_000_000_000.0


class _FailingSource:
    def __init__(self, label="your GitHub work items"):
        self._label = label

    async def fetch(self, user_id):
        raise EntitySourceReadFailed(self._label)


class _OkSource:
    def __init__(self, entities):
        self._entities = entities

    async def fetch(self, user_id):
        return list(self._entities)


class _BoomSource:
    """A generic, non-#1587 bug — must stay silent (pre-existing behavior)."""

    async def fetch(self, user_id):
        raise RuntimeError("unrelated bug")


def _doc(title, lifecycle="new"):
    return RadarEntity(
        entity_type=EntityType.DOCUMENT,
        title=title,
        lifecycle_state=lifecycle,
        provenance=Provenance.OBSERVED,
        attention=NOW,
    )


async def test_failed_source_recorded_in_degraded_sources():
    summary = await StandupAssembler(
        [_FailingSource(), _OkSource([_doc("a doc")])], now_epoch=NOW
    ).assemble("u1")
    assert summary.degraded_sources == ["your GitHub work items"]
    assert [it.display for it in summary.yesterday] == ["a doc"]


async def test_generic_exception_not_recorded_as_degraded():
    summary = await StandupAssembler(
        [_BoomSource(), _OkSource([_doc("a doc")])], now_epoch=NOW
    ).assemble("u1")
    assert summary.degraded_sources == []


async def test_to_prose_discloses_failure_alongside_real_content():
    summary = await StandupAssembler(
        [_FailingSource(), _OkSource([_doc("a doc")])], now_epoch=NOW
    ).assemble("u1")
    prose = summary.to_prose()
    assert "a doc" in prose  # real content still renders
    assert "couldn't reach" in prose.lower()
    assert "your GitHub work items" in prose


async def test_to_prose_never_says_nothing_to_show_when_everything_failed():
    """The core honesty property this issue exists for: when the ONLY source
    that would have populated the standup failed, the reply must say so
    plainly — never the "Nothing to show yet" all-clear over a read that
    never actually happened (GatherOutcome §4 rule 3)."""
    summary = await StandupAssembler([_FailingSource()], now_epoch=NOW).assemble("u1")
    assert summary.is_empty()
    prose = summary.to_prose()
    assert "nothing to show yet" not in prose.lower()
    assert "couldn't reach" in prose.lower()


async def test_to_prose_stays_unchanged_when_nothing_failed():
    """No degraded sources -> the original 'nothing to show yet' copy is
    untouched (regression guard against the new note leaking in)."""
    summary = await StandupAssembler([_OkSource([])], now_epoch=NOW).assemble("u1")
    assert summary.is_empty()
    prose = summary.to_prose()
    assert "nothing to show yet" in prose.lower()
    assert "couldn't reach" not in prose.lower()


def test_standup_summary_degraded_sources_defaults_empty():
    assert StandupSummary().degraded_sources == []


def test_standup_summary_to_dict_carries_degraded_sources():
    summary = StandupSummary(degraded_sources=["your GitHub work items"])
    assert summary.to_dict()["degraded_sources"] == ["your GitHub work items"]
