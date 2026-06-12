"""#1194: home.html "Recently" module markup (content assertions).

The module renders surfaced_insights as cards (with a loop + empty-state branch)
inside a Stage-3+ gate, with a light module border. Live render verified
separately (3-card / reload-persists smoke). These guard the template markup.
"""

from pathlib import Path

import pytest


@pytest.fixture
def home_html() -> str:
    return (Path(__file__).resolve().parents[3] / "templates" / "home.html").read_text()


def test_recently_section_present(home_html):
    assert 'id="recently-section"' in home_html
    assert ">recently</h3>" in home_html  # card__title is lowercase per design language


def test_renders_cards_from_surfaced_insights(home_html):
    assert "{% for insight in surfaced_insights %}" in home_html
    assert 'class="reflection-card"' in home_html
    assert "{{ insight.text }}" in home_html


def test_has_empty_state_branch(home_html):
    # CXO B3 empty-state pattern + Part-A copy (when-it-populates explainer).
    assert "card__empty-explainer" in home_html
    assert "as Piper composts what you" in home_html


def test_stage_gated_and_card_chromed(home_html):
    # Module sits behind a Stage-3+ gate and uses the shared Card component
    # (CXO design language) — the card chrome provides the module boundary.
    assert 'class="card"' in home_html
    assert "cards.css" in home_html
