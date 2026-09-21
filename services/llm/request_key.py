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

#1809 (2026-09-18): **the DEFAULT is inverted.** PM ruled the server key "is not a real
concept" (#1812, decisions.log 2026-09-14 ×2), so the resolver-level refusals above are no
longer enough: they only guard entry points that CALL the resolver. The ContextVar default
is now an UNBOUND sentinel, and the spend chokepoints **raise ``UnboundLLMKeyError`` when
nothing was bound** instead of returning the server's client. A path that forgets to bind
now fails loudly instead of billing the operator.

#1819 (2026-09-18): **the binding is PER-PROVIDER.** #1809 inverted the Anthropic
chokepoint, but ``_openai_complete`` / ``_gemini_complete`` still read the server's own
long-lived clients with no per-request path at all, and the KG embedding function read
the server's OpenAI key straight from the keychain — three spend surfaces outside the
inversion. The ContextVar now holds a provider-keyed mapping (a plain ``str`` binding
normalizes to ``{REQUEST_KEY_PROVIDER: key}``, so every #1162/#1809 call site is
unchanged), and ``request_spend_key(provider)`` is the ONE decision every leg and the
embedding path share: bound key for THAT provider → spend it; anything else →
``UnboundLLMKeyError``. A key bound for one provider never makes another provider
spendable (#1815's constraint, now enforced at the chokepoint rather than merely at
the availability gate).

#1812 steps 5–6 (2026-09-21): **the transitional operator seam is GONE.** #1807 had left
one double-gated server-key path for a designated operator principal; PM then ruled
their own account has normal-account semantics (decisions.log 2026-09-19), which removed
the last principal that seam could have served. ``PIPER_OPERATOR_SERVER_KEY``, the
resolver's operator rung, and the explicit ``None`` binding are all deleted; binding
``None`` now raises at bind time. There is no path — gated or otherwise — to a
product-owned credential. **Every LLM spend is the acting user's own key, resolved per
request, or an honest refusal.** ``request_spend_key`` is str-or-raise.

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
from contextvars import ContextVar
from typing import Any, Awaitable, Callable, Dict, Iterator, Mapping, Optional, Union


class _UnboundType:
    """#1809 sentinel: NOTHING was ever bound in this context.

    Before #1809 the ContextVar default was ``None`` and ``None`` meant "use the
    server's configured key" — so unbound and operator-authorized were the same
    value, and any path that forgot to bind silently spent the operator's key.
    #1812 step 5 removed the operator concept entirely, so the sentinel's only
    remaining job is making *forgetting to bind* a loud error at the chokepoint.
    """

    def __repr__(self) -> str:  # pragma: no cover - debugging nicety
        return "<UNBOUND request key (#1809)>"


_UNBOUND = _UnboundType()

# #1809 INVERSION: default is the UNBOUND sentinel, and unbound is an ERROR at the
# spend chokepoints (`UnboundLLMKeyError`), never a fallback to the server's key.
# PM ruled the server key "is not a real concept" (#1812, decisions.log 2026-09-14 ×2).
# #1819: the bound value is a provider-keyed mapping (str bindings normalize to
# {REQUEST_KEY_PROVIDER: key} at set time in `request_api_key`).
# #1812 step 5: `None` is no longer a representable binding — the operator seam it
# encoded is deleted, and `request_api_key(None)` raises at bind time.
_user_api_key: ContextVar[Union[Dict[str, str], _UnboundType]] = ContextVar(
    "user_api_key", default=_UNBOUND
)

# The provider the HEADER's key belongs to. The `X-User-Api-Key` header is documented
# as the caller's Anthropic key, so a plain-``str`` binding (the #1162 form every
# pre-#1819 call site uses) normalizes to this provider. Named here so readers assert
# that binding in ONE place instead of each re-hardcoding "anthropic" on their own
# authority. #1819: stored-key resolution is per-provider (each `user_api_keys` row
# names its provider), so OTHER providers bind through the mapping form of
# `request_api_key`, not through this constant.
REQUEST_KEY_PROVIDER = "anthropic"

# Providers whose completion leg can build a FRESH per-request client from a bound key
# (#1819). Anthropic: `anthropic_client_for_request`. OpenAI: `_openai_complete`
# constructs `OpenAI(api_key=...)` per call. Gemini is deliberately ABSENT:
# `google.generativeai` configures credentials process-globally (`genai.configure`),
# so honoring a per-request Gemini key would risk serving request A under request B's
# credential — the leg refuses instead (see `LLMClient._gemini_complete`).
PER_REQUEST_CLIENT_PROVIDERS = frozenset({"anthropic", "openai"})


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
    """Raised when a caller IS authenticated but has no key of their own (#1807;
    unconditional since #1812 step 5 — there is no operator exemption).

    The remediation is *add your LLM key* — NOT "sign in" (they already are) and NOT
    "try again" (retrying without a key changes nothing). Callers catch this and say so.
    """


class UnboundLLMKeyError(LLMKeyRequiredError):
    """Raised when the LLM client is reached with NO key binding at all (#1809).

    The fourth member of the family, and the one that exists so that FORGETTING is an
    error instead of a spend. Its siblings are raised by the resolver — a path that
    deliberately asked "whose key is this?". This one is raised by the CONSUMER
    (``request_spend_key`` and its callers) when no path ever asked: no header, no
    stored-key fetch — the request simply arrived at the client unbound.

    Before #1809, unbound meant "use the server's configured key": default-open, so a
    new entry point that skipped the resolver silently billed the operator and nothing
    failed. Now it refuses. The remediation depends on who you are:
      - a USER seeing this copy → add your own key (same as #1807's sibling; the
        message deliberately matches the "no key configured" error-table entry).
      - a DEVELOPER whose new code path raises this → bind the acting user's key
        (``resolve_request_api_key`` → ``request_api_key(...)``) before calling the
        LLM; do NOT catch-and-fallback.
    """


class ConsentUnreadableError(LLMKeyRequiredError):
    """Raised when the #946/#1415 CONSENT list could not be READ (#1816).

    The third member of this family, and the one whose truth conditions differ
    most from its siblings — which is exactly why it needs its own type and its
    own copy rather than inheriting theirs (CXO, 2026-09-15):

      - anonymous (#1320)      → "sign in, or bring a key"
      - authenticated (#1807)  → "add your own key"; never "try again"
      - HERE                   → the user may well HAVE a key. What failed is the
        read of which providers they authorized. Telling them to add a key
        recommends a known-failing action (the #1108 shape). And unlike its
        siblings, "try again in a moment" IS admissible here: a store hiccup is
        genuinely transient, where a missing key is not.

    Why it is a refusal at all, rather than a degradation (#1815 Gap 2, Arch
    ruling 2026-09-15 §3): #1415's F1 closed state was "narrow to the
    server-default provider", which assumed a server that owns a key. PM ruled
    (#1812) the server key is "not a real concept, not to be supported in any
    sense", so that degradation is now incoherent. **Fail-closed means closed,
    not quietly reassigned to the operator's key.**
    """


def get_request_api_key(provider: str = REQUEST_KEY_PROVIDER) -> Optional[str]:
    """The current request's user-supplied key for ``provider``, or None.

    Non-raising peek for readers that ask "did this request bring its OWN key?"
    (#1814's ``get_api_key`` step 0 and #1815's ``_is_provider_configured``). The
    SPEND decision lives in ``request_spend_key``, which raises where this returns
    ``None``.

    #1819: provider-keyed. The no-argument form keeps the #1162/#1809 contract
    (the header's provider, ``REQUEST_KEY_PROVIDER``); a key bound for one provider
    is never reported for another.
    """
    value = _user_api_key.get()
    if isinstance(value, dict):
        key = value.get(provider)
        return key if isinstance(key, str) and key else None
    return None


@contextlib.contextmanager
def request_api_key(key: Union[str, Mapping[str, Optional[str]]]) -> Iterator[None]:
    """Bind the per-request user API key(s) for the duration of the block, then reset.

    #1819 accepted forms:
      - ``str``      → the header's key; normalizes to ``{REQUEST_KEY_PROVIDER: key}``
                       (every pre-#1819 call site keeps its exact behavior).
      - ``Mapping``  → provider-keyed binding (e.g. the user's stored anthropic AND
                       openai keys). Blank/None values are dropped; an empty result
                       binds NOTHING SPENDABLE — every leg refuses.

    #1812 step 5: ``None`` (and blank ``""``) — formerly the explicit
    designated-operator binding — now **raises ``ValueError`` at bind time**. The
    operator concept is deleted; nothing legitimately produces a ``None`` binding,
    so accepting one silently would only let a stale caller re-encode the seam. A
    caller with no keys binds an empty mapping (refuses at spend) or binds nothing.

    The reset in the ``finally`` guarantees the binding never outlives the request —
    no cross-request leak, and the context returns to UNBOUND (refuse), not to any
    fallback.
    """
    if key is None or key == "":
        raise ValueError(
            "request_api_key(None) is no longer a valid binding: the designated-"
            "operator seam it encoded was deleted by #1812 step 5. Bind the acting "
            "user's own key(s), or bind nothing and let the spend chokepoint refuse."
        )
    normalized: Dict[str, str]
    if isinstance(key, str):
        normalized = {REQUEST_KEY_PROVIDER: key}
    else:
        normalized = {p: k for p, k in key.items() if isinstance(k, str) and k}
    token = _user_api_key.set(normalized)
    try:
        yield
    finally:
        _user_api_key.reset(token)


def request_spend_key(provider: str) -> str:
    """The credential this request is entitled to spend on ``provider`` — or REFUSE.

    #1819: the single spend decision every provider leg shares (Anthropic reaches it
    through ``anthropic_client_for_request``; ``_openai_complete``, ``_gemini_complete``
    and the KG embedding function call it directly). #1812 step 5: **str-or-raise** —
    the transitional "return ``None`` for the operator's server credential" arm is
    deleted with the operator concept itself:

      - a key is bound for THIS provider → return it (billed to the user, as ever).
        A key bound for a DIFFERENT provider does not count — #1815's constraint,
        enforced at the chokepoint.
      - anything else (UNBOUND, or bound-but-not-for-this-provider) →
        ``UnboundLLMKeyError``. Forgetting is an error, not a spend (#1809).

    Kept tiny + pure so every leg is unit-testable without standing up the full
    LLM client.

    Raises:
        UnboundLLMKeyError: no binding usable for ``provider``.
    """
    bound = _user_api_key.get()
    if isinstance(bound, dict):
        key = bound.get(provider)
        if isinstance(key, str) and key:
            return key
        raise UnboundLLMKeyError(
            f"No LLM key configured for provider '{provider}' on this call: the "
            "request bound no key for this provider, and a key bound for another "
            "provider is never spendable across providers (#1815/#1819). Bind the "
            "acting user's own key for this provider, or refuse honestly."
        )
    raise UnboundLLMKeyError(
        "No LLM key configured for this call: the request context never bound a key, "
        "and unbound no longer falls back to the server's own key (#1809). Bind the "
        "acting user's key (resolve_request_api_key -> request_api_key) before "
        "reaching the LLM, or refuse honestly."
    )


def provider_spend_entitled(provider: str) -> bool:
    """Non-raising peek: would ``request_spend_key(provider)`` succeed right now,
    AND does the leg have a client path to spend it?

    For the availability gate (`LLMClient._is_provider_configured`), which must
    answer per-REQUEST (#1815) without raising: a bound key for ``provider`` counts
    only when the leg can actually build a per-request client from it
    (``PER_REQUEST_CLIENT_PROVIDERS``). A bound Gemini key is NOT spendable (no
    per-request client path) — reporting it available would route the fallback
    loop into a guaranteed refusal. Unbound → False (#1812 step 5 removed the
    operator arm; there is no server client to be entitled to).
    """
    bound = _user_api_key.get()
    if isinstance(bound, dict):
        key = bound.get(provider)
        return provider in PER_REQUEST_CLIENT_PROVIDERS and isinstance(key, str) and bool(key)
    return False


def anthropic_client_for_request() -> Any:
    """Return a fresh Anthropic client keyed to the current request — or REFUSE.

    The single Anthropic spend chokepoint (`LLMClient._anthropic_complete` is its
    only production caller, and the only Anthropic construction site in the tree).
    #1812 step 5: the ``server_client`` parameter is GONE — with the operator seam
    deleted there is no server client to fall back to, so the fresh per-request
    client (billed to the acting user's bound key) is the only path. UNBOUND
    raises ``UnboundLLMKeyError`` (#1809): forgetting is an error, not a spend.

    Raises:
        UnboundLLMKeyError: no Anthropic key bound on this request.
    """
    key = request_spend_key(REQUEST_KEY_PROVIDER)
    from anthropic import Anthropic

    return Anthropic(api_key=key)


async def resolve_request_api_key(
    header_key: Optional[str],
    user_id: Optional[str],
    fetch_stored: Optional[Callable[[str], Awaitable[Optional[str]]]],
) -> str:
    """Resolve the per-request LLM key: header > stored > refuse (#1185, #1320,
    #1807). #1812 step 5: the designated-operator rung is deleted — this now
    returns a key or raises, never ``None``.

    Priority:
    - ``header_key`` (the ``X-User-Api-Key`` header — Claude Desktop BYOC) wins, and
      the DB is never touched: the user supplied an explicit per-call key. Works
      whether or not the caller is authenticated (BYOC needs no login).
    - else, for an authenticated ``user_id`` (truthy — the caller has a valid
      login): ``fetch_stored(user_id)`` resolves the user's *stored* key if present
      (hosted web).
    - else, still authenticated but with no key of their own: **raise**
      ``UserLLMKeyRequiredError``. Authentication establishes WHO a caller is, not
      that anyone else pays for their calls (#1807, unconditional since #1812).
    - else (unauthenticated AND no header key — a fully anonymous caller):
      **raise** ``AnonymousLLMKeyRequiredError`` (#1320).

    ``fetch_stored`` is injected so this module stays DB-free and unit-testable
    without a database; ``web/utils/llm_key.py`` supplies the real DB-backed
    fetcher.

    A blank header is treated as absent (falls through to the next step). The
    resolved key feeds ``request_api_key(...)`` — same ContextVar, same security
    properties (per-request, reset-in-finally, never logged).

    Raises:
        UserLLMKeyRequiredError: authenticated caller, no key of their own (#1807).
        AnonymousLLMKeyRequiredError: unauthenticated caller, no header key (#1320).
    """
    if header_key:
        return header_key
    if user_id:
        stored = await fetch_stored(user_id) if fetch_stored is not None else None
        if stored:
            return stored
        raise UserLLMKeyRequiredError(
            "Authenticated caller has no LLM key of their own — refusing to spend "
            "anyone else's key (#1807/#1812)."
        )
    raise AnonymousLLMKeyRequiredError(
        "No login and no X-User-Api-Key header — refusing to fall back to the "
        "server's own key for an anonymous caller (#1320)."
    )
