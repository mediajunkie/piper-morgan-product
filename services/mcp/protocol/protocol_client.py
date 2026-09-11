"""
MCP Protocol Client - Extended Client with JSON-RPC 2.0 Compliance

Extends the existing PiperMCPClient with Model Context Protocol message handling
and service discovery capabilities.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Union

from ..client import PiperMCPClient
from ..exceptions import MCPConnectionError, MCPTimeoutError
from .message_handler import MCPMessageHandler, MCPNotification, MCPRequest, MCPResponse

logger = logging.getLogger(__name__)


class MCPProtocolClient(PiperMCPClient):
    """
    Extended MCP client with protocol compliance

    Builds on existing PiperMCPClient infrastructure while adding
    JSON-RPC 2.0 protocol message handling capabilities.
    """

    def __init__(self, server_config: Dict[str, Any]):
        super().__init__(server_config)
        self.message_handler = MCPMessageHandler()
        # JSON-RPC 2.0 ids are `str | int` (see MCPMessage.__init__), so the
        # pending-request map must be keyed the same way — declaring it `str`
        # made every `request.id` lookup/pop a type error while the runtime
        # behaviour was already correct.
        self._pending_requests: Dict[Union[str, int], asyncio.Future] = {}
        self._server_capabilities: Optional[Dict[str, Any]] = None
        self._initialized = False

    async def initialize_connection(self) -> bool:
        """Initialize MCP connection with protocol handshake"""
        try:
            # First establish basic connection
            if not await self.connect():
                logger.error("Failed to establish basic connection")
                return False

            # Send initialize request
            client_info = {"name": "piper-morgan-mcp-client", "version": "1.0.0"}

            init_request = self.message_handler.create_initialize_request(client_info)
            response = await self._send_request(init_request)

            if response and response.result:
                self._server_capabilities = response.result.get("capabilities", {})
                self._initialized = True
                logger.info("MCP connection initialized successfully")
                return True
            else:
                logger.error("Failed to initialize MCP connection")
                return False

        except Exception as e:
            logger.error(f"Error during MCP initialization: {e}")
            return False

    async def list_resources_protocol(self, uri: Optional[str] = None) -> List[Dict[str, Any]]:
        """List resources using MCP protocol"""
        if not self._initialized:
            raise MCPConnectionError("MCP connection not initialized")

        request = self.message_handler.create_list_resources_request(uri)
        response = await self._send_request(request)

        if response and response.result:
            return response.result.get("resources", [])
        return []

    async def get_resource_protocol(self, uri: str) -> Optional[Dict[str, Any]]:
        """Get resource using MCP protocol"""
        if not self._initialized:
            raise MCPConnectionError("MCP connection not initialized")

        request = self.message_handler.create_get_resource_request(uri)
        response = await self._send_request(request)

        if response and response.result:
            return response.result
        return None

    async def list_tools_protocol(self) -> List[Dict[str, Any]]:
        """List available tools using MCP protocol"""
        if not self._initialized:
            raise MCPConnectionError("MCP connection not initialized")

        request = self.message_handler.create_list_tools_request()
        response = await self._send_request(request)

        if response and response.result:
            return response.result.get("tools", [])
        return []

    async def call_tool_protocol(self, name: str, arguments: Dict[str, Any]) -> Optional[Any]:
        """Call tool using MCP protocol"""
        if not self._initialized:
            raise MCPConnectionError("MCP connection not initialized")

        request = self.message_handler.create_call_tool_request(name, arguments)
        response = await self._send_request(request)

        if response and response.result:
            return response.result
        return None

    async def list_prompts_protocol(self) -> List[Dict[str, Any]]:
        """List available prompts using MCP protocol"""
        if not self._initialized:
            raise MCPConnectionError("MCP connection not initialized")

        request = self.message_handler.create_list_prompts_request()
        response = await self._send_request(request)

        if response and response.result:
            return response.result.get("prompts", [])
        return []

    async def subscribe_resource(self, uri: str) -> bool:
        """Subscribe to resource updates"""
        if not self._initialized:
            raise MCPConnectionError("MCP connection not initialized")

        request = self.message_handler.create_subscribe_request(uri)
        response = await self._send_request(request)

        return response is not None and response.result is not None

    async def unsubscribe_resource(self, uri: str) -> bool:
        """Unsubscribe from resource updates"""
        if not self._initialized:
            raise MCPConnectionError("MCP connection not initialized")

        request = self.message_handler.create_unsubscribe_request(uri)
        response = await self._send_request(request)

        return response is not None and response.result is not None

    async def _send_request(self, request: MCPRequest) -> Optional[MCPResponse]:
        """Send MCP request and wait for response"""
        try:
            # Serialize request
            request_json = self.message_handler.serialize_message(request)

            # Create future for response
            future: asyncio.Future = asyncio.Future()
            self._pending_requests[request.id] = future

            # Send request (implementation depends on transport)
            await self._send_message(request_json)

            # Wait for response with timeout
            try:
                response = await asyncio.wait_for(future, timeout=30.0)
                return response
            except asyncio.TimeoutError:
                logger.error(f"Request {request.id} timed out")
                self._pending_requests.pop(request.id, None)
                raise MCPTimeoutError(f"Request {request.id} timed out")

        except Exception as e:
            logger.error(f"Error sending MCP request: {e}")
            self._pending_requests.pop(request.id, None)
            raise

    async def _send_message(self, message_json: str):
        """Send message to MCP server (transport-specific implementation)"""
        # For now, use simulation mode - extend this for real transport
        if self.simulation_mode:
            logger.debug(f"Simulation mode: would send {message_json}")
            # Simulate response for testing
            await self._simulate_response(message_json)
        else:
            # Real transport implementation would go here
            # This would integrate with the existing connection infrastructure
            logger.debug(f"Real transport: would send {message_json}")
            raise NotImplementedError("Real transport not yet implemented")

    async def _simulate_response(self, message_json: str):
        """Simulate MCP server response for testing"""
        try:
            # Parse the request
            request = self.message_handler.deserialize_message(message_json)

            if isinstance(request, MCPRequest):
                # Simulate appropriate response based on method
                if request.method == "resources/list":
                    response = self.message_handler.create_success_response(
                        request.id, {"resources": self._simulated_resources}
                    )
                elif request.method == "tools/list":
                    response = self.message_handler.create_success_response(
                        request.id,
                        {"tools": [{"name": "list_issues", "description": "List GitHub issues"}]},
                    )
                else:
                    response = self.message_handler.create_success_response(
                        request.id, {"status": "success", "method": request.method}
                    )

                # Schedule response
                await asyncio.sleep(0.1)  # Simulate network delay
                await self._handle_response(response)

        except Exception as e:
            logger.error(f"Error simulating MCP response: {e}")

    async def _handle_response(self, response: MCPResponse):
        """Handle incoming MCP response"""
        try:
            if response.id in self._pending_requests:
                future = self._pending_requests.pop(response.id)
                if not future.done():
                    future.set_result(response)
            else:
                logger.warning(f"Received response for unknown request: {response.id}")

        except Exception as e:
            logger.error(f"Error handling MCP response: {e}")

    async def _handle_notification(self, notification: MCPNotification):
        """Handle incoming MCP notification"""
        try:
            logger.info(f"Received MCP notification: {notification.method}")
            # Handle notifications (e.g., resource updates)
            # This would integrate with the existing event system

        except Exception as e:
            logger.error(f"Error handling MCP notification: {e}")

    def get_server_capabilities(self) -> Optional[Dict[str, Any]]:
        """Get server capabilities from initialization"""
        return self._server_capabilities

    def is_initialized(self) -> bool:
        """Check if MCP connection is initialized"""
        return self._initialized

    async def disconnect_protocol(self):
        """Disconnect MCP protocol connection"""
        try:
            # Cancel pending requests
            for future in self._pending_requests.values():
                if not future.done():
                    future.cancel()
            self._pending_requests.clear()

            # Disconnect base client
            await self.disconnect()

            self._initialized = False
            self._server_capabilities = None

            logger.info("MCP protocol connection disconnected")

        except Exception as e:
            logger.error(f"Error disconnecting MCP protocol: {e}")

    def get_protocol_stats(self) -> Dict[str, Any]:
        """Get protocol-specific statistics"""
        base_stats = self.get_connection_stats()
        protocol_stats = {
            "initialized": self._initialized,
            "pending_requests": len(self._pending_requests),
            "server_capabilities": self._server_capabilities is not None,
            "message_handler": "active",
        }

        return {**base_stats, **protocol_stats}
