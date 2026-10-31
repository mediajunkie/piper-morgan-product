"""#2218 — the hosted MCP profile mirrors the chat floor's field-level read contract.

Residual of #2151: the profile resource served PIPER.md's fallback projects over a FAILED
projects read, the same wrong-person shape the chat floor fixed. Arch's ruling (issue
comment, 2026-10-31): a failed projects read serves ``projects: null`` with
``projects_status: "read_failed"`` (never ``[]``, never the config list); a failed
preferences read withholds ``priorities`` and ``organization`` the same way; a clean read
is unchanged; ``available: false`` stays for the whole-read exception only.

LAYER (m-43): the resource function ``_read_profile`` called directly with the caller
identity and the user-context read stubbed, i.e. the function layer, one below the MCP
round trip that ``test_resources_unit2.py`` pins (that file's clean-read and whole-read
exception pins still run over the real client and cover the protocol layer).
DENOMINATOR: the profile resource only; the colleague-model and GitHub resources have no
projects/preferences read.

The "PIPER.md value" the failure pins assert absent is the stub's own sentinel config
list and organization, so the assertion is on the resource's behaviour, not on what the
tracked ``config/PIPER.md`` happens to contain today.
"""

from __future__ import annotations

import json
import uuid

import pytest

from services.mcp.server import resources
from services.user_context_service import UserContext, user_context_service

CALLER = uuid.UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")
CONFIG_PROJECTS = ["piper-morgan-from-PIPER.md", "second-config-project"]
CONFIG_ORG = "Org from PIPER.md"
CONFIG_PRIORITIES = ["config priority one"]


def _stub(ctx: UserContext, monkeypatch) -> list[uuid.UUID | None]:
    seen: list[uuid.UUID | None] = []

    async def _get_user_context(session_id=None, user_id=None):
        seen.append(user_id)
        return ctx

    monkeypatch.setattr(user_context_service, "get_user_context", _get_user_context)
    monkeypatch.setattr(resources, "current_user_id", lambda: str(CALLER))
    return seen


def _fallback_ctx(**flags) -> UserContext:
    """What ``get_user_context`` returns when the DB reads fail: the PIPER.md fallback
    values with the #2151 failure flags set (``projects_source`` stays ``config``)."""
    return UserContext(
        user_id=CALLER,
        organization=CONFIG_ORG,
        projects=list(CONFIG_PROJECTS),
        priorities=list(CONFIG_PRIORITIES),
        projects_source="config",
        **flags,
    )


def _no_config_value_present(payload: dict) -> None:
    text = json.dumps(payload)
    for value in (*CONFIG_PROJECTS, CONFIG_ORG, *CONFIG_PRIORITIES):
        assert value not in text, f"PIPER.md value {value!r} served over a failed read"


@pytest.mark.asyncio
async def test_failed_projects_read_serves_null_and_read_failed_not_the_config_list(
    monkeypatch,
) -> None:
    seen = _stub(_fallback_ctx(projects_read_failed=True), monkeypatch)
    payload = json.loads(await resources._read_profile())
    assert seen == [CALLER]
    assert payload["available"] is True
    assert payload["projects"] is None
    assert payload["projects_status"] == "read_failed"
    assert payload["projects_source"] is None
    assert payload["projects"] != []
    assert CONFIG_PROJECTS[0] not in json.dumps(payload)
    # Preferences read was fine: those fields are served as they are.
    assert payload["organization"] == CONFIG_ORG
    assert payload["priorities"] == CONFIG_PRIORITIES
    assert "priorities_status" not in payload and "organization_status" not in payload


@pytest.mark.asyncio
async def test_failed_preferences_read_withholds_priorities_and_organization(
    monkeypatch,
) -> None:
    # With DB project rows present, a failed preferences read fails only preferences.
    ctx = UserContext(
        user_id=CALLER,
        organization=CONFIG_ORG,
        projects=["db-project"],
        priorities=list(CONFIG_PRIORITIES),
        projects_source="database",
        preferences_read_failed=True,
    )
    _stub(ctx, monkeypatch)
    payload = json.loads(await resources._read_profile())
    assert payload["available"] is True
    assert payload["priorities"] is None
    assert payload["priorities_status"] == "read_failed"
    assert payload["organization"] is None
    assert payload["organization_status"] == "read_failed"
    assert CONFIG_ORG not in json.dumps(payload)
    assert CONFIG_PRIORITIES[0] not in json.dumps(payload)
    # The projects read was fine: served unchanged.
    assert payload["projects"] == ["db-project"]
    assert payload["projects_source"] == "database"
    assert "projects_status" not in payload


@pytest.mark.asyncio
async def test_both_reads_failed_serves_no_piper_md_value_at_all(monkeypatch) -> None:
    # No rows + failed preferences: the service sets both flags (user_context_service
    # ~line 217). The fallback ctx carries every PIPER.md value; none may appear.
    _stub(_fallback_ctx(projects_read_failed=True, preferences_read_failed=True), monkeypatch)
    payload = json.loads(await resources._read_profile())
    assert payload == {
        "available": True,
        "organization": None,
        "organization_status": "read_failed",
        "projects": None,
        "projects_source": None,
        "projects_status": "read_failed",
        "priorities": None,
        "priorities_status": "read_failed",
    }
    _no_config_value_present(payload)


@pytest.mark.asyncio
async def test_clean_read_payload_is_unchanged(monkeypatch) -> None:
    ctx = UserContext(
        user_id=CALLER,
        organization="Org A",
        projects=["project-a"],
        priorities=["priority-a"],
        projects_source="database",
    )
    _stub(ctx, monkeypatch)
    payload = json.loads(await resources._read_profile())
    assert payload == {
        "available": True,
        "organization": "Org A",
        "projects": ["project-a"],
        "projects_source": "database",
        "priorities": ["priority-a"],
    }


@pytest.mark.asyncio
async def test_verified_empty_config_fallback_is_still_served_out_of_scope(
    monkeypatch,
) -> None:
    # Arch: the verified-empty fallback to PIPER.md (both reads GOOD, no rows, no prefs,
    # ``projects_source: "config"``) is out of #2218's scope and unchanged, as in chat.
    _stub(_fallback_ctx(), monkeypatch)
    payload = json.loads(await resources._read_profile())
    assert payload["projects"] == CONFIG_PROJECTS
    assert payload["projects_source"] == "config"
    assert "projects_status" not in payload


@pytest.mark.asyncio
async def test_only_the_services_own_bool_arms_a_withhold(monkeypatch) -> None:
    # ``is True`` as on the floor: a truthy non-bool never withholds.
    ctx = _fallback_ctx()
    ctx.projects_read_failed = "yes"  # type: ignore[assignment]
    _stub(ctx, monkeypatch)
    payload = json.loads(await resources._read_profile())
    assert payload["projects"] == CONFIG_PROJECTS
    assert "projects_status" not in payload


@pytest.mark.asyncio
async def test_whole_read_exception_is_still_available_false(monkeypatch) -> None:
    async def _boom(session_id=None, user_id=None):
        raise RuntimeError("db down")

    monkeypatch.setattr(user_context_service, "get_user_context", _boom)
    monkeypatch.setattr(resources, "current_user_id", lambda: str(CALLER))
    payload = json.loads(await resources._read_profile())
    assert payload == {"available": False, "reason": "profile_read_failed"}
