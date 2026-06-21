"""#1232 (RECONNECT WS-5) — the MCP-consumer Connector protocol (ADR-070 D5).

One contract every MCP-consumer adapter implements: ``connect`` / ``status`` /
``resolve`` / ``degrade``. Per ADR-070 D3 + Open-Q-5: the external MCP server owns the
OAuth/token lifecycle; ``connect()`` is a redirect+callback *orchestrator* that returns a
binding-or-``ConnectRequired`` — Piper stores bindings, never raw tokens. ``degrade()``
(ADR-070 D5; WS-4 made structural) is the honest-degradation contract: never silently
empty — an unconfigured/unresolvable connector says "connect me" / "here's what's missing".

The four **methods** are settled by ADR-070 D5. The **result-type shapes** below are
Lead-authored per ADR-070 Open-Q-4 (v1 — pending Arch review; may refine). Nothing consumes
this protocol yet; WS-3 (``resolve``) and WS-4 (``degrade``) build onto it next.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Optional, Protocol, runtime_checkable


class ConnectorStatusState(enum.Enum):
    """Health of a user's binding to a connector's MCP server (ADR-070 D5)."""

    BOUND = "bound"  # connected + healthy
    UNBOUND = "unbound"  # no binding — the user must connect
    UNREACHABLE = "unreachable"  # bound, but the MCP server isn't responding
    STALE = "stale"  # bound, but the token needs refresh


class DegradationReason(enum.Enum):
    """Why a connector can't serve a request (drives honest degradation)."""

    CONNECT_REQUIRED = "connect_required"  # unbound — "connect me"
    RESOURCE_NOT_FOUND = "resource_not_found"  # a resolve-miss
    UNREACHABLE = "unreachable"  # the MCP server is down
    STALE_TOKEN = "stale_token"  # bound but needs re-auth


@dataclass(frozen=True)
class DegradationResponse:
    """Honest degradation (ADR-070 D5 / WS-4): never silently empty.

    Carries a machine ``reason`` + a human-facing "connect me / here's what's missing"
    message, plus an optional structured hint (e.g. the connect URL).
    """

    reason: DegradationReason
    user_message: str
    action_hint: Optional[str] = None


@dataclass(frozen=True)
class ResourceQuery:
    """A request to resolve a connector resource (e.g. the user's default repo)."""

    kind: str  # e.g. "default_repo", "calendar", "channel"
    params: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ConnectResult:
    """Outcome of ``connect()``: a binding, or a ``ConnectRequired`` handoff."""

    bound: bool
    binding_id: Optional[str] = None
    connect_required: Optional[DegradationResponse] = None  # set when not bound


@dataclass(frozen=True)
class ConnectorStatus:
    """``status()``: binding health without a resource fetch (ADR-070 D5)."""

    state: ConnectorStatusState
    detail: str = ""


@dataclass(frozen=True)
class ResolveResult:
    """``resolve()``: a concrete resource handle, or a miss (→ degrade)."""

    resolved: bool
    resource_handle: Optional[str] = None
    degradation: Optional[DegradationResponse] = None


@runtime_checkable
class Connector(Protocol):
    """The MCP-consumer connector contract (ADR-070 D5).

    Every connector adapter implements all four methods. The m-41 AST-guard
    (``test_connector_contract_1232``) enforces this on **declared conformers**, so a
    connector cannot silently skip honest-degradation or status reporting.
    """

    async def connect(self, user_id: str) -> ConnectResult: ...

    async def status(self, user_id: str) -> ConnectorStatus: ...

    async def resolve(self, user_id: str, resource: ResourceQuery) -> ResolveResult: ...

    async def degrade(self, reason: DegradationReason) -> DegradationResponse: ...
