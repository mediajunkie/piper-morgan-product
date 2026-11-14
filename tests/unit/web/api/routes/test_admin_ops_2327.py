"""#2327: the counter's narrow read gate and the admin control for narrow flags.

Arch's rulings (2026-11-14), HOST's custody:
- The counter read is behind ``require_ops_reader`` (an admin, or an account holding
  ``users.ops_reader``), NOT ``require_admin``: a test account must not become an
  admin to read one counter. That gate opens this one route and nothing else.
- One admin-only control sets narrow flags on one named account. The flags are a
  closed list in code; ``is_admin`` is never settable from it.

LAYER: the dependency functions with their database read replaced at the one seam,
the live routers' declared dependencies, the route functions with the flag service
replaced, and source pins on the page. The flag service's SQL and its evidence line
are in tests/integration/test_floored_action_counter_2327.py.
DENOMINATOR: allowed, refused, check unavailable; every route file in the app for
the gate's use; the closed list; unknown flag, unknown account; the page's words.
"""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from services.auth import auth_middleware, narrow_flags
from services.auth.auth_middleware import require_admin, require_ops_reader
from web.api.routes import admin_ops

ROOT = Path(__file__).resolve().parents[5]
CLAIMS = SimpleNamespace(user_id="11111111-1111-1111-1111-111111111111")


def _deps(router, path, method):
    route = next(r for r in router.routes if r.path == path and method in r.methods)
    return {d.call for d in route.dependant.dependencies}


class TestTheReadGate:
    async def test_an_allowed_account_passes(self):
        with patch.object(auth_middleware, "_user_can_read_ops", AsyncMock(return_value=True)):
            assert await require_ops_reader(CLAIMS) is CLAIMS

    async def test_any_other_account_is_refused(self):
        with patch.object(auth_middleware, "_user_can_read_ops", AsyncMock(return_value=False)):
            with pytest.raises(HTTPException) as refused:
                await require_ops_reader(CLAIMS)
        assert refused.value.status_code == 403

    async def test_a_failed_check_refuses_never_allows(self):
        boom = AsyncMock(side_effect=RuntimeError("db down"))
        with patch.object(auth_middleware, "_user_can_read_ops", boom):
            with pytest.raises(HTTPException) as refused:
                await require_ops_reader(CLAIMS)
        assert refused.value.status_code == 503

    @pytest.mark.parametrize(
        "row,allowed",
        [
            (SimpleNamespace(is_admin=True, ops_reader=False), True),
            (SimpleNamespace(is_admin=False, ops_reader=True), True),
            (SimpleNamespace(is_admin=False, ops_reader=False), False),
            (None, False),
        ],
    )
    async def test_the_live_read_is_admin_or_the_flag(self, row, allowed):
        session = AsyncMock()
        session.get = AsyncMock(return_value=row)
        scope = AsyncMock()
        scope.__aenter__ = AsyncMock(return_value=session)
        scope.__aexit__ = AsyncMock(return_value=None)
        with patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
            return_value=scope,
        ):
            assert await auth_middleware._user_can_read_ops(CLAIMS.user_id) is allowed


class TestWhichRouteUsesWhichGate:
    def test_the_counter_read_uses_the_narrow_gate_and_not_the_admin_one(self):
        deps = _deps(admin_ops.router, "/api/v1/admin/floored-actions", "GET")
        assert require_ops_reader in deps
        assert require_admin not in deps

    @pytest.mark.parametrize("method", ["GET", "POST"])
    def test_the_flag_control_is_admin_only(self, method):
        deps = _deps(admin_ops.router, "/api/v1/admin/account-flags", method)
        assert require_admin in deps
        assert require_ops_reader not in deps

    def test_no_other_route_in_the_app_uses_the_narrow_gate(self):
        """Arch 11-14: ``ops_reader`` opens the counter read and nothing else. Every
        Python file under web/ and services/ is read for a use of the gate as a
        dependency; exactly one exists, on the counter route."""
        uses = {}
        for folder in ("web", "services"):
            for path in (ROOT / folder).rglob("*.py"):
                count = path.read_text(encoding="utf-8").count("Depends(require_ops_reader)")
                if count:
                    uses[path.relative_to(ROOT).as_posix()] = count
        assert uses == {"web/api/routes/admin_ops.py": 1}

    def test_the_page_is_admin_only(self):
        from web.api.routes import ui

        assert require_admin in _deps(ui.router, "/settings/account-flags", "GET")

    async def test_a_non_admin_gets_403_on_the_page_and_both_flag_routes(self):
        """Arch's condition for the ledger row (2026-11-14, the #2081 precedent): the
        page and both API routes run ``require_admin``, and that dependency, run for
        real with only its database read replaced, refuses a non-admin with 403."""
        from web.api.routes import ui

        gated = [
            _deps(ui.router, "/settings/account-flags", "GET"),
            _deps(admin_ops.router, "/api/v1/admin/account-flags", "GET"),
            _deps(admin_ops.router, "/api/v1/admin/account-flags", "POST"),
        ]
        assert all(require_admin in deps for deps in gated)
        with patch.object(auth_middleware, "_user_is_admin", AsyncMock(return_value=False)):
            with pytest.raises(HTTPException) as refused:
                await require_admin(CLAIMS)
        assert refused.value.status_code == 403

    def test_no_chat_or_agent_path_can_set_a_narrow_flag(self):
        """Arch's condition: outside the gate, the flag service, the admin route file
        and the model, no code under services/ or web/ names the flag or its setter
        (comments aside). A privilege flag set from chat would be a write on
        interpreted meaning to a permission."""
        allowed = {
            "services/auth/auth_middleware.py",
            "services/auth/narrow_flags.py",
            "services/database/models.py",
            "web/api/routes/admin_ops.py",
        }
        import io
        import tokenize

        # Code tokens only: a comment or a docstring that mentions the flag is not a
        # code path. A NAME token is an identifier the code actually uses.
        watched = {"ops_reader", "narrow_flags", "set_flag"}
        offenders = []
        for folder in ("web", "services"):
            for path in (ROOT / folder).rglob("*.py"):
                rel = path.relative_to(ROOT).as_posix()
                if rel in allowed:
                    continue
                text = path.read_text(encoding="utf-8")
                if not any(word in text for word in watched):
                    continue
                for token in tokenize.generate_tokens(io.StringIO(text).readline):
                    if token.type == tokenize.NAME and token.string in watched:
                        offenders.append(f"{rel}:{token.start[0]}: {token.string}")
        assert offenders == []

    def test_the_counter_rows_have_exactly_the_four_keys(self):
        assert admin_ops.FLOORED_ACTION_ROW_KEYS == ("name", "site", "day", "count")
        src = (ROOT / "web/api/routes/admin_ops.py").read_text()
        assert (
            '{"name": r.name, "site": r.site, "day": str(r.day), "count": int(r.count or 0)}' in src
        )


class TestTheClosedList:
    def test_the_list_is_closed_and_never_holds_is_admin(self):
        assert narrow_flags.NARROW_FLAGS == ("ops_reader",)
        assert "is_admin" not in narrow_flags.NARROW_FLAGS

    @pytest.mark.parametrize("flag", ["is_admin", "is_active", "password_hash", "", "OPS_READER"])
    async def test_a_flag_outside_the_list_is_refused_before_any_database_work(self, flag):
        with patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
            side_effect=AssertionError("the database must not be touched"),
        ):
            with pytest.raises(narrow_flags.UnknownFlag):
                await narrow_flags.set_flag("someone", flag, True, CLAIMS.user_id)

    async def test_the_route_refuses_is_admin_with_a_400(self):
        req = admin_ops.SetFlagRequest(username="someone", flag="is_admin", on=True)
        with patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
            side_effect=AssertionError("the database must not be touched"),
        ):
            with pytest.raises(HTTPException) as refused:
                await admin_ops.set_account_flag(req, CLAIMS)
        assert refused.value.status_code == 400
        assert refused.value.detail == admin_ops.UNKNOWN_FLAG_DETAIL


class TestTheControlRoutes:
    async def test_an_unknown_username_changes_nothing_and_says_so(self):
        """A plain answer, not a 404: the app's handler rewrites every 404's words
        to "It may have been moved or deleted", which is untrue for a mistyped name
        (seen in a rendered read before this was changed)."""
        said = {
            "found": False,
            "message": "No account has exactly that username. Nothing was changed.",
        }
        req = admin_ops.SetFlagRequest(username="nobody", flag="ops_reader", on=True)
        with patch.object(narrow_flags, "set_flag", AsyncMock(return_value=None)):
            assert await admin_ops.set_account_flag(req, CLAIMS) == said
        with patch.object(narrow_flags, "read_flags", AsyncMock(return_value=None)):
            assert await admin_ops.read_account_flags("nobody", CLAIMS) == said

    async def test_a_found_account_shows_its_current_flags_and_what_can_be_set(self):
        found = {"username": "web-seed", "flags": {"ops_reader": False}}
        with patch.object(narrow_flags, "read_flags", AsyncMock(return_value=found)):
            out = await admin_ops.read_account_flags("web-seed", CLAIMS)
        assert out == {
            "found": True,
            "username": "web-seed",
            "flags": {"ops_reader": False},
            "settable": ["ops_reader"],
        }

    async def test_a_set_passes_the_acting_admins_id(self):
        saved = {"username": "web-seed", "flags": {"ops_reader": True}, "changed": True}
        setter = AsyncMock(return_value=saved)
        req = admin_ops.SetFlagRequest(username="web-seed", flag="ops_reader", on=True)
        with patch.object(narrow_flags, "set_flag", setter):
            out = await admin_ops.set_account_flag(req, CLAIMS)
        setter.assert_awaited_once_with("web-seed", "ops_reader", True, CLAIMS.user_id)
        assert out["flags"] == {"ops_reader": True} and out["settable"] == ["ops_reader"]


class TestThePage:
    SRC = (ROOT / "templates/settings_account_flags.html").read_text()

    def test_it_says_what_it_does_and_what_it_cannot_do(self):
        assert "Give one account a narrow permission." in self.SRC
        assert "This page cannot make an account an admin." in self.SRC
        assert "Can read the operations counters. Nothing else." in self.SRC

    def test_it_offers_no_admin_control(self):
        script = self.SRC[self.SRC.index("{% block scripts %}") :]
        assert "is_admin" not in script
        # The checkboxes come from the server's closed list, never from the page.
        assert "account.settable.forEach" in script

    def test_it_shows_the_accounts_current_flags_before_saving(self):
        """Arch 11-14: the admin sees what is set before changing anything."""
        script = self.SRC[self.SRC.index("{% block scripts %}") :]
        assert "box.checked = !!account.flags[flag];" in script
        assert script.index("render(account);") < script.index('saveBtn.addEventListener("click"')

    def test_what_the_person_typed_is_shown_as_text(self):
        script = self.SRC[self.SRC.index("{% block scripts %}") :]
        assert "innerHTML" not in script

    def test_the_settings_index_links_it_for_admins_only(self):
        index = (ROOT / "templates/settings-index.html").read_text()
        card = index.index('href="/settings/account-flags"')
        guard = index.rindex("{% if user and user.is_admin %}", 0, card)
        assert "{% endif %}" not in index[guard:card]
