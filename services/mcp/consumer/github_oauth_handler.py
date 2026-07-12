"""GitHub OAuth handler for the MCP connector (#1317 inc.2; ADR-070 option C).

A plain GitHub **OAuth App** authorization-code flow (mirrors the Google Calendar
handler, ``services/integrations/calendar/oauth_handler.py``, pointed at GitHub) — NOT
the MCP-protocol PKCE flow. It obtains the **user's GitHub OAuth token**, which Piper
forwards (Authorization header) to our self-hosted ``github-mcp-server``. The token is
then stored encrypted (the #358 ``user_api_keys`` store) and the #1229 binding holds a
*reference* to it — never the token (ADR-070 D3, precise: no raw PAT; scoped/revocable
OAuth grants permitted, encrypted-at-rest, binding = pointer).

State is user_id-bound, single-use, and expiring (CSRF + multi-tenant isolation, #734).
"""

from __future__ import annotations

import base64
import json
import os
import secrets
import time
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from urllib.parse import urlencode

import aiohttp
import structlog

logger = structlog.get_logger(__name__)

# Module-level pending-state store (mirrors calendar; single-server alpha — Redis/DB later).
_PENDING_STATES: Dict[str, Dict] = {}

_DEFAULT_REDIRECT = "http://localhost:8001/api/v1/settings/integrations/github/callback"
_DEFAULT_SCOPES = ["repo"]  # repos/issues/PRs; confirm minimal set. Requested in-flow.
# The self-hosted github-mcp-server URL the binding records + resolve() connects to
# (ADR-070 C). Set GITHUB_MCP_SERVER_URL per-environment (Droplet → the deployed server).
_DEFAULT_MCP_SERVER_URL = os.getenv("GITHUB_MCP_SERVER_URL", "http://localhost:9100/mcp")


@dataclass
class GitHubOAuthTokens:
    """A user's GitHub OAuth grant. Classic OAuth-App tokens don't expire/refresh unless
    the App enables expiring tokens — hence refresh_token/expires_at are optional."""

    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[int] = None  # Unix ts, if the App issues expiring tokens
    token_type: str = "Bearer"
    scope: str = ""


class GitHubOAuthHandler:
    """OAuth 2.0 authorization-code flow for a GitHub OAuth App (#1317 inc.2)."""

    AUTHORIZATION_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_URL = "https://api.github.com/user"

    STATE_EXPIRATION = 900  # 15 min

    def __init__(self):
        self.client_id, self.client_secret = self._load_credentials()
        self.redirect_uri = os.getenv("GITHUB_OAUTH_REDIRECT_URI", _DEFAULT_REDIRECT)
        self.scopes = _DEFAULT_SCOPES

    def _load_credentials(self) -> Tuple[str, str]:
        """env first, then KeychainService (provider github_oauth_client_id/_secret)."""
        client_id = os.getenv("GITHUB_OAUTH_CLIENT_ID", "")
        client_secret = os.getenv("GITHUB_OAUTH_CLIENT_SECRET", "")
        if not client_id or not client_secret:
            try:
                from services.infrastructure.keychain_service import KeychainService

                kc = KeychainService()
                client_id = client_id or (kc.get_api_key("github_oauth_client_id") or "")
                client_secret = client_secret or (
                    kc.get_api_key("github_oauth_client_secret") or ""
                )
            except Exception:
                pass  # keychain unavailable → empty (handler still constructs; flow fails honestly)
        return client_id, client_secret

    def generate_authorization_url(self, user_id: str) -> Tuple[str, str]:
        """Build the GitHub authorize URL with a user-bound, single-use state (CSRF/#734)."""
        if not user_id:
            raise ValueError("user_id is required for OAuth state")

        nonce = secrets.token_urlsafe(16)
        state_data = {"user_id": user_id, "nonce": nonce}
        state = base64.urlsafe_b64encode(json.dumps(state_data).encode()).decode().rstrip("=")
        _PENDING_STATES[nonce] = {"created_at": time.time(), "user_id": user_id}

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
            "state": state,
        }
        auth_url = f"{self.AUTHORIZATION_URL}?{urlencode(params)}"
        logger.info("github_oauth_url_generated", user_id=user_id, state_prefix=state[:8])
        return auth_url, state

    def verify_state(self, state: str) -> Tuple[bool, Optional[str]]:
        """Validate + consume a state token. Returns (is_valid, user_id). Single-use."""
        try:
            padded = state + "=" * (-len(state) % 4)
            state_data = json.loads(base64.urlsafe_b64decode(padded))
        except (ValueError, json.JSONDecodeError):
            logger.warning("github_oauth_state_decode_failed", state_prefix=(state or "")[:8])
            return False, None

        nonce = state_data.get("nonce")
        user_id = state_data.get("user_id")
        if not nonce or not user_id or nonce not in _PENDING_STATES:
            logger.warning(
                "github_oauth_state_invalid", has_nonce=bool(nonce), has_uid=bool(user_id)
            )
            return False, None

        nonce_data = _PENDING_STATES[nonce]
        if time.time() - nonce_data["created_at"] > self.STATE_EXPIRATION:
            del _PENDING_STATES[nonce]
            logger.warning("github_oauth_state_expired", nonce_prefix=nonce[:8])
            return False, None
        if nonce_data.get("user_id") != user_id:  # tamper detection (#734)
            del _PENDING_STATES[nonce]
            logger.warning("github_oauth_state_user_mismatch")
            return False, None

        del _PENDING_STATES[nonce]  # single-use
        return True, user_id

    async def handle_oauth_callback(self, code: str, state: str) -> Dict:
        """Verify state → exchange code → return {tokens, user_id, login}. Raises on bad state."""
        is_valid, user_id = self.verify_state(state)
        if not is_valid:
            raise ValueError("Invalid or expired state token")
        tokens = await self._exchange_code_for_tokens(code)
        login = await self._get_login(tokens.access_token)
        logger.info(
            "github_oauth_callback_success",
            user_id=user_id,
            login=login,
            has_token=bool(tokens.access_token),  # presence only — never log the token
        )
        return {"tokens": tokens, "user_id": user_id, "login": login}

    async def _exchange_code_for_tokens(self, code: str) -> GitHubOAuthTokens:
        """Exchange the authorization code for a GitHub OAuth token (JSON via Accept header)."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.TOKEN_URL,
                headers={"Accept": "application/json"},
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": self.redirect_uri,
                },
            ) as response:
                data = await response.json()
                if response.status != 200 or "access_token" not in data:
                    logger.error(
                        "github_token_exchange_failed",
                        status=response.status,
                        error=data.get("error", "unknown"),
                    )
                    raise ValueError(
                        f"GitHub token exchange failed: {data.get('error', response.status)}"
                    )
                expires_in = data.get("expires_in")
                return GitHubOAuthTokens(
                    access_token=data["access_token"],
                    refresh_token=data.get("refresh_token"),
                    expires_at=(int(time.time()) + expires_in) if expires_in else None,
                    token_type=data.get("token_type", "Bearer"),
                    scope=data.get("scope", ""),
                )

    async def _get_login(self, access_token: str) -> str:
        """The authenticated user's GitHub login (identity for logging; best-effort)."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.USER_URL,
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/vnd.github+json",
                    },
                ) as response:
                    if response.status != 200:
                        return "unknown"
                    return (await response.json()).get("login", "unknown")
        except Exception:
            return "unknown"


async def persist_github_connection(
    session,
    user_id: str,
    access_token: str,
    *,
    grant_store=None,
    server_ref: Optional[str] = None,
) -> None:
    """Complete a GitHub connection (#1317 inc.2 slice D orchestration).

    Stores the user's OAuth grant encrypted (the #358 store via ``ConnectorGrantStore``)
    and marks the #1229 ``ConnectorBinding`` BOUND, recording the self-hosted server ref.
    The binding references the grant by the ``(owner, connector)`` convention — it holds
    no token (ADR-070 D3). Caller owns the transaction (commit after).
    """
    from services.connectors.binding_repository import ConnectorBindingRepository

    from .connector_grant_store import ConnectorGrantStore

    store = grant_store or ConnectorGrantStore()
    await store.store(session, user_id, "github", access_token)
    await ConnectorBindingRepository(session).upsert(
        user_id,
        "github",
        status="bound",
        # ADR-070-A (A1): managed bindings store the LOGICAL KEY; the URL
        # resolves from deployment config at connect-time (resolve_server_ref).
        # An explicit server_ref (BYOC literal) still passes through verbatim.
        mcp_server_ref=(server_ref or "github"),
    )
