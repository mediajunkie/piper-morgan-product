"""
ngrok Service for Slack Integration
Provides ngrok tunnel management for development following GitHub integration patterns.

Manages ngrok tunnels for local development including:
- Automatic tunnel creation and URL configuration
- Health monitoring and reconnection
- Integration with Slack webhook configuration
- Dynamic URL updates for OAuth callbacks
- Error handling and retry logic following established patterns
"""

import asyncio
import json
import logging
import os
import subprocess
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx

logger = logging.getLogger(__name__)


@dataclass
class NgrokTunnel:
    """ngrok tunnel information"""

    name: str
    public_url: str
    local_port: int
    protocol: str = "http"
    created_at: Optional[float] = None
    status: str = "active"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "public_url": self.public_url,
            "local_port": self.local_port,
            "protocol": self.protocol,
            "created_at": self.created_at,
            "status": self.status,
        }


class NgrokService:
    """
    ngrok tunnel management service for Slack development.

    Provides automated tunnel creation, health monitoring, and configuration
    management for local Slack integration development.
    """

    def __init__(self, local_port: int = 8001, api_port: int = 4040):
        self.local_port = local_port
        self.api_port = api_port
        self.api_base_url = f"http://localhost:{api_port}"

        # Tunnel tracking
        self._active_tunnels: Dict[str, NgrokTunnel] = {}
        self._ngrok_process: Optional[subprocess.Popen] = None

        # Configuration
        self.tunnel_name = "piper-morgan-slack"
        self.max_retries = 3
        self.retry_delay = 5.0

        logger.info(f"NgrokService initialized for port {local_port}")

    async def start_tunnel(
        self, subdomain: Optional[str] = None, auth_token: Optional[str] = None
    ) -> NgrokTunnel:
        """
        Start ngrok tunnel for Slack integration.

        Args:
            subdomain: Custom subdomain (requires ngrok pro/business)
            auth_token: ngrok auth token for advanced features

        Returns:
            NgrokTunnel instance with public URL information
        """
        try:
            # Check if ngrok is installed
            if not self._check_ngrok_installed():
                raise RuntimeError("ngrok is not installed or not in PATH")

            # Set auth token if provided
            if auth_token:
                await self._set_auth_token(auth_token)

            # Start ngrok process
            await self._start_ngrok_process(subdomain)

            # Wait for tunnel to be ready
            tunnel = await self._wait_for_tunnel_ready()

            # Store tunnel information
            self._active_tunnels[self.tunnel_name] = tunnel

            logger.info(f"ngrok tunnel started: {tunnel.public_url} -> localhost:{self.local_port}")

            return tunnel

        except Exception as e:
            logger.error(f"Failed to start ngrok tunnel: {e}")
            await self.stop_tunnel()  # Cleanup on failure
            raise RuntimeError(f"ngrok tunnel startup failed: {e}") from e

    def create_tunnel(self, port: int) -> str:
        """
        Create ngrok tunnel (TDD-compatible wrapper for start_tunnel).

        This method provides a simpler sync interface matching TDD test expectations.
        Internally delegates to _create_tunnel which can be mocked in tests.

        Args:
            port: Local port to tunnel to

        Returns:
            Public tunnel URL
        """
        return self._create_tunnel(port)

    def _create_tunnel(self, port: int) -> str:
        """
        Internal tunnel creation (for test mocking compatibility).

        This method does the actual work and can be mocked in tests.
        """
        import asyncio

        # Get or create event loop
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No running loop, create one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            tunnel_info = loop.run_until_complete(self.start_tunnel(port))
            loop.close()
        else:
            # Running in async context
            tunnel_info = asyncio.create_task(self.start_tunnel(port))

        # Extract public URL from tunnel info
        if isinstance(tunnel_info, dict):
            return tunnel_info.get("public_url", "")
        return str(tunnel_info)

    def _validate_tunnel_url(self, url: str) -> bool:
        """
        Validate that a URL is a valid ngrok tunnel URL.

        Args:
            url: URL to validate

        Returns:
            True if valid ngrok URL, False otherwise
        """
        if not url:
            return False

        # Check for ngrok.io domain
        if "ngrok.io" not in url and "ngrok.app" not in url:
            return False

        # Must be HTTPS
        if not url.startswith("https://"):
            return False

        return True

    async def stop_tunnel(self) -> bool:
        """Stop ngrok tunnel and cleanup resources"""

        try:
            success = True

            # Stop ngrok process
            if self._ngrok_process:
                try:
                    self._ngrok_process.terminate()

                    # Wait for graceful shutdown
                    try:
                        self._ngrok_process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        logger.warning("ngrok process did not terminate gracefully, forcing kill")
                        self._ngrok_process.kill()
                        self._ngrok_process.wait()

                    self._ngrok_process = None
                    logger.info("ngrok process stopped")

                except Exception as e:
                    logger.error(f"Error stopping ngrok process: {e}")
                    success = False

            # Clear tunnel tracking
            self._active_tunnels.clear()

            return success

        except Exception as e:
            logger.error(f"Error during tunnel cleanup: {e}")
            return False

    def cleanup_tunnel(self) -> None:
        """
        Cleanup ngrok tunnel (TDD-compatible wrapper for stop_tunnel).

        This method provides a simpler sync interface matching TDD test expectations.
        Internally delegates to _delete_tunnel which can be mocked in tests.
        """
        self._delete_tunnel()

    def setup_webhook_tunnel(self, port: int, webhook_router=None) -> str:
        """
        Setup complete webhook tunnel (convenience method for TDD).

        Creates tunnel and optionally configures webhook router with the URL.

        Args:
            port: Local port to tunnel to
            webhook_router: Optional webhook router to configure

        Returns:
            Tunnel URL
        """
        # Create the tunnel
        tunnel_url = self.create_tunnel(port)

        # Configure webhook router if provided
        if webhook_router and hasattr(webhook_router, "set_webhook_url"):
            webhook_router.set_webhook_url(tunnel_url)

        return tunnel_url

    def _delete_tunnel(self) -> None:
        """
        Internal tunnel deletion (for test mocking compatibility).

        This method does the actual work and can be mocked in tests.
        """
        import asyncio

        # Get or create event loop
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No running loop, create one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.stop_tunnel())
            loop.close()
        else:
            # Running in async context
            asyncio.create_task(self.stop_tunnel())

    async def get_tunnel_info(self) -> Optional[NgrokTunnel]:
        """Get information about the active tunnel"""

        if self.tunnel_name in self._active_tunnels:
            return self._active_tunnels[self.tunnel_name]

        # Try to discover existing tunnel
        try:
            tunnels = await self._get_tunnels_from_api()
            for tunnel_data in tunnels:
                if tunnel_data.get("name") == self.tunnel_name:
                    tunnel = NgrokTunnel(
                        name=tunnel_data["name"],
                        public_url=tunnel_data["public_url"],
                        local_port=self.local_port,
                        protocol=tunnel_data.get("proto", "http"),
                        status="active",
                    )
                    self._active_tunnels[self.tunnel_name] = tunnel
                    return tunnel

        except Exception as e:
            logger.warning(f"Could not discover existing tunnel: {e}")

        return None

    async def check_tunnel_health(self) -> Dict[str, Any]:
        """Check tunnel health and connectivity"""

        health_status = {
            "tunnel_active": False,
            "public_url": None,
            "local_reachable": False,
            "external_reachable": False,
            "ngrok_api_reachable": False,
            "last_check": time.time(),
        }

        try:
            # Check if tunnel exists
            tunnel = await self.get_tunnel_info()
            if tunnel:
                health_status["tunnel_active"] = True
                health_status["public_url"] = tunnel.public_url

                # Check local endpoint
                health_status["local_reachable"] = await self._check_local_endpoint()

                # Check external accessibility
                if tunnel.public_url:
                    health_status["external_reachable"] = await self._check_external_endpoint(
                        tunnel.public_url
                    )

            # Check ngrok API
            health_status["ngrok_api_reachable"] = await self._check_ngrok_api()

        except Exception as e:
            logger.error(f"Error checking tunnel health: {e}")
            health_status["error"] = str(e)

        return health_status

    async def restart_tunnel_if_needed(self) -> bool:
        """Restart tunnel if health check fails"""

        try:
            health = await self.check_tunnel_health()

            # Restart if tunnel is not active or not externally reachable
            if not health["tunnel_active"] or not health["external_reachable"]:
                logger.info("Tunnel health check failed, restarting...")

                await self.stop_tunnel()
                tunnel = await self.start_tunnel()

                logger.info(f"Tunnel restarted successfully: {tunnel.public_url}")
                return True

            return False  # No restart needed

        except Exception as e:
            logger.error(f"Error during tunnel restart: {e}")
            return False

    def get_webhook_url(self, endpoint: str = "/slack/webhooks") -> Optional[str]:
        """Get webhook URL for Slack configuration"""

        tunnel = self._active_tunnels.get(self.tunnel_name)
        if not tunnel:
            return None

        return urljoin(tunnel.public_url, endpoint.lstrip("/"))

    def get_oauth_redirect_url(self, endpoint: str = "/slack/oauth/callback") -> Optional[str]:
        """Get OAuth redirect URL for Slack app configuration"""

        tunnel = self._active_tunnels.get(self.tunnel_name)
        if not tunnel:
            return None

        return urljoin(tunnel.public_url, endpoint.lstrip("/"))

    # Private helper methods

    def _check_ngrok_installed(self) -> bool:
        """Check if ngrok is installed and accessible"""

        try:
            result = subprocess.run(
                ["ngrok", "version"], capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    async def _set_auth_token(self, auth_token: str) -> None:
        """Set ngrok auth token"""

        try:
            result = subprocess.run(
                ["ngrok", "config", "add-authtoken", auth_token],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                raise RuntimeError(f"Failed to set ngrok auth token: {result.stderr}")

            logger.info("ngrok auth token configured")

        except subprocess.TimeoutExpired:
            raise RuntimeError("ngrok auth token configuration timed out")

    async def _start_ngrok_process(self, subdomain: Optional[str] = None) -> None:
        """Start ngrok background process"""

        # Build ngrok command
        cmd = ["ngrok", "http", str(self.local_port), "--log=stdout"]

        if subdomain:
            cmd.extend(["--subdomain", subdomain])

        # Start process
        try:
            self._ngrok_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            # Give process time to start
            await asyncio.sleep(2)

            # Check if process is still running
            if self._ngrok_process.poll() is not None:
                stdout, stderr = self._ngrok_process.communicate()
                raise RuntimeError(f"ngrok process failed to start: {stderr}")

            logger.info("ngrok process started successfully")

        except Exception as e:
            if self._ngrok_process:
                self._ngrok_process.kill()
                self._ngrok_process = None
            raise RuntimeError(f"Failed to start ngrok process: {e}") from e

    async def _wait_for_tunnel_ready(self, timeout: int = 30) -> NgrokTunnel:
        """Wait for tunnel to be ready and get URL"""

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                tunnels = await self._get_tunnels_from_api()

                for tunnel_data in tunnels:
                    if tunnel_data.get("config", {}).get("addr") == f"localhost:{self.local_port}":
                        public_url = tunnel_data["public_url"]

                        # Prefer HTTPS URL if available
                        if public_url.startswith("http://"):
                            for t in tunnels:
                                if t.get("config", {}).get(
                                    "addr"
                                ) == f"localhost:{self.local_port}" and t["public_url"].startswith(
                                    "https://"
                                ):
                                    public_url = t["public_url"]
                                    break

                        tunnel = NgrokTunnel(
                            name=self.tunnel_name,
                            public_url=public_url,
                            local_port=self.local_port,
                            protocol=tunnel_data.get("proto", "http"),
                            created_at=time.time(),
                            status="active",
                        )

                        return tunnel

            except Exception as e:
                logger.debug(f"Waiting for tunnel: {e}")

            await asyncio.sleep(1)

        raise RuntimeError(f"Tunnel did not become ready within {timeout} seconds")

    async def _get_tunnels_from_api(self) -> list:
        """Get tunnel information from ngrok API"""

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.api_base_url}/api/tunnels", timeout=5.0)
                response.raise_for_status()

                data = response.json()
                return data.get("tunnels", [])

            except httpx.ConnectError:
                raise RuntimeError("Cannot connect to ngrok API - is ngrok running?")
            except httpx.TimeoutException:
                raise RuntimeError("ngrok API request timed out")

    async def _check_local_endpoint(self) -> bool:
        """Check if local endpoint is reachable"""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://localhost:{self.local_port}/health", timeout=5.0
                )
                return response.status_code < 500
        except Exception:
            return False

    async def _check_external_endpoint(self, public_url: str) -> bool:
        """Check if external endpoint is reachable"""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{public_url}/health", timeout=10.0)
                return response.status_code < 500
        except Exception:
            return False

    async def _check_ngrok_api(self) -> bool:
        """Check if ngrok API is reachable"""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_base_url}/api/tunnels", timeout=5.0)
                return response.status_code == 200
        except Exception:
            return False

    def get_service_status(self) -> Dict[str, Any]:
        """Get ngrok service status and metrics"""

        return {
            "service_status": "running" if self._ngrok_process else "stopped",
            "local_port": self.local_port,
            "api_port": self.api_port,
            "active_tunnels": len(self._active_tunnels),
            "tunnel_info": [t.to_dict() for t in self._active_tunnels.values()],
            "ngrok_process_running": self._ngrok_process is not None
            and self._ngrok_process.poll() is None,
        }
