"""
#1034 — StandupItem structured-item wiring tests.

Verifies the gameplan-mandated invariant: the standup pipeline carries
structured per-item data (`StandupItem` dataclass) through to the API
response, so #704 (MUX-LIFECYCLE-UI-A) can read `lifecycle_state` per
item from the standup.html template.

Coverage:
- StandupItem dataclass roundtrip (str + to_dict)
- StandupItems with `lifecycle_state` flow through to dict shape
- JSON formatter (`format_standup`) serializes to structured dicts
- Backwards-compat: slack/markdown formatters work via __str__

Updated: 2026-06-20 (#1289) — removed MorningStandupWorkflow pipeline
producer tests (tests_pipeline_produces_structured_items_from_commits,
etc.) because _generate_standup_content is no longer called; the
/generate route delegates to StandupAssembler. StandupItem dataclass
and formatter tests are retained — those contracts are still in use.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

import pytest

from services.features.morning_standup import (
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
