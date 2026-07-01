"""#1232 (RECONNECT WS-5) — the MCP-consumer Connector protocol (ADR-070 D5).

One contract every MCP-consumer adapter implements: ``connect`` / ``status`` /
``resolve`` / ``degrade``. Per ADR-070 D3 + Open-Q-5: the external MCP server owns the
OAuth/token lifecycle; ``connect()`` returns a ``Binding`` or a ``ConnectRequired`` —
Piper stores bindings, never raw tokens. The ``*Miss`` / ``ConnectRequired`` variants and
``degrade()`` are the honest-degradation contract (D5; WS-4 made structural): never
silently empty — an unconfigured/unresolvable connector says "connect me" / "here's
what's missing".

The four **methods** are settled by ADR-070 D5. The **result-type shapes** are
Lead-authored per ADR-070 Open-Q-4 and **Arch-ratified 2026-06-21** (v2; constraints 06-20): the outcomes
are explicit SUM types — ``ConnectResult = Binding | ConnectRequired`` and
``ResolveResult = ResourceHandle | ResolveMiss`` — so the "I don't have it" case is a
first-class, must-be-handled variant, not a nullable field a caller can ``or {}`` away.
No return type carries credential material (D3); ``test_connector_contract_1232`` asserts
that structurally. Nothing consumes this protocol yet; WS-3 (``resolve``) and WS-4
(``degrade``) build onto it next.
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

    NOT_CONFIGURED = "not_configured"  # #1231: never set up (admin/onboard gap) — distinct from CONNECT_REQUIRED
    CONNECT_REQUIRED = "connect_required"  # configured but this user hasn't connected — "connect me"
    RESOURCE_NOT_FOUND = "resource_not_found"  # a resolve-miss
    UNREACHABLE = "unreachable"  # the MCP server is down
    STALE_TOKEN = "stale_token"  # bound but needs re-auth
    REPO_UNRESOLVED = "repo_unresolved"  # #1327: repo-scoped read but no target repo — "which repo?"


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


# ── connect() outcome — an explicit SUM (ADR-070 Open-Q-4 constraint 1; Arch 2026-06-20).
#    The "I'm not connected" case is its own type the caller MUST handle, not a nullable
#    field that an ``or {}`` could mask away (D5 never-silently-empty).
@dataclass(frozen=True)
class Binding:
    """``connect()`` success: the user is bound. A binding id only — never a token (D3)."""

    binding_id: str


@dataclass(frozen=True)
class ConnectRequired:
    """``connect()`` needs the user to connect first — a first-class, must-be-handled
    variant carrying the honest "connect me" degradation (D5)."""

    degradation: DegradationResponse


ConnectResult = Binding | ConnectRequired


# ── resolve() outcome — an explicit SUM (constraint 2): a concrete handle, or a miss that
#    says WHAT'S MISSING (non-maskable honest degradation — D5 / WS-4).
@dataclass(frozen=True)
class ResourceHandle:
    """``resolve()`` success: a concrete handle (e.g. a repo id). No credential material (D3)."""

    handle: str
    kind: str = ""


@dataclass(frozen=True)
class ResolveMiss:
    """``resolve()`` miss: carries the honest "here's what's missing" degradation."""

    degradation: DegradationResponse


ResolveResult = ResourceHandle | ResolveMiss


@dataclass(frozen=True)
class ConnectorStatus:
    """``status()``: binding health without a resource fetch or token (ADR-070 D5 / D3)."""

    state: ConnectorStatusState
    detail: str = ""


@runtime_checkable
class Connector(Protocol):
    """The MCP-consumer connector contract (ADR-070 D5).

    Every connector adapter implements all four methods. The m-41 AST-guard
    (``test_connector_contract_1232``) enforces this on **declared conformers** and
    asserts no return type carries credential material, so a connector cannot silently
    skip honest-degradation, status reporting, or leak a token.
    """

    async def connect(self, user_id: str) -> ConnectResult: ...

    async def status(self, user_id: str) -> ConnectorStatus: ...

    async def resolve(self, user_id: str, resource: ResourceQuery) -> ResolveResult: ...

    async def degrade(self, reason: DegradationReason) -> DegradationResponse: ...
