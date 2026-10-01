"""Piper Morgan MCP server — skeleton + identity (Phase C units 0-1, #1462).

Companion docs: ``docs/internal/architecture/current/mcp/phase-c-build-plan-2026-09-25.md``
(Lead, the *how*) and ``phase-c-minimal-alpha-slice-2026-09-25.md`` (Arch, the
*what*), same directory. Arch's slice: resources only, ZERO tools, fail-closed
identity for a single named alpha tester. Unit 0 shipped deployable-dark: no
resources registered (that's unit 2, see :func:`register_resources`) and
every MCP request refused unconditionally (no identity resolver existed at
all). Unit 1 (this revision) adds the real identity resolver
(``services/mcp/server/identity.py:MCPTokenVerifier``) — the MCP path now
passes through to the SDK's own bearer-auth machinery instead of being denied
outright, and identity is fail-closed the same way unit 0's blanket denial
was: no branch anywhere resolves a missing/invalid/expired token to a real
user.

Three structural decisions worth reading before touching this file:

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

2. **Identity via FastMCP's own auth hook (unit 1).** ``build_mcp_server()``
   now passes ``auth=AuthSettings(...)`` and
   ``token_verifier=MCPTokenVerifier()`` to ``FastMCP(...)``. FastMCP wires
   this into ``streamable_http_app()`` as ``RequireAuthMiddleware`` around the
   MCP route itself, plus a global ``BearerAuthBackend`` +
   ``AuthContextMiddleware`` pair that stores the resolved identity in a
   request-scoped contextvar (``mcp.server.auth.middleware.auth_context``) —
   see ``services/mcp/server/identity.py:current_user_id()`` for how unit 2's
   resources read it back out. No ``auth_server_provider`` is configured
   (deliberately — see :func:`_auth_settings`'s docstring): as of unit 4 the
   OAuth authorization server is a SEPARATE HOST, the alpha web app
   (``web/routers/mcp_oauth.py``), because that is where the user's login
   session lives. This app therefore exposes no ``/authorize``/``/token``
   routes and issues nothing. Tokens reach it two ways, both landing in the
   same ``mcp_access_tokens`` table and both verified by the same verifier:
   operator-minted out-of-band (``scripts/mint_mcp_token.py``, like an invite
   token) or OAuth-minted by alpha's AS
   (``services/mcp/server/oauth_provider.py``).

3. **:class:`MCPPathGate` narrows in unit 1, it doesn't disappear.** Unit 0's
   ``FailClosedMCPGate`` denied the MCP path unconditionally, because no
   identity resolver existed to check anything against. Now that the SDK's
   own ``RequireAuthMiddleware`` sits inside the wrapped app and enforces
   identity on the MCP path itself, this gate's remaining job is exactly what
   its unit-0 review comment already named: deny-by-default for paths nobody
   has gated at all (a typo'd path, a future route someone forgets to
   protect) — never allow-by-default. The MCP path is let through to the
   inner app precisely because that inner app still fails closed on it; that
   is not the same thing as serving it anonymously.
"""

from __future__ import annotations

import os

import mcp.types as mcp_types
import structlog
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

from services.api.health.deploy_identity import deploy_identity
from services.mcp.server.identity import RESOURCE_READ_SCOPE, MCPTokenVerifier

logger = structlog.get_logger(__name__)

SERVICE_NAME = "piper-morgan-mcp"

# RFC 9728 protected-resource discovery. As of unit 4 the issuer is a REAL,
# separate authorization server — it runs in the alpha web app, because that is the
# host holding the user's login session (see web/routers/mcp_oauth.py). This app
# stays a pure resource server: it verifies tokens, it never issues them.
# The path component is deliberate and RFC 8414 permits it; keep this string and
# web/routers/mcp_oauth.py's AS_PREFIX in lockstep.
DEFAULT_ISSUER_URL = "https://alpha.pipermorgan.ai/mcp/oauth"
DEFAULT_RESOURCE_SERVER_URL = "https://mcp.pipermorgan.ai"

# DNS-rebinding protection (Host/Origin allowlist). FastMCP's default
# host="127.0.0.1" silently auto-enables this with a LOCALHOST-ONLY allowlist,
# so every request addressed to the real hostname was refused with 421
# "Invalid Host header: mcp.pipermorgan.ai" -- after auth had already passed.
# Found at PM's first live ChatGPT connection, 2026-10-01 ("Authentication
# succeeded, action discovery failed"). Protection stays ON; the allowlist
# just has to name the production host. Override with MCP_ALLOWED_HOSTS
# (comma-separated) for any other deployment hostname.
DEFAULT_ALLOWED_HOSTS = "mcp.pipermorgan.ai"
_LOCAL_HOSTS = ["127.0.0.1:*", "localhost:*", "[::1]:*"]
_LOCAL_ORIGINS = ["http://127.0.0.1:*", "http://localhost:*", "http://[::1]:*"]
# Origin is only checked when the header is present (server-to-server MCP
# calls usually omit it); these are the chat hosts PDR-006 targets.
_CLIENT_ORIGINS = ["https://chatgpt.com", "https://chat.openai.com", "https://claude.ai"]


def _transport_security() -> TransportSecuritySettings:
    hosts = [
        h.strip()
        for h in os.environ.get("MCP_ALLOWED_HOSTS", DEFAULT_ALLOWED_HOSTS).split(",")
        if h.strip()
    ]
    return TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=hosts + [f"{h}:*" for h in hosts] + _LOCAL_HOSTS,
        allowed_origins=[f"https://{h}" for h in hosts] + _CLIENT_ORIGINS + _LOCAL_ORIGINS,
    )


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
    """Seam for unit 2 (now implemented) — delegates to
    :mod:`services.mcp.server.resources`.

    Unit 2 (per the Lead's build plan) adds three named resources:
    ``piper://me/profile``, ``piper://me/colleague-model`` (referent per
    CXO's Q2 ruling: the #1510 verified-inference store, never #1735), and
    ``piper://me/github/issues``. The resource functions and their
    ``@app.resource(...)`` registrations live in ``services/mcp/server/
    resources.py`` (independently testable without this module's ASGI-wiring
    concerns) — this function keeps the same name/location the server-README
    documents as the seam, so :func:`build_mcp_server` doesn't need to
    restructure.
    """
    from services.mcp.server.resources import register_resources as _register_resources

    _register_resources(app)


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


def _auth_settings() -> AuthSettings:
    """OAuth settings for the MCP server as a **resource server**.

    This app configures no ``auth_server_provider``, so FastMCP never registers
    ``/authorize`` or ``/token`` here (see :func:`build_mcp_server`) — and as of
    unit 4 it should not, because the authorization server is a separate host:
    the alpha web app (``web/routers/mcp_oauth.py``), which is the only host
    holding the user's login session. RFC 9728 exists precisely to let a
    resource server name a different issuer, and that is what these two fields
    do.

    ``issuer_url`` (default ``https://alpha.pipermorgan.ai/mcp/oauth``) and
    ``resource_server_url`` (default ``https://mcp.pipermorgan.ai``) back the
    protected-resource-metadata endpoint FastMCP exposes
    (``/.well-known/oauth-protected-resource`` — kept reachable by
    :class:`MCPPathGate`'s ``OPEN_PATHS``, see the note there) and the
    ``resource_metadata`` hint in a 401's ``WWW-Authenticate`` header. A client
    that only knows the MCP URL follows that chain to alpha, authorizes there,
    and comes back with a token this app's unchanged
    :class:`~services.mcp.server.identity.MCPTokenVerifier` already accepts —
    the OAuth path mints ``mcp_access_tokens`` rows, the same table
    ``scripts/mint_mcp_token.py`` writes. Operator-minted bearer tokens remain
    valid alongside OAuth: one verifier, one boundary, two ways in.

    Both are overridable via env (``MCP_OAUTH_ISSUER_URL`` /
    ``MCP_RESOURCE_SERVER_URL``) so a local/staging run doesn't have to lie
    about serving from the production domains.
    """
    return AuthSettings(
        issuer_url=os.environ.get("MCP_OAUTH_ISSUER_URL", DEFAULT_ISSUER_URL),
        resource_server_url=os.environ.get("MCP_RESOURCE_SERVER_URL", DEFAULT_RESOURCE_SERVER_URL),
        required_scopes=[RESOURCE_READ_SCOPE],
    )


class MCPPathGate:
    """Deny-by-default at the raw ASGI layer for any path nobody has
    explicitly gated — the MCP path itself is no longer denied here in
    unit 1 (see class docstring point 3 at module top for why that's still
    fail-closed, not a relaxation).

    ``OPEN_PATHS`` bypass everything (health checks, the root pointer). The
    MCP path is let through to the wrapped app, which is the *complete*,
    unmodified Starlette app FastMCP's own ``streamable_http_app()``
    returns — including its ``RequireAuthMiddleware`` wrapping the MCP
    route (unit 1's real identity check) and its
    ``lifespan=lambda app: self.session_manager.run()`` wiring. Wrapping the
    finished app at the raw ASGI layer, rather than mounting it inside
    another Starlette app, is deliberate: mounted sub-apps do not reliably
    receive lifespan events in Starlette, which is exactly the trap that
    would silently break the streamable-HTTP session manager's startup.
    Any OTHER path — a typo, a future route someone forgets to register
    correctly — gets the unconditional 401 this class shipped unit 0 with.
    This wrapper only inspects ``scope["type"] == "http"`` requests and
    passes every other scope type (notably ``"lifespan"``) straight
    through untouched, so the inner app's lifespan fires normally.
    """

    # Lead review (2026-09-26, carried from unit 0): DENY BY DEFAULT. Only
    # the deliberately public routes and the MCP path (which enforces its
    # own identity check downstream) pass through; anything else is refused.
    #
    # ``/.well-known/oauth-protected-resource`` added in unit 4 (#1462), and it
    # was a real gate bug, not a nicety: FastMCP registers that route itself
    # whenever ``resource_server_url`` is set, the 401 this class emits on the MCP
    # path POINTS AT IT via ``WWW-Authenticate: resource_metadata=…``, and this
    # gate was answering it with a 401 — so RFC 9728 discovery could not complete
    # and an OAuth client had no way to find the authorization server. The
    # document is public BY DESIGN (it names the issuer and the supported scopes;
    # it contains no user data and no credential), which is why opening it is
    # correct rather than a relaxation.
    OPEN_PATHS: frozenset[str] = frozenset(
        {"", "/", "/health", "/.well-known/oauth-protected-resource"}
    )

    def __init__(self, app: ASGIApp, mcp_path: str) -> None:
        self._app = app
        self._mcp_path = mcp_path.rstrip("/") or "/"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        path = scope["path"].rstrip("/") or "/"
        if path in self.OPEN_PATHS or path == self._mcp_path:
            await self._app(scope, receive, send)
            return

        response = JSONResponse(
            {"error": "identity_required"},
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
        )
        await response(scope, receive, send)


def build_mcp_server() -> FastMCP:
    """Build the FastMCP instance: resources-only capability set, real
    bearer-token identity (unit 1).

    Separated from :func:`build_asgi_app` so tests can inspect the FastMCP
    instance's real advertised capabilities (via
    ``server._mcp_server.create_initialization_options()``, the same call the
    real ``initialize`` handshake makes) without standing up an HTTP client.
    """
    mcp = FastMCP(
        name="piper-morgan",
        auth=_auth_settings(),
        token_verifier=MCPTokenVerifier(),
        transport_security=_transport_security(),
    )
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
    """The full ASGI app: MCP streamable-HTTP (bearer-identity-gated) +
    plain ``/health`` + ``/``, deny-by-default for everything else.

    ``/health`` and ``/`` are registered as FastMCP ``custom_route``s (the
    SDK's documented escape hatch for non-protocol HTTP endpoints — "will not
    require authorization", per its own docstring), so they live inside the
    same Starlette app ``streamable_http_app()`` returns and share its
    lifespan, untouched by ``RequireAuthMiddleware`` (that middleware only
    wraps the MCP route itself). :class:`MCPPathGate` then wraps that whole
    app and denies anything that isn't one of those two paths or the MCP
    path.
    """
    mcp = build_mcp_server()
    inner_app = mcp.streamable_http_app()
    return MCPPathGate(inner_app, mcp_path=mcp.settings.streamable_http_path)


# Local dev / ad-hoc introspection only — the real process entrypoint is
# main_mcp.py at the repo root (uvicorn.run, PORT/HOST from env, structlog).
if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(build_asgi_app(), host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
