"""#2238 (xian 2026-11-03): staging test accounts are provisioned directly in the staging
database by ``scripts/create_test_alpha_user.py --staging``. The guard decides where the
script may run from the environment alone: local by default, staging only inside the
staging app, alpha never. The old guard read ``POSTGRES_HOST`` alone, which a Fly
container never sets, so it would have run against any hosted database."""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "create_test_alpha_user.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("create_test_alpha_user_2238", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "env, staging, target",
    [
        ({}, False, "local"),
        ({"POSTGRES_HOST": "127.0.0.1"}, False, "local"),
        ({"POSTGRES_HOST": "db.internal"}, False, None),
        ({"DATABASE_URL": "postgresql://x"}, False, None),
        ({"FLY_APP_NAME": "piper-morgan-staging"}, False, None),
        (
            {"FLY_APP_NAME": "piper-morgan-staging", "DATABASE_URL": "postgresql://x"},
            True,
            "staging",
        ),
        ({"FLY_APP_NAME": "piper-morgan"}, True, None),
        ({"FLY_APP_NAME": "piper-morgan"}, False, None),
        ({}, True, None),
        ({"DATABASE_URL": "postgresql://x"}, True, None),
    ],
)
def test_where_the_script_may_run(mod, env, staging, target):
    got, reason = mod.target_for(env, staging)
    assert got == target, reason
    assert reason


def test_the_staging_app_name_is_the_one_the_status_service_uses(mod):
    from services.integrations.integration_status_service import STAGING_APP_NAME

    assert mod.STAGING_APP_NAME == STAGING_APP_NAME


def test_the_script_names_its_concept_doc(mod):
    assert "Concept: docs/internal/operations/staging-fly-setup-2026-09-22.md" in (
        mod.__doc__ or ""
    )
