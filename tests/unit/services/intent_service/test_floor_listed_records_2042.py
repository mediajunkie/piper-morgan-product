"""#2042 rung 2 — the floor's listed-records event is emitted, log-only, at the seam.

Pins, in order:
  * the pure helpers (``#N`` extraction, list-line count, context reads);
  * the two served shapes the diagnosis names — #2184 (real numbers re-labelled:
    every reference IS in the prompt, the event still fires and names the reads
    that ran) and #2040 (numbers in no slice: ``unsourced_references`` names them);
  * the seam: ``ConversationalFloor.respond()`` driven with a stubbed model logs
    ``floor_listed_records`` with the payload, and a plain one-line reply logs
    nothing; the message is byte-identical either way (log-only).
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock

from structlog.testing import capture_logs

from services.intent_service.conversational_floor import ConversationalFloor, FloorContext
from services.intent_service.floor_listed_records import (
    context_reads,
    count_list_lines,
    listed_records_event,
    record_references,
)

# The #2184 served reply (alpha a1f46faafc, 10:12 PT 2026-10-28), shape only.
REPLY_2184 = (
    "Here are the 3 open issues in the MVP milestone:\n"
    "- **#2183**: Chat ignores a count\n"
    "- **#2151**: Sweep: every reply that reads user data\n"
    "- **#2018**: Settings → Integrations\n\n"
    "Notably, two of these (#2183 and #2151) are also in your top high-priority list."
)
# What the floor had in hand: the high-priority slice (numbers) + the milestones slice (counts).
PROMPT_2184 = (
    "Recent conversation:\nUser: can you show me issues from just one milestone?\n"
    "Piper: Which one? MVP (3 open), Production (27 open), ...\n"
    "[Available context]\n"
    "- High-priority open issues (5 open; top 5 shown):\n"
    "    • #2183 [P1]: Chat ignores a count\n"
    "    • #2151 [P1]: Sweep\n"
    "    • #2018 [P1]: Settings\n"
    "    • #1595 [P1]: EPIC\n"
    "    • #1386 [P1]: BETA-GATE\n"
    "- Active milestones (6 open):\n"
    "    • MVP — 3 open / 61 closed\n"
    "User: MVP"
)
PROVENANCE_2184 = {
    "high_priority_issues": {"source": "GitHubIntegrationRouter", "filter": "priority:high"},
    "active_milestones": {"source": "GitHubIntegrationRouter", "filter": "state:open"},
}


class TestHelpers:
    def test_references_strip_markdown_and_punctuation_and_dedupe(self):
        assert record_references("see **#2183**: and (#2018), then #2183 again; #abc #") == [
            "#2183",
            "#2018",
        ]

    def test_no_references_in_plain_prose(self):
        assert record_references("You have 261 open issues assigned to you.") == []

    def test_list_lines_count_markers_and_numbers(self):
        text = "Here:\n- a\n* b\n• c\n1. d\n2) e\nnot a list\n"
        assert count_list_lines(text) == 5

    def test_context_reads_name_key_and_filter_and_flag_unattributed_keys(self):
        reads = context_reads(
            PROVENANCE_2184,
            {"high_priority_issues": [], "active_milestones": [], "pending_todos": [{"text": "x"}]},
        )
        assert reads == [
            "active_milestones[state:open]",
            "high_priority_issues[priority:high]",
            "pending_todos[?]",
        ]


class TestShapes:
    def test_2184_shape_fires_with_every_reference_sourced_and_the_reads_named(self):
        ev = listed_records_event(REPLY_2184, PROMPT_2184, PROVENANCE_2184)
        assert ev is not None
        assert ev["references"] == ["#2183", "#2151", "#2018"]
        assert ev["reference_count"] == 3
        # The numbers were real and in the prompt: the 10-15 "not in context"
        # guard would have been silent here. The event is not.
        assert ev["unsourced_references"] == []
        assert ev["list_lines"] == 3
        assert "high_priority_issues[priority:high]" in ev["context_reads"]
        assert "active_milestones[state:open]" in ev["context_reads"]

    def test_2040_shape_names_the_unsourced_numbers(self):
        reply = "You've got 7 open total — here are the two I didn't show yet: #2 and #1."
        prompt = "Recent conversation:\nPiper: You have 7 open issues: #7, #6, #5, #4, #3.\nUser: show me the rest"
        history = [{"role": "assistant", "content": "You have 7 open issues: #7, #6, #5, #4, #3."}]
        ev = listed_records_event(reply, prompt, {}, {}, history, "show me the rest")
        assert ev is not None
        assert ev["unsourced_references"] == ["#2", "#1"]
        assert ev["reference_sources"] == {"#2": ["absent"], "#1": ["absent"]}

    def test_sources_name_every_holder_context_then_history_then_user(self):
        from services.intent_service.floor_listed_records import reference_sources

        ctx = {
            "blocked_items": [{"number": 11, "title": "x"}],
            "pending_todos": [{"text": "see #12"}],
        }
        hist = [{"role": "assistant", "content": "earlier: #13"}]
        got = reference_sources(["#11", "#12", "#13", "#14", "#15"], ctx, hist, "what about #14?")
        assert got == {
            "#11": ["blocked_items"],
            "#12": ["pending_todos"],
            "#13": ["history"],
            "#14": ["user"],
            "#15": ["absent"],
        }

    def test_a_number_in_two_slices_names_both(self):
        # Arch's 11:02 refinement: the offline criterion asks whether ANY source
        # matches the asked scope, so a first-match (alphabetical) would mis-flag
        # a legitimate list. Every holder is recorded, history and user too.
        from services.intent_service.floor_listed_records import reference_sources

        ctx = {
            "high_priority_issues": [{"number": 2018, "title": "Settings"}],
            "blocked_items": [{"number": 2018, "title": "Settings"}],
        }
        hist = [{"role": "assistant", "content": "You asked about #2018 earlier."}]
        got = reference_sources(["#2018"], ctx, hist, "and #2018?")
        assert got == {"#2018": ["blocked_items", "high_priority_issues", "history", "user"]}

    def test_one_sourced_reference_and_no_list_is_not_an_enumeration(self):
        assert (
            listed_records_event("Sure — #2018 is the recovery issue.", "User: what is #2018?")
            is None
        )

    def test_one_unsourced_reference_still_fires(self):
        ev = listed_records_event("That's tracked as #4242.", "User: where is that tracked?")
        assert ev is not None and ev["unsourced_references"] == ["#4242"]

    def test_a_todo_list_from_context_fires_as_an_enumeration_with_its_read_named(self):
        # Log-only by design: a legitimate read-back of pending todos is an
        # enumeration too. The discrimination (was a read of the ASKED scope
        # run?) is a query over the events, not a judgment here.
        reply = "On your plate:\n- draft brief\n- book venue"
        ev = listed_records_event(
            reply,
            "- Pending todos:\n    • draft brief\n    • book venue\nUser: what's on my plate?",
            {"pending_todos": {"source": "TodoManagementService", "filter": "open"}},
        )
        assert ev is not None
        assert ev["reference_count"] == 0 and ev["list_lines"] == 2
        assert ev["context_reads"] == ["pending_todos[open]"]


def _floor_returning(text: str) -> ConversationalFloor:
    llm = MagicMock()
    llm.complete = AsyncMock(return_value=text)
    return ConversationalFloor(
        llm_client=llm, system_prompt_base="You are Piper Morgan (test base)."
    )


def _ctx(user_message: str, **kw) -> FloorContext:
    return FloorContext(user_message=user_message, session_id="s2042", user_id="u2042", **kw)


class TestSeam:
    def test_enumerating_reply_logs_the_event_and_is_not_rewritten(self):
        floor = _floor_returning(REPLY_2184)
        ctx = _ctx(
            "MVP",
            intent_category="STATUS",
            intent_action="none",
            conversation_history=[
                {"role": "user", "content": "can you show me issues from just one milestone?"},
                {"role": "assistant", "content": "Which one? MVP (3 open), Production (27 open)"},
            ],
            domain_context={
                "high_priority_issues": [
                    {"number": 2183, "title": "Chat ignores a count"},
                    {"number": 2151, "title": "Sweep"},
                    {"number": 2018, "title": "Settings"},
                ],
                "active_milestones": [
                    {"title": "MVP", "number": 7, "open_issues": 3, "closed_issues": 61}
                ],
            },
            domain_context_provenance=PROVENANCE_2184,
        )
        with capture_logs() as events:
            resp = asyncio.run(floor.respond(ctx))
        listed = [e for e in events if e.get("event") == "floor_record_references"]
        assert len(listed) == 1, [e.get("event") for e in events]
        ev = listed[0]
        assert ev["session_id"] == "s2042"
        assert ev["intent_category"] == "STATUS"
        assert ev["references"] == ["#2183", "#2151", "#2018"]
        assert ev["unsourced_references"] == []
        assert "high_priority_issues[priority:high]" in ev["context_reads"]
        # Arch's mis-attribution datum: each number names the slice it came from.
        assert ev["reference_sources"] == {
            "#2183": ["high_priority_issues"],
            "#2151": ["high_priority_issues"],
            "#2018": ["high_priority_issues"],
        }
        # Log-only: the user sees exactly what the model composed.
        assert resp.message == REPLY_2184
        assert [e for e in events if e.get("event") == "floor_record_references_error"] == []

    def test_plain_reply_logs_nothing(self):
        floor = _floor_returning("I couldn't pull up that list just now — want me to check again?")
        with capture_logs() as events:
            resp = asyncio.run(floor.respond(_ctx("show the MVP issues", intent_category="STATUS")))
        assert [e for e in events if e.get("event") == "floor_record_references"] == []
        assert resp.message.startswith("I couldn't pull up that list just now")
