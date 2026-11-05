"""#2282 (xian 2026-11-05 10:47, Arch's shape 10:52): beta.pipermorgan.ai is the one public
host, and alpha.pipermorgan.ai answers with a permanent redirect to it, keeping the path
and the query.

The redirect is keyed on configuration, not on code: it is on only when the host
``PIPER_BASE_URL`` names (the canonical host) is a different host from the alias the
request came in on. So deploying this changes nothing until ``PIPER_BASE_URL`` moves to
beta, and the switch, the OAuth redirect URIs and #2283's host switch all move together.

Kept on the alias, never redirected (Arch's boundary): the MCP OAuth authorization
server, whose issuer is ``https://alpha.pipermorgan.ai/mcp/oauth`` and must match
exactly (RFC 8414), so every connector already registered keeps working; its well-known
metadata; the sign-in those pages send a signed-out browser to (``/login`` with an
``/mcp/`` ``next``, the auth API it posts to and the static files it loads); and
``/health``, which answers on every host. Moving the issuer is xian's separate decision.
"""

from __future__ import annotations

import os
from typing import Optional
from urllib.parse import parse_qs, urlsplit

#: Hosts that answer only with a redirect to the canonical host once it differs.
ALIAS_HOSTS = frozenset({"alpha.pipermorgan.ai"})

#: Paths that stay on the alias (Arch 10:52).
KEPT_PREFIXES = ("/mcp/", "/.well-known/", "/static/", "/api/v1/auth/")
KEPT_EXACT = frozenset({"/health"})


def canonical_host() -> Optional[str]:
    """The host ``PIPER_BASE_URL`` names, read at call time; None when unset."""
    base = os.getenv("PIPER_BASE_URL", "")
    host = (urlsplit(base).hostname or "").lower() if base else ""
    return host or None


def stays_on_alias(path: str, query: str) -> bool:
    if path in KEPT_EXACT or path.startswith(KEPT_PREFIXES):
        return True
    if path == "/login":
        nxt = (parse_qs(query).get("next") or [""])[0]
        return nxt.startswith("/mcp/")
    return False


def redirect_target(host: str, path: str, query: str) -> Optional[str]:
    """The canonical URL for a request on an alias host, or None to serve it here."""
    host = (host or "").split(":", 1)[0].lower()
    if host not in ALIAS_HOSTS:
        return None
    canonical = canonical_host()
    if not canonical or canonical == host or canonical in ALIAS_HOSTS:
        return None
    if stays_on_alias(path, query):
        return None
    return f"https://{canonical}{path}" + (f"?{query}" if query else "")


class CanonicalHostMiddleware:
    """Pure ASGI, outermost: the redirect answers before auth, so a signed-out browser on
    alpha is sent to beta rather than to alpha's sign-in."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http":
            return await self.app(scope, receive, send)
        headers = dict(scope.get("headers") or [])
        host = headers.get(b"host", b"").decode("latin-1")
        query = (scope.get("query_string") or b"").decode("latin-1")
        target = redirect_target(host, scope.get("path", ""), query)
        if target is None:
            return await self.app(scope, receive, send)
        # 301 for reads; 308 keeps the method and body for anything else.
        status = 301 if scope.get("method") in ("GET", "HEAD") else 308
        await send(
            {
                "type": "http.response.start",
                "status": status,
                "headers": [
                    (b"location", target.encode("latin-1")),
                    (b"content-length", b"0"),
                    (b"cache-control", b"no-store"),
                ],
            }
        )
        await send({"type": "http.response.body", "body": b""})
