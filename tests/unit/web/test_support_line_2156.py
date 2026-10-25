"""#2156 (CXO 10-24): Send feedback is easy to see in the rail, and every page with no app
shell (so no rail and no feedback link) names the support address.

- The rail's Send feedback link sits on its own line, outside the section links, in the
  secondary colour, not the divider colour.
- Each top-level template that doesn't use the shell carries CXO's line, "Stuck? Email
  support@pipermorgan.ai." The forcing test derives the set, so a new shell-less page has
  to carry it too.
"""

import re
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

TEMPLATES = Path(__file__).resolve().parents[3] / "templates"
CSS = Path(__file__).resolve().parents[3] / "web/static/css"
LINE = 'Stuck? Email <a href="mailto:support@pipermorgan.ai">support@pipermorgan.ai</a>.'


def _shell_less():
    return sorted(p.name for p in TEMPLATES.glob("*.html") if "app_shell" not in p.read_text())


def test_the_shell_less_set_is_the_six_cxo_named():
    assert _shell_less() == [
        "404.html",
        "500.html",
        "login.html",
        "network-error.html",
        "reset_password.html",
        "setup.html",
    ]


@pytest.mark.parametrize("name", _shell_less())
def test_every_shell_less_page_renders_the_support_line(name):
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)))
    html = env.get_template(name).render(request=None, asset_v="t", hosted=True)
    assert LINE in html, f"{name} has no shell and no support line"


def test_the_wizard_line_sits_outside_every_step():
    """The line shows on the intro and on every step, not inside one step."""
    src = (TEMPLATES / "setup.html").read_text()
    line_at = src.index(LINE)
    last_step = src.rindex('class="setup-step"')
    assert line_at > last_step
    tail = src[last_step:line_at]
    # step 5 closes before the line: the line is a sibling of the steps
    assert tail.count("<div") <= tail.count("</div>")


def test_the_rail_link_is_its_own_line_outside_the_section_links():
    rail = (TEMPLATES / "components/nav_rail.html").read_text()
    nav = rail[rail.index('<nav class="nav-rail-utility"') : rail.index("</nav>")]
    assert "/feedback" not in nav
    assert re.search(
        r'<a href="/feedback" class="nav-rail-feedback-link" id="nav-feedback"[^>]*>Send feedback</a>',
        rail,
    )
    assert rail.index('id="nav-feedback"') < rail.index('<nav class="nav-rail-utility"')


def test_the_rail_link_uses_the_secondary_colour_not_the_divider():
    css = (CSS / "nav-rail.css").read_text()
    rule = re.search(r"\.nav-rail-feedback-link \{([^}]*)\}", css)
    assert rule, "no .nav-rail-feedback-link rule"
    assert "color: var(--color-nav-text-secondary)" in rule.group(1)
    assert "--color-nav-divider" not in rule.group(1)
    assert "display: block" in rule.group(1)
