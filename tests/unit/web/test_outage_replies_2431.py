"""Issue 2431: a refusal answers a page load with a page and a background request with a sentence.

Spec: the issue body (CXO's outage sentence), Arch's ruling (comment of 2026-11-24 10:50 PT:
one "wants a page" predicate in ``services/api/``; both outage 503s answer a plain page built
from one constant; JSON elsewhere with the sentence as ``message``), and CXO's comment with
the 429 and at-capacity words (same mechanism).

LAYER: the reply each middleware produces, read from a small app that carries the REAL
middleware class and a route behind it (``TestClient``, no server). Redis is made to fail, or
to answer "over the limit", by patching the one seam ``RedisFactory.redis_scope`` in the
guard's module; the session check fails by giving the real ``AuthMiddleware`` a JWT service
whose ``validate_token`` raises ``BlacklistUnavailable``. No shared service is touched.
The pages' scripts are read as source; the shared reader is also run under ``node`` (no
browser) when ``node`` is on the path.
NOT COVERED: any rendering. Nothing here draws a page in a browser; what a person sees is
inferred from the reply bodies and the scripts' source.
DENOMINATOR: the four refusal kinds (capacity guard outage, session outage, 429, at
capacity), each as a page load and as a background request (``Accept: application/json``,
and an ``/api/`` path that accepts HTML).
"""

import ast
import json
import re
import shutil
import subprocess
from contextlib import asynccontextmanager
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from starlette.middleware.base import BaseHTTPMiddleware

import web.middleware.usage_cap_middleware as ucm
from services.api import refusal_pages
from services.api.errors import (
    PIPER_CANT_TAKE_REQUESTS_MESSAGE,
    PIPER_IS_FULL_MESSAGE,
    RATE_LIMITED_MESSAGE,
    SESSION_COULD_NOT_BE_CHECKED_MESSAGE,
)
from services.api.refusal_pages import (
    REFUSAL_PAGE_HTML,
    refusal_page,
    wants_a_page,
)
from services.auth.auth_middleware import AuthMiddleware
from services.auth.jwt_service import BlacklistUnavailable

ROOT = Path(__file__).resolve().parents[3]

# CXO's words, written out here so a change to a constant is a diff a reader sees.
CXO_OUTAGE = (
    "Piper can't take requests just now. Nothing was changed. Try again in a moment; "
    "if it keeps failing, tell us."
)
CXO_RATE_LIMITED_37 = (
    "That's more than I can take in a minute. Nothing was changed. Try again in 37 seconds."
)
CXO_FULL = (
    "Piper is full right now. Nothing was changed. Try again in a minute; if it keeps "
    "happening, tell us."
)
CXO_SESSION = (
    "Your session couldn't be checked just now. Nothing was changed. Try again in a "
    "moment; if it keeps failing, tell us."
)
CODE_WORDS = (
    "capacity_check_unavailable",
    "verification_unavailable",
    "service_unavailable",
    "rate_limited",
    "at_capacity",
    "retry_after_seconds",
)
PAGE_PATH = "/settings/integrations"
API_PATH = "/api/v1/probe-2431"
HTML_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
JSON_ACCEPT = "application/json"

# Distinctive numbers, so "the removed numbers do not appear" can be read off the body.
RATE_LIMIT_FOR_TEST = 4321
CAPACITY_FOR_TEST = 987
SECONDS_LEFT = 37


# ---------------------------------------------------------------------------
# Small apps: the real middleware class in front of routes that record they ran.
# ---------------------------------------------------------------------------


class _Ran:
    def __init__(self):
        self.calls = []


def _routes(app, ran):
    @app.get(PAGE_PATH)
    async def page():  # pragma: no cover - reached only if the middleware lets it
        ran.calls.append(PAGE_PATH)
        return {"ran": True}

    @app.get(API_PATH)
    @app.post(API_PATH)
    async def api():  # pragma: no cover - reached only if the middleware lets it
        ran.calls.append(API_PATH)
        return {"ran": True}


class _SignedIn(BaseHTTPMiddleware):
    """Stands in for AuthMiddleware's one effect the guard reads: ``request.state.user_id``
    (the concurrency gauge counts signed-in people only, #1390)."""

    async def dispatch(self, request: Request, call_next):
        request.state.user_id = "user-2431"
        return await call_next(request)


def _capacity_app(ran):
    app = FastAPI()
    _routes(app, ran)
    app.add_middleware(ucm.UsageCapMiddleware)
    app.add_middleware(_SignedIn)  # added later = outer, so it runs first
    return app


def _session_app(ran):
    jwt_service = MagicMock()
    jwt_service.validate_token = AsyncMock(side_effect=BlacklistUnavailable("store down"))
    app = FastAPI()
    _routes(app, ran)
    app.add_middleware(AuthMiddleware, jwt_service=jwt_service)
    return app


@asynccontextmanager
async def _redis_down():
    raise ConnectionError("Error 61 connecting to localhost:6379. Connection refused.")
    yield  # pragma: no cover


class _OverTheRateLimit:
    async def incr(self, key):
        return ucm.RATE_LIMIT_PER_MINUTE + 1

    async def expire(self, key, seconds):
        return True

    async def ttl(self, key):
        return SECONDS_LEFT


class _Full:
    async def incr(self, key):
        return 1

    async def expire(self, key, seconds):
        return True

    async def zremrangebyscore(self, key, low, high):
        return 0

    async def zscore(self, key, member):
        return None

    async def zcard(self, key):
        return ucm.MAX_CONCURRENT_SESSIONS

    async def zadd(self, key, mapping):  # pragma: no cover - a refusal never registers
        raise AssertionError("an at-capacity refusal registered the principal")


def _scope_of(fake):
    @asynccontextmanager
    async def scope():
        yield fake

    return scope


@pytest.fixture
def numbers(monkeypatch):
    monkeypatch.setattr(ucm, "RATE_LIMIT_PER_MINUTE", RATE_LIMIT_FOR_TEST)
    monkeypatch.setattr(ucm, "MAX_CONCURRENT_SESSIONS", CAPACITY_FOR_TEST)


SCOPES = {
    "outage": lambda: _redis_down,
    "rate_limited": lambda: _scope_of(_OverTheRateLimit()),
    "at_capacity": lambda: _scope_of(_Full()),
}


def _capacity_reply(kind, path, accept, method="get"):
    ran = _Ran()
    with patch.object(ucm.RedisFactory, "redis_scope", side_effect=SCOPES[kind]()):
        client = TestClient(_capacity_app(ran), raise_server_exceptions=False)
        reply = getattr(client, method)(path, headers={"Accept": accept}, follow_redirects=False)
    return reply, ran


def _session_reply(path, accept, method="get"):
    ran = _Ran()
    client = TestClient(_session_app(ran), raise_server_exceptions=False)
    client.cookies.set("auth_token", "a-cookie-2431")
    reply = getattr(client, method)(path, headers={"Accept": accept}, follow_redirects=False)
    return reply, ran


def _assert_is_the_page(reply, line, status, retry_after):
    assert reply.status_code == status
    assert reply.headers["content-type"].startswith("text/html")
    assert reply.headers["Retry-After"] == retry_after
    assert "location" not in {k.lower() for k in reply.headers.keys()}
    body = reply.text
    assert f"<p>{line.replace(chr(39), '&#x27;')}</p>" in body
    assert '<a href="">Try again</a>' in body
    for leftover in ("{{", "{%", "{seconds}", "__PIPER_REFUSAL_MESSAGE__", "/login"):
        assert leftover not in body, leftover
    for word in CODE_WORDS:
        assert word not in body, word
    assert not body.lstrip().startswith("{")  # never raw JSON


# ---------------------------------------------------------------------------
# 1. The predicate, and that it is the only copy.
# ---------------------------------------------------------------------------


def _request(path, accept):
    request = MagicMock()
    request.url.path = path
    request.headers = {} if accept is None else {"accept": accept}
    return request


class TestThePredicate:
    @pytest.mark.parametrize(
        "path, accept, wanted",
        [
            ("/settings/integrations", HTML_ACCEPT, True),
            ("/settings/integrations", "text/html", True),
            ("/", HTML_ACCEPT, True),
            ("/login", HTML_ACCEPT, True),
            ("/settings/integrations", JSON_ACCEPT, False),
            ("/settings/integrations", "*/*", False),  # fetch()'s default
            ("/settings/integrations", "", False),
            ("/settings/integrations", None, False),  # no Accept header at all
            ("/api/v1/intent", HTML_ACCEPT, False),
            ("/api/v1/intent", JSON_ACCEPT, False),
            ("/api/v1/intent", None, False),
            ("/apiary", HTML_ACCEPT, True),  # only the /api/ prefix counts
        ],
    )
    def test_the_table(self, path, accept, wanted):
        assert wants_a_page(_request(path, accept)) is wanted

    @staticmethod
    def _function(path, name):
        tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
                return node
        raise AssertionError(f"{name} not found in {path}")

    @staticmethod
    def _calls(func, name):
        return [
            n
            for n in ast.walk(func)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name
        ]

    @pytest.mark.parametrize(
        "path, name",
        [
            ("services/auth/auth_middleware.py", "_unauthorized_response"),  # /login redirect
            ("web/app.py", "_not_found_negotiated"),  # issue 2039's negotiated 404
            ("services/auth/auth_middleware.py", "_service_unavailable_response"),
            ("web/middleware/usage_cap_middleware.py", "_rate_limited_response"),
            ("web/middleware/usage_cap_middleware.py", "_at_capacity_response"),
            ("web/middleware/usage_cap_middleware.py", "_redis_unavailable_response"),
        ],
    )
    def test_each_site_calls_the_predicate(self, path, name):
        assert len(self._calls(self._function(path, name), "wants_a_page")) == 1

    # What a copy looks like: a "text/html" membership test, or a read of the Accept
    # header. Scanned in every .py file under services/ and web/, comments stripped.
    COPY_SHAPES = (
        re.compile(r"""["']text/html["']\s+in\b"""),
        re.compile(r"""headers\.get\(\s*["']accept["']""", re.IGNORECASE),
        # a read, not an outgoing header being set (``headers["Accept"] = ...``)
        re.compile(r"""headers\[\s*["']accept["']\s*\](?!\s*=[^=])""", re.IGNORECASE),
    )

    def test_no_other_code_re_implements_it(self):
        found = []
        for folder in ("services", "web"):
            for path in sorted((ROOT / folder).rglob("*.py")):
                rel = path.relative_to(ROOT).as_posix()
                for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                    code = line.split("#", 1)[0]
                    if any(shape.search(code) for shape in self.COPY_SHAPES):
                        found.append(f"{rel}:{number}")
        # Only the predicate's own module: its code, and its docstring naming the shape.
        assert found and {f.split(":")[0] for f in found} == {
            "services/api/refusal_pages.py"
        }, found

    @pytest.mark.parametrize(
        "copy",
        [
            'accepts_html = "text/html" in accept_header',
            "if 'text/html' in request.headers.get('accept', ''):",
            'accept = request.headers.get("Accept")',
            'if "html" in request.headers["accept"]:',
        ],
    )
    def test_the_scan_catches_the_old_shapes(self, copy):
        assert any(shape.search(copy) for shape in self.COPY_SHAPES)


class TestTheOldCallSitesStillBehave:
    """The /login redirect and the JSON 401 are unchanged by the extraction."""

    def _no_token(self, path, accept):
        ran = _Ran()
        app = FastAPI()
        _routes(app, ran)
        app.add_middleware(AuthMiddleware, jwt_service=MagicMock())
        client = TestClient(app, raise_server_exceptions=False)
        return client.get(path, headers={"Accept": accept}, follow_redirects=False)

    def test_a_signed_out_page_load_still_redirects_to_login(self):
        reply = self._no_token(PAGE_PATH, HTML_ACCEPT)
        assert reply.status_code == 302
        assert reply.headers["location"] == "/login?next=%2Fsettings%2Fintegrations"

    @pytest.mark.parametrize("path, accept", [(PAGE_PATH, JSON_ACCEPT), (API_PATH, HTML_ACCEPT)])
    def test_a_signed_out_background_request_still_gets_the_json_401(self, path, accept):
        reply = self._no_token(path, accept)
        assert reply.status_code == 401
        assert reply.json()["error"] == "authentication_required"


# ---------------------------------------------------------------------------
# 2. The page: one constant, nothing that is down.
# ---------------------------------------------------------------------------


class TestThePage:
    def test_the_page_is_one_constant_with_one_slot(self):
        assert REFUSAL_PAGE_HTML.count("__PIPER_REFUSAL_MESSAGE__") == 1
        assert "{{" not in REFUSAL_PAGE_HTML and "{%" not in REFUSAL_PAGE_HTML

    def test_the_line_is_escaped_as_text(self):
        reply = refusal_page("<b>x</b> & 'y'", 503, 5)
        assert "<b>" not in reply.body.decode()
        assert "&lt;b&gt;x&lt;/b&gt; &amp; &#x27;y&#x27;" in reply.body.decode()

    def test_the_429_template_takes_a_whole_number_of_seconds(self):
        assert RATE_LIMITED_MESSAGE.format(seconds=int(37.9)) == CXO_RATE_LIMITED_37
        assert RATE_LIMITED_MESSAGE.count("{") == 1  # the one slot, {seconds}

    def test_the_page_puts_the_line_in_as_given(self):
        body = refusal_page(PIPER_CANT_TAKE_REQUESTS_MESSAGE, 503, 5).body.decode()
        assert CXO_OUTAGE.replace("'", "&#x27;") in body

    def test_the_module_imports_no_template_engine_session_or_redis(self):
        tree = ast.parse((ROOT / "services/api/refusal_pages.py").read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported |= {a.name for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                imported.add(node.module)
        assert imported == {"html", "starlette.requests", "starlette.responses"}

    def test_the_page_builds_with_the_template_engine_session_factory_and_redis_all_raising(
        self,
    ):
        """Each is patched to raise if touched; the page still builds, and so does the
        guard's whole refusal through the real middleware."""
        import jinja2
        from starlette.templating import Jinja2Templates

        from services.cache.redis_factory import RedisFactory
        from services.database.session_factory import AsyncSessionFactory

        def touched(*_a, **_k):
            raise AssertionError("the outage page touched something that is down")

        with (
            patch.object(jinja2.Environment, "get_template", touched),
            patch.object(jinja2.Environment, "from_string", touched),
            patch.object(Jinja2Templates, "TemplateResponse", touched),
            patch.object(AsyncSessionFactory, "session_scope", touched),
            patch.object(AsyncSessionFactory, "session_scope_fresh", touched),
            patch.object(RedisFactory, "create_client", touched),
        ):
            page = refusal_page(PIPER_CANT_TAKE_REQUESTS_MESSAGE, 503, 5)
            assert CXO_OUTAGE.replace("'", "&#x27;") in page.body.decode()
            # The whole refusal: the guard's own redis_scope raising is the outage itself.
            ran = _Ran()
            with patch.object(RedisFactory, "redis_scope", side_effect=_redis_down):
                reply = TestClient(_capacity_app(ran), raise_server_exceptions=False).get(
                    PAGE_PATH, headers={"Accept": HTML_ACCEPT}
                )
        _assert_is_the_page(reply, CXO_OUTAGE, 503, "5")
        assert ran.calls == []


# ---------------------------------------------------------------------------
# 3. The two outage 503s.
# ---------------------------------------------------------------------------


class TestTheCapacityGuardsOutage:
    def test_a_page_load_gets_the_page(self):
        reply, ran = _capacity_reply("outage", PAGE_PATH, HTML_ACCEPT)
        _assert_is_the_page(reply, CXO_OUTAGE, 503, "5")
        assert ran.calls == []

    @pytest.mark.parametrize("path, accept", [(PAGE_PATH, JSON_ACCEPT), (API_PATH, HTML_ACCEPT)])
    def test_a_background_request_gets_the_sentence_as_message(self, path, accept):
        reply, ran = _capacity_reply("outage", path, accept)
        assert reply.status_code == 503
        assert reply.headers["Retry-After"] == "5"
        assert reply.json() == {
            "error": "capacity_check_unavailable",
            "message": CXO_OUTAGE,
            "retry_after_seconds": 5,
        }
        assert ran.calls == []

    def test_nothing_was_changed_a_write_is_refused_before_the_route_runs(self):
        reply, ran = _capacity_reply("outage", API_PATH, JSON_ACCEPT, method="post")
        assert reply.status_code == 503 and ran.calls == []


class TestTheSessionOutage:
    def test_a_page_load_gets_the_page_and_no_redirect(self):
        reply, ran = _session_reply(PAGE_PATH, HTML_ACCEPT)
        _assert_is_the_page(reply, CXO_SESSION, 503, "5")
        assert ran.calls == []

    @pytest.mark.parametrize("path, accept", [(PAGE_PATH, JSON_ACCEPT), (API_PATH, HTML_ACCEPT)])
    def test_a_background_request_keeps_the_session_json(self, path, accept):
        reply, ran = _session_reply(path, accept)
        assert reply.status_code == 503
        assert reply.headers["Retry-After"] == "5"
        assert reply.json() == {
            "error": "verification_unavailable",
            "message": CXO_SESSION,
            "type": "service_unavailable",
        }
        assert ran.calls == []

    def test_nothing_was_changed_a_write_is_refused_before_the_route_runs(self):
        reply, ran = _session_reply(API_PATH, JSON_ACCEPT, method="post")
        assert reply.status_code == 503 and ran.calls == []


# ---------------------------------------------------------------------------
# 4. The 429 and at-capacity refusals.
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("numbers")
class TestTheRateLimit:
    def _assert_no_removed_number(self, text):
        assert str(RATE_LIMIT_FOR_TEST) not in text
        assert "requests/minute" not in text and "Rate limit" not in text

    def test_a_page_load_gets_the_page_with_the_real_seconds(self):
        reply, ran = _capacity_reply("rate_limited", PAGE_PATH, HTML_ACCEPT)
        _assert_is_the_page(reply, CXO_RATE_LIMITED_37, 429, str(SECONDS_LEFT))
        self._assert_no_removed_number(reply.text)
        assert ran.calls == []

    @pytest.mark.parametrize("path, accept", [(PAGE_PATH, JSON_ACCEPT), (API_PATH, HTML_ACCEPT)])
    def test_a_background_request_gets_the_sentence_as_message(self, path, accept):
        reply, ran = _capacity_reply("rate_limited", path, accept)
        assert reply.status_code == 429
        assert reply.headers["Retry-After"] == str(SECONDS_LEFT)
        assert reply.json() == {
            "error": "rate_limited",
            "message": CXO_RATE_LIMITED_37,
            "retry_after_seconds": SECONDS_LEFT,
        }
        self._assert_no_removed_number(reply.text)
        assert ran.calls == []

    def test_nothing_was_changed_a_write_is_refused_before_the_route_runs(self):
        reply, ran = _capacity_reply("rate_limited", API_PATH, JSON_ACCEPT, method="post")
        assert reply.status_code == 429 and ran.calls == []


@pytest.mark.usefixtures("numbers")
class TestAtCapacity:
    def _assert_no_removed_number(self, text):
        assert str(CAPACITY_FOR_TEST) not in text
        assert "active sessions" not in text and "Instance at capacity" not in text

    def test_a_page_load_gets_the_page(self):
        reply, ran = _capacity_reply("at_capacity", PAGE_PATH, HTML_ACCEPT)
        _assert_is_the_page(reply, CXO_FULL, 503, "30")
        self._assert_no_removed_number(reply.text)
        assert ran.calls == []

    @pytest.mark.parametrize("path, accept", [(PAGE_PATH, JSON_ACCEPT), (API_PATH, HTML_ACCEPT)])
    def test_a_background_request_gets_the_sentence_as_message(self, path, accept):
        reply, ran = _capacity_reply("at_capacity", path, accept)
        assert reply.status_code == 503
        assert reply.headers["Retry-After"] == "30"
        assert reply.json() == {
            "error": "at_capacity",
            "message": CXO_FULL,
            "retry_after_seconds": 30,
        }
        self._assert_no_removed_number(reply.text)
        assert ran.calls == []

    def test_nothing_was_changed_a_write_is_refused_before_the_route_runs(self):
        reply, ran = _capacity_reply("at_capacity", API_PATH, JSON_ACCEPT, method="post")
        assert reply.status_code == 503 and ran.calls == []


# ---------------------------------------------------------------------------
# 5. The words: CXO's, each written once.
# ---------------------------------------------------------------------------


class TestTheWords:
    def test_the_constants_carry_cxos_words(self):
        assert PIPER_CANT_TAKE_REQUESTS_MESSAGE == CXO_OUTAGE
        assert PIPER_IS_FULL_MESSAGE == CXO_FULL
        assert RATE_LIMITED_MESSAGE == CXO_RATE_LIMITED_37.replace("37", "{seconds}")
        assert SESSION_COULD_NOT_BE_CHECKED_MESSAGE == CXO_SESSION

    def test_each_sentence_is_written_exactly_once_as_its_constant(self):
        found = {
            PIPER_CANT_TAKE_REQUESTS_MESSAGE: [],
            PIPER_IS_FULL_MESSAGE: [],
            RATE_LIMITED_MESSAGE: [],
        }
        old = []
        for folder in ("services", "web"):
            for path in sorted((ROOT / folder).rglob("*.py")):
                rel = path.relative_to(ROOT).as_posix()
                for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                    if isinstance(node, ast.Constant) and isinstance(node.value, str):
                        for line in found:
                            if line in node.value:
                                found[line].append(rel)
                        if rel == "web/middleware/usage_cap_middleware.py" and any(
                            s in node.value
                            for s in ("Temporarily unable", "Instance at capacity", "Rate limit:")
                        ):
                            old.append(node.value)
        for line, paths in found.items():
            assert paths == ["services/api/errors.py"], (line[:30], paths)
        assert old == []

    def test_no_template_or_script_shows_a_refusal_code(self):
        """The codes stay for code and the log; no page names them (issue 2431 acceptance)."""
        found = []
        for folder, pattern in (("templates", "*.html"), ("web/static", "*.js")):
            for path in sorted((ROOT / folder).rglob(pattern)):
                text = path.read_text(encoding="utf-8", errors="replace")
                for word in ("capacity_check_unavailable", "verification_unavailable"):
                    if word in text:
                        found.append(f"{path.relative_to(ROOT)}: {word}")
                for word in ("rate_limited", "at_capacity"):
                    if re.search(rf"['\"]{word}['\"]", text):
                        found.append(f"{path.relative_to(ROOT)}: {word}")
        assert found == []


# ---------------------------------------------------------------------------
# 6. The pages read `message` through one shared reader.
# ---------------------------------------------------------------------------

READER = ROOT / "web/static/js/route-message.js"


class TestThePagesReader:
    def test_the_reader_sets_text_never_html(self):
        src = READER.read_text(encoding="utf-8")
        assert "element.textContent = text" in src
        assert "innerHTML" not in src and "insertAdjacentHTML" not in src
        assert "outerHTML" not in src and "document.write" not in src

    def test_the_reader_is_the_only_one(self):
        """No other script defines a reader of its own under the same name."""
        defining = [
            p.relative_to(ROOT).as_posix()
            for p in sorted((ROOT / "web/static").rglob("*.js"))
            if "window.RouteMessage" in p.read_text(encoding="utf-8", errors="replace")
        ]
        assert defining == ["web/static/js/route-message.js"]

    def test_the_shell_loads_the_reader_before_chat(self):
        shell = (ROOT / "templates/layouts/app_shell.html").read_text(encoding="utf-8")
        assert shell.index("/static/js/route-message.js") < shell.index("/static/js/chat.js")

    def test_the_sign_in_page_loads_the_reader_before_its_script(self):
        login = (ROOT / "templates/login.html").read_text(encoding="utf-8")
        assert login.index("/static/js/route-message.js") < login.index("/static/js/auth.js")

    def test_test_all_reads_message_and_falls_back_to_its_old_words(self):
        src = (ROOT / "templates/integrations.html").read_text(encoding="utf-8")
        start = src.index("async function testAllConnections")
        block = src[start : src.index("function updateLastUpdated", start)]
        assert "if (!response.ok)" in block
        assert (
            "Toast.show('error', 'Test Error', RouteMessage.read(body, "
            "'Failed to test connections'));" in block
        )
        # The old words appear twice: the reader's fallback, and the catch for a
        # network failure or an unreadable reply (no message came).
        assert block.count("'Failed to test connections'") == 2
        assert block.index("if (!response.ok)") < block.index("for (const result of results)")

    def test_the_toast_sets_its_message_as_text(self):
        src = (ROOT / "web/static/js/toast.js").read_text(encoding="utf-8")
        assert "messageEl.textContent = message;" in src

    def test_the_chat_reply_reads_message_and_falls_back_to_its_old_words(self):
        src = (ROOT / "web/static/js/chat.js").read_text(encoding="utf-8")
        # The intent reply's own non-OK branch (the one that used to throw).
        start = src.index("if (!response.ok) {", src.index("const sendIntent = () =>"))
        block = src[start : src.index("return;", start)]
        assert (
            'RouteMessage.show(refusedLine, result, result.detail || "An API error occurred");'
            in block
        )
        assert "innerHTML" not in block
        assert 'throw new Error(result.detail || "An API error occurred")' not in src

    def test_the_sign_in_reads_message_and_falls_back_to_its_old_words(self):
        src = (ROOT / "web/static/js/auth.js").read_text(encoding="utf-8")
        assert (
            "showError(RouteMessage.read(error, error.detail || "
            "'Invalid username or password'));" in src
        )
        assert "errorMessage.textContent = message;" in src

    @pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
    def test_the_reader_run_under_node(self):
        """The reader itself, run in node with a stand-in element (no browser, no DOM)."""
        script = (
            "const vm = require('vm');"
            "const fs = require('fs');"
            "const ctx = { window: {} };"
            f"vm.runInNewContext(fs.readFileSync({json.dumps(str(READER))}, 'utf8'), ctx);"
            "const R = ctx.window.RouteMessage;"
            "const el = { textContent: '' };"
            "const out = {"
            f"  outage: R.read({json.dumps({'error': 'capacity_check_unavailable', 'message': CXO_OUTAGE})}, 'Failed to test connections'),"
            "  none: R.read({ detail: 'x' }, 'Failed to test connections'),"
            "  empty: R.read({ message: '   ' }, 'fallback'),"
            "  notJson: R.read(null, 'fallback'),"
            "  nonString: R.read({ message: { a: 1 } }, 'fallback'),"
            "  shown: R.show(el, { message: '<b>x</b>' }, 'fallback'),"
            "};"
            "out.elementText = el.textContent;"
            "process.stdout.write(JSON.stringify(out));"
        )
        result = subprocess.run(
            ["node", "-e", script], capture_output=True, text=True, timeout=30, check=True
        )
        out = json.loads(result.stdout)
        assert out == {
            "outage": CXO_OUTAGE,
            "none": "Failed to test connections",
            "empty": "fallback",
            "notJson": "fallback",
            "nonString": "fallback",
            "shown": "<b>x</b>",
            "elementText": "<b>x</b>",
        }


def test_the_module_exposes_the_predicate_once():
    assert refusal_pages.wants_a_page is wants_a_page
