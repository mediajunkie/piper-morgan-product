"""
Tests for #1102 PATTERN-073-DATA-SUBSTITUTION fix in
services/intent/intent_service.py:_handle_projects_query.

Previously: returned a hardcoded list of fake projects (Piper Morgan
Platform, Issue Tracker Integration, Documentation Updates) regardless of
which user asked.

Fixed: queries real ProjectRepository.list_active_projects(owner_id) via
PortfolioService, mirroring the canonical PORTFOLIO handler. Falls back to
an honest no-user-id message when user_id is missing rather than asserting
fake data.

Approach: inspect the function source to verify the hardcoded fakes are
gone + the real query path is in place. Full execution tests require DB
fixtures which are outside this slice's scope.
"""

import inspect
from pathlib import Path

import pytest


@pytest.fixture
def intent_service_source() -> str:
    return Path("services/intent/intent_service.py").read_text()


@pytest.fixture
def workflow_entries_source() -> str:
    # #1124: QUERY-category routing moved off _handle_query_intent's elif chain
    # onto the action-dispatch rail. The user_id-threading dispatch site for
    # _handle_projects_query now lives in the rail's entry-point registration.
    return Path("services/intent_service/workflow_entries.py").read_text()


# Hardcoded fakes removed -------------------------------------------------


def test_hardcoded_fake_projects_removed(intent_service_source: str) -> None:
    """The TODO and the three hardcoded fake-project strings must be gone."""
    src = intent_service_source
    # Find _handle_projects_query function block
    start = src.find("async def _handle_projects_query")
    # End at the next async def or class def to keep the block bounded
    end = src.find("async def ", start + 1)
    assert start >= 0 and end > start, "_handle_projects_query function must exist"
    block = src[start:end]

    # The three hardcoded fake-project names must NOT appear inside the
    # function (they can legitimately appear in docstrings/comments
    # referencing the prior state, but not in returned data).
    # Practical check: the literal string "Piper Morgan Platform"
    # cannot appear in the function as a dict value anymore.
    # We allow it in comments/docstrings — but check for the dict pattern.
    assert (
        '"Piper Morgan Platform"' not in block
    ), "Hardcoded fake project name must be removed from returned data"
    assert (
        '"Issue Tracker Integration"' not in block
    ), "Hardcoded fake project name must be removed from returned data"
    assert (
        '"Documentation Updates"' not in block
    ), "Hardcoded fake project name must be removed from returned data"

    # The TODO must be gone
    assert (
        "TODO: Replace hardcoded projects" not in block
    ), "TODO comment must be removed (work is done)"


# Real query path wired in -----------------------------------------------


def test_portfolio_service_imported_in_handler(intent_service_source: str) -> None:
    """The real query path uses PortfolioService.list_active_projects."""
    src = intent_service_source
    start = src.find("async def _handle_projects_query")
    end = src.find("async def ", start + 1)
    block = src[start:end]

    assert "PortfolioService" in block, "Must import or reference PortfolioService"
    assert "list_active_projects" in block, "Must call list_active_projects (the real query path)"
    assert "user_id=user_id" in block, "Must pass user_id to scope the query to the asking user"


def test_handler_accepts_user_id_param(intent_service_source: str) -> None:
    """Signature now accepts user_id."""
    src = intent_service_source
    start = src.find("async def _handle_projects_query")
    end = src.find(") -> IntentProcessingResult", start)
    signature_block = src[start:end]
    assert "user_id" in signature_block, "Signature must accept user_id"


def test_caller_passes_user_id(workflow_entries_source: str) -> None:
    """The dispatch site passes user_id through to _handle_projects_query.

    #1124: routing moved off _handle_query_intent's elif onto the action-dispatch
    rail. The user_id-threading now happens in workflow_entries.py via the
    pass_user_id=True entry-point registration: the factory calls
    ``getattr(intent_service, handler_attr)(intent, workflow_id, user_id)``.
    The #1102 invariant (user_id IS threaded, not dropped) is unchanged — only
    its location moved.
    """
    src = workflow_entries_source
    # The projects-query entry point must be registered with pass_user_id=True so
    # the factory threads user_id (rather than dropping it back to fake data).
    assert '_make_query_dispatch_entry_point("_handle_projects_query", pass_user_id=True)' in src, (
        "projects query entry point must be registered with pass_user_id=True "
        "so user_id is threaded through to _handle_projects_query "
        "(was previously just (intent, workflow_id))"
    )
    # And the pass_user_id branch of the factory must actually append user_id and
    # call the handler with it.
    assert (
        "getattr(intent_service, handler_attr)(*args)" in src and "args.append(user_id)" in src
    ), "the dispatch factory must thread user_id into the handler call " "when pass_user_id is set"


# Safe-fallback paths -----------------------------------------------------


def test_no_user_id_returns_honest_message(intent_service_source: str) -> None:
    """When user_id is None, return an honest 'need to know who you are' rather
    than fake data."""
    src = intent_service_source
    start = src.find("async def _handle_projects_query")
    end = src.find("async def ", start + 1)
    block = src[start:end]
    # Must check for None/falsy user_id
    assert (
        "if not user_id" in block
    ), "Must guard against missing user_id and return honest fallback"
    assert (
        "need to know who you are" in block
    ), "Fallback copy must honestly say the system can't query without user_id"


def test_db_error_returns_structured_fallback(intent_service_source: str) -> None:
    """A DB error during the query returns a structured fallback, not an
    exception trace to the user."""
    src = intent_service_source
    start = src.find("async def _handle_projects_query")
    end = src.find("async def ", start + 1)
    block = src[start:end]
    assert "except Exception" in block, "Must catch DB errors"
    assert (
        "trouble loading your projects" in block
    ), "Fallback must surface a user-friendly message on DB error"


# Documentation discipline ------------------------------------------------


def test_docstring_cites_issue_and_pattern_073(intent_service_source: str) -> None:
    """Per close-issue-properly + Pattern-073 discipline: the WHY is captured
    so a future agent doesn't restore the hardcoded fakes."""
    src = intent_service_source
    start = src.find("async def _handle_projects_query")
    end = src.find("async def ", start + 1)
    block = src[start:end]
    assert "#1102" in block, "Must cite issue number"
    assert "Pattern-073" in block, "Must cite the methodology discipline"


# Pattern-073 instance recording ------------------------------------------


def test_pattern_073_body_records_instance_8():
    """The Pattern-073 catalog body must record this fix as instance 8
    (data-substitution layer — sequential after instance 7 manifest-sync)."""
    body = Path(
        "docs/internal/architecture/patterns/pattern-073-documentation-asserted-behavior-drift.md"
    ).read_text()
    # We're not requiring full instance text, just that the issue number is
    # cited so the fix is traceable.
    assert "#1102" in body, "Pattern-073 body must reference #1102 as an instance/resolution"
