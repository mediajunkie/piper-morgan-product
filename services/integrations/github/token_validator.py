"""GitHub PAT validation via the canonical `GET /user` API call (#1192 slice c).

Background: the settings connect/status endpoints used to validate a GitHub
token through `GitHubIntegrationRouter.test_connection()`, but the MCP migration
(#198) left `test_connection` unimplemented on BOTH the MCP adapter and the
spatial fallback — so the call always raised `AttributeError`, and the connect
endpoint returned HTTP 500 for *any* PAT, valid or not (the #541 "stuck state").

This module replaces that broken path with a direct, dependency-free check:
hit `GET https://api.github.com/user` with the token. A 200 means the token is
valid and gives us the username; 401 means invalid/expired. It does not touch
the router/adapter, so it can't regress on their internals again.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

_GITHUB_USER_URL = "https://api.github.com/user"


async def verify_github_token(token: Optional[str], *, timeout: float = 10.0) -> Dict[str, Any]:
    """Validate a GitHub personal access token.

    Args:
        token: the PAT to validate (``None``/empty → not authenticated).
        timeout: per-request timeout in seconds.

    Returns:
        ``{"authenticated": bool, "username": str | None, "error": str | None}``
        — the same shape the old ``test_connection`` result was read for, so
        callers need only swap the call.
    """
    if not token:
        return {"authenticated": False, "username": None, "error": "No token provided"}

    import httpx

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "piper-morgan",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(_GITHUB_USER_URL, headers=headers)
    except Exception as e:  # network/DNS/timeout — surface, don't crash the endpoint
        return {"authenticated": False, "username": None, "error": f"Connection error: {e}"}

    if resp.status_code == 200:
        try:
            login = resp.json().get("login")
        except Exception:
            login = None
        return {"authenticated": True, "username": login, "error": None}
    if resp.status_code == 401:
        return {
            "authenticated": False,
            "username": None,
            "error": "Invalid or expired token (GitHub returned 401)",
        }
    if resp.status_code == 403:
        return {
            "authenticated": False,
            "username": None,
            "error": "Token rejected or rate-limited (GitHub returned 403)",
        }
    return {
        "authenticated": False,
        "username": None,
        "error": f"GitHub returned HTTP {resp.status_code}",
    }
