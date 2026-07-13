"""Hosted-aware setup-wizard system checks (the 2026-07-12 beta live find).

A fresh tester on beta.pipermorgan.ai saw the self-host wizard fail Docker/
PostgreSQL/ChromaDB checks — each a hosted env-contract mismatch: Fly's
Firecracker microVMs have no /.dockerenv; Fly carries DATABASE_URL (not
POSTGRES_*); fly.toml names CHROMA_HOST (not CHROMADB_HOST).
"""

from unittest.mock import AsyncMock, patch

import pytest

import web.api.routes.setup as setup_mod


class TestDatabaseCheck:
    @pytest.mark.asyncio
    async def test_database_url_honored_first(self, monkeypatch):
        monkeypatch.setenv("DATABASE_URL", "postgres://u:p@piper-morgan-db.flycast:5432/db")
        with patch.object(setup_mod, "check_service_port", new=AsyncMock(return_value=True)) as csp:
            assert await setup_mod.check_database() is True
        csp.assert_awaited_once_with("piper-morgan-db.flycast", 5432)

    @pytest.mark.asyncio
    async def test_postgres_env_fallback(self, monkeypatch):
        monkeypatch.delenv("DATABASE_URL", raising=False)
        monkeypatch.setenv("POSTGRES_HOST", "postgres")
        monkeypatch.setenv("POSTGRES_PORT", "5432")
        with patch.object(setup_mod, "check_service_port", new=AsyncMock(return_value=True)) as csp:
            assert await setup_mod.check_database() is True
        csp.assert_awaited_once_with("postgres", 5432)


class TestChromaCheck:
    @pytest.mark.asyncio
    async def test_chroma_host_spelling_honored(self, monkeypatch):
        """fly.toml's CHROMA_HOST/CHROMA_PORT names must work."""
        monkeypatch.setenv("CHROMA_HOST", "piper-morgan-chroma.internal")
        monkeypatch.setenv("CHROMA_PORT", "8000")
        with patch.object(setup_mod, "check_service_port", new=AsyncMock(return_value=True)) as csp:
            assert await setup_mod.check_chromadb() is True
        csp.assert_awaited_once_with("piper-morgan-chroma.internal", 8000)


class TestLoginTemplateInvitePath:
    def test_login_offers_the_invite_route(self):
        html = open("templates/login.html").read()
        assert "invite code" in html.lower()
        assert 'href="/setup"' in html
