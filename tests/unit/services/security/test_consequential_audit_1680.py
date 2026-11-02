"""#1680 Dashboard Criterion E (landing A): the consequential-site registry and the
``AuditLogger.log_consequential_action`` helper.

Registry integrity runs anywhere. The helper's write tests use the real Postgres the
run points at (``consequential_audit_db`` turns off the conftest stub) and read the row
back through a separate fresh session, so a pass shows the helper committed in its own
session. They skip only when Postgres is unreachable or not migrated to t1680flags.
"""

import ast
import os
import uuid
from pathlib import Path

import pytest
from sqlalchemy import text

from services.security import audit_logger as al
from services.security.consequential_sites import (
    CONSEQUENTIAL_SITES,
    GITHUB,
    SLACK,
    TRANSPORT_MODULES,
    coverage,
    coverage_headline,
)

REPO = Path(__file__).resolve().parents[4]


def _functions_in(path: Path) -> set:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = set()

    def walk(node, stack):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not isinstance(ch, ast.ClassDef):
                    names.add(".".join(stack + [ch.name]))
                walk(ch, stack + [ch.name])
            else:
                walk(ch, stack)

    walk(tree, [])
    return names


class TestRegistryIntegrity:
    def test_sixteen_sites_with_unique_keys(self):
        assert len(CONSEQUENTIAL_SITES) == 16
        assert all(k == s.key for k, s in CONSEQUENTIAL_SITES.items())

    def test_every_module_and_function_exists_on_disk(self):
        for site in CONSEQUENTIAL_SITES.values():
            path = REPO / site.module
            assert path.is_file(), f"{site.key}: {site.module} is missing"
            assert site.function in _functions_in(
                path
            ), f"{site.key}: {site.function} not found in {site.module}"

    def test_transport_modules_exist_and_hold_no_site(self):
        site_modules = {s.module for s in CONSEQUENTIAL_SITES.values()}
        for mod in TRANSPORT_MODULES:
            assert (REPO / mod).is_file(), f"transport module {mod} is missing"
            assert mod not in site_modules

    def test_families_and_flag_table(self):
        sites = CONSEQUENTIAL_SITES
        assert {s.family for s in sites.values()} == {SLACK, GITHUB}
        assert sum(s.family == SLACK for s in sites.values()) == 7
        assert sum(s.family == GITHUB for s in sites.values()) == 9
        assert all(s.external_message for s in sites.values())
        reversible = {k for k, s in sites.items() if not s.hard_to_reverse}
        assert reversible == {"github.chat.close_issue", "github.chat.reopen_issue"}
        proactive = {k for k, s in sites.items() if s.proactive}
        assert proactive == {
            "slack.standup.post",
            "github.standup.create_issue",
            "slack.socket.placeholder",
        }
        assert all(s.credits_note for s in sites.values())

    def test_coverage_headline(self):
        assert coverage() == (7, 16)
        assert coverage_headline() == "7 of 16 sites instrumented"


class TestHelperContract:
    @pytest.mark.consequential_audit_db
    async def test_unknown_site_raises(self):
        with pytest.raises(ValueError, match="unknown consequential site"):
            await al.audit_logger.log_consequential_action(
                site="github.chat.creat_issue",
                status="success",
                user_id=None,
                message="typo",
                credits_spent=False,
            )

    @pytest.mark.consequential_audit_db
    async def test_unknown_status_raises(self):
        with pytest.raises(ValueError, match="status must be one of"):
            await al.audit_logger.log_consequential_action(
                site="github.chat.create_issue",
                status="ok",
                user_id=None,
                message="bad status",
                credits_spent=False,
            )

    @pytest.mark.consequential_audit_db
    async def test_failed_write_is_counted_and_returns_none(self, monkeypatch):
        from services.database.session_factory import AsyncSessionFactory

        def _boom():
            raise ConnectionError("db down")

        monkeypatch.setattr(AsyncSessionFactory, "session_scope_fresh", staticmethod(_boom))
        before = al.consequential_write_failures()
        result = await al.audit_logger.log_consequential_action(
            site="github.chat.close_issue",
            status="success",
            user_id=None,
            message="write fails",
            credits_spent=False,
        )
        assert result is None
        assert al.consequential_write_failures() == before + 1

    def test_principal_coercion(self):
        u = uuid.uuid4()
        assert al._coerce_principal(u) == (u, None)
        assert al._coerce_principal(str(u)) == (u, None)
        assert al._coerce_principal("U123") == (None, "U123")
        assert al._coerce_principal(None) == (None, None)


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
        pytest.skip(
            f"audit_logs lacks the #1680 columns in {os.getenv('POSTGRES_DB', 'piper_morgan')}; "
            "run alembic upgrade head (t1680flags)"
        )


async def _read_row(row_id: str):
    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope_fresh() as s:
        return (
            (
                await s.execute(
                    text(
                        "SELECT event_type, action, status, severity, user_id, resource_type, "
                        "resource_id, details, proactive, credits_spent, external_message, "
                        "hard_to_reverse FROM audit_logs WHERE id = :id"
                    ),
                    {"id": row_id},
                )
            )
            .mappings()
            .first()
        )


async def _delete_row(row_id: str):
    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope_fresh() as s:
        await s.execute(text("DELETE FROM audit_logs WHERE id = :id"), {"id": row_id})
        await s.commit()


@pytest.mark.consequential_audit_db
class TestHelperWritesItsOwnRow:
    async def test_row_committed_with_registry_flags_and_status(self):
        await _db_ready()
        log = await al.audit_logger.log_consequential_action(
            site="github.chat.comment_issue",
            status="failed",
            user_id=None,
            resource_type="github_issue",
            resource_id=42,
            message="Comment on issue #42",
            credits_spent=True,
            details={"error_type": "GitHubWriteRefused"},
        )
        assert log is not None
        try:
            row = await _read_row(log.id)  # a different session: the helper committed
            assert row is not None
            assert row["event_type"] == "consequential"
            assert row["action"] == "github.chat.comment_issue"
            assert row["status"] == "failed"
            assert row["severity"] == "info"
            assert row["resource_type"] == "github_issue"
            assert row["resource_id"] == "42"
            assert row["details"] == {"error_type": "GitHubWriteRefused"}
            # flags from the registry entry; credits_spent from the caller
            assert row["proactive"] is False
            assert row["external_message"] is True
            assert row["hard_to_reverse"] is True
            assert row["credits_spent"] is True
        finally:
            await _delete_row(log.id)

    async def test_registry_flags_for_a_reversible_site(self):
        await _db_ready()
        log = await al.audit_logger.log_consequential_action(
            site="github.chat.close_issue",
            status="unconfirmed",
            user_id=None,
            message="Close issue #7",
            credits_spent=False,
            details={"write_unconfirmed": "empty_result"},
        )
        assert log is not None
        try:
            row = await _read_row(log.id)
            assert row["status"] == "unconfirmed"
            assert row["hard_to_reverse"] is False
            assert row["credits_spent"] is False
        finally:
            await _delete_row(log.id)

    async def test_slack_principal_goes_in_details_not_user_id(self):
        await _db_ready()
        log = await al.audit_logger.log_consequential_action(
            site="slack.response.individual",
            status="success",
            user_id="U123",
            resource_type="slack_channel",
            resource_id="C1",
            message="Slack reply",
            credits_spent=False,
        )
        assert log is not None
        try:
            row = await _read_row(log.id)
            assert row["user_id"] is None
            assert row["details"] == {"principal": "U123"}
        finally:
            await _delete_row(log.id)
