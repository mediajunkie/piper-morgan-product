"""#1576 — the standup PAGE render, at the layer that decides the face (m-43).

Why this test exists rather than a route check: ``GET /standup`` returns 200
whether or not the page ever shows a time, so a curl is a test of routing, not
of rendering. The question this file answers is narrower and is the one the fix
depends on — **does the zone label the server put on a calendar time survive to
the DOM, or does the page re-format it?**

It survives, and that is exactly why ``StandupCalendarProvider._fmt_time`` has to
label it. The page interpolates ``item.meta`` verbatim into an ``<li>``; there is
no ``toLocale*`` pass on that value anywhere in the template. So this surface is
NOT one of the audit's 23 "aware ISO + browser localization" sites and cannot be
converted into one by relabeling the server string — the server face is final.

The complementary case is ``/api/v1/standup/generate?format=json``, which DOES
reach a browser as an instant; its aware-ISO contract is pinned in
``test_standup_render_faces_1576.py``.
"""

import re
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

TEMPLATE_ROOT = Path(__file__).resolve().parents[4] / "templates"


@pytest.fixture(scope="module")
def rendered_page() -> str:
    """A real Jinja render of the page, not a fetch of a route."""
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_ROOT)))
    return env.get_template("standup.html").render(request=None, user=None)


def test_the_page_actually_renders(rendered_page):
    """Guards the render itself — a template that raises is invisible to any
    check that only looks at a status code."""
    assert len(rendered_page) > 1000
    assert "standup" in rendered_page.lower()


def test_item_meta_is_interpolated_verbatim(rendered_page):
    """``item.meta`` — which carries the calendar time face — goes straight into
    the markup."""
    assert re.search(r"class=\"standup-item-meta\">[^<]*\$\{item\.meta\}", rendered_page), (
        "item.meta is no longer interpolated verbatim; re-check whether the "
        "server-side zone label is still the one the user sees"
    )


def test_no_browser_side_reformatting_of_the_server_face(rendered_page):
    """If someone later wraps ``item.meta`` in ``toLocale*`` or ``new Date()``,
    the server's label would be silently dropped and the page would be back to
    a bare face. This fails loudly at that point rather than at the next audit."""
    for pattern in (r"toLocale\w*\([^)]*item\.meta", r"new Date\([^)]*item\.meta"):
        assert not re.search(
            pattern, rendered_page
        ), f"{pattern} applied to item.meta — the server face is being reformatted"
