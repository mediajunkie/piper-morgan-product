"""Issue #1693: create-todo task-text extraction — dash separators and the
hyphenated/spaced 'to-do' token.

PM live round 2026-08-29 (v64): routing delivered all of these to
handle_create_todo correctly, then the EXTRACTION returned "" and the user
got the didn't-catch ask — whose teach-copy suggests 'add todo: [description]',
a form whose hyphenated twin ('add to-do: ...') ALSO failed (teach-then-deny
in miniature, #1571's shape).

Fix is extraction-only (no routing/classification change): the command token
accepts 'todo'/'to-do'/'to do' in the COMMAND position, separators accept
':' and '- '/'–'/'—', and the 'new/another/one more' lead-ins bind. Task
text is captured verbatim — pinned below against normalization corruption.
"""

import pytest

from services.intent_service.todo_handlers import TodoIntentHandlers


@pytest.fixture
def handlers():
    return TodoIntentHandlers()


class TestPMFailingPhrasings1693:
    """PM's three exact live failures — each must now extract the task."""

    def test_new_todo_dash_separator(self, handlers):
        assert handlers._extract_todo_text("new todo - water the plants") == "water the plants"

    def test_one_more_hyphenated_todo_dash(self, handlers):
        assert (
            handlers._extract_todo_text("one more to-do - water the plants") == "water the plants"
        )

    def test_add_hyphenated_todo_colon(self, handlers):
        """The one that matters most: EXACTLY the teach-copy's suggested form
        plus a hyphen in 'to-do'."""
        assert handlers._extract_todo_text("add to-do: water the plants") == "water the plants"


class TestPMPassingPhrasingsNoRegression1693:
    """The two forms that PASSED in the same live round — pinned unchanged."""

    def test_add_todo_bare(self, handlers):
        assert handlers._extract_todo_text("add todo buy oat milk") == "buy oat milk"

    def test_add_a_todo_colon(self, handlers):
        assert handlers._extract_todo_text("add a todo: check the flayrod") == "check the flayrod"


class TestExtractionVariants1693:
    def test_teach_copy_form_still_works(self, handlers):
        """The teach-copy's literal suggestion 'add todo: [description]'."""
        assert handlers._extract_todo_text("add todo: water the plants") == "water the plants"

    def test_spaced_to_do_token(self, handlers):
        assert handlers._extract_todo_text("add to do: water the plants") == "water the plants"

    def test_em_dash_separator(self, handlers):
        assert handlers._extract_todo_text("add todo — water the plants") == "water the plants"

    def test_create_new_todo_dash(self, handlers):
        assert handlers._extract_todo_text("create a new todo - file the report") == (
            "file the report"
        )

    def test_bare_todo_prefix_dash(self, handlers):
        assert handlers._extract_todo_text("todo - empty the compost") == "empty the compost"

    def test_task_text_with_to_do_inside_is_verbatim(self, handlers):
        """The reason the token is accepted at the pattern level and the
        message is NEVER pre-normalized: 'to do' inside the task text must
        survive untouched."""
        assert (
            handlers._extract_todo_text("add todo: remember to do laundry")
            == "remember to do laundry"
        )

    def test_no_match_returns_empty(self, handlers):
        assert handlers._extract_todo_text("just some random text") == ""

    def test_to_downtown_is_not_a_todo_token(self, handlers):
        """'to do' inside 'to downtown' must not bind as the command token
        (the separator requires the token to END before it)."""
        assert handlers._extract_todo_text("drive to downtown") == ""


class TestReminderBoundary1693:
    """#1654 carriers unaffected — the reminder family and the todo family
    keep their extraction boundaries, both ways."""

    def test_reminder_message_does_not_extract_as_todo(self, handlers):
        assert handlers._extract_todo_text("remind me to water the plants") == ""

    def test_todo_dash_message_does_not_extract_as_reminder(self, handlers):
        assert handlers._extract_reminder_text("new todo - water the plants") is None

    def test_hyphenated_todo_message_does_not_extract_as_reminder(self, handlers):
        assert handlers._extract_reminder_text("add to-do: water the plants") is None

    def test_reminder_extraction_unchanged(self, handlers):
        assert (
            handlers._extract_reminder_text("remind me to water the plants") == "water the plants"
        )
