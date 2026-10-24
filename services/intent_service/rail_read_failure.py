"""#2151 step 3, RAIL-FALLTHROUGH: a READ rail entry that raises is a FAILED read.

Before this, ``dispatch_workflow`` caught any handler exception and returned None,
which the chat rail treats as "not mine": the turn fell through to category routing
and the conversational floor, which answered as if the read had never been asked
for (and could say "none" about data it never saw). Arch's ruling (#2151, comment
6377720778): an exception on the rail is a failed outcome and never falls through.

The words are CXO's (#2151, 2026-10-23 17:55), one template so renders cannot
drift; the house style is the "I couldn't check <X> just now" line already used
in canonical_handlers. Each READ entry names its source and what can't be said:

    "I couldn't check <source_noun> just now, so I can't say <unknown_clause>.
     Try again in a moment; if it keeps failing, tell us."

ONE registry, keyed by the entry's canonical (first-registered) action name.
Every canonical action-triggered READ entry must appear either here or in
``NO_USER_DATA_READ`` (a reason it reads nothing of the user's: a failure there
makes no claim about their data, so it may still fall through). The pin:
tests/unit/services/intent_service/test_rail_read_failure_2151.py.

WRITE and DESTRUCTIVE entries are out of this unit: their failure wording
("did it happen or not?") is a different line, not yet worded.
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple

RAIL_READ_FAILED_TEMPLATE = (
    "I couldn't check {source_noun} just now, so I can't say {unknown_clause}. "
    "Try again in a moment; if it keeps failing, tell us."
)

# canonical action → (source_noun, unknown_clause)
RAIL_READ_SOURCES: Dict[str, Tuple[str, str]] = {
    "analyze_blockers": ("your projects and GitHub issues", "what is blocking them"),
    "analyze_commits": ("your GitHub commits", "what changed in the code"),
    "analyze_data": ("your GitHub activity", "what your repository metrics are"),
    "analyze_document": ("your documents", "what that document says"),
    "attention_query": ("your tasks, meetings and projects", "what needs your attention"),
    "changes_query": ("your recent activity", "what changed"),
    "check_completion_status": ("your completed work", "when it was finished"),
    "clear_todos": ("your tasks and reminders", "which ones would be cleared"),
    "compare_documents": ("your uploaded files", "how those documents compare"),
    "explain_trust": ("how we've worked together so far", "how much I can do on my own yet"),
    "explain_suggestion": ("our earlier conversation", "why I suggested that"),
    "generate_content": ("your project activity", "what the content should cover"),
    "generate_report": ("your GitHub activity", "what the report would show"),
    "get_capabilities": ("your connected tools", "what I can do with them right now"),
    "get_current_time": ("your timezone and calendar", "what time it is for you"),
    "get_default_repo": ("your settings", "which repository is your default"),
    "get_feature_info": ("your connected tools", "how that feature is set up for you"),
    "get_identity": ("your connected tools and projects", "what I'm set up to help you with"),
    "get_memory": ("what I've stored about you", "what I remember"),
    "learn_pattern": ("your history", "what patterns it shows"),
    "list_archived_projects": ("your archived projects", "which ones are archived"),
    "list_branches": ("your GitHub branches", "which branches there are"),
    "list_issues": ("your GitHub issues", "which ones are open"),
    "list_labels": ("your GitHub labels", "which labels there are"),
    "list_milestones": ("your GitHub milestones", "which ones are open"),
    "list_projects": ("your projects", "which projects you have"),
    "list_prs": ("your GitHub pull requests", "which ones are open"),
    "list_releases": ("your GitHub releases", "what the latest release is"),
    "list_reminders_query": ("your reminders", "what is coming up"),
    "list_repos": ("your linked repositories", "which repositories are linked"),
    "list_todos_query": ("your Piper tasks", "what is due"),
    "local_git_status_query": ("the local repository", "what its status is"),
    "meeting_time": ("your calendar", "what is on it"),
    "productivity": ("your completed work", "what you got done"),
    "pull_insights": ("what I've learned about you", "what I've noticed"),
    "recurring_meetings": ("your calendar", "which meetings recur"),
    "review_issue": ("that GitHub issue", "what it says"),
    "search_documents": ("your Notion pages", "whether any match"),
    "search_projects": ("your projects", "whether any match"),
    "session_activity_query": ("this session's activity", "what we've created"),
    "shipped_this_week": ("your GitHub activity", "what shipped this week"),
    "show_standup": ("your connected tools", "what goes in your standup"),
    "stale_prs": ("your GitHub pull requests", "which ones need review"),
    "summarize_document": ("your uploaded files", "what that document says"),
    "week_calendar": ("your calendar", "what your week looks like"),
    "write_stakeholder_update": ("your project progress", "what the update should report"),
}

# canonical action → why a failure makes no claim about the user's own data.
NO_USER_DATA_READ: Dict[str, str] = {
    "prioritize": "computes over the items in the request itself",
    "strategic_planning": "plans from the request's own goal and timeframe",
    "get_contextual_guidance": "advice, no claim about stored data",
}


def rail_read_failed_message(canonical_action: str) -> Optional[str]:
    """The failed-read reply for a READ entry, or None when it reads no user data."""
    words = RAIL_READ_SOURCES.get(canonical_action)
    if words is None:
        return None
    source_noun, unknown_clause = words
    return RAIL_READ_FAILED_TEMPLATE.format(source_noun=source_noun, unknown_clause=unknown_clause)
