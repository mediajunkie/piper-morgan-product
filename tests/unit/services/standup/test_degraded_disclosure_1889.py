"""#1889 — a source that genuinely FAILED (#1587) is disclosed on EVERY standup
surface and on the Radar, never rendered as all-clear.

CXO ruled the copy 2026-10-08 (memo: rule-cxo-to-lead-cc-ppm-1889-copy-ruled-…):
- one line, placed FIRST, one sentence for all failed sources;
- per format: chat / Slack / Markdown+text wording below;
- nothing at all to show + a failed source → the line WITHOUT its "so…" clause,
  then "I can't put together a standup right now — try again in a bit.", and NO
  section list under it, in every format;
- Radar: empty + failed → its own card, no example card; populated + failed (#1963)
  → the standup line above everything.
"""

from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from services.domain.models import StandupItem, StandupSummary, degraded_disclosure
from services.domain.standup_orchestration_service import _summary_to_result
from services.integrations.mcp.skills.standup_workflow_skill import (
    StandupWorkflowSkill,
    _summary_to_legacy_dict,
)
from services.radar.feed import RadarFeed
from services.radar.models import EntityType, Provenance, RadarEntity
from services.radar.sources import EntitySourceReadFailed
from web.api.routes.standup import format_standup, get_today_standup

GH = "your GitHub work items"
CAL = "your calendar"

EMPTY_TAIL = "I can't put together a standup right now — try again in a bit."

# The ruled strings, verbatim (CXO 2026-10-08).
PARTIAL = {
    "chat": "I couldn't reach your GitHub work items just now, so what's below is incomplete.",
    "slack": "_Couldn't reach your GitHub work items just now, so what's below is incomplete._",
    "markdown": "Note: couldn't reach your GitHub work items just now, so what's below is incomplete.",
    "text": "Note: couldn't reach your GitHub work items just now, so what's below is incomplete.",
}
EMPTY = {
    "chat": f"I couldn't reach your GitHub work items just now. {EMPTY_TAIL}",
    "slack": f"_Couldn't reach your GitHub work items just now. {EMPTY_TAIL}_",
    "markdown": f"Note: couldn't reach your GitHub work items just now. {EMPTY_TAIL}",
    "text": f"Note: couldn't reach your GitHub work items just now. {EMPTY_TAIL}",
}

# Words that would render an all-clear / empty section list under a failed read.
SECTION_WORDS = ("Yesterday", "Today", "Watch", "Blockers", "BLOCKERS", "None", "No blockers")


def _item(display):
    return StandupItem(display=display, source="work", lifecycle_state="active")


def _summary(*, failed=(GH,), items=True):
    return StandupSummary(
        today=[_item("Ship the thing")] if items else [],
        degraded_sources=list(failed),
    )


# --- the one wording helper -------------------------------------------------


@pytest.mark.parametrize("fmt", ["chat", "slack", "markdown", "text"])
def test_helper_partial_and_empty_wording(fmt):
    assert degraded_disclosure([GH], fmt) == PARTIAL[fmt]
    assert degraded_disclosure([GH], fmt, empty=True) == EMPTY[fmt]


def test_helper_is_plural_safe_one_sentence():
    line = degraded_disclosure([GH, CAL], "chat")
    assert line == (
        "I couldn't reach your GitHub work items and your calendar just now, "
        "so what's below is incomplete."
    )
    assert " it " not in line  # no pronoun to disagree with a plural


def test_helper_silent_when_nothing_failed():
    assert degraded_disclosure([], "chat") == ""
    assert degraded_disclosure([], "slack", empty=True) == ""


# --- chat prose ------------------------------------------------------------


def test_chat_prose_puts_the_line_first():
    prose = _summary().to_prose()
    assert prose.startswith(PARTIAL["chat"] + "\n\n")
    assert prose.count("couldn't reach") == 1  # once, not repeated at the end


def test_chat_prose_wholly_empty_is_the_line_alone():
    assert _summary(items=False).to_prose() == EMPTY["chat"]


def test_chat_prose_unchanged_when_nothing_failed():
    prose = _summary(failed=()).to_prose()
    assert "couldn't reach" not in prose
    assert prose.startswith("**Yesterday**")


# --- /generate formatters (StandupResult) ----------------------------------


def _result(**kw):
    return _summary_to_result(_summary(**kw), user_id="u1", generation_time_ms=5)


def test_adapter_carries_degraded_sources():
    assert _result().degraded_sources == [GH]
    assert format_standup(_result(), "json")["degraded_sources"] == [GH]


@pytest.mark.parametrize("fmt", ["slack", "markdown", "text"])
def test_generate_formats_disclose_before_the_sections(fmt):
    out = format_standup(_result(), fmt, "UTC")
    assert PARTIAL[fmt] in out
    first_section = min(i for i in (out.find("Yesterday"), out.find("YESTERDAY")) if i >= 0)
    assert out.index(PARTIAL[fmt]) < first_section


@pytest.mark.parametrize("fmt", ["slack", "markdown", "text"])
def test_generate_formats_wholly_empty_render_no_section_list(fmt):
    out = format_standup(_result(items=False), fmt, "UTC")
    assert EMPTY[fmt] in out
    for word in SECTION_WORDS:
        assert word not in out, f"{fmt}: {word!r} rendered under a failed read"


@pytest.mark.parametrize("fmt", ["slack", "markdown", "text"])
def test_generate_formats_unchanged_when_nothing_failed(fmt):
    out = format_standup(_result(failed=()), fmt, "UTC")
    assert "ouldn't reach" not in out


# --- the standup skill's own formatters ------------------------------------


def _skill():
    return StandupWorkflowSkill.__new__(StandupWorkflowSkill)  # formatters need no deps


def test_skill_adapter_carries_degraded_sources():
    assert _summary_to_legacy_dict(_summary())["degraded_sources"] == [GH]


def test_skill_formats_disclose_first():
    d = _summary_to_legacy_dict(_summary())
    md = _skill()._format_as_markdown(d)["content"]
    plain = _skill()._format_as_plain_text(d)["content"]
    slack = _skill()._markdown_version(d)
    assert md.index(PARTIAL["markdown"]) < md.index("Yesterday")
    assert plain.index(PARTIAL["text"]) < plain.index("Yesterday")
    assert slack.startswith(PARTIAL["slack"] + "\n\n")


def test_skill_formats_wholly_empty_render_no_section_list():
    d = _summary_to_legacy_dict(_summary(items=False))
    md = _skill()._format_as_markdown(d)["content"]
    plain = _skill()._format_as_plain_text(d)["content"]
    slack = _skill()._markdown_version(d)
    assert md == f"# Daily Standup\n\n{EMPTY['markdown']}\n"
    assert plain == f"DAILY STANDUP\n\n{EMPTY['text']}\n"
    assert slack == EMPTY["slack"]


# --- /today (the /standup page's source) -----------------------------------


async def _today(summary):
    with patch(
        "services.standup.assembler.build_user_standup_summary",
        return_value=summary,
    ):
        return await get_today_standup(current_user=SimpleNamespace(sub="u1"))


async def test_today_carries_the_chat_disclosure():
    resp = await _today(_summary())
    assert resp.disclosure == PARTIAL["chat"]
    assert resp.summary["degraded_sources"] == [GH]
    assert resp.prose.startswith(PARTIAL["chat"])


async def test_today_wholly_empty_disclosure_is_the_empty_form():
    resp = await _today(_summary(items=False))
    assert resp.disclosure == EMPTY["chat"]


async def test_today_no_disclosure_when_nothing_failed():
    assert (await _today(_summary(failed=()))).disclosure == ""


# --- Radar -----------------------------------------------------------------


class _Failing:
    async def fetch(self, user_id):
        raise EntitySourceReadFailed(GH)


class _Empty:
    async def fetch(self, user_id):
        return []


class _One:
    async def fetch(self, user_id):
        return [
            RadarEntity(
                entity_type=EntityType.DOCUMENT,
                title="a doc",
                lifecycle_state="new",
                provenance=Provenance.OBSERVED,
                attention=datetime.now(timezone.utc).timestamp(),
            )
        ]


async def test_radar_empty_and_failed_drops_the_example_card():
    view = await RadarFeed([_Failing(), _Empty()]).assemble("u1")
    assert view.state == "empty"
    assert view.entities == []
    assert view.degraded_sources == [GH]


async def test_radar_empty_without_failure_keeps_the_example_card():
    view = await RadarFeed([_Empty()]).assemble("u1")
    assert view.state == "empty"
    assert len(view.entities) == 1


async def _radar_response(sources):
    from web.api.routes import radar as radar_route

    with patch.object(radar_route, "_build_feed", return_value=RadarFeed(sources)):
        return await radar_route.get_radar(current_user=SimpleNamespace(sub="u1"), service=None)


async def test_radar_route_renders_the_card_title_and_populated_note():
    empty = await _radar_response([_Failing()])
    assert empty.degraded_title == "I couldn't reach your GitHub work items just now."
    assert empty.degraded_note == ""  # each string only in its own state
    populated = await _radar_response([_Failing(), _One()])
    assert populated.degraded_note == PARTIAL["chat"]  # #1963: same line as the standup
    assert populated.degraded_title == ""


async def test_radar_route_silent_when_nothing_failed():
    resp = await _radar_response([_One()])
    assert resp.degraded_title == "" and resp.degraded_note == ""


# --- template copy pins (the browser render is the acceptance; these keep it) ---


@pytest.mark.parametrize(
    "path", ["templates/components/history_sidebar.html", "templates/home.html"]
)
def test_radar_templates_carry_the_ruled_card_and_no_refresh_promise(path):
    from pathlib import Path

    src = Path(__file__).resolve().parents[4].joinpath(path).read_text()
    flat = " ".join(src.replace('"\n', '"').split())
    for half in (
        "Your Radar may be missing what you're working on there. ",
        "An empty Radar doesn't mean all clear. Check back in a bit.",
    ):
        assert half in flat, f"{path}: CXO's card copy missing"
    assert "degraded_title" in src and "degraded_note" in src
    assert "refresh on its own" not in src  # CXO: no mechanism, no promise
