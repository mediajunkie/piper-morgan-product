"""
#714 — Staleness computation unit tests.

Pure-function tests for `services.lists.staleness`. No DB; just timestamps.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from services.lists.staleness import (
    DEFAULT_STALENESS_THRESHOLD_DAYS,
    StalenessSignal,
    compute_staleness,
    effective_updated_at,
    format_last_updated_human,
    get_staleness_threshold,
)


# =============================================================================
# Threshold from env
# =============================================================================


class TestThresholdFromEnv:
    def test_default_when_unset(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("PIPER_LIST_STALENESS_DAYS", None)
            assert get_staleness_threshold() == DEFAULT_STALENESS_THRESHOLD_DAYS

    def test_overridden_value(self):
        with patch.dict(os.environ, {"PIPER_LIST_STALENESS_DAYS": "30"}):
            assert get_staleness_threshold() == 30

    def test_invalid_value_falls_back_to_default(self):
        with patch.dict(os.environ, {"PIPER_LIST_STALENESS_DAYS": "not-a-number"}):
            assert get_staleness_threshold() == DEFAULT_STALENESS_THRESHOLD_DAYS

    def test_zero_or_negative_falls_back_to_default(self):
        with patch.dict(os.environ, {"PIPER_LIST_STALENESS_DAYS": "0"}):
            assert get_staleness_threshold() == DEFAULT_STALENESS_THRESHOLD_DAYS
        with patch.dict(os.environ, {"PIPER_LIST_STALENESS_DAYS": "-5"}):
            assert get_staleness_threshold() == DEFAULT_STALENESS_THRESHOLD_DAYS


# =============================================================================
# Effective timestamp
# =============================================================================


class TestEffectiveUpdatedAt:
    def test_no_items_returns_list_updated_at(self):
        list_ts = datetime(2026, 5, 1, tzinfo=timezone.utc)
        result = effective_updated_at(list_ts, [])
        assert result == list_ts

    def test_item_more_recent_than_list(self):
        """When an item was added more recently than the List was updated,
        the item's added_at wins (the list IS active even though the List
        record itself looks stale)."""
        list_ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
        item_ts = datetime(2026, 5, 1, tzinfo=timezone.utc)
        result = effective_updated_at(list_ts, [item_ts])
        assert result == item_ts

    def test_list_more_recent_than_items(self):
        list_ts = datetime(2026, 5, 1, tzinfo=timezone.utc)
        item_ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
        result = effective_updated_at(list_ts, [item_ts])
        assert result == list_ts

    def test_naive_datetimes_promoted_to_utc(self):
        """List.updated_at + item.added_at are TIMESTAMPTZ at the DB level
        but be defensive against naive datetimes from elsewhere."""
        naive_list = datetime(2026, 5, 1)  # naive
        naive_item = datetime(2026, 5, 5)  # naive
        result = effective_updated_at(naive_list, [naive_item])
        assert result.tzinfo is not None
        assert result == naive_item.replace(tzinfo=timezone.utc)


# =============================================================================
# Human label
# =============================================================================


class TestFormatLastUpdatedHuman:
    @pytest.mark.parametrize(
        "days,expected",
        [
            (0, "today"),
            (-3, "today"),  # clock-skew defense
            (1, "yesterday"),
            (2, "2 days ago"),
            (15, "15 days ago"),
            (29, "29 days ago"),
            (30, "about a month ago"),
            (45, "about a month ago"),
            (59, "about a month ago"),
            (60, "2 months ago"),
            (90, "3 months ago"),
            (180, "6 months ago"),
            (364, "12 months ago"),
            (365, "over a year ago"),
            (729, "over a year ago"),
            (730, "over 2 years ago"),
            (1100, "over 3 years ago"),
        ],
    )
    def test_bands(self, days, expected):
        assert format_last_updated_human(days) == expected


# =============================================================================
# Conceptual integrity (per audit Q5)
# =============================================================================


class TestConceptualIntegrityVocabulary:
    """No `archived` / lifecycle stage names in human labels."""

    @pytest.mark.parametrize("days", [0, 1, 30, 60, 365, 730])
    def test_no_lifecycle_terms_in_labels(self, days):
        label = format_last_updated_human(days)
        forbidden = [
            "archived",
            "ratified",
            "deprecated",
            "obsolete",
            "EMERGENT",
            "DERIVED",
            "NOTICED",
            "PROPOSED",
            "RATIFIED",
            "ARCHIVED",
            "COMPOSTED",
        ]
        for word in forbidden:
            assert (
                word.lower() not in label.lower()
            ), f"Forbidden vocabulary '{word}' in label for days={days}: '{label}'"


# =============================================================================
# End-to-end staleness signal
# =============================================================================


class TestComputeStaleness:
    def test_fresh_list_not_stale(self):
        now = datetime(2026, 5, 3, tzinfo=timezone.utc)
        list_ts = now - timedelta(days=5)
        result = compute_staleness(list_ts, [], threshold_days=60, now=now)
        assert result.is_stale is False
        assert result.days_since_update == 5
        assert result.last_updated_human == "5 days ago"

    def test_stale_list(self):
        now = datetime(2026, 5, 3, tzinfo=timezone.utc)
        list_ts = now - timedelta(days=90)
        result = compute_staleness(list_ts, [], threshold_days=60, now=now)
        assert result.is_stale is True
        assert result.days_since_update == 90

    def test_old_list_with_recent_items_not_stale(self):
        """Old list, but items have been added recently → not stale."""
        now = datetime(2026, 5, 3, tzinfo=timezone.utc)
        old_list_ts = now - timedelta(days=180)
        recent_item = now - timedelta(days=2)
        result = compute_staleness(old_list_ts, [recent_item], threshold_days=60, now=now)
        assert result.is_stale is False
        assert result.days_since_update == 2

    def test_just_at_threshold_not_stale(self):
        """`is_stale = days > threshold`, so exactly threshold is not stale."""
        now = datetime(2026, 5, 3, tzinfo=timezone.utc)
        list_ts = now - timedelta(days=60)
        result = compute_staleness(list_ts, [], threshold_days=60, now=now)
        assert result.is_stale is False
        assert result.days_since_update == 60

    def test_to_dict_round_trip(self):
        now = datetime(2026, 5, 3, tzinfo=timezone.utc)
        list_ts = now - timedelta(days=90)
        result = compute_staleness(list_ts, [], threshold_days=60, now=now)
        d = result.to_dict()
        assert d == {
            "is_stale": True,
            "days_since_update": 90,
            "last_updated_human": "3 months ago",
        }

    def test_threshold_via_env(self):
        """threshold_days arg overrides env; env overrides default."""
        now = datetime(2026, 5, 3, tzinfo=timezone.utc)
        list_ts = now - timedelta(days=45)

        with patch.dict(os.environ, {"PIPER_LIST_STALENESS_DAYS": "30"}):
            result = compute_staleness(list_ts, [], now=now)
            assert result.is_stale is True

        with patch.dict(os.environ, {"PIPER_LIST_STALENESS_DAYS": "90"}):
            result = compute_staleness(list_ts, [], now=now)
            assert result.is_stale is False
