"""#1569 — per-item vocabulary render discipline (CXO/PPM joint design,
signed off 2026-08-13).

The rule: each item's vocabulary is set by WHICH CONTEXT KEY it arrived
through — `context:reminders:{user_id}` (-> the floor's `due_reminders` key)
means "reminder"; the todo-listing key (`context:pending_todos:{user_id}` ->
`pending_todos`) means "todo". Mixed-origin turns render as VISUALLY DISTINCT
sections (todo list, then a separate "Also due:" reminder block) — never one
flattened list — and the floor prompt's instructions carry the vocabulary
rule so the LLM doesn't reclassify an item mid-thread.

Layer honesty (m-43): these assert on the PROMPT the floor actually builds
(`_format_domain_context` output) — the render-discipline layer this design
changes. What the LLM does with the instruction is the layer above; the
instruction being present, correct, and per-origin is what's testable
deterministically. No new store, no schema change, no per-item data field
(the design's own constraint) — asserted by construction: the inputs here
are exactly the pre-existing context keys.
"""

from services.intent_service.conversational_floor import ConversationalFloor


def _render(domain_context):
    return ConversationalFloor()._format_domain_context(domain_context)


_MIXED = {
    "due_reminders": ["submit the report"],
    "reminder_count": 1,
    "pending_todos": [{"text": "review the PR"}, {"text": "update the roadmap"}],
}


class TestReminderVocabulary:
    def test_reminder_block_carries_reminder_vocabulary_rule(self):
        out = _render({"due_reminders": ["submit the report"], "reminder_count": 1})
        assert "call it a 'reminder'" in out
        assert "never a 'todo'" in out

    def test_reminder_vocabulary_forbids_mid_thread_reclassification(self):
        out = _render({"due_reminders": ["submit the report"], "reminder_count": 1})
        assert "do not reclassify it mid-thread" in out


class TestTodoVocabulary:
    def test_todo_section_is_titled_with_count_and_vocabulary(self):
        out = _render({"pending_todos": [{"text": "review the PR"}]})
        assert "PENDING TODOS (1)" in out
        assert "call each one a 'todo'" in out

    def test_todo_count_uses_gathered_denominator_when_present(self):
        """m-44: the header's count is the gathered total, not the slice."""
        out = _render(
            {"pending_todos": [{"text": "review the PR"}], "pending_todo_count": 7}
        )
        assert "PENDING TODOS (7)" in out

    def test_todo_items_render_indented_under_their_section(self):
        out = _render({"pending_todos": [{"text": "review the PR"}]})
        assert "    • Pending todo: review the PR" in out


class TestMixedOriginSectioning:
    def test_mixed_origin_instructs_two_visually_distinct_sections(self):
        out = _render(_MIXED)
        assert "VISUALLY DISTINCT" in out
        assert "'Also due:'" in out
        assert "never merged into one list" in out

    def test_mixed_origin_orders_todo_list_first_then_also_due_block(self):
        """The design's render order: todo list, then the separate
        'Also due:' reminder block."""
        out = _render(_MIXED)
        assert "the todo list first" in out

    def test_item_in_both_origins_belongs_to_the_reminder_block_only(self):
        """A due reminder IS a pending todo in the unified model — the same
        row can arrive through both keys. The instruction resolves the
        collision: reminder block only, never listed twice."""
        out = _render(_MIXED)
        assert "'Also due:' reminder block only, not twice" in out

    def test_mixed_origin_todo_header_cross_references_reminder_block(self):
        out = _render(_MIXED)
        assert "an item also listed under DUE REMINDERS above is a 'reminder'" in out


class TestSingleOriginStaysClean:
    def test_todo_only_turn_has_no_also_due_sectioning(self):
        out = _render({"pending_todos": [{"text": "review the PR"}]})
        assert "'Also due:'" not in out
        assert "DUE REMINDERS above" not in out

    def test_reminder_only_turn_has_no_mixed_origin_instruction(self):
        out = _render({"due_reminders": ["submit the report"], "reminder_count": 1})
        assert "'Also due:'" not in out
        assert "PENDING TODOS" not in out


class Test1566Canaries:
    """The #1566 surfacing properties this build must not regress."""

    def test_due_reminders_still_render_with_the_due_header(self):
        out = _render({"due_reminders": ["check in with the Lead Developer"], "reminder_count": 1})
        assert "DUE REMINDER" in out
        assert "check in with the Lead Developer" in out

    def test_truncation_denominator_still_stated(self):
        rems = [f"reminder {i}" for i in range(7)]
        out = _render({"due_reminders": rems, "reminder_count": 7})
        assert "7" in out and "more" in out

    def test_source_failed_still_renders_honest_couldnt_check(self):
        out = _render({"source_failed": True})
        assert "Reminder check FAILED" in out

    def test_empty_context_still_renders_empty(self):
        assert _render({}) == ""
