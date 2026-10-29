"""#2194 — the issue-list header names the scope the read used (CXO 2026-10-29 08:51).

Before this, #2185's scope words were a fixed suffix on every connector read,
so a milestone read said "assigned to you across all your repositories in
milestone "MVP"" although the milestone lives in one repo. ONE composer now
builds the scope from the qualifiers the read actually applied, in this order:

- no qualifiers (the connector's ``assignee:@me`` read):
  ``assigned to you across all your repositories``
- a named or bound repo (a repo-wide read with no assignee term): ``in <repo>``
- a milestone on the assignee read (``_qualified_search_query`` keeps
  ``assignee:@me`` and appends ``milestone:"X"``): ``assigned to you in <repo>
  in milestone "X"``, where ``<repo>`` is the one repository the returned items
  share; the resolved default repo only when no item came back; left out rather
  than guessed when items carry no repository field or span several
- a label: `` labelled "<label>"`` after the scope (CXO's spelling)
- singular ``issue`` for 1; a closed read says ``closed``.

"across all your repositories" appears ONLY when no repo and no milestone was
applied. The empty-result lines follow the same scope rule. Pure functions; the
handler (``IntentService._handle_list_issues_query``) supplies the facts.
"""

from __future__ import annotations

from typing import Any, Iterable, Optional
from urllib.parse import urlsplit

ACROSS_ALL_REPOS = " across all your repositories"


def _repo_from_url(url: Any, *, api: bool) -> Optional[str]:
    """``owner/repo`` from an issue's ``repository_url``
    (``https://api.github.com/repos/o/r``) or ``html_url``
    (``https://github.com/o/r/issues/N``). No regex: path split."""
    if not isinstance(url, str) or not url:
        return None
    parts = [p for p in urlsplit(url).path.split("/") if p]
    if api:
        if len(parts) >= 3 and parts[0] == "repos":
            return f"{parts[1]}/{parts[2]}"
        return None
    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}"
    return None


def repo_of_item(item: Any) -> Optional[str]:
    """The repository one search item belongs to, from the fields github-mcp-server's
    ``search_issues`` passes through (go-github ``IssuesSearchResult``:
    ``repository_url`` and ``html_url``; a ``repository.full_name`` if present)."""
    if not isinstance(item, dict):
        return None
    repo = item.get("repository")
    if isinstance(repo, dict) and isinstance(repo.get("full_name"), str) and repo["full_name"]:
        return str(repo["full_name"])
    return _repo_from_url(item.get("repository_url"), api=True) or _repo_from_url(
        item.get("html_url"), api=False
    )


def shared_repo(items: Iterable[Any]) -> Optional[str]:
    """The one repository every item carries, else None (no items, an item with
    no repository field, or more than one repository)."""
    found: set[str] = set()
    any_item = False
    for item in items:
        any_item = True
        repo = repo_of_item(item)
        if repo is None:
            return None
        found.add(repo)
    if not any_item or len(found) != 1:
        return None
    return next(iter(found))


def compose_scope(
    *,
    named_repo: Optional[str],
    assignee_scoped: bool,
    milestone: Optional[str] = None,
    label: Optional[str] = None,
    milestone_repo: Optional[str] = None,
) -> str:
    """The scope words after the count, e.g. `` assigned to you in o/r in milestone "MVP"``."""
    if named_repo:
        scope = f" in {named_repo}"
    elif assignee_scoped:
        if milestone:
            scope = " assigned to you" + (f" in {milestone_repo}" if milestone_repo else "")
        else:
            scope = " assigned to you" + ACROSS_ALL_REPOS
    else:
        scope = ""
    if milestone:
        scope += f' in milestone "{milestone}"'
    if label:
        scope += f' labelled "{label}"'
    return scope


def compose_count_header(*, total: int, state_word: str, scope: str) -> str:
    """``You have **N open issues**<scope>.`` (singular for 1)."""
    return f"You have **{total} {state_word} issue{'s' if total != 1 else ''}**{scope}."


def compose_empty_line(
    *,
    state_word: str,
    named_repo: Optional[str],
    assignee_scoped: bool,
    milestone: Optional[str] = None,
    label: Optional[str] = None,
    milestone_repo: Optional[str] = None,
) -> str:
    """The no-results line under the same scope rule."""
    filters = (f' in milestone "{milestone}"' if milestone else "") + (
        f' labelled "{label}"' if label else ""
    )
    if named_repo:
        return f"No {state_word} issues in {named_repo}{filters} right now."
    if assignee_scoped:
        where = f" in {milestone_repo}" if (milestone and milestone_repo) else ""
        return f"You have no {state_word} issues assigned to you{where}{filters}."
    if filters:
        return f"You have no {state_word} issues{filters}."
    return f"You don't have any {state_word} issues right now."


__all__ = (
    "ACROSS_ALL_REPOS",
    "repo_of_item",
    "shared_repo",
    "compose_scope",
    "compose_count_header",
    "compose_empty_line",
)
