"""
Portfolio Service - Manage user project portfolios.

Part of #569 MUX-INTERACT-PORTFOLIO-DEL.

This module provides:
- PortfolioService: CRUD operations for user projects
- Archive/restore functionality (soft delete)
- Permanent delete with explicit confirmation
- Project listing (active and archived)

Design Decision: Archive is the default removal action.
Permanent delete requires explicit confirmation.
"""

import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

import structlog

from services.database.repositories import ProjectRepository
from services.domain.models import Project

logger = structlog.get_logger()


# =============================================================================
# Result Types
# =============================================================================


class PortfolioActionResult(str, Enum):
    """Result of a portfolio action."""

    SUCCESS = "success"
    NOT_FOUND = "not_found"
    NOT_OWNER = "not_owner"
    ALREADY_ARCHIVED = "already_archived"
    NOT_ARCHIVED = "not_archived"
    CONFIRMATION_REQUIRED = "confirmation_required"


@dataclass
class PortfolioResult:
    """
    Result of a portfolio operation.

    Includes status, optional project, and message for UI.
    """

    status: PortfolioActionResult
    project: Optional[Project] = None
    message: str = ""

    @property
    def success(self) -> bool:
        """Check if operation succeeded."""
        return self.status == PortfolioActionResult.SUCCESS


# =============================================================================
# Portfolio Service
# =============================================================================


class PortfolioService:
    """
    Service for managing user project portfolios.

    Provides archive/restore/delete operations with proper
    authorization and confirmation flows.

    Example:
        service = PortfolioService(project_repository)

        # Archive a project (soft delete, recoverable)
        result = await service.archive_project(project_id, user_id)

        # Restore an archived project
        result = await service.restore_project(project_id, user_id)

        # Permanently delete (requires confirmation)
        result = await service.delete_project(
            project_id, user_id, confirmed=True
        )
    """

    def __init__(self, project_repository: ProjectRepository):
        """
        Initialize the portfolio service.

        Args:
            project_repository: Repository for project operations
        """
        self.project_repository = project_repository

    # =========================================================================
    # Read Operations
    # =========================================================================

    async def get_project(
        self,
        project_id: str,
        user_id: str,
    ) -> Optional[Project]:
        """
        Get a project by ID if user is owner.

        Args:
            project_id: Project to retrieve
            user_id: User requesting access

        Returns:
            Project if found and owned by user, None otherwise
        """
        project = await self.project_repository.get_by_id(project_id)
        if project and project.owner_id == user_id:
            return project
        return None

    async def list_active_projects(
        self,
        user_id: str,
    ) -> List[Project]:
        """
        List all active (non-archived) projects for a user.

        Args:
            user_id: User whose projects to list

        Returns:
            List of active projects
        """
        return await self.project_repository.list_active_projects(owner_id=user_id)

    async def list_archived_projects(
        self,
        user_id: str,
    ) -> List[Project]:
        """
        List all archived projects for a user.

        Args:
            user_id: User whose archived projects to list

        Returns:
            List of archived projects
        """
        # #1431: dedicated repository method — the previous implementation
        # filtered an active-only source, so this always returned [].
        return await self.project_repository.list_archived_projects(owner_id=user_id)

    async def find_project_by_name(
        self,
        name: str,
        user_id: str,
        include_archived: bool = False,
    ) -> Optional[Project]:
        """
        Find a project by name (case-insensitive).

        Args:
            name: Project name to search for
            user_id: User whose projects to search
            include_archived: Whether to include archived projects

        Returns:
            Matching project or None
        """
        # #1470: include_archived is threaded into the repository QUERY. It
        # used to be only a post-filter here, over a result set the repo had
        # already hard-filtered to is_archived == False — so archived projects
        # were unreachable by name and restore-by-name always failed.
        return await self.project_repository.find_by_name(
            name=name,
            owner_id=user_id,
            include_archived=include_archived,
        )

    async def search_projects(
        self,
        query: str,
        user_id: str,
        include_archived: bool = False,
        limit: int = 10,
    ) -> List[Project]:
        """
        Search projects by name (partial match).

        Part of #567 MUX-INTERACT-CONV-SEARCH.

        Supports typeahead-style search where results update as user types.
        Returns projects matching the query as a substring of the name.

        Args:
            query: Search query (partial name match)
            user_id: User whose projects to search
            include_archived: Whether to include archived projects
            limit: Maximum results to return

        Returns:
            List of matching projects, ordered by name
        """
        if not query or not query.strip():
            # Empty query - return all active projects
            projects = await self.list_active_projects(user_id)
            return projects[:limit]

        return await self.project_repository.search_projects(
            query=query.strip(),
            owner_id=user_id,
            include_archived=include_archived,
            limit=limit,
        )

    # =========================================================================
    # Archive Operations (Soft Delete)
    # =========================================================================

    async def archive_project(
        self,
        project_id: str,
        user_id: str,
    ) -> PortfolioResult:
        """
        Archive a project (soft delete).

        Archived projects are hidden from active list but can be restored.

        Args:
            project_id: Project to archive
            user_id: User performing the action

        Returns:
            PortfolioResult with status and message
        """
        project = await self.project_repository.get_by_id(project_id)

        if not project:
            return PortfolioResult(
                status=PortfolioActionResult.NOT_FOUND,
                message="I couldn't find that project.",
            )

        if project.owner_id != user_id:
            return PortfolioResult(
                status=PortfolioActionResult.NOT_OWNER,
                message="You can only archive your own projects.",
            )

        if project.is_archived:
            return PortfolioResult(
                status=PortfolioActionResult.ALREADY_ARCHIVED,
                project=project,
                message=f"{project.name} is already archived.",
            )

        # Perform archive
        await self.project_repository.update(
            project_id,
            is_archived=True,
            updated_at=datetime.now(),
        )

        # Refresh project
        updated_project = await self.project_repository.get_by_id(project_id)

        logger.info(
            "project_archived",
            project_id=project_id,
            project_name=project.name,
            user_id=user_id,
        )

        return PortfolioResult(
            status=PortfolioActionResult.SUCCESS,
            project=updated_project,
            message=f"I've archived {project.name}. You can restore it anytime.",
        )

    async def restore_project(
        self,
        project_id: str,
        user_id: str,
    ) -> PortfolioResult:
        """
        Restore an archived project.

        Args:
            project_id: Project to restore
            user_id: User performing the action

        Returns:
            PortfolioResult with status and message
        """
        project = await self.project_repository.get_by_id(project_id)

        if not project:
            return PortfolioResult(
                status=PortfolioActionResult.NOT_FOUND,
                message="I couldn't find that project.",
            )

        if project.owner_id != user_id:
            return PortfolioResult(
                status=PortfolioActionResult.NOT_OWNER,
                message="You can only restore your own projects.",
            )

        if not project.is_archived:
            return PortfolioResult(
                status=PortfolioActionResult.NOT_ARCHIVED,
                project=project,
                message=f"{project.name} isn't archived.",
            )

        # Perform restore
        await self.project_repository.update(
            project_id,
            is_archived=False,
            updated_at=datetime.now(),
        )

        # Refresh project
        updated_project = await self.project_repository.get_by_id(project_id)

        logger.info(
            "project_restored",
            project_id=project_id,
            project_name=project.name,
            user_id=user_id,
        )

        return PortfolioResult(
            status=PortfolioActionResult.SUCCESS,
            project=updated_project,
            message=f"Welcome back, {project.name}! I've restored it to your portfolio.",
        )

    # =========================================================================
    # Delete Operations (Hard Delete)
    # =========================================================================

    async def delete_project(
        self,
        project_id: str,
        user_id: str,
        confirmed: bool = False,
    ) -> PortfolioResult:
        """
        Permanently delete a project.

        Requires explicit confirmation. Without confirmation,
        returns CONFIRMATION_REQUIRED status.

        Args:
            project_id: Project to delete
            user_id: User performing the action
            confirmed: Whether user has confirmed deletion

        Returns:
            PortfolioResult with status and message
        """
        project = await self.project_repository.get_by_id(project_id)

        if not project:
            return PortfolioResult(
                status=PortfolioActionResult.NOT_FOUND,
                message="I couldn't find that project.",
            )

        if project.owner_id != user_id:
            return PortfolioResult(
                status=PortfolioActionResult.NOT_OWNER,
                message="You can only delete your own projects.",
            )

        # Require confirmation for permanent delete
        if not confirmed:
            return PortfolioResult(
                status=PortfolioActionResult.CONFIRMATION_REQUIRED,
                project=project,
                message=(
                    f"Are you sure you want to permanently delete {project.name}? "
                    f"This cannot be undone. Say 'yes, delete it' to confirm, "
                    f"or 'archive instead' to keep it recoverable."
                ),
            )

        # Store name before deletion
        project_name = project.name

        # Perform hard delete
        await self.project_repository.delete(project_id)

        logger.info(
            "project_deleted",
            project_id=project_id,
            project_name=project_name,
            user_id=user_id,
        )

        return PortfolioResult(
            status=PortfolioActionResult.SUCCESS,
            message=f"I've permanently deleted {project_name}.",
        )

    # NOTE (#1431): the former _get_all_user_projects helper lived here. It
    # claimed to return "active and archived" but only ever returned active
    # (the repo query filters is_archived == False), which made the archived
    # list mathematically empty. Removed when list_archived_projects gained a
    # dedicated repository method; zero other callers existed.


# =============================================================================
# Conversation Patterns for Delete/Archive
# =============================================================================


# Patterns for detecting archive intent
ARCHIVE_PATTERNS = [
    r"\barchive\s+(?:my\s+)?(?:project\s+)?(.+)",
    r"\bhide\s+(?:my\s+)?(?:project\s+)?(.+)",
    r"\bput\s+(.+)\s+(?:away|aside)",
]

# Patterns for detecting delete intent
DELETE_PATTERNS = [
    r"\bdelete\s+(?:my\s+)?(?:project\s+)?(.+)",
    r"\bremove\s+(?:my\s+)?(?:project\s+)?(.+)",
    r"\bget rid of\s+(.+)",
]

# Patterns for detecting permanent delete intent
PERMANENT_DELETE_PATTERNS = [
    r"\bpermanently\s+delete\b",
    r"\bdelete\s+(?:it\s+)?forever\b",
    r"\byes,?\s+delete\s+it\b",
    r"\bconfirm\s+delete\b",
]

# Patterns for detecting restore intent
RESTORE_PATTERNS = [
    r"\brestore\s+(?:my\s+)?(?:project\s+)?(.+)",
    r"\bunarchive\s+(.+)",
    r"\bbring\s+back\s+(.+)",
]

# Patterns for archive-instead response
ARCHIVE_INSTEAD_PATTERNS = [
    r"\barchive\s+instead\b",
    r"\bjust\s+archive\b",
    r"\bkeep\s+it\s+recoverable\b",
]


# Trailing politeness/filler words to strip from captured project names.
# Fixes "delete X please" capturing "X please".
_TRAILING_WORDS = [
    "please",
    "now",
    "thanks",
    "thank you",
    "asap",
    "for me",
    "right now",
    "immediately",
    "today",
]

# Matching quote pairs to unwrap from captured names (straight + curly).
_QUOTE_PAIRS = [
    ('"', '"'),
    ("'", "'"),
    ("“", "”"),  # “ ”
    ("‘", "’"),  # ‘ ’
]


def clean_project_name(name: Optional[str]) -> Optional[str]:
    """
    Normalize a project name captured by the ARCHIVE/DELETE/RESTORE patterns.

    Hoisted from the nested helper in canonical_handlers._handle_portfolio_query
    so it is testable and shared (Issue #1492: 'Archive my Test project,
    please.' / 'called "Test"' / '"Test"' all failed; only the bare form
    worked). Handles, iteratively until stable:

    - trailing sentence punctuation ("Test." → "Test")
    - trailing politeness/filler words ("Test please" → "Test")
    - a leading 'called'/'named' ("called Test" → "Test")
    - wrapping quotes, straight or curly ('"Test"' → "Test")

    and finally the adjective-position noun ("Test project" → "Test", from
    "Archive my Test project" where the pattern can't consume "project").
    """
    if not name:
        return name
    cleaned = name.strip()
    prev = None
    while cleaned and cleaned != prev:
        prev = cleaned
        # Trailing sentence punctuation ("test project, please." → "... please")
        cleaned = cleaned.rstrip(".,!?;:").strip()
        # Politeness/filler tails ("X please" → "X")
        for word in _TRAILING_WORDS:
            if cleaned.lower().endswith(f" {word}"):
                cleaned = cleaned[: -(len(word) + 1)].strip()
        # Leading 'called'/'named' ("called \"Test\"" → "\"Test\"")
        cleaned = re.sub(r"^(?:called|named)\s+", "", cleaned, flags=re.IGNORECASE)
        # Unwrap matching quotes ("\"Test\"" → "Test")
        for open_q, close_q in _QUOTE_PAIRS:
            if len(cleaned) >= 2 and cleaned.startswith(open_q) and cleaned.endswith(close_q):
                cleaned = cleaned[1:-1].strip()
                break
    # Adjective position: "Archive my Test project" captures "test project"
    # (the pattern's optional "project " prefix can't consume a trailing
    # noun). Strip it, but never down to an empty name ("archive my project"
    # legitimately captures just "project").
    stripped = re.sub(r"\s+projects?$", "", cleaned, flags=re.IGNORECASE)
    if stripped:
        cleaned = stripped
    return cleaned
