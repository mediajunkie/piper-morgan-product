"""F2 #1171 — migrated pages render correctly inside app_shell (real render, per-page).

Parametrized over the migrated cohort: each page must render through the shell (global nav
chrome + footer + widget runtime present), declare no own `<!DOCTYPE>`/`<html>` (it extends
the shell), and still show its own content. Add a (template, content-marker) row per page as
the migration proceeds. Real `template.render()` — the UI-fix discipline, not curl-200.
"""

from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

TEMPLATES = Path(__file__).resolve().parents[3] / "templates"

# (template, a content marker that must appear in the rendered page). Grows per migration.
MIGRATED = [
    ("insights.html", "Insight Journal"),
    ("advanced-settings.html", "Advanced Settings"),
]

_USER = {"username": "xian", "user_id": "u1", "is_admin": False}


@pytest.fixture
def env():
    return Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)


@pytest.mark.parametrize("template,marker", MIGRATED)
def test_migrated_page_renders_in_shell(env, template, marker):
    html = env.get_template(template).render(trust_stage=1, user=_USER)
    assert "global-nav" in html  # shell chrome (nav)
    assert "app-shell-footer" in html  # shell footer
    assert "/static/js/chat.js" in html  # shell-owned widget runtime
    assert marker in html  # the page's own content rendered into {% block main %}


@pytest.mark.parametrize("template,marker", MIGRATED)
def test_migrated_page_extends_shell_no_own_doctype(env, template, marker):
    src = (TEMPLATES / template).read_text()
    assert "<!DOCTYPE" not in src  # no own document — it extends the shell
    assert "<html" not in src
    assert (
        '{% extends "layouts/app_shell.html" %}' in src
        or "{% extends 'layouts/app_shell.html' %}" in src
    )
    # the per-page nav include is retired — the shell owns the chrome
    assert "{% include 'components/navigation.html' %}" not in src
