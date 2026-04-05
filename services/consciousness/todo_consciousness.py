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
    """
    Format todo list with consciousness.

    Transforms from:
        "Your active todos:
         1. ○ Review PR 🟡
         2. ○ Fix bug
         Total: 2 active todos"

    To:
        "I checked your todo list - looks like you have 2 things on your plate.

         The Review PR item seems important based on the priority you set.
         There's also the Fix bug task waiting.

         How would you like to tackle these? Let me know if you want to
         reprioritize anything."

    Args:
        todos: List of Todo objects
        include_completed: Whether to show completed todos

    Returns:
        Conscious narrative string
    """
    if not todos:
        return _format_empty_list_conscious()

    # Analyze the todos for context
    urgent_count = sum(1 for t in todos if t.priority == "urgent")
    high_count = sum(1 for t in todos if t.priority == "high")
    total_count = len(todos)

    # Build the narrative
    sections = []

    # Opening with source transparency
    sections.append(_build_opening(total_count, urgent_count, high_count))

    # Discovery - the todos themselves
    sections.append(_build_todo_discovery(todos))

    # Closing with dialogue invitation
    sections.append(_build_closing(total_count, urgent_count))

    narrative = "\n\n".join(sections)

    # Validate MVC and fix if needed
    mvc_result = validate_mvc(narrative)
    if not mvc_result.passes:
        narrative = _fix_mvc_gaps(narrative, mvc_result)

    return narrative


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
        "Nice - I've marked 'Review PR' as done. Good progress!
         What's next on your list?"
    """
    return f"Nice - I've marked '{todo.text}' as done. Good progress! What's next on your list?"


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
    """Format empty todo list with consciousness."""
    return (
        "I checked your todo list and it's empty - your mind is clear! "
        "If you want to capture something, just say 'add todo: [your task]'. "
        "Or I can help you think about what might need attention."
    )


def _build_opening(total: int, urgent: int, high: int) -> str:
    """Build opening with source transparency and epistemic humility."""
    # Source attribution
    opening = "I checked your todo list"

    # Epistemic assessment
    if urgent > 0:
        opening += (
            f" - looks like you have {total} things on your plate, with {urgent} marked urgent"
        )
    elif high > 0:
        opening += (
            f" - looks like you have {total} things on your plate, with {high} flagged as important"
        )
    elif total > 5:
        opening += f" - looks like quite a bit going on with {total} items"
    else:
        opening += f" - looks like you have {total} {'thing' if total == 1 else 'things'} to track"

    opening += "."
    return opening


def _build_todo_discovery(todos: List[Todo]) -> str:
    """Build the discovery section with todos."""
    lines = []

    # Show first few todos with context
    for i, todo in enumerate(todos[:5]):
        if i == 0:
            prefix = "The first one is"
        elif i == 1:
            prefix = "Then there's"
        elif i == 2:
            prefix = "Also"
        else:
            prefix = "And"

        # Priority context
        priority_note = ""
        if todo.priority == "urgent":
            priority_note = " (urgent)"
        elif todo.priority == "high":
            priority_note = " (important)"

        # Completion state (Issue #904)
        completion_note = ""
        if getattr(todo, "completed", False) or getattr(todo, "status", "") == "completed":
            completion_note = " ✓ done"

        # Truncate long text
        text = todo.text[:50] + "..." if len(todo.text) > 50 else todo.text
        lines.append(f"{prefix} '{text}'{priority_note}{completion_note}.")

    # If more than 5, summarize the rest
    if len(todos) > 5:
        remaining = len(todos) - 5
        item_word = "item" if remaining == 1 else "items"
        lines.append(f"Plus {remaining} more {item_word}.")

    return " ".join(lines)


def _build_closing(total: int, urgent: int) -> str:
    """Build closing with synthesis and dialogue invitation."""
    if urgent > 0:
        return "Those urgent items might be worth tackling first. How would you like to approach today?"
    elif total > 5:
        return "That's a full list. Want help prioritizing, or should I focus on a specific area?"
    else:
        return (
            "How would you like to tackle these? Let me know if you want to reprioritize anything."
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
