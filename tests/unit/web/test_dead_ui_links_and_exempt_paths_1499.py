"""#1499 Class 3 — dead UI links and stale auth-exempt entries.

Two small families the 2026-08-07 route audit found, grouped because both are the same
shape: a reference that survived the thing it referenced.

**Dead UI links.** Two shipped pages link to paths no router serves:
  - `templates/learning-dashboard.html` → `/api/v1/learning/health`. The audit recorded
    this as "route commented out at learning.py:530"; as of 2026-09-23 there is no
    `health` token anywhere in `web/api/routes/learning.py` at all — not even commented —
    so there was nothing left to re-enable. The link is removed.
  - `templates/privacy-settings.html` → `/privacy-policy`. No route, and no
    `privacy-policy.html` template exists. The markup shipped with its own placeholder
    text, "(if exists, or link to external)". Authoring a privacy policy is a product/
    legal decision, not a route fix, so the link is removed rather than stubbed.

**Stale auth-exempt entries.** `EXEMPT_OAUTH_CALLBACK_PATHS` listed two paths no mounted
router serves: `/slack/oauth/callback` (defined only on the unmounted `SlackWebhookRouter`
— #1496) and `/github/oauth/callback` (defined nowhere at all). The exempt list is a
security boundary (#1308): once the perimeter gate is gone it IS the attack surface, and
a dead entry is a hole pre-drilled for whatever route later claims that path. Same
reasoning, same treatment as the `/api/v1/auth/register` entry the #1504 audit pruned.

LAYER (m-43): template `render()` for the UI half (never a grep of the raw file — these
pages extend `layouts/app_shell.html` and the shell could reintroduce a link); direct
inspection of the assembled exempt list plus a live `AuthMiddleware` path decision for
the auth half.
DENOMINATOR: the 2 dead UI links and the 2 stale exempt entries named by the #1499 audit.
The general "no exempt path lacks a mounted route" guard is NOT implemented here — see
`TestGeneralExemptGuardIsAFollowUp` below for why, honestly stated rather than implied.
"""

from jinja2 import Environment, FileSystemLoader

from services.auth.auth_middleware import (
    DEFAULT_EXCLUDE_PATHS,
    EXEMPT_OAUTH_CALLBACK_PATHS,
)


def _render(template_name: str) -> str:
    env = Environment(loader=FileSystemLoader("templates"))
    return env.get_template(template_name).render(request=None, user={"username": "t"})


class TestLearningDashboardHasNoDeadHealthLink:
    def test_no_link_to_the_nonexistent_learning_health_route(self):
        assert "/api/v1/learning/health" not in _render("learning-dashboard.html")

    def test_the_route_really_does_not_exist(self):
        """Pin the premise: if someone adds /health to the learning router, this test
        fails and the link can be restored deliberately rather than by accident."""
        import web.api.routes.learning as learning

        paths = {r.path for r in learning.router.routes}
        assert "/api/v1/learning/health" not in paths

    def test_the_surviving_footer_links_still_point_somewhere_real(self):
        """Removal must not leave an empty footer — /docs is a real exempt surface."""
        html = _render("learning-dashboard.html")
        assert 'href="/docs"' in html


class TestPrivacySettingsHasNoDeadPolicyLink:
    def test_no_link_to_the_nonexistent_privacy_policy_route(self):
        assert 'href="/privacy-policy"' not in _render("privacy-settings.html")

    def test_no_shipped_placeholder_text(self):
        """The page literally rendered '(if exists, or link to external)' to users."""
        assert "if exists, or link to external" not in _render("privacy-settings.html")

    def test_back_to_settings_link_survives(self):
        assert 'href="/settings"' in _render("privacy-settings.html")


class TestStaleOAuthCallbackExemptionsAreGone:
    def test_slack_oauth_callback_is_not_exempt(self):
        """Only on the unmounted #1496 router — exempting it pre-authorizes a path
        that does not exist yet."""
        assert "/slack/oauth/callback" not in EXEMPT_OAUTH_CALLBACK_PATHS
        assert "/slack/oauth/callback" not in DEFAULT_EXCLUDE_PATHS

    def test_github_oauth_callback_is_not_exempt(self):
        """Defined by no router anywhere, mounted or not."""
        assert "/github/oauth/callback" not in EXEMPT_OAUTH_CALLBACK_PATHS
        assert "/github/oauth/callback" not in DEFAULT_EXCLUDE_PATHS

    def test_the_live_settings_callbacks_are_still_exempt(self):
        """The denominator matters: this prunes TWO entries, not the category.
        The real, mounted OAuth callbacks must keep working."""
        for path in (
            "/api/v1/settings/integrations/slack/connect",
            "/api/v1/settings/integrations/slack/callback",
            "/api/v1/settings/integrations/calendar/connect",
            "/api/v1/settings/integrations/calendar/callback",
        ):
            assert path in EXEMPT_OAUTH_CALLBACK_PATHS

    def test_the_setup_wizards_real_slack_callback_is_still_exempt(self):
        """The near-miss this prune had to clear, pinned so it can't be re-broken.

        `web/api/routes/setup.py:1361` DOES define a Slack OAuth callback — at
        `/api/v1/setup/slack/oauth/callback`, because its router carries the
        `/api/v1/setup` prefix. It is a real, mounted, pre-login route that must stay
        auth-free or the wizard cannot complete. It is exempt via the `/api/v1/setup`
        entry's prefix match, NOT via the bare `/slack/oauth/callback` entry removed
        here — which only ever matched the unmounted #1496 router's path. Verified by
        enumerating `setup.router.routes` before pruning, not inferred from the name.
        """
        from unittest.mock import MagicMock

        import web.api.routes.setup as setup
        from services.auth.auth_middleware import AuthMiddleware

        assert "/api/v1/setup/slack/oauth/callback" in {r.path for r in setup.router.routes}
        mw = AuthMiddleware(app=None, jwt_service=MagicMock())
        assert mw._should_exclude_path("/api/v1/setup/slack/oauth/callback") is True

    def test_middleware_now_requires_auth_on_the_pruned_paths(self):
        """Behavior, not just list membership — the middleware's own decision."""
        from unittest.mock import MagicMock

        from services.auth.auth_middleware import AuthMiddleware

        mw = AuthMiddleware(app=None, jwt_service=MagicMock())
        assert mw._should_exclude_path("/slack/oauth/callback") is False
        assert mw._should_exclude_path("/github/oauth/callback") is False
        assert mw._should_exclude_path("/health") is True


class TestGeneralExemptGuardIsAFollowUp:
    """#1499 asked whether to pin the GENERAL rule — 'no exempt path is served by no
    mounted router'. It is NOT pinned here, on purpose, and this states so rather than
    letting the absence read as coverage (m-44).

    Deriving the mounted set requires importing every module named in `web/app.py`'s
    mount calls plus `web/startup.py` plus the runtime plugin registry — the plugin half
    only resolves at app startup, so a static version of the check would produce false
    positives on exactly the paths that matter. The two specific stale entries are pinned
    above; the general guard wants the router-inventory work that #1499 Class 2's
    disposal ruling will produce anyway.
    """

    def test_exempt_categories_are_still_assembled_into_the_flat_list(self):
        """The one structural thing worth holding meanwhile: no category silently
        stops contributing to `DEFAULT_EXCLUDE_PATHS`."""
        for path in EXEMPT_OAUTH_CALLBACK_PATHS:
            assert path in DEFAULT_EXCLUDE_PATHS
