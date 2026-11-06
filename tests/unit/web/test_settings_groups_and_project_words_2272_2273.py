"""#2273 Settings in four headed groups (Integrations first) and #2272 / #2271 page words.
Layer: template source (the served read is Web's, on a promoted build)."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SETTINGS = (REPO / "templates" / "settings-index.html").read_text(encoding="utf-8")
PANEL = (REPO / "templates" / "components" / "project_config_panel.html").read_text(
    encoding="utf-8"
)
PROJECTS = (REPO / "templates" / "projects.html").read_text(encoding="utf-8")

GROUPS = [
    (
        "Connect Piper to your tools",
        [
            "/settings/integrations",
            "/settings/projects",
            "/settings/llm-keys",
            "/settings/connected-apps",
        ],
    ),
    ("About you", ["/account", "/settings/preferences", "/personality-preferences", "/learning"]),
    ("Privacy and trust", ["/settings/privacy", "/transparency"]),
    ("For admins and developers", ["/settings/invites", "/settings/advanced"]),
]


def test_four_groups_in_order_with_their_cards():
    sections = re.findall(r'<section class="settings-group".*?</section>', SETTINGS, re.S)
    assert len(sections) == 4
    for sec, (title, hrefs) in zip(sections, GROUPS):
        assert f">{title}</h2>" in sec
        assert re.findall(r'<a href="([^"]+)" class="settings-card">', sec) == hrefs


def test_every_card_has_a_group_and_integrations_is_first():
    hrefs = re.findall(r'<a href="([^"]+)" class="settings-card">', SETTINGS)
    assert len(hrefs) == 12 and hrefs[0] == "/settings/integrations"


def test_group_headings_are_h2_labelling_their_section():
    assert (
        len(
            re.findall(r'<section class="settings-group" aria-labelledby="group-[a-z]+">', SETTINGS)
        )
        == 4
    )
    assert SETTINGS.count('<h2 class="settings-group-title"') == 4


def test_card_words_changed_as_designed():
    assert "Connect your tools, such as GitHub, and check that each one is working." in SETTINGS
    assert "Create invite codes, see which were used, and revoke the rest." in SETTINGS
    assert "Monitor health and test connections" not in SETTINGS
    assert "Mint alpha invite codes" not in SETTINGS


def test_project_page_words():
    assert "Link a repository" in PANEL
    assert "No repository is linked to ${escapeHtml(projectName())} yet." in PANEL
    assert "This only removes the link in Piper. The repository itself is not changed." in PANEL
    assert "from ${projectName()}?" in PANEL


def test_projects_list_has_no_edit_button():
    assert 'class="edit-btn"' not in PROJECTS
    assert "editProject" not in PROJECTS
    assert "Edit functionality coming soon" not in PROJECTS
