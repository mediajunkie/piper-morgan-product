import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from services.database.models import User
from services.domain.models import Intent, IntentCategory, UploadedFile
from services.file_context.exceptions import AmbiguousFileReferenceError
from services.file_context.file_resolver import FileResolver
from services.repositories.file_repository import FileRepository


async def create_test_user(session, owner_id: str) -> User:
    """
    Create a test user for file resolver tests.
    Required for SEC-RBAC owner_id foreign key constraint.
    """
    user = User(
        id=owner_id,
        username=f"test_user_{owner_id[:8]}",
        email=f"test_{owner_id[:8]}@example.com",
        role="user",
        is_active=True,
        is_verified=True,
        is_alpha=True,
    )
    session.add(user)
    await session.flush()  # Ensure user exists before file creation
    return user


# NOTE: Use db_session_factory for fresh sessions per operation (2025-07-14)
# This prevents asyncpg/SQLAlchemy concurrency errors. See conftest.py for details.

# TODO PM-058: ASYNCPG CONCURRENCY ISSUE
# Tests in this class fail when run in batch due to AsyncPG connection pool contention
# when using async_transaction fixture. The error "cannot perform operation: another
# operation is in progress" occurs when multiple async operations try to use the same
# database connection. Individual tests pass, batch execution fails.
# Current status: 1/5 tests pass in batch (test_no_files_in_session)


class TestFileResolverEdgeCases:
    @pytest.mark.smoke
    async def test_no_files_in_session(self, async_transaction):
        """Test when user references files but none uploaded"""
        async with async_transaction as session:
            resolver = FileResolver(FileRepository(session))
            # Use a valid UUID that will have no files associated with it
            empty_session_id = str(uuid4())
            intent = Intent(
                category=IntentCategory.ANALYSIS,
                action="analyze_document",
                context={"original_message": "analyze the report"},
            )
            file_id, confidence = await resolver.resolve_file_reference(intent, empty_session_id)
            assert file_id is None
            assert confidence == 0.0

    @pytest.mark.smoke
    async def test_very_old_file_scoring(self, async_transaction):
        """Test that very old files score lower than recent ones"""
        owner_id = str(uuid4())
        old_file = UploadedFile(
            owner_id=owner_id,
            filename="old_report.pdf",
            file_type="application/pdf",
            file_size=1000,
            storage_path="/test/old_report.pdf",
            upload_time=datetime.now() - timedelta(days=7),  # 1 week old
        )
        recent_file = UploadedFile(
            owner_id=owner_id,
            filename="recent_report.pdf",
            file_type="application/pdf",
            file_size=1000,
            storage_path="/test/recent_report.pdf",
            upload_time=datetime.now() - timedelta(minutes=5),
        )
        async with async_transaction as session:
            # Create test user first (SEC-RBAC requires owner_id FK)
            await create_test_user(session, owner_id)
            repo = FileRepository(session)
            await repo.save_file_metadata(old_file)
            await repo.save_file_metadata(recent_file)
            resolver = FileResolver(repo)
            intent = Intent(
                category=IntentCategory.ANALYSIS,
                action="analyze_report",
                context={"original_message": "analyze the report"},
            )
            file_id, confidence = await resolver.resolve_file_reference(intent, owner_id)
            assert file_id == recent_file.id
            assert confidence > 0.5

    @pytest.mark.smoke
    async def test_identical_filenames_different_times(self, async_transaction):
        """Test handling multiple files with same name but different upload times.

        Issue #768: With correct timezone handling, files with significantly different
        upload times now have different recency scores. Files 1+ hours apart will
        have score differences > 0.2 (ambiguity threshold), so the most recent
        file should be returned.
        """
        owner_id = str(uuid4())
        files = []
        async with async_transaction as session:
            # Create test user first (SEC-RBAC requires owner_id FK)
            await create_test_user(session, owner_id)
            repo = FileRepository(session)
            for i in range(3):
                file = UploadedFile(
                    owner_id=owner_id,
                    filename="report.pdf",  # Same name
                    file_type="application/pdf",
                    file_size=1000,
                    storage_path=f"/test/report_{i}.pdf",
                    upload_time=datetime.now() - timedelta(hours=i),
                )
                saved = await repo.save_file_metadata(file)
                files.append(saved)
            resolver = FileResolver(repo)
            intent = Intent(
                category=IntentCategory.ANALYSIS,
                action="analyze_report",
                context={"original_message": "analyze the report"},
            )

            # With correct timezone handling (#768), files hours apart have
            # significantly different recency scores (>0.2 difference).
            # The most recent file should be returned, not ambiguity error.
            file_id, confidence = await resolver.resolve_file_reference(intent, owner_id)
            assert file_id == files[0].id  # Most recent file wins
            assert confidence > 0.5  # Should have reasonable confidence

    @pytest.mark.smoke
    async def test_special_characters_in_filename(self, async_transaction):
        """Test files with spaces, unicode, special chars"""
        owner_id = str(uuid4())
        test_files = [
            ("résumé (final).pdf", "application/pdf"),
            ("2024 Q3 Report - Sales & Marketing.pdf", "application/pdf"),
            (
                "データ分析.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ),
            (
                "report[v2](draft)_FINAL.docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        ]
        async with async_transaction as session:
            # Create test user first (SEC-RBAC requires owner_id FK)
            await create_test_user(session, owner_id)
            repo = FileRepository(session)
            base_time = datetime.now()
            for i, (filename, file_type) in enumerate(test_files):
                # Make résumé (first file) most recent, others much older
                upload_time = base_time - timedelta(minutes=i * 20)
                file = UploadedFile(
                    owner_id=owner_id,
                    filename=filename,
                    file_type=file_type,
                    file_size=1000,
                    storage_path=f"/test/{filename}",
                    upload_time=upload_time,
                )
                await repo.save_file_metadata(file)
            resolver = FileResolver(repo)
            intent = Intent(
                category=IntentCategory.ANALYSIS,
                action="analyze_document",
                context={"original_message": "analyze the résumé"},
            )
            # With special characters and similar scores, ambiguity is expected
            # The test verifies Unicode handling works and résumé is top candidate
            from services.file_context.exceptions import AmbiguousFileReferenceError

            try:
                file_id, confidence = await resolver.resolve_file_reference(intent, owner_id)
                # If resolved without ambiguity, should be the résumé file
                assert (
                    "résumé"
                    in [f.filename for f in await repo.get_files(owner_id) if f.id == file_id][0]
                )
            except AmbiguousFileReferenceError as e:
                # Ambiguity is acceptable - verify résumé is the top candidate
                assert "résumé" in e.files[0].filename  # First candidate should be résumé

    @pytest.mark.smoke
    async def test_performance_with_many_files(self, async_transaction):
        """Test resolution performance with many files"""
        import time

        owner_id = str(uuid4())
        async with async_transaction as session:
            # Create test user first (SEC-RBAC requires owner_id FK)
            await create_test_user(session, owner_id)
            repo = FileRepository(session)
            for i in range(100):
                file = UploadedFile(
                    owner_id=owner_id,
                    filename=f"document_{i}.pdf",
                    file_type="application/pdf",
                    file_size=1000,
                    storage_path=f"/test/document_{i}.pdf",
                    upload_time=datetime.now() - timedelta(minutes=i),
                )
                await repo.save_file_metadata(file)
            resolver = FileResolver(repo)
            intent = Intent(
                category=IntentCategory.ANALYSIS,
                action="analyze_document",
                context={"original_message": "analyze document_50"},
            )
            start_time = time.time()
            try:
                file_id, confidence = await resolver.resolve_file_reference(intent, owner_id)
                elapsed = (time.time() - start_time) * 1000  # Convert to ms
                assert elapsed < 100, f"Resolution took {elapsed:.2f}ms, should be <100ms"
                assert file_id is not None
            except AmbiguousFileReferenceError:
                # Ambiguity is acceptable - still verify performance
                elapsed = (time.time() - start_time) * 1000  # Convert to ms
                assert elapsed < 100, f"Resolution took {elapsed:.2f}ms, should be <100ms"
