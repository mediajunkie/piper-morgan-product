"""Piper Morgan MCP OAuth 2.1 authorization server provider (Phase C unit 4, #1462).

Companion docs: ``docs/internal/architecture/current/mcp/phase-c-build-plan-2026-09-25.md``
(unit 4) and ``server-README.md`` (the two-host topology). The HTTP surface that
mounts this provider lives in ``web/routers/mcp_oauth.py`` — in the **alpha web
app**, not the MCP server, because alpha is the host that holds the user's login
session. The MCP server stays a pure resource server: it verifies the tokens this
module mints via unit 1's unchanged
``services/mcp/server/identity.py:MCPTokenVerifier``.

WHY IT LIVES HERE (``services/mcp/server/``) AND NOT UNDER ``web/``: this is the
credential-*issuance* half of the same identity boundary unit 1 built the
verification half of. They share the ``mcp_access_tokens`` table and the one hash
function (:func:`services.mcp.server.identity.hash_credential`); splitting them
across trees is how the two halves drift.

═══ THE ONE PROPERTY THIS MODULE EXISTS TO GUARANTEE ═══

Arch's unit-4 review condition (2026-09-26): *the minted token must be bound to
the SAME identity that authenticated at the authorize step, throughout — the
failure shape being ``exchange_authorization_code`` minting a token for a
different (or unresolved) identity than the one that consented.*

Four structural facts implement it, in order of how they'd have to ALL fail:

1. **``authorize()`` cannot mint a code without a resolved identity.** The user id
   comes from :func:`consenting_user_id` — a contextvar set ONLY by the consent
   route in ``web/routers/mcp_oauth.py``, and only after alpha's own
   ``AuthMiddleware`` authenticated a real session AND that session's owner posted
   Approve. If the contextvar is unset, :meth:`PiperMCPOAuthProvider.authorize`
   raises ``AuthorizeError`` and writes nothing. There is no default user, no
   client-supplied user, and no "resolve later" path.
2. **The code row is the only carrier of identity**, and ``user_id`` on it is NOT
   NULL (``services/database/models.py:MCPOAuthCode``).
3. **``exchange_authorization_code`` mints for the STORED ROW's ``user_id``**, read
   back from the store after the code has been atomically claimed — never for a
   value carried on the ``AuthorizationCode`` object the SDK handler passed in. If
   the object's ``user_id`` and the row's disagree, that is a tamper signal and the
   exchange REFUSES rather than picking one. The whole decision is one pure
   function, :func:`_refuse_code`, so "may this code be exchanged, and for whom?"
   is readable and testable in one place; :meth:`PiperMCPOAuthProvider._mint_pair`
   is the only code in this module that creates a usable credential and it takes
   the owner as an explicit argument rather than deriving one.
4. **The minted access token is an ``mcp_access_tokens`` row** whose ``user_id`` is
   that same value, so the resource server's existing verifier resolves the caller
   to the consenting user by construction — one verifier, one boundary, no second
   credential format to keep in sync.

Pinned by ``tests/unit/services/mcp/server/test_oauth_as_unit4.py`` — explicitly,
not as an assumed property of using the SDK's provider frame correctly.

═══ AT REST ═══

Authorization codes, access tokens and refresh tokens are stored ONLY as SHA-256
hex digests, via the same :func:`~services.mcp.server.identity.hash_credential` the
verifier uses. Raw values exist only in the HTTP response that returns them. No raw
credential is ever logged (:func:`~services.mcp.server.identity.mask_token` is used
where a log line needs to name one). The one at-rest exception, and why, is
documented on ``MCPOAuthClient.client_secret``.
"""

from __future__ import annotations

import enum
import secrets
import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, AsyncContextManager, Callable, Iterator, cast

import structlog
from mcp.server.auth.provider import (
    AccessToken,
    AuthorizationCode,
    AuthorizationParams,
    AuthorizeError,
    RefreshToken,
    RegistrationError,
    TokenError,
    construct_redirect_uri,
)
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken
from pydantic import AnyUrl
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import (
    MCPAccessToken,
    MCPOAuthClient,
    MCPOAuthCode,
    MCPOAuthRefreshToken,
)
from services.database.session_factory import AsyncSessionFactory
from services.mcp.server.identity import (
    RESOURCE_READ_SCOPE,
    hash_credential,
    mask_token,
)

SessionScopeFactory = Callable[[], AsyncContextManager[AsyncSession]]

logger = structlog.get_logger(__name__)

# ── Lifetimes ────────────────────────────────────────────────────────────────
# Authorization code: OAuth 2.1 §4.1.2 says codes SHOULD be short-lived and
# single-use; 10 minutes is the RFC 6749 §4.1.2 recommended maximum.
CODE_TTL = timedelta(minutes=10)
# Access token: short, because a refresh token exists to renew it and the
# resource server has no introspection round trip to catch a mid-life revoke.
ACCESS_TOKEN_TTL = timedelta(hours=1)
REFRESH_TOKEN_TTL = timedelta(days=30)

# Prefixes make a leaked credential identifiable in a log or a paste, and make
# the three families visually distinct in an incident. They are NOT parsed for
# authorization decisions anywhere.
CODE_PREFIX = "mcp_code_"
ACCESS_TOKEN_PREFIX = "mcp_"  # same shape operator-minted tokens use (unit 1)
REFRESH_TOKEN_PREFIX = "mcp_refresh_"

# `mcp_access_tokens.label` for an OAuth-minted row. The client_id suffix is how
# `load_access_token` (used ONLY by /revoke — see its docstring) recovers which
# OAuth client a token belongs to.
OAUTH_LABEL_PREFIX = "oauth:"

# Registration limits (the "sane limits" half of ClientRegistrationOptions).
MAX_REDIRECT_URIS = 10


class _Refusal(str, enum.Enum):
    """Named so refusals are grep-able in the log. Never surfaced to a caller
    verbatim — the OAuth error responses carry the spec's own error codes."""

    NO_CONSENTING_IDENTITY = "no_consenting_identity"
    CODE_NOT_FOUND = "code_not_found"
    CODE_WRONG_CLIENT = "code_wrong_client"
    CODE_ALREADY_USED = "code_already_used"
    CODE_EXPIRED = "code_expired"
    CODE_NO_OWNER = "code_no_owner"
    CODE_OWNER_MISMATCH = "code_owner_mismatch"
    REFRESH_NOT_FOUND = "refresh_not_found"
    REFRESH_WRONG_CLIENT = "refresh_wrong_client"
    REFRESH_REVOKED = "refresh_revoked"
    REFRESH_EXPIRED = "refresh_expired"


# ── The consenting-identity contextvar ───────────────────────────────────────
#
# The SDK's `AuthorizationHandler` calls `provider.authorize(client, params)` with
# no access to the HTTP request, so the resolved session user has to reach the
# provider some other way. A contextvar is the right mechanism and not a
# workaround: it is set by the consent route in the SAME task that then awaits the
# handler, it is reset on the way out, and — critically — its DEFAULT is None, so
# the failure mode of forgetting to set it is a refusal, never an anonymous mint.
# (This is the same shape the SDK itself uses to carry the verified identity into
# a resource handler: `mcp.server.auth.middleware.auth_context`.)
_consenting_user_id: ContextVar[str | None] = ContextVar(
    "mcp_oauth_consenting_user_id", default=None
)


@contextmanager
def consenting_user(user_id: str) -> Iterator[None]:
    """Bind the authenticated-and-consenting alpha session user for the duration
    of one ``/authorize`` completion.

    Refuses an empty/None user id outright: the whole point is that there is no
    such thing as "authorize on behalf of nobody", so an empty binding must fail
    at the binding site rather than produce a code with no owner downstream.
    """
    if not user_id:
        raise ValueError(
            "consenting_user() requires a real user id — there is no anonymous "
            "consent path (see module docstring, property 1)."
        )
    token = _consenting_user_id.set(str(user_id))
    try:
        yield
    finally:
        _consenting_user_id.reset(token)


def consenting_user_id() -> str | None:
    """The consenting alpha session user for the current task, or ``None``.

    ``None`` is a refusal signal, never "use a default".
    """
    return _consenting_user_id.get()


# ── SDK model subclasses carrying the owner ──────────────────────────────────
# The SDK explicitly sanctions this ("NOTE: FastMCP doesn't render any of these
# types in the user response, so it's OK to add fields to subclasses which should
# not be exposed externally" — mcp/server/auth/provider.py). `user_id` is REQUIRED
# on both: a pydantic validation error is a better outcome than an owner-less code
# object reaching the exchange.


class PiperAuthorizationCode(AuthorizationCode):
    """An authorization code plus the id of the user who actually consented."""

    user_id: str


class PiperRefreshToken(RefreshToken):
    """A refresh token plus the id of the user it was originally consented for."""

    user_id: str


@dataclass(frozen=True)
class _CodeSnapshot:
    """A detached read of one ``mcp_oauth_codes`` row.

    Detached on purpose: every refusal decision about a code is made on these plain
    values, outside any open session — see :meth:`PiperMCPOAuthProvider.exchange_authorization_code`
    for why a raise must not cross a session scope's exit in this SDK.
    """

    id: uuid.UUID
    user_id: str | None
    client_id: str
    scopes: list[str]
    expires_at: datetime | None


def _refuse_code(
    client: OAuthClientInformationFull,
    snapshot: _CodeSnapshot | None,
    *,
    claimed_user_id: str | None,
    now: datetime,
) -> str | None:
    """``None`` = this code may be exchanged. Otherwise the ``error_description`` to
    refuse with.

    A PURE function (no I/O, no state) so the identity-binding decision is readable
    in one place and directly testable without a store. The order matters less than
    the fact that every branch is a refusal: there is no branch that repairs a bad
    code, substitutes an owner, or falls through.

    ``claimed_user_id`` is what the SDK handler carried in on the
    ``AuthorizationCode`` object. It is used ONLY to detect disagreement — the
    stored row is the authority. If they differ, something between the store and
    this call changed the owner, and the right answer to that is to refuse, not to
    pick a side. That is Arch's named failure shape, made unreachable rather than
    merely unlikely.
    """
    if snapshot is None:
        logger.warning(
            "mcp_oauth_exchange_refused",
            reason=_Refusal.CODE_NOT_FOUND.value,
            client_id=client.client_id,
        )
        return "authorization code does not exist"
    if not snapshot.user_id:
        # The column is NOT NULL, so this is unreachable through the store —
        # checked anyway, and tested, because "structurally impossible" is a claim
        # and a refusal is a mechanism.
        logger.error(
            "mcp_oauth_exchange_refused",
            reason=_Refusal.CODE_NO_OWNER.value,
            client_id=client.client_id,
        )
        return "authorization code is invalid"
    if claimed_user_id and claimed_user_id != snapshot.user_id:
        logger.error(
            "mcp_oauth_exchange_refused",
            reason=_Refusal.CODE_OWNER_MISMATCH.value,
            client_id=client.client_id,
            stored_user_id=snapshot.user_id,
            claimed_user_id=claimed_user_id,
        )
        return "authorization code is invalid"
    if snapshot.client_id != str(client.client_id):
        logger.warning(
            "mcp_oauth_exchange_refused",
            reason=_Refusal.CODE_WRONG_CLIENT.value,
            client_id=client.client_id,
            code_client_id=snapshot.client_id,
        )
        return "authorization code is invalid"
    if snapshot.expires_at is not None and snapshot.expires_at <= now:
        logger.warning(
            "mcp_oauth_exchange_refused",
            reason=_Refusal.CODE_EXPIRED.value,
            client_id=client.client_id,
        )
        return "authorization code has expired"
    return None


def _as_aware_utc(value: datetime | None) -> datetime | None:
    """Normalize to tz-aware UTC — SQLite (the unit tests' backend) drops tzinfo
    on read-back where PostgreSQL's TIMESTAMPTZ preserves it. Same helper, same
    reasoning, as ``identity.py``'s; every value this module writes is already UTC.
    """
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


class PiperMCPOAuthProvider:
    """``OAuthAuthorizationServerProvider`` over Piper's own tables.

    Structurally typed against the SDK's Protocol (no inheritance needed); the
    mount in ``web/routers/mcp_oauth.py`` passes an instance to
    ``mcp.server.auth.routes.create_auth_routes``.

    ``session_scope`` is resolved LAZILY (not captured in ``__init__``) so a test
    that monkeypatches ``AsyncSessionFactory.session_scope`` after this provider
    was constructed still takes effect — the alpha app builds its provider at
    import time, long before any test fixture runs.
    """

    def __init__(self, session_scope: SessionScopeFactory | None = None) -> None:
        self._injected_scope = session_scope

    def _scope(self) -> AsyncContextManager[AsyncSession]:
        scope = self._injected_scope or AsyncSessionFactory.session_scope
        return scope()

    # ── Dynamic client registration (RFC 7591) ───────────────────────────────

    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        """Persist a self-registered client.

        Deliberately stores NO ``user_id``: a client is an application, not a
        user's possession. Identity enters the flow exactly one table later
        (``mcp_oauth_codes.user_id``), set only from the consenting session.
        """
        redirect_uris = [str(u) for u in (client_info.redirect_uris or [])]
        if not redirect_uris:
            raise RegistrationError(
                error="invalid_redirect_uri",
                error_description="At least one redirect_uri is required.",
            )
        if len(redirect_uris) > MAX_REDIRECT_URIS:
            raise RegistrationError(
                error="invalid_client_metadata",
                error_description=f"At most {MAX_REDIRECT_URIS} redirect URIs may be registered.",
            )
        for uri in redirect_uris:
            if not _is_acceptable_redirect_uri(uri):
                raise RegistrationError(
                    error="invalid_redirect_uri",
                    error_description=(
                        "A redirect_uri must be https, or http on localhost/127.0.0.1 "
                        "for local development."
                    ),
                )

        async with self._scope() as session:
            session.add(
                MCPOAuthClient(
                    client_id=str(client_info.client_id),
                    client_secret=client_info.client_secret,
                    client_secret_expires_at=(
                        datetime.fromtimestamp(client_info.client_secret_expires_at, timezone.utc)
                        if client_info.client_secret_expires_at
                        else None
                    ),
                    redirect_uris=redirect_uris,
                    client_name=client_info.client_name,
                    token_endpoint_auth_method=(
                        client_info.token_endpoint_auth_method or "client_secret_post"
                    ),
                    grant_types=list(client_info.grant_types),
                    response_types=list(client_info.response_types),
                    scope=client_info.scope,
                )
            )

        logger.info(
            "mcp_oauth_client_registered",
            client_id=client_info.client_id,
            client_name=client_info.client_name,
            redirect_uris=redirect_uris,
        )

    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        async with self._scope() as session:
            row = await session.get(MCPOAuthClient, client_id)
            if row is None:
                return None
            return OAuthClientInformationFull(
                client_id=str(row.client_id),
                client_secret=row.client_secret,
                client_secret_expires_at=(
                    int(_as_aware_utc(row.client_secret_expires_at).timestamp())  # type: ignore[union-attr]
                    if row.client_secret_expires_at is not None
                    else None
                ),
                redirect_uris=[AnyUrl(u) for u in (row.redirect_uris or [])],
                client_name=row.client_name,
                token_endpoint_auth_method=row.token_endpoint_auth_method,
                grant_types=list(row.grant_types or []),
                response_types=list(row.response_types or []),
                scope=row.scope,
            )

    # ── /authorize ───────────────────────────────────────────────────────────

    async def authorize(
        self, client: OAuthClientInformationFull, params: AuthorizationParams
    ) -> str:
        """Issue an authorization code bound to the CONSENTING user, or refuse.

        Reached only from the consent route's approve branch (see module docstring
        property 1). ``consenting_user_id()`` returning ``None`` here means one of:
        the route was bypassed, the contextvar was not set, or someone wired a new
        caller. All three are refusals — there is no default user.
        """
        user_id = consenting_user_id()
        if not user_id:
            logger.warning(
                "mcp_oauth_authorize_refused",
                reason=_Refusal.NO_CONSENTING_IDENTITY.value,
                client_id=client.client_id,
            )
            raise AuthorizeError(
                error="access_denied",
                error_description=(
                    "No authenticated Piper Morgan session has consented to this "
                    "authorization request."
                ),
            )

        raw_code = CODE_PREFIX + secrets.token_urlsafe(32)  # 256 bits of entropy
        now = datetime.now(timezone.utc)
        scopes = list(params.scopes or [RESOURCE_READ_SCOPE])

        async with self._scope() as session:
            session.add(
                MCPOAuthCode(
                    id=uuid.uuid4(),
                    code_hash=hash_credential(raw_code),
                    client_id=str(client.client_id),
                    user_id=uuid.UUID(str(user_id)),
                    redirect_uri=str(params.redirect_uri),
                    redirect_uri_provided_explicitly=params.redirect_uri_provided_explicitly,
                    code_challenge=params.code_challenge,
                    scopes=scopes,
                    resource=params.resource,
                    created_at=now,
                    expires_at=now + CODE_TTL,
                )
            )

        logger.info(
            "mcp_oauth_code_issued",
            client_id=client.client_id,
            user_id=str(user_id),
            code=mask_token(raw_code),
            scopes=scopes,
        )
        return construct_redirect_uri(str(params.redirect_uri), code=raw_code, state=params.state)

    async def load_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: str
    ) -> PiperAuthorizationCode | None:
        """Load a code by its raw value, or ``None``.

        Returns a row even when ``used_at`` is already set — DELIBERATELY. The
        SDK's token handler only calls ``exchange_authorization_code`` for a code
        this method returned, and the replay revocation OAuth 2.1 §4.1.2.5 requires
        lives there. Refusing a used code here would turn a replay into a plain
        "no such code" and silently skip the revocation.
        """
        code_hash = hash_credential(authorization_code)
        async with self._scope() as session:
            # ADR-079 D4/D6: the code IS the credential; this lookup RESOLVES the
            # owner (user_id is the OUTPUT), and code_hash is UNIQUE, so it is a
            # single-row lookup by the credential itself. Same shape as unit 1's
            # token lookup in identity.py.
            row = (
                await session.execute(
                    select(MCPOAuthCode).where(  # global-ok: resolves owner, see above
                        MCPOAuthCode.code_hash == code_hash
                    )
                )
            ).scalar_one_or_none()

            if row is None:
                logger.warning(
                    "mcp_oauth_code_refused",
                    reason=_Refusal.CODE_NOT_FOUND.value,
                    client_id=client.client_id,
                )
                return None
            if str(row.client_id) != str(client.client_id):
                # Defense in depth: the SDK's token handler checks this too, but a
                # code must never be READABLE by another client either.
                logger.warning(
                    "mcp_oauth_code_refused",
                    reason=_Refusal.CODE_WRONG_CLIENT.value,
                    client_id=client.client_id,
                    code_client_id=str(row.client_id),
                )
                return None
            if not row.user_id:
                # Structurally impossible (NOT NULL) — asserted anyway, because a
                # code with no owner must never reach the exchange.
                logger.error(
                    "mcp_oauth_code_refused",
                    reason=_Refusal.CODE_NO_OWNER.value,
                    client_id=client.client_id,
                )
                return None

            expires_at = _as_aware_utc(row.expires_at)
            return PiperAuthorizationCode(
                code=authorization_code,
                scopes=list(row.scopes or [RESOURCE_READ_SCOPE]),
                expires_at=expires_at.timestamp() if expires_at else 0.0,
                client_id=str(row.client_id),
                code_challenge=str(row.code_challenge),
                redirect_uri=AnyUrl(str(row.redirect_uri)),
                redirect_uri_provided_explicitly=bool(row.redirect_uri_provided_explicitly),
                resource=row.resource,
                user_id=str(row.user_id),
            )

    # ── /token (authorization_code grant) ────────────────────────────────────

    async def exchange_authorization_code(
        self,
        client: OAuthClientInformationFull,
        authorization_code: PiperAuthorizationCode,
    ) -> OAuthToken:
        """Mint an access + refresh token for the code's OWNER, once.

        Single-use is an atomic conditional UPDATE (``used_at IS NULL``), so two
        concurrent exchanges cannot both win. The loser — and any later replay —
        gets ``invalid_grant`` AND causes the credentials the winner minted to be
        revoked, per OAuth 2.1 §4.1.2.5 ("If an authorization code is used more
        than once, the authorization server MUST deny the request and SHOULD
        revoke ... all tokens previously issued based on that authorization code").
        """
        code_hash = hash_credential(authorization_code.code)
        now = datetime.now(timezone.utc)

        # ⚠️ THREE SCOPES, NOT ONE, AND THE SPLIT IS LOAD-BEARING. `_scope()` rolls
        # back on any exception (#1193 contract), so doing the claim, the replay
        # revocation, and the mint in one transaction would mean that raising
        # TokenError for a replay ROLLS BACK the revocation the spec requires —
        # a fail-open dressed as a refusal. Claiming separately also means a
        # refusal during minting leaves the code BURNED, which is the safe
        # direction for a single-use credential.
        if not await self._claim_code(code_hash, now):
            # Already exchanged (replay) or never existed. Revoke whatever the
            # first exchange minted (committed on its own), then refuse.
            await self._revoke_credentials_minted_for_code(code_hash)
            logger.warning(
                "mcp_oauth_exchange_refused",
                reason=_Refusal.CODE_ALREADY_USED.value,
                client_id=client.client_id,
                code=mask_token(authorization_code.code),
            )
            raise TokenError(
                error="invalid_grant",
                error_description="authorization code has already been used",
            )

        snapshot = await self._read_code(code_hash)
        # ⚠️ The refusal decision is made here, OUTSIDE any session scope, and so is
        # the raise. The SDK's OAuth error types are FROZEN dataclasses, and
        # `contextlib`'s async-CM exit assigns `exc.__traceback__` on the way out —
        # which raises `FrozenInstanceError` and turns a clean `invalid_grant` into
        # a 500. Found by test, not by reading: raising a TokenError inside
        # `async with self._scope()` does not work in this SDK. Keep refusals out of
        # the `with`.
        refusal = _refuse_code(
            client, snapshot, claimed_user_id=authorization_code.user_id, now=now
        )
        if refusal is not None:
            raise TokenError(error="invalid_grant", error_description=refusal)
        assert snapshot is not None and snapshot.user_id  # narrowed by _refuse_code

        return await self._mint_pair(
            grant="authorization_code",
            user_id=snapshot.user_id,
            client_id=str(client.client_id),
            scopes=snapshot.scopes,
            now=now,
            code_id=snapshot.id,
        )

    async def _read_code(self, code_hash: str) -> _CodeSnapshot | None:
        """Read the stored code as a plain snapshot, so every decision downstream is
        made on detached values rather than on a live ORM row bound to a session
        that has to stay open (and that a raise must not escape — see
        :meth:`exchange_authorization_code`)."""
        async with self._scope() as session:
            row = (
                await session.execute(
                    # global-ok: same single-credential lookup as load_authorization_code
                    select(MCPOAuthCode).where(MCPOAuthCode.code_hash == code_hash)
                )
            ).scalar_one_or_none()
            if row is None:
                return None
            return _CodeSnapshot(
                # The PK is NOT NULL; `Column` reads as `Any | None` to mypy.
                id=cast(uuid.UUID, row.id),
                user_id=str(row.user_id) if row.user_id else None,
                client_id=str(row.client_id),
                scopes=list(row.scopes or [RESOURCE_READ_SCOPE]),
                expires_at=_as_aware_utc(row.expires_at),
            )

    async def _claim_code(self, code_hash: str, now: datetime) -> bool:
        """Atomically mark a code used. ``False`` = it was already used (or never
        existed), which is the replay signal. Its own transaction, so the claim is
        durable before anything else in the exchange can fail."""
        async with self._scope() as session:
            claimed = await session.execute(
                update(MCPOAuthCode)
                .where(  # global-ok: claims one row BY THE CREDENTIAL's unique hash; the owner is the row's OUTPUT
                    MCPOAuthCode.code_hash == code_hash,
                    MCPOAuthCode.used_at.is_(None),
                )
                .values(used_at=now)
            )
            return bool(claimed.rowcount)

    async def _mint_pair(
        self,
        *,
        grant: str,
        user_id: str,
        client_id: str,
        scopes: list[str],
        now: datetime,
        code_id: uuid.UUID | None = None,
    ) -> OAuthToken:
        """Mint an access + refresh token FOR ``user_id`` — the only place in this
        module that creates a usable credential, and it takes the owner as an
        explicit argument rather than deriving one, so there is exactly one line in
        the codebase where "who is this token for?" is answered.

        ``code_id``, when given, records what was minted on the authorization-code
        row so a replay can revoke it (OAuth 2.1 §4.1.2.5).
        """
        async with self._scope() as session:
            access_raw, access_id = await self._mint_access_token(
                session, user_id=user_id, client_id=client_id, now=now
            )
            refresh_raw, refresh_id = await self._mint_refresh_token(
                session, user_id=user_id, client_id=client_id, scopes=scopes, now=now
            )
            if code_id is not None:
                await session.execute(
                    update(MCPOAuthCode)
                    .where(
                        MCPOAuthCode.id == code_id
                    )  # global-ok: primary key of the row just claimed
                    .values(minted_access_token_id=access_id, minted_refresh_token_id=refresh_id)
                )

        logger.info(
            "mcp_oauth_tokens_minted",
            grant=grant,
            client_id=client_id,
            user_id=user_id,
            access_token=mask_token(access_raw),
        )
        return OAuthToken(
            access_token=access_raw,
            token_type="Bearer",
            expires_in=int(ACCESS_TOKEN_TTL.total_seconds()),
            scope=" ".join(scopes),
            refresh_token=refresh_raw,
        )

    # ── /token (refresh_token grant) ─────────────────────────────────────────

    async def load_refresh_token(
        self, client: OAuthClientInformationFull, refresh_token: str
    ) -> PiperRefreshToken | None:
        token_hash = hash_credential(refresh_token)
        async with self._scope() as session:
            row = (
                await session.execute(
                    # global-ok: resolves owner from the credential's unique hash
                    select(MCPOAuthRefreshToken).where(
                        MCPOAuthRefreshToken.token_hash == token_hash
                    )
                )
            ).scalar_one_or_none()
            if row is None:
                logger.warning(
                    "mcp_oauth_refresh_refused",
                    reason=_Refusal.REFRESH_NOT_FOUND.value,
                    client_id=client.client_id,
                )
                return None
            if str(row.client_id) != str(client.client_id):
                logger.warning(
                    "mcp_oauth_refresh_refused",
                    reason=_Refusal.REFRESH_WRONG_CLIENT.value,
                    client_id=client.client_id,
                )
                return None
            if row.revoked_at is not None:
                logger.warning(
                    "mcp_oauth_refresh_refused",
                    reason=_Refusal.REFRESH_REVOKED.value,
                    client_id=client.client_id,
                )
                return None
            expires_at = _as_aware_utc(row.expires_at)
            return PiperRefreshToken(
                token=refresh_token,
                client_id=str(row.client_id),
                scopes=list(row.scopes or [RESOURCE_READ_SCOPE]),
                expires_at=int(expires_at.timestamp()) if expires_at else None,
                user_id=str(row.user_id),
            )

    async def exchange_refresh_token(
        self,
        client: OAuthClientInformationFull,
        refresh_token: PiperRefreshToken,
        scopes: list[str],
    ) -> OAuthToken:
        """Rotate: revoke the presented refresh token, mint a new pair for the
        SAME user the original consent bound.

        The owner comes from the stored row, re-read inside the rotating
        transaction — the same discipline as the code exchange. A refresh token is
        a carrier of an identity already established at consent time; it can never
        name a different one.
        """
        token_hash = hash_credential(refresh_token.token)
        now = datetime.now(timezone.utc)

        # Same two-scope split, same reason, as exchange_authorization_code: the
        # rotation must be durable before the mint can fail, or a failed mint would
        # roll back the revocation and leave a refresh token replayable.
        async with self._scope() as session:
            rotated = await session.execute(
                update(MCPOAuthRefreshToken)
                .where(  # global-ok: claims one row BY THE CREDENTIAL's unique hash; the owner is the row's OUTPUT
                    MCPOAuthRefreshToken.token_hash == token_hash,
                    MCPOAuthRefreshToken.revoked_at.is_(None),
                )
                .values(revoked_at=now)
            )
            rotated_one = bool(rotated.rowcount)
        if not rotated_one:
            logger.warning(
                "mcp_oauth_refresh_refused",
                reason=_Refusal.REFRESH_REVOKED.value,
                client_id=client.client_id,
            )
            raise TokenError(
                error="invalid_grant", error_description="refresh token is no longer valid"
            )

        # Read the rotated row as a detached snapshot, decide outside the scope, and
        # raise outside it too (the frozen-dataclass constraint documented on
        # exchange_authorization_code applies identically here).
        async with self._scope() as session:
            row = (
                await session.execute(
                    # global-ok: same single-credential lookup as load_refresh_token
                    select(MCPOAuthRefreshToken).where(
                        MCPOAuthRefreshToken.token_hash == token_hash
                    )
                )
            ).scalar_one_or_none()
            owner_id = str(row.user_id) if row is not None and row.user_id else None
            row_client_id = str(row.client_id) if row is not None else None
            row_scopes = list(row.scopes or []) if row is not None else []
            row_expires_at = _as_aware_utc(row.expires_at) if row is not None else None

        if owner_id is None or row_client_id != str(client.client_id):
            logger.warning(
                "mcp_oauth_refresh_refused",
                reason=_Refusal.REFRESH_WRONG_CLIENT.value,
                client_id=client.client_id,
            )
            raise TokenError(
                error="invalid_grant", error_description="refresh token is no longer valid"
            )
        if row_expires_at is not None and row_expires_at <= now:
            logger.warning(
                "mcp_oauth_refresh_refused",
                reason=_Refusal.REFRESH_EXPIRED.value,
                client_id=client.client_id,
            )
            raise TokenError(error="invalid_grant", error_description="refresh token has expired")

        return await self._mint_pair(
            grant="refresh_token",
            user_id=owner_id,
            client_id=str(client.client_id),
            scopes=list(scopes or row_scopes or [RESOURCE_READ_SCOPE]),
            now=now,
        )

    # ── /revoke ──────────────────────────────────────────────────────────────

    async def load_access_token(self, token: str) -> AccessToken | None:
        """Load an OAuth-minted access token — for the REVOCATION endpoint only.

        ⚠️ This is NOT the resource server's verification path. The MCP app
        verifies bearer tokens with ``MCPTokenVerifier`` (unit 1), whose
        ``AccessToken.client_id`` deliberately carries the **user id** so
        ``current_user_id()`` can read it back. ``RevocationHandler``, by contrast,
        compares ``token.client_id`` against the authenticated **OAuth client**,
        so this method returns the client id recovered from the row's
        ``oauth:<client_id>`` label. Two different consumers, two correct answers,
        no shared code path — stated here because the field name is the same and a
        future reader WILL wonder.
        """
        token_hash = hash_credential(token)
        async with self._scope() as session:
            row = (
                await session.execute(
                    # global-ok: resolves the row from the credential's unique hash
                    select(MCPAccessToken).where(MCPAccessToken.token_hash == token_hash)
                )
            ).scalar_one_or_none()
            if row is None or row.revoked_at is not None:
                return None
            label = str(row.label or "")
            if not label.startswith(OAUTH_LABEL_PREFIX):
                # Operator-minted (unit 1) token: not an OAuth client's to revoke.
                return None
            expires_at = _as_aware_utc(row.expires_at)
            return AccessToken(
                token=token,
                client_id=label[len(OAUTH_LABEL_PREFIX) :],
                scopes=[RESOURCE_READ_SCOPE],
                expires_at=int(expires_at.timestamp()) if expires_at else None,
            )

    async def revoke_token(self, token: Any) -> None:
        """Revoke an access or refresh token (RFC 7009). Idempotent by shape: a
        row already revoked is simply re-stamped to the same effect, and an unknown
        token is a no-op, exactly as the RFC requires."""
        now = datetime.now(timezone.utc)
        token_hash = hash_credential(token.token)
        async with self._scope() as session:
            if isinstance(token, RefreshToken):
                await session.execute(
                    update(MCPOAuthRefreshToken)
                    .where(  # global-ok: identified by the credential's unique hash
                        MCPOAuthRefreshToken.token_hash == token_hash,
                        MCPOAuthRefreshToken.revoked_at.is_(None),
                    )
                    .values(revoked_at=now)
                )
            else:
                await session.execute(
                    update(MCPAccessToken)
                    .where(  # global-ok: identified by the credential's unique hash
                        MCPAccessToken.token_hash == token_hash,
                        MCPAccessToken.revoked_at.is_(None),
                    )
                    .values(revoked_at=now)
                )
        logger.info("mcp_oauth_token_revoked", token=mask_token(token.token))

    # ── Minting helpers (the only two places a credential is created) ────────

    async def _mint_access_token(
        self, session: AsyncSession, *, user_id: str, client_id: str, now: datetime
    ) -> tuple[str, uuid.UUID]:
        """Write an ``mcp_access_tokens`` row — unit 1's table, unit 1's verifier.

        No second token format and no second verification path: an OAuth-minted
        credential and an operator-minted one are the same kind of row, which is
        why ``MCPTokenVerifier`` needed no change for unit 4.
        """
        raw = ACCESS_TOKEN_PREFIX + secrets.token_urlsafe(32)
        token_id = uuid.uuid4()
        session.add(
            MCPAccessToken(
                id=token_id,
                user_id=uuid.UUID(user_id),
                token_hash=hash_credential(raw),
                label=f"{OAUTH_LABEL_PREFIX}{client_id}",
                created_at=now,
                expires_at=now + ACCESS_TOKEN_TTL,
            )
        )
        return raw, token_id

    async def _mint_refresh_token(
        self,
        session: AsyncSession,
        *,
        user_id: str,
        client_id: str,
        scopes: list[str],
        now: datetime,
    ) -> tuple[str, uuid.UUID]:
        raw = REFRESH_TOKEN_PREFIX + secrets.token_urlsafe(32)
        token_id = uuid.uuid4()
        session.add(
            MCPOAuthRefreshToken(
                id=token_id,
                token_hash=hash_credential(raw),
                client_id=client_id,
                user_id=uuid.UUID(user_id),
                scopes=list(scopes),
                created_at=now,
                expires_at=now + REFRESH_TOKEN_TTL,
            )
        )
        return raw, token_id

    async def _revoke_credentials_minted_for_code(self, code_hash: str) -> None:
        """OAuth 2.1 §4.1.2.5: on a code replay, revoke what the first exchange
        issued. Finds the code row's recorded ``minted_*`` ids and stamps both.

        Its OWN transaction, committed before the caller raises ``TokenError`` — in
        a shared scope the raise would roll this revocation back and the spec's
        requirement would be satisfied only in the logs.
        """
        now = datetime.now(timezone.utc)
        async with self._scope() as session:
            row = (
                await session.execute(
                    # global-ok: identified by the credential's unique hash
                    select(MCPOAuthCode).where(MCPOAuthCode.code_hash == code_hash)
                )
            ).scalar_one_or_none()
            if row is None:
                return
            if row.minted_access_token_id is not None:
                await session.execute(
                    update(MCPAccessToken)
                    .where(
                        MCPAccessToken.id == row.minted_access_token_id
                    )  # global-ok: primary key
                    .values(revoked_at=now)
                )
            if row.minted_refresh_token_id is not None:
                await session.execute(
                    update(MCPOAuthRefreshToken)
                    .where(  # global-ok: primary key
                        MCPOAuthRefreshToken.id == row.minted_refresh_token_id
                    )
                    .values(revoked_at=now)
                )
            logger.warning(
                "mcp_oauth_code_replay_revoked_minted_tokens",
                user_id=str(row.user_id),
                client_id=str(row.client_id),
            )


def _is_acceptable_redirect_uri(uri: str) -> bool:
    """https anywhere, http only on loopback.

    A plain-http redirect to a remote host would hand an authorization code to the
    network; loopback http is the documented native-client case (RFC 8252 §7.3).
    """
    from urllib.parse import urlparse

    parsed = urlparse(uri)
    if parsed.scheme == "https":
        return True
    if parsed.scheme == "http" and (parsed.hostname in ("localhost", "127.0.0.1", "::1")):
        return True
    return False
