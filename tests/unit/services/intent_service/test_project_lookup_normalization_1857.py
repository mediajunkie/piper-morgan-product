"""#1857: project-name LOOKUP tolerates the article/noun the extractor keeps.

PM live 2026-09-23: 'Add Design-in-Product/one-job to the One Job project' ->
"I couldn't find a project called 'one job project'" (the link-repo extractor
in `canonical_handlers._handle_repo_management` captures "one job project"
verbatim — its `(?:project\\s+)?` only strips a LEADING "project ", not the
trailing noun); 'Add Design-in-Product/one-job to One Job' succeeds. Per the
supersession-gate corollary (CLAUDE.md) and TestExtractionPatternRatchet,
the fix is RESOLVER-side, not a new extraction regex: every project-name
lookup funnels through `ProjectRepository.find_by_name` (PortfolioService.
find_project_by_name is a thin delegate to it — see canonical_handlers.py's
seven call sites), so a single normalization there covers every caller.

`normalize_project_name` / `_resolve_unambiguous_normalized_match` are the
real resolver-side implementation added for #1857 (services/database/
repositories.py) — these tests exercise them directly (the "data seam" is
the in-memory candidate list, standing in for the DB query the real
`find_by_name` runs when its exact-match fast path misses) and, for the
end-to-end wiring, through `ProjectRepository.find_by_name` itself against a
stubbed AsyncSession.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

import pytest

from services.database.models import ProjectDB
from services.database.repositories import (
    ProjectRepository,
    _resolve_unambiguous_normalized_match,
    normalize_project_name,
)

OWNER = "owner-1857"


def _project(name: str, *, id_: Optional[str] = None, is_archived: bool = False) -> ProjectDB:
    """A transient (never session-attached) ProjectDB row — enough for
    find_by_name's normalization path and to_domain(), no DB required."""
    return ProjectDB(
        id=id_ or f"proj-{name.lower().replace(' ', '-')}",
        owner_id=OWNER,
        name=name,
        description=None,
        shared_with=None,
        is_default=False,
        is_archived=is_archived,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        lifecycle_state=None,
        integrations=[],
        repository_links=[],
    )


# =============================================================================
# normalize_project_name — pure function
# =============================================================================


class TestNormalizeProjectName:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("One Job", "one job"),
            ("one job", "one job"),
            ("ONE JOB", "one job"),
            ("the One Job project", "one job"),
            ("The one job project", "one job"),
            ("one job project", "one job"),
            ("my One Job project", "one job"),
            ("my one job repo", "one job"),
            ("One   Job", "one job"),  # whitespace collapse
            ("  One Job  ", "one job"),  # outer whitespace
            # A bare noun with nothing preceding it is never stripped to
            # empty (mirrors clean_project_name's own rule: "archive my
            # project" legitimately captures just "project") — the trailing-
            # noun strip only fires when there's a WORD before it.
            ("the project", "project"),
            ("project", "project"),
        ],
    )
    def test_normalizes(self, raw, expected):
        assert normalize_project_name(raw) == expected

    def test_does_not_strip_mid_string_noun(self):
        # "project" appearing mid-name (not the trailing token) must survive —
        # only a TRAILING " project"/" repo" is stripped.
        assert normalize_project_name("Project Phoenix") == "project phoenix"

    def test_does_not_strip_unrelated_trailing_word(self):
        assert normalize_project_name("One Job Archive") == "one job archive"


# =============================================================================
# _resolve_unambiguous_normalized_match — pure function, ambiguity discipline
# =============================================================================


class TestResolveUnambiguousNormalizedMatch:
    def test_exact_normalized_single_candidate(self):
        candidates = [_project("One Job"), _project("Some Other Thing")]
        matched = _resolve_unambiguous_normalized_match("the One Job project", candidates)
        assert matched is not None
        assert matched.name == "One Job"

    def test_two_similar_names_exact_normalized_wins_unambiguously(self):
        """query 'one job' -> exact-normalized match to 'One Job' only;
        'One Job Archive' normalizes to 'one job archive', not 'one job'."""
        one_job = _project("One Job")
        archive = _project("One Job Archive")
        matched = _resolve_unambiguous_normalized_match("one job", [one_job, archive])
        assert matched is not None
        assert matched.name == "One Job"

    def test_ambiguous_substring_never_silently_picked(self):
        """query 'job' matches neither name's exact-normalized form, and the
        substring/prefix fallback finds BOTH 'One Job' and 'One Job Archive'
        — must return None (the #1694 anti-pattern is guessing here)."""
        one_job = _project("One Job")
        archive = _project("One Job Archive")
        matched = _resolve_unambiguous_normalized_match("job", [one_job, archive])
        assert matched is None

    def test_no_candidates_returns_none(self):
        assert _resolve_unambiguous_normalized_match("the One Job project", []) is None

    def test_empty_normalized_query_returns_none(self):
        # An empty/whitespace-only query must never match everything.
        candidates = [_project("One Job"), _project("Other")]
        assert _resolve_unambiguous_normalized_match("   ", candidates) is None

    def test_unambiguous_prefix_match_used_when_no_exact_normalized_hit(self):
        candidates = [_project("One Job Tracker")]
        matched = _resolve_unambiguous_normalized_match("one job", candidates)
        assert matched is not None
        assert matched.name == "One Job Tracker"


# =============================================================================
# ProjectRepository.find_by_name — the real resolver, DB stubbed at the seam
# =============================================================================


class _FakeScalars:
    def __init__(self, rows: List[ProjectDB]):
        self._rows = list(rows)

    def first(self) -> Optional[ProjectDB]:
        return self._rows[0] if self._rows else None

    def all(self) -> List[ProjectDB]:
        return list(self._rows)


class _FakeResult:
    def __init__(self, rows: List[ProjectDB]):
        self._rows = rows

    def scalars(self) -> _FakeScalars:
        return _FakeScalars(self._rows)


class _FakeSession:
    """Stub at find_by_name's data seam: the real method issues (1) an exact
    case-insensitive-match query, then — ONLY on a miss — (2) a scope-only
    candidates query it resolves in Python via `_resolve_unambiguous_
    normalized_match`. This fake reproduces the SAME scope semantics
    (owner_id / is_archived) the real SQL filters apply, so find_by_name's
    actual control flow and the real normalization code both run; only the
    SQL engine itself is stubbed out.
    """

    def __init__(
        self,
        projects: List[ProjectDB],
        *,
        query_name: str,
        owner_id: Optional[str] = None,
        include_archived: bool = False,
    ):
        self._projects = projects
        self._query_name = query_name
        self._owner_id = owner_id
        self._include_archived = include_archived
        self.call_count = 0

    def _in_scope(self, p: ProjectDB) -> bool:
        if not self._include_archived and p.is_archived:
            return False
        if self._owner_id and p.owner_id != self._owner_id:
            return False
        return True

    async def execute(self, _stmt) -> _FakeResult:
        self.call_count += 1
        scoped = [p for p in self._projects if self._in_scope(p)]
        if self.call_count == 1:
            # exact-match fast path
            rows = [p for p in scoped if p.name.lower() == self._query_name.lower()]
        else:
            # #1857 normalized-fallback candidate fetch (no name filter)
            rows = scoped
        return _FakeResult(rows)


async def _find(projects: List[ProjectDB], query_name: str, **kwargs) -> Optional[object]:
    session = _FakeSession(projects, query_name=query_name, owner_id=OWNER, **kwargs)
    repo = ProjectRepository(session)
    return await repo.find_by_name(name=query_name, owner_id=OWNER)


class TestFindByNameNormalization1857:
    async def test_pm_minimal_pair_resolves_to_same_project(self):
        """PM's verbatim pair: 'the One Job project' and 'One Job' resolve
        to the SAME project (same id)."""
        projects = [_project("One Job", id_="proj-one-job")]

        via_article = await _find(projects, "the One Job project")
        via_bare = await _find(projects, "One Job")

        assert via_article is not None
        assert via_bare is not None
        assert via_article.id == via_bare.id == "proj-one-job"

    async def test_extractor_literal_string_resolves(self):
        """The exact string the live extractor produced ('one job project',
        already-lowercased since it's captured from `message_lower`)."""
        projects = [_project("One Job", id_="proj-one-job")]
        matched = await _find(projects, "one job project")
        assert matched is not None
        assert matched.id == "proj-one-job"

    async def test_case_insensitive(self):
        projects = [_project("One Job", id_="proj-one-job")]
        matched = await _find(projects, "THE ONE JOB PROJECT")
        assert matched is not None
        assert matched.id == "proj-one-job"

    async def test_ambiguity_two_projects_exact_normalized_wins(self):
        """'One Job' and 'One Job Archive' both exist; query 'one job'
        resolves unambiguously to 'One Job' (exact-normalized match)."""
        projects = [
            _project("One Job", id_="proj-one-job"),
            _project("One Job Archive", id_="proj-one-job-archive"),
        ]
        matched = await _find(projects, "one job")
        assert matched is not None
        assert matched.id == "proj-one-job"

    async def test_ambiguity_no_silent_pick(self):
        """Query 'job' is a substring of BOTH names — never silently
        guessed; find_by_name returns None like any other not-found."""
        projects = [
            _project("One Job", id_="proj-one-job"),
            _project("One Job Archive", id_="proj-one-job-archive"),
        ]
        matched = await _find(projects, "job")
        assert matched is None

    async def test_no_project_exists_returns_none(self):
        """The existing not-found path (caller renders "I couldn't find a
        project called '...'") is reached honestly — no project, no match."""
        matched = await _find([_project("Some Other Project")], "the One Job project")
        assert matched is None

    async def test_normalized_fallback_only_queried_on_exact_miss(self):
        """Exact case-insensitive hits never need the second (candidates)
        query — the fast path stays fast."""
        projects = [_project("One Job", id_="proj-one-job")]
        session = _FakeSession(projects, query_name="One Job", owner_id=OWNER)
        repo = ProjectRepository(session)
        matched = await repo.find_by_name(name="One Job", owner_id=OWNER)
        assert matched is not None
        assert session.call_count == 1

    async def test_archived_project_excluded_without_include_archived(self):
        projects = [_project("One Job", id_="proj-one-job", is_archived=True)]
        matched = await _find(projects, "the One Job project")
        assert matched is None

    async def test_archived_project_found_with_include_archived(self):
        projects = [_project("One Job", id_="proj-one-job", is_archived=True)]
        session = _FakeSession(
            projects, query_name="the One Job project", owner_id=OWNER, include_archived=True
        )
        repo = ProjectRepository(session)
        matched = await repo.find_by_name(
            name="the One Job project", owner_id=OWNER, include_archived=True
        )
        assert matched is not None
        assert matched.id == "proj-one-job"
