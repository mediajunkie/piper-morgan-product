"""
MCP Consumer Core - Main Consumer Implementation

Integrates protocol handling, service discovery, and spatial adapter patterns
to provide a working MCP Consumer for external service integration.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from services.infrastructure.mcp.connection_pool import MCPConnectionPool

from ..exceptions import MCPConnectionError, MCPTimeoutError
from ..protocol.protocol_client import MCPProtocolClient
from ..protocol.service_discovery import MCPServiceDiscovery, MCPServiceInfo

logger = logging.getLogger(__name__)


class MCPConsumerCore:
    """
    Minimal viable MCP consumer

    - Connect to one service
    - Send/receive messages
    - Handle errors gracefully
    - Integrate with existing spatial adapter patterns
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.service_discovery = MCPServiceDiscovery()
        self.connection_pool = MCPConnectionPool()
        self._active_connections: Dict[str, MCPProtocolClient] = {}
        self._service_configs: Dict[str, Dict[str, Any]] = {}
        self._connected = False

    async def connect(
        self, service_name: str, service_config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Connect to an MCP service"""
        try:
            self.logger.info(f"Connecting to MCP service: {service_name}")

            # Use provided config or default
            if service_config is None:
                service_config = self._get_default_service_config(service_name)

            # Store service config
            self._service_configs[service_name] = service_config

            # Discover and connect to service
            services = await self.service_discovery.discover_services(
                {"services": [service_config]}
            )

            if services:
                # Get the discovered service
                service_info = services[0]
                self.logger.info(f"Discovered MCP service: {service_info.name}")

                # Connect to the service
                client = await self.service_discovery.connect_to_service(service_name)
                if client:
                    self._active_connections[service_name] = client
                    self._connected = True
                    self.logger.info(f"Successfully connected to MCP service: {service_name}")
                    return True
                else:
                    self.logger.error(f"Failed to connect to MCP service: {service_name}")
                    return False
            else:
                self.logger.error(f"No MCP service discovered for: {service_name}")
                return False

        except Exception as e:
            self.logger.error(f"Error connecting to MCP service {service_name}: {e}")
            return False

    def is_connected(self) -> bool:
        """Check if connected to any MCP service"""
        return self._connected and len(self._active_connections) > 0

    async def disconnect(self, service_name: Optional[str] = None) -> None:
        """Disconnect from MCP service(s)"""
        try:
            if service_name:
                # Disconnect specific service
                if service_name in self._active_connections:
                    client = self._active_connections.pop(service_name)
                    await client.disconnect()
                    self.logger.info(f"Disconnected from MCP service: {service_name}")
            else:
                # Disconnect all services
                for service, client in self._active_connections.items():
                    await client.disconnect()
                    self.logger.info(f"Disconnected from MCP service: {service}")
                self._active_connections.clear()

            # Update connection status
            self._connected = len(self._active_connections) > 0

        except Exception as e:
            self.logger.error(f"Error disconnecting from MCP service: {e}")

    async def execute(self, command: str, **kwargs) -> Any:
        """Execute a command on the connected MCP service"""
        try:
            # For now, assume we're connected to the first service
            # In a real implementation, this would be more sophisticated
            if not self._active_connections:
                raise MCPConnectionError("No MCP services connected")

            service_name = list(self._active_connections.keys())[0]
            client = self._active_connections[service_name]

            self.logger.info(
                f"Executing command '{command}' on service '{service_name}' with args: {kwargs}"
            )

            # Execute command based on type
            if command == "list_issues":
                return await self._execute_list_issues(client, **kwargs)
            elif command == "list_tools":
                return await client.list_tools_protocol()
            elif command == "list_resources":
                return await client.list_resources_protocol()
            elif command == "call_tool":
                tool_name = kwargs.get("tool_name")
                arguments = kwargs.get("arguments", {})
                if tool_name:
                    return await client.call_tool_protocol(tool_name, arguments)
                else:
                    raise ValueError("tool_name required for call_tool command")
            else:
                raise ValueError(f"Unknown command: {command}")

        except Exception as e:
            self.logger.error(f"Error executing command '{command}': {e}")
            raise

    async def _execute_list_issues(
        self, client: MCPProtocolClient, **kwargs
    ) -> List[Dict[str, Any]]:
        """Execute list_issues command.

        Issue #1042: removed hardcoded "piper-morgan" fallback. Callers must
        pass ``repo`` (typically the GitHub adapter does after resolving
        via ``repo_resolver``). Returns empty list if not provided.
        """
        try:
            repo = kwargs.get("repo")
            if not repo:
                self.logger.warning(
                    "_execute_list_issues called without 'repo' kwarg; "
                    "returning empty list (Issue #1042)"
                )
                return []
            self.logger.info(f"Listing issues for repository: {repo}")

            # Try to call the list_issues tool if available
            try:
                result = await client.call_tool_protocol("list_issues", {"repository": repo})
                if result:
                    return result
            except Exception as e:
                self.logger.debug(f"list_issues tool not available, trying resources: {e}")

            # Fallback to listing resources
            resources = await client.list_resources_protocol()

            # Transform resources to issue format for demo
            issues = []
            for i, resource in enumerate(resources):
                issues.append(
                    {
                        "number": i + 1,
                        "title": resource.get("name", f"Issue {i + 1}"),
                        "description": resource.get("description", "No description available"),
                        "state": "open",
                        "repository": repo,
                        "uri": resource.get("uri", ""),
                        "mime_type": resource.get("mime_type", "text/plain"),
                    }
                )

            self.logger.info(f"Found {len(issues)} issues for repository {repo}")
            return issues

        except Exception as e:
            self.logger.error(f"Error executing list_issues: {e}")
            # Return demo data for testing (Issue #1042: use whatever repo was
            # passed, no hardcoded fallback)
            demo_repo = kwargs.get("repo") or "<unspecified>"
            return [
                {
                    "number": 1,
                    "title": "MCP Integration Implementation",
                    "description": "Implement MCP Consumer for external service integration",
                    "state": "open",
                    "repository": demo_repo,
                    "uri": "mcp://demo/issue/1",
                    "mime_type": "text/plain",
                },
                {
                    "number": 2,
                    "title": "GitHub MCP Adapter",
                    "description": "Create GitHub MCP spatial adapter following established patterns",
                    "state": "open",
                    "repository": demo_repo,
                    "uri": "mcp://demo/issue/2",
                    "mime_type": "text/plain",
                },
            ]

    def _get_default_service_config(self, service_name: str) -> Dict[str, Any]:
        """Get default configuration for a service"""
        if service_name.lower() == "github":
            return {
                "name": "github",
                "version": "1.0.0",
                "description": "GitHub MCP Service",
                "transport": "stdio",
                "simulation_mode": True,  # Use simulation for demo
                "timeout": 30.0,
            }
        elif service_name.lower() == "linear":
            return {
                "name": "linear",
                "version": "1.0.0",
                "description": "Linear MCP Service",
                "transport": "stdio",
                "simulation_mode": True,
                "timeout": 30.0,
            }
        else:
            # Generic service config
            return {
                "name": service_name,
                "version": "1.0.0",
                "description": f"{service_name} MCP Service",
                "transport": "stdio",
                "simulation_mode": True,
                "timeout": 30.0,
            }

    async def disconnect(self, service_name: Optional[str] = None):
        """Disconnect from MCP service(s)"""
        try:
            if service_name:
                # Disconnect from specific service
                if service_name in self._active_connections:
                    await self.service_discovery.disconnect_from_service(service_name)
                    del self._active_connections[service_name]
                    self.logger.info(f"Disconnected from MCP service: {service_name}")
            else:
                # Disconnect from all services
                for name in list(self._active_connections.keys()):
                    await self.service_discovery.disconnect_from_service(name)
                    del self._active_connections[name]
                self.logger.info("Disconnected from all MCP services")

        except Exception as e:
            self.logger.error(f"Error disconnecting from MCP service(s): {e}")

    def is_connected(self, service_name: Optional[str] = None) -> bool:
        """Check if connected to MCP service(s)"""
        if service_name:
            return service_name in self._active_connections
        else:
            return len(self._active_connections) > 0

    def get_connected_services(self) -> List[str]:
        """Get list of connected service names"""
        return list(self._active_connections.keys())

    def get_service_info(self, service_name: str) -> Optional[MCPServiceInfo]:
        """Get information about a service"""
        return self.service_discovery.get_service_info(service_name)

    async def health_check(self) -> Dict[str, bool]:
        """Check health of all connected services"""
        try:
            health_status = {}

            for service_name in self._active_connections:
                try:
                    client = self._active_connections[service_name]
                    health_status[service_name] = client.is_initialized()
                except Exception as e:
                    self.logger.error(f"Error checking health of service {service_name}: {e}")
                    health_status[service_name] = False

            return health_status

        except Exception as e:
            self.logger.error(f"Error during health check: {e}")
            return {}

    def get_stats(self) -> Dict[str, Any]:
        """Get consumer statistics"""
        discovery_stats = self.service_discovery.get_discovery_stats()

        consumer_stats = {
            "active_connections": len(self._active_connections),
            "connected_services": list(self._active_connections.keys()),
            "service_configs": len(self._service_configs),
        }

        return {**discovery_stats, **consumer_stats}

    async def cleanup(self):
        """Cleanup resources"""
        try:
            # Disconnect from all services
            await self.disconnect()

            # Clear service configs
            self._service_configs.clear()

            self.logger.info("MCP Consumer cleanup completed")

        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.cleanup()
