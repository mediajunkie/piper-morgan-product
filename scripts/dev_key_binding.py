"""Bind the DEVELOPER's own LLM keys for an in-process script run (#1812 aftermath).

Since #1809/#1812 the LLM legs spend ONLY a key bound in the request context
(``services.llm.request_key.request_api_key``); the designated-operator /
server-key fallback that scripts silently relied on is gone. Every script that
routes or classifies in-process — the Inversion instruments (phase-0 baseline,
phase-1 shadow score, phase-2 gate) and any judge/retest harness — therefore
died with 107/107 "the request context never bound a key" the first time it
ran after that change (found 2026-09-23 running the shadow score).

This helper is the honest replacement: it resolves the developer's own keys
from the OS keychain (the same ``KeychainService`` path the app uses, never
an env var) and binds them for the duration of the script's work, exactly the
way a request binds a user's keys. It never invents a key, never falls back,
and refuses loudly when the keychain holds nothing — a script with no key
should say so, not degrade into a fake verdict (m-44).

Usage::

    from scripts.dev_key_binding import developer_keys_bound

    with developer_keys_bound():
        asyncio.run(run(...))
"""

from __future__ import annotations

import contextlib
import sys
from typing import Dict, Iterator

_PROVIDERS = ("anthropic", "openai")


def _developer_keys() -> Dict[str, str]:
    from services.infrastructure.keychain_service import get_keychain_service

    kc = get_keychain_service()
    found: Dict[str, str] = {}
    for provider in _PROVIDERS:
        key = kc.get_api_key(provider)
        if isinstance(key, str) and key:
            found[provider] = key
    return found


@contextlib.contextmanager
def developer_keys_bound(*, require: bool = True) -> Iterator[Dict[str, str]]:
    """Bind the developer's keychain keys as the request binding for this block.

    ``require=True`` (default) exits the process with a clear message when no
    key resolves — every LLM call in the block would refuse anyway, and a
    100%-ERROR run is not a measurement.
    """
    from services.llm.request_key import request_api_key

    keys = _developer_keys()
    if require and not keys:
        sys.exit(
            "dev_key_binding: no anthropic/openai key in the OS keychain — nothing to bind. "
            "Provision via KeychainService (the service appends _api_key to account names; "
            "entries stored with the `security` CLI are invisible to the app). Refusing to "
            "run an LLM script whose every call would refuse."
        )
    with request_api_key(keys):
        yield keys
