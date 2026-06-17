"""
Unit tests for transparency.html (#1099 MUX/UI Round 2 Surface 7).

Verifies the User-Facing Audit Envelope Read View structural contract per
ADR-063:
- AC-1: template exists at expected path
- AC-3: JS fetches /api/v1/transparency/audit-log/{session_id} with credentials
- AC-3: active session sourced from piper_active_conversation_id localStorage
- AC-4: renders event_type, boundary_category, action_taken, severity, timestamp
- AC-5: redacted markers wrapped in styled span
- AC-6: safe-fallback states (no-session, empty-list, 403, generic error)
- AC-7: settings-index card links to /transparency
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def transparency_html() -> str:
    return Path("templates/transparency.html").read_text()


@pytest.fixture
def soup(transparency_html: str) -> BeautifulSoup:
    return BeautifulSoup(transparency_html, "html.parser")


@pytest.fixture
def settings_index_html() -> str:
    return Path("templates/settings-index.html").read_text()


# AC-1 ---------------------------------------------------------------------


def test_transparency_template_exists() -> None:
    """AC-1: template file present at templates/transparency.html."""
    assert Path("templates/transparency.html").is_file()


def test_page_title(transparency_html: str) -> None:
    """Page declares its title via the shell's page_title block (F2 #1171 migration)."""
    assert "{% block page_title %}" in transparency_html
    assert "transparency" in transparency_html.lower()


# AC-3 (data fetch) --------------------------------------------------------


def test_fetch_targets_audit_log_endpoint(transparency_html: str) -> None:
    """AC-3: client calls /api/v1/transparency/audit-log/{session_id}."""
    assert (
        "/api/v1/transparency/audit-log/" in transparency_html
    ), "transparency.html must fetch from the shipped #1095 endpoint"


def test_fetch_includes_credentials(transparency_html: str) -> None:
    """AC-3: fetch uses credentials: 'include' for JWT auth (Issue #840)."""
    assert (
        "credentials: 'include'" in transparency_html
    ), "Cross-origin / cookie auth requires credentials: 'include'"


def test_active_session_from_localstorage(transparency_html: str) -> None:
    """AC-3: active session id read from piper_active_conversation_id key (#583)."""
    assert (
        "piper_active_conversation_id" in transparency_html
    ), "Active session must be sourced from the established localStorage key"


# AC-4 (rendering) ---------------------------------------------------------


def test_renders_event_type_and_timestamp(transparency_html: str) -> None:
    """AC-4: renderEntry surfaces event_type + timestamp fields per AuditLogResponse."""
    assert "entry.event_type" in transparency_html
    assert "entry.timestamp" in transparency_html


def test_renders_boundary_and_action(transparency_html: str) -> None:
    """AC-4: renderEntry surfaces boundary_type / violation_type + action_taken."""
    assert "boundary_type" in transparency_html
    assert "action_taken" in transparency_html


def test_renders_severity_with_class_variant(transparency_html: str) -> None:
    """AC-4: severity rendered with a class-variant for styling (CRITICAL etc.)."""
    assert "severityClass" in transparency_html
    assert "audit-badge-severity-critical" in transparency_html
    assert "audit-badge-severity-important" in transparency_html
    assert "audit-badge-severity-informational" in transparency_html


# AC-5 (redacted markers) --------------------------------------------------


def test_redacted_marker_styling(transparency_html: str) -> None:
    """AC-5: [REDACTED] occurrences wrapped in a .redacted-marker span for styling."""
    assert (
        ".redacted-marker" in transparency_html
    ), "CSS class for the redacted marker must be defined"
    assert (
        "renderWithRedactedMarkers" in transparency_html
    ), "Function that wraps [REDACTED] in styled spans must exist"


def test_redacted_marker_recognizes_plain_token(transparency_html: str) -> None:
    """AC-5: handler matches the SecurityRedactor plain [REDACTED] token.

    Note: ADR-063 specs typed markers <REDACTED-{type}>; current impl uses
    plain [REDACTED] — Pattern-073 instance 8 tracked in #1099 Phase 0.
    """
    assert (
        r"/\[REDACTED\]/g" in transparency_html
    ), "Replace regex must match plain [REDACTED] token used by SecurityRedactor"


# AC-6 (safe fallback states) ----------------------------------------------


def test_safe_fallback_no_session(transparency_html: str) -> None:
    """AC-6: structured no-active-session state, not error."""
    assert "renderNoSession" in transparency_html
    assert "audit-empty" in transparency_html


def test_safe_fallback_empty_list(transparency_html: str) -> None:
    """AC-6: structured empty-entry-list state, not error."""
    assert "renderEmpty" in transparency_html


def test_safe_fallback_unauthorized(transparency_html: str) -> None:
    """AC-6: 403/401 surfaces structured access-not-available state."""
    assert "renderUnauthorized" in transparency_html
    # Per ADR-063 uniform 403 messaging — don't leak session existence.
    assert "403" in transparency_html or "401" in transparency_html


def test_safe_fallback_generic_error(transparency_html: str) -> None:
    """AC-6: generic-error path renders structured error, not raw exception."""
    assert "renderError" in transparency_html


# AC-7 (settings card) -----------------------------------------------------


def test_settings_index_links_to_transparency(settings_index_html: str) -> None:
    """AC-7: settings-index.html grid contains a card linking to /transparency."""
    soup = BeautifulSoup(settings_index_html, "html.parser")
    card = soup.find("a", href="/transparency")
    assert card is not None, "settings-index.html must contain a card linking to /transparency"
    # Card must follow the established .settings-card pattern.
    assert "settings-card" in (card.get("class") or [])


# Pattern-073 discipline ---------------------------------------------------


def test_no_universal_claims_in_user_facing_copy(transparency_html: str) -> None:
    """Per Pattern-073: user-facing copy must not assert more than queried scope.

    Forbidden phrases: 'all decisions', 'every decision', 'complete record',
    'full audit' — these assert universal scope while the endpoint only returns
    a bounded slice for the active session.
    """
    lower = transparency_html.lower()
    forbidden = ["all decisions", "every decision", "complete record", "full audit"]
    found = [phrase for phrase in forbidden if phrase in lower]
    assert not found, (
        f"Pattern-073 discipline violation: user-facing copy contains "
        f"unverifiable universal claims: {found}"
    )
