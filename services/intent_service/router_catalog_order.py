"""The router catalog's render order: an append-only ledger (#2195).

Arch's ruling, decisions.log 2026-10-29 19:39: ``derive_routing_grammar``
still derives WHICH operations exist from the live registries; their ORDER in
the rendered router prompt comes from this ledger of canonical names. Measured
that day, a line's position in the catalog is a routing variable on the served
router model (a pure reorder flipped the link_repo sentinel x6; a sort by name
lost 18 rows of the full run), so registration must never move a line.

Rules for ``CATALOG_ORDER_LEDGER``:

- **Append-only.** Generated once from main's render on 2026-10-29 (the 72
  canonical names, in the order main rendered them: rail ops in registration
  order, then registry-only ops).
- **A new op is appended at the end.** Until it is, it renders after every
  ledger op in derivation order, and the completeness test fails.
- **A name is never moved or removed** without a rule-7 full run; a reorder is
  a deliberate rule-7 unit, never a side effect of registration.
- A ledger op renders at its ledger slot whichever pass produced it (rail or
  ``ACTION_REGISTRY``), so an op that gains a rail entry keeps its slot.
- A stale name (no op) is skipped here and flagged by the completeness test.
"""

from __future__ import annotations

from typing import Iterable, Protocol, Sequence, TypeVar

CATALOG_ORDER_LEDGER: tuple[str, ...] = (
    "update_document",
    "changes_query",
    "get_current_time",
    "get_capabilities",
    "explain_trust",
    "get_memory",
    "pull_insights",
    "analyze_blockers",
    "get_feature_info",
    "check_completion_status",
    "write_stakeholder_update",
    "get_identity",
    "explain_suggestion",
    "get_contextual_guidance",
    "list_repos",
    "search_projects",
    "archive_project",
    "restore_project",
    "add_project",
    "link_repo",
    "unlink_repo",
    "close_issue",
    "reopen_issue",
    "comment_issue",
    "update_issue",
    "create_issue",
    "prioritize",
    "generate_content",
    "create_reminder",
    "create_todo",
    "delete_todo",
    "complete_todo",
    "clear_todos",
    "set_default_repo",
    "get_default_repo",
    "set_timezone",
    "list_archived_projects",
    "summarize_document",
    "shipped_this_week",
    "stale_prs",
    "review_issue",
    "list_issues",
    "list_prs",
    "list_milestones",
    "list_releases",
    "list_labels",
    "list_branches",
    "meeting_time",
    "recurring_meetings",
    "week_calendar",
    "analyze_commits",
    "generate_report",
    "analyze_data",
    "local_git_status_query",
    "search_documents",
    "productivity",
    "session_activity_query",
    "show_standup",
    "list_projects",
    "attention_query",
    "list_todos_query",
    "list_reminders_query",
    "analyze_document",
    "strategic_planning",
    "learn_pattern",
    "greeting",
    "farewell",
    "thanks",
    "get_project_status",
    "get_top_priority",
    "manage_portfolio",
    "manage_repos",
)


class _Named(Protocol):
    @property
    def name(self) -> str: ...


_Op = TypeVar("_Op", bound=_Named)


def order_operations(ops: Iterable[_Op], ledger: Sequence[str] = CATALOG_ORDER_LEDGER) -> list[_Op]:
    """Ledger ops in ledger order, then non-ledger ops in their derivation order.

    Pure: ``ops`` is not mutated, and no op is dropped (should two ops ever
    share a name, both render, at that name's slot, in derivation order). A
    ledger name with no op is skipped.
    """
    derived = list(ops)
    by_name: dict[str, list[_Op]] = {}
    for op in derived:
        by_name.setdefault(op.name, []).append(op)
    in_ledger = set(ledger)
    ordered = [op for name in ledger for op in by_name.get(name, ())]
    ordered.extend(op for op in derived if op.name not in in_ledger)
    return ordered


def ledger_drift(
    names: Iterable[str], ledger: Sequence[str] = CATALOG_ORDER_LEDGER
) -> tuple[list[str], list[str]]:
    """``(missing, stale)``: derived op names absent from the ledger (append
    them at the end), and ledger names with no derived op (remove them, a
    rule-7 decision)."""
    derived = list(names)
    in_ledger = set(ledger)
    present = set(derived)
    missing = [n for n in derived if n not in in_ledger]
    stale = [n for n in ledger if n not in present]
    return missing, stale
