"""Issue 2390 (ADR-084 D4): the ``ops_reader`` routes are a closed, pinned list, and the
active-keys read returns provider names from a fixed list with counts and nothing else.

LAYER: the live router's declared dependencies; the route function with its database
session replaced at ``AsyncSessionFactory.session_scope``; the gate dependencies run
for real with only their one database read replaced; source reads of web/ and services/.
No database, no server, no model.
DENOMINATOR: every route on ``admin_ops.router``; every Python file under web/ and
services/ for a use of the gate; both routes for 403, 200 and the read line.
NOT COVERED HERE: the SQL against a real database, and the served read by a seat
account (the issue's last two rows).
"""

import inspect
import io
import tokenize
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from services.auth import auth_middleware
from services.auth.auth_middleware import require_admin, require_ops_reader
from services.llm.config import LLMProvider
from web.api.routes import admin_ops

ROOT = Path(__file__).resolve().parents[5]
READER = SimpleNamespace(user_id="22222222-2222-2222-2222-222222222222")
PINNED = ("/api/v1/admin/active-keys", "/api/v1/admin/floored-actions")


def _gated_paths(router):
    return sorted(
        route.path
        for route in router.routes
        if require_ops_reader in {d.call for d in route.dependant.dependencies}
    )


def _session_returning(rows):
    result = MagicMock()
    result.all.return_value = rows
    result.scalars.return_value.all.return_value = []
    session = AsyncMock()
    session.execute = AsyncMock(return_value=result)
    scope = AsyncMock()
    scope.__aenter__ = AsyncMock(return_value=session)
    scope.__aexit__ = AsyncMock(return_value=None)
    return scope, session


class TestTheClosedList:
    def test_the_list_is_exactly_the_pinned_one(self):
        """Adding or removing an entry is a diff HOST reads; this copy makes the test
        fail until it is changed too."""
        assert admin_ops.OPS_READER_ROUTES == PINNED

    def test_every_route_behind_the_gate_is_on_the_list_and_the_reverse(self):
        assert _gated_paths(admin_ops.router) == sorted(admin_ops.OPS_READER_ROUTES)

    def test_no_other_file_can_put_a_route_behind_the_gate(self):
        """The gate's name appears as code only where it is defined and in the one route
        file, so a route in another file, or a router-level dependency, cannot join
        the gate unseen. Code tokens only; a comment that mentions it is not a use."""
        allowed = {"services/auth/auth_middleware.py", "web/api/routes/admin_ops.py"}
        users = set()
        for folder in ("web", "services"):
            for path in (ROOT / folder).rglob("*.py"):
                text = path.read_text(encoding="utf-8")
                if "require_ops_reader" not in text:
                    continue
                for token in tokenize.generate_tokens(io.StringIO(text).readline):
                    if token.type == tokenize.NAME and token.string == "require_ops_reader":
                        users.add(path.relative_to(ROOT).as_posix())
        assert users == allowed

    def test_the_gate_is_declared_per_route_never_on_the_router(self):
        src = (ROOT / "web/api/routes/admin_ops.py").read_text(encoding="utf-8")
        assert src.count("Depends(require_ops_reader)") == len(admin_ops.OPS_READER_ROUTES)
        assert "dependencies=" not in src

    def test_the_seat_reader_may_read_only_listed_routes(self):
        text = (ROOT / "scripts/seat_read.py").read_text(encoding="utf-8")
        for path in admin_ops.OPS_READER_ROUTES:
            assert f'"{path}"' in text
        listed = text[text.index("ALLOWED_PATHS = frozenset(") :].split(")", 1)[0]
        assert listed.count('"/api/') == len(admin_ops.OPS_READER_ROUTES)


class TestTheGate:
    @pytest.mark.parametrize("path", PINNED)
    def test_each_route_uses_the_narrow_gate_and_not_the_admin_one(self, path):
        route = next(r for r in admin_ops.router.routes if r.path == path)
        deps = {d.call for d in route.dependant.dependencies}
        assert require_ops_reader in deps and require_admin not in deps
        assert route.methods == {"GET"}

    async def test_an_account_without_the_flag_gets_403(self):
        with patch.object(auth_middleware, "_user_can_read_ops", AsyncMock(return_value=False)):
            with pytest.raises(HTTPException) as refused:
                await require_ops_reader(READER)
        assert refused.value.status_code == 403

    async def test_a_reader_who_is_not_an_admin_reads_and_is_refused_admin_pages(self):
        """The flag opens the reads and nothing else: the same account passes this gate
        and is refused by ``require_admin`` (which guards every admin page and route)."""
        with patch.object(auth_middleware, "_user_can_read_ops", AsyncMock(return_value=True)):
            assert await require_ops_reader(READER) is READER
        with patch.object(auth_middleware, "_user_is_admin", AsyncMock(return_value=False)):
            with pytest.raises(HTTPException) as refused:
                await require_admin(READER)
        assert refused.value.status_code == 403


class TestActiveKeys:
    def test_the_provider_names_are_the_fixed_list(self):
        assert admin_ops.KEY_PROVIDERS == tuple(sorted(p.value for p in LLMProvider))
        assert admin_ops.OTHER_PROVIDERS not in admin_ops.KEY_PROVIDERS
        assert admin_ops.ACTIVE_KEYS_ROW_KEYS == ("provider", "active_keys")

    def test_it_takes_no_parameter(self):
        """D4 rule 1: nothing a caller sends can select a user, a row or free text."""
        assert list(inspect.signature(admin_ops.active_keys).parameters) == ["reader"]
        route = next(r for r in admin_ops.router.routes if r.path == "/api/v1/admin/active-keys")
        assert route.dependant.query_params == []
        assert route.dependant.path_params == []
        assert route.dependant.body_params == []

    async def test_rows_are_a_listed_name_and_a_count_and_nothing_else(self):
        scope, _ = _session_returning([("anthropic", 3), ("openai", 1)])
        with patch.object(admin_ops.AsyncSessionFactory, "session_scope", return_value=scope):
            with patch.object(admin_ops, "evidence"):
                out = await admin_ops.active_keys(READER)
        assert out == {
            "rows": [
                {"provider": "anthropic", "active_keys": 3},
                {"provider": "gemini", "active_keys": 0},
                {"provider": "openai", "active_keys": 1},
                {"provider": "other", "active_keys": 0},
            ]
        }
        assert set(out) == {"rows"}
        assert all(tuple(row) == admin_ops.ACTIVE_KEYS_ROW_KEYS for row in out["rows"])

    async def test_a_provider_off_the_list_is_counted_as_other_and_never_named(self):
        rows = [("github", 2), ("sk-something-typed-by-mistake", 1), ("anthropic", 1)]
        scope, _ = _session_returning(rows)
        with patch.object(admin_ops.AsyncSessionFactory, "session_scope", return_value=scope):
            with patch.object(admin_ops, "evidence"):
                out = await admin_ops.active_keys(READER)
        by_name = {row["provider"]: row["active_keys"] for row in out["rows"]}
        assert by_name == {"anthropic": 1, "gemini": 0, "openai": 0, "other": 3}
        assert "github" not in str(out) and "sk-something" not in str(out)

    async def test_no_stored_key_says_zero_for_every_listed_provider(self):
        scope, _ = _session_returning([])
        with patch.object(admin_ops.AsyncSessionFactory, "session_scope", return_value=scope):
            with patch.object(admin_ops, "evidence"):
                out = await admin_ops.active_keys(READER)
        assert [row["active_keys"] for row in out["rows"]] == [0, 0, 0, 0]

    async def test_the_query_reads_provider_and_a_count_of_active_rows_only(self):
        scope, session = _session_returning([])
        with patch.object(admin_ops.AsyncSessionFactory, "session_scope", return_value=scope):
            with patch.object(admin_ops, "evidence"):
                await admin_ops.active_keys(READER)
        sql = str(session.execute.await_args.args[0]).lower()
        selected = sql[: sql.index("from")]
        assert "user_api_keys.provider" in selected and "count(" in selected
        for column in ("user_id", "key_reference", "encrypted_secret", "created_at", ".id"):
            assert column not in selected
        assert "is_active is true" in sql and "group by user_api_keys.provider" in sql


class TestEachReadIsNoted:
    async def test_active_keys_writes_the_route_and_the_reader_and_no_body(self):
        scope, _ = _session_returning([("anthropic", 7)])
        with patch.object(admin_ops.AsyncSessionFactory, "session_scope", return_value=scope):
            with patch.object(admin_ops, "evidence") as noted:
                await admin_ops.active_keys(READER)
        noted.assert_called_once_with(
            "ops_read", route="/api/v1/admin/active-keys", reader=READER.user_id
        )

    async def test_floored_actions_writes_the_route_and_the_reader_and_no_body(self):
        scope, _ = _session_returning([])
        with patch.object(admin_ops.AsyncSessionFactory, "session_scope", return_value=scope):
            with patch.object(admin_ops, "evidence") as noted:
                await admin_ops.floored_actions(30, READER)
        noted.assert_called_once_with(
            "ops_read", route="/api/v1/admin/floored-actions", reader=READER.user_id
        )

    def test_every_listed_route_notes_its_read_under_its_own_path(self):
        src = (ROOT / "web/api/routes/admin_ops.py").read_text(encoding="utf-8")
        for path in admin_ops.OPS_READER_ROUTES:
            assert f'_note_read("{path}", reader)' in src
        assert src.count("_note_read(") == len(admin_ops.OPS_READER_ROUTES) + 1  # and its def
