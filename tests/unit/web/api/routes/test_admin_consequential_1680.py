"""#1680 Dashboard Criterion E (landing B): ``GET /api/v1/admin/consequential-actions``.

The admin read of the consequential-action census and counts, behind ``require_admin``
(#2096's pattern). DENOMINATOR: refusal for a non-admin; the response shape with the
live headline; the ``days`` bounds; the mount in the real app; and the counts against
three rows (one per status) really written to the scratch database by the helper.
"""

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import text

from services.auth.auth_middleware import get_current_user, require_admin
from services.security import audit_logger as al
from services.security.consequential_sites import CONSEQUENTIAL_SITES, coverage_headline
from web.api.routes import admin_consequential as api

USER = SimpleNamespace(
    user_id="11111111-1111-1111-1111-111111111111", sub="11111111-1111-1111-1111-111111111111"
)
PATH = "/api/v1/admin/consequential-actions"


def _client(admin=True):
    app = FastAPI()
    app.include_router(api.router)
    app.dependency_overrides[get_current_user] = lambda: USER
    if admin:
        app.dependency_overrides[require_admin] = lambda: USER
    return TestClient(app, raise_server_exceptions=False)


_ZERO_COUNTS = {
    "window_days": 7,
    "since": "2026-10-26T00:00:00+00:00",
    "total": 0,
    "by_status": {"success": 0, "failed": 0, "unconfirmed": 0},
    "by_flag": {"proactive": 0, "credits_spent": 0, "external_message": 0, "hard_to_reverse": 0},
    "by_site": {},
}


class TestAccess:
    def test_non_admin_is_refused(self, monkeypatch):
        import services.auth.auth_middleware as am

        async def _not_admin(_uid):
            return False

        monkeypatch.setattr(am, "_user_is_admin", _not_admin, raising=False)
        counts = AsyncMock(return_value=_ZERO_COUNTS)
        monkeypatch.setattr(api, "_action_counts", counts)
        r = _client(admin=False).get(PATH)
        assert r.status_code == 403
        counts.assert_not_awaited()  # nothing was read for a non-admin

    def test_mounted_in_the_real_app(self):
        from web.app import app

        assert PATH in {getattr(r, "path", None) for r in app.routes}


class TestShape:
    def test_admin_gets_headline_sites_actions_and_failed_write_window(self, monkeypatch):
        counts = AsyncMock(return_value=_ZERO_COUNTS)
        monkeypatch.setattr(api, "_action_counts", counts)
        r = _client().get(PATH)
        assert r.status_code == 200
        body = r.json()
        assert set(body) == {"headline", "sites", "actions", "failed_writes"}
        assert body["headline"] == coverage_headline() == "16 of 16 sites instrumented"
        sites = body["sites"]
        assert sites["instrumented"] == sites["censused"] == len(CONSEQUENTIAL_SITES) == 16
        assert sites["complete"] is True
        assert [e["key"] for e in sites["entries"]] == list(CONSEQUENTIAL_SITES)
        assert set(sites["entries"][0]) == {
            "key",
            "family",
            "module",
            "function",
            "instrumented",
            "proactive",
            "external_message",
            "hard_to_reverse",
        }
        assert body["actions"] == _ZERO_COUNTS
        assert counts.await_args.args == (7,)
        assert body["failed_writes"] == al.consequential_write_failures_window()
        assert set(body["failed_writes"]) == {"count", "since"}

    @pytest.mark.parametrize("days,code", [(0, 422), (91, 422), (1, 200), (90, 200)])
    def test_days_bounds(self, monkeypatch, days, code):
        monkeypatch.setattr(api, "_action_counts", AsyncMock(return_value=_ZERO_COUNTS))
        assert _client().get(PATH, params={"days": days}).status_code == code


async def _db_ready():
    from services.database.session_factory import AsyncSessionFactory

    try:
        async with AsyncSessionFactory.session_scope_fresh() as s:
            has = (
                await s.execute(
                    text(
                        "SELECT count(*) FROM information_schema.columns "
                        "WHERE table_name = 'audit_logs' AND column_name = 'hard_to_reverse'"
                    )
                )
            ).scalar()
    except Exception as e:  # silent-ok: infra absence is a skip, not a verdict
        pytest.skip(f"Postgres not reachable: {e}")
    if not has:
        pytest.skip("audit_logs lacks the #1680 columns; run alembic upgrade head (t1680flags)")


@pytest.mark.consequential_audit_db
class TestCountsFromTheDatabase:
    async def test_three_rows_one_per_status_are_counted(self):
        from services.database.session_factory import AsyncSessionFactory

        await _db_ready()
        before = _client().get(PATH).json()["actions"]
        written = []
        tag = uuid.uuid4().hex[:8]
        for site, status, credits in (
            ("github.chat.comment_issue", "success", True),
            ("slack.standup.post", "failed", False),
            ("github.chat.close_issue", "unconfirmed", False),
        ):
            log = await al.audit_logger.log_consequential_action(
                site=site,
                status=status,
                user_id=None,
                message=f"#1680 admin read count {tag}",
                credits_spent=credits,
            )
            assert log is not None
            written.append(log.id)
        try:
            after = _client().get(PATH).json()["actions"]
            assert after["total"] - before["total"] == 3
            for status in ("success", "failed", "unconfirmed"):
                assert after["by_status"][status] - before["by_status"][status] == 1
            delta = {k: after["by_flag"][k] - before["by_flag"][k] for k in after["by_flag"]}
            # comment: credits; standup post: proactive; close: reversible; all external
            assert delta == {
                "proactive": 1,
                "credits_spent": 1,
                "external_message": 3,
                "hard_to_reverse": 2,
            }
            for site in (
                "github.chat.comment_issue",
                "slack.standup.post",
                "github.chat.close_issue",
            ):
                assert after["by_site"][site] - before["by_site"].get(site, 0) == 1
            assert after["window_days"] == 7 and after["since"]
        finally:
            async with AsyncSessionFactory.session_scope_fresh() as s:
                await s.execute(
                    text("DELETE FROM audit_logs WHERE id = ANY(:ids)"), {"ids": written}
                )
                await s.commit()
