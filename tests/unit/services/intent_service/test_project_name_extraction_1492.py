"""#1492: project-name extraction brittle on archive/restore phrasings.

PM 8/7 walkthrough (v30): of four natural archive phrasings, only the bare
'Archive my project Test' resolved; 'Archive my Test project, please.'
looked up 'test project, please.', and both quoted/'called' forms kept
their quotes ('called "test"', '"test"').

The name-slot cleaning is `clean_project_name` in
services.onboarding.portfolio_service (hoisted from a nested helper in
canonical_handlers._handle_portfolio_query so it is testable/shared).
These tests mirror the handler's exact extraction flow: lowercase the
message, match the pattern tables, clean group(1).

NOTE: tests/unit/services/onboarding/test_portfolio_service.py is blanket-
skipped ("ADR-059: onboarding on ice"), so this file also carries the live
regression pins for the previously-working extraction forms.

Downstream lookup (find_project_by_name) is case-insensitive, so resolving
to lowercase 'test' resolves the project named 'Test'.
"""

import re

import pytest

from services.onboarding.portfolio_service import (
    ARCHIVE_PATTERNS,
    DELETE_PATTERNS,
    RESTORE_PATTERNS,
    clean_project_name,
)


def extract(message, patterns):
    """Replicate canonical_handlers._handle_portfolio_query extraction."""
    message_lower = message.lower().strip()
    for pattern in patterns:
        match = re.search(pattern, message_lower, re.IGNORECASE)
        if match:
            return clean_project_name(match.group(1).strip()) if match.groups() else None
    return None


class TestArchiveNameExtraction1492:
    """PM's four verbatim phrasings, all resolving to 'test' (== 'Test')."""

    @pytest.mark.parametrize(
        "message",
        [
            # PM's verbatim phrasings from the 8/7 walkthrough:
            "Archive my Test project, please.",  # adjective position + tail
            'Archive my project called "Test" please',  # 'called X' + quotes
            'Archive my project "Test"',  # double quotes
            "Archive my project Test",  # bare form (the one that worked)
        ],
    )
    def test_pm_verbatim_phrasings_resolve_to_test(self, message):
        assert extract(message, ARCHIVE_PATTERNS) == "test"

    @pytest.mark.parametrize(
        "message",
        [
            "Archive my project 'Test'",  # single quotes
            "Archive my project named Test",  # 'named X'
            "Archive my Test project",  # adjective position, no tail
            "Archive my project Test, please",  # comma + politeness, no quote
            "Archive my project Test.",  # trailing period only
            'Archive my project called "Test", please.',  # everything at once
        ],
    )
    def test_nearby_variants_resolve_to_test(self, message):
        assert extract(message, ARCHIVE_PATTERNS) == "test"


class TestRestoreAndDeleteNameExtraction1492:
    """The cleaning is shared; restore/delete phrasings get the same fixes."""

    @pytest.mark.parametrize(
        "message",
        [
            "Restore my Test project, please.",
            'Restore my project "Test"',
            "Restore my project called Test",
            "Restore my project Test",
        ],
    )
    def test_restore_phrasings_resolve_to_test(self, message):
        assert extract(message, RESTORE_PATTERNS) == "test"

    @pytest.mark.parametrize(
        "message",
        [
            "Delete my Test project, please.",
            'Delete my project "Test"',
        ],
    )
    def test_delete_phrasings_resolve_to_test(self, message):
        assert extract(message, DELETE_PATTERNS) == "test"


class TestExtractionRegressionPins:
    """Previously-working forms must keep working (the skipped onboarding
    suite pinned these; re-pin them in a live file)."""

    @pytest.mark.parametrize(
        "message,patterns,expected",
        [
            ("archive HealthTrack", ARCHIVE_PATTERNS, "healthtrack"),
            ("archive my project HealthTrack", ARCHIVE_PATTERNS, "healthtrack"),
            ("hide my project DataViz", ARCHIVE_PATTERNS, "dataviz"),
            ("put HealthTrack away", ARCHIVE_PATTERNS, "healthtrack"),
            ("delete HealthTrack please", DELETE_PATTERNS, "healthtrack"),
            ("remove my project DataViz", DELETE_PATTERNS, "dataviz"),
            ("get rid of HealthTrack", DELETE_PATTERNS, "healthtrack"),
            ("restore my project HealthTrack", RESTORE_PATTERNS, "healthtrack"),
            ("unarchive HealthTrack", RESTORE_PATTERNS, "healthtrack"),
            ("bring back HealthTrack now", RESTORE_PATTERNS, "healthtrack"),
        ],
    )
    def test_working_forms_unchanged(self, message, patterns, expected):
        assert extract(message, patterns) == expected

    def test_multiword_names_survive_cleaning(self):
        """A multi-word name that isn't adjective-position stays intact."""
        assert extract("archive my project Data Pipeline", ARCHIVE_PATTERNS) == "data pipeline"

    def test_none_and_empty_passthrough(self):
        assert clean_project_name(None) is None
        assert clean_project_name("") == ""
