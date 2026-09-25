"""ADR-070 Amendment A / #1850 — write-time enforcement for connector_bindings.

The gap this closes: ``ConnectorBindingRepository.upsert`` (``binding_repository.py``)
wrote ``mcp_server_ref`` verbatim, whatever a caller passed — nothing enforced
Amendment A's shape. A1 rules that a managed-connector binding
(``github``/``calendar``/``notion``/``slack``) stores the LOGICAL KEY, not a topology;
A3 carves out exactly one legitimate literal, a scheme-prefixed BYOC override (the
user's own self-hosted server). A droplet/Fly hostname or bare IP written for a
managed key reproduces the 2026-07-12 Fly-cutover incident: the binding reads
BOUND-and-healthy while resolving against a host that no longer exists, and the
failure surfaces as a phantom server outage, not the config problem it is.

Reject, not normalize: Amendment A (docs/internal/architecture/adrs/
adr-070-mcp-consumer-connector-architecture.md, "Amendment A") describes what a
managed-connector row SHOULD hold (A1) and how BYOC is discriminated (A3); it does
not decide what a write-time enforcement point does with a bad literal — rewrite it
to the key, or refuse the write. #1850 rules REJECT: a silent rewrite of caller
intent is the same "value pinned without visibility into what changed it" shape
Amendment A's own root-cause paragraph names as the problem, applied one layer
earlier (at write time instead of read time). A rejected write surfaces the caller's
bug immediately, at the call site, instead of writing a row that only breaks on the
next host move.

Call-site-independent: ``ConnectorBindingRepository.upsert`` calls
``validate_mcp_server_ref`` before touching the row, so every write path — today's
one production caller (``github_oauth_handler.persist_github_connection``) and any
future one — gets the same enforcement without re-deriving the managed-key set or
the BYOC shape-check. Both are imported from ``server_ref_resolver`` (the A2 single
resolve-authority module) rather than re-derived here, so the write-time check and
the read-time resolver can never drift apart on what counts as a managed key or a
BYOC literal.
"""

from __future__ import annotations

from typing import Optional

from services.connectors.server_ref_resolver import _KEY_TO_ENV, is_byoc_literal

# The managed-connector key set, sourced from the resolver's own registry (A2) —
# never hand-listed here. Adding a connector to _KEY_TO_ENV extends enforcement
# automatically.
MANAGED_CONNECTOR_KEYS = frozenset(_KEY_TO_ENV)


class ManagedConnectorRefRejected(ValueError):
    """Raised when a managed-connector write's ``mcp_server_ref`` is a literal
    that is neither the logical key nor a scheme-prefixed BYOC override
    (ADR-070 Amendment A1/A3). Carries ``connector`` and ``value`` for callers
    that want to react programmatically (e.g. surface the expected key in a
    setup-guidance message) in addition to the human-readable message.
    """

    def __init__(self, connector: str, value: str):
        self.connector = connector
        self.value = value
        super().__init__(
            f"connector_bindings write rejected for connector={connector!r}: "
            f"mcp_server_ref={value!r} is neither the logical key {connector!r} "
            f"(ADR-070 Amendment A1) nor a scheme-prefixed BYOC URL (A3). "
            f"Managed connectors store the key itself — pass "
            f"mcp_server_ref={connector!r} (or omit it to leave the row's "
            f"existing/default value), or use a genuine http(s):// BYOC URL "
            f"if this really is a user-owned self-hosted server."
        )


def validate_mcp_server_ref(connector: str, mcp_server_ref: Optional[str]) -> None:
    """Enforce ADR-070 A1/A3 shape on a connector-binding write.

    No-op unless ALL of:
      - ``connector`` is one of the four managed keys (``MANAGED_CONNECTOR_KEYS``),
        and
      - ``mcp_server_ref`` is a non-empty (post-strip) literal, and
      - that literal is neither a scheme-prefixed BYOC override (A3) nor the
        connector's own logical key (A1).

    A connector outside the managed set is out of scope for this validator —
    it makes no enforcement claim about non-managed connectors' bindings.

    Raises ``ManagedConnectorRefRejected`` on a violation; never rewrites the
    value (see module docstring — #1850 rules reject, not silent-normalize).
    """
    if mcp_server_ref is None:
        return
    value = mcp_server_ref.strip()
    if not value:
        return
    if connector not in MANAGED_CONNECTOR_KEYS:
        return  # not a managed connector; this validator makes no claim here
    if is_byoc_literal(value):
        return  # A3: legitimate BYOC override
    if value == connector:
        return  # A1: the logical key itself
    raise ManagedConnectorRefRejected(connector, value)
