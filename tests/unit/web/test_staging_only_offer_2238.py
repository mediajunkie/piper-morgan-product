"""#2238: Notion is offered on STAGING only, so its served check can run where no partner can reach it.

PPM (2026-11-01 08:4x): ``BETA_OFFERED_CONNECTORS`` is one code constant and one image
serves alpha and beta, so the check cannot use the beta offer; it runs on staging, by a
mechanism that cannot offer Notion on alpha or beta by any route. The mechanism:
``offered_connectors()`` = the beta set, plus ``STAGING_ONLY_OFFERED_CONNECTORS`` when and
only when ``FLY_APP_NAME`` is the staging app's name. Alpha and beta run as
``piper-morgan``; no env knob, no flag and no promotion changes their set.
"""

from __future__ import annotations

import pytest

from services.integrations import integration_status_service as iss


@pytest.fixture
def _no_app(monkeypatch):
    monkeypatch.delenv("FLY_APP_NAME", raising=False)


class TestWhereNotionIsOffered:
    def test_the_beta_set_is_unchanged(self, _no_app):
        assert iss.BETA_OFFERED_CONNECTORS == {"github": "GitHub", "calendar": "Google Calendar"}
        assert "notion" not in iss.BETA_OFFERED_CONNECTORS

    def test_locally_notion_is_not_offered(self, _no_app):
        assert iss.offered_connectors() == iss.BETA_OFFERED_CONNECTORS
        assert iss.connector_offered("notion") is False

    def test_on_alpha_and_beta_notion_is_not_offered(self, monkeypatch):
        monkeypatch.setenv(
            "FLY_APP_NAME", "piper-morgan"
        )  # fly.toml: one app serves alpha and beta
        assert iss.offered_connectors() == iss.BETA_OFFERED_CONNECTORS
        assert iss.connector_offered("notion") is False
        with pytest.raises(Exception) as caught:
            iss.refuse_unless_offered("notion")
        assert getattr(caught.value, "status_code", None) == 409

    def test_on_staging_notion_is_offered(self, monkeypatch):
        monkeypatch.setenv("FLY_APP_NAME", iss.STAGING_APP_NAME)
        assert iss.STAGING_APP_NAME == "piper-morgan-staging"
        offered = iss.offered_connectors()
        assert offered["notion"] == "Notion"
        assert set(iss.BETA_OFFERED_CONNECTORS) <= set(offered)
        assert iss.connector_offered("notion") is True
        iss.refuse_unless_offered("notion")  # no raise

    def test_a_misspelt_or_other_app_name_offers_nothing_extra(self, monkeypatch):
        for name in ("piper-morgan-staging-2", "staging", "PIPER-MORGAN-STAGING", ""):
            monkeypatch.setenv("FLY_APP_NAME", name)
            assert "notion" not in iss.offered_connectors(), name

    def test_the_pages_and_chat_read_this_hosts_set(self, monkeypatch):
        """The integrations page, the setup page and the chat capability lines read
        ``offered_connectors()``, not the constant, so the staging extra reaches the
        save route, the card and the chat lines together."""
        from pathlib import Path

        root = Path(__file__).resolve().parents[3]
        ui = (root / "web/api/routes/ui.py").read_text()
        assert "integration_status_service.BETA_OFFERED_CONNECTORS" not in ui
        assert ui.count("integration_status_service.offered_connectors()") == 2
        cap = (root / "services/intent_service/capability_answer.py").read_text()
        assert "offered_connectors()" in cap
        handlers = (root / "services/intent_service/canonical_handlers.py").read_text()
        assert "BETA_OFFERED_CONNECTORS = offered_connectors()" in handlers
