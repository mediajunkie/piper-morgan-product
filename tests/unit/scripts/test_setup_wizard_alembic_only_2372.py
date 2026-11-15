"""#2372: the setup wizard builds the schema with alembic only, and stops on failure.

Arch's ruling (2026-11-14). The wizard used to run ``Base.metadata.create_all`` on an
empty database and then ``alembic upgrade head``; a failed migration was printed as a
warning and setup continued, leaving a database with no ``alembic_version`` stamp.
Now it takes the one path the self-host guide and CI use, and a migration failure
stops setup with the error.

Also pinned here, from the same ruling: no NEW migration may carry a skip-if-exists
guard. ``v2327floored``'s guard was accepted as a one-off; once the fresh-database
test stopped writing tables into shared databases, a guard is never needed.

LAYER: the wizard's database step with the migration run replaced at its one seam;
source pins on the wizard and on ``alembic/versions``. The real run from an empty
database is quoted on the issue (a scratch database, not a unit test).
DENOMINATOR: success, a failed migration, a timeout, a missing interpreter module;
every file in alembic/versions for the guard pin.
"""

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from scripts import setup_wizard  # noqa: E402


def _done(returncode=0, stdout="", stderr=""):
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


async def _run(result=None, raises=None):
    printed = []
    target = "scripts.setup_wizard._run_migrations"
    kwargs = {"side_effect": raises} if raises else {"return_value": result}
    with (
        patch(target, **kwargs),
        patch("builtins.print", lambda *a, **k: printed.append(" ".join(map(str, a)))),
    ):
        ok = await setup_wizard._wizard_database_setup()
    return ok, "\n".join(printed)


class TestTheDatabaseStep:
    async def test_a_clean_migration_run_continues_setup(self):
        ok, said = await _run(_done(0))
        assert ok is True
        assert "Database schema up to date" in said

    async def test_a_failed_migration_stops_setup_and_shows_the_error(self):
        ok, said = await _run(_done(1, stderr="DuplicateTable: relation already exists"))
        assert ok is False
        assert "Setup has stopped." in said
        assert "DuplicateTable: relation already exists" in said
        assert "Continuing setup" not in said

    async def test_a_timeout_stops_setup(self):
        ok, said = await _run(raises=subprocess.TimeoutExpired(cmd="alembic", timeout=600))
        assert ok is False and "Setup has stopped." in said

    async def test_any_other_failure_to_run_stops_setup(self):
        ok, said = await _run(raises=FileNotFoundError("no interpreter"))
        assert ok is False and "Setup has stopped." in said

    def test_it_runs_alembic_with_this_interpreter(self):
        with patch("scripts.setup_wizard.subprocess.run", return_value=_done(0)) as run:
            setup_wizard._run_migrations("/somewhere")
        command = run.call_args.args[0]
        assert command == [sys.executable, "-m", "alembic", "upgrade", "head"]
        assert run.call_args.kwargs["cwd"] == "/somewhere"

    def test_the_wizard_never_builds_tables_outside_alembic(self):
        """No call to ``create_tables`` or ``create_all`` anywhere in the wizard.
        Code tokens only, so the docstring that explains the history doesn't count."""
        import io
        import tokenize

        text = (ROOT / "scripts/setup_wizard.py").read_text(encoding="utf-8")
        names = {
            token.string
            for token in tokenize.generate_tokens(io.StringIO(text).readline)
            if token.type == tokenize.NAME
        }
        assert not names & {"create_tables", "create_all"}
        assert "Continuing setup" not in text


class TestNoNewGuardedMigration:
    # The migrations that inspect the database for an existing table or column.
    # Frozen 2026-11-14: three older ones and v2327floored (Arch's accepted one-off).
    # A new file here means a new guard, which the ruling forbids.
    GUARDED = {
        "a1267projintegrations_create_project_integrations_table.py",
        "a1273coretables_create_intent_workflow_task_stakeholder.py",
        "a358encsecret_add_encrypted_secret_to_user_api_keys.py",
        "v2327floored_floored_action_counts.py",
    }
    INSPECTORS = (
        "has_table(",
        "get_table_names(",
        "get_columns(",
        "has_column",
        "has_index(",
        "get_indexes(",
    )

    def test_only_the_frozen_set_inspects_for_existing_objects(self):
        versions = ROOT / "alembic/versions"
        files = sorted(versions.glob("*.py"))
        assert len(files) > 50, "the versions folder moved or the glob is wrong"
        found = {
            path.name
            for path in files
            if any(word in path.read_text(encoding="utf-8") for word in self.INSPECTORS)
        }
        new = found - self.GUARDED
        assert not new, (
            f"new skip-if-exists guard in {sorted(new)}. A migration creates its objects "
            "plainly (#2372, Arch 2026-11-14): the guard hides model-vs-migration drift. If "
            "a database already has the table, find what created it outside alembic."
        )
        assert (
            found == self.GUARDED
        ), f"a guarded migration was removed: {sorted(self.GUARDED - found)}"
