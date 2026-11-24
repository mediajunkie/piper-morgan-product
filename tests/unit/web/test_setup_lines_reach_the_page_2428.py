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


# Issue 2430 (Arch, mail 01M8786G87): the closed list of picker functions a marked
# ``detail=`` may call. The guard reads each one's body and fails unless every ``return``
# is an UPPER_CASE name or ``None``. A new entry here is a diff Arch reads.
DETAIL_PICKERS = ("github_degrade_fixed_line",)


def _returns_only_constants(func):
    """True when every ``return`` in ``func`` is an UPPER_CASE name or ``None``."""
    returns = [n for n in ast.walk(func) if isinstance(n, ast.Return)]
    if not returns:
        return False
    for node in returns:
        value = node.value
        ok = (
            value is None
            or (isinstance(value, ast.Constant) and value.value is None)
            or (isinstance(value, ast.Name) and value.id.isupper())
        )
        if not ok:
            return False
    return True


def _picker_definitions(name):
    """Every function named ``name`` defined under ``web/`` and ``services/``."""
    found = []
    for folder in ("web", "services"):
        for path in sorted((ROOT / folder).rglob("*.py")):
            text = path.read_text(encoding="utf-8")
            if f"def {name}" not in text:
                continue
            for node in ast.walk(ast.parse(text)):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
                    found.append(node)
    return found


def _detail_problem(detail, find_definitions=_picker_definitions):
    """None when a marked ``detail`` is allowed, else why not: a string literal, an
    UPPER_CASE name, or a call to a listed picker whose body returns only constants."""
    if isinstance(detail, ast.Constant) and isinstance(detail.value, str):
        return None
    if isinstance(detail, ast.Name) and detail.id.isupper():
        return None
    if isinstance(detail, ast.Call) and isinstance(detail.func, ast.Name):
        name = detail.func.id
        if name not in DETAIL_PICKERS:
            return f"{name} is not on the closed list of pickers"
        definitions = find_definitions(name)
        if len(definitions) != 1:
            return f"{name} is defined {len(definitions)} times, not once"
        if not _returns_only_constants(definitions[0]):
            return f"{name} returns something other than an UPPER_CASE name or None"
        return None
    return "not a literal, an UPPER_CASE name or a listed picker"


def _renaming_imports(tree):
    """Line numbers of every import that binds ``UserFacingHTTPException`` to another name."""
    return [
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
        if alias.name.split(".")[-1] == "UserFacingHTTPException"
        and alias.asname not in (None, "UserFacingHTTPException")
    ]


def _fixed_line_or_whole_number_format(node):
    """Issue 2431's sink rule (Arch, mail 01M87EY4N7): a string literal, an UPPER_CASE name,
    or ``UPPER_CASE_TEMPLATE.format(<name>=int(<expr>))`` with keyword arguments only, at
    least one, each value a call to the bare name ``int`` with one positional argument."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return True
    if isinstance(node, ast.Name):
        return node.id.isupper()
    if not (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "format"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id.isupper()
    ):
        return False
    if node.args or not node.keywords:
        return False
    for keyword in node.keywords:
        value = keyword.value
        if keyword.arg is None:  # **mapping
            return False
        if not (
            isinstance(value, ast.Call)
            and isinstance(value.func, ast.Name)
            and value.func.id == "int"
            and len(value.args) == 1
            and not value.keywords
        ):
            return False
    return True


class TestArchsGuardOverEveryMarkedRaise:
    """Arch, 2026-11-24 (mail 01M8742TG4): across ``web/`` and ``services/``, the detail of
    every ``UserFacingHTTPException(...)`` call is a string literal or a module-level
    UPPER_CASE constant. An f-string, ``str(e)``, a concatenation or an ordinary variable
    fails, so exception text cannot reach a person through the one path the handler does
    not mask (2402's rule). One allowance (issue 2430, Arch mail 01M8786G87): a call to a
    picker on ``DETAIL_PICKERS`` whose every ``return`` is an UPPER_CASE name or None.
    DENOMINATOR: every Python file under both folders."""

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

    @staticmethod
    def _trees():
        for folder in ("web", "services"):
            for path in sorted((ROOT / folder).rglob("*.py")):
                text = path.read_text(encoding="utf-8")
                yield path.relative_to(ROOT).as_posix(), text

    def test_the_guard_sees_the_known_sites(self):
        per_file = {}
        for path, _ in self._marked_calls():
            per_file[path] = per_file.get(path, 0) + 1
        # setup.py: the eleven vetted lines, and 2345's three (Redis down at the Calendar
        # start; Google's and Slack's clients not configured). settings_integrations.py:
        # eight preferences reads, the Notion check, the GitHub token read, 2345's two
        # starts and (issue 2430) the repository list's named degrade line. Issue 2429: the
        # session line at the refresh route, standup's dependency and get_current_user; the
        # admin and operations-reader gates.
        assert per_file == {
            "web/api/routes/setup.py": 14,
            "web/api/routes/settings_integrations.py": 13,
            "web/api/routes/auth.py": 1,
            "web/api/routes/standup.py": 1,
            "services/auth/auth_middleware.py": 3,
        }

    def test_no_import_renames_the_class(self):
        """Issue 2429 (Arch): ``import ... as`` would hide a call from this guard, which
        reads calls by the name ``UserFacingHTTPException``."""
        renamed = []
        for path, text in self._trees():
            if "UserFacingHTTPException" not in text:
                continue
            renamed += [f"{path}:{line}" for line in _renaming_imports(ast.parse(text))]
        assert renamed == []

    def test_the_class_is_never_called_through_an_attribute(self):
        """``errors.UserFacingHTTPException(...)`` would also escape the by-name read."""
        found = []
        for path, text in self._trees():
            if "UserFacingHTTPException" not in text:
                continue
            for node in ast.walk(ast.parse(text)):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "UserFacingHTTPException"
                ):
                    found.append(f"{path}:{node.lineno}")
        assert found == []

    @pytest.mark.parametrize(
        "source",
        [
            "from services.api.errors import UserFacingHTTPException as Shown",
            "from web.api.exceptions import UserFacingHTTPException as UFE",
        ],
    )
    def test_the_rename_rule_refuses_an_alias(self, source):
        assert _renaming_imports(ast.parse(source)) == [1]

    def test_the_rename_rule_allows_the_plain_import(self):
        assert (
            _renaming_imports(ast.parse("from services.api.errors import UserFacingHTTPException"))
            == []
        )

    def test_every_middleware_503_message_is_a_literal_or_an_upper_case_constant(self):
        """Issue 2429: ``AuthMiddleware._service_unavailable_response`` builds its own 503,
        which never passes the app's handler, so its message reaches the client as
        written. The same rule as a marked detail holds for every call."""
        calls = []
        for path, text in self._trees():
            if "_service_unavailable_response" not in text:
                continue
            for node in ast.walk(ast.parse(text)):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "_service_unavailable_response"
                ):
                    calls.append((path, node))
        assert [path for path, _ in calls] == ["services/auth/auth_middleware.py"]
        for path, node in calls:
            keywords = {k.arg: k.value for k in node.keywords}
            message = node.args[0] if node.args else keywords.get("message")
            ok = (isinstance(message, ast.Constant) and isinstance(message.value, str)) or (
                isinstance(message, ast.Name) and message.id.isupper()
            )
            assert ok, f"{path}:{node.lineno}: {ast.unparse(message)[:70] if message else None}"

    # Issue 2431 (Arch's ruling, item 4, and his addendum, mail 01M87EY4N7): the page
    # builder and all four of the capacity guard's refusal builders (the outage, the 429
    # and at capacity) join the sinks. A message there is a literal, an UPPER_CASE name,
    # or exactly ``UPPER_CASE_TEMPLATE.format(<name>=int(<expr>))``: keywords only, each a
    # call to the builtin ``int``. The one pass-through allowed is
    # ``_service_unavailable_response`` handing on its own ``message`` parameter, whose
    # every caller the test above already reads.
    REFUSAL_PAGE_PASS_THROUGH = {"_service_unavailable_response": "message"}
    CAPACITY_REFUSALS = (
        "_rate_limited_response",
        "_at_capacity_response",
        "_redis_unavailable_response",
    )

    @staticmethod
    def _fixed_line(node):
        return _fixed_line_or_whole_number_format(node)

    @pytest.mark.parametrize(
        "source",
        [
            "RATE_LIMITED_MESSAGE",
            "'a literal line'",
            "RATE_LIMITED_MESSAGE.format(seconds=int(retry_after))",
            "RATE_LIMITED_MESSAGE.format(seconds=int(max(2, retry_after)))",  # the floor (CXO)
            "TEMPLATE.format(seconds=int(a), minutes=int(b))",
        ],
    )
    def test_the_sink_rule_allows_the_ruled_shapes(self, source):
        assert _fixed_line_or_whole_number_format(ast.parse(source, mode="eval").body)

    @pytest.mark.parametrize(
        "source",
        [
            "RATE_LIMITED_MESSAGE.format(seconds=retry_after)",  # not an int(...) call
            "RATE_LIMITED_MESSAGE.format(seconds=str(retry_after))",
            "RATE_LIMITED_MESSAGE.format(thing=thing)",  # this morning's ruling stands
            "RATE_LIMITED_MESSAGE.format(int(retry_after))",  # a positional argument
            "RATE_LIMITED_MESSAGE.format(int(a), seconds=int(b))",
            "rate_limited_message.format(seconds=int(retry_after))",  # lowercase template
            "RATE_LIMITED_MESSAGE.format(seconds=x.int(retry_after))",  # int as an attribute
            "RATE_LIMITED_MESSAGE.format(**values)",
            "RATE_LIMITED_MESSAGE.format()",
            "RATE_LIMITED_MESSAGE.format(seconds=int(a, b))",
            "RATE_LIMITED_MESSAGE.replace('{seconds}', str(n))",
            "fill_in_seconds(RATE_LIMITED_MESSAGE, n)",
            "f'Try again in {n} seconds.'",
            "message",
        ],
    )
    def test_the_sink_rule_refuses_every_other_shape(self, source):
        assert not _fixed_line_or_whole_number_format(ast.parse(source, mode="eval").body)

    def _refusal_page_calls(self):
        """(path, enclosing function name, call) for every ``refusal_page(...)`` call."""
        calls = []
        for path, text in self._trees():
            if "refusal_page" not in text:
                continue
            for func in ast.walk(ast.parse(text)):
                if not isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                for node in ast.walk(func):
                    if (
                        isinstance(node, ast.Call)
                        and isinstance(node.func, ast.Name)
                        and node.func.id == "refusal_page"
                    ):
                        calls.append((path, func.name, node))
        return calls

    def test_the_guard_sees_the_known_refusal_page_sites(self):
        per_file = {}
        for path, _, _ in self._refusal_page_calls():
            per_file[path] = per_file.get(path, 0) + 1
        # The capacity guard's three refusals, and the auth middleware's session 503.
        assert per_file == {
            "web/middleware/usage_cap_middleware.py": 3,
            "services/auth/auth_middleware.py": 1,
        }

    def test_every_refusal_page_message_is_a_literal_or_an_upper_case_constant(self):
        for path, enclosing, node in self._refusal_page_calls():
            keywords = {k.arg: k.value for k in node.keywords}
            message = node.args[0] if node.args else keywords.get("message")
            passed_on = (
                isinstance(message, ast.Name)
                and self.REFUSAL_PAGE_PASS_THROUGH.get(enclosing) == message.id
            )
            assert (
                self._fixed_line(message) or passed_on
            ), f"{path}:{node.lineno}: {ast.unparse(message)[:70] if message else None}"

    def test_refusal_page_is_never_renamed_or_called_through_an_attribute(self):
        found = []
        for path, text in self._trees():
            if "refusal_page" not in text:
                continue
            for node in ast.walk(ast.parse(text)):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    found += [
                        f"{path}:{node.lineno}"
                        for alias in node.names
                        if alias.name.split(".")[-1] == "refusal_page"
                        and alias.asname not in (None, "refusal_page")
                    ]
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "refusal_page"
                ):
                    found.append(f"{path}:{node.lineno}")
        assert found == []

    def test_every_capacity_refusal_message_is_a_fixed_line(self):
        """Each of the capacity guard's three refusal builders sends a JSON ``message`` that
        passes the sink rule (the 429's is the one ``.format(seconds=int(...))``)."""
        tree = ast.parse((ROOT / "web/middleware/usage_cap_middleware.py").read_text())
        seen = {}
        for func in ast.walk(tree):
            if not (isinstance(func, ast.FunctionDef) and func.name in self.CAPACITY_REFUSALS):
                continue
            for node in ast.walk(func):
                if not isinstance(node, ast.Dict):
                    continue
                for key, value in zip(node.keys, node.values):
                    if not (isinstance(key, ast.Constant) and key.value == "message"):
                        continue
                    seen[func.name] = seen.get(func.name, 0) + 1
                    assert _fixed_line_or_whole_number_format(
                        value
                    ), f"{func.name}:{node.lineno}: {ast.unparse(value)[:70]}"
        assert seen == {name: 1 for name in self.CAPACITY_REFUSALS}

    def test_only_the_429_uses_the_format_shape(self):
        """At capacity and the outage are plain constants; the 429 alone formats, and only
        with ``seconds=int(...)``."""
        tree = ast.parse((ROOT / "web/middleware/usage_cap_middleware.py").read_text())
        formats = [
            ast.unparse(node)
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "format"
        ]
        assert formats == ["RATE_LIMITED_MESSAGE.format(seconds=int(max(2, retry_after)))"] * 2

    def test_every_marked_detail_is_a_literal_or_an_upper_case_constant(self):
        """No exception to the rule (Arch, mail 01M8762YMW): a ``.format`` on a template
        would trust every caller to pass a literal, which the guard cannot see."""
        for path, node in self._marked_calls():
            keywords = {k.arg: k.value for k in node.keywords}
            assert "detail" in keywords, f"{path}:{node.lineno}: detail must be a keyword"
            detail = keywords["detail"]
            problem = _detail_problem(detail)
            assert problem is None, f"{path}:{node.lineno}: {ast.unparse(detail)[:70]}: {problem}"

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
        assert _detail_problem(detail) is not None

    @staticmethod
    def _detail_of(source):
        return {k.arg: k.value for k in ast.parse(source).body[0].value.keywords}["detail"]

    def test_the_closed_list_holds_one_picker(self):
        assert DETAIL_PICKERS == ("github_degrade_fixed_line",)

    def test_the_allowance_refuses_a_function_not_on_the_list(self):
        detail = self._detail_of(
            "UserFacingHTTPException(status_code=502, detail=github_degrade_reply(d))"
        )
        assert "not on the closed list" in _detail_problem(detail)

    @pytest.mark.parametrize(
        "body",
        [
            "    return degradation.user_message",
            "    if x:\n        return LINE\n    return getattr(d, 'user_message', '')",
            '    return f"{LINE}"',
            "    return line",
            "    return LINE + OTHER",
            "    pass",
        ],
    )
    def test_the_allowance_refuses_a_listed_picker_with_a_bad_return(self, body):
        picker = ast.parse(f"def github_degrade_fixed_line(degradation):\n{body}\n").body[0]
        detail = self._detail_of(
            "UserFacingHTTPException(status_code=502, detail=github_degrade_fixed_line(d))"
        )
        problem = _detail_problem(detail, find_definitions=lambda _name: [picker])
        assert problem is not None and "returns something other" in problem

    def test_the_allowance_accepts_a_listed_picker_with_constant_returns(self):
        picker = ast.parse(
            "def github_degrade_fixed_line(d):\n    if d:\n        return LINE\n    return None\n"
        ).body[0]
        detail = self._detail_of(
            "UserFacingHTTPException(status_code=502, detail=github_degrade_fixed_line(d))"
        )
        assert _detail_problem(detail, find_definitions=lambda _name: [picker]) is None

    def test_the_real_picker_passes_the_body_read(self):
        (definition,) = _picker_definitions("github_degrade_fixed_line")
        assert _returns_only_constants(definition)


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
