"""
Slice 2 tests for transparency.html (#1100 — MUX/UI Round 2 Surface 7 slice 2).

Verifies session selector + audit-summary integration:
- Session selector <select> exists + is wired to onchange handler
- Conversations fetched from /api/v1/conversations?state=active&limit=20
- audit-summary fetched from /api/v1/transparency/audit-summary/{session_id}
- Summary rendering skips audit_completeness + transparency_level fields
  (Pattern-073 discipline — universal-claim avoidance)
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


# Session selector (AC-1, AC-2, AC-3) -------------------------------------


def test_session_selector_select_element_exists(soup: BeautifulSoup) -> None:
    """AC-1: <select> element with id=session-selector-input is in markup."""
    select = soup.find("select", {"id": "session-selector-input"})
    assert select is not None, "Session selector <select> must be in markup"


def test_session_selector_has_accessible_label(soup: BeautifulSoup) -> None:
    """AC-1: <select> has an associated <label> or aria-label."""
    select = soup.find("select", {"id": "session-selector-input"})
    label = soup.find("label", {"for": "session-selector-input"})
    assert label is not None or select.get("aria-label"), (
        "Selector must be labeled (label[for] or aria-label) for accessibility"
    )


def test_conversations_fetch_target(transparency_html: str) -> None:
    """AC-2: conversations list fetched from active state with limit=20."""
    assert "/api/v1/conversations?state=active&limit=20" in transparency_html, (
        "Slice 2 must fetch conversations list from the established endpoint "
        "with limit=20 (more than Surface 1 left-rail's limit=5)"
    )


def test_selector_change_triggers_reload(transparency_html: str) -> None:
    """AC-2: selector's change event triggers loadAuditForSession()."""
    assert "select.addEventListener('change'" in transparency_html
    assert "loadAuditForSession(select.value)" in transparency_html


def test_default_selection_active_session(transparency_html: str) -> None:
    """AC-3: when populating, the active session id pre-selects."""
    assert "if (conv.id === currentSessionId) opt.selected = true" in transparency_html


# Audit summary (AC-4, AC-5) ----------------------------------------------


def test_summary_fetch_target(transparency_html: str) -> None:
    """AC-4: audit-summary fetched from the documented endpoint per session."""
    assert "/api/v1/transparency/audit-summary/" in transparency_html


def test_summary_renders_verifiable_counts(transparency_html: str) -> None:
    """AC-4: summary surfaces total/violations/decisions/clean/recent24h counts."""
    assert "total_entries" in transparency_html
    assert "violation_entries" in transparency_html
    assert "decision_entries" in transparency_html
    assert "clean_interactions" in transparency_html
    assert "recent_activity_24h" in transparency_html


def test_summary_renders_boundary_breakdown(transparency_html: str) -> None:
    """AC-4: summary surfaces boundary_type_breakdown."""
    assert "boundary_type_breakdown" in transparency_html
    assert "Boundary breakdown" in transparency_html


def test_summary_skips_universal_claim_fields(transparency_html: str) -> None:
    """AC-5: Pattern-073 discipline — audit_completeness and transparency_level
    fields NOT surfaced to the UI (they assert universal claims the backend
    can't actually verify; bounded by limit=1000 in the service).

    Test checks for data-accessor usage (`summary.<field>`) rather than the
    literal field name appearing anywhere — comments that mention the field
    names for documentation purposes are fine."""
    text = transparency_html
    start = text.find("function renderSummary(")
    end = text.find("async function fetchAuditSummary(")
    assert start >= 0 and end > start, "renderSummary block must be present"
    block = text[start:end]
    # The data-accessor pattern is what surfaces a field to the UI.
    # The comment block in the source legitimately mentions the field names
    # as part of the Pattern-073 discipline note; check accessors only.
    assert "summary.audit_completeness" not in block, (
        "Pattern-073 discipline violation: audit_completeness asserts '100%' "
        "but is bounded by service-side limit; do not surface in UI"
    )
    assert "summary.transparency_level" not in block, (
        "Pattern-073 discipline violation: transparency_level asserts "
        "'Full transparency with privacy protection' (universal claim); "
        "do not surface in UI"
    )


# Empty-state behaviors (AC-6) --------------------------------------------


def test_no_sessions_falls_back_to_no_session_state(transparency_html: str) -> None:
    """AC-6: when no active session AND no conversations, render no-session."""
    # The effective-session-id selection logic must be present
    assert "effectiveSessionId" in transparency_html
    # And feed into renderNoSession
    assert "if (!effectiveSessionId)" in transparency_html


def test_summary_fetch_failure_returns_null_not_throws(transparency_html: str) -> None:
    """AC-6: summary fetch failure quietly returns null; renderSummary handles
    null by clearing the container (does NOT crash the audit-log view)."""
    # The fetch function must catch and return null
    start = transparency_html.find("async function fetchAuditSummary(")
    end = transparency_html.find("async function loadAuditForSession(")
    assert start >= 0 and end > start
    block = transparency_html[start:end]
    assert "return null" in block
    # And renderSummary must handle null
    assert "if (!summary)" in transparency_html


# Test surface exposure for browser-side testability ----------------------


def test_renderSummary_exposed_for_tests(transparency_html: str) -> None:
    """window.TransparencyPage exposes renderSummary for any browser-side tests."""
    assert "renderSummary: renderSummary" in transparency_html
    assert "populateSessionSelector: populateSessionSelector" in transparency_html
