"""
Consciousness Wrapper for Todo/List Responses

Transforms todo data into conscious narrative expression.
Part of Phase 3: Proof of Concept Transforms (#407)

Uses the consciousness injection framework to apply standup patterns
to todo responses, making them feel like Piper is present and aware.

Issue: #407 MUX-VISION-STANDUP-EXTRACT
ADR: ADR-056 Consciousness Expression Patterns
"""

from typing import List, Optional

from services.consciousness.validation import validate_mvc
from services.domain.models import Todo


def format_todo_list_conscious(todos: List[Todo], include_completed: bool = False) -> str:
    """The "show my todos" reply: the empty-list line, or the grouped list (#2219).

    #2219 (CXO 10-30) replaced the narrative ("I checked your todo list - looks like
    quite a bit going on … The first one is 'review prs'. Then there's 'review prs'.")
    that read repeats out one by one and never showed the list.
    """
    if not todos:
        return _format_empty_list_conscious()
    # #2219 (CXO): "show my todos" shows the list, with identical items grouped, never
    # one sentence per repeat.
    return format_todo_list_grouped(todos, include_completed=include_completed)


def _todo_is_done(todo: Todo) -> bool:
    return bool(getattr(todo, "completed", False) or getattr(todo, "status", "") == "completed")


def format_todo_list_grouped(todos: List[Todo], include_completed: bool = False) -> str:
    """#2219 (CXO 10-30): the list itself. ``You have 13 open todos. Here they are:``,
    then one line per distinct item in the list's order (priority, then oldest first),
    repeats grouped as ``review prs (×3)``. An item keeps its priority note; a done one
    says so. One line shown reads ``Here it is:`` (CXO 11-06 07:23)."""
    groups: List[List[Todo]] = []
    index: dict = {}
    for todo in todos:
        key = (todo.text, _todo_is_done(todo))
        if key not in index:
            index[key] = len(groups)
            groups.append([])
        groups[index[key]].append(todo)
    open_count = sum(1 for t in todos if not _todo_is_done(t))
    done_count = len(todos) - open_count
    noun = "todo" if open_count == 1 else "todos"
    here = "Here it is:" if len(groups) == 1 else "Here they are:"
    if include_completed and done_count:
        # CXO's form (#2219, ruled 11-05 19:25).
        header = f"You have {open_count} open {noun} and {done_count} done. {here}"
    else:
        header = f"You have {open_count} open {noun}. {here}"
    lines = [header]
    for group in groups:
        first = group[0]
        line = f"• {first.text}"
        if len(group) > 1:
            line += f" (×{len(group)})"
        if first.priority == "urgent":
            line += " (urgent)"
        elif first.priority == "high":
            # CXO 11-06: the Todos page names this level "High".
            line += " (high)"
        if _todo_is_done(first):
            line += " ✓ done"
        lines.append(line)
    return "\n".join(lines)


def format_next_todo_line(open_todos: List[Todo]) -> str:
    """#2219 (CXO 11-05 20:47, kept 11-06): the one next todo, the first open row in
    the list's own order, with its repeats counted.

    ``Your next todo is "review prs" (×3). Say "show my todos" for the rest.``"""
    first = open_todos[0]
    copies = sum(1 for t in open_todos if t.text == first.text)
    repeat = f" (×{copies})" if copies > 1 else ""
    return f'Your next todo is "{first.text}"{repeat}. Say "show my todos" for the rest.'


def format_completed_todos(done_todos: List[Todo]) -> str:
    """#2295 (CXO 11-06 07:35): only the completed todos, never "open"."""
    if not done_todos:
        return "You haven't completed any todos yet."
    groups: List[List[Todo]] = []
    index: dict = {}
    for todo in done_todos:
        if todo.text not in index:
            index[todo.text] = len(groups)
            groups.append([])
        groups[index[todo.text]].append(todo)
    count = len(done_todos)
    noun = "todo" if count == 1 else "todos"
    here = "Here it is:" if len(groups) == 1 else "Here they are:"
    lines = [f"You have {count} completed {noun}. {here}"]
    for group in groups:
        line = f"• {group[0].text}"
        if len(group) > 1:
            line += f" (×{len(group)})"
        lines.append(line + " ✓")
    return "\n".join(lines)


def format_todo_created_conscious(todo: Todo) -> str:
    """
    Format todo creation confirmation with consciousness.

    Transforms from:
        "✓ Added todo #a1b2c3d4: Review PR (priority: high)"

    To:
        "I've added that to your list. 'Review PR' is now tracked,
         and I've marked it as high priority based on what you said.
         Let me know if you want to adjust anything."
    """
    sections = []

    # Identity statement with what was done
    sections.append(f"I've added that to your list.")

    # What was captured
    priority_note = ""
    if todo.priority != "medium":
        priority_note = f", and I've marked it as {todo.priority} priority"
    sections.append(f"'{todo.text}' is now tracked{priority_note}.")

    # Dialogue invitation
    sections.append("Let me know if you want to adjust anything.")

    return " ".join(sections)


def format_todo_completed_conscious(todo: Todo) -> str:
    """
    Format todo completion with consciousness.

    Transforms from:
        "✓ Completed: Review PR"

    To:
        "Nice - I've marked 'Review PR' as done. Good progress!"

    CXO ruling 2026-10-05: the closing "What's next on your list?" was an
    unarmed question (nothing resolved a reply to it) and read oddly after a
    multi-item ask; the warmth stays, the question goes.
    """
    return f"Nice - I've marked '{todo.text}' as done. Good progress!"


def format_todo_deleted_conscious(todo_text: str) -> str:
    """
    Format todo deletion with consciousness.

    Transforms from:
        "✓ Removed: Review PR"

    To:
        "I've removed 'Review PR' from your list. If that was a mistake,
         just add it again. Anything else you need?"
    """
    return (
        f"I've removed '{todo_text}' from your list. "
        "If that was a mistake, just add it again. Anything else you need?"
    )


def format_next_todo_conscious(todo: Todo, total_count: int) -> str:
    """
    Format "next todo" response with consciousness.

    Transforms from:
        "Your next todo: 🔴
         Review PR
         Due: 2026-01-25"

    To:
        "Looking at your list, I'd suggest tackling 'Review PR' next -
         it's marked urgent and due on January 25th. You have 5 other
         items after this one. Does that priority feel right?"
    """
    sections = []

    # Opening with source attribution
    sections.append("Looking at your list, I'd suggest tackling")

    # The todo with context
    priority_context = ""
    if todo.priority == "urgent":
        priority_context = " - it's marked urgent"
    elif todo.priority == "high":
        priority_context = " - it's high priority"

    due_context = ""
    if todo.due_date:
        due_context = f" and due on {todo.due_date.strftime('%B %d')}"

    sections[0] += f" '{todo.text}' next{priority_context}{due_context}."

    # Remaining context
    remaining = total_count - 1
    if remaining > 0:
        item_word = "item" if remaining == 1 else "items"
        sections.append(f"You have {remaining} other {item_word} after this one.")

    # Dialogue invitation
    sections.append("Does that priority feel right?")

    return " ".join(sections)


def _format_empty_list_conscious() -> str:
    """Format empty todo list with consciousness.

    Issue #1096 slice 2 (Pattern-073 discipline): drop "your mind is clear" —
    the system knows the DB returned zero matching todos, not that the user's
    mind is clear (a categorical claim that goes beyond verified knowledge).
    """
    return (
        "I checked your todo list and it's empty. "
        "If you want to capture something, just say 'add todo: [your task]'. "
        "Or I can help you think about what might need attention."
    )


def _fix_mvc_gaps(narrative: str, mvc_result) -> str:
    """Fix any missing MVC requirements."""
    fixed = narrative

    if "identity" in mvc_result.missing:
        fixed = "I took a look at your todos. " + fixed

    if "uncertainty" in mvc_result.missing:
        # Add "looks like" if not present
        fixed = fixed.replace("you have", "it looks like you have", 1)

    if "invitation" in mvc_result.missing:
        fixed = fixed.rstrip(".") + ". Anything you'd like me to adjust?"

    if "attribution" in mvc_result.missing:
        fixed = "Looking at your todo list, " + fixed

    return fixed


def format_todos_created_conscious(todos: list) -> str:
    """#2094: several todos from one message, every one named.

    "I've added 3 todos to your list: 'draft brief', 'book venue' and 'send invites'.
    Let me know if you want to adjust anything."
    """
    names = [f"'{t.text}'" for t in todos]
    if len(names) == 1:
        joined = names[0]
    else:
        joined = ", ".join(names[:-1]) + " and " + names[-1]
    return (
        f"I've added {len(todos)} todos to your list: {joined}. "
        "Let me know if you want to adjust anything."
    )
