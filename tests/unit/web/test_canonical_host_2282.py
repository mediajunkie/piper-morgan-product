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

    @pytest.mark.parametrize("path", ["/reset-password", "/setup", "/home", "/api/v1/auth/me"])
    def test_the_login_pages_other_links_go_to_beta(self, beta_canonical, path):
        assert ch.redirect_target(ALPHA, path, "").startswith(BETA)

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
            ("/login", ""),
            ("/api/v1/auth/login", ""),
            ("/static/css/auth.css", ""),
            ("/assets/logo.svg", ""),
            ("/health", ""),
        ],
    )
    def test_the_mcp_issuer_and_its_sign_in_stay(self, beta_canonical, path, query):
        assert ch.redirect_target(ALPHA, path, query) is None

    def test_the_issuer_does_not_follow_the_base_url(self, beta_canonical, monkeypatch):
        """Arch pin 1: with PIPER_BASE_URL on beta, the AS issuer and the MCP app's
        protected-resource authorization server both still read alpha's issuer."""
        from services.mcp.server import app as mcp_app
        from web.routers import mcp_oauth

        monkeypatch.delenv("MCP_OAUTH_ISSUER_URL", raising=False)
        assert mcp_oauth.issuer_url() == "https://alpha.pipermorgan.ai/mcp/oauth"
        assert str(mcp_app._auth_settings().issuer_url).rstrip("/") == (
            "https://alpha.pipermorgan.ai/mcp/oauth"
        )

    def test_the_served_metadata_names_alphas_issuer(self, beta_canonical, monkeypatch):
        from web.app import app

        monkeypatch.delenv("MCP_OAUTH_ISSUER_URL", raising=False)
        client = TestClient(app, base_url=f"https://{ALPHA}", follow_redirects=False)
        r = client.get("/.well-known/oauth-authorization-server/mcp/oauth")
        assert r.status_code == 200
        assert r.json()["issuer"].rstrip("/") == "https://alpha.pipermorgan.ai/mcp/oauth"

    def test_a_signed_out_connector_sign_in_never_leaves_alpha(self, beta_canonical):
        """Arch pin 2, at the redirect layer: authorize sends a signed-out browser to
        alpha's own /login, the page and its POST answer on alpha, never 301/308. The
        consent page after a real sign-in needs a database user, so the last hop is
        PA's served check (b)."""
        from web.app import app

        client = TestClient(app, base_url=f"https://{ALPHA}", follow_redirects=False)
        r = client.get("/mcp/oauth/authorize?client_id=x&response_type=code")
        assert r.status_code not in (301, 308)
        loc = r.headers.get("location", "")
        assert not loc.startswith(BETA)
        assert client.get("/login?next=%2Fmcp%2Foauth%2Fauthorize").status_code not in (301, 308)
        login = client.post("/api/v1/auth/login", json={"username": "x", "password": "y"})
        assert login.status_code not in (301, 308)


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
