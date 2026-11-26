"""
Tests for #1318 fix: system-check functions use env-var addresses, not hardcoded localhost.

Verifies that check_database, check_redis, check_chromadb, check_temporal, and check_docker
all read from environment variables so they work correctly on the hosted Droplet (Docker-internal
addresses) and in local dev (localhost defaults).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


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
    """#2244: the three tests here pinned which server host and port the check
    probed (CHROMADB_HOST, the docker service name, localhost). The app has no
    Chroma server client, so the check now tests the in-process store's folder.
    One test keeps the class's point: no environment spelling sends it to a port.
    Full coverage: tests/unit/services/infrastructure/test_data_paths_2244.py."""

    @pytest.mark.asyncio
    async def test_no_host_spelling_sends_the_check_to_a_port(self, tmp_path):
        with patch("web.api.routes.setup.check_service_port", new_callable=AsyncMock) as mock_port:
            mock_port.return_value = False
            env = {
                "CHROMADB_HOST": "my-chromadb",
                "CHROMADB_PORT": "9000",
                "CHROMA_HOST": "other",
                "PIPER_DATA_DIR": str(tmp_path / "vol"),
            }
            with patch.dict("os.environ", env):
                from web.api.routes.setup import check_chromadb

                assert await check_chromadb() is True
            mock_port.assert_not_called()


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
