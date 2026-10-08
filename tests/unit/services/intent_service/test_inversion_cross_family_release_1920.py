"""#1920 — the cross-family WRITE release for armed-carrier off-intent
discriminators (Arch's shape, CXO's ruling, 2026-10-02).

The fifth Phase 3 deletion (GITHUB_QUERY_PATTERNS) removed the surface-1
literals that used to release "close issue #108" from a reminder pick, so a
stuck carrier re-asked instead of releasing. ``read_op_claims_turn`` now also
releases a router-named WRITE at/above threshold when its ACTION_REGISTRY
category DIFFERS from the carrier's own pending op's category — mechanical,
registry-read, never a same-family write (those are the carrier's answers:
"delete it", "clear them all"). A released write executes nothing by itself;
the turn goes back to normal routing and the write meets its own confirm.

Deterministic layer only: the router is stubbed (same idiom as
test_inversion_read_release_1899.py) — no live LLM call anywhere. What the
real router returns for these phrasings is UNMEASURED here.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from services.intent_service import inversion_live
from services.intent_service.inversion_router import RoutingDecision
from services.intent_service.workflow_entries import register_default_workflows

pytestmark = pytest.mark.asyncio


def _svc():
    register_default_workflows()
    return SimpleNamespace(intent_classifier=None)


def _stub_route(monkeypatch, *, operation, confidence=0.95):
    from services.intent_service import inversion_router as ir

    async def _route(message, session_state=None, **kwargs):
        return RoutingDecision(outcome="operation", operation=operation, confidence=confidence)

    monkeypatch.setattr(ir, "route", _route)


def test_registry_category_for_reads_the_registry():
    """The carrier's family comes from the registry, alias-aware, never a
    call-site constant: the reminder carriers are EXECUTION; the GitHub
    writes the fifth deletion orphaned are QUERY-registered."""
    assert inversion_live.registry_category_for("delete_todo") == "EXECUTION"
    assert inversion_live.registry_category_for("create_reminder") == "EXECUTION"
    assert inversion_live.registry_category_for("close_issue_query") == "QUERY"
    assert inversion_live.registry_category_for("close_issue") == "QUERY"  # alias
    assert inversion_live.registry_category_for("no_such_op_xyz") is None


def test_registry_category_for_the_new_portfolio_writes():
    """#1595 Phase 3 (2026-10-04, Arch's manage_portfolio split, §2):
    archive_project / restore_project / add_project are PORTFOLIO-
    registered — DIFFERENT from the reminder/todo carriers' own EXECUTION
    family, the precondition for the cross-family release pinned below."""
    assert inversion_live.registry_category_for("archive_project") == "PORTFOLIO"
    assert inversion_live.registry_category_for("restore_project") == "PORTFOLIO"
    assert inversion_live.registry_category_for("add_project") == "PORTFOLIO"


def test_registry_category_for_link_repo():
    """#1595 Phase 3 (2026-10-03, Arch's manage_repos split, §2): link_repo
    is PORTFOLIO-registered too — same precondition, same family as the
    manage_portfolio writes above, SAME manage_repos split that produced
    list_repos (READ, joined into read_portfolio)."""
    assert inversion_live.registry_category_for("link_repo") == "PORTFOLIO"


def test_registry_category_for_unlink_repo():
    """#1926 / #1595 Phase 3 (2026-10-04, CXO's 2026-10-03 ruling on #1926,
    Arch's 2026-10-03 manage_repos split, §2): unlink_repo is
    PORTFOLIO-registered too — the DESTRUCTIVE third of the SAME split that
    produced list_repos/link_repo above, same cross-family precondition."""
    assert inversion_live.registry_category_for("unlink_repo") == "PORTFOLIO"


class TestCrossFamilyWriteRelease:
    async def test_cross_family_write_releases(self, monkeypatch):
        """'close issue #108' inside a reminder pick: QUERY-registered write,
        carrier is EXECUTION → release (nothing executes; the write still
        meets its own confirm downstream). Not gated on the live flag —
        the flag governs dispatch, a release dispatches nothing."""
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status")  # no writes live
        _stub_route(monkeypatch, operation="close_issue_query", confidence=0.9)
        result = await inversion_live.read_op_claims_turn(
            "close issue #108",
            session_id="s1",
            user_id="u1",
            intent_service=_svc(),
            carrier_category="EXECUTION",
        )
        assert result == "close_issue_query"

    async def test_same_family_write_binds(self, monkeypatch):
        """'delete it' is an ANSWER to a reminder carrier — never released."""
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status,delete_todo")
        _stub_route(monkeypatch, operation="delete_todo", confidence=0.95)
        result = await inversion_live.read_op_claims_turn(
            "delete it",
            session_id="s1",
            user_id="u1",
            intent_service=_svc(),
            carrier_category="EXECUTION",
        )
        assert result is None

    @pytest.mark.parametrize(
        "operation",
        ["archive_project", "restore_project", "add_project", "link_repo", "unlink_repo"],
    )
    async def test_portfolio_write_releases_an_execution_carrier(self, monkeypatch, operation):
        """#1595 Phase 3 (2026-10-04 manage_portfolio split + 2026-10-03
        manage_repos split) + #1926 (unlink_repo, 2026-10-04): Arch's
        intended consequence of both splits — archive_project/
        restore_project/add_project/link_repo/unlink_repo are all
        PORTFOLIO-registered (DIFFERENT from the reminder/todo carriers'
        own EXECUTION family), so a router-named turn now releases an armed
        EXECUTION carrier exactly like 'close issue #108' already does.
        Not gated on the live flag (read_status only; none of the five
        writes are live) — a release dispatches nothing."""
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status")
        _stub_route(monkeypatch, operation=operation, confidence=0.9)
        result = await inversion_live.read_op_claims_turn(
            "archive my project Foo",
            session_id="s1",
            user_id="u1",
            intent_service=_svc(),
            carrier_category="EXECUTION",
        )
        assert result == operation

    async def test_without_a_carrier_category_writes_never_release(self, monkeypatch):
        """The FTUX carrier passes none — reads-only, byte-for-byte #1899."""
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status")
        _stub_route(monkeypatch, operation="close_issue_query", confidence=0.95)
        result = await inversion_live.read_op_claims_turn(
            "close issue #108", session_id="s1", user_id="u1", intent_service=_svc()
        )
        assert result is None

    async def test_sub_threshold_cross_family_write_binds(self, monkeypatch):
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status")
        _stub_route(monkeypatch, operation="close_issue_query", confidence=0.6)
        result = await inversion_live.read_op_claims_turn(
            "close issue #108",
            session_id="s1",
            user_id="u1",
            intent_service=_svc(),
            carrier_category="EXECUTION",
        )
        assert result is None

    async def test_reads_still_release_exactly_as_before(self, monkeypatch):
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status")
        _stub_route(monkeypatch, operation="list_reminders_query", confidence=0.9)
        result = await inversion_live.read_op_claims_turn(
            "list my reminders",
            session_id="s1",
            user_id="u1",
            intent_service=_svc(),
            carrier_category="EXECUTION",
        )
        assert result == "list_reminders_query"


class TestCarrierWiringAndExit:
    def test_both_reminder_carriers_pass_their_registry_family(self):
        """The pick-target carrier (unchanged, out of #1886's scope) still
        names its pending op's family from the registry via
        ``read_op_claims_turn``'s ``carrier_category``.

        #1886(b) (Arch's binding ruling, 2026-10-07): the reminder-TASK
        carrier (``todo_handlers.handle_reminder_task_turn``) no longer
        calls ``read_op_claims_turn`` at all — its off-intent release is
        now the SHARED, stateless armed-turn consult
        (``armed_turn_consult.classify_armed_reply``), which releases on
        ANY operation at/above threshold regardless of registry family (no
        ``carrier_category`` concept at that layer — see
        test_task_clarify_1654.py::TestTaskTurnHandlerSeam::
        test_write_op_now_releases_per_1886b for the pin). This assertion
        is narrowed to the carrier that still owns the #1920 mechanism;
        asserting the OLD literal against ``todo_handlers`` would require
        reintroducing the call site #1886(b) deliberately removed."""
        import inspect

        from services.intent_service import reminder_clear

        pick = inspect.getsource(reminder_clear._handle_pick_target_turn)
        assert 'carrier_category=registry_category_for("delete_todo")' in pick
        # The FTUX interview carrier stays reads-only.
        from services.intent_service import first_contact

        assert "carrier_category" not in inspect.getsource(first_contact)

    def test_exit_copy_at_both_prompt_sites(self):
        """CXO's copy, one exit phrase at both sites."""
        import inspect

        from services.intent_service import reminder_clear

        src = inspect.getsource(reminder_clear)
        # The initial-arm string is split across two literals in source;
        # check its two halves and the re-ask's whole clause.
        assert "or say 'never mind' and I'll " in src and '"leave it alone."' in src
        assert "or say 'never mind' to drop it." in src
        assert "act on just that" not in src

    def test_never_mind_is_a_decline_at_the_pick_target_seam(self):
        """CXO's open build question, answered by probing the real seam:
        the exact phrase already resolves as DECLINE — no special case.
        (Variants — 'nevermind', 'forget it' — do NOT; a tolerance question
        for CXO, recorded here as measured.)"""
        from services.intent_service.acceptance import (
            AcceptanceVerdict,
            declared_axes_for_workflow,
            evaluate_acceptance,
        )
        from services.intent_service.reminder_clear import CLEAR_PICK_TARGET_WORKFLOW

        axes = declared_axes_for_workflow(CLEAR_PICK_TARGET_WORKFLOW)
        question = (
            "Still not sure which one — you have: 'hydrate', 'review the pr'. Tell me which "
            "one you mean (first, second, by name, or 'the overdue one'), or say 'never mind' "
            "to drop it."
        )
        verdict = evaluate_acceptance(
            "never mind",
            effect=axes[0] if axes else None,
            outwardness=axes[1] if axes else None,
            armed_question=question,
        )
        assert verdict is AcceptanceVerdict.DECLINE
