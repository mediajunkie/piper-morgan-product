"""GitHubOperations — the contract GitHubIntegrationRouter actually dispatches against.

Issue #1723 (PM-ratified 2026-09-06, Exec ruling → Arch). Until this file existed, the
router's ``_get_integration()`` was typed ``-> Any`` and the only Protocol in sight
(``SpatialAdapter``) declared spatial-mapping methods — none of the operations the
router dispatches. The contract in actual use had never been written down, so nothing
could enforce it: a router method written optimistically failed only when someone
finally called it in the wild (#892 ``create_issue``, #1709 ``get_recent_activity``).

Membership rule: a method is in this Protocol iff the router dispatches it through
``_get_integration()`` AND the operation has at least one live caller outside the
router. Dead router methods were deleted in the same change that created this file
(6 of the 15 dispatched names had zero external callers) — a contract should state
what the system needs, not enshrine what an old router accumulated.

Enforcement is the runtime ratchet in ``tests/test_github_operations_protocol.py``
(same idiom as ``MAX_DISPATCH_SITES``): every Protocol member must exist on the MCP
adapter or appear in that test's ``KNOWN_MISSING`` set with a tracking issue. The
set is shrink-only. ``get_integration_status`` is deliberately NOT a member — the
router composes its own status and guards the adapter call with ``hasattr``;
introspection is optional by design, operations are not.

The spatial fallback (``GitHubSpatialIntelligence``) is deliberately NOT a party to
this contract: measured 2026-09-06, it implements zero of the dispatched operations,
so it cannot serve as a fallback for any of them (see #1723 for the measurement).
"""

from typing import Any, Dict, List, Optional, Protocol, Tuple, runtime_checkable


@runtime_checkable
class GitHubOperations(Protocol):
    """What an object returned by ``_get_integration()`` owes its callers."""

    # ── Backed today by the MCP adapter ────────────────────────────────

    async def create_issue(
        self,
        owner: str,
        repo_name: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
    ) -> Dict[str, Any]: ...

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
    ) -> Dict[str, Any]: ...

    async def add_comment(
        self, owner: str, repo_name: str, issue_number: int, body: str
    ) -> Dict[str, Any]: ...

    async def get_closed_issues(
        self, project: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]: ...

    # ── Live callers exist; implementation tracked in #1709 / #1723 ────

    async def get_recent_activity(
        self, days: int, repository: Optional[str] = None
    ) -> Dict[str, Any]: ...

    async def get_issue_by_url(self, url: str) -> Dict[str, Any]: ...

    # #1723 implementation note: declared sync when this Protocol was written
    # (transcribing the router's then-dispatch, a PyGithub-era fossil); went
    # async when the MCP adapter implemented it — an aiohttp-backed adapter
    # cannot honor a sync signature without blocking the event loop. The full
    # chain (router → domain service → _get_project_metadata) went async in
    # the same change.
    async def list_repositories(self) -> List[Dict[str, Any]]: ...

    def parse_github_url(self, url: str) -> Optional[Tuple[str, str, int]]: ...
