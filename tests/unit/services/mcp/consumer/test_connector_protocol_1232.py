"""#1232 P1 — Connector protocol + result types (TDD)."""
import pytest

from services.mcp.consumer.connector import (
    Connector,
    ConnectorStatus,
    ConnectorStatusState,
    ConnectResult,
    DegradationReason,
    DegradationResponse,
    ResolveResult,
    ResourceQuery,
)


def test_status_states_cover_the_four_adr070_d5_states():
    assert {s.value for s in ConnectorStatusState} == {
        "bound",
        "unbound",
        "unreachable",
        "stale",
    }


def test_degradation_response_carries_reason_and_human_message():
    d = DegradationResponse(
        reason=DegradationReason.CONNECT_REQUIRED,
        user_message="Connect GitHub to continue",
        action_hint="/connect/github",
    )
    assert d.reason is DegradationReason.CONNECT_REQUIRED
    assert "Connect" in d.user_message
    assert d.action_hint == "/connect/github"


def test_connect_result_unbound_carries_connect_required():
    cr = DegradationResponse(
        reason=DegradationReason.CONNECT_REQUIRED, user_message="connect me"
    )
    r = ConnectResult(bound=False, connect_required=cr)
    assert not r.bound
    assert r.connect_required.reason is DegradationReason.CONNECT_REQUIRED


def test_resolve_result_miss_carries_degradation():
    d = DegradationResponse(
        reason=DegradationReason.RESOURCE_NOT_FOUND, user_message="no default repo"
    )
    r = ResolveResult(resolved=False, degradation=d)
    assert not r.resolved
    assert r.degradation.reason is DegradationReason.RESOURCE_NOT_FOUND


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


def test_status_and_connect_results_construct():
    s = ConnectorStatus(state=ConnectorStatusState.BOUND, detail="ok")
    assert s.state is ConnectorStatusState.BOUND
    r = ConnectResult(bound=True, binding_id="b1")
    assert r.bound and r.binding_id == "b1"


def test_frozen_result_types_are_immutable():
    r = ConnectResult(bound=True, binding_id="b1")
    with pytest.raises(Exception):
        r.bound = False  # frozen dataclass
