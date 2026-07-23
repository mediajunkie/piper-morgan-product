"""
Tests for #1318 fix: system-check functions use env-var addresses, not hardcoded localhost.

Verifies that check_database, check_redis, check_chromadb, check_temporal, and check_docker
all read from environment variables so they work correctly on the hosted Droplet (Docker-internal
addresses) and in local dev (localhost defaults).
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock


class TestCheckDatabase:
    @pytest.mark.asyncio
    async def test_uses_postgres_host_env_var(self):
        with patch("web.api.routes.setup.check_service_port", new_callable=AsyncMock) as mock_port:
            mock_port.return_value = True
            with patch.dict("os.environ", {"POSTGRES_HOST": "postgres", "POSTGRES_PORT": "5432"}):
                from web.api.routes.setup import check_database

                await check_database()
            mock_port.assert_called_once_with("postgres", 5432)

    @pytest.mark.asyncio
    async def test_falls_back_to_localhost_5433_for_local_dev(self):
        with patch("web.api.routes.setup.check_service_port", new_callable=AsyncMock) as mock_port:
            mock_port.return_value = True
            with patch.dict("os.environ", {}, clear=False):
                env_without = {
                    k: v
                    for k, v in __import__("os").environ.items()
                    if k not in ("POSTGRES_HOST", "POSTGRES_PORT")
                }
                with patch.dict("os.environ", env_without, clear=True):
                    from web.api.routes.setup import check_database

                    await check_database()
            mock_port.assert_called_once_with("localhost", 5433)


class TestCheckRedis:
    @pytest.mark.asyncio
    async def test_parses_host_and_port_from_redis_url(self):
        with patch("web.api.routes.setup.check_service_port", new_callable=AsyncMock) as mock_port:
            mock_port.return_value = True
            with patch.dict("os.environ", {"REDIS_URL": "redis://:secret@redis:6379"}):
                from web.api.routes.setup import check_redis

                await check_redis()
            mock_port.assert_called_once_with("redis", 6379)

    @pytest.mark.asyncio
    async def test_falls_back_to_localhost_6379_without_redis_url(self):
        with patch("web.api.routes.setup.check_service_port", new_callable=AsyncMock) as mock_port:
            mock_port.return_value = True
            env_without = {k: v for k, v in __import__("os").environ.items() if k != "REDIS_URL"}
            with patch.dict("os.environ", env_without, clear=True):
                from web.api.routes.setup import check_redis

                await check_redis()
            mock_port.assert_called_once_with("localhost", 6379)

    @pytest.mark.asyncio
    async def test_handles_redis_url_with_no_password(self):
        with patch("web.api.routes.setup.check_service_port", new_callable=AsyncMock) as mock_port:
            mock_port.return_value = True
            with patch.dict("os.environ", {"REDIS_URL": "redis://myredis:6380"}):
                from web.api.routes.setup import check_redis

                await check_redis()
            mock_port.assert_called_once_with("myredis", 6380)


class TestCheckChromadb:
    @pytest.mark.asyncio
    async def test_uses_chromadb_host_env_var_when_set(self):
        with patch("web.api.routes.setup.check_service_port", new_callable=AsyncMock) as mock_port:
            mock_port.return_value = True
            # #1452: the route honors the Fly spelling CHROMA_HOST FIRST —
            # .env sets it locally (via conftest load_dotenv), shadowing the
            # CHROMADB_* patch. Control both spellings.
            import os as _os

            env_clean = {
                k: v
                for k, v in _os.environ.items()
                if k not in ("CHROMA_HOST", "CHROMA_PORT")
            }
            env_clean.update({"CHROMADB_HOST": "my-chromadb", "CHROMADB_PORT": "9000"})
            with patch.dict("os.environ", env_clean, clear=True):
                from web.api.routes.setup import check_chromadb

                await check_chromadb()
            mock_port.assert_called_once_with("my-chromadb", 9000)

    @pytest.mark.asyncio
    async def test_defaults_to_chromadb_service_name_inside_docker(self):
        with patch("web.api.routes.setup.check_service_port", new_callable=AsyncMock) as mock_port:
            mock_port.return_value = True
            with patch("web.api.routes.setup._IN_DOCKER", True):
                env_without = {
                    k: v
                    for k, v in __import__("os").environ.items()
                    if k
                    not in ("CHROMADB_HOST", "CHROMADB_PORT", "CHROMA_HOST", "CHROMA_PORT")
                }
                with patch.dict("os.environ", env_without, clear=True):
                    from web.api.routes.setup import check_chromadb

                    await check_chromadb()
            mock_port.assert_called_once_with("chromadb", 8000)

    @pytest.mark.asyncio
    async def test_defaults_to_localhost_outside_docker(self):
        with patch("web.api.routes.setup.check_service_port", new_callable=AsyncMock) as mock_port:
            mock_port.return_value = True
            with patch("web.api.routes.setup._IN_DOCKER", False):
                env_without = {
                    k: v
                    for k, v in __import__("os").environ.items()
                    if k
                    not in ("CHROMADB_HOST", "CHROMADB_PORT", "CHROMA_HOST", "CHROMA_PORT")
                }
                with patch.dict("os.environ", env_without, clear=True):
                    from web.api.routes.setup import check_chromadb

                    await check_chromadb()
            mock_port.assert_called_once_with("localhost", 8000)


class TestCheckTemporal:
    @pytest.mark.asyncio
    async def test_uses_temporal_host_env_var(self):
        with patch("web.api.routes.setup.check_service_port", new_callable=AsyncMock) as mock_port:
            mock_port.return_value = True
            with patch.dict("os.environ", {"TEMPORAL_HOST": "temporal", "TEMPORAL_PORT": "7233"}):
                from web.api.routes.setup import check_temporal

                await check_temporal()
            mock_port.assert_called_once_with("temporal", 7233)

    @pytest.mark.asyncio
    async def test_falls_back_to_localhost_7233(self):
        with patch("web.api.routes.setup.check_service_port", new_callable=AsyncMock) as mock_port:
            mock_port.return_value = True
            env_without = {
                k: v
                for k, v in __import__("os").environ.items()
                if k not in ("TEMPORAL_HOST", "TEMPORAL_PORT")
            }
            with patch.dict("os.environ", env_without, clear=True):
                from web.api.routes.setup import check_temporal

                await check_temporal()
            mock_port.assert_called_once_with("localhost", 7233)


class TestCheckDocker:
    @pytest.mark.asyncio
    async def test_returns_true_when_running_inside_docker(self):
        with patch("web.api.routes.setup._IN_DOCKER", True):
            from web.api.routes.setup import check_docker

            result = await check_docker()
        assert result is True

    @pytest.mark.asyncio
    async def test_checks_cli_outside_docker_when_available(self):
        mock_result = MagicMock()
        mock_result.returncode = 0
        with patch("web.api.routes.setup._IN_DOCKER", False):
            with patch("asyncio.to_thread", new_callable=AsyncMock, return_value=mock_result):
                from web.api.routes.setup import check_docker

                result = await check_docker()
        assert result is True

    @pytest.mark.asyncio
    async def test_returns_false_outside_docker_without_cli(self):
        with patch("web.api.routes.setup._IN_DOCKER", False):
            with patch("asyncio.to_thread", side_effect=FileNotFoundError):
                from web.api.routes.setup import check_docker

                result = await check_docker()
        assert result is False
