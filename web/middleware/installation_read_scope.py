"""#2379 (Arch 2026-11-15 15:49): one GitHub App installation read per request.

On a GitHub App grant every repository list, issue search and repo-scoped read first
asks GitHub where the App is installed. A chat turn can ask more than once (the
resolver, then the read). This opens ``installation_read_scope`` around each HTTP
request, so the first answer is reused until the response is sent and then dropped.
Nothing is held across requests.

Pure ASGI, not ``BaseHTTPMiddleware``: the scope is a context variable, and the layers
inside this one run in tasks that copy this context when they start.
"""

from __future__ import annotations

from services.mcp.consumer.github_app_install import installation_read_scope


class InstallationReadScopeMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return
        with installation_read_scope():
            await self.app(scope, receive, send)
