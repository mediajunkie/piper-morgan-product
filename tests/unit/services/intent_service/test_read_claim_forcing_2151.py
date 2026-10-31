"""#2151 step 2: the forcing test. A rail read that FAILS must never be said as verified.

Arch's ruling (2026-10-23, issue comment 6377720778) made this file the code form of the
read-claim inventory's rail rows (docs/internal/architecture/current/read-claim-inventory.yaml).

THE DENOMINATOR is derived: every canonical action-triggered ``WorkflowEntry`` in
``WORKFLOW_REGISTRY`` (one name per unique entry: the ``wired_chat_actions`` part-1 walk, the
same walk ``scripts/read_claim_inventory.py`` uses). A new entry is tested by default. Every
canonical entry is in exactly one of:

- ``FORCE``   its read seams are mapped and the forcing check runs on it;
- ``EXEMPT``  by design it claims nothing about the user's data (a reason is required;
              additions are reviewed by Arch);
- neither     the test FAILS: "map its read seam, or list it with a reason".

``KNOWN_RED`` is a subset of ``FORCE``: rows whose forcing check fails TODAY, each tagged with
its cause (the inventory header's shared causes, plus the row-level tags in ``CAUSE_TAGS``).
A listed row must STILL fail; a listed row that now passes fails with "fixed: remove <id>
from KNOWN_RED". ``len(KNOWN_RED)`` may only fall (``KNOWN_RED_CEILING``).

THE FORCING CHECK (one entry = one or more runs; the entry passes only if every run passes)
-----------------------------------------------------------------------------------------
1. Intent: action = the canonical key; category = the entry's ``ACTION_REGISTRY`` category
   (QUERY when it has none, the rail's own default); context = a user id, a plausible
   ``original_message``, and any slots the handler takes from context (``Force.context``).
2. Dispatch through ``workflow_dispatcher.dispatch_workflow`` with the context shape
   ``IntentService._dispatch_action_rail`` passes (``intent``, ``workflow_id``,
   ``intent_service``) on a real ``IntentService``, and handle a raise the way the rail's
   dispatch block does (``raise_errors=True``; a raise becomes
   ``IntentService._rail_read_failed_result``, which is None, a fall-through, for a WRITE
   entry or one with no failed-read text). The consent/confirm gates in front of that block
   are not run: the "yes" turn re-dispatches the same intent, and the read under test lives
   in the handler.
3. Base for every run: unforced database reads succeed EMPTY (``AsyncSession`` reads return
   an empty result), so the one read a run forces is the only failure in it; the floor's
   ride-along gathers (due reminders, the first-contact demo) are off, since they are their own
   surfaces (``floor:source_failed`` rows) and would otherwise arm the floor's failed-check
   directive for every floor turn. Preconditions (``PRECONDITIONS``) make the read reachable:
   a credential exists, a repo resolves, the calendar authenticates, Notion is configured.
   LLM slot extraction is replaced by the slots the message carries (``Force.slots``).
4. The read is forced to fail at the lowest seam we can name (``SEAMS``), so every swallow
   between the seam and the reply is in the path:

   - ``db``        ``AsyncSession.execute/scalar/scalars/get`` raise ``OperationalError``;
   - ``gh_rest``   ``aiohttp.ClientSession._request`` raises ``ClientConnectionError``;
   - ``gh_mcp``    ``MCPClient.connect_http`` raises ``ConnectionError``;
   - ``calendar``  the Google API request's ``execute()`` raises ``ConnectionError``;
   - ``notion``    every ``notion_client`` endpoint call raises ``ConnectionError``;
   - ``iss``       ``IntegrationStatusService.get_status/get_all`` raise;
   - ``local_git`` GitPython's ``Repo`` raises ``OSError`` when opened.

   A GitHub entry runs twice: ``connector`` (the user's credential resolves, so the MCP / grant
   leg is taken) and ``native`` (no binding: CONNECT_REQUIRED, so the native-PAT REST fallback
   is taken). Handlers with no native leg take the connector run only.
5. A run PASSES when all of these hold:
   - at least one of the run's forced seams was called (else the harness, not the product, is
     wrong, and the test fails with "seam not reached");
   - ``dispatch_workflow`` returned a result (``None`` is RAIL-FALLTHROUGH: the turn falls to
     category routing and the floor, which never saw the read);
   - the reply contains none of ``GLOBAL_ABSENCE_MARKERS`` or the entry's ``absence`` markers
     (its verified-empty / not-connected / positive wording, from the YAML ``texts.verified``
     and the handler source);
   - the reply carries a couldn't-check signal (one of ``FAILED_SIGNALS``).
   A floor-riding entry's reply is composed by the LLM (stubbed here), so the evidence is the
   composed floor PROMPT instead: the run passes when the floor's aggregate directive
   ("DATA CHECKS FAILED this turn — could not check: ...") names every check in
   ``floor_checks``, or the prompt carries one of the gather's in-band failure lines
   (``floor_inband``). A failed read the prompt says nothing about is FLOOR-ABSENT.

OFFLINE: every socket connect and name lookup raises, ``LLMClient.complete`` is a stub that
records the prompt, and the classifier's LLM is explosive. No key, no network.

LAYER: unit, real handlers with the read seams patched. It measures the reply (or the floor
prompt) under a forced failure, not served LLM prose. DENOMINATOR: every canonical
action-triggered rail entry, asserted equal to the registry walk and > 0.
"""

from __future__ import annotations

import asyncio
import contextlib
import re
import socket
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
from unittest.mock import patch

import pytest

REPO_OWNER, REPO_NAME = "forced-owner", "forced-repo"
REPO = f"{REPO_OWNER}/{REPO_NAME}"

# A couldn't-check signal, as the handlers' honest failed-read copy already words it.
FAILED_SIGNALS = (
    "couldn't",
    "could not",
    "can't check",
    "unable to",
    "wasn't able",
    "had trouble",
    "ran into something",
    "unreachable",
    "didn't confirm",  # a fired-but-unverified write (#1322 read-back guard)
)

# Wording that, over a forced failure, is a claim about the user's data or connection.
GLOBAL_ABSENCE_MARKERS = (
    "don't have any",
    "isn't connected yet",
    "isn't configured yet",
    "No commits found",
)

_AGGREGATE_RE = re.compile(r"DATA CHECKS FAILED this turn — could not check: ([^.]*)\.")


# ─── Seams ──────────────────────────────────────────────────────────────────


class _Hits:
    def __init__(self) -> None:
        self.counts: Dict[str, int] = {}

    def hit(self, name: str) -> None:
        self.counts[name] = self.counts.get(name, 0) + 1


def _forced(name: str, hits: _Hits, exc_factory: Callable[[], BaseException]):
    async def _raise(*_a, **_k):
        hits.hit(name)
        raise exc_factory()

    return _raise


def _db_error() -> BaseException:
    from sqlalchemy.exc import OperationalError

    return OperationalError("forced: the database read failed (#2151)", None, Exception("forced"))


def _seam_db(hits: _Hits) -> List[Any]:
    from sqlalchemy.ext.asyncio import AsyncSession

    return [
        patch.object(AsyncSession, name, _forced("db", hits, _db_error))
        for name in ("execute", "scalar", "scalars", "get")
    ]


def _seam_gh_rest(hits: _Hits) -> List[Any]:
    import aiohttp

    def _err():
        return aiohttp.ClientConnectionError("forced: GitHub REST unreachable")

    return [patch.object(aiohttp.ClientSession, "_request", _forced("gh_rest", hits, _err))]


def _seam_gh_mcp(hits: _Hits) -> List[Any]:
    from services.mcp.consumer.mcp_client import MCPClient

    @contextlib.asynccontextmanager
    async def _raise(*_a, **_k):
        hits.hit("gh_mcp")
        raise ConnectionError("forced: the GitHub MCP server is unreachable")
        yield  # pragma: no cover

    return [patch.object(MCPClient, "connect_http", _raise)]


class _RaisingGoogleService:
    """The googleapiclient service: building a request works, ``execute()`` (the HTTP call)
    raises."""

    def __init__(self, hits: _Hits) -> None:
        self._hits = hits

    def __getattr__(self, _name):
        return self

    def __call__(self, *_a, **_k):
        return self

    def execute(self, *_a, **_k):
        self._hits.hit("calendar")
        raise ConnectionError("forced: the Google Calendar read failed")


def _seam_calendar(hits: _Hits) -> List[Any]:
    """Authentication succeeds (the precondition) and installs a service whose request
    ``execute()`` raises (the seam)."""
    from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

    async def _auth(self, *_a, **_k):
        self._service = _RaisingGoogleService(hits)
        self._circuit_open = False
        return True

    return [patch.object(GoogleCalendarMCPAdapter, "authenticate", _auth)]


class _RaisingNotionClient:
    def __init__(self, hits: _Hits) -> None:
        self._hits = hits

    def __getattr__(self, _name):
        return self

    def __call__(self, *_a, **_k):
        self._hits.hit("notion")
        raise ConnectionError("forced: the Notion API call failed")


def _seam_notion(hits: _Hits) -> List[Any]:
    """Notion is configured for the user and connects (the precondition); every endpoint call
    on the client raises (the seam)."""
    from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
    from services.mcp.consumer.notion_adapter import NotionMCPAdapter

    async def _connect(self, *_a, **_k):
        self._notion_client = _RaisingNotionClient(hits)
        return True

    return [
        patch.object(NotionIntegrationRouter, "is_available", lambda self, *a, **k: True),
        patch.object(NotionMCPAdapter, "connect_with_token", _connect),
    ]


def _seam_iss(hits: _Hits) -> List[Any]:
    from services.integrations.integration_status_service import IntegrationStatusService

    def _err():
        return RuntimeError("forced: the integration status lookup failed")

    return [
        patch.object(IntegrationStatusService, "get_status", _forced("iss", hits, _err)),
        patch.object(IntegrationStatusService, "get_all", _forced("iss", hits, _err)),
    ]


def _seam_local_git(hits: _Hits) -> List[Any]:
    """GitPython's ``Repo`` raises when opened; the inspector's own catch is in the path."""

    def _raise(*_a, **_k):
        hits.hit("local_git")
        raise OSError("forced: the working tree could not be read")

    return [patch("git.Repo", _raise)]


SEAMS: Dict[str, Callable[[_Hits], List[Any]]] = {
    "db": _seam_db,
    "gh_rest": _seam_gh_rest,
    "gh_mcp": _seam_gh_mcp,
    "calendar": _seam_calendar,
    "notion": _seam_notion,
    "iss": _seam_iss,
    "local_git": _seam_local_git,
}
GH_SEAMS: Tuple[str, ...] = ("gh_rest", "gh_mcp")


# ─── Base and preconditions ─────────────────────────────────────────────────


class _EmptyResult:
    """A database result with no rows, for every unforced read."""

    rowcount = 0

    def __getattr__(self, name):
        if name in ("all", "fetchall"):
            return lambda *a, **k: []
        if name in ("scalars", "mappings", "unique", "tuples"):
            return lambda *a, **k: self
        return lambda *a, **k: None

    def __iter__(self):
        return iter(())


def _base_db_empty() -> List[Any]:
    from sqlalchemy.ext.asyncio import AsyncSession

    async def _empty(*_a, **_k):
        return _EmptyResult()

    async def _none(*_a, **_k):
        return None

    return [
        patch.object(AsyncSession, "execute", _empty),
        patch.object(AsyncSession, "scalars", _empty),
        patch.object(AsyncSession, "scalar", _none),
        patch.object(AsyncSession, "get", _none),
    ]


def _base_floor_ride_alongs_off() -> List[Any]:
    from services.intent_service.context_assembler import ContextAssembler

    async def _no_reminders(self, *_a, **_k):
        return {}

    return [
        patch.object(ContextAssembler, "_gather_reminder_context", _no_reminders),
        patch("services.intent_service.first_contact.is_first_exchange", lambda *a, **k: False),
    ]


def _pre_repo() -> List[Any]:
    from services.integrations.github.repo_resolver import ResolvedRepo

    async def _user_default(*_a, **_k):
        return ResolvedRepo(owner=REPO_OWNER, name=REPO_NAME, source="user_default")

    async def _default_name(*_a, **_k):
        return REPO

    return [
        patch(
            "services.integrations.github.repo_resolver._resolve_from_user_default",
            _user_default,
        ),
        patch("services.integrations.github.repo_resolver.get_user_default_repo", _default_name),
    ]


def _pre_gh_common() -> List[Any]:
    from services.integrations.github.config_service import GitHubConfigService
    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

    async def _token(self, *_a, **_k):
        return "fake-token-forced-2151"

    async def _account_pat(*_a, **_k):
        return "fake-token-forced-2151"

    return [
        patch.object(GitHubConfigService, "aget_authentication_token", _token),
        # #1966: a user's native REST token is their own PAT, read through account_pat.
        patch.object(GitHubMCPSpatialAdapter, "account_pat", staticmethod(_account_pat)),
        patch.object(
            GitHubConfigService, "get_authentication_token", lambda s, *a, **k: "fake-token-2151"
        ),
        patch.object(GitHubConfigService, "is_configured", lambda s, *a, **k: True),
        *_pre_repo(),
    ]


def _pre_gh_connector(_hits: _Hits) -> List[Any]:
    """The user's credential resolves (the PAT leg, so no grant-store read): the connector /
    grant leg is taken."""
    from services.mcp.consumer.github_adapter import GitHubCredential, GitHubMCPSpatialAdapter

    async def _cred(self, user_id, *_a, **_k):
        return GitHubCredential(
            owner_id=user_id,
            mcp_server_ref="http://forced-mcp.invalid/github",
            token="fake-token-forced-2151",
            leg="pat",
        )

    return [*_pre_gh_common(), patch.object(GitHubMCPSpatialAdapter, "resolve_credential", _cred)]


def _pre_gh_native(_hits: _Hits) -> List[Any]:
    """No connector binding (CONNECT_REQUIRED): the native-PAT REST fallback is taken.

    Since #2151 (Arch 10-24 16:49) ``is_available()`` derives from ``resolve_credential``,
    so for a principal a CONNECT_REQUIRED resolver closes the gate before the native leg.
    The leg is still reached through the legacy gate (no principal, ``is_configured``), so
    the gate is held open here to keep measuring the leg's failure line."""
    from services.integrations.github.github_integration_router import GitHubIntegrationRouter
    from services.mcp.consumer.connector import DegradationReason
    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

    async def _no_binding(self, *_a, **_k):
        return await self.degrade(DegradationReason.CONNECT_REQUIRED)

    async def _gate_open(self, *_a, **_k):
        return True

    return [
        *_pre_gh_common(),
        patch.object(GitHubMCPSpatialAdapter, "resolve_credential", _no_binding),
        patch.object(GitHubIntegrationRouter, "is_available", _gate_open),
    ]


def _pre_env_repo(_hits: _Hits) -> List[Any]:
    """The host sets PIPER_DEFAULT_REPO (ENV-REPO): the only way a principal-less GitHub read
    (learn_pattern's never-initialized router) resolves a repo at all."""
    import os

    return [patch.dict(os.environ, {"PIPER_DEFAULT_REPO": REPO})]


PRECONDITIONS: Dict[str, Callable[[_Hits], List[Any]]] = {
    "gh_connector": _pre_gh_connector,
    "gh_native": _pre_gh_native,
    "env_repo": _pre_env_repo,
}


# ─── The per-entry map ──────────────────────────────────────────────────────


@dataclass(frozen=True)
class Run:
    seams: Tuple[str, ...]
    pre: Tuple[str, ...] = ()
    checks: Tuple[str, ...] = ()  # a floor run: the check names this run's failure must arm

    @property
    def label(self) -> str:
        return "+".join(self.pre + self.seams)


@dataclass
class Force:
    runs: Tuple[Run, ...]
    message: str
    absence: Tuple[str, ...] = ()
    context: Dict[str, Any] = field(default_factory=dict)
    slots: Optional[Dict[str, Any]] = None
    floor_checks: Tuple[str, ...] = ()
    floor_inband: Tuple[str, ...] = ()
    reply_is_evidence: bool = False  # #2236: the served reply, not the prompt, is the evidence

    @property
    def floor(self) -> bool:
        return bool(self.floor_checks or self.floor_inband)


def one(*seams: str, pre: Tuple[str, ...] = (), checks: Tuple[str, ...] = ()) -> Tuple[Run, ...]:
    return (Run(seams=seams, pre=pre, checks=checks),)


def gh(
    *extra: str,
    native: bool = True,
    checks: Tuple[str, ...] = (),
    pre: Tuple[str, ...] = (),
) -> Tuple[Run, ...]:
    runs = [Run(seams=GH_SEAMS + extra, pre=("gh_connector",) + pre, checks=checks)]
    if native:
        runs.append(Run(seams=GH_SEAMS + extra, pre=("gh_native",) + pre, checks=checks))
    return tuple(runs)


# The status/priority baseline gather: its GitHub reads (blocked items, milestones, recent
# activity, high-priority issues), the GitHub connection status, and the pending todos.
# #2151 FLOOR-ABSENT (2026-10-29): each run names the checks its failure must arm, by the
# registered labels of the reads it fails (``SOURCE_FAILED_FLAGS``). Step 2 wrote "GitHub"
# here before the per-read flags existed; no STATUS read is registered as "GitHub", so the
# row could not pass however the gather stated the failure. A failed GitHub read must name
# all four GitHub reads; a failed status check is "integrations" (ISS-STATUS); a failed
# database must name the todos, the user's projects and priorities (user context), and
# the open issues (the default-repo read under them, never "no repo configured").
_GH_STATUS_CHECKS = ("open issues", "blocked items", "milestones", "recent repository activity")
_GH_STATUS_FLOOR = (
    gh(native=False, checks=_GH_STATUS_CHECKS)
    + one("iss", checks=("integrations",))
    + one("db", checks=("pending todos", "projects", "priorities", "open issues"))
)

FORCE: Dict[str, Force] = {
    # ── floor-riding adapters: the floor prompt is the evidence ──
    # identity / capabilities: the per-user integration status (ISS) and the user context.
    "get_capabilities": Force(
        one("iss"), "what can you do?", floor_checks=("integrations",), reply_is_evidence=True
    ),
    "get_identity": Force(one("iss"), "who are you?", floor_checks=("integrations",)),
    "explain_trust": Force(
        one("db"), "how much do you trust me?", floor_inband=("Trust relationship stage: unknown",)
    ),
    "get_memory": Force(
        one("db"), "do you remember what we discussed?", floor_checks=("past conversations",)
    ),
    "pull_insights": Force(
        one("db"), "what have you learned about me?", floor_checks=("insights",)
    ),
    # the status/priority baseline: GitHub reads, the GitHub status, the todos.
    "analyze_blockers": Force(
        _GH_STATUS_FLOOR, "what's blocking the launch?", floor_checks=_GH_STATUS_CHECKS
    ),
    "get_feature_info": Force(
        _GH_STATUS_FLOOR, "what does the standup feature do?", floor_checks=_GH_STATUS_CHECKS
    ),
    # #2195: get_project_status rides the same STATUS floor branch
    # (context_assembler.gather_context -> _gather_status_priority_context).
    "get_project_status": Force(
        _GH_STATUS_FLOOR, "give me a project overview", floor_checks=_GH_STATUS_CHECKS
    ),
    "check_completion_status": Force(
        one("db"), "when did I finish the onboarding work?", floor_checks=("completed todos",)
    ),
    "write_stakeholder_update": Force(
        _GH_STATUS_FLOOR,
        "write a stakeholder update for this week",
        floor_checks=_GH_STATUS_CHECKS,
    ),
    # ── Piper's own store (the database) ──
    "changes_query": Force(one("db"), "what changed since yesterday?"),
    "list_repos": Force(one("db"), "list my repos", absence=("registered repositories yet",)),
    "search_projects": Force(
        one("db"), "search my projects for Alpha", absence=("couldn't find any projects",)
    ),
    "archive_project": Force(one("db"), "archive project Alpha"),
    "restore_project": Force(one("db"), "restore project Alpha"),
    "add_project": Force(one("db"), "add project Alpha"),
    "link_repo": Force(one("db"), f"link repo {REPO} to project Alpha"),
    "unlink_repo": Force(one("db"), f"unlink {REPO} from Alpha"),
    "delete_todo": Force(one("db"), "delete todo 1"),
    "complete_todo": Force(one("db"), "complete todo 1"),
    "clear_todos": Force(one("db"), "clear my todos"),
    "get_default_repo": Force(
        one("db"), "what's my default repo?", absence=("haven't set a default repo",)
    ),
    "set_default_repo": Force(
        one("db") + gh(native=False), "set my default repo to piper", absence=("look like",)
    ),
    "list_archived_projects": Force(
        one("db"), "show archived projects", absence=("don't have any archived",)
    ),
    "list_projects": Force(one("db"), "list my projects"),
    "list_todos_query": Force(one("db"), "show my todos"),
    "list_reminders_query": Force(
        one("db"), "what reminders do I have?", absence=("there are none",)
    ),
    "session_activity_query": Force(
        one("db"), "what did we create this session?", absence=("haven't created anything",)
    ),
    "attention_query": Force(
        one("db") + one("calendar"),
        "what needs my attention?",
        absence=("Nothing due today", "Nothing from your flagged"),
    ),
    "explain_suggestion": Force(
        one("db"), "why did you suggest that?", absence=("don't have a clear record",)
    ),
    # ── the user's files (FileResolver over the database) ──
    "summarize_document": Force(
        one("db"), "summarize roadmap.pdf", absence=("don't see any uploaded",)
    ),
    "compare_documents": Force(one("db"), "compare roadmap.pdf and plan.pdf"),
    # ── Notion ──
    "update_document": Force(
        one("notion"),
        "update the Roadmap document: add a launch line",
        absence=("No document found",),
        slots={"doc_name": "Roadmap", "content": "add a launch line"},
    ),
    "search_documents": Force(
        one("notion"), "search documents for roadmap", absence=("didn't find any documents",)
    ),
    "analyze_document": Force(
        one("db") + one("notion"),
        "analyze the Roadmap document",
        absence=("couldn't find a specific document", "don't see that document"),
        context={"document_title": "Roadmap"},
    ),
    # ── Google Calendar ──
    "get_current_time": Force(one("calendar"), "what time is it?", absence=("No meetings",)),
    "meeting_time": Force(
        one("calendar"), "how much time am I in meetings today?", absence=("no meetings",)
    ),
    "recurring_meetings": Force(
        one("calendar"), "review my recurring meetings", absence=("didn't find any recurring",)
    ),
    "week_calendar": Force(one("calendar"), "what's my week like?", absence=("no meetings",)),
    # ── GitHub ──
    "close_issue": Force(gh(), "close the login bug issue"),
    "reopen_issue": Force(gh(native=False), "reopen the login bug issue"),
    "comment_issue": Force(
        gh(),
        f"comment on issue #12 in {REPO} saying looks good",
        slots={"issue_number": "12", "comment_text": "looks good"},
    ),
    "update_issue": Force(gh(), f"change the title of #12 in {REPO} to Login fix"),
    "create_issue": Force(
        gh(),
        f"create an issue in {REPO} about the login bug",
        context={"title": "Login bug", "repository": REPO},
    ),
    "shipped_this_week": Force(
        gh(native=False), "what did we ship this week?", absence=("No closures", "nothing closed")
    ),
    "stale_prs": Force(gh(native=False), "show me stale PRs", absence=("No open PRs returned",)),
    "review_issue": Force(gh(), "show me issue #12"),
    "list_issues": Force(gh(native=False), "list my issues", absence=("no open issues",)),
    "list_prs": Force(
        gh(native=False), "list my pull requests", absence=("no open pull requests",)
    ),
    "list_milestones": Force(gh(native=False), "list milestones", absence=("no open milestones",)),
    "list_releases": Force(gh(native=False), "list releases", absence=("no releases",)),
    "list_labels": Force(gh(native=False), "list labels", absence=("don't see any labels",)),
    "list_branches": Force(gh(native=False), "list branches", absence=("don't see any branches",)),
    "analyze_commits": Force(
        gh(native=False), f"analyze commits in {REPO}", context={"repository": REPO}
    ),
    "generate_report": Force(
        gh(native=False), f"generate a report for {REPO}", context={"repository": REPO}
    ),
    "analyze_data": Force(
        gh(native=False),
        f"analyze data for {REPO}",
        absence=("0 total activities",),
        context={"repository": REPO},
    ),
    "generate_content": Force(
        gh(native=False),
        f"write a status report for {REPO}",
        absence=("0 total activities", "**0**"),
        context={"content_type": "status_report", "repository": REPO},
    ),
    "learn_pattern": Force(
        gh(native=False, pre=("env_repo",)),
        "find similar issues",
        absence=("No historical data",),
        context={"pattern_type": "issue_similarity", "source": "github_issues"},
    ),
    "productivity": Force(one("db") + gh(native=False), "how productive was I this week?"),
    # #2182: the work-items read goes through the one resolver for the signed-in user, so
    # the native-leg run (resolver CONNECT_REQUIRED) is the not-connected state here, as
    # for list_issues; its honest reply is the not-connected line.
    "show_standup": Force(
        gh(native=False) + one("calendar") + one("db"),
        "show my standup",
        absence=("no observed activity",),
    ),
    # ── the server's working tree ──
}

# By design these claim nothing about the user's data. Mirrors the inventory's exempt rail
# rows. ADDITIONS ARE REVIEWED BY ARCH: an entry that reads the user's data before replying is
# never exempt, even when it also writes, and a write that returns success over a swallowed
# failure is not "write-only".
EXEMPT: Dict[str, str] = {
    "prioritize": "scores the items passed in the request; reads nothing stored",
    "strategic_planning": "builds a plan from the request; reads nothing stored",
    "create_reminder": "write-only: reads nothing before writing",
    "create_todo": "write-only: reads nothing before writing",
    "set_timezone": "write-only: reads nothing before writing",
    "get_contextual_guidance": "how-to guidance; the inventory row is exempt",
    # Lead 10-23 (#2151, CXO + Arch): declines on hosted (the server's tree is not the
    # user's) and when the local read fails; reads none of the user's data. Arch to review.
    "local_git_status_query": "declines plainly (CXO's line); never reads the user's data",
}

# Row-level causes used beside the inventory header's shared ones.
CAUSE_TAGS = {
    # the inventory header's shared causes
    "RAIL-FALLTHROUGH": "dispatch_workflow catches the raise and returns None",
    "ISS-STATUS": "a failed integration-status lookup reads as not configured",
    "GH-NONSTRICT": "a non-strict GitHub read returns [] on any error",
    "ENV-REPO": "a host-wide PIPER_DEFAULT_REPO resolves the repo",
    "TODO-CAP": "the 100-row todo window",
    "FLOOR-ABSENT": "a floor gather returns {}/None on error, the floor prompt says nothing",
    "NOT-PERFORMED": "the product never performs the read the row asks about (fourth state)",
    "NOTION-SEARCH": "NotionMCPAdapter.search_notion returns [] on any exception",
    # row-level
    "CAL-SWALLOW": (
        "GoogleCalendarMCPAdapter swallows a failed read into []/None (get_recurring_events "
        "without last_read_error; get_temporal_summary reports success=True with "
        "events_read_established=False), and the handler reads it as an empty calendar"
    ),
    "ACTIVITY-READ-FAILED": (
        "get_recent_activity marks a failed read with read_failed, and the handler does not "
        "check it, so the failure is computed as zero activity"
    ),
    "SWALLOW-EMPTY": (
        "the handler catches the failed read itself and renders its empty / no-record / "
        "ask-again wording with no couldn't-check signal"
    ),
    "WRITE-SWALLOW": (
        "a write's transport failure returns None below the handler, and the handler reports "
        "success (comment_issue's native path: 'Successfully added comment')"
    ),
    "NO-SEAM-YET": "the read could not be mapped to a seam in reasonable effort",
}

KNOWN_RED: Dict[str, str] = {
    # WRITE entries: a raise still falls through (the #2151 step-3 fix covers READ entries)
    # floor adapters: get_memory left on 2026-10-30 (#2215: its row expected a label no
    # read registers; on the registered "past conversations" the prompt names the failure).
    # check_completion_status moved to NOT_PERFORMED the same day (#2215, part 2).
    # GitHub
    "close_issue": "GH-NONSTRICT",
    "reopen_issue": "GH-NONSTRICT",
    "learn_pattern": "GH-NONSTRICT",
    "set_default_repo": "SWALLOW-EMPTY",
    # Notion
    "update_document": "NOTION-SEARCH",
    "search_documents": "NOTION-SEARCH",
    "analyze_document": "NOTION-SEARCH",
    # Google Calendar
    "attention_query": "CAL-SWALLOW",
    # Piper's own store
    "explain_suggestion": "SWALLOW-EMPTY",
}
KNOWN_RED_CEILING = 9

# #2215 part 2 (2026-10-30; Arch 10-29 21:46, the four-state rule's fourth state): rows whose
# forced read is NOT PERFORMED by the product at all, so no failure can be stated and the row
# can never pass. They stay in FORCE (every rail entry is forced: the coverage pin below) and
# stay red, but they are not silent failures (KNOWN_RED): the honest fix is a product one,
# tracked on the read-claim inventory's ``not_performed`` state, not a stated-failure seam.
# Shrink-only, like KNOWN_RED. A row leaves when the product performs the read (it then either
# passes or joins KNOWN_RED with a cause tag) or the rail entry is deleted.
NOT_PERFORMED: Dict[str, str] = {
    # STATUS gathers pending todos but no completed todos and no closed issues; a
    # completion-history ask reaches the floor without the data it asks about.
    "check_completion_status": "NOT-PERFORMED",
}
NOT_PERFORMED_CEILING = 1


# ─── Harness ────────────────────────────────────────────────────────────────


def canonical_rail_entries() -> Dict[str, Any]:
    from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    out: Dict[str, Any] = {}
    seen: set = set()
    for key, entry in WORKFLOW_REGISTRY.items():
        if not entry.action_triggered or id(entry) in seen:
            continue
        seen.add(id(entry))
        out[key] = entry
    return out


def _category_for(op: str) -> str:
    from services.intent_service.action_registry import ACTION_REGISTRY

    for category, action in ACTION_REGISTRY:
        if action == op:
            return category
    return "QUERY"


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@dataclass
class RunOutcome:
    run: Run
    result_none: bool
    message: str
    prompt: str
    hits: Dict[str, int] = field(default_factory=dict)
    verdict: str = ""  # "pass" or why the run failed

    def describe(self) -> str:
        shown = "<None: fell through>" if self.result_none else self.message
        return f"[{self.run.label}] {self.verdict}; hits={self.hits}; reply={shown[:200]!r}"


def _blocked(*_a, **_k):
    raise OSError("network blocked in the #2151 forcing test")


# Host-wide credentials and the env repo (tests/conftest.py loads some from the keychain and
# the gh CLI). A run sets what it needs through its preconditions; nothing leaks in.
_HOST_ENV = (
    "GITHUB_TOKEN",
    "GITHUB_ACCESS_TOKEN",
    "SLACK_BOT_TOKEN",
    "NOTION_API_KEY",
    "NOTION_API_TOKEN",
    "GOOGLE_CALENDAR_CREDENTIALS",
    "MCP_ENABLED",
    "PIPER_DEFAULT_REPO",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
)


@contextlib.contextmanager
def _no_host_env():
    import os

    with patch.dict(os.environ, {}):
        for name in _HOST_ENV:
            os.environ.pop(name, None)
        yield


def _offline(prompts: List[str]) -> List[Any]:
    from services.llm.clients import LLMClient

    async def _stub_complete(self, task_type, prompt, *a, **k):
        prompts.append(f"{k.get('system') or ''}\n{prompt}")
        return "(#2151 floor stub reply)"

    return [
        _no_host_env(),
        patch.object(socket, "getaddrinfo", _blocked),
        patch.object(socket.socket, "connect", _blocked),
        patch.object(socket.socket, "connect_ex", _blocked),
        patch.object(LLMClient, "complete", _stub_complete),
    ]


def _slot_patch(slots: Dict[str, Any]) -> Any:
    async def _extract(*_a, **_k):
        return dict(slots)

    return patch("services.slot_filling.slot_extractor.extract_slots", _extract)


def _judge(force: Force, out: RunOutcome) -> str:
    if not any(out.hits.get(s) for s in out.run.seams):
        return "seam not reached"
    if out.result_none:
        return "fell through (None)"
    if force.floor:
        # #2236 (Arch ruling 4): the capability answer renders the failed-read sentence in
        # code, so for get_capabilities ONLY the evidence is the served reply, strictly:
        # exactly the couldn't-check line and no connection facts. get_identity keeps the
        # prompt evidence below (identity turns still hand the model the integrations block).
        if force.reply_is_evidence:
            from services.intent_service.capability_answer import COULDNT_CHECK_LINE

            low = out.message.lower()
            if (
                COULDNT_CHECK_LINE in out.message
                and "not connected" not in low
                and "none of your tools" not in low
            ):
                return "pass"
            return "capability reply lacks the exact couldn't-check line or states connection facts"
        if any(line in out.prompt for line in force.floor_inband):
            return "pass"
        m = _AGGREGATE_RE.search(out.prompt)
        named = {n.strip() for n in m.group(1).split(",")} if m else set()
        wanted = out.run.checks or force.floor_checks
        missing = [c for c in wanted if c not in named]
        if wanted and not missing:
            return "pass"
        return f"floor prompt does not name the failed check(s) {missing or force.floor_inband}"
    low = out.message.lower()
    for marker in GLOBAL_ABSENCE_MARKERS + force.absence:
        if marker.lower() in low:
            return f"absence/verified wording {marker!r}"
    if not any(s in low for s in FAILED_SIGNALS):
        return "no couldn't-check signal"
    return "pass"


async def _run_once(entry_id: str, force: Force, run: Run) -> RunOutcome:
    from services.domain.models import Intent
    from services.intent.intent_service import IntentService
    from services.intent_service.classifier import IntentClassifier
    from services.intent_service.workflow_dispatcher import dispatch_workflow
    from services.shared_types import IntentCategory

    # A fresh principal per run, so no in-process cache carries one run's reads into another.
    user_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"piper-2151/{entry_id}/{run.label}"))
    hits = _Hits()
    prompts: List[str] = []
    with contextlib.ExitStack() as stack:
        layers: List[Any] = [*_offline(prompts), *_base_db_empty(), *_base_floor_ride_alongs_off()]
        for name in run.pre:
            layers += PRECONDITIONS[name](hits)
        if force.slots is not None:
            layers.append(_slot_patch(force.slots))
        for name in run.seams:  # last, so a forced seam overrides the empty base
            layers += SEAMS[name](hits)
        for layer in layers:
            stack.enter_context(layer)
        service = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))
        intent = Intent(
            category=IntentCategory[_category_for(entry_id)],
            action=entry_id,
            confidence=1.0,
            context={"user_id": user_id, "original_message": force.message, **force.context},
            original_message=force.message,
        )
        # The rail's own dispatch block (_dispatch_action_rail after its consent gates):
        # raise_errors=True, and a raise becomes the READ entry's failed-read reply, or None
        # (fall-through) for an entry with no such reply.
        try:
            result = await asyncio.wait_for(
                dispatch_workflow(
                    workflow_type=entry_id,
                    session_id=f"s-2151-{entry_id}-{run.label}",
                    user_id=user_id,
                    context={
                        "intent": intent,
                        "workflow_id": "wf-2151",
                        "intent_service": service,
                    },
                    raise_errors=True,
                ),
                timeout=20,
            )
        except asyncio.TimeoutError:
            raise
        except Exception:
            entry = canonical_rail_entries()[entry_id]
            result = service._rail_read_failed_result(intent, entry)
    out = RunOutcome(
        run=run,
        result_none=result is None,
        message="" if result is None else str(getattr(result, "message", result) or ""),
        prompt="\n".join(prompts),
        hits=dict(hits.counts),
    )
    out.verdict = _judge(force, out)
    return out


async def force_entry(entry_id: str) -> List[RunOutcome]:
    force = FORCE[entry_id]
    return [await _run_once(entry_id, force, run) for run in force.runs]


# ─── Tests ──────────────────────────────────────────────────────────────────

_CANONICAL = sorted(canonical_rail_entries())


def test_denominator_is_the_registry_walk():
    from services.intent_service.workflow_dispatcher import wired_chat_actions

    assert len(_CANONICAL) > 0, "the rail walk found no entries; detection is broken (#1423)"
    assert set(_CANONICAL) <= set(wired_chat_actions())
    stale = sorted((set(FORCE) | set(EXEMPT)) - set(_CANONICAL))
    assert not stale, f"rows naming no canonical rail entry: {stale}"


def test_every_entry_is_in_exactly_one_place():
    both = sorted(set(FORCE) & set(EXEMPT))
    assert not both, f"in FORCE and EXEMPT at once: {both}"
    unmapped = sorted(set(_CANONICAL) - set(FORCE) - set(EXEMPT))
    assert not unmapped, (
        f"rail entries with no failure path: {unmapped}. Map each one's read seam in FORCE, "
        "or list it in EXEMPT with a reason (Arch reviews EXEMPT additions)."
    )
    assert len(FORCE) + len(EXEMPT) == len(_CANONICAL)
    not_forced = sorted(set(KNOWN_RED) - set(FORCE))
    assert not not_forced, f"KNOWN_RED rows must be forced rows: {not_forced}"
    for entry_id, force in FORCE.items():
        assert force.runs and all(r.seams for r in force.runs), f"{entry_id}: a run with no seam"
        for r in force.runs:
            assert set(r.seams) <= set(SEAMS) and set(r.pre) <= set(PRECONDITIONS), entry_id


def test_known_red_ceiling_only_falls():
    assert len(KNOWN_RED) <= KNOWN_RED_CEILING, (
        f"KNOWN_RED has {len(KNOWN_RED)} rows, over the ceiling {KNOWN_RED_CEILING}: a new red "
        "row is a defect to fix, not a row to add."
    )
    for entry_id, tag in KNOWN_RED.items():
        assert tag in CAUSE_TAGS, f"{entry_id}: unknown cause tag {tag!r}"


def test_not_performed_ceiling_only_falls():
    """#2215 part 2: the fourth state has its own shrink-only list; a row is forced (coverage),
    red (nothing can be stated), and not a silent failure (never in KNOWN_RED)."""
    assert len(NOT_PERFORMED) <= NOT_PERFORMED_CEILING, (
        f"NOT_PERFORMED has {len(NOT_PERFORMED)} rows, over the ceiling {NOT_PERFORMED_CEILING}: "
        "a read the product does not perform is a product gap to fix, not a row to add."
    )
    assert set(NOT_PERFORMED) <= set(FORCE), "NOT_PERFORMED rows must be forced rows"
    assert not (set(NOT_PERFORMED) & set(KNOWN_RED)), "a row is not performed OR silently failed"
    assert set(NOT_PERFORMED.values()) == {"NOT-PERFORMED"}
    assert "NOT-PERFORMED" in CAUSE_TAGS


@pytest.mark.parametrize("entry_id", sorted(FORCE))
async def test_forced_read_failure_is_not_said_as_verified(entry_id):
    outcomes = await force_entry(entry_id)
    unreached = [o for o in outcomes if o.verdict == "seam not reached"]
    assert not unreached, (
        f"{entry_id}: a forced seam was never called, so nothing was measured; fix its FORCE "
        "row. " + " | ".join(o.describe() for o in unreached)
    )
    passed = all(o.verdict == "pass" for o in outcomes)
    detail = " | ".join(o.describe() for o in outcomes)
    if entry_id in KNOWN_RED:
        assert (
            not passed
        ), f"fixed: remove {entry_id} from KNOWN_RED and lower KNOWN_RED_CEILING. {detail}"
    elif entry_id in NOT_PERFORMED:
        assert not passed, (
            f"{entry_id}: the product now performs this read; move it out of NOT_PERFORMED "
            f"(to green, or to KNOWN_RED with a cause tag) and lower NOT_PERFORMED_CEILING. {detail}"
        )
    else:
        assert passed, f"{entry_id}: a forced read failure was not said as failed. {detail}"


def test_every_cause_tag_is_in_the_inventory_header():
    """Arch 10-23: tags can't drift into one-offs. Every CAUSE_TAGS key (so every
    KNOWN_RED tag) is defined in the read-claim inventory YAML's header."""
    import re
    from pathlib import Path

    yaml_path = (
        Path(__file__).resolve().parents[4]
        / "docs/internal/architecture/current/read-claim-inventory.yaml"
    )
    header = yaml_path.read_text().split("\nsurfaces:", 1)[0]
    defined = set(re.findall(r"^#   ([A-Z][A-Z-]+)\s", header, flags=re.M))
    assert set(KNOWN_RED.values()) <= set(CAUSE_TAGS)
    missing = sorted(set(CAUSE_TAGS) - defined)
    assert not missing, f"cause tags not defined in the inventory header: {missing}"
