"""Issue 2427 (CXO 2026-11-23, 01M852NDAN): the confirmation for one todo added to no
project is one sentence with the title, in the attach line's voice, and ends there.

Before: "I've added that to your list. 'confirm the caterer' is now tracked. Let me know
if you want to adjust anything." (served on beta d6ed62181a): the fact twice, then a
closing offer that nothing armed.
"""

import pytest

from services.consciousness.todo_consciousness import (
    format_todo_created_conscious,
    format_todos_created_conscious,
)
from services.domain.models import Todo


def _todo(text, priority="medium"):
    return Todo(id="t-2427", text=text, priority=priority, status="pending", completed=False)


def test_one_sentence_with_the_title():
    assert (
        format_todo_created_conscious(_todo("confirm the caterer"))
        == "I've added 'confirm the caterer' to your list."
    )


@pytest.mark.parametrize("priority", ["high", "low", "urgent"])
def test_a_priority_the_person_gave_is_said_in_the_same_sentence(priority):
    line = format_todo_created_conscious(_todo("confirm the caterer", priority))
    assert line == (
        f"I've added 'confirm the caterer' to your list, and I've marked it as {priority} priority."
    )
    assert line.count(".") == 1


def test_no_closing_offer_and_no_second_statement_of_the_fact():
    line = format_todo_created_conscious(_todo("confirm the caterer"))
    for gone in ("Let me know", "adjust", "is now tracked", "added that"):
        assert gone not in line
    assert "?" not in line


def test_several_todos_end_with_the_fact_too():
    """CXO 01M853ANMP: two replies in the same voice end the same way."""
    todos = [_todo("draft brief"), _todo("book venue"), _todo("send invites")]
    line = format_todos_created_conscious(todos)
    assert (
        line == "I've added 3 todos to your list: 'draft brief', 'book venue' and 'send invites'."
    )
    assert "Let me know" not in line and "adjust" not in line
