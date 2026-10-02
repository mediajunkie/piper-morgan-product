"""MCP OAuth 2.1 authorization server — the HTTP surface, mounted in the ALPHA app
(Phase C unit 4, #1462).

Companion docs: ``docs/internal/architecture/current/mcp/server-README.md`` (the
two-host topology), ``phase-c-build-plan-2026-09-25.md`` (unit 4), and
``web-routes-conventions.md`` (these paths are a documented ``/api/v1/``
exception — they are RFC-fixed).

═══ WHY THE AS LIVES IN ALPHA AND NOT IN THE MCP SERVER ═══

The authorization server must authenticate the *end user*, and the only host that
holds a Piper Morgan login session is the alpha web app (``web/app.py``, cookie +
JWT via ``services/auth/auth_middleware.py``). The MCP server
(``mcp.pipermorgan.ai``) has no session, no login page, and no business growing
one. RFC 9728 lets a resource server name a *separate* issuer, so:

    ChatGPT ──1── GET https://mcp.pipermorgan.ai/mcp            (401 + RS metadata hint)
            ──2── GET https://mcp.pipermorgan.ai/.well-known/oauth-protected-resource
                     -> {"authorization_servers": ["https://alpha.pipermorgan.ai/mcp/oauth"]}
            ──3── GET https://alpha.pipermorgan.ai/.well-known/oauth-authorization-server/mcp/oauth
                     -> {"authorization_endpoint": ".../mcp/oauth/authorize", "token_endpoint": ...}
            ──4── POST .../mcp/oauth/register        (RFC 7591 dynamic registration)
            ──5── browser -> .../mcp/oauth/authorize (alpha session REQUIRED; consent page)
            ──6── POST .../mcp/oauth/token           (PKCE S256; code -> access token)
            ──7── GET https://mcp.pipermorgan.ai/mcp with that Bearer -> resources

The tester configures ONE thing in ChatGPT: the MCP URL. Steps 2-6 are discovery.

═══ THE IDENTITY BINDING (Arch's unit-4 review condition) ═══

``/mcp/oauth/authorize`` is NOT the SDK's handler mounted raw. It is this module's
wrapper, and the order is load-bearing:

1. **Alpha's own ``AuthMiddleware`` gates the path.** These paths are deliberately
   NOT in that middleware's exempt list (unlike ``/token`` and ``/register``, which
   are machine-to-machine and must be), so an unauthenticated browser GET is
   turned into ``302 /login?next=<this url>`` by the existing mechanism — no second
   auth path, no new cookie reader, nothing to keep in sync.
2. **The route re-checks anyway** (:func:`_session_user_id`) and issues the same
   login redirect itself, so the "no identity, no code" property does not depend on
   middleware registration order.
3. **GET renders a consent page**; nothing is written. **Only POST-with-Approve**
   binds the session user into :func:`~services.mcp.server.oauth_provider.consenting_user`
   and delegates to the SDK's ``AuthorizationHandler``, which validates the request
   and calls ``provider.authorize`` — which refuses outright if that binding is
   absent.
4. **The consent POST carries an HMAC consent token** bound to (user_id, client_id,
   code_challenge). A cross-site forged approve POST therefore cannot mint a code
   for a victim's session: the attacker cannot produce a token for the victim's
   user id. This is the classic consent-CSRF hole, closed rather than noted.

Deny → redirect to the client's *registered* redirect_uri with
``error=access_denied`` (validated first, so this is not an open redirect).
"""

from __future__ import annotations

import hashlib
import hmac
import html
import os
import time
import uuid
from urllib.parse import quote

import structlog
from fastapi import FastAPI
from mcp.server.auth.handlers.authorize import AuthorizationHandler
from mcp.server.auth.provider import construct_redirect_uri
from mcp.server.auth.routes import create_auth_routes
from mcp.server.auth.settings import ClientRegistrationOptions, RevocationOptions
from mcp.shared.auth import InvalidRedirectUriError
from pydantic import AnyHttpUrl, AnyUrl
from sqlalchemy import select
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from starlette.routing import Route

from services.mcp.server.identity import RESOURCE_READ_SCOPE
from services.mcp.server.oauth_provider import PiperMCPOAuthProvider, consenting_user
from services.mcp.server.resources import (
    COLLEAGUE_MODEL_URI,
    GITHUB_ISSUES_URI,
    PROFILE_URI,
)

logger = structlog.get_logger(__name__)

# ── Paths ────────────────────────────────────────────────────────────────────
# The prefix is FIXED, not configurable: it is baked into the issuer identifier
# that the resource server advertises and that clients validate (RFC 8414 §3.3),
# so making it an env knob would let the two hosts disagree silently.
AS_PREFIX = "/mcp/oauth"
AUTHORIZE_PATH = f"{AS_PREFIX}/authorize"
TOKEN_PATH = f"{AS_PREFIX}/token"
REGISTER_PATH = f"{AS_PREFIX}/register"
REVOKE_PATH = f"{AS_PREFIX}/revoke"

# RFC 8414 §3.1: for an issuer WITH a path component, the well-known URI inserts
# the well-known segment between host and path. That is the canonical location and
# the one the MCP spec's discovery sequence uses.
METADATA_PATH_RFC8414 = f"/.well-known/oauth-authorization-server{AS_PREFIX}"
# Also served at the path-appended location, because several clients (and the SDK's
# own route table, mounted under a prefix) look there first. Same metadata object,
# same `issuer` value, so a client that validates the issuer is satisfied either way.
METADATA_PATH_SUFFIXED = f"{AS_PREFIX}/.well-known/oauth-authorization-server"

DEFAULT_ISSUER_URL = "https://alpha.pipermorgan.ai" + AS_PREFIX

# Every path this module mounts — the single source the auth-middleware exempt
# list and the route-conventions doc are checked against.
ALL_AS_PATHS = (
    AUTHORIZE_PATH,
    TOKEN_PATH,
    REGISTER_PATH,
    REVOKE_PATH,
    METADATA_PATH_RFC8414,
    METADATA_PATH_SUFFIXED,
)
# The subset that is machine-to-machine (no browser, no session) and therefore MUST
# be exempt from alpha's AuthMiddleware. `/authorize` is deliberately absent.
MACHINE_TO_MACHINE_PATHS = (
    TOKEN_PATH,
    REGISTER_PATH,
    REVOKE_PATH,
    METADATA_PATH_RFC8414,
    METADATA_PATH_SUFFIXED,
)

CONSENT_TTL_SECONDS = 600


def issuer_url() -> str:
    """The AS's issuer identifier. Env-overridable so a local/staging run doesn't
    have to claim it is serving from the production domain."""
    return os.environ.get("MCP_OAUTH_ISSUER_URL", DEFAULT_ISSUER_URL)


# ── Consent token (CSRF binding) ─────────────────────────────────────────────


def _consent_secret() -> bytes:
    """HMAC key for the consent token.

    Reuses the app's JWT signing secret rather than introducing a second secret to
    provision (one fewer thing that can be missing in production; that secret's own
    resolver already refuses to fall back in prod — see
    ``services/auth/jwt_service.py:_get_secret_key``). ``MCP_OAUTH_CONSENT_SECRET``
    overrides it if an operator wants them separated. Domain-separated by the
    literal below so a consent token can never be confused with anything else
    signed by the same key.
    """
    explicit = os.environ.get("MCP_OAUTH_CONSENT_SECRET")
    if explicit:
        return b"piper-mcp-oauth-consent-v1:" + explicit.encode("utf-8")
    from services.auth.container import AuthContainer

    return b"piper-mcp-oauth-consent-v1:" + AuthContainer.get_jwt_service().secret_key.encode(
        "utf-8"
    )


def _sign_consent(user_id: str, client_id: str, code_challenge: str, expires_at: int) -> str:
    payload = f"{user_id}|{client_id}|{code_challenge}|{expires_at}".encode("utf-8")
    digest = hmac.new(_consent_secret(), payload, hashlib.sha256).hexdigest()
    return f"{expires_at}.{digest}"


def _consent_token_is_valid(
    token: str, *, user_id: str, client_id: str, code_challenge: str
) -> bool:
    """True only for a token this server issued, to THIS user, for THIS client and
    code_challenge, still inside its TTL."""
    if not token or "." not in token:
        return False
    raw_expiry, _, _digest = token.partition(".")
    try:
        expires_at = int(raw_expiry)
    except ValueError:
        return False
    if expires_at < int(time.time()):
        return False
    expected = _sign_consent(user_id, client_id, code_challenge, expires_at)
    return hmac.compare_digest(token, expected)


# ── Identity lookup (CXO design spec #1911 §1a) ──────────────────────────────


async def _lookup_user_identity(user_id: str) -> tuple[str, str] | None:
    """``(username, email)`` for the consent page's identity line, or ``None``.

    ``None`` on ANY failure (bad UUID, DB unreachable, missing row) rather than
    raising — ``user_id`` already came from a validated session, so a lookup
    failure here is a should-never-happen path, not a designed state, and the
    caller falls back to the raw UUID rather than rendering a broken page.
    """
    from services.database.models import User
    from services.database.session_factory import AsyncSessionFactory

    try:
        parsed = uuid.UUID(str(user_id))
    except ValueError:
        return None
    try:
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(select(User).where(User.id == parsed))
            user = result.scalar_one_or_none()
    except Exception:
        logger.warning("mcp_oauth_consent_identity_lookup_failed", exc_info=True)
        return None
    if user is None:
        return None
    return user.username, user.email


# ── Session resolution ───────────────────────────────────────────────────────


def _session_user_id(request: Request) -> str | None:
    """The authenticated alpha user for this request, or ``None``.

    Reads exactly what ``services/auth/auth_middleware.py:AuthMiddleware`` sets
    (``request.state.user_id``, from validated JWT claims — the same value
    ``get_current_user`` resolves). ``getattr`` with a ``None`` default because
    ``request.state`` raises ``AttributeError`` for an unset attribute, and an
    unset attribute means "no session", which must be a refusal and never a crash.
    """
    user_id = getattr(request.state, "user_id", None)
    return str(user_id) if user_id else None


def _login_redirect(request: Request) -> RedirectResponse:
    """Bounce an unauthenticated browser to alpha's login, preserving the whole
    authorize URL in ``next`` — the same percent-encoded single-param shape
    ``AuthMiddleware._unauthorized_response`` uses (#1480), so the round trip lands
    back on this exact request with its PKCE parameters intact."""
    target = request.url.path
    if request.url.query:
        target += f"?{request.url.query}"
    return RedirectResponse(url=f"/login?next={quote(target, safe='')}", status_code=302)


# ── The consent page ─────────────────────────────────────────────────────────

_CONSENT_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Authorize {client_label} — Piper Morgan</title>
<link rel="stylesheet" href="/static/css/tokens.css">
<style>
  body {{ font: 16px/1.5 var(--font-family);
         margin: 0; padding: 2rem 1rem; display: flex; justify-content: center; }}
  main {{ max-width: 34rem; width: 100%; }}
  .brand {{ font-weight: var(--font-weight-semibold); color: var(--color-primary);
           font-size: var(--font-size-lg); margin-bottom: var(--space-md); }}
  h1 {{ font-size: 1.35rem; margin: 0 0 1rem; }}
  ul {{ padding-left: 1.25rem; }}
  code {{ font-size: 0.9em; }}
  .actions {{ display: flex; gap: 0.75rem; margin-top: 1.5rem; }}
  button {{ font: inherit; padding: 0.6rem 1.2rem; border-radius: var(--border-radius-md); cursor: pointer; }}
  .approve {{ border: 1px solid var(--color-accent-success); background: var(--color-accent-success); color: #fff; }}
  .deny {{ border: 1px solid var(--color-neutral-medium-gray-decorative); background: transparent; }}
  .who {{ color: var(--color-text-secondary); font-size: 0.9rem; }}
</style>
</head>
<body>
<main>
  <div class="brand">Piper Morgan</div>
  <h1>{client_label} wants read-only access to your Piper Morgan account</h1>
  <p>If you approve, it will be able to read:</p>
  <ul>
    <li>your profile — organization, active projects, stated priorities
        (<code>{profile_uri}</code>)</li>
    <li>your colleague model — what Piper has confirmed with you about how you work
        (<code>{colleague_uri}</code>)</li>
    <li>your open GitHub issues, through your own connected GitHub account
        (<code>{issues_uri}</code>)</li>
  </ul>
  <p>Read-only: it cannot change anything, and it cannot see another person's data.</p>
  <p class="who">{who_html}</p>
  <form method="post" action="{action}">
    {hidden_fields}
    <div class="actions">
      <button class="approve" type="submit" name="consent" value="approve">Approve</button>
      <button class="deny" type="submit" name="consent" value="deny">Deny</button>
    </div>
  </form>
</main>
</body>
</html>
"""


def _hidden(name: str, value: str | None) -> str:
    if value is None:
        return ""
    return f'<input type="hidden" name="{html.escape(name)}" value="{html.escape(value)}">'


async def _render_consent_page(
    *,
    user_id: str,
    client_label: str,
    params: dict[str, str | None],
    consent_token: str,
) -> HTMLResponse:
    hidden_fields = (
        "\n    ".join(_hidden(k, v) for k, v in params.items() if v is not None)
        + "\n    "
        + _hidden("consent_token", consent_token)
    )
    identity = await _lookup_user_identity(user_id)
    if identity is not None:
        username, email = identity
        who_html = f"Signed in as <strong>{html.escape(username)}</strong> ({html.escape(email)})."
    else:
        # Should-never-happen fallback (user_id came from a validated session) —
        # render the raw UUID rather than a broken page. See _lookup_user_identity.
        who_html = f"Signed in as <code>{html.escape(user_id)}</code>."
    return HTMLResponse(
        _CONSENT_PAGE.format(
            client_label=html.escape(client_label),
            who_html=who_html,
            profile_uri=html.escape(PROFILE_URI),
            colleague_uri=html.escape(COLLEAGUE_MODEL_URI),
            issues_uri=html.escape(GITHUB_ISSUES_URI),
            action=AUTHORIZE_PATH,
            hidden_fields=hidden_fields,
        ),
        headers={"Cache-Control": "no-store"},
    )


def _oauth_error(error: str, description: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        {"error": error, "error_description": description},
        status_code=status_code,
        headers={"Cache-Control": "no-store"},
    )


# ── The authorize wrapper ────────────────────────────────────────────────────

# The parameters the consent page round-trips back to the SDK handler verbatim.
_AUTHORIZE_PARAMS = (
    "client_id",
    "redirect_uri",
    "response_type",
    "code_challenge",
    "code_challenge_method",
    "state",
    "scope",
    "resource",
)


def build_authorize_endpoint(provider: PiperMCPOAuthProvider):
    """The session-gated, consent-gated ``/authorize`` endpoint.

    Returns a closure rather than a module-level function so the provider (and thus
    its session scope) is explicit and injectable in tests.
    """
    sdk_handler = AuthorizationHandler(provider)

    async def authorize(request: Request) -> Response:
        user_id = _session_user_id(request)
        if not user_id:
            # NO IDENTITY, NO CODE. Nothing is read, nothing is written; the browser
            # goes to login carrying this exact request so it can be retried.
            logger.info("mcp_oauth_authorize_no_session_redirecting_to_login")
            return _login_redirect(request)

        form = await request.form() if request.method == "POST" else None
        source = form if form is not None else request.query_params
        params: dict[str, str | None] = {}
        for key in _AUTHORIZE_PARAMS:
            raw = source.get(key)
            params[key] = raw if isinstance(raw, str) else None

        client_id = params.get("client_id")
        if not client_id:
            return _oauth_error("invalid_request", "client_id is required")
        client = await provider.get_client(client_id)
        if client is None:
            return _oauth_error("invalid_request", f"Client ID '{client_id}' not found")

        raw_redirect_uri = params.get("redirect_uri")
        try:
            redirect_uri = client.validate_redirect_uri(
                AnyUrl(raw_redirect_uri) if raw_redirect_uri else None
            )
        except (InvalidRedirectUriError, ValueError) as e:
            return _oauth_error("invalid_request", str(e))

        code_challenge = params.get("code_challenge") or ""
        if not code_challenge:
            # PKCE is mandatory (the SDK's own AuthorizationRequest requires S256);
            # refuse before showing a consent page we could not honor.
            return _oauth_error("invalid_request", "code_challenge is required (PKCE S256)")

        if request.method == "GET":
            expires_at = int(time.time()) + CONSENT_TTL_SECONDS
            return await _render_consent_page(
                user_id=user_id,
                client_label=client.client_name or "This application",
                params=params,
                consent_token=_sign_consent(user_id, client_id, code_challenge, expires_at),
            )

        # ── POST: the consent decision ──
        decision = source.get("consent")
        raw_consent_token = source.get("consent_token")
        consent_token = raw_consent_token if isinstance(raw_consent_token, str) else ""
        if not _consent_token_is_valid(
            consent_token, user_id=user_id, client_id=client_id, code_challenge=code_challenge
        ):
            # Forged, stale, or issued to a DIFFERENT session's user. Refuse; do not
            # redirect (a redirect would tell an attacker their POST was shaped right).
            logger.warning("mcp_oauth_consent_token_rejected", client_id=client_id)
            return _oauth_error(
                "invalid_request",
                "This authorization request has expired or could not be verified. "
                "Start again from the application.",
            )

        if decision != "approve":
            logger.info("mcp_oauth_consent_denied", client_id=client_id)
            return RedirectResponse(
                url=construct_redirect_uri(
                    str(redirect_uri),
                    error="access_denied",
                    error_description="The user denied the request.",
                    state=params.get("state"),
                ),
                status_code=302,
                headers={"Cache-Control": "no-store"},
            )

        # Approved. Bind the consenting identity for exactly the span of the SDK
        # handler's call — `provider.authorize` reads it and refuses without it.
        with consenting_user(user_id):
            return await sdk_handler.handle(request)

    return authorize


# ── Mounting ─────────────────────────────────────────────────────────────────


def build_mcp_oauth_routes(provider: PiperMCPOAuthProvider | None = None) -> list[Route]:
    """The AS's Starlette routes, at their final (prefixed) paths.

    Built FROM the SDK's own ``create_auth_routes`` so the token/registration/
    revocation/metadata handlers are the SDK's, not re-implementations — only the
    paths are rewritten (``Route`` stores the original ``endpoint``, so re-passing
    it reproduces the SDK's exact ASGI wrapping) and ``/authorize`` is replaced by
    this module's session+consent wrapper.

    ``create_auth_routes`` derives its metadata endpoints by appending
    ``/authorize`` / ``/token`` / ``/register`` / ``/revoke`` to the issuer, and our
    issuer ends in ``/mcp/oauth`` — so the advertised URLs and the paths mounted
    here are the same strings by construction, not by coincidence.
    """
    provider = provider or PiperMCPOAuthProvider()
    sdk_routes = create_auth_routes(
        provider=provider,  # type: ignore[arg-type]
        issuer_url=AnyHttpUrl(issuer_url()),
        client_registration_options=ClientRegistrationOptions(
            enabled=True,
            valid_scopes=[RESOURCE_READ_SCOPE],
            default_scopes=[RESOURCE_READ_SCOPE],
            client_secret_expiry_seconds=None,
        ),
        revocation_options=RevocationOptions(enabled=True),
    )

    routes: list[Route] = []
    for route in sdk_routes:
        methods = sorted(route.methods or {"GET"})
        if route.path == "/authorize":
            continue  # replaced below
        if route.path == "/.well-known/oauth-authorization-server":
            # Served at BOTH discovery locations (see the METADATA_PATH_* comments).
            routes.append(Route(METADATA_PATH_RFC8414, endpoint=route.endpoint, methods=methods))
            routes.append(Route(METADATA_PATH_SUFFIXED, endpoint=route.endpoint, methods=methods))
            continue
        routes.append(Route(AS_PREFIX + route.path, endpoint=route.endpoint, methods=methods))

    routes.append(
        Route(
            AUTHORIZE_PATH,
            endpoint=build_authorize_endpoint(provider),
            methods=["GET", "POST"],
        )
    )
    return routes


def mount_mcp_oauth_routes(
    app: FastAPI, provider: PiperMCPOAuthProvider | None = None
) -> list[str]:
    """Append the AS routes to ``app``. Returns the mounted paths (for logging and
    for a test to assert against without re-deriving them).

    Appended to ``app.router.routes`` rather than mounted as a sub-app on purpose:
    the routes must sit INSIDE alpha's middleware stack (``AuthMiddleware`` is what
    gates ``/authorize`` — see the module docstring), and a Starlette sub-mount
    would also not reliably receive lifespan events.
    """
    mounted: list[str] = []
    for route in build_mcp_oauth_routes(provider):
        app.router.routes.append(route)
        mounted.append(route.path)
    logger.info("mcp_oauth_as_mounted", issuer=issuer_url(), paths=mounted)
    return mounted
