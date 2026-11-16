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

The dollar cap (#2383, ADR-084 D2). A run that makes calls states ``max_usd``
before the first one, or the binder refuses to start. Inside the block the
provider legs keep a running total (``services/llm/spend_cap.py``) and refuse the
call that could take the run past the cap. The binder prints a ``PLANNED:`` line
on entry and a ``COST:`` line, from the provider's own token counts, on exit. It
never prints a key or the environment. A batch submit is not a live call: it is
bounded by ``router_batch.py submit --cap-usd`` before it is sent, and passes that
same figure here. A cap above $10.00 is refused unless the run passes
``approved_by``, the mail id of Exec's relay of xian's approval, which the
``PLANNED:`` line prints. A run in which any call was refused at the cap exits
non-zero when the block ends.

Usage::

    from dev_key_binding import developer_keys_bound

    with developer_keys_bound(providers=("anthropic",), max_usd=2.00, planned_calls=26):
        asyncio.run(run(...))
"""

from __future__ import annotations

import contextlib
import os
import re
import sys
from typing import Dict, Iterator, Optional, Sequence

KNOWN_PROVIDERS = ("anthropic", "openai")
# The most a seat's run may spend without asking (xian, 2026-11-16; ADR-084 D2,
# docs/internal/architecture/adrs/adr-084-seat-resources-are-separate-granted-once-and-bounded.md).
# A higher cap needs the mail id of Exec's relay of xian's approval.
PER_RUN_USD_WITHOUT_ASKING = 10.00
_MAIL_ID = re.compile(r"^01[0-9A-HJKMNP-TV-Z]{24}$")
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


def planned_calls_line(
    calls: Optional[int],
    providers: Sequence[str],
    what: str = "model calls",
    max_usd: Optional[float] = None,
    approved_by: Optional[str] = None,
) -> str:
    """The line a script prints before its first call (#2340 ask 3, #2383)."""
    named = ", ".join(providers) if providers else "no provider named"
    count = f"{calls} {what}" if calls is not None else f"{what}, count not stated"
    cap = f" Cap ${max_usd:.2f}." if max_usd is not None else ""
    if max_usd is not None and max_usd > PER_RUN_USD_WITHOUT_ASKING:
        cap += f" Above ${PER_RUN_USD_WITHOUT_ASKING:.2f} on approval {approved_by}."
    return f"PLANNED: {count} on {named}.{cap} Nothing has been sent yet."


def pop_approved_by_flag(argv: list[str]) -> Optional[str]:
    """Take ``--approved-by ID`` (or ``--approved-by=ID``) out of ``argv`` and return ID."""
    for i, arg in enumerate(argv):
        if arg == "--approved-by" and i + 1 < len(argv):
            value = argv[i + 1]
            del argv[i : i + 2]
            return value
        if arg.startswith("--approved-by="):
            del argv[i]
            return arg.split("=", 1)[1]
    return None


def pop_max_usd_flag(argv: list[str]) -> Optional[float]:
    """Take ``--max-usd N`` (or ``--max-usd=N``) out of ``argv`` and return N.

    For the scripts whose own argument parsing runs inside the bound block. A
    value that is not a number refuses here, before any call.
    """
    raw: Optional[str] = None
    for i, arg in enumerate(argv):
        if arg == "--max-usd" and i + 1 < len(argv):
            raw = argv[i + 1]
            del argv[i : i + 2]
            break
        if arg.startswith("--max-usd="):
            raw = arg.split("=", 1)[1]
            del argv[i]
            break
    if raw is None:
        return None
    try:
        return float(raw)
    except ValueError:
        _refuse(f"--max-usd takes a dollar figure, not {raw!r}.")
        return None


def _checked_cap(max_usd: Optional[float]) -> float:
    """The cap as a positive number, or a refusal before any call (#2383)."""
    if max_usd is None:
        _refuse(
            "no cap. Pass --max-usd with the most this run may spend, in dollars: a paid "
            "run states its cap before the first call and can't pass it (#2383, ADR-084 "
            "D2). Refusing before the first call."
        )
    if isinstance(max_usd, bool) or not isinstance(max_usd, (int, float)) or not max_usd > 0:
        _refuse(f"the cap must be a dollar figure above zero, not {max_usd!r}.")
    return float(max_usd)  # type: ignore[arg-type]


def _checked_approval(cap_usd: float, approved_by: Optional[str]) -> None:
    """A cap above the per-run figure needs the id of Exec's relay of xian's approval."""
    if cap_usd <= PER_RUN_USD_WITHOUT_ASKING:
        return
    if not approved_by:
        _refuse(
            f"a cap of ${cap_usd:.2f} is above the ${PER_RUN_USD_WITHOUT_ASKING:.2f} a run may "
            "spend without asking (ADR-084 D2). Ask xian through Exec, then pass "
            "--approved-by with the mail id of Exec's relay of his approval. Refusing "
            "before the first call."
        )
    if not _MAIL_ID.match(approved_by or ""):
        _refuse(
            "--approved-by takes the mail id of Exec's relay (26 characters, starting 01), "
            f"not {approved_by!r}."
        )


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
    *,
    providers: Sequence[str],
    max_usd: Optional[float] = None,
    planned_calls: Optional[int] = None,
    approved_by: Optional[str] = None,
    announce: bool = True,
    require: bool = True,
) -> Iterator[Dict[str, str]]:
    """Bind the developer's keys for ``providers``, and only those, for this block.

    ``max_usd`` is the run's dollar cap and is required when the run makes calls
    (#2383). ``planned_calls`` is the count for the ``PLANNED:`` line, when the
    script knows it. ``approved_by`` is the mail id of Exec's relay of xian's
    approval, required for a cap above ``PER_RUN_USD_WITHOUT_ASKING``. A run in
    which the cap refused any call exits non-zero here, whatever caught the
    refusal on the way: its rows are not counted. ``announce=False`` is for a batch submit, which prints its
    own two lines. ``require=False`` is for dry runs that make no model call:
    nothing is looked up, nothing is bound and no cap is needed.
    """
    from services.llm.request_key import request_api_key
    from services.llm.spend_cap import spend_cap

    if not require:
        with request_api_key({}):
            yield {}
        return

    cap_usd = _checked_cap(max_usd)
    _checked_approval(cap_usd, approved_by)
    keys = _developer_keys(tuple(providers))
    if announce:
        print(
            planned_calls_line(
                planned_calls, tuple(providers), max_usd=cap_usd, approved_by=approved_by
            ),
            flush=True,
        )
    with spend_cap(cap_usd) as cap:
        try:
            with request_api_key(keys):
                yield keys
        finally:
            if announce:
                print(cap.cost_line(), flush=True)
            if cap.refused:
                # Whatever caught the refusal in between, the run did not finish.
                _refuse(
                    f"the run was stopped at its ${cap_usd:.2f} cap: {cap.refused} calls were "
                    "refused and not sent. The run is incomplete; do not count its rows."
                )
