"""#1661 — the file-summary rail's reply site: an aged-only account gets a
reply that NAMES what exists instead of the false "I don't see any uploaded
documents" (the Files page would list the aged document).

Layer (m-43): `run_summarize_document_workflow`'s composed reply text, with
`FileResolver` mocked at the boundary (the same `_boundary_patches` idiom
`test_summarize_document_rail_1624.py` uses) — this file is about the RAIL'S
reply composition given a resolver verdict, not about `FileResolver`'s own
temporal-window parsing (`test_file_resolver_temporal_window_1661.py` covers
that, against real Postgres).

PM's design decision (relayed by Lead): on an empty temporal window, name
what does exist — bounded, owner-scoped, most-recent-first; when the message
states a distance ("last month", "a year ago"), the window widens to THAT
distance rather than silently staying at 7 days. A true zero-document account
keeps the ORIGINAL honest-empty reply unchanged.

Issue: #1661
"""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.file_context.file_resolver import FileResolver
from services.intent_service.list_remainder import REMAINDER_OFFER_THRESHOLD
from services.intent_service.workflow_entries import (
    _DOCUMENT_NAMING_RENDER_CAP,
    _render_document_naming_reply,
    run_summarize_document_workflow,
)
from services.shared_types import IntentCategory

_USER = "3f7b8a52-1624-4b00-9e00-000000001661"


def _intent(message: str) -> Intent:
    return Intent(
        category=IntentCategory.SYNTHESIS,
        action="summarize_document",
        original_message=message,
        confidence=0.9,
        context={"original_message": message},
    )


@asynccontextmanager
async def _fake_scope():
    yield MagicMock()


def _doc(filename, file_id=None):
    f = MagicMock()
    f.id = file_id or filename
    f.filename = filename
    return f


def _patches(account_documents=None, is_temporal=None):
    """Mocked FileResolver boundary: resolution always misses (the temporal
    query came back empty — the shape this issue is about); the account-wide
    fallback list is what's under test.

    ``is_temporal`` lets a single case override the REAL classifier (used
    once, to prove the fallback branch is gated on it and not just on an
    empty resolution)."""
    resolver_cls = MagicMock()
    resolver_cls.return_value.resolve_file_reference = AsyncMock(return_value=(None, 0.0))
    resolver_cls.return_value.list_owner_documents = AsyncMock(return_value=account_documents or [])
    resolver_cls.is_temporal_reference = (
        (lambda msg: is_temporal) if is_temporal is not None else FileResolver.is_temporal_reference
    )
    resolver_cls.temporal_window_days = FileResolver.temporal_window_days
    return (
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            _fake_scope,
        ),
        patch("services.repositories.file_repository.FileRepository", MagicMock()),
        patch("services.file_context.file_resolver.FileResolver", resolver_cls),
        resolver_cls,
    )


class TestNamingReplyRendering:
    """`_render_document_naming_reply` in isolation — no rail, no mocks."""

    def test_small_set_renders_whole_list_no_count_line(self):
        docs = [_doc("a.md"), _doc("b.pdf")]
        assert len(docs) <= REMAINDER_OFFER_THRESHOLD
        text = _render_document_naming_reply(docs)
        assert "a.md" in text and "b.pdf" in text
        assert "That's" not in text

    def test_set_at_or_under_render_cap_shows_all_no_count_line(self):
        # Between the PPM ceremony threshold and the render cap: everything
        # requested gets shown, so there is nothing to count honestly against.
        count = REMAINDER_OFFER_THRESHOLD + 2
        assert (
            count <= _DOCUMENT_NAMING_RENDER_CAP
        ), "test assumption: cap comfortably above threshold"
        docs = [_doc(f"doc{i}.md") for i in range(count)]
        text = _render_document_naming_reply(docs)
        for d in docs:
            assert d.filename in text
        assert "That's" not in text

    def test_large_set_bounds_and_states_honest_count(self):
        docs = [_doc(f"doc{i}.md") for i in range(15)]
        text = _render_document_naming_reply(docs)
        shown = [d for d in docs[:_DOCUMENT_NAMING_RENDER_CAP]]
        for d in shown:
            assert d.filename in text
        for d in docs[_DOCUMENT_NAMING_RENDER_CAP:]:
            assert d.filename not in text
        assert f"That's {_DOCUMENT_NAMING_RENDER_CAP} of 15" in text
        # Never an uncashable "and N more" promise — no arm/session at this
        # call site (#1661 design constraint, stated in the docstring).
        assert "more" not in text.lower()
        assert "say the word" not in text.lower()


class TestRailNamingFallback:
    @pytest.mark.asyncio
    async def test_temporal_empty_with_aged_account_names_documents(self):
        """The core defect: 'summarize the file' (bare, temporal-shaped) with
        only an aged document in the account must NOT say the false flat
        empty — it names what exists."""
        p1, p2, p3, resolver_cls = _patches(account_documents=[_doc("survivor.md")])
        with p1, p2, p3:
            result = await run_summarize_document_workflow(
                session_id="sess-1661",
                user_id=_USER,
                context={"intent": _intent("summarize the file")},
            )
        assert result.success is True
        assert "survivor.md" in result.message
        assert "I don't see any uploaded documents" not in result.message
        assert result.intent_data["context"]["reason"] == "no_documents_in_window"

    @pytest.mark.asyncio
    async def test_stated_distance_still_names_when_resolution_misses(self):
        """'the file I uploaded last month' — even though FileResolver
        widens to 30 days internally, THIS test's resolver mock still misses
        (a genuinely-outside-30-days case); the naming fallback still fires
        because the message is temporal-shaped and the account has docs."""
        p1, p2, p3, resolver_cls = _patches(account_documents=[_doc("ancient.pdf")])
        with p1, p2, p3:
            result = await run_summarize_document_workflow(
                session_id="sess-1661",
                user_id=_USER,
                context={"intent": _intent("summarize the file I uploaded last month")},
            )
        assert "ancient.pdf" in result.message
        assert result.intent_data["context"]["reason"] == "no_documents_in_window"

    @pytest.mark.asyncio
    async def test_truly_empty_account_keeps_the_original_honest_empty(self):
        """Zero documents anywhere — the ORIGINAL honest-empty reply is
        unchanged. That one was already true."""
        p1, p2, p3, resolver_cls = _patches(account_documents=[])
        with p1, p2, p3:
            result = await run_summarize_document_workflow(
                session_id="sess-1661",
                user_id=_USER,
                context={"intent": _intent("summarize the file")},
            )
        assert "I don't see any uploaded documents" in result.message
        assert result.intent_data["context"]["reason"] == "no_uploaded_documents"

    @pytest.mark.asyncio
    async def test_non_temporal_miss_keeps_the_original_honest_empty(self):
        """A non-temporal-shaped ask that resolves to nothing must NOT
        trigger the naming fallback — that branch is gated on
        `is_temporal_reference`, never on 'file_id is None' alone (matches
        #1624's existing 'summarize the document' honest-empty pin)."""
        p1, p2, p3, resolver_cls = _patches(
            account_documents=[_doc("would-have-shown.md")], is_temporal=False
        )
        with p1, p2, p3:
            result = await run_summarize_document_workflow(
                session_id="sess-1661",
                user_id=_USER,
                context={"intent": _intent("summarize the document")},
            )
        assert "I don't see any uploaded documents" in result.message
        assert "would-have-shown.md" not in result.message
        assert result.intent_data["context"]["reason"] == "no_uploaded_documents"

    @pytest.mark.asyncio
    async def test_resolved_document_fast_path_unaffected(self):
        """A resolvable file never reaches the naming-fallback code at all —
        `list_owner_documents` must not even be called."""
        p1, p2, p3, resolver_cls = _patches()
        resolver_cls.return_value.resolve_file_reference = AsyncMock(
            return_value=("file-fresh", 0.95)
        )
        with (
            p1,
            p2,
            p3,
            patch(
                "services.intent_service.document_handlers.handle_summarize_document",
                AsyncMock(
                    return_value={
                        "file_id": "file-fresh",
                        "filename": "fresh.md",
                        "summary": "A short summary",
                        "format": "bullet",
                    }
                ),
            ),
        ):
            result = await run_summarize_document_workflow(
                session_id="sess-1661",
                user_id=_USER,
                context={"intent": _intent("summarize the file")},
            )
        assert "Here's my summary of fresh.md" in result.message
        resolver_cls.return_value.list_owner_documents.assert_not_awaited()
