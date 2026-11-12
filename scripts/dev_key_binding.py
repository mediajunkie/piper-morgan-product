"""Bind the DEVELOPER's own LLM keys for an in-process script run (#1812 aftermath, #2340).

Since #1809/#1812 the LLM legs spend ONLY a key bound in the request context
(``services.llm.request_key.request_api_key``); the designated-operator /
server-key fallback that scripts silently relied on is gone. Every script that
routes or classifies in-process (the Inversion instruments, the rule-7 screens,
any judge or retest harness) binds its keys here, the way a request binds a
user's keys.

Where the keys come from (#2340, Arch's ruling of 2026-11-11, after xian's rule
that nothing a seat runs reads his login keychain without his permission):

1. ``PIPER_CREDENTIAL_STORE`` must be set, to ``db``. Unset, the app's own
   provider selection reads the OS keychain during a call (the consent and
   default-provider slots, and the server slot of any unbound provider), so an
   environment key alone does not keep the run out of the keychain. The binder
   never sets the variable itself. ``keychain`` set explicitly is xian's own
   permission; a seat does not set it.
2. Each named provider's key is taken from the environment
   (``ANTHROPIC_API_KEY`` / ``OPENAI_API_KEY``, named on the command line after
   the ``env -u`` flags), else from ``KeychainService``, which under ``db`` is
   the encrypted database store.
3. A named provider with no key refuses before the first call.

Only the providers the run names are bound. A call that lands on any other
provider raises ``UnboundLLMKeyError`` at the spend chokepoint (#1809), so a run
asked for Anthropic stops when Anthropic refuses. It does not carry on against
OpenAI.

Usage::

    from dev_key_binding import developer_keys_bound

    with developer_keys_bound(providers=("anthropic",)):
        asyncio.run(run(...))
"""

from __future__ import annotations

import contextlib
import os
import sys
from typing import Dict, Iterator, Optional, Sequence

KNOWN_PROVIDERS = ("anthropic", "openai")
_ENV_VAR = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY"}
_ALLOWED_STORES = ("db", "keychain")


def providers_from_flag(provider: Optional[str]) -> tuple[str, ...]:
    """The ``providers=`` value for a script with a ``--provider`` flag.

    No flag means no provider named, which the binder refuses: a run says
    which account it spends on.
    """
    return (provider,) if provider else ()


def pop_provider_flag(argv: list[str]) -> Optional[str]:
    """Take ``--provider NAME`` (or ``--provider=NAME``) out of ``argv`` and return NAME.

    For the scripts whose own argument parsing runs inside the bound block.
    """
    for i, arg in enumerate(argv):
        if arg == "--provider" and i + 1 < len(argv):
            name = argv[i + 1]
            del argv[i : i + 2]
            return name
        if arg.startswith("--provider="):
            del argv[i]
            return arg.split("=", 1)[1]
    return None


def planned_calls_line(calls: int, providers: Sequence[str], what: str = "model calls") -> str:
    """The line a script prints before its first call (#2340 ask 3)."""
    named = ", ".join(providers) if providers else "no provider named"
    return f"PLANNED: {calls} {what} on {named}. Nothing has been sent yet."


def _refuse(message: str) -> None:
    sys.exit(f"dev_key_binding: {message}")


def _developer_keys(providers: Sequence[str]) -> Dict[str, str]:
    """Resolve a key for each named provider; exit before any call if one is missing."""
    if not providers:
        _refuse(
            "no provider named. Pass --provider anthropic or --provider openai: a run "
            "binds only the provider it asks for, so a refusal stops it instead of "
            "switching it to another account (#2340)."
        )
    unknown = [p for p in providers if p not in KNOWN_PROVIDERS]
    if unknown:
        _refuse(f"unknown provider {unknown!r}; known: {', '.join(KNOWN_PROVIDERS)}.")

    store = os.getenv("PIPER_CREDENTIAL_STORE", "").strip().lower()
    if store not in _ALLOWED_STORES:
        _refuse(
            "PIPER_CREDENTIAL_STORE is not set. Set PIPER_CREDENTIAL_STORE=db and name a "
            "key on the command line (ANTHROPIC_API_KEY=… or OPENAI_API_KEY=…, after the "
            "env -u flags), or store one in the database store. Do not use the keychain: "
            "nothing a seat runs reads xian's login keychain without his permission "
            "(2026-11-11), and with the store unset the app reads it during a call. "
            "Refusing before the first call."
        )

    found: Dict[str, str] = {}
    missing = []
    for provider in providers:
        key = os.getenv(_ENV_VAR[provider], "")
        if key:
            found[provider] = key
        else:
            missing.append(provider)
    if missing:
        from services.infrastructure.keychain_service import get_keychain_service

        kc = get_keychain_service()
        for provider in missing:
            key = kc.get_api_key(provider)
            if isinstance(key, str) and key:
                found[provider] = key
    still_missing = [p for p in providers if p not in found]
    if still_missing:
        names = ", ".join(_ENV_VAR[p] for p in still_missing)
        _refuse(
            f"no key for {', '.join(still_missing)}. Name it on the command line ({names}=…, "
            f"after the env -u flags) or store it in the {store} store. Refusing to run an "
            "LLM script whose calls would refuse."
        )
    return found


@contextlib.contextmanager
def developer_keys_bound(
    *, providers: Sequence[str], require: bool = True
) -> Iterator[Dict[str, str]]:
    """Bind the developer's keys for ``providers``, and only those, for this block.

    ``require=False`` is for dry runs that make no model call: nothing is
    looked up and nothing is bound.
    """
    from services.llm.request_key import request_api_key

    keys = _developer_keys(tuple(providers)) if require else {}
    with request_api_key(keys):
        yield keys
