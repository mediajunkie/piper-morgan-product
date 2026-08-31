"""Tests for #1101 service-side Pattern-073 cleanup on audit-summary response.

#1099 / #1100 (Surface 7 slices) discovered that
`services/api/transparency.py:get_user_audit_summary` returned two
unverifiable universal-claim fields:

  audit_completeness: "100%"     # bounded by limit=1000 upstream
  transparency_level: "Full transparency..."  # categorical claim

The UI applied Pattern-073 discipline by not rendering them (#1100 slice 2);
#1101 is the service-side cleanup. The summary now reports:

  entries_examined: <int>        # how many entries were actually examined
  entries_examined_limit: 1000   # the upstream bound

This file verifies both fields are gone + the verifiable substitutes are present.
"""

from pathlib import Path

SOURCE_FILE = Path("services/api/transparency.py")


def test_audit_completeness_field_removed() -> None:
    """The unverifiable universal-claim field is no longer set in the summary."""
    src = SOURCE_FILE.read_text()
    # Locate the summary dict in get_user_audit_summary
    start = src.find("async def get_user_audit_summary")
    end = src.find("\n@", start + 1)
    if end == -1:
        end = len(src)
    block = src[start:end]
    # The field as a dict key must not appear in the summary block
    assert (
        '"audit_completeness"' not in block
    ), "audit_completeness universal-claim field must be removed (Pattern-073 instance 9)"


def test_transparency_level_field_removed() -> None:
    """The 'Full transparency with privacy protection' universal claim is gone."""
    src = SOURCE_FILE.read_text()
    start = src.find("async def get_user_audit_summary")
    end = src.find("\n@", start + 1)
    if end == -1:
        end = len(src)
    block = src[start:end]
    assert (
        '"transparency_level"' not in block
    ), "transparency_level universal-claim field must be removed (Pattern-073 instance 10)"


def test_verifiable_substitutes_present() -> None:
    """Replacement fields provide verifiable scope: entries_examined + limit."""
    src = SOURCE_FILE.read_text()
    start = src.find("async def get_user_audit_summary")
    end = src.find("\n@", start + 1)
    if end == -1:
        end = len(src)
    block = src[start:end]
    assert '"entries_examined"' in block, "Verifiable entries_examined field must be present"
    assert '"entries_examined_limit"' in block, (
        "Verifiable entries_examined_limit field must be present so consumers "
        "know the upstream bound"
    )


def test_existing_verifiable_fields_preserved() -> None:
    """Don't accidentally drop the other (already-verifiable) summary fields."""
    src = SOURCE_FILE.read_text()
    start = src.find("async def get_user_audit_summary")
    end = src.find("\n@", start + 1)
    if end == -1:
        end = len(src)
    block = src[start:end]
    # These fields should still be there
    assert '"total_entries"' in block
    assert '"violation_entries"' in block
    assert '"decision_entries"' in block
    assert '"clean_interactions"' in block
    assert '"boundary_type_breakdown"' in block
    assert '"recent_activity_24h"' in block
    assert '"session_id"' in block


def test_change_documented_with_issue_reference() -> None:
    """Code comment cites #1101 + Pattern-073 for future-reader anchoring."""
    src = SOURCE_FILE.read_text()
    start = src.find("async def get_user_audit_summary")
    end = src.find("\n@", start + 1)
    block = src[start:end]
    assert "#1101" in block, "Code change must cite issue number"
    assert "Pattern-073" in block, "Code change must cite the discipline"


def test_pattern_073_body_records_instances_9_and_10() -> None:
    """The Pattern-073 catalog records the API-layer instances."""
    body = Path(
        "docs/internal/architecture/patterns/pattern-073-documentation-asserted-behavior-drift.md"
    ).read_text()
    assert "#1101" in body, "Pattern-073 body must reference #1101 fix"
    assert (
        "Instances 9 + 10" in body or "instances 9 + 10" in body.lower() or "9 + 10" in body
    ), "Pattern-073 body must record instances 9+10 (API-response universal claims)"
