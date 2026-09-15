"""#1162 BYOC credential decoupling — per-request, user-supplied LLM API key.

A hosted-BYOC user supplies their OWN Anthropic key (Claude Desktop env →
``X-User-Api-Key`` header on the request to ``/api/v1/intent``). The route binds it
into a request-scoped ``ContextVar``; the LLM client uses it for *that request's*
Anthropic calls instead of the server's configured key, falling back to the server
key when absent for an *authenticated* caller (PM's own use).

Why this unblocks distribution (#1162): with users paying for their own LLM calls,
the hosted server no longer has to authenticate them to use it — the static
bearer-token gate (the thing 401-ing external testers) can come off.

#1320 (2026-07-01): the Caddy edge gate above was in fact removed (2026-06-29). The
memo that shipped alongside #1162 (2026-06-17, mailboxes/pa/read/memo-lead-to-pa-cc-
pm-caddy-gate-issue-explainer-plus-fallback-security-interaction-2026-06-17.md)
flagged that the gate and this fallback were load-bearing *together*: the server-key
fallback is safe only because the gate restricted who could reach it. Remove the
gate without the paired server-side change, and any fully anonymous caller (no
login, no header key) silently bills the server's own key. That pairing hadn't
shipped — fixed here: ``resolve_request_api_key`` now raises
``AnonymousLLMKeyRequiredError`` for the unauthenticated+keyless case instead of
returning ``None``. Authenticated callers are unaffected (still fall back to the
server key when logged in but keyless — that's the intended "PM's own use" path).

#1807 (2026-09-14): **the sentence above was the remaining half of the hole, and it is
now closed.** #1320 shipped the anonymous half of the paired fix because at the time the
only authenticated identity was PM. It is not any more: every alpha tester who logs in
and skips the key step is, by construction, a known authenticated identity — and was
silently billing the operator's balance. **Authentication establishes WHO a caller is; it
does not establish that they may spend the operator's money.** An authenticated caller
with no key of their own now raises ``UserLLMKeyRequiredError`` instead of returning
``None``.

The only surviving server-key path is an explicitly **designated operator principal**,
and it is gated twice, both default-OFF:
  1. ``PIPER_OPERATOR_SERVER_KEY`` must be opted in (env, absent ⇒ off — the
     ``PIPER_DEMO_PLUGIN`` operator-opt-in idiom, #1690); AND
  2. the caller must BE the configured PM/operator principal, resolved through the
     existing convention (``resolve_pm_owner_id``: env ``PIPER_PM_USER_ID`` → the "PM
     Identity" section of ``config/PIPER.user.md``; #1260, ADR-071 D7).
Two knobs rather than one on purpose: identity config alone must never confer *spending*
authority, or a machine that merely names its PM for doc provenance would silently
acquire it. ``is_operator`` is injected (this module stays DB-free); omitting it refuses,
so every caller that has not deliberately wired an operator check is fail-closed.

PM's directive is stricter than this default and may make the flag moot: *"there
shouldn't be any key that belongs to the product itself that isn't paid for by somebody
else."* Whether PM's own use should also require a stored key is a product decision left
open on #1807 — the flag is the seam where that decision lands, not a claim that it is
settled.

Security properties (this is credential handling — keep them):
- The key lives ONLY in the ContextVar for the request's duration and is **reset in
  a finally** (`request_api_key` context manager) → it never outlives the request.
- ContextVars are per-asyncio-task, so concurrent requests can't leak keys to each
  other (each request is its own task).
- The key is **never logged** and **never persisted** — it transits in the header
  (HTTPS at the edge) and is used in-memory for the one call.
- A blank/empty header binds nothing → falls through to the next resolution step.
"""

from __future__ import annotations

import contextlib
import os
from contextvars import ContextVar
from typing import Any, Awaitable, Callable, Iterator, Optional

# Default None = "no per-request key bound; use the server's configured key".
_user_api_key: ContextVar[Optional[str]] = ContextVar("user_api_key", default=None)

# #1807: the operator's own key is spendable ONLY when this is explicitly opted in.
# Absent ⇒ off, which is the hosted default (AC 2). Same shape as #1690's
# `PIPER_DEMO_PLUGIN` — an operator knob that must be *typed*, never inferred.
OPERATOR_SERVER_KEY_ENV = "PIPER_OPERATOR_SERVER_KEY"
_TRUTHY = {"1", "true", "yes", "on"}

# The provider the per-request key belongs to. It is an ANTHROPIC key by construction:
# `web/utils/llm_key.py` fetches the stored key for provider "anthropic", the
# `X-User-Api-Key` header is documented as the caller's Anthropic key, and
# `anthropic_client_for_request` below is its only consumer. Named here so readers of
# this ContextVar (#1814 added one in `LLMConfigService.get_api_key`) assert that
# binding in ONE place instead of each re-hardcoding "anthropic" on their own authority.
REQUEST_KEY_PROVIDER = "anthropic"


def operator_server_key_opted_in() -> bool:
    """True only when the operator explicitly allowed their own key to be spent (#1807).

    Deliberately env-only and DB-free so the default path costs nothing and cannot be
    turned on as a side effect of unrelated configuration.
    """
    return os.getenv(OPERATOR_SERVER_KEY_ENV, "").strip().lower() in _TRUTHY


class LLMKeyRequiredError(Exception):
    """Base: this request has no key it is entitled to use, so it must be refused
    rather than silently charged to the server's own key. Subclasses distinguish WHY,
    because the honest remediation differs and serving the wrong one is its own bug
    (#1520 is the worked example)."""


class AnonymousLLMKeyRequiredError(LLMKeyRequiredError):
    """Raised when a request has no authenticated user_id AND no X-User-Api-Key
    header (#1320) — the server's own key must never be used for a fully anonymous
    caller. Callers should catch this and return an honest, actionable message
    (sign in, or supply your own key) — never silently fall back to the server key."""


class UserLLMKeyRequiredError(LLMKeyRequiredError):
    """Raised when a caller IS authenticated but has no key of their own, and is not
    the designated operator principal (#1807).

    The remediation is *add your LLM key* — NOT "sign in" (they already are) and NOT
    "try again" (retrying without a key changes nothing). Callers catch this and say so.
    """


def get_request_api_key() -> Optional[str]:
    """The current request's user-supplied API key, or None (→ use the server key)."""
    return _user_api_key.get()


@contextlib.contextmanager
def request_api_key(key: Optional[str]) -> Iterator[None]:
    """Bind a per-request user API key for the duration of the block, then reset.

    A blank/None key binds None (falls back to the server key). The reset in the
    ``finally`` guarantees the key never outlives the request — no cross-request leak.
    """
    token = _user_api_key.set(key or None)
    try:
        yield
    finally:
        _user_api_key.reset(token)


def anthropic_client_for_request(server_client: Any) -> Any:
    """Return the Anthropic client to use for the current request.

    If the request bound a user-supplied key (BYOC), return a fresh client keyed to
    it; otherwise return the server's configured client. Kept tiny + pure so it's
    unit-testable without standing up the full LLM client.
    """
    user_key = get_request_api_key()
    if user_key:
        from anthropic import Anthropic

        return Anthropic(api_key=user_key)
    return server_client


async def resolve_request_api_key(
    header_key: Optional[str],
    user_id: Optional[str],
    fetch_stored: Optional[Callable[[str], Awaitable[Optional[str]]]],
    is_operator: Optional[Callable[[str], Awaitable[bool]]] = None,
) -> Optional[str]:
    """Resolve the per-request LLM key: header > stored > designated-operator (#1185,
    #1320, #1807). There is no "any authenticated user" rung any more.

    Priority:
    - ``header_key`` (the ``X-User-Api-Key`` header — Claude Desktop BYOC) wins, and
      the DB is never touched: the user supplied an explicit per-call key. Works
      whether or not the caller is authenticated (BYOC needs no login).
    - else, for an authenticated ``user_id`` (truthy — the caller has a valid
      login): ``fetch_stored(user_id)`` resolves the user's *stored* key if present
      (hosted web).
    - else, still authenticated but with no key of their own: ``is_operator(user_id)``
      decides. **True** → ``None``, i.e. the LLM client uses the server's configured
      key; this is the one remaining operator path and it is default-OFF (#1807).
      **False, or no checker injected at all** → **raise**
      ``UserLLMKeyRequiredError``. Omitting the checker refuses, so a caller that has
      not deliberately wired the operator path is fail-closed by construction.
    - else (unauthenticated AND no header key — a fully anonymous caller):
      **raise** ``AnonymousLLMKeyRequiredError`` (#1320).

    ``is_operator`` is injected for the same reason ``fetch_stored`` is: this module
    stays DB-free and unit-testable without a database. ``web/utils/llm_key.py`` is the
    one place that supplies the real, config-backed implementation.

    A blank header is treated as absent (falls through to the next step). The
    resolved key feeds ``request_api_key(...)`` — same ContextVar, same security
    properties (per-request, reset-in-finally, never logged).

    Raises:
        UserLLMKeyRequiredError: authenticated caller, no key of their own, not the
            designated operator (#1807).
        AnonymousLLMKeyRequiredError: unauthenticated caller, no header key (#1320).
    """
    if header_key:
        return header_key
    if user_id:
        stored = await fetch_stored(user_id) if fetch_stored is not None else None
        if stored:
            return stored
        if is_operator is not None and await is_operator(user_id):
            return None
        raise UserLLMKeyRequiredError(
            "Authenticated caller has no LLM key of their own and is not the "
            "designated operator — refusing to spend the server's key (#1807)."
        )
    raise AnonymousLLMKeyRequiredError(
        "No login and no X-User-Api-Key header — refusing to fall back to the "
        "server's own key for an anonymous caller (#1320)."
    )
