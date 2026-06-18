"""
#1034 — StandupItem structured-item wiring tests.

Verifies the gameplan-mandated invariant: the standup pipeline carries
structured per-item data (`StandupItem` dataclass) through to the API
response, so #704 (MUX-LIFECYCLE-UI-A) can read `lifecycle_state` per
item from the standup.html template.

Coverage:
- StandupItem dataclass roundtrip (str + to_dict)
- Producer (`MorningStandupWorkflow._generate_standup_content`) builds
  StandupItems with correct source/icon per data category
- StandupItems with `lifecycle_state` flow through to dict shape
- JSON formatter (`format_standup`) serializes to structured dicts
- Backwards-compat: slack/markdown/text formatters work via __str__

Mirrors the pattern at `tests/unit/services/test_insight_repository_1035.py`
in scope: thin, focused unit tests on the new schema's contract.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock

import pytest

from services.features.morning_standup import (
    MorningStandupWorkflow,
    StandupItem,
    StandupResult,
)


# =============================================================================
# StandupItem dataclass behavior
# =============================================================================


class TestStandupItem:
    """StandupItem dataclass behavior tests."""

    def test_str_returns_legacy_format(self):
        """str(item) returns the pre-#1034 emoji-prefix format."""
        item = StandupItem(display="commit message", icon="✅", source="commit")
        assert str(item) == "✅ commit message"

    def test_str_without_icon(self):
        """str(item) without icon returns bare display text."""
        item = StandupItem(display="bare text", icon="", source="other")
        assert str(item) == "bare text"

    def test_to_dict_carries_all_fields(self):
        item = StandupItem(
            display="audit_transparency Phase 2",
            source="work",
            lifecycle_state="ratified",
            icon="📋",
            meta="hasn't moved in 5 days",  # #1269: optional context line
        )
        d = item.to_dict()
        assert d == {
            "display": "audit_transparency Phase 2",
            "source": "work",
            "lifecycle_state": "ratified",
            "icon": "📋",
            "meta": "hasn't moved in 5 days",
        }

    def test_to_dict_with_no_lifecycle(self):
        item = StandupItem(display="commit", icon="✅", source="commit")
        d = item.to_dict()
        assert d["lifecycle_state"] is None


# =============================================================================
# Pipeline producer behavior
# =============================================================================


@pytest.mark.asyncio
async def test_pipeline_produces_structured_items_from_commits():
    """`_generate_standup_content` builds StandupItems from GitHub commits."""
    workflow = MorningStandupWorkflow(
        preference_manager=MagicMock(),
        session_manager=MagicMock(),
        github_domain_service=MagicMock(),
        user_id="alpha",
    )
    github_activity = {
        "commits": [{"message": "first commit"}, {"message": "second commit"}],
    }
    session_context = {}
    import time as time_module

    result = await workflow._generate_standup_content(
        user_id="alpha",
        session_context=session_context,
        github_activity=github_activity,
        start_time=time_module.time(),
    )

    assert len(result.yesterday_accomplishments) == 2
    for item in result.yesterday_accomplishments:
        assert isinstance(item, StandupItem)
        assert item.source == "commit"
        assert item.icon == "✅"
        assert item.lifecycle_state is None

    assert result.yesterday_accomplishments[0].display == "first commit"
    assert result.yesterday_accomplishments[1].display == "second commit"


@pytest.mark.asyncio
async def test_pipeline_produces_structured_items_from_work_items():
    """When session_context has yesterday_work, items carry source='work'."""
    workflow = MorningStandupWorkflow(
        preference_manager=MagicMock(),
        session_manager=MagicMock(),
        github_domain_service=MagicMock(),
        user_id="alpha",
    )
    github_activity = {"commits": []}
    session_context = {
        "session_context": {"yesterday_work": ["audit transparency Phase 2"]},
    }
    import time as time_module

    result = await workflow._generate_standup_content(
        user_id="alpha",
        session_context=session_context,
        github_activity=github_activity,
        start_time=time_module.time(),
    )

    work_items = [
        i for i in result.yesterday_accomplishments if i.source == "work"
    ]
    assert len(work_items) == 1
    assert work_items[0].display == "audit transparency Phase 2"
    assert work_items[0].icon == "📋"


@pytest.mark.asyncio
async def test_pipeline_carries_lifecycle_state_when_work_is_dict():
    """When yesterday_work entries are dicts with lifecycle_state, it propagates."""
    workflow = MorningStandupWorkflow(
        preference_manager=MagicMock(),
        session_manager=MagicMock(),
        github_domain_service=MagicMock(),
        user_id="alpha",
    )
    github_activity = {"commits": []}
    session_context = {
        "session_context": {
            "yesterday_work": [
                {"display": "ratified work item", "lifecycle_state": "ratified"}
            ]
        },
    }
    import time as time_module

    result = await workflow._generate_standup_content(
        user_id="alpha",
        session_context=session_context,
        github_activity=github_activity,
        start_time=time_module.time(),
    )

    work_items = [
        i for i in result.yesterday_accomplishments if i.source == "work"
    ]
    assert len(work_items) == 1
    assert work_items[0].display == "ratified work item"
    assert work_items[0].lifecycle_state == "ratified"
    assert work_items[0].icon == "📋"


@pytest.mark.asyncio
async def test_pipeline_active_repos_become_priority_items():
    workflow = MorningStandupWorkflow(
        preference_manager=MagicMock(),
        session_manager=MagicMock(),
        github_domain_service=MagicMock(),
        user_id="alpha",
    )
    github_activity = {"commits": [{"message": "x"}]}
    session_context = {"active_repos": ["piper-morgan", "klatch"]}
    import time as time_module

    result = await workflow._generate_standup_content(
        user_id="alpha",
        session_context=session_context,
        github_activity=github_activity,
        start_time=time_module.time(),
    )

    assert all(isinstance(i, StandupItem) for i in result.today_priorities)
    repo_items = [i for i in result.today_priorities if i.source == "active_repo"]
    assert {i.display for i in repo_items} == {
        "Continue work on piper-morgan",
        "Continue work on klatch",
    }
    for item in repo_items:
        assert item.icon == "🎯"
        assert item.lifecycle_state is None


@pytest.mark.asyncio
async def test_pipeline_blocker_when_no_commits():
    workflow = MorningStandupWorkflow(
        preference_manager=MagicMock(),
        session_manager=MagicMock(),
        github_domain_service=MagicMock(),
        user_id="alpha",
    )
    github_activity = {"commits": []}
    session_context = {}
    import time as time_module

    result = await workflow._generate_standup_content(
        user_id="alpha",
        session_context=session_context,
        github_activity=github_activity,
        start_time=time_module.time(),
    )

    assert len(result.blockers) == 1
    blocker = result.blockers[0]
    assert isinstance(blocker, StandupItem)
    assert blocker.source == "system"
    assert blocker.icon == "⚠️"
    assert "No recent GitHub activity" in blocker.display


# =============================================================================
# JSON serialization (the contract #704 will consume)
# =============================================================================


def test_json_format_serializes_structured_items():
    """format_standup(result, 'json') returns dicts per item with all fields."""
    from web.api.routes.standup import format_standup

    items = [
        StandupItem(display="first", source="commit", icon="✅"),
        StandupItem(
            display="second",
            source="work",
            lifecycle_state="ratified",
            icon="📋",
        ),
    ]
    result = StandupResult(
        user_id="alpha",
        generated_at=datetime(2026, 5, 3, 12, 0, 0),
        generation_time_ms=1234,
        yesterday_accomplishments=items,
        today_priorities=[],
        blockers=[],
        context_source="persistent",
        github_activity={},
        performance_metrics={},
        time_saved_minutes=15,
    )

    out: Dict[str, Any] = format_standup(result, "json")

    assert isinstance(out["yesterday_accomplishments"], list)
    assert len(out["yesterday_accomplishments"]) == 2
    first = out["yesterday_accomplishments"][0]
    assert first == {
        "display": "first",
        "source": "commit",
        "lifecycle_state": None,
        "icon": "✅",
        "meta": "",  # #1269: optional context line, empty by default
    }
    second = out["yesterday_accomplishments"][1]
    assert second["lifecycle_state"] == "ratified"


def test_slack_format_works_via_str_magic():
    """slack/markdown formatters keep working transparently because
    StandupItem.__str__ returns the legacy `f"{icon} {display}"` format."""
    from web.api.routes.standup import format_as_slack

    result = StandupResult(
        user_id="alpha",
        generated_at=datetime(2026, 5, 3, 12, 0, 0),
        generation_time_ms=1234,
        yesterday_accomplishments=[
            StandupItem(display="first commit", source="commit", icon="✅"),
        ],
        today_priorities=[
            StandupItem(display="Continue work on piper", source="active_repo", icon="🎯"),
        ],
        blockers=[],
        context_source="persistent",
        github_activity={},
        performance_metrics={},
        time_saved_minutes=15,
    )

    output = format_as_slack(result)
    assert "✅ first commit" in output
    assert "🎯 Continue work on piper" in output


def test_markdown_format_works_via_str_magic():
    from web.api.routes.standup import format_as_markdown

    result = StandupResult(
        user_id="alpha",
        generated_at=datetime(2026, 5, 3, 12, 0, 0),
        generation_time_ms=1234,
        yesterday_accomplishments=[
            StandupItem(display="commit message", source="commit", icon="✅"),
        ],
        today_priorities=[],
        blockers=[],
        context_source="persistent",
        github_activity={},
        performance_metrics={},
        time_saved_minutes=15,
    )

    output = format_as_markdown(result)
    assert "✅ commit message" in output
