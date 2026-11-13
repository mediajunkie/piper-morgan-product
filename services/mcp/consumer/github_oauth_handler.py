"""GitHub OAuth handler for the MCP connector (#1317 inc.2; ADR-070 option C).

A plain GitHub **OAuth App** authorization-code flow (mirrors the Google Calendar
handler, ``services/integrations/calendar/oauth_handler.py``, pointed at GitHub) — NOT
the MCP-protocol PKCE flow. It obtains the **user's GitHub OAuth token**, which Piper
forwards (Authorization header) to our self-hosted ``github-mcp-server``. The token is
then stored encrypted (the #358 ``user_api_keys`` store) and the #1229 binding holds a
*reference* to it — never the token (ADR-070 D3, precise: no raw PAT; scoped/revocable
OAuth grants permitted, encrypted-at-rest, binding = pointer).

State is user_id-bound, single-use, and expiring (CSRF + multi-tenant isolation, #734).

#2342 (ADR-081 D3): in **App mode** (``github_app_grant.app_mode``: the published GitHub
App's client ID and secret are both configured) the same authorization-code flow runs
against the App instead of the classic OAuth App. No ``scope`` is sent: the App's
permissions and the user's installation decide the reach. The token reply carries an
expiring access token and a refresh token, stored together as one grant record, and
``refresh_grant`` exchanges the refresh token for a new pair. With App mode off, nothing
here differs from before.
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

from services.infrastructure.logging.evidence import evidence  # noqa: E402 (#2350)

from .github_app_grant import GitHubAppGrant, app_client, app_mode

logger = structlog.get_logger(__name__)

# Module-level pending-state store (mirrors calendar; single-server alpha — Redis/DB later).
_PENDING_STATES: Dict[str, Dict] = {}


def _default_redirect() -> str:
    """#2043 (#1324 class): the settings-flow callback derives from PIPER_BASE_URL, so a
    deployed host needs no per-provider redirect secret; localhost only when the
    variable is absent. Read at call time, not import time, so the deployed value wins."""
    base = os.getenv("PIPER_BASE_URL", "http://localhost:8001").rstrip("/")
    return f"{base}/api/v1/settings/integrations/github/callback"


_DEFAULT_REDIRECT = _default_redirect()  # import-time value, kept for readers of the name
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
    refresh_expires_at: Optional[int] = None  # #2342: Unix ts of the refresh token's end

    def __repr__(self) -> str:  # never a token
        return (
            f"GitHubOAuthTokens(expires_at={self.expires_at}, "
            f"refresh_expires_at={self.refresh_expires_at}, "
            f"has_refresh={bool(self.refresh_token)})"
        )

    def as_app_grant(self) -> GitHubAppGrant:
        """#2342: the grant record for a token reply from the GitHub App. Raises
        ``ValueError`` when the reply lacks the refresh token or either expiry: the App
        must have "Expire user authorization tokens" on, and a record without the pair
        could never be refreshed."""
        if not (self.refresh_token and self.expires_at and self.refresh_expires_at):
            raise ValueError(
                "GitHub App token reply has no expiring pair "
                '(is "Expire user authorization tokens" on for the App?)'
            )
        return GitHubAppGrant(
            access_token=self.access_token,
            access_expires_at=int(self.expires_at),
            refresh_token=self.refresh_token,
            refresh_expires_at=int(self.refresh_expires_at),
        )


@dataclass(frozen=True)
class RefreshOutcome:
    """#2342, Arch's requirement 5 (2026-11-11 19:11). Exactly one of three:

    * ``grant`` set: GitHub issued a new pair;
    * ``rejected``: GitHub answered and refused the refresh token (expired, revoked or
      already spent), read from the reply body's ``error`` field, never from the status
      alone;
    * neither: the refresh could not complete (timeout, connection failure, 5xx, or an
      answer with no ``error`` and no token). The stored pair must be left as it was.
    """

    grant: Optional[GitHubAppGrant] = None
    rejected: bool = False
    error: Optional[str] = None  # GitHub's error code, or our own short label
    status: Optional[int] = None

    @property
    def refreshed(self) -> bool:
        return self.grant is not None

    @property
    def could_not_complete(self) -> bool:
        return self.grant is None and not self.rejected


# GitHub's token-endpoint error codes that mean "this refresh token is refused". Any
# other error code (for example ``incorrect_client_credentials``, a deployment fault) is
# not the person's grant going stale, so it reads as could-not-complete.
_REFRESH_REJECTED_ERRORS = frozenset({"bad_refresh_token", "invalid_grant"})
#: Bound on the refresh call; the per-owner lock is held across it (Arch: 10 s).
REFRESH_TIMEOUT_SECONDS = 10


class GitHubOAuthHandler:
    """OAuth 2.0 authorization-code flow for a GitHub OAuth App (#1317 inc.2)."""

    AUTHORIZATION_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_URL = "https://api.github.com/user"

    STATE_EXPIRATION = 900  # 15 min

    def __init__(self, *, classic: bool = False):
        """``classic=True`` forces the classic OAuth App's credentials even in App mode.
        Only two callers may pass it (Arch 2026-11-12): the cutover script's revoke and
        the disconnect of a classic grant."""
        self.app_mode = app_mode() and not classic
        if self.app_mode:
            self.client_id, self.client_secret = app_client()
            self.scopes = []  # #2342: no scope; the App's permissions and install decide
        else:
            self.client_id, self.client_secret = self._load_credentials()
            self.scopes = _DEFAULT_SCOPES
        self.redirect_uri = os.getenv("GITHUB_OAUTH_REDIRECT_URI") or _default_redirect()  # #2043

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
            "state": state,
        }
        if self.scopes:  # #2342: the GitHub App flow sends no scope at all
            params["scope"] = " ".join(self.scopes)
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

    async def handle_oauth_callback(
        self, code: str, state: str, *, session_user_id: Optional[str]
    ) -> Dict:
        """Verify state → (#2283) the browser's session user is the state's user → exchange
        code → return {tokens, user_id, login}. Raises on a bad state, and raises
        ``OAuthCallbackSessionMismatch`` before any exchange when the session doesn't match
        (the state is consumed either way)."""
        from services.auth.oauth_callback_guard import require_session_matches_state

        is_valid, user_id = self.verify_state(state)
        if not is_valid:
            raise ValueError("Invalid or expired state token")
        require_session_matches_state(user_id, session_user_id)
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
                return self._tokens_from_reply(data)

    @staticmethod
    def _tokens_from_reply(data: Dict) -> GitHubOAuthTokens:
        """The token endpoint's reply as tokens: the four fields #2342 stores are the
        access token, ``expires_in``, the refresh token and ``refresh_token_expires_in``."""
        now = int(time.time())
        expires_in = data.get("expires_in")
        refresh_expires_in = data.get("refresh_token_expires_in")
        return GitHubOAuthTokens(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            expires_at=(now + int(expires_in)) if expires_in else None,
            token_type=data.get("token_type", "Bearer"),
            scope=data.get("scope", ""),
            refresh_expires_at=(now + int(refresh_expires_in)) if refresh_expires_in else None,
        )

    async def refresh_grant(self, refresh_token: str) -> RefreshOutcome:
        """#2342: exchange a refresh token for a new pair at GitHub's token endpoint.

        GitHub spends the refresh token it is given, so the caller must hold the
        per-owner lock and write the returned pair before releasing it. Never raises and
        never logs a token. See ``RefreshOutcome`` for the three results."""
        if not (self.app_mode and refresh_token):
            return RefreshOutcome(error="not_app_mode")
        try:
            timeout = aiohttp.ClientTimeout(total=REFRESH_TIMEOUT_SECONDS)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    self.TOKEN_URL,
                    headers={"Accept": "application/json"},
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "grant_type": "refresh_token",
                        "refresh_token": refresh_token,
                    },
                ) as response:
                    status = response.status
                    try:
                        data = await response.json(content_type=None)
                    except Exception:
                        data = None
        except Exception as e:  # timeout, DNS, connection reset
            logger.warning("github_app_refresh_unreachable", error=type(e).__name__)
            return RefreshOutcome(error=type(e).__name__)
        if not isinstance(data, dict):
            data = {}
        error = data.get("error")
        if status >= 500:
            logger.warning("github_app_refresh_unreachable", status=status)
            return RefreshOutcome(error="server_error", status=status)
        if isinstance(error, str) and error:
            if error in _REFRESH_REJECTED_ERRORS:
                evidence("github_app_refresh_rejected", error=error, status=status)
                return RefreshOutcome(rejected=True, error=error, status=status)
            logger.warning("github_app_refresh_refused_other", error=error, status=status)
            return RefreshOutcome(error=error, status=status)
        if data.get("access_token"):
            try:
                grant = self._tokens_from_reply(data).as_app_grant()
            except ValueError:
                logger.warning("github_app_refresh_reply_incomplete", status=status)
                return RefreshOutcome(error="incomplete_reply", status=status)
            return RefreshOutcome(grant=grant, status=status)
        logger.warning("github_app_refresh_unclassifiable", status=status)
        return RefreshOutcome(error="unclassifiable", status=status)

    REVOKE_URL_TEMPLATE = "https://api.github.com/applications/{client_id}/grant"

    async def revoke_grant(self, access_token: str) -> bool:
        """#2178 (Arch 2026-10-25; P0 before any invite, xian 2026-11-04 19:31): revoke the
        person's authorization of this OAuth App at GitHub, so Piper no longer appears under
        their GitHub Settings, Applications. ``DELETE /applications/{client_id}/grant`` with
        the app's own client id and secret as basic auth and the token in the body.

        True on 204. A 404 is NOT proof (Arch 2026-11-04 20:21): GitHub answers it both for
        a grant it no longer knows and for app credentials that don't match the app the
        grant was made under (two OAuth Apps exist; a re-registered app would make that
        real). So a 404 is confirmed by a different method, ``GET /user`` with the token:
        401 means the token is gone (True); anything else means it still works or can't be
        told (False). False on any other status, on a network failure, or when this process
        holds no app credentials; the caller says the access may stay valid at GitHub.
        Never raises; never logs the token."""
        if not access_token or not self.client_id or not self.client_secret:
            return False
        url = self.REVOKE_URL_TEMPLATE.format(client_id=self.client_id)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    url,
                    auth=aiohttp.BasicAuth(self.client_id, self.client_secret),
                    headers={
                        "Accept": "application/vnd.github+json",
                        "X-GitHub-Api-Version": "2022-11-28",
                    },
                    json={"access_token": access_token},
                ) as response:
                    status = response.status
            if status == 204:
                return True
            if status == 404:
                return await self._token_is_dead(access_token)
            logger.warning("github_grant_revoke_refused", status=status)
            return False
        except Exception as e:
            logger.warning("github_grant_revoke_failed", error=type(e).__name__)
            return False

    async def _token_is_dead(self, access_token: str) -> bool:
        """#2178's 404 confirmation: ``GET /user`` with the token answers 401 only when
        GitHub no longer accepts it. Anything else (200, 403, 5xx, a network error) is not
        proof it is gone."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.USER_URL,
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/vnd.github+json",
                    },
                ) as response:
                    dead = response.status == 401
            if not dead:
                logger.warning("github_grant_revoke_404_but_token_alive")
            return dead
        except Exception as e:
            logger.warning("github_grant_revoke_confirm_failed", error=type(e).__name__)
            return False

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
    app_grant: Optional[GitHubAppGrant] = None,
) -> None:
    """Complete a GitHub connection (#1317 inc.2 slice D orchestration).

    Stores the user's OAuth grant encrypted (the #358 store via ``ConnectorGrantStore``)
    and marks the #1229 ``ConnectorBinding`` BOUND, recording the self-hosted server ref.
    The binding references the grant by the ``(owner, connector)`` convention — it holds
    no token (ADR-070 D3). Caller owns the transaction (commit after).

    #2342: with ``app_grant`` (a GitHub App connect) the grant record is stored, both
    tokens and both expiries in one row, and ``access_token`` is ignored. Marking the
    binding BOUND clears any stored ``status_reason``.
    """
    from services.connectors.binding_repository import ConnectorBindingRepository

    from .connector_grant_store import ConnectorGrantStore

    store = grant_store or ConnectorGrantStore()
    if app_grant is not None:
        await store.store_app_grant(session, user_id, "github", app_grant)
    else:
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
