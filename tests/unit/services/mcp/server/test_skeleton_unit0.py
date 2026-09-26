"""Phase C unit 0 — MCP server skeleton (#1462).

Pins the five acceptance points from the Lead's build plan
(docs/internal/architecture/current/mcp/phase-c-build-plan-2026-09-25.md,
unit 0) and Arch's slice doc's condition 1 (fail-closed identity, no
anonymous read path):

(a) GET /health -> 200 with status/service/version/git_sha
(b) GET /       -> 200 plain text pointer
(c) POST <mcp path> initialize, no Authorization -> 401 (see note below —
    the exact body/header shape changed under unit 1)
(d) the real initialize handshake's advertised capabilities contain
    `resources` and NOT `tools`/`prompts` — asserted against the actual
    ServerCapabilities object FastMCP's own create_initialization_options()
    produces, not a string in a response body.
(e) register_resources() exists and registers nothing in unit 0.

⚠️ **Amended for unit 1 (#1462, 2026-09-26)**: unit 0 had no identity
resolver, so `MCPPathGate` (née `FailClosedMCPGate`) denied the MCP path
unconditionally with its own fixed `{"error": "identity_required"}` body.
Unit 1 gives the MCP path a real identity check (FastMCP's own
`RequireAuthMiddleware`, wired via `services/mcp/server/identity.py`'s
`MCPTokenVerifier`) — the MCP path itself still refuses an unauthenticated
request with 401, but the body/header shape is now the SDK's own
(`error: invalid_token`), not the gate's. `TestMCPPathFailsClosed` below
asserts on the invariant that still holds (401, `WWW-Authenticate` present,
no 200) rather than the exact unit-0-era body, which no longer applies.
`test_unknown_path_is_refused_not_served` is untouched — genuinely
ungated paths still get the gate's own fixed 401 shape, unchanged.
See `tests/unit/services/mcp/server/test_identity_unit1.py` for unit 1's own
identity-specific tests (401/200/revoked/expired, two-caller isolation).

⚠️ **Amended for unit 2 (#1462, 2026-09-26)**: `register_resources()` is no
longer a no-op — it registers the three named resources (see
`services/mcp/server/resources.py`). `TestRegisterResourcesSeam` below now
pins "the seam actually registers unit 2's three resources" rather than
"registers nothing yet"; the full per-resource behavior (owner-scoping,
honest-empty payloads, the GitHub connect-required shape) is
`tests/unit/services/mcp/server/test_resources_unit2.py`'s scope, not
re-proven here.

LAYER (m-43): a real ASGI app via httpx.ASGITransport / Starlette TestClient
— the same protocol surface uvicorn serves, not a call into a handler
function in isolation. Test (d) additionally calls the SDK's own
capability-computation entrypoint directly, so it can't be fooled by a
response-body string that merely looks right.
DENOMINATOR: unit 0's skeleton only — no resources exist yet (unit 2), so
that's out of scope here by design, not by omission. Real identity
resolution now exists (unit 1) and is exercised here only at the
"no bearer at all" boundary; the fuller identity matrix lives in
test_identity_unit1.py.
"""

from __future__ import annotations

import mcp.types as mcp_types
from fastapi.testclient import TestClient

from services.mcp.server.app import build_asgi_app, build_mcp_server

MCP_PATH = "/mcp"


class TestHealthAndRootStayOpen:
    def test_health_reports_the_four_fields(self) -> None:
        app = build_asgi_app()
        with TestClient(app) as client:
            resp = client.get("/health")

        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "healthy"
        assert body["service"] == "piper-morgan-mcp"
        assert "version" in body
        assert "git_sha" in body

    def test_root_is_a_plain_text_pointer(self) -> None:
        app = build_asgi_app()
        with TestClient(app) as client:
            resp = client.get("/")

        assert resp.status_code == 200
        assert "MCP" in resp.text

    def test_health_works_without_a_lifespan_error(self) -> None:
        """The streamable-HTTP session manager's lifespan
        (``session_manager.run()``) must start cleanly even though unit 0
        registers no resources — TestClient's context-manager entry runs the
        full ASGI lifespan cycle, so a broken session-manager startup would
        raise here, not silently no-op."""
        app = build_asgi_app()
        with TestClient(app) as client:
            resp = client.get("/health")
        assert resp.status_code == 200


class TestMCPPathFailsClosed:
    """Unit 1 note: without a bearer, the MCP path is still refused — but the
    refusal now comes from FastMCP's own RequireAuthMiddleware (wired via
    the real MCPTokenVerifier), not MCPPathGate's fixed unit-0 body. Assert
    the invariant (401, a WWW-Authenticate challenge, never a 200), not the
    exact unit-0-era shape. See test_identity_unit1.py for the full
    401/200/revoked/expired matrix."""

    def test_initialize_without_bearer_is_refused(self) -> None:
        app = build_asgi_app()
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "0.0.1"},
            },
        }
        with TestClient(app) as client:
            resp = client.post(
                MCP_PATH,
                json=payload,
                headers={"Accept": "application/json, text/event-stream"},
            )

        assert resp.status_code == 401
        assert "bearer" in resp.headers.get("www-authenticate", "").lower()

    def test_get_on_mcp_path_is_also_refused(self) -> None:
        """The gate lets the MCP path through to the inner app regardless of
        method; the inner app's own RequireAuthMiddleware refuses it just
        the same — there is no anonymous read path through the MCP endpoint
        at all."""
        app = build_asgi_app()
        with TestClient(app) as client:
            resp = client.get(MCP_PATH)

        assert resp.status_code == 401
        assert "bearer" in resp.headers.get("www-authenticate", "").lower()


class TestCapabilitiesAreResourcesOnly:
    def test_advertised_capabilities_have_resources_not_tools_or_prompts(self) -> None:
        server = build_mcp_server()
        init_options = server._mcp_server.create_initialization_options()
        caps = init_options.capabilities

        assert caps.resources is not None
        assert caps.tools is None
        assert caps.prompts is None

    def test_no_tool_or_prompt_request_handlers_are_registered(self) -> None:
        """Direct check on the handler table `get_capabilities()` itself
        reads — belt and suspenders against the capability object being
        right for the wrong reason."""
        server = build_mcp_server()
        handlers = server._mcp_server.request_handlers

        assert mcp_types.ListResourcesRequest in handlers
        assert mcp_types.ListToolsRequest not in handlers
        assert mcp_types.CallToolRequest not in handlers
        assert mcp_types.ListPromptsRequest not in handlers
        assert mcp_types.GetPromptRequest not in handlers


class TestRegisterResourcesSeam:
    async def test_register_resources_registers_unit_twos_three_resources(self) -> None:
        """Unit 0's version of this test pinned "registers nothing yet"; unit 2 landed
        the three named resources through this exact seam (see amendment note above).
        `build_mcp_server()` calls `register_resources()` internally, so building a
        server and listing its resources is the observable proof the seam fired."""
        server = build_mcp_server()

        resources = await server.list_resources()

        assert len(resources) == 3


def test_unknown_path_is_refused_not_served():
    # Deny-by-default (Lead review): a path nobody gated is still 401, never a
    # 404 from the inner app (which would prove the request reached it).
    from starlette.testclient import TestClient

    from services.mcp.server.app import build_asgi_app

    with TestClient(build_asgi_app()) as client:
        r = client.get("/mcp/anything")
        assert r.status_code == 401
        assert r.headers.get("www-authenticate") == "Bearer"
        r2 = client.post("/not-a-route")
        assert r2.status_code == 401
