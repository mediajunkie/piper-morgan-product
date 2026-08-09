"""#1547 (audit F5 + lying-source retirement): the four real plugins stop
publishing constant-false configuration status.

- F5: each plugin's ``GET /api/v1/integrations/{name}/status`` sub-route emitted
  ``configured: false`` forever, for everyone (plugin ``is_configured()`` is
  hardcoded False, #784). The #1499 audit found no template consumer; the routes
  are deleted. The truthful equivalents are ``/api/v1/integrations/health`` and
  the per-integration oauth/settings status routes.
- get_status(): ``configured`` is now ``None`` (unknowable at plugin level —
  integration truth is user-scoped) plus a note pointing at the canonical
  IntegrationStatusService. A None reads falsy for any legacy `.get("configured",
  False)` consumer — no surface gets MORE credulous.
"""

import pytest

from services.integrations.calendar.calendar_plugin import CalendarPlugin
from services.integrations.github.github_plugin import GitHubPlugin
from services.integrations.notion.notion_plugin import NotionPlugin
from services.integrations.slack.slack_plugin import SlackPlugin

REAL_PLUGINS = [GitHubPlugin, SlackPlugin, CalendarPlugin, NotionPlugin]


@pytest.mark.parametrize("plugin_cls", REAL_PLUGINS)
def test_no_constant_false_status_subroute(plugin_cls):
    """F5: the lying /status sub-route is gone (router itself may remain)."""
    router = plugin_cls().get_router()
    if router is None:
        return  # no router at all — trivially no lying route
    paths = [getattr(r, "path", "") for r in router.routes]
    assert not any(p.endswith("/status") for p in paths), (
        f"{plugin_cls.__name__} still serves a /status sub-route — that endpoint "
        "reported configured:false forever for everyone (#784/#1547)."
    )


@pytest.mark.parametrize("plugin_cls", REAL_PLUGINS)
def test_get_status_no_longer_claims_unconfigured(plugin_cls):
    """The registry status dict stops asserting a false negative: configured is
    None (unknowable without a user), with a note naming the canonical source."""
    status = plugin_cls().get_status()
    assert status["configured"] is None, (
        f"{plugin_cls.__name__}.get_status()['configured'] must be None — a "
        "plugin has no user context, so a boolean here is a fabrication (#784)."
    )
    assert "configured_note" in status
    assert "IntegrationStatusService" in status["configured_note"]


def test_demo_plugin_untouched():
    """Demo's env-fed status is real at plugin level (DEMO_ENABLED) — it keeps
    its boolean; exclusion from user-facing surfaces is structural (the
    canonical service's known set), not a demo-side change."""
    from services.integrations.demo.demo_plugin import DemoPlugin

    assert isinstance(DemoPlugin().get_status().get("configured"), bool)
