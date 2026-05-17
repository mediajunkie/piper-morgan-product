"""
Unit tests for home.html left-sidebar Surface 1 reconciliation (#1097)

Verifies the MUX/UI Round 2 Surface 1 contract:
- Left rail = "current session continuation" (~5 recent ACTIVE)
- Differentiated from right slide-out (history_sidebar.html, full archive)

Round 2 ratification: 2026-05-16 (Architect's CEO ratification distribution).
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def home_html() -> str:
    return Path("templates/home.html").read_text()


@pytest.fixture
def soup(home_html: str) -> BeautifulSoup:
    return BeautifulSoup(home_html, "html.parser")


def test_left_rail_fetch_caps_at_five_active(home_html: str) -> None:
    """AC-1: left rail fetches at most 5 active conversations."""
    assert "/api/v1/conversations?state=active&limit=5" in home_html, (
        "Left rail must fetch with state=active&limit=5 per Round 2 Surface 1 spec "
        "(current-session continuation, ~5 recent)"
    )


def test_left_rail_aria_label_distinguishes_from_history_sidebar(soup: BeautifulSoup) -> None:
    """AC-2: left rail aside has aria-label that names its role.

    History sidebar (right slide-out) uses aria-label="Conversation history".
    Left rail must use a distinct aria-label so assistive tech users can tell them apart.
    """
    left_rail = soup.find("aside", {"id": "sidebar"})
    assert left_rail is not None, "Left rail aside#sidebar must exist"
    aria_label = left_rail.get("aria-label", "")
    assert aria_label, "Left rail must have aria-label"
    # Must be distinct from right slide-out's "Conversation history"
    assert aria_label.lower() != "conversation history", (
        "Left rail aria-label must differ from right slide-out's "
        "'Conversation history' label"
    )


def test_left_rail_has_recent_section_header(soup: BeautifulSoup) -> None:
    """AC-2: visible 'Recent' header inside the left rail differentiates from
    right slide-out's 'History' header."""
    left_rail = soup.find("aside", {"id": "sidebar"})
    assert left_rail is not None
    header = left_rail.find(class_="sidebar-section-header")
    assert header is not None, (
        "Left rail must have a .sidebar-section-header element to make the "
        "current-session-continuation role visible"
    )
    assert "recent" in header.get_text().strip().lower(), (
        "Section header text must convey recency (left rail role per Round 2)"
    )
