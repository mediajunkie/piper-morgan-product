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
(14 with issue 2345's). The other route files are not covered here; the sweep is on the issue.
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

# No setup 5xx line stays masked. The two that told an operator which environment variables
# to set left this list on 2026-11-24 (issue 2345, CXO): the wizard's page now gets
# "Google Calendar sign-in isn't set up on this server." or its Slack twin, and the variable
# names are logged. A new unmarked 5xx in the setup routes is a CXO ruling, added here.
KEPT_MASKED = ()

# CXO's words of 2026-11-24 for the two database lines (mail 01M8749H51): each says the
# own-computer case and the hosted case, and the command carries no quote marks.
DATABASE_LINE = (
    "Cannot connect to the database. If you run Piper on your own computer, make sure "
    "Docker is running, then start the services with: docker compose up -d postgres redis "
    "chromadb. Then try again. On a hosted instance, tell the person who runs it."
)
TABLES_LINE = (
    "Database tables are missing. If you run Piper on your own computer, create them with: "
    "python -m alembic upgrade head. Then try again. On a hosted instance, tell the person "
    "who runs it."
)
VETTED_LINES = (
    setup.SETUP_COULD_NOT_BE_CHECKED_MESSAGE,
    setup.SYSTEM_CHECK_COULD_NOT_RUN_MESSAGE,
    setup.INVITE_CHECK_COULD_NOT_RUN_MESSAGE,
    TABLES_LINE,
    DATABASE_LINE,
    setup.ACCOUNT_COULD_NOT_BE_CREATED_MESSAGE,
    setup.SERVER_CANNOT_STORE_KEYS_MESSAGE,
    setup.SETUP_COULD_NOT_FINISH_MESSAGE,
    setup.PROJECT_COULD_NOT_BE_CREATED_MESSAGE,
    setup.SLACK_CONNECT_COULD_NOT_START_MESSAGE,
    setup.CALENDAR_CONNECT_COULD_NOT_START_MESSAGE,
    setup.CALENDAR_CONNECT_COULD_NOT_START_MESSAGE,  # 2345: the same line when Redis is down
    setup.CALENDAR_SIGN_IN_NOT_SET_UP_MESSAGE,  # 2345, CXO: Google's client not configured
    setup.SLACK_SIGN_IN_NOT_SET_UP_MESSAGE,  # 2345, CXO: Slack's client not configured
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
    def test_the_denominator_is_fourteen_5xx_raises(self):
        assert len(_five_xx_raises()) == 14  # thirteen, and 2345's Redis-down refusal

    def test_every_setup_5xx_is_marked(self):
        unmarked = [
            _detail_value(detail)
            for _, callee, _, detail in _five_xx_raises()
            if callee == "HTTPException"
        ]
        assert len(unmarked) == len(KEPT_MASKED)
        for line in unmarked:
            assert line and KEPT_MASKED and line.startswith(KEPT_MASKED), line

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


class TestArchsGuardOverEveryMarkedRaise:
    """Arch, 2026-11-24 (mail 01M8742TG4): across ``web/`` and ``services/``, the detail of
    every ``UserFacingHTTPException(...)`` call is a string literal or a module-level
    UPPER_CASE constant. An f-string, ``str(e)``, a concatenation or an ordinary variable
    fails, so exception text cannot reach a person through the one path the handler does
    not mask (2402's rule). DENOMINATOR: every Python file under both folders."""

    @staticmethod
    def _marked_calls():
        calls = []
        for folder in ("web", "services"):
            for path in sorted((ROOT / folder).rglob("*.py")):
                text = path.read_text(encoding="utf-8")
                if "UserFacingHTTPException" not in text:
                    continue
                for node in ast.walk(ast.parse(text)):
                    if (
                        isinstance(node, ast.Call)
                        and isinstance(node.func, ast.Name)
                        and node.func.id == "UserFacingHTTPException"
                    ):
                        calls.append((path.relative_to(ROOT).as_posix(), node))
        return calls

    def test_the_guard_sees_the_known_sites(self):
        files = {path for path, _ in self._marked_calls()}
        assert files == {"web/api/routes/setup.py", "web/api/routes/settings_integrations.py"}
        per_file = {}
        for path, _ in self._marked_calls():
            per_file[path] = per_file.get(path, 0) + 1
        # setup.py: the eleven vetted lines, and 2345's two (Redis down at the Calendar
        # start; Google's client not configured). settings_integrations.py: eight
        # preferences reads, the Notion check, the GitHub token read, and 2345's two starts.
        assert per_file == {
            "web/api/routes/setup.py": 14,
            "web/api/routes/settings_integrations.py": 12,
        }

    def test_every_marked_detail_is_a_literal_or_an_upper_case_constant(self):
        """No exception to the rule (Arch, mail 01M8762YMW): a ``.format`` on a template
        would trust every caller to pass a literal, which the guard cannot see."""
        for path, node in self._marked_calls():
            keywords = {k.arg: k.value for k in node.keywords}
            assert "detail" in keywords, f"{path}:{node.lineno}: detail must be a keyword"
            detail = keywords["detail"]
            ok = (isinstance(detail, ast.Constant) and isinstance(detail.value, str)) or (
                isinstance(detail, ast.Name) and detail.id.isupper()
            )
            assert ok, f"{path}:{node.lineno}: {ast.unparse(detail)[:70]}"

    @pytest.mark.parametrize(
        "source",
        [
            'UserFacingHTTPException(status_code=500, detail=f"failed: {e}")',
            "UserFacingHTTPException(status_code=500, detail=str(e))",
            'UserFacingHTTPException(status_code=500, detail="a" + reason)',
            "UserFacingHTTPException(status_code=500, detail=error_msg)",
            "UserFacingHTTPException(status_code=503, detail=TEMPLATE.format(thing=thing))",
        ],
    )
    def test_the_rule_refuses_the_shapes_arch_named(self, source):
        detail = {k.arg: k.value for k in ast.parse(source).body[0].value.keywords}["detail"]
        fixed = (isinstance(detail, ast.Constant) and isinstance(detail.value, str)) or (
            isinstance(detail, ast.Name) and detail.id.isupper()
        )
        assert not fixed


class TestThePreferencesLinesAreWrittenWhole:
    """Arch 2026-11-24: one constant per sentence, each written whole. Pinned to #2154's
    template with its old ``thing``, so no word changed and CXO has nothing new to read."""

    THINGS = {
        "SLACK_PREFS_LOAD_FAILED_MESSAGE": "your Slack preferences",
        "CALENDAR_CHOICES_LOAD_FAILED_MESSAGE": "your saved calendar choices",
        "CALENDAR_PREFS_LOAD_FAILED_MESSAGE": "your Google Calendar preferences",
        "NOTION_DATABASE_CHOICES_LOAD_FAILED_MESSAGE": "your saved database choices",
        "NOTION_PREFS_LOAD_FAILED_MESSAGE": "your Notion preferences",
        "GITHUB_REPOSITORY_CHOICES_LOAD_FAILED_MESSAGE": "your saved repository choices",
        "GITHUB_PREFS_LOAD_FAILED_MESSAGE": "your GitHub preferences",
    }

    @pytest.mark.parametrize("name", sorted(THINGS))
    def test_each_constant_equals_the_template_with_its_thing(self, name):
        from web.api.routes import settings_integrations as si

        assert getattr(si, name) == si.PREFS_LOAD_FAILED_TEMPLATE.format(thing=self.THINGS[name])

    def test_no_preferences_line_is_built_at_run_time_any_more(self):
        src = (ROOT / "web/api/routes/settings_integrations.py").read_text(encoding="utf-8")
        assert "PREFS_LOAD_FAILED_TEMPLATE.format(" not in src
        assert "_prefs_unavailable" not in src
        for thing in self.THINGS.values():
            assert src.count(f'"{thing}"') == 0, thing  # only inside its whole sentence

    async def test_a_failed_read_raises_the_callers_own_line(self):
        from unittest.mock import AsyncMock

        from web.api.routes import settings_integrations as si

        unavailable = UserFacingHTTPException(
            status_code=503, detail=si.SLACK_PREFS_LOAD_FAILED_MESSAGE
        )
        with patch.object(
            si, "_load_prefs_db", AsyncMock(side_effect=si.PreferencesReadFailed("x"))
        ):
            with pytest.raises(UserFacingHTTPException) as raised:
                await si._load_prefs_or_503("u-1", "slack", unavailable)
        assert raised.value is unavailable and raised.value.status_code == 503
