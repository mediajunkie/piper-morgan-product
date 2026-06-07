"""
Action Registry — Issue #915/#916/#919 systemic fix.

Maps every (category, action) pair emitted by the pre-classifier to its
handler disposition. Provides startup validation to prevent silent regressions
when new patterns are added without handlers.

Design principle: "Don't classify what you can't handle."
If the pre-classifier emits an action, the registry MUST have an entry for it.
If no specialized handler exists, route to the conversational floor.
"""

from enum import Enum
from typing import Optional


class ActionDisposition(Enum):
    """What should happen when this (category, action) pair is encountered."""

    CANONICAL = "canonical"  # Handled by CanonicalHandlers (fast-path/deterministic)
    FLOOR = "floor"  # Route to conversational floor with context assembly
    WORKFLOW = "workflow"  # Requires workflow creation + handler dispatch


# Complete registry of all pre-classifier (category, action) pairs.
#
# Every action string emitted by PreClassifier.pre_classify() MUST have
# an entry here. The startup validator enforces this.
#
# When adding a new pre-classifier pattern:
#   1. Add the pattern to pre_classifier.py
#   2. Add the (category, action) entry HERE
#   3. If disposition is HANDLER/WORKFLOW, implement the handler
#   4. If disposition is FLOOR, the floor will handle it conversationally
#
ACTION_REGISTRY: dict[tuple[str, str], ActionDisposition] = {
    # ---- CONVERSATION ----
    ("CONVERSATION", "greeting"): ActionDisposition.CANONICAL,
    ("CONVERSATION", "farewell"): ActionDisposition.CANONICAL,
    ("CONVERSATION", "thanks"): ActionDisposition.CANONICAL,
    # ---- IDENTITY ----
    ("IDENTITY", "get_identity"): ActionDisposition.CANONICAL,
    # ---- DISCOVERY ----
    ("DISCOVERY", "get_capabilities"): ActionDisposition.CANONICAL,
    # ---- TRUST ----
    ("TRUST", "explain_trust"): ActionDisposition.CANONICAL,
    # ---- MEMORY ----
    ("MEMORY", "get_memory"): ActionDisposition.CANONICAL,
    # Issue #1030 INSIGHT-PULL: "What have you learned about X?" — FLOOR-routed
    # with InsightRepository context enrichment in context_assembler.
    ("MEMORY", "pull_insights"): ActionDisposition.FLOOR,
    # ---- TEMPORAL ----
    ("TEMPORAL", "get_current_time"): ActionDisposition.CANONICAL,
    # ---- STATUS ----
    ("STATUS", "get_project_status"): ActionDisposition.CANONICAL,
    # ---- PRIORITY ----
    ("PRIORITY", "get_top_priority"): ActionDisposition.CANONICAL,
    # ---- GUIDANCE ----
    ("GUIDANCE", "get_contextual_guidance"): ActionDisposition.CANONICAL,
    # ---- PORTFOLIO ----
    ("PORTFOLIO", "manage_portfolio"): ActionDisposition.CANONICAL,
    ("PORTFOLIO", "manage_repos"): ActionDisposition.CANONICAL,
    # ---- PROVENANCE ----
    # Issue #1030 R4: "Why did you suggest that?" — CANONICAL because it's pure
    # deterministic lookup (no LLM needed). Handler reads
    # ConversationContext.turn_provenance and formats colleague-prose citation.
    ("PROVENANCE", "explain_suggestion"): ActionDisposition.CANONICAL,
    # ---- QUERY: Calendar ----
    ("QUERY", "meeting_time"): ActionDisposition.WORKFLOW,
    ("QUERY", "recurring_meetings"): ActionDisposition.WORKFLOW,
    ("QUERY", "week_calendar"): ActionDisposition.WORKFLOW,
    # ---- QUERY: GitHub ----
    ("QUERY", "shipped_query"): ActionDisposition.WORKFLOW,
    ("QUERY", "stale_prs_query"): ActionDisposition.WORKFLOW,
    ("QUERY", "close_issue_query"): ActionDisposition.WORKFLOW,
    ("QUERY", "reopen_issue_query"): ActionDisposition.WORKFLOW,
    ("QUERY", "comment_issue_query"): ActionDisposition.WORKFLOW,
    ("QUERY", "list_issues_query"): ActionDisposition.WORKFLOW,
    ("QUERY", "list_prs_query"): ActionDisposition.WORKFLOW,
    ("QUERY", "review_issue_query"): ActionDisposition.WORKFLOW,
    # Issue #1039: GitHub milestone + release listing
    ("QUERY", "list_milestones_query"): ActionDisposition.WORKFLOW,
    ("QUERY", "list_releases_query"): ActionDisposition.WORKFLOW,
    # Issue #1040: GitHub label + branch listing
    ("QUERY", "list_labels_query"): ActionDisposition.WORKFLOW,
    ("QUERY", "list_branches_query"): ActionDisposition.WORKFLOW,
    # ---- QUERY: Documents ----
    ("QUERY", "update_document_query"): ActionDisposition.WORKFLOW,
    # ---- QUERY: Contextual ----
    ("QUERY", "changes_query"): ActionDisposition.WORKFLOW,
    ("QUERY", "attention_query"): ActionDisposition.WORKFLOW,
    # ---- QUERY: Productivity ----
    ("QUERY", "productivity_query"): ActionDisposition.WORKFLOW,
    # ---- QUERY: Todos ----
    ("QUERY", "list_todos_query"): ActionDisposition.WORKFLOW,
    ("QUERY", "list_completed_todos"): ActionDisposition.WORKFLOW,
    ("QUERY", "next_todo_query"): ActionDisposition.WORKFLOW,
    # ---- QUERY: Feature Info (was stub → now floor) ----
    ("QUERY", "get_feature_info"): ActionDisposition.FLOOR,
    # ---- EXECUTION ----
    ("EXECUTION", "complete_todo"): ActionDisposition.WORKFLOW,
    # ---- ANALYSIS (was stub → now floor) ----
    ("ANALYSIS", "analyze_blockers"): ActionDisposition.FLOOR,
}

# Example messages for each action (used by smoke tests and documentation).
# One realistic user message per (category, action) pair.
ACTION_EXAMPLES: dict[tuple[str, str], str] = {
    ("CONVERSATION", "greeting"): "Good morning!",
    ("CONVERSATION", "farewell"): "Goodbye, talk later",
    ("CONVERSATION", "thanks"): "Thanks for your help",
    ("IDENTITY", "get_identity"): "Who are you?",
    ("DISCOVERY", "get_capabilities"): "What can you do?",
    ("TRUST", "explain_trust"): "How do you handle my data?",
    ("MEMORY", "get_memory"): "What do you remember about me?",
    ("MEMORY", "pull_insights"): "What have you learned about my work style?",
    ("TEMPORAL", "get_current_time"): "What time is it?",
    ("STATUS", "get_project_status"): "What's the project status?",
    ("PRIORITY", "get_top_priority"): "What should I work on first?",
    ("GUIDANCE", "get_contextual_guidance"): "How should I approach this sprint?",
    ("PORTFOLIO", "manage_portfolio"): "List my projects",
    ("PORTFOLIO", "manage_repos"): "Add a GitHub repo",
    ("PROVENANCE", "explain_suggestion"): "Why did you suggest that?",
    ("QUERY", "meeting_time"): "How much time do I spend in meetings today?",
    ("QUERY", "recurring_meetings"): "Show me my recurring meetings",
    ("QUERY", "week_calendar"): "What does my week look like?",
    ("QUERY", "shipped_query"): "What shipped this week?",
    ("QUERY", "stale_prs_query"): "Show me stale pull requests",
    ("QUERY", "close_issue_query"): "Close issue #42",
    ("QUERY", "reopen_issue_query"): "Reopen issue #42",
    ("QUERY", "comment_issue_query"): "Add a comment to issue #42",
    ("QUERY", "list_issues_query"): "List open issues",
    ("QUERY", "list_prs_query"): "Show me open pull requests",
    ("QUERY", "review_issue_query"): "Show me issue #42",
    ("QUERY", "list_milestones_query"): "Show milestones",
    ("QUERY", "list_releases_query"): "Recent releases",
    ("QUERY", "list_labels_query"): "List labels",
    ("QUERY", "list_branches_query"): "Show branches",
    ("QUERY", "update_document_query"): "Update the project roadmap document",
    ("QUERY", "changes_query"): "What changed since yesterday?",
    ("QUERY", "attention_query"): "What needs my attention?",
    ("QUERY", "productivity_query"): "How productive was I this week?",
    ("QUERY", "list_todos_query"): "Show me my todos",
    ("QUERY", "list_completed_todos"): "Show me completed todos",
    ("QUERY", "next_todo_query"): "What's my next todo?",
    ("QUERY", "get_feature_info"): "Tell me more about the GitHub integration",
    ("EXECUTION", "complete_todo"): "Mark my first todo as done",
    ("ANALYSIS", "analyze_blockers"): "What's blocking the milestone?",
}


def get_disposition(category: str, action: str) -> ActionDisposition:
    """
    Look up the disposition for a (category, action) pair.

    Returns FLOOR as the safe default for unknown pairs — the floor
    can engage conversationally with anything. But unknown pairs
    are logged as warnings by the caller.
    """
    return ACTION_REGISTRY.get(
        (category.upper(), action),
        ActionDisposition.FLOOR,  # Safe default: floor handles the unknown
    )


def validate_registry_coverage() -> list[str]:
    """
    Validate that every pre-classifier action has a registry entry.

    Returns a list of missing (category, action) pairs. Empty list = all good.
    Called at startup and in tests.
    """
    from services.intent_service.pre_classifier import PreClassifier

    missing = []

    # Test each pattern group by running representative messages through pre_classify
    # This is more robust than inspecting pattern data structures directly
    test_messages = list(ACTION_EXAMPLES.values())

    for msg in test_messages:
        result = PreClassifier.pre_classify(msg)
        if result:
            key = (result.category.value.upper(), result.action)
            if key not in ACTION_REGISTRY:
                missing.append(f"{key[0]}/{key[1]}")

    return missing


# ============================================================================
# #1124 Phase 2 — Verb canonicalization (ADR-060 amendment; layer-then-migrate)
# ============================================================================
# Per the Architect ruling (2026-06-06, "layer-then-migrate"): the canonical
# action vocabulary is a small typed VERB enum (the *verb* dimension), kept
# separate from the `source_type` slot (the *source* dimension, in
# `intent.slots`). This block is strictly ADDITIVE — the (category, action)
# ACTION_REGISTRY keys above are UNCHANGED and still drive dispatch. The Verb
# enum + ACTION_TO_VERB bridge let the action-dispatch rail (#1124) and the
# Phase-3 boundary validator reason about verbs without remapping the registry.
# Legacy `_query`-suffixed actions are retired progressively post-#1124.
#
# Pattern-072 (6th application): typed enum + documented consumers (the rail +
# ACTION_TO_VERB) + register-time validation (validate_verb_coverage) + explicit
# default policy (unknown verb -> None -> caller floors, per ADR-060).


class Verb(Enum):
    """Canonical, closed verb vocabulary the classifier emits (verb dimension).

    Source of truth for the verb dimension. The classifier emits a Verb +
    populates `source_type`; handlers read source from `intent.slots`, never
    from the verb. Unknown verb -> floor (ADR-060 floor-default).
    """

    # ---- Conversation ----
    GREET = "greet"
    FAREWELL = "farewell"
    THANK = "thank"
    # ---- Retrieval / informational read ----
    GET = "get"  # retrieve a specific fact/value (identity, time, status, …)
    LIST = "list"  # enumerate a collection (issues, prs, todos, labels, …)
    EXPLAIN = "explain"  # explain reasoning/policy (trust, a suggestion)
    ANALYZE = "analyze"  # analytical synthesis (blockers)
    # ---- Management ----
    MANAGE = "manage"  # portfolio / repo management
    # ---- Object mutations ----
    CLOSE = "close"
    REOPEN = "reopen"
    COMMENT = "comment"
    UPDATE = "update"
    COMPLETE = "complete"
    # ---- Cohort verbs awaiting Phase-5 migration ----
    # No legacy action maps to these yet; the #1124 cohort registers handlers
    # against these typed verbs instead of improvising collapsed names like
    # `summarize_github_issue`. SUMMARIZE is the subject of SUMMARIZE-TAXONOMY.
    SUMMARIZE = "summarize"
    PRIORITIZE = "prioritize"


# Bridge: every existing ACTION_REGISTRY action -> its canonical Verb.
# Phase-2 baseline; per-action verb assignment is refined in Phase 4
# (classifier-prompt canonicalization) + SUMMARIZE-TAXONOMY. Because nothing
# dispatches on Verb yet (the registry keys still drive dispatch), refining a
# mapping here carries zero runtime risk. Keyed by action string (globally
# unique across the registry).
ACTION_TO_VERB: dict[str, Verb] = {
    "greeting": Verb.GREET,
    "farewell": Verb.FAREWELL,
    "thanks": Verb.THANK,
    "get_identity": Verb.GET,
    "get_capabilities": Verb.GET,
    "explain_trust": Verb.EXPLAIN,
    "get_memory": Verb.GET,
    "pull_insights": Verb.GET,
    "get_current_time": Verb.GET,
    "get_project_status": Verb.GET,
    "get_top_priority": Verb.GET,
    "get_contextual_guidance": Verb.GET,
    "manage_portfolio": Verb.MANAGE,
    "manage_repos": Verb.MANAGE,
    "explain_suggestion": Verb.EXPLAIN,
    "meeting_time": Verb.GET,
    "recurring_meetings": Verb.GET,
    "week_calendar": Verb.GET,
    "shipped_query": Verb.GET,
    "stale_prs_query": Verb.GET,
    "close_issue_query": Verb.CLOSE,
    "reopen_issue_query": Verb.REOPEN,
    "comment_issue_query": Verb.COMMENT,
    "list_issues_query": Verb.LIST,
    "list_prs_query": Verb.LIST,
    "review_issue_query": Verb.GET,
    "list_milestones_query": Verb.LIST,
    "list_releases_query": Verb.LIST,
    "list_labels_query": Verb.LIST,
    "list_branches_query": Verb.LIST,
    "update_document_query": Verb.UPDATE,
    "changes_query": Verb.GET,
    "attention_query": Verb.GET,
    "productivity_query": Verb.GET,
    "list_todos_query": Verb.LIST,
    "list_completed_todos": Verb.LIST,
    "next_todo_query": Verb.GET,
    "get_feature_info": Verb.GET,
    "complete_todo": Verb.COMPLETE,
    "analyze_blockers": Verb.ANALYZE,
}


def get_verb(action: str) -> Optional[Verb]:
    """Return the canonical Verb for a pre-classifier action, or None.

    None means "no registered verb" -> the caller floors (ADR-060 floor-default),
    exactly as get_disposition() defaults an unknown (category, action) to FLOOR.
    """
    return ACTION_TO_VERB.get(action)


def validate_verb_coverage() -> list[str]:
    """Every (category, action) in ACTION_REGISTRY must map to a canonical Verb.

    Returns a list of "category/action" strings with no Verb mapping. Empty list
    = full coverage. Parallel to validate_registry_coverage(); enforced via the
    test suite (and available as a startup gate) so a new registry action without
    a verb fails loudly rather than silently improvising (methodology-30
    consumer-trace; #1124 Phase 2).
    """
    missing = []
    for category, action in ACTION_REGISTRY:
        if action not in ACTION_TO_VERB:
            missing.append(f"{category}/{action}")
    return missing
