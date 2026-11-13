"""#2089 / #2088: the hosted wizard has no System step and asks for the invite first.

CXO's rulings (2026-10-19 13:54): hosted order 1 Invite -> 2 API Keys -> 3 Account
-> 4 Projects -> 5 Complete; skip the System check on hosted with no replacement
and no "skipped" words; self-host unchanged; the code is checked at step 1
without being spent (it is spent only at Create Account, #1344).
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from jinja2 import Environment, FileSystemLoader

from services.auth.invite_token_service import check_invite_token
from web.api.routes import setup as setup_routes

REPO_ROOT = Path(__file__).resolve().parents[3]


def _render(hosted: bool) -> str:
    env = Environment(loader=FileSystemLoader(str(REPO_ROOT / "templates")))
    return env.get_template("setup.html").render(asset_v="t", hosted=hosted)


class TestRender:
    def test_hosted_has_no_system_step_and_starts_at_the_invite(self):
        html = _render(True)
        assert 'data-hosted="true"' in html
        assert "1. Invite" in html
        assert "1. System" not in html
        assert "System Requirements" not in html
        assert "check-system-btn" not in html
        assert 'id="invite-token-first"' in html
        assert (
            "Piper is invite-only while it's in private beta. Paste the code you received." in html
        )
        # carried hidden to Create Account, never asked twice
        assert re.search(r'<input type="hidden" id="invite-token"', html)
        assert 'for="invite-token"' not in html
        assert "skipped" not in html.lower()

    def test_hosted_still_has_five_steps(self):
        html = _render(True)
        assert len(re.findall(r'class="step(?: active)?" data-step="\d"', html)) == 5

    def test_self_host_is_unchanged(self):
        html = _render(False)
        assert 'data-hosted="false"' in html
        assert "1. System" in html
        assert "System Requirements" in html
        assert 'id="check-system-btn"' in html
        assert 'id="invite-token-first"' not in html
        assert 'for="invite-token"' in html  # step 3 still asks

    @pytest.mark.asyncio
    async def test_setup_page_passes_hosted_from_the_server(self):
        from web.api.routes.ui import setup_page

        tpl = MagicMock()
        with (
            patch("web.api.routes.ui._get_templates", return_value=tpl),
            patch("web.api.routes.ui.wizard_is_hosted", return_value=True),
        ):
            await setup_page(MagicMock())
        ctx = tpl.TemplateResponse.call_args.args[1]
        assert ctx["hosted"] is True

    def test_hosted_is_the_same_signal_the_docker_check_trusts(self):
        assert setup_routes.wizard_is_hosted() is setup_routes._IN_DOCKER


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(setup_routes.router)
    return TestClient(app)


def _scope(session):
    scope = MagicMock()
    scope.__aenter__ = AsyncMock(return_value=session)
    scope.__aexit__ = AsyncMock(return_value=False)
    return scope


class TestCheckInviteRoute:
    def test_a_valid_code_answers_valid_and_spends_nothing(self):
        with (
            patch.object(
                setup_routes.AsyncSessionFactory,
                "session_scope_fresh",
                return_value=_scope(AsyncMock()),
            ),
            patch.object(
                setup_routes, "check_invite_token", new=AsyncMock(return_value=True)
            ) as chk,
            patch.object(setup_routes, "consume_invite_token", new=AsyncMock()) as burn,
        ):
            r = _client().post("/api/v1/setup/check-invite", json={"invite_token": "abcd-efgh"})
        assert r.status_code == 200, r.text
        assert r.json() == {"valid": True, "message": None}
        chk.assert_awaited_once()
        burn.assert_not_awaited()

    def test_a_refused_code_gets_cxos_sentence(self):
        with (
            patch.object(
                setup_routes.AsyncSessionFactory,
                "session_scope_fresh",
                return_value=_scope(AsyncMock()),
            ),
            patch.object(setup_routes, "check_invite_token", new=AsyncMock(return_value=False)),
        ):
            r = _client().post("/api/v1/setup/check-invite", json={"invite_token": "nope"})
        assert r.status_code == 200
        assert r.json()["valid"] is False
        assert r.json()["message"] == (
            "That code isn't valid or has already been used. Check it and try again, "
            "or ask whoever sent it for a new one."
        )

    def test_an_empty_code_is_a_422_not_a_query(self):
        with patch.object(setup_routes, "check_invite_token", new=AsyncMock()) as chk:
            r = _client().post("/api/v1/setup/check-invite", json={"invite_token": ""})
        assert r.status_code == 422
        chk.assert_not_awaited()

    def test_a_db_failure_is_a_503_that_names_no_token(self):
        broken = MagicMock()
        broken.__aenter__ = AsyncMock(side_effect=RuntimeError("secret-token-text"))
        broken.__aexit__ = AsyncMock(return_value=False)
        with patch.object(
            setup_routes.AsyncSessionFactory, "session_scope_fresh", return_value=broken
        ):
            r = _client().post("/api/v1/setup/check-invite", json={"invite_token": "abcd"})
        assert r.status_code == 503
        assert "secret-token-text" not in r.text

    def test_the_route_is_a_read_not_behind_the_lockout(self):
        route = next(r for r in setup_routes.router.routes if r.path.endswith("/check-invite"))
        calls = {d.call for d in route.dependant.dependencies if d.call is not None}
        assert setup_routes.require_setup_incomplete not in calls


class TestCheckInviteToken:
    @pytest.mark.asyncio
    async def test_issues_a_select_never_an_update(self):
        session = AsyncMock()
        result = MagicMock()
        result.scalar_one_or_none.return_value = "ABCDEFGHJKMNPQRSTVWXYZ01"
        session.execute = AsyncMock(return_value=result)
        assert await check_invite_token(session, "abcd-efgh") is True
        stmt = session.execute.await_args.args[0]
        assert str(stmt).lstrip().upper().startswith("SELECT")
        assert "UPDATE" not in str(stmt).upper()

    @pytest.mark.asyncio
    async def test_an_unknown_or_spent_code_is_false(self):
        session = AsyncMock()
        result = MagicMock()
        result.scalar_one_or_none.return_value = None
        session.execute = AsyncMock(return_value=result)
        assert await check_invite_token(session, "zzzz") is False

    @pytest.mark.asyncio
    async def test_an_empty_code_never_queries(self):
        session = AsyncMock()
        assert await check_invite_token(session, " -- ") is False
        session.execute.assert_not_awaited()


class TestWizardScript:
    def test_hosted_continue_checks_the_invite_before_step_2(self):
        js = (REPO_ROOT / "web/static/js/setup.js").read_text()
        assert "document.body.dataset.hosted === 'true'" in js
        fn = js[
            js.index("async function continueFromInviteStep") : js.index(
                "document.getElementById('next-1').addEventListener"
            )
        ]
        assert fn.index("fetch('/api/v1/setup/check-invite'") < fn.index("showStep(2)")
        assert "document.getElementById('invite-token').value = code" in fn
        assert "That code isn't valid or has already been used" in fn
        tail = js[js.index("document.getElementById('next-1').addEventListener") :]
        assert "if (hosted)" in tail[:200]

    def test_the_system_check_handler_is_guarded_so_hosted_does_not_throw(self):
        js = (REPO_ROOT / "web/static/js/setup.js").read_text()
        assert "if (checkSystemBtn) checkSystemBtn.addEventListener" in js
        assert "document.getElementById('check-system-btn').addEventListener" not in js
