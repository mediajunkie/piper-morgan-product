"""#1690 — demo template plugin must NOT mount live routes by default.

The 2026-08 architectural review (Leg B live-state census) found that with
config/PIPER.user.md absent (it is gitignored, so absent in every deployment),
the plugin registry's "no config -> enable everything" default enabled the demo
template plugin too, mounting live example routes at /api/v1/integrations/demo
in every default deployment. PM ruled 2026-08-29: fix it.

The fix: the demo plugin is excluded from the default-enabled set unless the
operator opts in explicitly — PIPER_DEMO_PLUGIN=1 (dev/demo walkthroughs) or an
explicit plugins.enabled listing in config/PIPER.user.md.

Two layers pinned here (m-43 — name the layer):
1. Policy layer: get_enabled_plugins() default branch excludes/includes demo.
2. Route-table layer: the REAL mounting phase (web.startup
   PluginInitializationPhase.startup) run against a real FastAPI app — demo
   routes absent from app.routes by default, present + serving when opted in.
   Asserted via the app's actual route table and a real request, not config.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.plugins import get_plugin_registry, reset_plugin_registry
from services.plugins.plugin_registry import (
    DEMO_PLUGIN_ENV,
    PluginRegistry,
    demo_plugin_opted_in,
)
from web.startup import PluginInitializationPhase

DEMO_PREFIX = "/api/v1/integrations/demo"


@pytest.fixture(autouse=True)
def _fresh_registry():
    """Isolate the singleton registry per test (and clean up after)."""
    reset_plugin_registry()
    yield
    reset_plugin_registry()


@pytest.fixture()
def _no_user_config(monkeypatch):
    """Pin the deploy condition: no PIPER.user.md plugin config.

    The file is gitignored and absent in every deployment; patching keeps the
    test correct even on a dev machine that has a local overlay.
    """
    monkeypatch.setattr(PluginRegistry, "_read_plugin_config", lambda self: {})


# --- opt-in switch semantics ---


def test_opt_in_env_parsing(monkeypatch):
    for value, expected in [
        ("1", True),
        ("true", True),
        ("YES", True),
        ("0", False),
        ("", False),
        ("no", False),
    ]:
        monkeypatch.setenv(DEMO_PLUGIN_ENV, value)
        assert demo_plugin_opted_in() is expected, value
    monkeypatch.delenv(DEMO_PLUGIN_ENV)
    assert demo_plugin_opted_in() is False


# --- policy layer: the default-enabled set ---


def test_demo_excluded_from_default_enabled(monkeypatch, _no_user_config):
    monkeypatch.delenv(DEMO_PLUGIN_ENV, raising=False)
    enabled = get_plugin_registry().get_enabled_plugins()
    assert "demo" not in enabled
    # The gate is demo-specific: real integrations stay default-enabled.
    assert "slack" in enabled
    assert "github" in enabled


def test_demo_included_when_env_opted_in(monkeypatch, _no_user_config):
    monkeypatch.setenv(DEMO_PLUGIN_ENV, "1")
    enabled = get_plugin_registry().get_enabled_plugins()
    assert "demo" in enabled


def test_explicit_config_listing_still_honored(monkeypatch):
    """An explicit plugins.enabled listing is an operator choice — honored."""
    monkeypatch.delenv(DEMO_PLUGIN_ENV, raising=False)
    monkeypatch.setattr(
        PluginRegistry,
        "_read_plugin_config",
        lambda self: {"plugins": {"enabled": ["demo"]}},
    )
    assert get_plugin_registry().get_enabled_plugins() == ["demo"]


# --- route-table layer: the real mounting phase against a real app ---
#
# Discovery is narrowed to the demo plugin so these tests don't import and
# initialize the real integrations (network-facing); everything downstream —
# the default-branch enablement decision, load_enabled_plugins, router
# mounting via app.include_router — is the real code path, and the assertion
# is on the app's actual route table / a real request.


@pytest.fixture()
def _demo_only_discovery(monkeypatch):
    monkeypatch.setattr(
        PluginRegistry,
        "discover_plugins",
        lambda self: {"demo": "services.integrations.demo.demo_plugin"},
    )


async def test_demo_routes_absent_from_route_table_by_default(
    monkeypatch, _no_user_config, _demo_only_discovery
):
    monkeypatch.delenv(DEMO_PLUGIN_ENV, raising=False)
    app = FastAPI()
    await PluginInitializationPhase.startup(app)

    # Guard against a false clear (m-44): the phase swallows exceptions and
    # "continues without plugin system" — prove it actually completed.
    assert app.state.plugin_registry is not None

    demo_paths = [r.path for r in app.routes if r.path.startswith(DEMO_PREFIX)]
    assert demo_paths == []

    # And the behavioral check the issue asked for: health 404s by default.
    client = TestClient(app, raise_server_exceptions=False)
    assert client.get(f"{DEMO_PREFIX}/health").status_code == 404


async def test_demo_routes_mounted_and_serving_when_opted_in(
    monkeypatch, _no_user_config, _demo_only_discovery
):
    monkeypatch.setenv(DEMO_PLUGIN_ENV, "1")
    app = FastAPI()
    await PluginInitializationPhase.startup(app)

    assert app.state.plugin_registry is not None

    paths = {r.path for r in app.routes}
    assert f"{DEMO_PREFIX}/health" in paths
    assert f"{DEMO_PREFIX}/echo" in paths
    assert f"{DEMO_PREFIX}/status" in paths

    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get(f"{DEMO_PREFIX}/health")
    assert resp.status_code == 200
    assert resp.json()["service"] == "demo"
