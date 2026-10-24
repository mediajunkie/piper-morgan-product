"""#2151 (CXO 10-23 17:55, line 5): a named file outside the 20 most recent uploads.

FileResolver's candidates are the 20 most recent uploads (plus artifacts). A filename
the message named that wasn't among them returned (None, 0.0), and summarize said "I
don't see any uploaded documents I can summarize", which is false for a user who has
the file. The name is now looked up across all of the owner's uploads (exact name,
owner-scoped) before the resolver gives up, and a name found nowhere is said by name.
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import Intent, UploadedFile
from services.file_context.exceptions import AmbiguousFileReferenceError
from services.file_context.file_resolver import FileResolver
from services.shared_types import IntentCategory

OWNER = "owner-2151"


def _upload(name, file_id, age_days=0):
    return UploadedFile(
        id=file_id,
        owner_id=OWNER,
        filename=name,
        file_type="text/plain",
        upload_time=datetime.now() - timedelta(days=age_days),
    )


def _intent(message):
    return Intent(
        category=IntentCategory.SYNTHESIS,
        action="summarize_document",
        original_message=message,
        context={"original_message": message},
    )


def _resolver(recent, everything):
    repo = MagicMock()
    repo.get_files_for_session = AsyncMock(return_value=recent)
    repo.search_files_by_name = AsyncMock(
        side_effect=lambda owner, q: [
            f for f in everything if f.owner_id == owner and q.lower() in f.filename.lower()
        ]
    )
    return FileResolver(repo), repo


@pytest.mark.asyncio
async def test_a_named_file_past_the_twenty_most_recent_is_found():
    recent = [_upload(f"recent-{i}.txt", f"r{i}") for i in range(20)]
    old = _upload("launch-notes-2131.txt", "old-1", age_days=90)
    resolver, repo = _resolver(recent, recent + [old])
    file_id, conf = await resolver.resolve_file_reference(
        _intent("summarize launch-notes-2131.txt"), OWNER
    )
    assert (file_id, conf) == ("old-1", 0.98)
    repo.search_files_by_name.assert_awaited_with(OWNER, "launch-notes-2131.txt")


@pytest.mark.asyncio
async def test_the_lookup_is_exact_not_a_substring_match():
    recent = [_upload("a.txt", "a")]
    near_miss = _upload("old-notes.txt", "x")  # contains "notes.txt" but isn't it
    resolver, _ = _resolver(recent, recent + [near_miss])
    assert await resolver.resolve_file_reference(_intent("summarize notes.txt"), OWNER) == (
        None,
        0.0,
    )


@pytest.mark.asyncio
async def test_two_files_with_the_named_name_past_the_cap_ask_which():
    recent = [_upload("a.txt", "a")]
    twins = [_upload("notes.txt", "n1", 40), _upload("notes.txt", "n2", 80)]
    resolver, _ = _resolver(recent, recent + twins)
    with pytest.raises(AmbiguousFileReferenceError):
        await resolver.resolve_file_reference(_intent("summarize notes.txt"), OWNER)


@pytest.mark.asyncio
async def test_a_named_file_is_found_even_with_no_recent_candidates():
    old = _upload("plan.md", "p1", age_days=200)
    resolver, _ = _resolver([], [old])
    assert await resolver.resolve_file_reference(_intent("summarize plan.md"), OWNER) == (
        "p1",
        0.98,
    )


@pytest.mark.asyncio
async def test_exact_name_matches_reaches_past_the_cap_too():
    recent = [_upload(f"recent-{i}.txt", f"r{i}") for i in range(20)]
    old = _upload("launch-notes-2131.txt", "old-1", age_days=90)
    resolver, _ = _resolver(recent, recent + [old])
    matches = await resolver.exact_name_matches(
        _intent("what does launch-notes-2131.txt say?"), OWNER
    )
    assert [m.id for m in matches] == ["old-1"]
