"""#2279 (CXO 2026-11-04 18:32): the dedicated GitHub settings page's OAuth-connected
subtitle claims no owner. "Connected with your GitHub account." said "your" without
naming one, the claim the #2266 thread was about; the page reads ``oauth-status``, which
carries no login, so the ruled text is "Connected with GitHub.", matching the group line
on the same page. "Connected as {login}" lives on the Integrations card, read from the
account's own grant."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def test_the_subtitle_claims_no_owner():
    src = (ROOT / "templates/settings_github.html").read_text()
    assert "subtitleEl.textContent = 'Connected with GitHub.'" in src
    assert "Connected with your GitHub account." not in src


def test_the_oauth_status_route_carries_no_login_so_the_page_names_none():
    src = (ROOT / "web/api/routes/settings_integrations.py").read_text()
    i = src.index("async def github_oauth_status")
    body = src[i : src.index("\n\n\nasync def _github_pat_serving", i)]
    assert '"login"' not in body and "account_login" not in body
