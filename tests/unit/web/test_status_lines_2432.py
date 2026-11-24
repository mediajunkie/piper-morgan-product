"""Issue 2432, steps 2 to 4: a 4xx's words reach a person only if they are vetted.

The Chief Architect's ruling (decisions.log 2026-11-24 11:50): an unmarked 4xx answers one
fixed line per status (the CXO's words, comment 7144095698) and its own detail goes to the
log; a ``UserFacingHTTPException`` with a 4xx status keeps its words; 401 and 404 keep their
lines; FastAPI's own request validation answers the CXO's fixed 422 sentence and logs field
names and error types only.

LAYER: the app's REAL handlers, taken from ``web.app`` and mounted on a small app, so each
assertion is on what a client receives; and an ``ast`` read of ``web/`` and ``services/``.
DENOMINATOR: every status with a line (nine and the catch-all), 401 and 404, the 5xx
branches, the validation handler; every ``UserFacingHTTPException`` call under both folders.
NOT COVERED: any rendered page. Nothing here was put on a screen.
"""

import ast
import re
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from pydantic import BaseModel

from services.api import errors
from services.api.errors import UserFacingHTTPException

ROOT = Path(__file__).resolve().parents[3]
POISON = "Traceback /srv/secret/path.py: KeyError('sk-ant-made-up') user_id=42"

# The CXO's ten lines, word for word (comment 7144095698, table C).
STATUS_LINES = {
    400: "I couldn't use that request. Check what you entered and try again.",
    403: "You don't have permission to do that.",
    405: "That isn't something I can do here.",
    409: "That conflicts with something that is already there.",
    410: "That is no longer available.",
    413: "That is too large for me to take.",
    415: "I can't use that kind of file.",
    422: "I couldn't read that request. Check what you entered and try again.",
    429: "That's more than I can take in a minute. Try again in a moment.",
}
CATCH_ALL = "I couldn't do that. Try again; if it keeps failing, tell us."

# Today's 401 and 404 replies, pinned from the handler before the change (2026-11-24).
BAD_CREDENTIALS = (
    "That email and password didn't work. Check both and try again, or use Forgot password."
)
SESSION_EXPIRED = "Let's try logging in again. Your session may have expired."
NOT_FOUND = "I couldn't find that. It may have been moved or deleted."
GENERIC_5XX = "Something went wrong on my end. I've logged the details for debugging."


def _app():
    from web.app import app as real_app

    app = FastAPI()
    app.add_exception_handler(HTTPException, real_app.exception_handlers[HTTPException])
    app.add_exception_handler(
        RequestValidationError, real_app.exception_handlers[RequestValidationError]
    )
    return app


def _reply(exc):
    app = _app()

    @app.get("/call")
    async def _call():
        raise exc

    return TestClient(app).get("/call")


def _both(reply, line):
    assert reply.json() == {"message": line, "detail": line}


class TestTheTenLines:
    def test_the_constants_are_the_cxos_words(self):
        assert errors.FOUR_XX_STATUS_LINES == STATUS_LINES
        assert errors.OTHER_CLIENT_ERROR_LINE == CATCH_ALL

    @pytest.mark.parametrize("status_code", sorted(STATUS_LINES))
    def test_an_unmarked_4xx_answers_its_status_line_and_none_of_its_own_words(self, status_code):
        reply = _reply(HTTPException(status_code=status_code, detail=POISON))
        assert reply.status_code == status_code
        _both(reply, STATUS_LINES[status_code])
        for word in ("Traceback", "secret", "sk-ant", "user_id"):
            assert word not in reply.text

    @pytest.mark.parametrize("status_code", [402, 406, 408, 411, 418, 423, 451])
    def test_any_other_4xx_answers_the_catch_all(self, status_code):
        reply = _reply(HTTPException(status_code=status_code, detail=POISON))
        assert reply.status_code == status_code
        _both(reply, CATCH_ALL)

    def test_a_specific_403_no_longer_passes_through(self):
        """The old 403 branch sent any non-bare detail (#1875). It goes (Arch, item 6)."""
        reply = _reply(HTTPException(status_code=403, detail="Only admins: " + POISON))
        _both(reply, STATUS_LINES[403])

    def test_the_old_422_wrapper_is_gone(self):
        reply = _reply(HTTPException(status_code=422, detail=[{"loc": ["body"], "msg": POISON}]))
        _both(reply, STATUS_LINES[422])
        assert "couldn't process" not in reply.text

    @pytest.mark.parametrize("status_code", sorted(STATUS_LINES) + [418])
    def test_a_marked_4xx_keeps_its_words(self, status_code):
        line = "A vetted line for the test."
        reply = _reply(UserFacingHTTPException(status_code=status_code, detail=line))
        assert reply.status_code == status_code
        _both(reply, line)

    def test_the_raisers_detail_goes_to_the_log(self):
        import web.app as web_app

        with patch.object(web_app, "logger") as logger:
            _reply(HTTPException(status_code=400, detail=POISON))
        (call,) = [c for c in logger.error.call_args_list if c.args == ("http_exception",)]
        assert call.kwargs["detail"] == POISON
        assert call.kwargs["status_code"] == 400


class TestWhatDidNotChange:
    def test_the_login_401_keeps_its_line(self):
        from web.api.routes.auth import BAD_CREDENTIALS_DETAIL

        reply = _reply(HTTPException(status_code=401, detail=BAD_CREDENTIALS_DETAIL))
        assert reply.status_code == 401
        _both(reply, BAD_CREDENTIALS)

    def test_every_other_401_is_the_session_line(self):
        reply = _reply(HTTPException(status_code=401, detail=POISON))
        _both(reply, SESSION_EXPIRED)

    def test_a_marked_401_is_still_the_session_line(self):
        reply = _reply(UserFacingHTTPException(status_code=401, detail="A marked 401."))
        _both(reply, SESSION_EXPIRED)

    def test_the_cookie_clearing_401_still_clears(self):
        from web.api.exceptions import HTTPExceptionWithCookieClear

        reply = _reply(
            HTTPExceptionWithCookieClear(
                status_code=401, detail=POISON, clear_cookies=["auth_token"]
            )
        )
        _both(reply, SESSION_EXPIRED)
        assert 'auth_token=""' in reply.headers["set-cookie"]

    @pytest.mark.parametrize("cls", [HTTPException, UserFacingHTTPException])
    def test_a_404_is_its_one_line(self, cls):
        reply = _reply(cls(status_code=404, detail=POISON))
        assert reply.status_code == 404
        _both(reply, NOT_FOUND)

    def test_an_unmarked_5xx_is_still_masked(self):
        reply = _reply(HTTPException(status_code=503, detail=POISON))
        _both(reply, GENERIC_5XX)

    def test_a_marked_5xx_still_keeps_its_words(self):
        reply = _reply(UserFacingHTTPException(status_code=503, detail="A vetted 503."))
        _both(reply, "A vetted 503.")


class Body2432(BaseModel):
    count: int
    email_address: str


class TestTheValidation422:
    def _post(self, payload):
        app = _app()

        @app.post("/typed")
        async def _typed(body: Body2432):
            return {"ok": True}

        return TestClient(app).post("/typed", json=payload)

    def test_a_bad_body_answers_the_fixed_sentence_in_both_keys(self):
        reply = self._post({"count": "sk-ant-made-up-value", "unexpected": 1})
        assert reply.status_code == 422
        _both(reply, STATUS_LINES[422])
        for word in (
            "count",
            "email_address",
            "int_parsing",
            "missing",
            "loc",
            "msg",
            "pydantic",
            "Input should",
            "sk-ant-made-up-value",
            "body",
        ):
            assert word not in reply.text, word

    def test_the_log_names_fields_and_error_types_and_no_value(self):
        import web.app as web_app

        with patch.object(web_app, "logger") as logger:
            self._post({"count": "sk-ant-made-up-value"})
        (call,) = logger.warning.call_args_list
        assert call.args == ("request_validation_failed",)
        assert sorted(call.kwargs["fields"]) == ["body.count", "body.email_address"]
        assert sorted(call.kwargs["error_types"]) == ["int_parsing", "missing"]
        assert "sk-ant-made-up-value" not in repr(call)
        assert "Input should" not in repr(call)

    def test_the_real_app_carries_the_handler(self):
        """A typed route of the real app: setup's request model refuses a provider."""
        import uuid

        from services.auth.container import AuthContainer
        from web.app import app

        token = AuthContainer.get_jwt_service().generate_access_token(
            user_id=uuid.uuid4(), user_email="u2432@example.invalid", scopes=["user"]
        )
        client = TestClient(app, follow_redirects=False)
        client.cookies.set("auth_token", token)
        with patch("web.api.routes.setup.AsyncSessionFactory"):
            reply = client.post(
                "/api/v1/setup/complete", json={"default_llm_provider": "not-a-provider"}
            )
        assert reply.status_code == 422
        _both(reply, STATUS_LINES[422])
        assert "default_llm_provider" not in reply.text


def _picker_names():
    from tests.unit.web.test_setup_lines_reach_the_page_2428 import DETAIL_PICKERS

    return set(DETAIL_PICKERS)


def _status_is_4xx(code):
    text = ast.unparse(code).replace("status.", "")
    return bool(re.fullmatch(r"4\d\d", text) or re.match(r"HTTP_4\d\d", text))


def _echo_problems(func, call, pickers):
    """Why a marked 4xx's ``detail`` could echo what the person sent, or [] if it cannot:
    an f-string piece; a name that is a parameter of the enclosing function; any attribute
    read off such a parameter (``request.role``, ``req.provider``). Arguments to a listed
    picker are skipped: the 2428 guard reads that picker's body and holds every return to
    an UPPER_CASE constant or None, so what it is given cannot reach its result."""
    detail = {k.arg: k.value for k in call.keywords}.get("detail")
    if detail is None:
        return ["no detail keyword"]
    params = set()
    if func is not None:
        a = func.args
        params = {p.arg for p in a.posonlyargs + a.args + a.kwonlyargs + [a.vararg, a.kwarg] if p}
    skip = set()
    for node in ast.walk(detail):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in pickers
        ):
            for arg in node.args + [k.value for k in node.keywords]:
                skip.update(id(n) for n in ast.walk(arg))
        # Issue 2432 (Arch, mail 01M87QXPZZ): what sits inside a bare ``int(<expr>)`` is
        # skipped. ``int()`` returns a whole number or raises, so no text a person sent
        # can come out of it. The 2428 guard holds the surrounding shape to
        # ``UPPER_CASE_TEMPLATE.format(<name>=int(<expr>))``.
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "int"
            and len(node.args) == 1
            and not node.keywords
        ):
            skip.update(id(n) for n in ast.walk(node.args[0]))
    problems = []
    for node in ast.walk(detail):
        if id(node) in skip:
            continue
        if isinstance(node, (ast.JoinedStr, ast.FormattedValue)):
            problems.append("f-string")
        elif isinstance(node, ast.Name) and node.id in params:
            problems.append(f"parameter {node.id}")
    return problems


def _marked_4xx_calls():
    for folder in ("web", "services"):
        for path in sorted((ROOT / folder).rglob("*.py")):
            text = path.read_text(encoding="utf-8")
            if "UserFacingHTTPException" not in text:
                continue
            tree = ast.parse(text)
            owner = {}
            for func in ast.walk(tree):
                if isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    for node in ast.walk(func):
                        owner[id(node)] = func  # innermost wins: walk order is outer first
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id == "UserFacingHTTPException"
                ):
                    keywords = {k.arg: k.value for k in node.keywords}
                    code = keywords.get("status_code") or (node.args[0] if node.args else None)
                    if code is not None and _status_is_4xx(code):
                        yield path.relative_to(ROOT).as_posix(), owner.get(id(node)), node


class TestNoMarked4xxEchoesWhatThePersonSent:
    """The echo scan (brief item "Echo scan"). For every ``UserFacingHTTPException`` call
    with a 4xx status under ``web/`` and ``services/``: its ``detail`` holds no f-string and
    no name that is a parameter of the enclosing function (so no ``request.x``/``req.x``,
    which are reads off a parameter). CANNOT SEE: a value that reaches a module-level
    UPPER_CASE name at run time (the 2428 guard is what refuses non-constant names, and a
    constant assigned at import from request data is impossible); a local variable that
    copies a parameter (the 2428 guard refuses any lower-case name as a detail, so such a
    variable can only appear as a listed picker's argument, which this scan skips by
    design); raises through a helper that builds the exception elsewhere."""

    def test_there_are_marked_4xx_calls_to_scan(self):
        assert len(list(_marked_4xx_calls())) >= 90

    def test_none_echoes(self):
        pickers = _picker_names()
        found = []
        for path, func, call in _marked_4xx_calls():
            problems = _echo_problems(func, call, pickers)
            if problems:
                found.append(f"{path}:{call.lineno}: {problems}")
        assert found == []

    @pytest.mark.parametrize(
        "source, caught",
        [
            ('def f(request):\n    UserFacingHTTPException(400, detail=f"{request.role}")', True),
            ("def f(req):\n    UserFacingHTTPException(400, detail=req.provider)", True),
            ("def f(value):\n    UserFacingHTTPException(400, detail=value)", True),
            ("def f(value):\n    UserFacingHTTPException(400, detail=LINE)", False),
            ('def f(value):\n    UserFacingHTTPException(400, detail="fixed")', False),
            (
                "def f(name):\n    UserFacingHTTPException(409, detail=not_offered_line(name))",
                False,
            ),
            ("def f(name):\n    UserFacingHTTPException(409, detail=other_call(name))", True),
        ],
    )
    def test_the_scan_sees_the_shapes_it_is_for(self, source, caught):
        func = ast.parse(source).body[0]
        call = func.body[0].value
        problems = _echo_problems(func, call, {"not_offered_line", "password_rule_line"})
        assert bool(problems) is caught


class TestNoUnmarked4xxCanReachTheClientWithItsOwnWords:
    """By the handler's code path: the one branch that sends ``exc.detail`` for a 4xx is
    guarded by ``user_facing``. Shown here by reading the handler's source once, beside the
    behavioural tests above (every status with a line, and the catch-all)."""

    def test_the_handler_sends_a_4xx_detail_only_when_marked(self):
        src = (ROOT / "web/app.py").read_text(encoding="utf-8")
        tree = ast.parse(src)
        (handler,) = [
            n
            for n in ast.walk(tree)
            if isinstance(n, ast.AsyncFunctionDef) and n.name == "http_exception_handler"
        ]
        body = ast.unparse(handler)
        assert "400 <= exc.status_code < 500 and getattr(exc, 'user_facing', False)" in body
        assert "friendly_message = status_line_for(exc.status_code)" in body
        # The only assignments of the raiser's detail to the reply: the marked 4xx and 5xx
        # branches, and the <400 fallback that no 4xx reaches.
        sends_detail = [
            n
            for n in ast.walk(handler)
            if isinstance(n, ast.Assign)
            and ast.unparse(n.value) == "str(exc.detail)"
            and ast.unparse(n.targets[0]) == "friendly_message"
        ]
        assert len(sends_detail) == 3


class TestTheResetPageKeepsItsLengthRule:
    """Arch, mail 01M87RHFPQ (2026-11-24): the reset request carried ``min_length=8`` on its
    two password fields, so pydantic refused a short password before the route ran and,
    with the validation 422 now one fixed line, the person would have lost "at least 8
    characters". The rule lives in ``PasswordValidator`` only. LAYER: the real app, its
    real handlers and the real route, through a TestClient; the short password is refused
    before any database read, so none is needed."""

    @staticmethod
    def _post(new, confirm):
        from web.app import app

        return TestClient(app, follow_redirects=False).post(
            "/api/v1/auth/reset-password",
            json={
                "reset_token": "a-made-up-code",
                "new_password": new,
                "new_password_confirm": confirm,
            },
        )

    def test_a_seven_character_password_gets_the_length_line_not_the_422_line(self):
        from services.api.errors import UNREADABLE_REQUEST_LINE

        reply = self._post("Abc12!x", "Abc12!x")
        assert reply.status_code == 400
        line = "Your password needs at least 8 characters."
        assert reply.json() == {"message": line, "detail": line}
        assert UNREADABLE_REQUEST_LINE not in reply.text

    def test_a_mismatched_pair_gets_the_mismatch_line(self):
        reply = self._post("Abcdef12!", "Abcdef12?")
        assert reply.status_code == 400
        assert reply.json()["message"] == "The new passwords don't match."

    def test_a_password_with_no_listed_special_character_is_told_which_count(self):
        reply = self._post("Abcdefg12-", "Abcdefg12-")
        assert reply.status_code == 400
        assert reply.json()["message"] == (
            "Your password needs a special character, such as ! @ # $ % ^ & * ( )."
        )

    def test_the_reset_request_holds_no_length_rule_of_its_own(self):
        from web.api.routes.auth import PasswordResetRequest

        for name in ("new_password", "new_password_confirm"):
            assert PasswordResetRequest.model_fields[name].metadata == []

    def test_a_missing_reset_code_is_still_a_validation_422(self):
        from services.api.errors import UNREADABLE_REQUEST_LINE

        reply = TestClient(__import__("web.app", fromlist=["app"]).app).post(
            "/api/v1/auth/reset-password",
            json={"reset_token": "", "new_password": "x", "new_password_confirm": "x"},
        )
        assert reply.status_code == 422
        assert reply.json()["message"] == UNREADABLE_REQUEST_LINE
