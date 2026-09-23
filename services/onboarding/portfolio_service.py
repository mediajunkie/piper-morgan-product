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

        #1857: the underlying repository also tolerates a leading article
        ("the "/"my ") and a trailing "project"/"repo" noun, and collapses
        whitespace, on BOTH the query and the candidate names — see
        `ProjectRepository.find_by_name` / `normalize_project_name`.

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
            # Keyword form so the #1532/#1501 principal-threading AST guard
            # can see the principal (it recognizes user_id/owner_id kwargs).
            projects = await self.list_active_projects(user_id=user_id)
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

# Patterns for detecting an ADD/CREATE intent that CARRIES its arguments
# (#1856). Siblings of the ARCHIVE/DELETE/RESTORE families above and used the
# same way: the already-claiming handler matches them to fill its own slots.
# NOT a routing pattern — the pre-classifier's PORTFOLIO family already claims
# every shape here; it just hands the handler nothing but original_message.
#
# ⚠️ These are matched against the ORIGINAL message, never message_lower. The
# siblings above can lower-case their captures because a name is only ever
# used for a case-insensitive lookup; an ADD capture BECOMES the stored
# project name, so "One Job" must not be persisted as "one job".
ADD_PROJECT_PATTERNS = [
    r"\b(?:add|create|start|set\s+up)\s+(?:a\s+|an\s+|the\s+|my\s+)?(?:new\s+)?"
    r"projects?\s+(?:called\s+|named\s+)?(.+)",
]

# The trailing "... with repo owner/name" clause, split off before the name is
# captured so it never lands inside the name. Accepts the phrasings the app
# itself suggests plus the near neighbours.
_ADD_REPO_CLAUSE_RE = re.compile(
    r"[,;]?\s*\b(?:with|for|using|linked\s+to|and\s+link(?:ed)?\s+to)\s+"
    r"(?:the\s+|a\s+)?(?:git\s*hub\s+)?(?:repo(?:sitory)?|github)\s+"
    r"(?P<repo>[\w.-]+/[\w.-]+)\s*\.?\s*$",
    re.IGNORECASE,
)

_ADD_NAME_RES = [re.compile(p, re.IGNORECASE) for p in ADD_PROJECT_PATTERNS]

# Tokens that make a reply a correction/refusal/question rather than a name.
# Word-boundary matched, never substring: the #1837 lesson ("no" inside
# "nothing"/"know") applies verbatim here.
_NOT_A_NAME_WORDS = frozenset(
    {
        "no",
        "not",
        "nope",
        "cancel",
        "nevermind",
        "stop",
        "wrong",
        "isn",  # isn't, after the apostrophe split
        "doesn",
        "didn",
        "circles",
    }
)

# A name the user could plausibly have typed. Deliberately generous on the
# upper bound (#1856 names the ~8-word threshold).
_MAX_NAME_WORDS = 8


def extract_add_project_slots(message: Optional[str]) -> dict:
    """Pull the slots an 'add project' utterance already carries (#1856).

    PM live 2026-09-23 sent the app's OWN suggested phrasing —
    ``add project One Job with repo Design-in-Product/one-job`` — and the flow
    answered "What would you like to call it?", discarding both arguments.

    Returns ``{"name": str | None, "repo": str | None}``. A ``name`` of None
    means the utterance asked to add a project without saying which, and the
    caller must ask — once, imperatively (see #1856 defect 2).

    Shapes covered (the four named on the issue, plus their polite/quoted
    variants):

        add project One Job with repo Design-in-Product/one-job
        add project One Job
        add a project called One Job
        create project One Job for repo Design-in-Product/one-job
    """
    if not message:
        return {"name": None, "repo": None}

    text = message.strip()
    repo = None

    # 1. Split off the repo clause so it cannot be captured as part of the name.
    repo_match = _ADD_REPO_CLAUSE_RE.search(text)
    if repo_match:
        repo = repo_match.group("repo")
        text = text[: repo_match.start()].strip()

    # 2. Capture the name from what remains.
    name = None
    for pattern in _ADD_NAME_RES:
        match = pattern.search(text)
        if match and match.group(1).strip():
            name = clean_project_name(match.group(1).strip())
            break

    # A capture that normalises away to nothing ("add a new project" →
    # "project" → "") is NOT a name.
    if name is not None and (not name or not is_plausible_project_name(name)):
        name = None

    return {"name": name, "repo": repo}


def is_plausible_project_name(text: Optional[str]) -> bool:
    """Could this text be what the user wants their project CALLED? (#1856)

    False for the shapes that made PM's second turn loop: a correction or
    refusal ("no that is not the name of the new project"), a question, or a
    sentence too long to be a name. Used to choose honest copy — never to
    silently adopt the text as a name.
    """
    if not text:
        return False
    stripped = text.strip()
    if not stripped:
        return False
    if "?" in stripped:
        return False

    words = re.findall(r"[A-Za-z']+", stripped.lower())
    if len(stripped.split()) > _MAX_NAME_WORDS:
        return False
    # Word-boundary matching, not substring (#1837).
    if any(w.strip("'") in _NOT_A_NAME_WORDS for w in words):
        return False
    # A bare "project"/"a project" is the noun, not a name.
    if stripped.lower().strip(" .") in ("project", "a project", "new project", "a new project"):
        return False
    return True


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
