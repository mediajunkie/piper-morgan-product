"""#2270 (Arch 2026-11-07 17:53): a read this session performed is a code-held fact.

The advisor's turn 2 ("I thought you had access to the GitHub repository …") was
answered with a false doubt about Piper's own previous read: the floor's honesty rule
treats data absence as a claim about THIS turn. Arch's fix is not a looser prompt but a
recorded read: the read's handler records it on success, and the floor renders it as a
fact line. Sentinel: a session that did not read never shows such a line.
"""

from datetime import timedelta
from uuid import uuid4

import pytest

from services.intent_service.context_assembler import ContextAssembler, _recorded_reads_for
from services.intent_service.conversation_context import (
    get_or_create_context,
    record_read,
)
from services.intent_service.conversational_floor import ConversationalFloor

_USER = "2270aaaa-0000-4000-8000-000000002270"


def _floor_text(domain_context):
    floor = ConversationalFloor.__new__(ConversationalFloor)
    return floor._format_domain_context(domain_context)


def test_a_recorded_read_reaches_the_floor_as_a_fact_line():
    sid = f"rr-{uuid4().hex[:8]}"
    record_read(sid, _USER, "analyze_repository", "piper-test-repo", "its issues")
    reads = _recorded_reads_for(sid, _USER)
    assert reads == [{"target": "piper-test-repo", "covered": "its issues", "minutes_ago": 0}]
    text = _floor_text({"recorded_reads": reads})
    assert "- Earlier this session you read piper-test-repo (its issues), just now." in text


def test_the_age_is_said_in_minutes():
    sid = f"rr-{uuid4().hex[:8]}"
    record_read(sid, _USER, "get_project_status", "your projects", "their status")
    ctx = get_or_create_context(sid, user_id=_USER)
    ctx.recorded_reads[-1].at -= timedelta(minutes=3)
    text = _floor_text({"recorded_reads": _recorded_reads_for(sid, _USER)})
    assert "you read your projects (their status), 3 minutes ago." in text


def test_sentinel_no_read_no_line():
    """Arch's sentinel: a turn after a turn that did NOT read never claims a read."""
    sid = f"rr-{uuid4().hex[:8]}"
    assert _recorded_reads_for(sid, _USER) == []
    assert "Earlier this session you read" not in _floor_text({"current_time": "05:01 PM PST"})


def test_reads_are_capped_at_five_most_recent_last():
    sid = f"rr-{uuid4().hex[:8]}"
    for n in range(7):
        record_read(sid, _USER, "analyze_repository", f"repo-{n}", "its issues")
    targets = [r["target"] for r in _recorded_reads_for(sid, _USER)]
    assert targets == ["repo-2", "repo-3", "repo-4", "repo-5", "repo-6"]


def test_no_session_records_nothing():
    record_read(None, _USER, "analyze_repository", "piper-test-repo", "its issues")
    assert _recorded_reads_for(None, _USER) == []


# ---------------------------------------------------------------------------
# Arch 19:41 / PA 19:39: analysis/analyze_repository has no handler; it floors, and
# the floor composes from the GitHub issues the assembler gathers. That read must be
# recorded so the TRUST floor's next turn (explain_trust) sees it.
# ---------------------------------------------------------------------------

_ISSUES = {
    "high_priority_issues": [
        {
            "number": 43,
            "title": "search cluster",
            "url": "https://github.com/dinp-machine/piper-test-activity/issues/43",
        }
    ],
    "open_issue_count": 6,
}


@pytest.fixture
def assembler(monkeypatch):
    a = ContextAssembler()
    status = {"ctx": dict(_ISSUES)}

    async def _status(user_id=None):
        return dict(status["ctx"])

    async def _trust(user_id=None):
        return {"trust_profile": {"stage": 1}}

    async def _no_reminders(user_id=None):
        return {}

    async def _clock(user_id):
        return ("", "")

    import services.intent_service.context_assembler as ca

    monkeypatch.setattr(a, "_gather_status_priority_context", _status)
    monkeypatch.setattr(a, "_gather_trust_context", _trust)
    monkeypatch.setattr(a, "_gather_reminder_context", _no_reminders)
    monkeypatch.setattr(ca, "_current_time_and_date_for_user", _clock)
    a.status = status
    return a


@pytest.mark.asyncio
async def test_an_analysis_floor_read_reaches_the_trust_floor_next_turn(assembler):
    sid = f"rr-{uuid4().hex[:8]}"
    await assembler.gather_context(
        intent_category="ANALYSIS",
        user_id=_USER,
        session_id=sid,
        intent_action="analyze_repository",
    )
    trust_ctx = await assembler.gather_context(
        intent_category="TRUST", user_id=_USER, session_id=sid, intent_action="explain_trust"
    )
    assert trust_ctx["recorded_reads"] == [
        {
            "target": "dinp-machine/piper-test-activity",
            "covered": "its open issues",
            "minutes_ago": 0,
        }
    ]
    assert (
        "- Earlier this session you read dinp-machine/piper-test-activity (its open issues), just now."
        in _floor_text(trust_ctx)
    )


@pytest.mark.asyncio
async def test_sentinel_other_floor_turns_gather_issues_but_record_no_read(assembler):
    """The same baseline rides UNKNOWN and CONVERSATION turns, where nobody asked
    for a read. Those never record one."""
    sid = f"rr-{uuid4().hex[:8]}"
    for category in ("UNKNOWN", "CONVERSATION", "STATUS"):
        await assembler.gather_context(intent_category=category, user_id=_USER, session_id=sid)
    assert _recorded_reads_for(sid, _USER) == []


@pytest.mark.asyncio
async def test_a_failed_issue_read_records_nothing(assembler):
    sid = f"rr-{uuid4().hex[:8]}"
    assembler.status["ctx"] = {**_ISSUES, "open_issues_source_failed": True}
    await assembler.gather_context(intent_category="ANALYSIS", user_id=_USER, session_id=sid)
    assert _recorded_reads_for(sid, _USER) == []


@pytest.mark.asyncio
async def test_no_issues_read_records_nothing(assembler):
    sid = f"rr-{uuid4().hex[:8]}"
    assembler.status["ctx"] = {"high_priority_issues": [], "open_issue_count": 0}
    await assembler.gather_context(intent_category="ANALYSIS", user_id=_USER, session_id=sid)
    assert _recorded_reads_for(sid, _USER) == []
