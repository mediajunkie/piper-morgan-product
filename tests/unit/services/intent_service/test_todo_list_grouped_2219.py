"""#2219 (CXO, from PA's row-2 run on alpha 10-30): "show my todos" shows the list, with
identical items grouped, and a complete confirm says the noun the person used.

PA's case: 13 open todos, three of them "review prs". The old reply read "The first one
is 'review prs'. Then there's 'review prs'. Also 'review prs'. … Plus 8 more" and never
showed the list; "Complete the PR review todo" was confirmed as "Complete 3 reminders".
"""

from types import SimpleNamespace

from services.consciousness.todo_consciousness import format_todo_list_conscious
from services.intent_service.todo_handlers import _batch_confirm_question, _confirm_question


def _todo(text, priority="medium", completed=False):
    return SimpleNamespace(text=text, priority=priority, completed=completed, status="")


def _pas_list():
    return [_todo("review prs")] * 3 + [_todo(f"task {i}") for i in range(10)]


def test_pas_thirteen_todos_are_shown_with_the_repeat_grouped():
    reply = format_todo_list_conscious(_pas_list())
    lines = reply.split("\n")
    assert lines[0] == "You have 13 open todos. Here they are:"
    assert lines[1] == "• review prs (×3)"
    assert lines[2:] == [f"• task {i}" for i in range(10)]
    assert reply.count("review prs") == 1
    assert "Plus" not in reply and "The first one is" not in reply


def test_one_todo_is_singular_and_notes_ride_their_line():
    assert format_todo_list_conscious([_todo("ship it", "urgent")]) == (
        "You have 1 open todo. Here they are:\n• ship it (urgent)"
    )
    reply = format_todo_list_conscious([_todo("a", "high"), _todo("a", "high")])
    assert reply.endswith("• a (×2) (important)")


def test_a_done_item_is_its_own_group_and_says_so():
    todos = [_todo("a"), _todo("a", completed=True)]
    reply = format_todo_list_conscious(todos, include_completed=True)
    assert reply.split("\n") == [
        "You have 1 open todo and 1 done. Here they are:",
        "• a",
        "• a ✓ done",
    ]


def test_the_empty_list_line_is_unchanged():
    assert format_todo_list_conscious([]).startswith("I checked your todo list and it's empty.")


def test_a_complete_confirm_says_the_noun_the_person_used():
    targets = ["review prs"] * 3
    assert _batch_confirm_question(targets, [], "todo").startswith("Complete 3 todos:")
    assert _batch_confirm_question(targets, [], "reminder").startswith("Complete 3 reminders:")


def test_todo_is_the_default_and_the_persons_word_wins():
    """CXO 2026-11-05 19:25: "todo" by default, no hyphen; "reminder" or "remind" wins."""
    from services.intent_service.reminder_copy import copy_noun

    assert _confirm_question("Complete", ["a", "b"], []).startswith("Complete 2 todos:")
    assert copy_noun("Complete the PR review todo") == "todo"
    assert copy_noun("delete the first reminder") == "reminder"
    assert copy_noun("remind me to call mom") == "reminder"
    assert copy_noun("finish that task") == "todo"


def test_the_done_header_counts_in_the_noun():
    two_open = [_todo("a"), _todo("b"), _todo("c", completed=True)]
    assert format_todo_list_conscious(two_open, include_completed=True).startswith(
        "You have 2 open todos and 1 done. Here they are:"
    )
