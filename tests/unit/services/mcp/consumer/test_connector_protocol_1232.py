"""#1232 P1 (v2 — Arch-ratified 2026-06-20) — Connector protocol + result types.

The result types are explicit SUM types per Arch's ADR-070 Open-Q-4 constraints (2026-06-20):
``ConnectResult = Binding | ConnectRequired`` and ``ResolveResult = ResourceHandle | ResolveMiss``.
The "I don't have it" case is a first-class, must-be-handled variant — not a nullable field a
caller can ``or {}`` away (D5 never-silently-empty). No return type carries credential material
(D3) — enforced structurally by ``test_connector_contract_1232.test_no_return_type_exposes_credential_material``.
"""
import dataclasses

import pytest

from services.mcp.consumer.connector import (
    Binding,
    Connector,
    ConnectorStatus,
    ConnectorStatusState,
    ConnectRequired,
    ConnectResult,
    DegradationReason,
    DegradationResponse,
    ResolveMiss,
    ResolveResult,
    ResourceHandle,
    ResourceQuery,
)


def test_status_states_cover_the_four_adr070_d5_states():
    assert {s.value for s in ConnectorStatusState} == {"bound", "unbound", "unreachable", "stale"}


def test_degradation_response_carries_reason_and_human_message():
    d = DegradationResponse(
        reason=DegradationReason.CONNECT_REQUIRED,
        user_message="Connect GitHub to continue",
        action_hint="/connect/github",
    )
    assert d.reason is DegradationReason.CONNECT_REQUIRED
    assert "Connect" in d.user_message
    assert d.action_hint == "/connect/github"


# ── ConnectResult is a SUM: Binding | ConnectRequired (Arch constraint 1) ──
def test_connect_result_is_a_sum_of_binding_or_connect_required():
    assert isinstance(Binding(binding_id="b1"), ConnectResult)
    cr = ConnectRequired(
        degradation=DegradationResponse(
            reason=DegradationReason.CONNECT_REQUIRED, user_message="connect me"
        )
    )
    assert isinstance(cr, ConnectResult)


def test_binding_carries_only_a_binding_id_no_token():
    # D3: a binding, never a credential. Binding holds the binding id and nothing token-shaped.
    assert {f.name for f in dataclasses.fields(Binding)} == {"binding_id"}


def test_connect_required_carries_honest_degradation():
    cr = ConnectRequired(
        degradation=DegradationResponse(
            reason=DegradationReason.CONNECT_REQUIRED,
            user_message="connect me",
            action_hint="/connect/github",
        )
    )
    assert cr.degradation.reason is DegradationReason.CONNECT_REQUIRED
    assert cr.degradation.action_hint == "/connect/github"


# ── ResolveResult is a SUM: ResourceHandle | ResolveMiss (Arch constraint 2) ──
def test_resolve_result_is_a_sum_of_handle_or_miss():
    assert isinstance(ResourceHandle(handle="owner/repo", kind="default_repo"), ResolveResult)
    miss = ResolveMiss(
        degradation=DegradationResponse(
            reason=DegradationReason.RESOURCE_NOT_FOUND, user_message="no default repo"
        )
    )
    assert isinstance(miss, ResolveResult)


def test_resolve_miss_says_what_is_missing():
    miss = ResolveMiss(
        degradation=DegradationResponse(
            reason=DegradationReason.RESOURCE_NOT_FOUND,
            user_message="no default repo configured",
        )
    )
    assert miss.degradation.reason is DegradationReason.RESOURCE_NOT_FOUND
    assert "default repo" in miss.degradation.user_message


def test_resource_handle_has_no_credential_field():
    names = {f.name for f in dataclasses.fields(ResourceHandle)}
    assert "token" not in names and "secret" not in names


# ── the variants are DISTINCT — you must handle which one (no silent `or {}` masking) ──
def test_variants_are_distinct_types():
    assert Binding is not ConnectRequired
    assert ResourceHandle is not ResolveMiss
    assert not isinstance(Binding(binding_id="b"), ConnectRequired)
    assert not isinstance(
        ResolveMiss(
            degradation=DegradationResponse(
                reason=DegradationReason.RESOURCE_NOT_FOUND, user_message="x"
            )
        ),
        ResourceHandle,
    )


def test_connector_status_is_metadata_only():
    # Arch constraint 4: status is metadata-only — no resource fetch, no token.
    assert {f.name for f in dataclasses.fields(ConnectorStatus)} == {"state", "detail"}
    s = ConnectorStatus(state=ConnectorStatusState.BOUND, detail="ok")
    assert s.state is ConnectorStatusState.BOUND


def test_runtime_checkable_conformance_accepts_full_impl():
    class Good:
        async def connect(self, user_id): ...

        async def status(self, user_id): ...

        async def resolve(self, user_id, resource): ...

        async def degrade(self, reason): ...

    assert isinstance(Good(), Connector)


def test_runtime_checkable_rejects_missing_method():
    class MissingDegrade:
        async def connect(self, user_id): ...

        async def status(self, user_id): ...

        async def resolve(self, user_id, resource): ...

    assert not isinstance(MissingDegrade(), Connector)


def test_resource_query_holds_kind_and_params():
    q = ResourceQuery(kind="default_repo", params={"project_id": "p1"})
    assert q.kind == "default_repo"
    assert q.params["project_id"] == "p1"


def test_result_variants_are_frozen():
    b = Binding(binding_id="b1")
    with pytest.raises(Exception):
        b.binding_id = "b2"  # frozen dataclass
    h = ResourceHandle(handle="owner/repo")
    with pytest.raises(Exception):
        h.handle = "x"  # frozen dataclass
