"""#1231 (WS-4) — the ONE place mapping a `DegradationReason` to user-facing "connect me"
nudge copy (Arch-ratified 2026-07-01: "unify the vocabulary, share a copy policy").

Generalizes `calendar_offer_policy`'s connect-me copy into a connector-agnostic,
reason-keyed policy: every honest-degrade consumer derives its nudge here rather than
inlining strings, so a new consumer can't forget the nudge or diverge the wording, and
CXO has a single surface to voice-pass.

Trust note (HOST / ADR-072 D5 transparency-when-gated): this copy is *how* Piper is
honest about what it can't do — it's a trust artifact, not incidental UX text.

Altitude: this is the intent/response layer's degrade-copy. The adapter layer carries the
same `DegradationReason` on its `DegradationResponse` result-type (services/mcp/consumer/
connector.py) — share the currency (the enum), not the container.
"""

from __future__ import annotations

from services.mcp.consumer.connector import DegradationReason

# Per-reason nudge templates. `{c}` = connector display name (e.g. "GitHub").
# Neutral phrasing so one line serves every surface (priority, project, …).
_NUDGES = {
    # CXO voice pass 2026-07-01 (mailboxes/lead/inbox/2026-07-01-cxo-copy-passes-1201-1231.md)
    DegradationReason.NOT_CONFIGURED: (
        "{c} isn't set up yet — connect it in Settings and I'll pull in your data."
    ),
    DegradationReason.CONNECT_REQUIRED: (
        "{c} isn't connected yet — connect it and I'll pull in your data."
    ),
    DegradationReason.STALE_TOKEN: (
        "Your {c} connection needs re-authorizing — reconnect it in Settings and I'll pick back up."
    ),
    DegradationReason.UNREACHABLE: (
        "I can't reach {c} right now — try again in a moment."
    ),
    DegradationReason.REPO_UNRESOLVED: (
        "I couldn't tell which repo you mean — link one to this project or try 'owner/name'."
    ),
    DegradationReason.RESOURCE_NOT_FOUND: ("I couldn't find that in {c}."),
}


def degrade_nudge(reason: DegradationReason, connector: str = "GitHub") -> str:
    """The user-facing "connect me / here's what's missing" line for a degradation reason.

    Returns '' for an unknown/None reason (caller then stays silent — but callers should
    only invoke this when they have a real reason, so silence here is a defensive default,
    not the honest-degrade path)."""
    template = _NUDGES.get(reason)
    return template.format(c=connector) if template else ""
