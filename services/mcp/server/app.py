"""Piper Morgan MCP server — skeleton (Phase C unit 0, #1462).

Companion docs: ``docs/internal/architecture/current/mcp/phase-c-build-plan-2026-09-25.md``
(Lead, the *how*) and ``phase-c-minimal-alpha-slice-2026-09-25.md`` (Arch, the
*what*), same directory. Arch's slice: resources only, ZERO tools, fail-closed
identity for a single named alpha tester. This module builds unit 0 only —
deployable dark, nothing user-facing: no resources are registered yet (that's
unit 2, see :func:`register_resources`) and no caller can reach the MCP
protocol at all yet (that's unit 1's identity resolver; until it lands, every
MCP request is refused unconditionally — see :class:`FailClosedMCPGate`).

Two structural decisions worth reading before touching this file:

1. **Capability trimming.** FastMCP's constructor unconditionally wires
   ``list_tools``/``call_tool``/``list_prompts``/``get_prompt`` handlers onto
   its low-level ``Server`` (see ``_setup_handlers`` in
   ``mcp/server/fastmcp/server.py``), regardless of whether any tool or prompt
   is ever added — so an unmodified ``FastMCP`` instance always advertises
   ``tools`` and ``prompts`` capabilities in the ``initialize`` handshake, even
   with zero of each registered. That fails Arch's "resources only" condition
   outright, not cosmetically: a client would see ``tools`` advertised and
   could legitimately attempt ``tools/list``. There is no public FastMCP knob
   to suppress a capability, so :func:`_restrict_to_resources_only` reaches
   into the low-level server's handler table directly and removes the
   tool/prompt request handlers immediately after construction. See its
   docstring for what unit 2 must (and must not) do around this.

2. **Fail-closed wrapping, not FastMCP's auth hook.** FastMCP has a built-in
   auth mechanism (``settings.auth`` + a ``TokenVerifier``), but that
   mechanism exists to *verify* a real bearer token against a real identity
   store — and unit 1 (the identity resolver) doesn't exist yet. Wiring a
   ``TokenVerifier`` that always rejects would mean inventing throwaway
   plumbing unit 1 immediately deletes. Instead, :class:`FailClosedMCPGate` is
   a thin ASGI wrapper placed *around* the fully-built MCP ASGI app: it
   intercepts every request to the MCP path and refuses it, before the
   request ever reaches FastMCP's session/auth machinery, and lets every other
   request (``/health``, ``/``) through untouched. Unit 1 replaces this one
   class; nothing else in this file needs to change shape.
"""

from __future__ import annotations

import os

import mcp.types as mcp_types
import structlog
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

from services.api.health.deploy_identity import deploy_identity

logger = structlog.get_logger(__name__)

SERVICE_NAME = "piper-morgan-mcp"


def _restrict_to_resources_only(mcp: FastMCP) -> None:
    """Strip the tool/prompt protocol handlers FastMCP registers unconditionally.

    ``get_capabilities()`` (``mcp/server/lowlevel/server.py``) derives the
    advertised capability set purely from which request types have a
    registered handler in ``Server.request_handlers``. FastMCP's own
    ``_setup_handlers`` always populates ``ListToolsRequest``/
    ``CallToolRequest``/``ListPromptsRequest``/``GetPromptRequest`` at
    construction time, whether or not anything is ever registered under them.
    Popping those four handler entries here is the only way (short of not
    using FastMCP at all) to make the real ``initialize`` handshake advertise
    resources without also advertising empty-but-present tools/prompts.

    Unit 2: call :func:`register_resources` BEFORE this (order doesn't
    actually matter for resources — ``ListResourcesRequest`` is untouched
    either way — but keep the call order in :func:`build_mcp_server` as the
    canonical shape) and do not re-add a tool or prompt handler without
    reopening Arch's "zero tools" condition explicitly.
    """
    handlers = mcp._mcp_server.request_handlers
    for request_type in (
        mcp_types.ListToolsRequest,
        mcp_types.CallToolRequest,
        mcp_types.ListPromptsRequest,
        mcp_types.GetPromptRequest,
    ):
        handlers.pop(request_type, None)


def register_resources(app: FastMCP) -> None:
    """Seam for unit 2 — no-op in unit 0.

    Unit 2 (per the Lead's build plan) adds three named resources here via
    ``@app.resource(...)``: ``piper://me/profile``, ``piper://me/colleague-model``
    (referent pending CXO/PPM), and ``piper://me/github/issues``. This
    function exists now, doing nothing, so unit 2 has a fixed place to land
    without restructuring :func:`build_mcp_server` or :func:`build_asgi_app`.
    """
    return None


def _health_response() -> JSONResponse:
    """Mirror alpha's ``/health`` deploy-identity fields via the shared helper.

    Reuses ``services.api.health.deploy_identity.deploy_identity()`` — the
    same helper the alpha app's ``/health`` and ``/api/v1/version`` routes
    both call (``web/api/routes/admin.py``) — rather than re-parsing
    ``pyproject.toml``/``VERSION`` a second time. ``deploy_identity()``'s
    ``version`` is read from the shipped ``VERSION`` file (falling back to
    ``PIPER_VERSION`` env, then the literal ``"unknown"``), which is kept in
    lockstep with ``pyproject.toml``'s ``version`` field — not a second,
    independently-drifting version source. ``git_sha`` is
    ``PIPER_GIT_SHA`` (the Dockerfile build arg) or ``"unknown"``, exactly as
    specified.
    """
    identity = deploy_identity()
    return JSONResponse(
        {
            "status": "healthy",
            "service": SERVICE_NAME,
            "version": identity["version"],
            "git_sha": identity["git_sha"],
        }
    )


class FailClosedMCPGate:
    """Unconditionally reject MCP protocol traffic until unit 1 ships identity.

    Unit 0 has no identity resolver, so there is no code path — a bearer
    present, absent, or well-formed — that this gate can distinguish as safe
    to serve anonymously. Every request whose path matches the MCP endpoint
    gets a 401 with ``WWW-Authenticate: Bearer`` and
    ``{"error": "identity_required"}``, before it ever reaches
    ``session_manager`` or any FastMCP handler. Requests to any other path
    (``/health``, ``/``) pass straight through to the wrapped app, which is
    the *complete*, unmodified Starlette app FastMCP's own
    ``streamable_http_app()`` returns — including its
    ``lifespan=lambda app: self.session_manager.run()`` wiring. Wrapping the
    finished app at the raw ASGI layer, rather than mounting it inside another
    Starlette app, is deliberate: mounted sub-apps do not reliably receive
    lifespan events in Starlette, which is exactly the trap that would silently
    break the streamable-HTTP session manager's startup. This wrapper only
    inspects ``scope["type"] == "http"`` requests and passes every other scope
    type (notably ``"lifespan"``) straight through untouched, so the inner
    app's lifespan fires normally.
    """

    # Lead review (2026-09-26): DENY BY DEFAULT. The first cut matched the MCP
    # path exactly and let every other path through — allow-by-default, the
    # inverse of fail-closed. Only the two deliberately public routes are
    # open; anything else (the MCP endpoint, a typo'd path, a future route
    # someone forgets to gate) is refused until identity exists.
    OPEN_PATHS: frozenset[str] = frozenset({"", "/", "/health"})

    def __init__(self, app: ASGIApp, mcp_path: str) -> None:
        self._app = app
        self._mcp_path = mcp_path.rstrip("/") or "/"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http" and scope["path"].rstrip("/") not in self.OPEN_PATHS:
            response = JSONResponse(
                {"error": "identity_required"},
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"},
            )
            await response(scope, receive, send)
            return
        await self._app(scope, receive, send)


def build_mcp_server() -> FastMCP:
    """Build the FastMCP instance: resources-only capability set, unit-0 seam.

    Separated from :func:`build_asgi_app` so tests can inspect the FastMCP
    instance's real advertised capabilities (via
    ``server._mcp_server.create_initialization_options()``, the same call the
    real ``initialize`` handshake makes) without standing up an HTTP client.
    """
    mcp = FastMCP(name="piper-morgan")
    register_resources(mcp)
    _restrict_to_resources_only(mcp)

    @mcp.custom_route("/health", methods=["GET"])
    async def health(_request: Request) -> Response:
        return _health_response()

    @mcp.custom_route("/", methods=["GET"])
    async def root(_request: Request) -> Response:
        return PlainTextResponse(
            "Piper Morgan MCP endpoint — connect with an MCP client; see docs."
        )

    return mcp


def build_asgi_app() -> ASGIApp:
    """The full ASGI app: MCP streamable-HTTP + plain ``/health`` + ``/``, fail-closed.

    ``/health`` and ``/`` are registered as FastMCP ``custom_route``s (the
    SDK's documented escape hatch for non-protocol HTTP endpoints — "will not
    require authorization", per its own docstring), so they live inside the
    same Starlette app ``streamable_http_app()`` returns and share its
    lifespan. :class:`FailClosedMCPGate` then wraps that whole app and gates
    only the MCP path itself.
    """
    mcp = build_mcp_server()
    inner_app = mcp.streamable_http_app()
    return FailClosedMCPGate(inner_app, mcp_path=mcp.settings.streamable_http_path)


# Local dev / ad-hoc introspection only — the real process entrypoint is
# main_mcp.py at the repo root (uvicorn.run, PORT/HOST from env, structlog).
if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(build_asgi_app(), host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
