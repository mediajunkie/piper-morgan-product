"""#1859 — static assets carry an explicit cache policy.

LAYER (m-43): the real mounted StaticFiles subclass under a TestClient — the
headers the browser will actually see. DENOMINATOR: both mounts (/static,
/assets), both URL shapes (versioned, unversioned), and a conditional request.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    from web.app import app

    return TestClient(app)


@pytest.mark.smoke
@pytest.mark.parametrize("path", ["/static/js/setup.js", "/assets/markdown-renderer.js"])
def test_unversioned_asset_revalidates(client, path):
    r = client.get(path)
    assert r.status_code == 200
    assert r.headers["cache-control"] == "public, max-age=0, must-revalidate"
    assert "etag" in r.headers


@pytest.mark.smoke
def test_versioned_asset_is_immutable_for_a_year(client):
    r = client.get("/static/js/setup.js?v=abc123")
    assert r.status_code == 200
    assert r.headers["cache-control"] == "public, max-age=31536000, immutable"


def test_conditional_request_gets_a_bodiless_304(client):
    first = client.get("/static/js/setup.js")
    r = client.get("/static/js/setup.js", headers={"If-None-Match": first.headers["etag"]})
    assert r.status_code == 304
    assert r.headers["cache-control"] == "public, max-age=0, must-revalidate"


@pytest.mark.smoke
def test_shell_asset_tags_carry_the_deploy_version():
    """Render layer: the shell's static tags are versioned so the immutable policy applies."""
    from pathlib import Path

    shell = (Path(__file__).resolve().parents[3] / "templates/layouts/app_shell.html").read_text()
    import re

    tags = re.findall(r'(?:href|src)="(/static/[^"]+|/assets/[^"]+)"', shell)
    assert tags, "no static tags found in the shell"
    unversioned = [t for t in tags if "?v={{ asset_v }}" not in t]
    assert not unversioned, f"unversioned asset tags: {unversioned}"


@pytest.mark.smoke
def test_page_transition_never_hides_content_or_delays_navigation():
    """The visual half of #1859 (m-43: the shipped JS/CSS is what the browser runs; there
    is no JS harness in this repo). The entry keyframe must not start at opacity 0, and
    a link click must navigate immediately rather than fade the body and wait."""
    import re
    from pathlib import Path

    root = Path(__file__).resolve().parents[3]
    css = (root / "web/static/css/page-transitions.css").read_text()
    js = (root / "web/static/js/page-transitions.js").read_text()

    slide_up = css[
        css.index("@keyframes slideUp") : css.index(
            "}", css.index("to {", css.index("@keyframes slideUp"))
        )
    ]
    assert "opacity: 0" not in slide_up, "entry animation starts the new document invisible"

    transition_to = js[js.index("transitionTo(url)") : js.index("onPageEnter()")]
    assert "page-exiting" not in transition_to, "exit fade hides content before navigating"
    assert not re.search(
        r"setTimeout\([^)]*window\.location\.href", transition_to, re.S
    ), "navigation is delayed behind a timer"
    assert "window.location.href = url;" in transition_to
    on_enter = js[js.index("onPageEnter()") : js.index("_handleLinkClick(event)")]
    assert "classList.add('page-entering')" not in on_enter
