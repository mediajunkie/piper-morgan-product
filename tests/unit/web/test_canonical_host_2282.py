"""#2282 (xian 2026-11-05 10:47, Arch's shape 10:52): beta.pipermorgan.ai is the one public
host; alpha.pipermorgan.ai redirects to it, keeping path and query, once PIPER_BASE_URL
names beta. The MCP OAuth issuer, its metadata, the sign-in it uses and /health stay on
alpha. #2283's host switch reverses with the same configuration."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from web.middleware import canonical_host as ch

ALPHA = "alpha.pipermorgan.ai"
BETA = "https://beta.pipermorgan.ai"


@pytest.fixture
def beta_canonical(monkeypatch):
    monkeypatch.setenv("PIPER_BASE_URL", BETA)


class TestOffUntilTheConfigurationMoves:
    def test_alpha_base_url_serves_alpha(self, monkeypatch):
        monkeypatch.setenv("PIPER_BASE_URL", f"https://{ALPHA}")
        assert ch.redirect_target(ALPHA, "/settings/integrations", "") is None

    def test_no_base_url_serves_alpha(self, monkeypatch):
        monkeypatch.delenv("PIPER_BASE_URL", raising=False)
        assert ch.redirect_target(ALPHA, "/", "") is None


class TestTheRedirect:
    def test_a_page_keeps_its_path_and_query(self, beta_canonical):
        assert (
            ch.redirect_target(ALPHA, "/settings/integrations", "github_success=true")
            == "https://beta.pipermorgan.ai/settings/integrations?github_success=true"
        )

    def test_the_old_callback_goes_to_beta_with_code_and_state(self, beta_canonical):
        path = "/api/v1/settings/integrations/github/callback"
        assert (
            ch.redirect_target(f"{ALPHA}:443", path, "code=c&state=s")
            == f"{BETA}{path}?code=c&state=s"
        )

    def test_a_login_for_the_app_goes_to_beta(self, beta_canonical):
        assert ch.redirect_target(ALPHA, "/login", "next=%2Fhome").startswith(BETA)

    @pytest.mark.parametrize("host", ["beta.pipermorgan.ai", "piper-morgan.fly.dev", "localhost"])
    def test_other_hosts_are_served_as_they_are(self, beta_canonical, host):
        assert ch.redirect_target(host, "/", "") is None


class TestWhatStaysOnAlpha:
    @pytest.mark.parametrize(
        "path, query",
        [
            ("/mcp/oauth/authorize", "client_id=x&code_challenge=y"),
            ("/mcp/oauth/token", ""),
            ("/.well-known/oauth-authorization-server/mcp/oauth", ""),
            ("/.well-known/oauth-protected-resource", ""),
            ("/login", "next=%2Fmcp%2Foauth%2Fauthorize%3Fclient_id%3Dx"),
            ("/api/v1/auth/login", ""),
            ("/static/css/auth.css", ""),
            ("/health", ""),
        ],
    )
    def test_the_mcp_issuer_and_its_sign_in_stay(self, beta_canonical, path, query):
        assert ch.redirect_target(ALPHA, path, query) is None

    def test_the_issuer_does_not_follow_the_base_url(self, beta_canonical, monkeypatch):
        from web.routers import mcp_oauth

        monkeypatch.delenv("MCP_OAUTH_ISSUER_URL", raising=False)
        assert mcp_oauth.issuer_url() == "https://alpha.pipermorgan.ai/mcp/oauth"


class TestTheServedApp:
    def test_alpha_answers_301_before_auth(self, beta_canonical):
        from web.app import app

        client = TestClient(app, base_url=f"https://{ALPHA}", follow_redirects=False)
        r = client.get("/settings/integrations?x=1")
        assert r.status_code == 301
        assert r.headers["location"] == f"{BETA}/settings/integrations?x=1"

    def test_a_post_keeps_its_method(self, beta_canonical):
        from web.app import app

        client = TestClient(app, base_url=f"https://{ALPHA}", follow_redirects=False)
        r = client.post("/api/v1/settings/integrations/github/disconnect")
        assert r.status_code == 308

    def test_health_answers_on_alpha(self, beta_canonical):
        from web.app import app

        client = TestClient(app, base_url=f"https://{ALPHA}", follow_redirects=False)
        assert client.get("/health").status_code != 301


class TestTheHostSwitchReverses:
    def test_a_connect_started_on_alpha_goes_to_beta(self):
        from services.auth.oauth_callback_guard import host_switch_url

        request = SimpleNamespace(url=SimpleNamespace(hostname=ALPHA))
        redirect = f"{BETA}/api/v1/settings/integrations/github/callback"
        assert host_switch_url(request, redirect, "/settings/github") == f"{BETA}/settings/github"
