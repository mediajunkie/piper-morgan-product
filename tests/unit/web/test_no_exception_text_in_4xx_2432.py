"""Issue 2432, step 1: no 4xx reply carries an exception's own text.

Five routes answered a 4xx with ``detail=str(e)``, and the app's handler passes a 4xx's
words through to the person (a 404 excepted, which always gets one fixed line). Each now
answers with a fixed line in the CXO's words (mail 01M87HSM8A, 2026-11-24); the
exception's text stays in the log. The Chief Architect ruled this as the first step
(decisions.log 2026-11-24 11:50), ahead of the per-status default and the marks.

LAYER: each route's function, called with the one failure patched in, inside a small app
that carries the app's REAL ``HTTPException`` handler, so the assertion is on what a
client receives; and an ``ast`` read of ``web/`` and ``services/``.
DENOMINATOR: the six ``str(e)`` sites the 4xx sweep found (five the CXO worded and the
document search's 403), plus the four other 404 sites in the documents routes that shared
the first one's shape; and every ``HTTPException``-family raise under both folders.
NOT COVERED: the rendered page; the 34 other 4xx details that are not fixed lines (the
issue's later rows).
"""

import ast
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[3]
NOT_FOUND_LINE = "I couldn't find that. It may have been moved or deleted."
# Text that must never reach a client: what the patched failures carry.
POISON = "Traceback /srv/secret/path.py line 42: KeyError('sk-ant-made-up')"

USER = SimpleNamespace(
    sub="u-2432",
    user_id=UUID("00000000-0000-0000-0000-000000002432"),
    user_email="t2432@example.invalid",
    username="t2432",
)


def _through_the_real_handler(route_function):
    """What a client receives when ``route_function`` raises, by the app's real handler."""
    from web.app import app as real_app

    app = FastAPI()
    app.add_exception_handler(HTTPException, real_app.exception_handlers[HTTPException])

    @app.get("/call")
    async def _call():
        return await route_function()

    return TestClient(app).get("/call")


def _fake_scope():
    session = AsyncMock()
    scope = AsyncMock()
    scope.__aenter__ = AsyncMock(return_value=session)
    scope.__aexit__ = AsyncMock(return_value=None)
    return scope


def _assert_line(reply, status_code, line):
    assert reply.status_code == status_code, reply.text
    assert reply.json() == {"message": line, "detail": line}
    assert "Traceback" not in reply.text and "secret" not in reply.text
    assert "sk-ant" not in reply.text


class TestTheKeyRoutes:
    def test_a_refused_store_says_the_cxos_line(self):
        from web.api.routes import api_keys

        service = MagicMock()
        service.store_user_key = AsyncMock(side_effect=ValueError(POISON))
        request = api_keys.StoreKeyRequest(provider="anthropic", api_key="made-up-key-value")

        async def call():
            with patch.object(
                api_keys.AsyncSessionFactory, "session_scope", return_value=_fake_scope()
            ):
                return await api_keys.store_api_key(
                    req=MagicMock(), request=request, current_user=USER, service=service
                )

        _assert_line(
            _through_the_real_handler(call),
            400,
            "That key couldn't be saved. Check the provider and the key, then try again.",
        )

    def test_a_refused_replace_says_the_cxos_line(self):
        from web.api.routes import api_keys

        service = MagicMock()
        service.rotate_user_key = AsyncMock(side_effect=ValueError(POISON))
        request = api_keys.RotateKeyRequest(new_api_key="made-up-key-value")

        async def call():
            with patch.object(
                api_keys.AsyncSessionFactory, "session_scope", return_value=_fake_scope()
            ):
                return await api_keys.rotate_api_key(
                    provider="anthropic",
                    req=MagicMock(),
                    request=request,
                    current_user=USER,
                    service=service,
                )

        _assert_line(
            _through_the_real_handler(call),
            400,
            "That key couldn't be replaced. Check the provider and the key, then try again.",
        )


class TestThePasswordRoute:
    def test_a_service_refusal_says_the_fallback_line(self):
        """The service's ValueError here is not a password rule (the rules are checked
        earlier, by ``PasswordValidator``); on main it can only be "User not found"."""
        from services.auth.models import PasswordChangeRequest
        from web.api.routes import auth

        jwt_service = MagicMock()
        jwt_service.change_password = AsyncMock(side_effect=ValueError(POISON))
        data = PasswordChangeRequest(
            current_password="Made-up-Old-Passw0rd!",
            new_password="Made-up-New-Passw0rd!",
            new_password_confirm="Made-up-New-Passw0rd!",
        )

        async def call():
            with (
                patch.object(auth.db, "_initialized", True, create=True),
                patch.object(
                    auth.AsyncSessionFactory, "session_scope_fresh", return_value=_fake_scope()
                ),
                patch.object(auth, "PasswordService", MagicMock()),
            ):
                return await auth.change_password(
                    request=MagicMock(),
                    data=data,
                    current_user=USER,
                    credentials=SimpleNamespace(credentials="made-up-token"),
                    jwt_service=jwt_service,
                )

        _assert_line(
            _through_the_real_handler(call),
            400,
            "That password can't be used. Choose a different one.",
        )


class TestTheTimeZoneRoute:
    def test_an_unknown_zone_says_the_cxos_line_and_does_not_echo_the_value(self):
        from web.api.routes import preferences

        async def call():
            with patch.object(
                preferences.preference_manager,
                "set_reminder_timezone",
                AsyncMock(side_effect=ValueError("Unknown timezone 'Mars/Olympus_Mons' " + POISON)),
            ):
                return await preferences.set_timezone(
                    preferences.SetTimezoneRequest(timezone="Mars/Olympus_Mons"), current_user=USER
                )

        reply = _through_the_real_handler(call)
        _assert_line(
            reply, 400, "That isn't a time zone I recognise. Use a name like America/Los_Angeles."
        )
        assert "Mars" not in reply.text


class TestTheDocumentRoutes:
    def test_the_search_key_refusal_says_the_routes_vetted_line(self):
        """The refusal's own text is developer wording that cites issue numbers."""
        from services.llm.request_key import UserLLMKeyRequiredError
        from web.api.routes import documents

        async def refusing(**_kwargs):
            raise UserLLMKeyRequiredError(
                "Authenticated caller has no LLM key of their own (#1807/#1812). " + POISON
            )

        async def call():
            with (
                patch.object(documents, "resolve_user_openai_key", AsyncMock(return_value="k")),
                patch.object(documents, "handle_search_documents", refusing),
            ):
                return await documents.search_documents(q="pricing", current_user=USER)

        reply = _through_the_real_handler(call)
        _assert_line(reply, 403, documents.SEARCH_KEY_REQUIRED_DETAIL)
        assert "#1807" not in reply.text

    def test_a_missing_document_never_sends_the_exceptions_text(self):
        """The handler gives every 404 its own fixed line, so the route's line is the belt:
        if that handler branch ever changed, a file path still could not reach the page."""
        from web.api.routes import documents

        assert documents.DOCUMENT_NOT_FOUND_MESSAGE == "I couldn't find that document."
        src = (ROOT / "web/api/routes/documents.py").read_text(encoding="utf-8")
        assert src.count("detail=DOCUMENT_NOT_FOUND_MESSAGE") == 5

        app = FastAPI()
        from web.app import app as real_app

        app.add_exception_handler(HTTPException, real_app.exception_handlers[HTTPException])

        @app.get("/call")
        async def _call():
            raise HTTPException(status_code=404, detail=documents.DOCUMENT_NOT_FOUND_MESSAGE)

        reply = TestClient(app).get("/call")
        assert reply.status_code == 404
        assert reply.json() == {"message": NOT_FOUND_LINE, "detail": NOT_FOUND_LINE}


class TestNoRaiseSendsAnExceptionsText:
    """Across ``web/`` and ``services/``: no ``HTTPException``-family raise, of any status,
    passes ``str(<name>)`` as its whole ``detail``. (An f-string that embeds one is a 5xx
    in every case found, which the handler masks; the 4xx f-strings are the issue's later
    rows.) DENOMINATOR: every Python file under both folders."""

    NAMES = {"HTTPException", "HTTPExceptionWithCookieClear", "UserFacingHTTPException"}

    def _offenders(self):
        found = []
        for folder in ("web", "services"):
            for path in sorted((ROOT / folder).rglob("*.py")):
                text = path.read_text(encoding="utf-8")
                if "HTTPException" not in text or "str(" not in text:
                    continue
                for node in ast.walk(ast.parse(text)):
                    if not (
                        isinstance(node, ast.Call)
                        and isinstance(node.func, ast.Name)
                        and node.func.id in self.NAMES
                    ):
                        continue
                    detail = {k.arg: k.value for k in node.keywords}.get("detail")
                    if detail is None and len(node.args) > 1:
                        detail = node.args[1]
                    if (
                        isinstance(detail, ast.Call)
                        and isinstance(detail.func, ast.Name)
                        and detail.func.id == "str"
                    ):
                        found.append(f"{path.relative_to(ROOT).as_posix()}:{node.lineno}")
        return found

    def test_none_does(self):
        assert self._offenders() == []

    @pytest.mark.parametrize(
        "source, caught",
        [
            ("HTTPException(status_code=400, detail=str(e))", True),
            ("HTTPException(400, str(exc))", True),
            ("HTTPException(status_code=400, detail=FIXED_LINE)", False),
            ('HTTPException(status_code=400, detail="a fixed line")', False),
        ],
    )
    def test_the_scan_sees_the_shape_it_is_for(self, source, caught):
        node = ast.parse(source).body[0].value
        detail = {k.arg: k.value for k in node.keywords}.get("detail")
        if detail is None and len(node.args) > 1:
            detail = node.args[1]
        is_str_call = (
            isinstance(detail, ast.Call)
            and isinstance(detail.func, ast.Name)
            and detail.func.id == "str"
        )
        assert is_str_call is caught
