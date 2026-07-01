"""Connector-agnostic target-resolution types (#1342, RECONNECT-WS3 Phase 2).

Arch ruling 2026-07-01 (decisions.log, ADR-070 family): target-selection-from-Piper-
config is an intent-layer boundary **adjacent** to the #1232 Connector protocol — it
SHARES the protocol's vocabularies but is a **separate resolution service, NOT a 5th
Connector method**. The protocol's ``resolve`` is resource-fetch-from-server;
``resolve_target`` is target-selection-from-config (pre-connector, zero MCP calls) —
two different altitudes, so "resolve" is not overloaded onto one interface.

``ResolutionSource`` is promoted here **as-is** (it was already connector-agnostic in
``services/integrations/github/repo_resolver.py``; ``repo_resolver`` now re-imports it
from here, keeping it importable there for back-compat). ``ResolvedTarget`` is the
connector-agnostic envelope; ``payload`` is the connector-specific resolved value
(e.g. ``ResolvedRepo`` for GitHub).

**Design-for-calendar-on-paper, build-GitHub-only** (m-40): a second connector impl
lands on demand, not speculatively. On paper, calendar resolves the same shape —
explicit calendar id → user-default calendar → primary — reusing ``ResolutionSource``
(``project``/``default_project`` become N/A for calendar; ``explicit``/``user_default``/
``env_var`` carry over) and returning ``ResolvedTarget(connector="calendar", ...)``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

# The per-call resolution paths, in precedence order. Connector-agnostic: every
# connector's target selection walks the same decision tree —
#   explicit → project → default_project → user_default → env_var → (miss).
# (For connectors without a project notion, project/default_project are simply
# never produced; the vocabulary is shared, the applicable subset differs.)
ResolutionSource = Literal["explicit", "project", "default_project", "user_default", "env_var"]


@dataclass(frozen=True)
class ResolvedTarget:
    """A resolved target selection, connector-agnostic (#1342).

    Attributes:
        source: which resolution path produced this result (the shared vocabulary).
        connector: the connector this target is for (e.g. ``"github"``, ``"calendar"``).
        payload: the connector-specific resolved value (e.g. a ``ResolvedRepo`` for
            GitHub). Typed ``Any`` per m-40 — one impl today; the concrete payload
            type is asserted at each connector's call site, not over-abstracted here.
    """

    source: ResolutionSource
    connector: str
    payload: Any
