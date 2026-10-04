"""#1595 Phase 3 — the WRITE thirds of `manage_portfolio`'s split (Arch's
ruling 2026-10-04, mailboxes/lead/read/rule-arch-to-lead-cc-cxo-ppm-exec-
execute-vocab-coverage-portfolio-split-file-reference-2026-10-04.md, section
2: "manage_portfolio: your four questions").

Three new WRITE rail entries, each wrapping an EXISTING (hoisted, for
archive/restore; already-separate, for add) canonical handler directly —
the `get_current_time` precedent, same shape as `read_portfolio`'s
`list_repos` adapter:

  - `archive_project` — CanonicalHandlers._handle_archive_project, hoisted
    out of `_handle_portfolio_query`'s ARCHIVE branch.
  - `restore_project` — CanonicalHandlers._handle_restore_project, hoisted
    out of `_handle_portfolio_query`'s RESTORE branch.
  - `add_project` — CanonicalHandlers._handle_add_project (#1856's own
    method; no hoist needed, just a new rail entry wrapping it).

Disposition stays CANONICAL for all three (PORTFOLIO is a whole category
`CanonicalHandlers.can_handle` claims unconditionally); none carries a
flip_group (non-READ keys never carry one); each is individually named in
FLIP_WRITE_ALLOWLIST (#1677); NOT flipped by this build.

Also pinned here: the `list_archived` retirement (delegates to the EXISTING
`list_archived_projects` rail entry — "one source, no second READ
adapter", Arch's §2 question 4) and the `list_projects` naming COLLISION
this build deliberately did NOT resolve by overwriting (see Lead's
handback) — a regression guard that the pre-existing `list_projects` rail
entry (QUERY category, `_handle_projects_query`) survives this build
untouched.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from services.intent_service import workflow_entries as we
from services.intent_service.action_registry import ACTION_REGISTRY, ActionDisposition
from services.intent_service.collaboration_gate import FRAMING_EXECUTE, classify_framing
from services.intent_service.workflow_dispatcher import FLIP_WRITE_ALLOWLIST, get_action_workflows
from services.shared_types import EffectClass

WRITE_OPS = ("archive_project", "restore_project", "add_project")


# ---------------------------------------------------------------------------
# 1. Registration shape — WRITE, no flip_group, allowlisted, action_triggered
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("op", WRITE_OPS)
def test_registers_as_a_write_entry_with_no_flip_group(op):
    we.register_default_workflows()
    rail = get_action_workflows()
    entry = rail[op]
    assert entry.effect == EffectClass.WRITE
    assert entry.flip_group is None, f"{op} must never carry a flip_group (non-READ invariant)"
    assert entry.action_triggered is True
    assert entry.flip_write_allowlist_key == op
    assert op in FLIP_WRITE_ALLOWLIST


@pytest.mark.parametrize("op", WRITE_OPS)
def test_disposition_stays_canonical(op):
    """PORTFOLIO is a whole category CanonicalHandlers.can_handle() claims
    unconditionally, so each op's registry disposition must stay CANONICAL
    — WORKFLOW would fail test_registry_disposition_matches_live_runtime's
    oracle (it resolves can_handle() before ever consulting the rail)."""
    assert ACTION_REGISTRY[("PORTFOLIO", op)] is ActionDisposition.CANONICAL


@pytest.mark.parametrize("op", WRITE_OPS)
def test_verb_classifies_execute(op):
    """TestExecuteVocabCoverage (test_architecture_enforcement.py) already
    sweeps this mechanically; pinned again here, scoped to just these three
    ops, so a regression on THIS split shows up in this file too."""
    from services.intent_service.action_registry import get_verb

    verb = get_verb(op)
    assert verb is not None, f"{op} has no registered Verb"
    assert classify_framing(f"{verb.value} the item") == FRAMING_EXECUTE


# ---------------------------------------------------------------------------
# 2. Entry points call the existing handler directly, never reimplement
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_archive_entry_point_calls_the_existing_handler_directly():
    calls = {}

    async def _archive(intent, session_id, user_id=None):
        calls["intent"] = intent
        calls["session_id"] = session_id
        calls["user_id"] = user_id
        return {
            "message": "archived",
            "intent": {"action": "archive_project"},
            "requires_clarification": False,
        }

    canonical_handlers = SimpleNamespace(_handle_archive_project=_archive)
    svc = SimpleNamespace(canonical_handlers=canonical_handlers)
    intent = SimpleNamespace(action="archive_project", context={})
    out = await we.run_archive_project_workflow(
        "s1", "u1", {"intent": intent, "intent_service": svc}
    )
    assert out.message == "archived"
    assert calls["intent"] is intent
    assert calls["session_id"] == "s1"
    assert calls["user_id"] == "u1"


@pytest.mark.asyncio
async def test_restore_entry_point_calls_the_existing_handler_directly():
    calls = {}

    async def _restore(intent, session_id, user_id=None):
        calls["intent"] = intent
        calls["session_id"] = session_id
        calls["user_id"] = user_id
        return {
            "message": "restored",
            "intent": {"action": "restore_project"},
            "requires_clarification": False,
        }

    canonical_handlers = SimpleNamespace(_handle_restore_project=_restore)
    svc = SimpleNamespace(canonical_handlers=canonical_handlers)
    intent = SimpleNamespace(action="restore_project", context={})
    out = await we.run_restore_project_workflow(
        "s1", "u1", {"intent": intent, "intent_service": svc}
    )
    assert out.message == "restored"
    assert calls["intent"] is intent
    assert calls["session_id"] == "s1"
    assert calls["user_id"] == "u1"


@pytest.mark.asyncio
async def test_add_project_entry_point_calls_the_existing_handler_directly():
    calls = {}

    async def _add(original_message, session_id, user_id=None):
        calls["original_message"] = original_message
        calls["session_id"] = session_id
        calls["user_id"] = user_id
        return {
            "message": "added",
            "intent": {"action": "add_project"},
            "requires_clarification": False,
        }

    canonical_handlers = SimpleNamespace(_handle_add_project=_add)
    svc = SimpleNamespace(canonical_handlers=canonical_handlers)
    intent = SimpleNamespace(action="add_project", context={"original_message": "add project Foo"})
    out = await we.run_add_project_workflow("s1", "u1", {"intent": intent, "intent_service": svc})
    assert out.message == "added"
    assert calls["original_message"] == "add project Foo"
    assert calls["session_id"] == "s1"
    assert calls["user_id"] == "u1"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "runner",
    [we.run_archive_project_workflow, we.run_restore_project_workflow, we.run_add_project_workflow],
)
async def test_entry_point_without_context_returns_none_not_a_crash(runner):
    assert await runner("s1", "u1", {}) is None


# ---------------------------------------------------------------------------
# 3. Legacy canonical dispatch delegates to the SAME hoisted methods
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_legacy_archive_branch_delegates_to_the_hoisted_method(monkeypatch):
    from services.intent_service.canonical_handlers import CanonicalHandlers

    handler = CanonicalHandlers()
    calls = {}

    async def _fake_archive(intent, session_id, user_id=None):
        calls["called"] = True
        return {"message": "delegated", "intent": {"action": "archive_project"}}

    monkeypatch.setattr(handler, "_handle_archive_project", _fake_archive)

    intent = SimpleNamespace(
        action="manage_portfolio", context={"original_message": "archive my project Foo"}
    )
    result = await handler._handle_portfolio_query(intent, "sess", user_id="u1")
    assert calls.get("called") is True
    assert result["message"] == "delegated"


@pytest.mark.asyncio
async def test_legacy_restore_branch_delegates_to_the_hoisted_method(monkeypatch):
    from services.intent_service.canonical_handlers import CanonicalHandlers

    handler = CanonicalHandlers()
    calls = {}

    async def _fake_restore(intent, session_id, user_id=None):
        calls["called"] = True
        return {"message": "delegated", "intent": {"action": "restore_project"}}

    monkeypatch.setattr(handler, "_handle_restore_project", _fake_restore)

    intent = SimpleNamespace(
        action="manage_portfolio", context={"original_message": "restore project Foo"}
    )
    result = await handler._handle_portfolio_query(intent, "sess", user_id="u1")
    assert calls.get("called") is True
    assert result["message"] == "delegated"


@pytest.mark.asyncio
async def test_legacy_list_archived_branch_delegates_to_the_existing_rail_entry(monkeypatch):
    """Arch's §2 question 4: retire the in-handler branch in favour of the
    EXISTING list_archived_projects rail entry — one source, no second READ
    adapter."""
    from services.domain.models import Intent
    from services.intent_service import workflow_entries as we_module
    from services.intent_service.canonical_handlers import CanonicalHandlers
    from services.shared_types import IntentCategory

    handler = CanonicalHandlers()
    calls = {}

    async def _fake_archived_query(session_id, user_id=None, context=None):
        calls["called"] = True
        calls["session_id"] = session_id
        calls["user_id"] = user_id
        from services.intent.intent_service import IntentProcessingResult

        return IntentProcessingResult(
            success=True,
            message="delegated archived list",
            intent_data={"context": {"project_count": 0}},
            workflow_id=None,
            requires_clarification=False,
        )

    monkeypatch.setattr(we_module, "run_archived_projects_query_workflow", _fake_archived_query)

    intent = Intent(
        category=IntentCategory.PORTFOLIO,
        action="manage_portfolio",
        confidence=1.0,
        context={"original_message": "list my archived projects"},
    )
    result = await handler._handle_portfolio_query(intent, "sess1", user_id="u1")
    assert calls.get("called") is True
    assert calls["session_id"] == "sess1"
    assert calls["user_id"] == "u1"
    assert result["message"] == "delegated archived list"
    assert result["intent"]["action"] == "list_archived_projects"


# ---------------------------------------------------------------------------
# 4. The naming collision this build deliberately did NOT resolve by
#    overwriting — a regression guard, not a feature.
# ---------------------------------------------------------------------------


def test_list_projects_collision_survives_untouched():
    """`list_projects` is an EXISTING rail key (QUERY category,
    `_handle_projects_query`, flip_group read_status) this build did NOT
    reuse or overwrite for the new PORTFOLIO active-list+search op (Arch
    named it `list_projects` too — a real key collision, not just a name
    coincidence: `_default_entries` is one Python dict, and a later
    `_query_cohort` loop in workflow_entries.py assigns
    `_default_entries["list_projects"] = <the QUERY entry>` AFTER the main
    dict literal this build's new keys live in — so a same-named PORTFOLIO
    entry placed in that literal would be silently clobbered by the loop).
    This pin fails loudly if a future change re-introduces that collision."""
    we.register_default_workflows()
    rail = get_action_workflows()
    entry = rail["list_projects"]
    assert entry.effect == EffectClass.READ
    assert entry.flip_group == "read_status"
    assert entry.flip_write_allowlist_key is None
    # None of this build's three new WRITE entries occupy this key.
    for op in WRITE_OPS:
        assert rail[op] is not entry
