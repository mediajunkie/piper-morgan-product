"""Issue 2428: the setup routes' own 5xx lines reach the page.

The app's error handler replaces the detail of every 5xx with one generic line unless the
exception is marked ``user_facing`` (#2154). The setup routes raised their vetted lines
unmarked, so a person saw "Something went wrong on my end…" in place of every one of them
(found by rendering issue 2386's database line on a local server, 2026-11-24).

LAYER: the app's REAL ``HTTPException`` handler, taken from ``web.app`` and mounted on a
small app, as ``test_setup_wizard_step1_honest_1875`` does; the create-user route called
through that handler with its database session replaced; and an ``ast`` read of
``web/api/routes/setup.py``.
DENOMINATOR: every ``HTTPException``-family raise with a 5xx status in the setup routes
(13). The other route files are not covered here; the sweep is on the issue.
NOT COVERED: the page's rendering of the line (a served or local render, on the issue).
"""

import ast
import re
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from web.api.exceptions import UserFacingHTTPException
from web.api.routes import setup

ROOT = Path(__file__).resolve().parents[3]
SRC = (ROOT / "web/api/routes/setup.py").read_text(encoding="utf-8")
TREE = ast.parse(SRC)
GENERIC = "Something went wrong on my end. I've logged the details for debugging."

# The two 5xx lines that stay masked: they tell an operator which environment variables
# to set, and are not worded for a person on the page. Changing this set is a CXO ruling.
KEPT_MASKED = (
    "Slack OAuth not configured.",
    "Google Calendar OAuth not configured.",
)

DATABASE_LINE = (
    "Cannot connect to the database. Make sure Docker is running, then start the "
    "services with: docker compose up -d postgres redis chromadb. Then try again."
)
VETTED_LINES = (
    "Couldn't verify setup state — try again in a moment.",
    setup.SYSTEM_CHECK_COULD_NOT_RUN_MESSAGE,
    "The invite check couldn't run. Try again in a moment.",
    "Database tables are missing. Run 'python -m alembic upgrade head' to create them, "
    "then try again.",
    DATABASE_LINE,
    setup.ACCOUNT_COULD_NOT_BE_CREATED_MESSAGE,
    setup.SERVER_CANNOT_STORE_KEYS_MESSAGE,
    setup.SETUP_COULD_NOT_FINISH_MESSAGE,
    setup.PROJECT_COULD_NOT_BE_CREATED_MESSAGE,
    setup.SLACK_CONNECT_COULD_NOT_START_MESSAGE,
    setup.CALENDAR_CONNECT_COULD_NOT_START_MESSAGE,
)


def _real_handler():
    from web.app import app as real_app  # the handler is registered on the module-level app

    return real_app.exception_handlers[HTTPException]


def _five_xx_raises():
    """(lineno, callee name, status source, detail node) for every 5xx raise."""
    found = []
    for node in ast.walk(TREE):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
            continue
        if node.func.id not in ("HTTPException", "UserFacingHTTPException"):
            continue
        keywords = {k.arg: k.value for k in node.keywords}
        if "status_code" not in keywords or "detail" not in keywords:
            continue
        code = ast.unparse(keywords["status_code"]).replace("status.", "")
        if re.fullmatch(r"50\d", code) or re.match(r"HTTP_50\d", code):
            found.append((node.lineno, node.func.id, code, keywords["detail"]))
    return found


def _detail_value(node):
    """The line a detail node stands for: a string literal, or a module constant's value."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return getattr(setup, node.id)
    return None


class TestTheHandler:
    @pytest.mark.parametrize("status_code", [500, 503])
    @pytest.mark.parametrize("line", VETTED_LINES)
    def test_a_marked_5xx_reaches_the_client_as_written(self, line, status_code):
        app = FastAPI()
        app.add_exception_handler(HTTPException, _real_handler())

        @app.get("/raise")
        async def _raise():
            raise UserFacingHTTPException(status_code=status_code, detail=line)

        reply = TestClient(app).get("/raise")
        assert reply.status_code == status_code
        assert reply.json() == {"message": line, "detail": line}

    def test_an_unmarked_5xx_is_still_masked(self):
        app = FastAPI()
        app.add_exception_handler(HTTPException, _real_handler())

        @app.get("/raise")
        async def _raise():
            raise HTTPException(status_code=500, detail="OSError: [Errno 61] at /srv/secret/path")

        reply = TestClient(app).get("/raise")
        assert reply.json() == {"message": GENERIC, "detail": GENERIC}


class TestEverySetupSite:
    def test_the_denominator_is_thirteen_5xx_raises(self):
        assert len(_five_xx_raises()) == 13

    def test_every_5xx_is_marked_except_the_two_operator_lines(self):
        unmarked = [
            _detail_value(detail)
            for _, callee, _, detail in _five_xx_raises()
            if callee == "HTTPException"
        ]
        assert len(unmarked) == len(KEPT_MASKED)
        for line in unmarked:
            assert line and line.startswith(KEPT_MASKED), line

    def test_the_marked_lines_are_exactly_the_vetted_ones(self):
        marked = [
            _detail_value(detail)
            for _, callee, _, detail in _five_xx_raises()
            if callee == "UserFacingHTTPException"
        ]
        assert sorted(marked) == sorted(VETTED_LINES)

    def test_a_marked_detail_is_a_fixed_line_never_built_from_an_exception(self):
        """A literal or a module constant only: no f-string, no call, no variable, so no
        exception text, path or name can ride a line the handler will not mask."""
        for lineno, callee, _, detail in _five_xx_raises():
            if callee != "UserFacingHTTPException":
                continue
            fixed = isinstance(detail, ast.Constant) or (
                isinstance(detail, ast.Name) and detail.id.isupper()
            )
            assert fixed, f"setup.py:{lineno}: {ast.unparse(detail)[:60]}"
        for name in dir(setup):
            if name.endswith("_MESSAGE") and isinstance(getattr(setup, name), str):
                assert "{" not in getattr(setup, name), name

    def test_no_marked_line_carries_exception_words(self):
        for line in VETTED_LINES:
            for word in ("Traceback", "Error:", "Errno", "Exception", "/app/", "sqlalchemy"):
                assert word not in line, line


class TestTheDatabaseLineThroughTheRoute:
    def test_create_user_with_the_database_unreachable_says_the_ruled_line(self):
        """Issue 2386's second string, at the layer a person reads: the create-user route
        run through the real handler, with the database session raising as it does when
        Postgres's port is closed."""
        app = FastAPI()
        app.add_exception_handler(HTTPException, _real_handler())
        app.include_router(setup.router)

        def unreachable(*_args, **_kwargs):
            raise OSError("Multiple exceptions: [Errno 61] Connect call failed ('127.0.0.1', 5499)")

        body = {
            "username": "t2428",
            "email": "t2428@example.invalid",
            "password": "Made-up-Passw0rd-2428!",
            "password_confirm": "Made-up-Passw0rd-2428!",
            "invite_token": "MADEUP-2428",
        }
        with patch.object(setup.AsyncSessionFactory, "session_scope_fresh", unreachable):
            reply = TestClient(app).post("/api/v1/setup/create-user", json=body)
        assert reply.status_code == 500
        assert reply.json() == {"message": DATABASE_LINE, "detail": DATABASE_LINE}
        assert "Errno" not in reply.text and "5499" not in reply.text
