"""#1316 / RECONNECT WS-1 (#1226) — committed real-DB integration test for the
connector-config default-repo store: **configured → repo, unconfigured → None**
(the honest-degrade signal that drives resolve_repo's user-default path, and
UnresolvedRepoError when absent).

The unit test (tests/unit/services/connectors/test_connector_config_repo_1226.py) uses
in-memory SQLite with a single-table create. This closes the #1316 gap: exercise the
SAME behavior against **real Postgres** via the integration_db fixture — real FK
constraints (users), the real JSONB config column, real upsert semantics.

Note on scope: resolve_repo itself opens its own AsyncSessionFactory session, which
can't see the integration fixture's rollback-isolated transaction — so this verifies the
WS-1 STORE round-trip (what #1226 built) that feeds resolution. resolve_repo's full
path is covered by the #1230 per-path proof-tests + manual e2e.
"""

import uuid

import pytest

from services.connectors.config_service import ConnectorConfigService

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_configured_returns_repo_unconfigured_returns_none(integration_db, create_test_user):
    """The core #1226 behavior on real PG: a user with a stored default repo resolves
    it; a user without one gets None (→ honest-degrade / UnresolvedRepoError upstream)."""
    svc = ConnectorConfigService(integration_db)
    configured = str(uuid.uuid4())
    unconfigured = str(uuid.uuid4())
    await create_test_user(configured)
    await create_test_user(unconfigured)

    await svc.set_default_repo(configured, "octo/myrepo")
    await integration_db.flush()

    assert await svc.get_default_repo(configured) == "octo/myrepo"  # configured → repo
    assert await svc.get_default_repo(unconfigured) is None  # unconfigured → honest None


async def test_per_owner_isolation_real_db(integration_db, create_test_user):
    """Two users' default repos don't bleed across owners (real PG per-owner isolation)."""
    svc = ConnectorConfigService(integration_db)
    a, b = str(uuid.uuid4()), str(uuid.uuid4())
    await create_test_user(a)
    await create_test_user(b)

    await svc.set_default_repo(a, "alpha/repo")
    await svc.set_default_repo(b, "beta/repo")
    await integration_db.flush()

    assert await svc.get_default_repo(a) == "alpha/repo"
    assert await svc.get_default_repo(b) == "beta/repo"


async def test_clearing_default_repo_reverts_to_unconfigured(integration_db, create_test_user):
    """Setting then clearing returns to the unconfigured (None) state — real-DB upsert."""
    svc = ConnectorConfigService(integration_db)
    u = str(uuid.uuid4())
    await create_test_user(u)

    await svc.set_default_repo(u, "octo/myrepo")
    await svc.set_default_repo(u, None)
    await integration_db.flush()

    assert await svc.get_default_repo(u) is None
