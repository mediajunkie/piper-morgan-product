"""The evidence logger, ``piper.evidence`` (#2350, Arch's ruling of 2026-11-12).

The hosts run with the root logger at WARNING, so every ``info`` line is dropped
before the platform keeps it. Twice that made an absent line look like a clear answer
(#2335, #2337). Lowering the root would bring back library info noise, which once
leaked a key (2026-01-17). So operational evidence has its own logger:

- its level is INFO whatever the root's is;
- it writes through its own handler, so it works in a process that never configured
  logging (the MCP app), and the URL redaction filter is attached to the logger itself.
  (A filter on the root logger does not see records from other loggers; only records
  logged on the root pass through it.)

An evidence line is a low-volume event a seat will later cite as proof that something
happened: a pool coming up, a refresh pass and its outcomes, a status change. It
carries names, counts, ids and reason codes. Never a value: no token, URL, password or
person's content.

Use ``evidence("event_name", count=3)``. The event must be in ``EVIDENCE_EVENTS``;
``tests/unit/services/infrastructure/test_evidence_logger_2350.py`` pins the list and
every call site, so moving one back to a plain logger fails.
"""

from __future__ import annotations

import logging
import sys
from typing import Any

import structlog

from services.infrastructure.logging.url_redaction import URLRedactionFilter

EVIDENCE_LOGGER_NAME = "piper.evidence"

# Every event that goes through the evidence logger, with where it is emitted.
EVIDENCE_EVENTS = frozenset(
    {
        # services/cache/redis_factory.py: the Redis pool came up (host name only)
        "Redis connection pool initialized",
        # services/auth/token_blacklist.py: each start reseeded the revoked-token list
        "TokenBlacklist: Redis available",
        # services/mcp/server/rate_limit.py: which backend the MCP limit uses, once
        "mcp_rate_limit_backend_active",
        # services/mcp/consumer/github_app_refresh.py: the 30-minute refresh pass
        "github_app_background_refresh_pass",
        "github_app_grant_refreshed",
        "github_app_grant_refresh_raced_served_newer",
        # services/mcp/consumer/github_oauth_handler.py: GitHub refused a refresh
        "github_app_refresh_rejected",
    }
)

# A field whose NAME says it holds a value is dropped, and the drop is logged.
_VALUE_FIELD_WORDS = ("token", "secret", "password", "passwd", "authorization", "url", "key")
_ALLOWED_DESPITE_WORD = frozenset({"key_name", "key_count"})


def _is_value_field(name: str) -> bool:
    lowered = name.lower()
    if lowered in _ALLOWED_DESPITE_WORD:
        return False
    return any(word in lowered for word in _VALUE_FIELD_WORDS)


def configure_evidence_logger() -> logging.Logger:
    """Idempotent. INFO, its own stderr handler, the redaction filter, no propagation
    (so a line is written once, whatever the root has)."""
    log = logging.getLogger(EVIDENCE_LOGGER_NAME)
    log.setLevel(logging.INFO)
    log.propagate = False
    if not any(isinstance(f, URLRedactionFilter) for f in log.filters):
        log.addFilter(URLRedactionFilter())
    if not any(getattr(h, "piper_evidence_handler", False) for h in log.handlers):
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter("%(message)s"))
        handler.piper_evidence_handler = True  # type: ignore[attr-defined]
        log.addHandler(handler)
    return log


def evidence(event: str, **fields: Any) -> None:
    """Emit one evidence line. Never raises: a log call must not break its caller."""
    try:
        configure_evidence_logger()
        dropped = sorted(name for name in fields if _is_value_field(name))
        kept = {name: value for name, value in fields.items() if name not in dropped}
        log = structlog.get_logger(EVIDENCE_LOGGER_NAME)
        if event not in EVIDENCE_EVENTS:
            # Still emitted (losing evidence is worse), and flagged so it gets listed.
            kept["evidence_event_unlisted"] = True
        if dropped:
            kept["evidence_fields_dropped"] = dropped
        log.info(event, **kept)
    except Exception:  # pragma: no cover - logging must never take a caller down
        pass


configure_evidence_logger()
