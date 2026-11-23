"""Issue 2417: a GitHub read that fails because GitHub is not connected, or needs
reconnecting, is not reported as a second failure.

Served on beta 2026-11-22: "open issues, blockers, and recent activity all came back
empty due to a data check failure. On top of that, your GitHub connection looks like it
needs to be reconnected". One cause was given to the floor as two facts: the
failed-checks line and the GitHub line.

Arch's ruling (mail 01M82R5YAW): when the context says GitHub is not connected or needs
reconnecting, the GitHub-derived failed checks are left out of the failed-checks line.
The set is declared on the registry by source, never inferred from a check name; the
trigger is the one issue 2414's guard change uses; other failed reads are untouched;
the guard's armed set is the same filtered list.

Layer: the registry, the rendered context block and the respond seam with a stub model.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.intent_service.conversational_floor import (
    SOURCE_FAILED_FLAGS,
    ConversationalFloor,
    FloorContext,
    github_unavailable_by_context,
    reported_failed_sources,
)

GITHUB_FLAGS = {
    "first_contact_source_failed",
    "open_issues_source_failed",
    "blocked_items_source_failed",
    "milestones_source_failed",
    "github_activity_source_failed",
}
THREE = {
    "open_issues_source_failed": True,
    "blocked_items_source_failed": True,
    "github_activity_source_failed": True,
}
RECONNECT = {"github_connected": True, "github_needs_reconnecting": True}
NOT_CONNECTED = {"github_connected": False}
HEALTHY = {"github_connected": True, "github_needs_reconnecting": False}


def _block(context):
    return ConversationalFloor(system_prompt_base="x")._format_domain_context(context)


def test_the_github_derived_set_is_declared_on_the_registry_by_source():
    declared = {entry.flag for entry in SOURCE_FAILED_FLAGS if entry.source == "github"}
    assert declared == GITHUB_FLAGS
    assert {entry.source for entry in SOURCE_FAILED_FLAGS} == {"github", None}
    # the integrations read covers every integration, so it is not GitHub's alone
    assert "integrations_source_failed" not in declared


@pytest.mark.parametrize(
    "context, expected",
    [
        (RECONNECT, True),
        (NOT_CONNECTED, True),
        (HEALTHY, False),
        ({}, False),
        ({"github_needs_reconnecting": True}, False),  # no key the prompt renders from
    ],
)
def test_the_one_trigger(context, expected):
    assert github_unavailable_by_context(context) is expected
    assert github_unavailable_by_context(None) is False


@pytest.mark.parametrize("github", [RECONNECT, NOT_CONNECTED])
def test_three_github_failures_with_github_unavailable_give_no_failed_checks_line(github):
    context = {**THREE, **github}
    assert reported_failed_sources(context) == ()
    block = _block(context)
    assert "DATA CHECKS FAILED" not in block
    # the fact is still said, by the GitHub line
    assert "GitHub: needs reconnecting" in block or "GitHub: not connected" in block


def test_a_todo_failure_on_the_same_turn_is_still_reported_and_only_it():
    context = {**THREE, **RECONNECT, "pending_todos_source_failed": True}
    assert [entry.check_name for entry in reported_failed_sources(context)] == ["pending todos"]
    block = _block(context)
    assert "DATA CHECKS FAILED this turn — could not check: pending todos." in block
    for name in ("open issues", "blocked items", "recent repository activity"):
        assert f"could not check: {name}" not in block and f", {name}" not in block


def test_github_connected_and_fine_reports_a_github_failure_as_today():
    context = {**THREE, **HEALTHY}
    assert [entry.check_name for entry in reported_failed_sources(context)] == [
        "open issues",
        "blocked items",
        "recent repository activity",
    ]
    assert (
        "DATA CHECKS FAILED this turn — could not check: open issues, blocked items, "
        "recent repository activity."
    ) in _block(context)


def test_with_no_github_key_in_the_context_nothing_is_left_out():
    assert len(reported_failed_sources(dict(THREE))) == 3


def _floor_returning(text):
    llm = MagicMock()
    llm.complete = AsyncMock(return_value=text)
    return ConversationalFloor(llm_client=llm, system_prompt_base="You are Piper Morgan (test).")


@pytest.mark.asyncio
async def test_the_guards_armed_set_is_the_same_filtered_list():
    """With GitHub needing reconnecting and only GitHub reads failed, nothing is armed,
    so the guard does not scan and a sentence about another source is left alone."""
    reply = "I don't have your calendar in front of me this turn. GitHub needs reconnecting."
    floor = _floor_returning(reply)
    resp = await floor.respond(
        FloorContext(
            user_message="how is the Harbor Survey project going?",
            session_id="s2417-a",
            intent_category="STATUS",
            intent_action="get_project_status",
            domain_context={"projects": [], **THREE, **RECONNECT},
        )
    )
    assert resp.scope_guard_dropped == 0 and resp.message == reply


@pytest.mark.asyncio
async def test_a_non_github_failure_still_arms_the_guard():
    reply = (
        "I couldn't check your calendar this turn. GitHub needs reconnecting, so issue "
        "data is unavailable."
    )
    floor = _floor_returning(reply)
    resp = await floor.respond(
        FloorContext(
            user_message="how is the Harbor Survey project going?",
            session_id="s2417-b",
            intent_category="STATUS",
            intent_action="get_project_status",
            domain_context={
                "projects": [],
                **THREE,
                **RECONNECT,
                "pending_todos_source_failed": True,
            },
        )
    )
    assert resp.scope_guard_dropped == 1
    assert "calendar" not in resp.message and "GitHub needs reconnecting" in resp.message


# -- CXO 01M82SPNM3: no prompt line states a cause for reconnecting ----------------


def test_the_never_connected_line_is_unchanged():
    """CXO's reworded line for this case (01M82SPNM3) was measured and not landed: with
    it, 0 of 6 replies said GitHub wasn't connected. The old line stays until she rules."""
    assert "- GitHub: not connected (issue/PR data unavailable until connected)" in _block(
        {"github_connected": False}
    )


def test_no_prompt_line_states_a_cause_for_reconnecting():
    from pathlib import Path

    source = (
        Path(__file__).resolve().parents[4]
        / "services"
        / "intent_service"
        / "conversational_floor.py"
    ).read_text()
    assert "the grant was revoked or expired" not in source
    assert '"- Needs reconnecting (reconnect in Settings → Integrations): "' in source
