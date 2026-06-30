"""
GitHub MCP Spatial Adapter

GitHub-specific MCP spatial adapter implementation following the established
spatial adapter pattern for external system integration.
"""

import asyncio
import json
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import aiohttp

from services.integrations.mcp.token_counter import TokenCounter
from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialContext,
    SpatialPosition,
)

from services.connectors.binding_repository import ConnectorBindingRepository
from services.database.session_factory import AsyncSessionFactory
from services.integrations.github.repo_resolver import (
    ResolvedRepo,
    UnresolvedRepoError,
    resolve_repo,
)

from .connector import (
    Binding,
    ConnectRequired,
    ConnectorStatus,
    ConnectorStatusState,
    ConnectResult,
    DegradationReason,
    DegradationResponse,
    ResolveMiss,
    ResolveResult,
    ResourceHandle,
    ResourceQuery,
)
from .connector_grant_store import ConnectorGrantStore
from .mcp_client import MCPClient

_GITHUB = "github"

# The github-mcp-server tool that resolves a resource to a handle. PROVISIONAL
# (#1230 / #1220 provisioning): the concrete tool name + args depend on the chosen
# github-mcp-server; isolated here so the resolve() rail is testable against a fixture.
_RESOLVE_TOOL = "resolve_resource"

# The Settings route that starts the GitHub OAuth connect flow (#1317 inc.2 slice E) —
# surfaced as the connect action_hint on a CONNECT_REQUIRED honest-degrade.
_CONNECT_URL = "/api/v1/settings/integrations/github/connect"

# The github-mcp-server tool + canonical query for the user's open issues (#1322 cutover).
# search_issues is user-wide (assignee:@me, across repos) → no repo resolution, sidestepping
# the vestigial resolve_repo / #1230. De-risked live (179 issues). Isolated for testability.
_ISSUES_TOOL = "search_issues"
_MY_OPEN_ISSUES_QUERY = "assignee:@me is:open is:issue"
# PRs (#1322 P3): search_pull_requests, same payload shape, user-wide "PRs I opened".
_PRS_TOOL = "search_pull_requests"
_MY_OPEN_PRS_QUERY = "author:@me is:open is:pr"

# ── #1327 gap 2: repo-scoped read tools (github-mcp-server, authoritative tool names) ──
# These REQUIRE a target repo (resolve_repo) — unlike the user-wide search tools above.
# NOTE: github-mcp-server has NO list tool for milestones OR labels → both stay native-PAT
# (#1039 / #1040), NOT here. (Labels was briefly cut to a `list_label` connector tool in gap 2
# and reverted: live, `list_label` returned `unknown tool`; the server exposes only `get_label`,
# fetching ONE label by name, with no list-labels tool.)
_BRANCHES_TOOL = "list_branches"  # args: owner, repo, page, perPage
_RELEASES_TOOL = "list_releases"  # args: owner, repo, page, perPage
# Single-issue read is the CONSOLIDATED issue_read tool (method="get"), not a get_issue tool.
_ISSUE_READ_TOOL = "issue_read"  # args: owner, repo, issue_number, method
_ISSUE_READ_GET = "get"

# Stored non-BOUND binding statuses → the honest ResolveMiss reason (#1231).
_NONBOUND_REASON = {
    ConnectorStatusState.STALE.value: DegradationReason.STALE_TOKEN,
    ConnectorStatusState.UNREACHABLE.value: DegradationReason.UNREACHABLE,
}

logger = logging.getLogger(__name__)


@dataclass
class GitHubIssuesResult:
    """Connector issue-fetch result (#1322): issues on success, else an honest degrade.

    Exactly one of ``issues`` / ``degradation`` is set. Chat handlers branch on it —
    issues → answer; degradation → the honest "Connect GitHub" message (+ connect link),
    never a silent empty list (#1231).
    """

    issues: Optional[List[Dict[str, Any]]] = None
    total: Optional[int] = None  # TRUE match count (search_issues total_count); issues is a page
    degradation: Optional[DegradationResponse] = None


@dataclass
class GitHubRepoScopedResult:
    """Connector repo-scoped LIST-read result (#1327 gap 2): items on success, else honest degrade.

    The repo-scoped counterpart to ``GitHubIssuesResult`` — for branches / releases,
    which target ONE repo (resolved via ``resolve_repo``). Exactly one of ``items`` /
    ``degradation`` is set. ``resolved_repo`` (``owner/name``) is surfaced on success so the
    handler can name the repo it read. ``REPO_UNRESOLVED`` degradation = the "which repo?" case
    (no target repo) — never a silent empty, never get-all (#1231 / #1327 doc-of-record).
    """

    items: Optional[List[Dict[str, Any]]] = None
    resolved_repo: Optional[str] = None  # "owner/name" on a hit (which repo we read)
    degradation: Optional[DegradationResponse] = None


@dataclass
class GitHubIssueResult:
    """Connector single-issue read result (#1327 gap 2, "review issue #N"): item or honest degrade.

    Like ``GitHubRepoScopedResult`` but a single ``item`` dict (one issue) rather than a list.
    """

    item: Optional[Dict[str, Any]] = None
    resolved_repo: Optional[str] = None
    degradation: Optional[DegradationResponse] = None


class GitHubMCPSpatialAdapter(BaseSpatialAdapter):
    """
    GitHub MCP spatial adapter implementation.

    Maps GitHub issue numbers to spatial positions using MCP protocol
    for external service integration.
    """

    def __init__(self):
        super().__init__("github_mcp")
        self._lock = asyncio.Lock()
        self._issue_to_position: Dict[str, int] = {}
        self._position_to_issue: Dict[int, str] = {}
        self._context_storage: Dict[str, Dict[str, Any]] = {}

        # GitHub API configuration
        self._github_token: Optional[str] = None
        self._github_api_base = "https://api.github.com"
        self._session: Optional[aiohttp.ClientSession] = None

        # Token counting for MCP operations (Issue #369)
        self.token_counter = TokenCounter()

        logger.info("GitHubMCPSpatialAdapter initialized")

    # ── #1232 (RECONNECT WS-5) Connector-protocol conformance (ADR-070 D5) ──
    # #1317 port, increment 1 (2026-06-26): connect()/status() now read the per-user
    # ConnectorBinding store (#1229 / ADR-070 D3 — Piper stores bindings, never raw
    # tokens). The OAuth redirect-orchestrator + callback that CREATES the binding
    # (ADR-070 OQ-5: MCP server owns OAuth) is increment 2; resolve() via the MCP
    # client is increment 3. Honest-degrade throughout (never silently empty).
    IMPLEMENTS_CONNECTOR = (
        True  # #1232: AST-guard (test_connector_contract_1232) enforces the 4 methods
    )

    async def connect(self, user_id: str) -> ConnectResult:
        """Bound already → return the Binding; otherwise the must-be-handled ConnectRequired.

        (#1317 inc.2 adds the redirect-orchestrator + callback that creates the binding —
        until then an unbound user honestly gets "connect me", never a fake success.)
        """
        async with AsyncSessionFactory.session_scope() as session:
            binding = await ConnectorBindingRepository(session).get(user_id, _GITHUB)
        if binding is not None and binding.status == ConnectorStatusState.BOUND.value:
            return Binding(binding_id=str(binding.id))
        return ConnectRequired(degradation=await self.degrade(DegradationReason.CONNECT_REQUIRED))

    async def status(self, user_id: str) -> ConnectorStatus:
        """The user's GitHub binding health (ADR-070 D5) — read from the binding store, no
        resource fetch, no token (D3). No binding → UNBOUND (the user must connect)."""
        async with AsyncSessionFactory.session_scope() as session:
            binding = await ConnectorBindingRepository(session).get(user_id, _GITHUB)
        if binding is None:
            return ConnectorStatus(
                state=ConnectorStatusState.UNBOUND,
                detail="No GitHub binding — connect to continue.",
            )
        try:
            state = ConnectorStatusState(binding.status)
        except ValueError:
            state = ConnectorStatusState.UNBOUND  # unknown stored status → honest UNBOUND
        return ConnectorStatus(state=state, detail=f"GitHub binding status: {binding.status}")

    async def resolve(self, user_id: str, resource: ResourceQuery) -> ResolveResult:
        """Resolve a GitHub resource to a handle over the real MCP transport (#1220) —
        honest-degrade throughout (#1231 / ADR-070 D5: never silently empty).

        The binding-aware degrade rail (no binding / stale / unreachable / server-down →
        the matching ``ResolveMiss``) is server-agnostic and fully real. The concrete
        github-mcp-server resolution (#1230) rides the real ``MCPClient`` transport; its
        tool mapping + server provisioning are gated on the #1220 infra decision (see
        ``_resolve_via_mcp`` / ``_server_params_for``), so a BOUND-but-unprovisioned
        binding honestly degrades to UNREACHABLE rather than faking a result.
        """
        async with AsyncSessionFactory.session_scope() as session:
            binding = await ConnectorBindingRepository(session).get(user_id, _GITHUB)

        # ── honest-degrade rail (#1231): degrade on binding state, never silently empty ──
        if binding is None:
            return ResolveMiss(await self.degrade(DegradationReason.CONNECT_REQUIRED))
        if binding.status != ConnectorStatusState.BOUND.value:
            reason = _NONBOUND_REASON.get(binding.status, DegradationReason.CONNECT_REQUIRED)
            return ResolveMiss(await self.degrade(reason))

        # ── bound → resolve over the real MCP transport; any failure → honest UNREACHABLE ──
        try:
            async with self._mcp_client_ctx(binding) as client:
                handle = await self._resolve_via_mcp(client, resource)
        except Exception:
            logger.warning(
                "GitHub MCP resolve failed (server unreachable/unprovisioned)", exc_info=True
            )
            return ResolveMiss(await self.degrade(DegradationReason.UNREACHABLE))

        if not handle:
            return ResolveMiss(await self.degrade(DegradationReason.RESOURCE_NOT_FOUND))
        return ResourceHandle(handle=handle, kind=resource.kind)

    async def degrade(self, reason: DegradationReason) -> DegradationResponse:
        messages = {
            DegradationReason.CONNECT_REQUIRED: "Connect GitHub to continue.",
            DegradationReason.RESOURCE_NOT_FOUND: "That GitHub resource wasn't found.",
            DegradationReason.UNREACHABLE: "GitHub's MCP server is unreachable right now.",
            DegradationReason.STALE_TOKEN: "Your GitHub connection needs re-authorizing.",
            DegradationReason.REPO_UNRESOLVED: (
                "Which repo? I couldn't tell which repository you mean — name one "
                "(e.g. `owner/name`), link a repo to your project, or set a default repo."
            ),
        }
        return DegradationResponse(
            reason=reason,
            user_message=messages.get(reason, "The GitHub connector is degraded."),
            action_hint=(_CONNECT_URL if reason is DegradationReason.CONNECT_REQUIRED else None),
        )

    # ── #1322 cutover: the user's open issues / PRs over the OAuth connector ──
    async def list_open_issues(self, user_id: str, *, limit: int = 50) -> GitHubIssuesResult:
        """List the user's open GitHub issues over the per-user OAuth connector (#1322).

        The RECONNECT chat-cutover read primitive — reads via the user's binding + grant
        (``search_issues``, user-wide ``assignee:@me`` across repos → no repo resolution,
        sidestepping the vestigial ``resolve_repo`` / #1230), NOT the native shared PAT.
        """
        return await self._search_via_connector(
            user_id, tool=_ISSUES_TOOL, query=_MY_OPEN_ISSUES_QUERY, limit=limit
        )

    async def list_open_prs(self, user_id: str, *, limit: int = 50) -> GitHubIssuesResult:
        """List the user's open GitHub pull requests over the OAuth connector (#1322 P3).

        Same binding-aware rail as ``list_open_issues`` — ``search_pull_requests`` with the
        user-wide ``author:@me`` query (PRs you opened, across repos). The result's ``issues``
        field holds the PR item page (``GitHubIssuesResult`` serves both issue + PR searches —
        identical ``total_count`` + ``items`` payload shape, verified live).
        """
        return await self._search_via_connector(
            user_id, tool=_PRS_TOOL, query=_MY_OPEN_PRS_QUERY, limit=limit
        )

    async def _search_via_connector(
        self, user_id: str, *, tool: str, query: str, limit: int
    ) -> GitHubIssuesResult:
        """Binding-aware GitHub search over the OAuth connector → (item page + true total), or
        an honest degrade — the shared rail behind ``list_open_issues`` / ``list_open_prs``.

        Honest-degrade throughout (#1231, never a silent empty): no binding → CONNECT_REQUIRED
        (+ connect link); non-bound → its stored reason; bound-but-server-unreachable →
        UNREACHABLE. Mirrors ``resolve()``'s rail. (Rule-of-three dedup of the per-connector
        rail into a shared mixin is tracked as #1323.)
        """
        async with AsyncSessionFactory.session_scope() as session:
            binding = await ConnectorBindingRepository(session).get(user_id, _GITHUB)
        if binding is None:
            return GitHubIssuesResult(
                degradation=await self.degrade(DegradationReason.CONNECT_REQUIRED)
            )
        if binding.status != ConnectorStatusState.BOUND.value:
            reason = _NONBOUND_REASON.get(binding.status, DegradationReason.CONNECT_REQUIRED)
            return GitHubIssuesResult(degradation=await self.degrade(reason))
        try:
            async with self._mcp_client_ctx(binding) as client:
                result = await client.call_tool(tool, {"query": query})
                items, total = self._parse_issue_search(
                    self._first_text(result.content), limit=limit
                )
        except Exception:
            logger.warning(
                "GitHub MCP search failed (server unreachable/unprovisioned)", exc_info=True
            )
            return GitHubIssuesResult(
                degradation=await self.degrade(DegradationReason.UNREACHABLE)
            )
        return GitHubIssuesResult(issues=items, total=total)

    @staticmethod
    def _parse_issue_search(
        payload: Optional[str], *, limit: int
    ) -> "tuple[List[Dict[str, Any]], Optional[int]]":
        """Parse a ``search_issues`` JSON payload → ``(issue dicts truncated, total match count)``.

        ``total_count`` is authoritative (the full match count); for a ``list_issues`` payload
        shape (no total_count) the count falls back to the number of items returned.
        """
        if not payload:
            return [], 0
        try:
            data = json.loads(payload)
        except (ValueError, TypeError):
            return [], None
        if not isinstance(data, dict):
            return [], None
        items = data.get("items")
        if items is None:
            items = data.get("issues")  # tolerate the list_issues payload shape too
        items = items or []
        total = data.get("total_count")
        if total is None:
            total = len(items)  # list_issues shape: count is what we got
        return items[:limit], total

    # ── #1327 gap 2: repo-scoped reads over the OAuth connector (branches/releases/issue) ──
    # Mirror the #1322 user-wide rail, but repo-scoped: resolve_repo() FIRST (a target repo is
    # REQUIRED), then call the github-mcp-server repo-scoped tool with {owner, repo, ...}. On
    # UnresolvedRepoError → honest REPO_UNRESOLVED ("which repo?"), never silent-empty / get-all.

    async def list_branches_connector(
        self, user_id: str, *, explicit_repo: Optional[str] = None, project_id=None
    ) -> GitHubRepoScopedResult:
        """List a repo's branches over the OAuth connector (#1327). Tool: ``list_branches``.

        The pattern-establishing repo-scoped read. Resolves the target repo via
        ``resolve_repo`` then reads via the user's binding + grant — NOT the native shared PAT.
        Branch dicts are normalized to ``{name, protected, commit_sha}`` (the shape the handler
        + the native ``list_branches`` already use).
        """
        return await self._repo_scoped_list_via_connector(
            user_id,
            tool=_BRANCHES_TOOL,
            parse=self._parse_branches,
            explicit_repo=explicit_repo,
            project_id=project_id,
        )

    # NOTE: there is intentionally NO list_labels_connector. github-mcp-server has no list-labels
    # tool (only get_label for ONE label by name), so labels stays native (#1040) — mirror
    # milestones. The gap-2 `list_label` connector cutover was reverted (live: `unknown tool`).

    async def list_releases_connector(
        self, user_id: str, *, explicit_repo: Optional[str] = None, project_id=None
    ) -> GitHubRepoScopedResult:
        """List a repo's releases over the OAuth connector (#1327). Tool: ``list_releases``.

        Release dicts normalized to ``{tag_name, name, published_at, prerelease, draft,
        html_url, body}`` (the native shape; body truncated to keep memory bounded).
        """
        return await self._repo_scoped_list_via_connector(
            user_id,
            tool=_RELEASES_TOOL,
            parse=self._parse_releases,
            explicit_repo=explicit_repo,
            project_id=project_id,
        )

    async def get_issue_connector(
        self,
        user_id: str,
        *,
        issue_number: int,
        explicit_repo: Optional[str] = None,
        project_id=None,
    ) -> GitHubIssueResult:
        """Read a single repo issue over the OAuth connector (#1327, "review issue #N").

        Tool: the consolidated ``issue_read`` with ``method="get"`` (github-mcp-server has no
        standalone ``get_issue``). Resolves the repo via ``resolve_repo`` (honoring an explicit
        ``owner/name`` from "issue #N in owner/name"). Issue dict normalized to the native
        ``get_github_issue_direct`` shape so the handler renders identically.
        """
        resolved = await self._resolve_or_degrade(
            user_id, explicit_repo=explicit_repo, project_id=project_id
        )
        if isinstance(resolved, DegradationResponse):
            return GitHubIssueResult(degradation=resolved)

        binding_or_degrade = await self._bound_binding_or_degrade(user_id)
        if isinstance(binding_or_degrade, DegradationResponse):
            return GitHubIssueResult(degradation=binding_or_degrade)

        try:
            async with self._mcp_client_ctx(binding_or_degrade) as client:
                result = await client.call_tool(
                    _ISSUE_READ_TOOL,
                    {
                        "owner": resolved.owner,
                        "repo": resolved.name,
                        "issue_number": issue_number,
                        "method": _ISSUE_READ_GET,
                    },
                )
                item = self._parse_issue_detail(self._first_text(result.content))
        except Exception:
            logger.warning(
                "GitHub MCP issue_read failed (server unreachable/unprovisioned)", exc_info=True
            )
            return GitHubIssueResult(degradation=await self.degrade(DegradationReason.UNREACHABLE))
        return GitHubIssueResult(item=item, resolved_repo=resolved.full_name)

    async def _repo_scoped_list_via_connector(
        self, user_id: str, *, tool: str, parse, explicit_repo=None, project_id=None
    ) -> GitHubRepoScopedResult:
        """Shared repo-scoped LIST rail: resolve_repo → bound binding → call tool → parse, or
        an honest degrade — the rail behind ``list_branches/releases_connector``.

        Order mirrors the #1322 ``_search_via_connector`` rail with repo resolution prepended:
        UnresolvedRepoError → REPO_UNRESOLVED ("which repo?"); no binding → CONNECT_REQUIRED
        (+ link); non-bound → stored reason; bound-but-unreachable → UNREACHABLE. Never a silent
        empty (#1231). ``parse`` maps the tool's JSON payload → normalized item dicts.
        """
        resolved = await self._resolve_or_degrade(
            user_id, explicit_repo=explicit_repo, project_id=project_id
        )
        if isinstance(resolved, DegradationResponse):
            return GitHubRepoScopedResult(degradation=resolved)

        binding_or_degrade = await self._bound_binding_or_degrade(user_id)
        if isinstance(binding_or_degrade, DegradationResponse):
            return GitHubRepoScopedResult(degradation=binding_or_degrade)

        try:
            async with self._mcp_client_ctx(binding_or_degrade) as client:
                result = await client.call_tool(
                    tool, {"owner": resolved.owner, "repo": resolved.name}
                )
                items = parse(self._first_text(result.content))
        except Exception:
            logger.warning(
                "GitHub MCP repo-scoped read failed (server unreachable/unprovisioned)",
                exc_info=True,
            )
            return GitHubRepoScopedResult(
                degradation=await self.degrade(DegradationReason.UNREACHABLE)
            )
        return GitHubRepoScopedResult(items=items, resolved_repo=resolved.full_name)

    async def _resolve_or_degrade(self, user_id, *, explicit_repo=None, project_id=None):
        """Resolve the target repo, or return a REPO_UNRESOLVED degrade ("which repo?").

        Repo-scoped reads REQUIRE a repo (#1327 doc-of-record): an ``UnresolvedRepoError`` must
        become an honest "which repo?" — NEVER a get-all or a silent empty (#1231). Returns a
        ``ResolvedRepo`` on success or a ``DegradationResponse`` the caller wraps in its result.
        """
        user_uuid = self._coerce_user_uuid(user_id)
        try:
            return await resolve_repo(
                user_id=user_uuid, project_id=project_id, explicit=explicit_repo
            )
        except UnresolvedRepoError:
            return await self.degrade(DegradationReason.REPO_UNRESOLVED)

    async def _bound_binding_or_degrade(self, user_id):
        """Return the user's BOUND github binding, or the honest degrade for its absence/state.

        The binding half of the #1322 rail, factored out so the repo-scoped reads share it:
        no binding → CONNECT_REQUIRED (+ connect link); non-bound status → its mapped reason.
        """
        async with AsyncSessionFactory.session_scope() as session:
            binding = await ConnectorBindingRepository(session).get(user_id, _GITHUB)
        if binding is None:
            return await self.degrade(DegradationReason.CONNECT_REQUIRED)
        if binding.status != ConnectorStatusState.BOUND.value:
            reason = _NONBOUND_REASON.get(binding.status, DegradationReason.CONNECT_REQUIRED)
            return await self.degrade(reason)
        return binding

    @staticmethod
    def _coerce_user_uuid(user_id):
        """Coerce a user_id to a UUID for resolve_repo's user-default lookup (None on non-UUID).

        resolve_repo's user-scoped paths take a UUID; a non-UUID / None principal simply skips
        those paths (the explicit/project/env paths still apply) — never an error."""
        from uuid import UUID

        if isinstance(user_id, UUID):
            return user_id
        if isinstance(user_id, str):
            try:
                return UUID(user_id)
            except (ValueError, TypeError):
                return None
        return None

    @staticmethod
    def _parse_branches(payload: Optional[str]) -> List[Dict[str, Any]]:
        """Parse a ``list_branches`` JSON array → normalized ``{name, protected, commit_sha}``."""
        out = []
        for b in GitHubMCPSpatialAdapter._json_array(payload):
            commit = b.get("commit") or {}
            out.append(
                {
                    "name": b.get("name", ""),
                    "protected": bool(b.get("protected")),
                    "commit_sha": commit.get("sha", "") if isinstance(commit, dict) else "",
                }
            )
        return out

    # NOTE: no _parse_labels — labels reverted to native (no github-mcp-server list-labels tool).

    @staticmethod
    def _parse_releases(payload: Optional[str]) -> List[Dict[str, Any]]:
        """Parse a ``list_releases`` JSON array → the native release dict shape (body truncated)."""
        out = []
        for r in GitHubMCPSpatialAdapter._json_array(payload):
            body = r.get("body") or ""
            if len(body) > 500:
                body = body[:500] + "..."
            out.append(
                {
                    "tag_name": r.get("tag_name", ""),
                    "name": r.get("name") or r.get("tag_name", ""),
                    "published_at": r.get("published_at"),
                    "prerelease": bool(r.get("prerelease")),
                    "draft": bool(r.get("draft")),
                    "html_url": r.get("html_url"),
                    "body": body,
                }
            )
        return out

    @staticmethod
    def _parse_issue_detail(payload: Optional[str]) -> Optional[Dict[str, Any]]:
        """Parse an ``issue_read`` (method=get) JSON object → the native get_issue_direct shape.

        Returns ``None`` for an empty/unparseable payload (handler renders "couldn't find #N").
        """
        if not payload:
            return None
        try:
            data = json.loads(payload)
        except (ValueError, TypeError):
            return None
        if not isinstance(data, dict) or not data:
            return None
        labels = data.get("labels") or []
        assignees = data.get("assignees") or []
        return {
            "number": data.get("number"),
            "title": data.get("title"),
            "description": data.get("body", ""),
            "body": data.get("body", ""),
            "state": data.get("state"),
            "uri": data.get("html_url"),
            "html_url": data.get("html_url"),
            "labels": [
                lbl.get("name", "") if isinstance(lbl, dict) else lbl for lbl in labels
            ],
            "assignees": [
                a.get("login", "") if isinstance(a, dict) else a for a in assignees
            ],
            "milestone": (
                data.get("milestone", {}).get("title")
                if isinstance(data.get("milestone"), dict)
                else None
            ),
            "user": (data.get("user") or {}).get("login")
            if isinstance(data.get("user"), dict)
            else None,
            "retrieved_via": "github_connector",
        }

    @staticmethod
    def _json_array(payload: Optional[str]) -> List[Dict[str, Any]]:
        """Parse a JSON payload to a list of dicts (tolerant): ``[]`` on empty/non-list/error.

        github-mcp-server repo-scoped list tools return a JSON array; some wrap it as
        ``{"items": [...]}`` — tolerate both shapes (mirrors ``_parse_issue_search``)."""
        if not payload:
            return []
        try:
            data = json.loads(payload)
        except (ValueError, TypeError):
            return []
        if isinstance(data, dict):
            data = data.get("items") or data.get("branches") or []
        if not isinstance(data, list):
            return []
        return [item for item in data if isinstance(item, dict)]

    # ── resolve() transport seam (the real MCP path; #1220) ──
    # Isolated so resolve()'s degrade rail is testable against a fixture-backed client,
    # and so the provisioning-gated bits below are confined to two small methods.

    @asynccontextmanager
    async def _mcp_client_ctx(self, binding):
        """Yield a connected ``MCPClient`` for this binding — streamable-HTTP to the
        self-hosted ``github-mcp-server`` (ADR-070 C), forwarding the user's stored OAuth
        grant as the ``Authorization`` header. ``binding.mcp_server_ref`` is the server
        URL; the grant lives in the #358 store (the binding row holds no token — D3).

        Tests patch this method to yield a fixture-backed client (bypassing the live
        connect). A connect failure / missing grant surfaces as ``resolve()`` UNREACHABLE.
        """
        async with AsyncSessionFactory.session_scope() as session:
            grant = await ConnectorGrantStore().get(session, str(binding.owner_id), _GITHUB)
        headers = {"Authorization": f"Bearer {grant}"} if grant else None
        async with MCPClient.connect_http(binding.mcp_server_ref, headers=headers) as client:
            yield client

    async def _resolve_via_mcp(self, client: MCPClient, resource: ResourceQuery) -> Optional[str]:
        """Resolve a resource to a handle via the GitHub MCP server (real round-trip).

        Returns the handle string, or ``None`` for a miss. PROVISIONAL (#1230 / #1220):
        the tool name + args + result parsing depend on the chosen github-mcp-server; the
        WIRING (binding → real ``MCPClient`` → result → handle) is proven against a FastMCP
        fixture, with the tool identifier (``_RESOLVE_TOOL``) the one provisional constant.
        """
        result = await client.call_tool(_RESOLVE_TOOL, {"kind": resource.kind, **resource.params})
        return self._first_text(result.content) or None

    @staticmethod
    def _first_text(content) -> str:
        """First non-empty ``.text`` off an SDK content list (TextContent items)."""
        for item in content or []:
            text = getattr(item, "text", None)
            if text:
                return text
        return ""

    async def configure_github_api(
        self, token: Optional[str] = None, api_base: Optional[str] = None
    ):
        """Configure GitHub API access"""
        try:
            self._github_token = token
            if api_base:
                self._github_api_base = api_base

            # Create HTTP session for GitHub API calls
            if self._session is None:
                headers = {}
                if self._github_token:
                    headers["Authorization"] = f"token {self._github_token}"
                headers["Accept"] = "application/vnd.github.v3+json"

                self._session = aiohttp.ClientSession(headers=headers)
                logger.info("GitHub API session created")

            return True

        except Exception as e:
            logger.error(f"Error configuring GitHub API: {e}")
            return False

    async def _call_github_api(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Make GitHub API call"""
        try:
            if not self._session:
                logger.warning("GitHub API session not configured")
                return None

            url = f"{self._github_api_base}/{endpoint}"
            async with self._session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 401:
                    logger.error("GitHub API authentication failed")
                    return None
                elif response.status == 403:
                    logger.error("GitHub API rate limit exceeded")
                    return None
                else:
                    logger.error(f"GitHub API error: {response.status}")
                    return None

        except Exception as e:
            logger.error(f"Error calling GitHub API: {e}")
            return None

    async def _post_github_api(
        self, endpoint: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Make GitHub API POST call"""
        try:
            if not self._session:
                logger.warning("GitHub API session not configured")
                return None

            url = f"{self._github_api_base}/{endpoint}"
            async with self._session.post(url, json=data) as response:
                if response.status in (200, 201):
                    return await response.json()
                elif response.status == 401:
                    logger.error("GitHub API authentication failed")
                    return None
                elif response.status == 403:
                    logger.error("GitHub API rate limit exceeded")
                    return None
                else:
                    logger.error(f"GitHub API error: {response.status}")
                    return None

        except Exception as e:
            logger.error(f"Error calling GitHub API: {e}")
            return None

    async def _patch_github_api(
        self, endpoint: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Make GitHub API PATCH call.

        Issue #902: Added for update operations (close/reopen issues, edit titles, etc.).
        Mirrors _post_github_api but uses PATCH method.
        """
        try:
            if not self._session:
                logger.warning("GitHub API session not configured")
                return None

            url = f"{self._github_api_base}/{endpoint}"
            async with self._session.patch(url, json=data) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 401:
                    logger.error("GitHub API authentication failed")
                    return None
                elif response.status == 403:
                    logger.error("GitHub API rate limit exceeded")
                    return None
                elif response.status == 404:
                    logger.error(f"GitHub resource not found: {endpoint}")
                    return None
                elif response.status == 422:
                    error_body = await response.text()
                    logger.error(f"GitHub API validation error: {response.status} — {error_body}")
                    return None
                else:
                    logger.error(f"GitHub API error: {response.status}")
                    return None

        except Exception as e:
            logger.error(f"Error calling GitHub API PATCH: {e}")
            return None

    async def create_issue(
        self,
        owner: str,
        repo_name: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a GitHub issue via the REST API.

        Issue #892: This method was missing from GitHubMCPSpatialAdapter,
        causing AttributeError when GitHubIntegrationRouter._get_integration()
        returned the MCP adapter for create_issue operations.

        Issue #1042: ``owner`` is now a required positional arg (was hardcoded
        to "mediajunkie"). Callers must resolve owner via ``repo_resolver``.
        """
        endpoint = f"repos/{owner}/{repo_name}/issues"
        data: Dict[str, Any] = {"title": title, "body": body}
        if labels:
            data["labels"] = labels
        if assignees:
            data["assignees"] = assignees
        result = await self._post_github_api(endpoint, data)
        if result is None:
            raise RuntimeError("Failed to create GitHub issue — API returned no response")
        return result

    async def update_issue(
        self,
        owner: str,
        repo_name: str,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Update a GitHub issue via the REST API.

        Issue #902: Completes the issue lifecycle — create, update, close, reopen.
        Previously missing, causing AttributeError when router delegated
        update_issue to MCP adapter.

        Issue #1042: ``owner`` is now a required positional arg (was hardcoded
        to "mediajunkie"). Callers must resolve owner via ``repo_resolver``.

        Args:
            owner: Repository owner (e.g., GitHub username/org)
            repo_name: Repository name (without owner prefix)
            issue_number: Issue number to update
            title: New title (optional)
            body: New body (optional)
            state: "open" or "closed" (optional)
            labels: New label list (optional, replaces existing)
            assignees: New assignee list (optional, replaces existing)
        """
        endpoint = f"repos/{owner}/{repo_name}/issues/{issue_number}"
        data: Dict[str, Any] = {}
        if title is not None:
            data["title"] = title
        if body is not None:
            data["body"] = body
        if state is not None:
            data["state"] = state
        if labels is not None:
            data["labels"] = labels
        if assignees is not None:
            data["assignees"] = assignees

        if not data:
            raise ValueError("update_issue called with no fields to update")

        result = await self._patch_github_api(endpoint, data)
        if result is None:
            raise RuntimeError(
                f"Failed to update GitHub issue #{issue_number} — API returned no response"
            )
        return result

    async def add_comment(
        self, owner: str, repo_name: str, issue_number: int, body: str
    ) -> Optional[Dict[str, Any]]:
        """Add comment to GitHub issue.

        Issue #1042: ``owner`` is now a required positional arg.
        """
        endpoint = f"repos/{owner}/{repo_name}/issues/{issue_number}/comments"
        return await self._post_github_api(endpoint, {"body": body})

    async def list_github_issues_direct(self, repo: str, owner: str) -> List[Dict[str, Any]]:
        """List GitHub issues directly via GitHub API.

        Issue #1042: ``repo`` and ``owner`` are now required positional args
        (were defaulted to "piper-morgan-product" / "mediajunkie"). Callers
        must resolve via ``repo_resolver``.
        """
        try:

            async def _operation():
                endpoint = f"repos/{owner}/{repo}/issues"
                params = {"state": "all", "per_page": 100}

                issues_data = await self._call_github_api(endpoint, params)
                if not issues_data:
                    logger.warning("No GitHub issues data received")
                    return []

                # Transform GitHub API response to our format
                issues = []
                for issue in issues_data:
                    issue_info = {
                        "number": issue.get("number"),
                        "title": issue.get("title"),
                        "description": issue.get("body", ""),
                        "state": issue.get("state"),
                        "repository": repo,
                        "uri": issue.get("html_url"),
                        "mime_type": "text/markdown",
                        "created_at": issue.get("created_at"),
                        "updated_at": issue.get("updated_at"),
                        "labels": [label["name"] for label in issue.get("labels", [])],
                        "assignees": [assignee["login"] for assignee in issue.get("assignees", [])],
                        "milestone": (
                            issue.get("milestone", {}).get("title")
                            if issue.get("milestone")
                            else None
                        ),
                        "user": issue.get("user", {}).get("login"),
                        # #986: GitHub's /issues endpoint returns PRs as issues
                        # with a `pull_request` object; absent on plain issues.
                        # Preserved as a bool so callers can distinguish.
                        "is_pull_request": issue.get("pull_request") is not None,
                        "retrieved_via": "github_api",
                    }
                    issues.append(issue_info)

                    # Store context for spatial mapping
                    await self._store_github_context(issue_info)

                return issues

            result = await self.token_counter.wrap_mcp_call(
                "github_list_issues_direct",
                _operation(),
                input_data=f"repo={repo},owner={owner}",
            )
            logger.info(f"Retrieved {len(result)} issues from GitHub API for {owner}/{repo}")
            return result

        except Exception as e:
            logger.error(f"Error listing GitHub issues directly: {e}")
            return []

    async def get_closed_issues(
        self,
        repo: str,
        owner: str,
        project: str = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """#969: Get closed issues from GitHub API.

        Filters issues by state=closed. Used by _handle_shipped_this_week().

        Issue #1042: ``repo`` and ``owner`` are now required positional args
        (were defaulted to "piper-morgan-product" / "mediajunkie").
        """
        try:
            endpoint = f"repos/{owner}/{repo}/issues"
            params = {"state": "closed", "per_page": min(limit, 100)}
            issues_data = await self._call_github_api(endpoint, params)
            if not issues_data:
                return []

            issues = []
            for issue in issues_data:
                issues.append(
                    {
                        "number": issue.get("number"),
                        "title": issue.get("title"),
                        "state": issue.get("state"),
                        "closed_at": issue.get("closed_at"),
                        "repository": repo,
                        "labels": [label["name"] for label in issue.get("labels", [])],
                        "user": issue.get("user", {}).get("login"),
                    }
                )
            return issues

        except Exception as e:
            logger.error(f"Error getting closed issues: {e}")
            return []

    async def list_milestones(
        self, repo: str, owner: str, state: str = "open"
    ) -> List[Dict[str, Any]]:
        """List GitHub milestones for a repo (Issue #1039).

        Args:
            repo: Repository name (required; per #1042 no defaults)
            owner: Repository owner (required; per #1042 no defaults)
            state: GitHub milestone state filter — "open" (default), "closed",
                or "all". State-filter user-facing UX is deferred to #1051;
                this kwarg is the underlying capability.

        Returns:
            List of normalized milestone dicts with keys: title, number,
            state, due_on, open_issues, closed_issues, html_url, description.
            Empty list on any failure.
        """
        try:
            endpoint = f"repos/{owner}/{repo}/milestones"
            params = {"state": state, "per_page": 100}
            milestones_data = await self._call_github_api(endpoint, params)
            if not milestones_data:
                return []

            milestones = []
            for m in milestones_data:
                milestones.append(
                    {
                        "title": m.get("title", "Untitled"),
                        "number": m.get("number"),
                        "state": m.get("state"),
                        "due_on": m.get("due_on"),
                        "open_issues": m.get("open_issues", 0),
                        "closed_issues": m.get("closed_issues", 0),
                        "html_url": m.get("html_url"),
                        "description": m.get("description") or "",
                    }
                )
            logger.info(
                f"Retrieved {len(milestones)} milestones from {owner}/{repo} (state={state})"
            )
            return milestones

        except Exception as e:
            logger.error(f"Error listing milestones for {owner}/{repo}: {e}")
            return []

    async def list_releases(self, repo: str, owner: str) -> List[Dict[str, Any]]:
        """List GitHub releases for a repo (Issue #1039).

        Args:
            repo: Repository name (required; per #1042 no defaults)
            owner: Repository owner (required; per #1042 no defaults)

        Returns:
            List of normalized release dicts with keys: tag_name, name,
            published_at, prerelease, draft, html_url, body. Empty list
            on any failure.

        Note: prerelease-only / stable-only filter is deferred to #1051.
        Handler shows prerelease flag inline where useful.
        """
        try:
            endpoint = f"repos/{owner}/{repo}/releases"
            params = {"per_page": 100}
            releases_data = await self._call_github_api(endpoint, params)
            if not releases_data:
                return []

            releases = []
            for r in releases_data:
                body = r.get("body") or ""
                # Truncate body to keep memory bounded; full body via html_url
                if len(body) > 500:
                    body = body[:500] + "..."
                releases.append(
                    {
                        "tag_name": r.get("tag_name", ""),
                        "name": r.get("name") or r.get("tag_name", ""),
                        "published_at": r.get("published_at"),
                        "prerelease": bool(r.get("prerelease")),
                        "draft": bool(r.get("draft")),
                        "html_url": r.get("html_url"),
                        "body": body,
                    }
                )
            logger.info(f"Retrieved {len(releases)} releases from {owner}/{repo}")
            return releases

        except Exception as e:
            logger.error(f"Error listing releases for {owner}/{repo}: {e}")
            return []

    async def list_labels(self, repo: str, owner: str) -> List[Dict[str, Any]]:
        """List GitHub labels for a repo (Issue #1040).

        Args:
            repo: Repository name (required; per #1042 no defaults)
            owner: Repository owner (required; per #1042 no defaults)

        Returns:
            List of normalized label dicts with keys: name, color, description,
            html_url. Empty list on any failure.
        """
        try:
            endpoint = f"repos/{owner}/{repo}/labels"
            params = {"per_page": 100}
            labels_data = await self._call_github_api(endpoint, params)
            if not labels_data:
                return []

            labels = []
            for label in labels_data:
                labels.append(
                    {
                        "name": label.get("name", ""),
                        "color": label.get("color", ""),
                        "description": label.get("description") or "",
                        "html_url": label.get("url"),
                    }
                )
            logger.info(f"Retrieved {len(labels)} labels from {owner}/{repo}")
            return labels

        except Exception as e:
            logger.error(f"Error listing labels for {owner}/{repo}: {e}")
            return []

    async def list_branches(self, repo: str, owner: str) -> List[Dict[str, Any]]:
        """List GitHub branches for a repo (Issue #1040).

        Args:
            repo: Repository name (required; per #1042 no defaults)
            owner: Repository owner (required; per #1042 no defaults)

        Returns:
            List of normalized branch dicts with keys: name, protected,
            commit_sha. Default-branch identification happens at the
            handler layer (compares against repo's default_branch).
            Empty list on any failure.

        Note: per Q5 disposition, returns ALL branches; default-vs-non-default
        sorting + filtering for "feature branches" colloquial query happens
        at the handler layer. Filter syntax (e.g., claude/* patterns) deferred
        to post-MVP.
        """
        try:
            endpoint = f"repos/{owner}/{repo}/branches"
            params = {"per_page": 100}
            branches_data = await self._call_github_api(endpoint, params)
            if not branches_data:
                return []

            branches = []
            for b in branches_data:
                commit = b.get("commit", {}) or {}
                branches.append(
                    {
                        "name": b.get("name", ""),
                        "protected": bool(b.get("protected")),
                        "commit_sha": commit.get("sha", ""),
                    }
                )
            logger.info(f"Retrieved {len(branches)} branches from {owner}/{repo}")
            return branches

        except Exception as e:
            logger.error(f"Error listing branches for {owner}/{repo}: {e}")
            return []

    async def get_repository_info(self, repo: str, owner: str) -> Optional[Dict[str, Any]]:
        """Fetch repository metadata (used to identify default_branch).

        Issue #1040: needed by branch handler to identify which branch is
        the default and surface it first.
        """
        try:
            endpoint = f"repos/{owner}/{repo}"
            data = await self._call_github_api(endpoint)
            if not data:
                return None
            return {
                "name": data.get("name", ""),
                "full_name": data.get("full_name", ""),
                "default_branch": data.get("default_branch", ""),
                "html_url": data.get("html_url"),
            }
        except Exception as e:
            logger.error(f"Error fetching repo info for {owner}/{repo}: {e}")
            return None

    async def get_github_issue_direct(
        self, issue_number: str, repo: str, owner: str
    ) -> Optional[Dict[str, Any]]:
        """Get specific GitHub issue directly via GitHub API.

        Issue #1042: ``repo`` and ``owner`` are now required positional args.
        """
        try:

            async def _operation():
                endpoint = f"repos/{owner}/{repo}/issues/{issue_number}"

                issue_data = await self._call_github_api(endpoint)
                if not issue_data:
                    return None

                # Transform to our format
                issue_info = {
                    "number": issue_data.get("number"),
                    "title": issue_data.get("title"),
                    "description": issue_data.get("body", ""),
                    "state": issue_data.get("state"),
                    "repository": repo,
                    "uri": issue_data.get("html_url"),
                    "mime_type": "text/markdown",
                    "created_at": issue_data.get("created_at"),
                    "updated_at": issue_data.get("updated_at"),
                    "labels": [label["name"] for label in issue_data.get("labels", [])],
                    "assignees": [
                        assignee["login"] for assignee in issue_data.get("assignees", [])
                    ],
                    "milestone": (
                        issue_data.get("milestone", {}).get("title")
                        if issue_data.get("milestone")
                        else None
                    ),
                    "user": issue_data.get("user", {}).get("login"),
                    "retrieved_via": "github_api",
                }

                # Store context for spatial mapping
                await self._store_github_context(issue_info)

                return issue_info

            result = await self.token_counter.wrap_mcp_call(
                "github_get_issue_direct",
                _operation(),
                input_data=f"issue_number={issue_number},repo={repo},owner={owner}",
            )
            logger.info(f"Retrieved GitHub issue #{issue_number} from API")
            return result

        except Exception as e:
            logger.error(f"Error getting GitHub issue {issue_number}: {e}")
            return None

    async def _store_github_context(self, issue_info: Dict[str, Any]) -> None:
        """Store GitHub issue context for spatial mapping"""
        try:
            issue_number = str(issue_info.get("number"))
            if issue_number:
                context = {
                    "repository": issue_info.get("repository"),
                    "labels": issue_info.get("labels", []),
                    "milestone": issue_info.get("milestone"),
                    "priority": (
                        "high"
                        if "urgent" in str(issue_info.get("labels", [])).lower()
                        else "medium"
                    ),
                    "sentiment": "positive" if issue_info.get("state") == "closed" else "neutral",
                    "intent": "monitor",
                    "timestamp": issue_info.get("updated_at"),
                    "user": issue_info.get("user"),
                    "assignees": issue_info.get("assignees", []),
                }

                async with self._lock:
                    self._context_storage[issue_number] = context

        except Exception as e:
            logger.error(f"Error storing GitHub context: {e}")

    async def map_to_position(self, external_id: str, context: Dict[str, Any]) -> SpatialPosition:
        """
        Map GitHub issue number to spatial position.

        Args:
            external_id: GitHub issue number (e.g., "123")
            context: Additional context including repository, labels, etc.

        Returns:
            SpatialPosition with integer position and context
        """
        async with self._lock:
            # Check if mapping already exists
            if external_id in self._mappings:
                return self._mappings[external_id]

            # Create new spatial position
            position = self._create_spatial_position(external_id, context)

            # Store bidirectional mapping
            self._issue_to_position[external_id] = position.position
            self._position_to_issue[position.position] = external_id

            # Store context for response routing
            self._store_context_for_routing(external_id, context)

            # Store mapping in parent class _mappings (no deadlock)
            self._mappings[external_id] = position

            logger.debug(f"Mapped GitHub issue {external_id} to position {position.position}")
            return position

    async def map_from_position(self, position: SpatialPosition) -> Optional[str]:
        """
        Map spatial position back to GitHub issue number.

        Args:
            position: Spatial position to reverse map

        Returns:
            GitHub issue number if mapping exists, None otherwise
        """
        async with self._lock:
            return self._position_to_issue.get(position.position)

    async def store_mapping(self, external_id: str, position: SpatialPosition) -> bool:
        """
        Store mapping between GitHub issue number and spatial position.

        Args:
            external_id: GitHub issue number
            position: Spatial position to map to

        Returns:
            True if mapping stored successfully, False otherwise
        """
        try:
            async with self._lock:
                self._mappings[external_id] = position
                self._issue_to_position[external_id] = position.position
                self._position_to_issue[position.position] = external_id

                logger.debug(
                    f"Stored mapping: GitHub issue {external_id} -> position {position.position}"
                )
                return True

        except Exception as e:
            logger.error(f"Error storing mapping for GitHub issue {external_id}: {e}")
            return False

    async def get_context(self, external_id: str) -> Optional[SpatialContext]:
        """
        Get spatial context for GitHub issue.

        Args:
            external_id: GitHub issue number

        Returns:
            SpatialContext if available, None otherwise
        """
        async with self._lock:
            if external_id in self._context_storage:
                context_data = self._context_storage[external_id]

                return SpatialContext(
                    territory_id=context_data.get("repository", "unknown"),
                    room_id=context_data.get("labels", "general"),
                    path_id=context_data.get("milestone", None),
                    object_position=self._issue_to_position.get(external_id),
                    attention_level=context_data.get("priority", "medium"),
                    emotional_valence=context_data.get("sentiment", "neutral"),
                    navigation_intent=context_data.get("intent", "monitor"),
                    external_system="github",
                    external_id=external_id,
                    external_context=context_data,
                )

            return None

    async def create_spatial_event_from_github(
        self, issue_number: str, event_type: str, context: Dict[str, Any]
    ) -> Any:
        """
        Create spatial event from GitHub issue event.

        Args:
            issue_number: GitHub issue number
            event_type: Type of event (created, updated, closed, etc.)
            context: Event context including changes, user, timestamp

        Returns:
            SpatialEvent representing the GitHub event
        """
        try:
            # Get spatial position for this issue
            position = await self.map_to_position(issue_number, context)

            # Create spatial event (placeholder - would integrate with existing event system)
            event_data = {
                "type": event_type,
                "issue_number": issue_number,
                "position": position.position,
                "context": context,
                "timestamp": context.get("timestamp"),
                "user": context.get("user"),
                "changes": context.get("changes", {}),
            }

            logger.info(f"Created spatial event for GitHub issue {issue_number}: {event_type}")
            return event_data

        except Exception as e:
            logger.error(f"Error creating spatial event for GitHub issue {issue_number}: {e}")
            return None

    async def create_spatial_object_from_github(
        self, issue_number: str, object_type: str, context: Dict[str, Any]
    ) -> Any:
        """
        Create spatial object from GitHub issue.

        Args:
            issue_number: GitHub issue number
            object_type: Type of object (issue, pull_request, etc.)
            context: Object context including metadata

        Returns:
            SpatialObject representing the GitHub object
        """
        try:
            # Get spatial position for this issue
            position = await self.map_to_position(issue_number, context)

            # Create spatial object (placeholder - would integrate with existing object system)
            object_data = {
                "type": object_type,
                "issue_number": issue_number,
                "position": position.position,
                "context": context,
                "repository": context.get("repository"),
                "labels": context.get("labels", []),
                "assignees": context.get("assignees", []),
                "milestone": context.get("milestone"),
                "state": context.get("state", "open"),
            }

            logger.info(f"Created spatial object for GitHub issue {issue_number}: {object_type}")
            return object_data

        except Exception as e:
            logger.error(f"Error creating spatial object for GitHub issue {issue_number}: {e}")
            return None

    async def get_response_context(self, issue_number: str) -> Optional[Dict[str, Any]]:
        """
        Get response context for GitHub issue.

        Args:
            issue_number: GitHub issue number

        Returns:
            Response context if available, None otherwise
        """
        async with self._lock:
            return self._context_storage.get(issue_number, {})

    def _store_context_for_routing(self, external_id: str, context: Dict[str, Any]) -> None:
        """Store context for response routing"""
        self._context_storage[external_id] = context.copy()

    async def get_mapping_stats(self) -> Dict[str, Any]:
        """Get mapping statistics"""
        async with self._lock:
            return {
                "total_mappings": len(self._mappings),
                "github_issues": len(self._issue_to_position),
                "spatial_positions": len(self._position_to_issue),
                "context_entries": len(self._context_storage),
            }

    async def cleanup_old_mappings(self, max_age_hours: int = 24) -> int:
        """
        Clean up old mappings.

        Args:
            max_age_hours: Maximum age in hours for mappings

        Returns:
            Number of mappings cleaned up
        """
        # This would implement cleanup logic based on age
        # For now, return 0 (placeholder)
        logger.debug(f"Cleanup requested for mappings older than {max_age_hours} hours")
        return 0

    async def disconnect(self):
        """Disconnect from MCP service and cleanup GitHub API session"""
        try:
            # Close GitHub API session
            if self._session:
                await self._session.close()
                self._session = None
                logger.info("GitHub API session closed")

            logger.info("GitHub MCP spatial adapter disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting GitHub MCP spatial adapter: {e}")

    async def cleanup(self):
        """Cleanup all resources"""
        try:
            await self.disconnect()

            # Clear mappings and context
            async with self._lock:
                self._issue_to_position.clear()
                self._position_to_issue.clear()
                self._context_storage.clear()

            logger.info("GitHub MCP spatial adapter cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
