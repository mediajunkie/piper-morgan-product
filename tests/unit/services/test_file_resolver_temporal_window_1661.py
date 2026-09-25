"""#1661 — temporal file references cap at a 7-day window: aged documents get
a false honest-empty reply ("I don't see any uploaded documents") even though
the Files page lists them.

Two pieces pinned here, at the `FileResolver` layer (real Postgres,
`async_transaction` — the same house pattern `test_file_resolver_edge_cases.py`
uses, rolled back per test):

1. `temporal_window_days` / `is_temporal_reference` — the parser: a STATED
   distance ("last month", "a year ago", "3 weeks ago") widens the window to
   THAT distance; with none stated, the default 7 days is unchanged; a
   distance narrower than the account's aged document (e.g. "yesterday")
   must NOT accidentally resolve to it.
2. `resolve_file_reference` end-to-end with the widened window actually
   finding an aged file, and `list_owner_documents` — the account-wide,
   NOT-time-bound fallback set the rail reply site uses to name what exists
   when the temporal window comes back empty.

Layer (m-43): FileResolver + FileRepository against real Postgres. Not the
rail's composed reply text — that's `test_summarize_document_naming_1661.py`.

Issue: #1661
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from services.database.models import User
from services.domain.models import Intent, IntentCategory, UploadedFile
from services.file_context.file_resolver import FileResolver
from services.repositories.file_repository import FileRepository


async def _create_test_user(session, owner_id: str) -> User:
    user = User(
        id=owner_id,
        username=f"t1661_{owner_id[:8]}",
        email=f"t1661_{owner_id[:8]}@example.com",
        role="user",
        is_active=True,
        is_verified=True,
        is_alpha=True,
    )
    session.add(user)
    await session.flush()
    return user


def _aged_file(owner_id: str, days_old: float, filename: str = "survivor.md") -> UploadedFile:
    return UploadedFile(
        owner_id=owner_id,
        filename=filename,
        file_type="text/markdown",
        file_size=42,
        storage_path=f"/test/{filename}",
        # A margin under the exact boundary — the cutoff is computed at QUERY
        # time, which is always slightly after insertion, so an exact N-day
        # delta at insert time reads as (N + epsilon) days old by query time.
        upload_time=datetime.now(timezone.utc) - timedelta(days=days_old, hours=-1),
    )


class TestTemporalWindowParsing:
    """Pure parsing — no DB needed, but grouped here for locality with the
    resolver-level behavior it feeds."""

    def test_default_window_is_seven_days_when_no_distance_stated(self):
        assert FileResolver.temporal_window_days("summarize the file") == 7
        assert FileResolver.temporal_window_days("summarize that file") == 7

    def test_last_month_widens_to_thirty_days(self):
        assert FileResolver.temporal_window_days("the file I uploaded last month") == 30

    def test_a_year_ago_widens_to_365_days(self):
        assert FileResolver.temporal_window_days("the file I uploaded a year ago") == 365

    def test_yesterday_narrows_to_one_day(self):
        assert FileResolver.temporal_window_days("the file I uploaded yesterday") == 1

    def test_numeric_distance_parses(self):
        assert FileResolver.temporal_window_days("the file from 3 weeks ago") == 21
        assert FileResolver.temporal_window_days("the file from 2 months ago") == 60

    def test_is_temporal_reference_true_for_bare_the_file(self):
        assert FileResolver.is_temporal_reference("summarize the file") is True
        assert FileResolver.is_temporal_reference("summarize that file") is True
        assert FileResolver.is_temporal_reference("summarize my file") is True

    def test_is_temporal_reference_false_for_non_temporal_ask(self):
        assert FileResolver.is_temporal_reference("summarize this document") is False


class TestResolveWithWidenedWindow:
    @pytest.mark.smoke
    async def test_bare_the_file_default_window_misses_aged_doc(self, async_transaction):
        """The pre-fix defect at the resolver layer: a bare temporal phrase
        stays on the 7-day default and an aged-only account resolves to
        nothing — this is the honest signal the rail reply site consults to
        decide whether to name what exists."""
        owner_id = str(uuid4())
        async with async_transaction as session:
            await _create_test_user(session, owner_id)
            repo = FileRepository(session)
            await repo.save_file_metadata(_aged_file(owner_id, 30))
            resolver = FileResolver(repo)
            intent = Intent(
                category=IntentCategory.SYNTHESIS,
                action="summarize_document",
                context={"original_message": "summarize the file"},
            )
            file_id, confidence = await resolver.resolve_file_reference(intent, owner_id)
            assert file_id is None
            assert confidence == 0.0

    @pytest.mark.smoke
    async def test_stated_last_month_resolves_the_thirty_day_old_file(self, async_transaction):
        """A stated distance widens the window to THAT distance and the
        aged file resolves — the user's instruction is honored, not ignored."""
        owner_id = str(uuid4())
        async with async_transaction as session:
            await _create_test_user(session, owner_id)
            repo = FileRepository(session)
            saved = await repo.save_file_metadata(_aged_file(owner_id, 30))
            resolver = FileResolver(repo)
            intent = Intent(
                category=IntentCategory.SYNTHESIS,
                action="summarize_document",
                context={"original_message": "summarize the file I uploaded last month"},
            )
            file_id, confidence = await resolver.resolve_file_reference(intent, owner_id)
            assert file_id == saved.id
            assert confidence > 0.5

    @pytest.mark.smoke
    async def test_stated_yesterday_does_not_bind_to_the_aged_file(self, async_transaction):
        """The anti-widening guarantee: 'yesterday' must not silently bind to
        a 30-day-old file just because it's the only candidate. A narrower
        stated distance than the document's actual age stays empty."""
        owner_id = str(uuid4())
        async with async_transaction as session:
            await _create_test_user(session, owner_id)
            repo = FileRepository(session)
            await repo.save_file_metadata(_aged_file(owner_id, 30))
            resolver = FileResolver(repo)
            intent = Intent(
                category=IntentCategory.SYNTHESIS,
                action="summarize_document",
                context={"original_message": "summarize the file I uploaded yesterday"},
            )
            file_id, confidence = await resolver.resolve_file_reference(intent, owner_id)
            assert file_id is None
            assert confidence == 0.0

    @pytest.mark.smoke
    async def test_fresh_doc_fast_path_unchanged(self, async_transaction):
        """A recently-uploaded file with an explicit bare reference still
        resolves at high confidence — the pre-#1661 fast path is untouched."""
        owner_id = str(uuid4())
        async with async_transaction as session:
            await _create_test_user(session, owner_id)
            repo = FileRepository(session)
            fresh = UploadedFile(
                owner_id=owner_id,
                filename="fresh.md",
                file_type="text/markdown",
                file_size=10,
                storage_path="/test/fresh.md",
                upload_time=datetime.now(timezone.utc),
            )
            saved = await repo.save_file_metadata(fresh)
            resolver = FileResolver(repo)
            intent = Intent(
                category=IntentCategory.SYNTHESIS,
                action="summarize_document",
                context={"original_message": "summarize the file"},
            )
            file_id, confidence = await resolver.resolve_file_reference(intent, owner_id)
            assert file_id == saved.id
            assert confidence >= 0.9


class TestListOwnerDocuments:
    @pytest.mark.smoke
    async def test_returns_documents_outside_the_temporal_window(self, async_transaction):
        """The fallback set the rail uses to name what exists — NOT time-bound,
        unlike the temporal query it's a fallback FOR."""
        owner_id = str(uuid4())
        async with async_transaction as session:
            await _create_test_user(session, owner_id)
            repo = FileRepository(session)
            saved = await repo.save_file_metadata(_aged_file(owner_id, 30))
            resolver = FileResolver(repo)
            docs = await resolver.list_owner_documents(owner_id)
            assert [d.id for d in docs] == [saved.id]

    @pytest.mark.smoke
    async def test_empty_account_returns_empty(self, async_transaction):
        """A genuinely empty account — the true honest-empty case, unchanged."""
        owner_id = str(uuid4())
        async with async_transaction as session:
            await _create_test_user(session, owner_id)
            repo = FileRepository(session)
            resolver = FileResolver(repo)
            docs = await resolver.list_owner_documents(owner_id)
            assert docs == []

    @pytest.mark.smoke
    async def test_most_recent_first(self, async_transaction):
        owner_id = str(uuid4())
        async with async_transaction as session:
            await _create_test_user(session, owner_id)
            repo = FileRepository(session)
            older = await repo.save_file_metadata(_aged_file(owner_id, 60, "older.md"))
            newer = await repo.save_file_metadata(_aged_file(owner_id, 10, "newer.md"))
            resolver = FileResolver(repo)
            docs = await resolver.list_owner_documents(owner_id)
            assert [d.id for d in docs] == [newer.id, older.id]
