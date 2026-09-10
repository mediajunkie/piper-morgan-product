"""#1732 [SECURITY] — chat render-boundary assets: vendored, pinned, loaded.

Before #1732 the app_shell loaded marked UNPINNED from cdn.jsdelivr.net (a
supply-chain + silent-parse-drift exposure) and loaded NO sanitizer at all,
while renderBotMessage/marked.parse output went straight to innerHTML.

LAYER (named honestly): real Jinja `template.render()` for what the shipped
page loads (not curl-200, per the UI-fix discipline), plus on-disk content
pins for the vendored files the tags point to (a tag whose file is absent or
version-drifted would pass a source-grep — m-43), plus SOURCE pins on the JS
files' sanitizer wiring. The runtime-DOM half (attempted exploits through the
real marked + DOMPurify + renderer) lives in the jsdom harness:
tests/frontend/unit/chat-render-xss-1732.test.js.
"""

import re
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

REPO = Path(__file__).resolve().parents[3]
TEMPLATES = REPO / "templates"
VENDOR = REPO / "web" / "static" / "vendor"

MARKED_TAG = "/static/vendor/marked-15.0.12.min.js"
PURIFY_TAG = "/static/vendor/purify-3.2.7.min.js"
RENDERER_TAG = "/assets/bot-message-renderer.js"

_USER = {"username": "xian", "user_id": "u1", "is_admin": False}


@pytest.fixture(scope="module")
def env():
    return Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)


@pytest.fixture(scope="module")
def shell_html(env):
    """A minimal app_shell page — what every migrated page inherits."""
    return env.from_string(
        "{% extends 'layouts/app_shell.html' %}{% block main %}m{% endblock %}"
    ).render(trust_stage=1, user=_USER)


@pytest.fixture(scope="module")
def home_html(env):
    return env.get_template("home.html").render(trust_stage=1, user=_USER)


class TestNoCdnAssets:
    """The unpinned-CDN exposure is gone from every shell page."""

    def test_shell_has_no_cdn_script(self, shell_html):
        for cdn in ("cdn.jsdelivr.net", "unpkg.com", "cdnjs.cloudflare.com"):
            assert cdn not in shell_html

    def test_home_has_no_cdn_script(self, home_html):
        for cdn in ("cdn.jsdelivr.net", "unpkg.com", "cdnjs.cloudflare.com"):
            assert cdn not in home_html


class TestShellLoadsPinnedRenderStack:
    def test_vendored_marked_and_purify_load_before_chat_js(self, shell_html):
        for tag in (MARKED_TAG, PURIFY_TAG, RENDERER_TAG):
            assert tag in shell_html, f"shell must load {tag}"
        # Order: parser + sanitizer + renderer all precede chat.js, so the
        # sanitized renderBotMessage chokepoint exists before any chat render.
        chat = shell_html.index("/static/js/chat.js")
        assert shell_html.index(MARKED_TAG) < chat
        assert shell_html.index(PURIFY_TAG) < chat
        assert shell_html.index(RENDERER_TAG) < chat

    def test_renderer_loads_exactly_once_on_home(self, home_html):
        # home.html used to carry its own copy of the renderer tag; it is
        # shell-provided now — a double load would re-run marked.use().
        assert home_html.count(RENDERER_TAG) == 1


class TestVendoredFilesActuallyPinned:
    """m-43: the tags above prove nothing if the files are absent/drifted."""

    def test_marked_file_exists_at_pinned_version(self):
        f = VENDOR / "marked-15.0.12.min.js"
        assert f.is_file()
        assert "marked v15.0.12" in f.read_text(encoding="utf-8")[:500]

    def test_purify_file_exists_at_pinned_version(self):
        f = VENDOR / "purify-3.2.7.min.js"
        assert f.is_file()
        assert "DOMPurify 3.2.7" in f.read_text(encoding="utf-8")[:500]


class TestSanitizerWiredAtEverySink:
    """SOURCE pins (the runtime half is the jsdom suite): each JS file that
    innerHTMLs bot content routes through a DOMPurify-backed sanitizer."""

    @pytest.mark.parametrize(
        "js_path",
        [
            "web/assets/bot-message-renderer.js",
            "web/bot-message-renderer.js",
        ],
    )
    def test_renderer_copies_sanitize_before_wrap(self, js_path):
        src = (REPO / js_path).read_text(encoding="utf-8")
        assert "DOMPurify.sanitize" in src
        # The chokepoint applies to processedContent before the wrapper div.
        assert re.search(
            r"processedContent\s*=\s*_sanitizeRenderedHtml\(processedContent\)", src
        ), f"{js_path}: renderBotMessage must sanitize processedContent"

    def test_chat_js_fallback_sinks_are_sanitized(self):
        src = (REPO / "web/static/js/chat.js").read_text(encoding="utf-8")
        assert "DOMPurify.sanitize" in src
        # No bare marked.parse reaching innerHTML: every marked.parse call in
        # chat.js is wrapped in sanitizeRendered(...).
        for m in re.finditer(r"innerHTML\s*=\s*([^\n;]+)", src):
            rhs = m.group(1)
            if "marked.parse" in rhs:
                assert "sanitizeRendered(" in rhs, f"unsanitized sink: {rhs.strip()}"
        # The error interpolation is sanitized too.
        assert re.search(r"result error\">\$\{sanitizeRendered\(errorMsg\)\}", src)
