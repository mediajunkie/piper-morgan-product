"""
Integration Tests for Document Processing (Issue #290 - Tests 19-24)

Tests the complete document analysis workflow:
- Test 19: Analyze uploaded document
- Test 20: Ask question about document
- Test 21: Reference document in conversation
- Test 22: Summarize document
- Test 23: Compare multiple documents
- Test 24: Search across documents

All tests require:
- JWT authentication
- User isolation
- Real file uploads (not mocks)
"""

import asyncio
import io
import uuid
from pathlib import Path
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

from services.auth.password_service import PasswordService
from services.database.connection import db
from services.database.models import UploadedFileDB, User
from web.app import app


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create async HTTP client for testing"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def test_user():
    """
    Create a test user for document processing tests.

    Yields the user_id and password, then cleans up.
    """
    # Reinitialize database for this event loop
    if not db._initialized:
        await db.initialize()

    # Create test user
    test_password = "test_doc_password_123"
    ps = PasswordService()
    hashed = ps.hash_password(test_password)

    test_user = User(
        id=str(uuid.uuid4()),
        username="doc_test_user",
        email="doctest@example.com",
        password_hash=hashed,
        is_active=True,
        is_verified=True,
    )

    # Add to database
    async with await db.get_session() as session:
        session.add(test_user)
        await session.commit()

    user_id = test_user.id
    username = test_user.username

    yield {"user_id": user_id, "username": username, "password": test_password}

    # Cleanup - delete user and their uploaded files
    async with await db.get_session() as session:
        # Delete uploaded files first (foreign key constraint)
        from sqlalchemy import delete, select

        await session.execute(
            delete(UploadedFileDB).where(
                UploadedFileDB.filename.in_(["test_document.pdf", "second_document.pdf"])
            )
        )

        # Delete user
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user_to_delete = result.scalar_one_or_none()

        if user_to_delete:
            await session.delete(user_to_delete)

        await session.commit()


@pytest.fixture
async def auth_token(async_client: AsyncClient, test_user: dict) -> str:
    """
    Get authentication token for tests using the test user.
    """
    response = await async_client.post(
        "/api/v1/auth/login",
        # the login endpoint takes FORM fields, not JSON (contract drift caught 1452)
        data={"username": test_user["username"], "password": test_user["password"]},
    )
    assert response.status_code == 200, f"Login failed: {response.text}"

    data = response.json()
    token = data.get("token")
    assert token, "No access token returned"

    return token


@pytest.fixture
async def uploaded_file_id(async_client: AsyncClient, auth_token: str) -> str:
    """
    Upload a test PDF file for document processing tests.

    Creates a simple PDF with test content.
    """
    # Create test PDF content
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Add test content
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Test Document for Issue #290")
    c.drawString(100, 730, "")
    c.drawString(100, 710, "This is a test document for document processing.")
    c.drawString(100, 690, "")
    c.drawString(100, 670, "Key Points:")
    c.drawString(100, 650, "- Testing methodology is important")
    c.drawString(100, 630, "- Documents should be analyzed carefully")
    c.drawString(100, 610, "- Integration testing validates end-to-end workflows")
    c.drawString(100, 590, "")
    c.drawString(100, 570, "Conclusion:")
    c.drawString(100, 550, "This document demonstrates the document analysis system.")

    c.save()
    pdf_buffer.seek(0)

    # Upload file
    files = {"file": ("test_document.pdf", pdf_buffer, "application/pdf")}

    response = await async_client.post(
        "/api/v1/files/upload",
        files=files,
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200, f"Upload failed: {response.text}"

    data = response.json()
    file_id = data.get("file_id")
    assert file_id, "No file_id returned from upload"

    return file_id


@pytest.fixture
async def second_uploaded_file_id(async_client: AsyncClient, auth_token: str) -> str:
    """
    Upload a second test PDF for comparison tests.
    """
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Second Test Document")
    c.drawString(100, 730, "")
    c.drawString(100, 710, "This is a different document for comparison.")
    c.drawString(100, 690, "")
    c.drawString(100, 670, "Key Differences:")
    c.drawString(100, 650, "- Different focus area")
    c.drawString(100, 630, "- Alternative approach to testing")
    c.drawString(100, 610, "- Comparison helps identify unique aspects")

    c.save()
    pdf_buffer.seek(0)

    files = {"file": ("second_document.pdf", pdf_buffer, "application/pdf")}

    response = await async_client.post(
        "/api/v1/files/upload",
        files=files,
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200, f"Upload failed: {response.text}"

    data = response.json()
    file_id = data.get("file_id")
    assert file_id, "No file_id returned from upload"

    return file_id


@pytest.mark.integration
@pytest.mark.llm
class TestDocumentProcessing:
    """Integration tests for document processing (Tests 19-24)"""

    async def test_19_analyze_uploaded_document(
        self, async_client: AsyncClient, auth_token: str, uploaded_file_id: str
    ):
        """
        Test 19: Can you analyze the document I just uploaded?

        Verifies:
        - POST /api/v1/documents/{file_id}/analyze works
        - Returns summary and key_findings
        - Requires authentication
        """
        response = await async_client.post(
            f"/api/v1/documents/{uploaded_file_id}/analyze",
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 200, f"Analysis failed: {response.text}"

        data = response.json()

        # Verify response structure
        assert "summary" in data, "Response missing 'summary'"
        assert "key_findings" in data, "Response missing 'key_findings'"
        assert "file_id" in data, "Response missing 'file_id'"
        assert "filename" in data, "Response missing 'filename'"

        # Verify content
        assert data["file_id"] == uploaded_file_id
        assert data["filename"] == "test_document.pdf"
        assert isinstance(data["summary"], str)
        assert len(data["summary"]) > 0, "Summary is empty"

        print(f"✅ Test 19 PASSED - Document analyzed successfully")

    async def test_20_question_document(
        self, async_client: AsyncClient, auth_token: str, uploaded_file_id: str
    ):
        """
        Test 20: What are the key decision points in this document?

        Verifies:
        - POST /api/v1/documents/{file_id}/question works
        - Returns answer based on document content
        - Question answering is context-aware
        """
        question = "What does this document say about testing methodology?"

        response = await async_client.post(
            f"/api/v1/documents/{uploaded_file_id}/question",
            params={"question": question},
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 200, f"Question failed: {response.text}"

        data = response.json()

        # Verify response structure
        assert "answer" in data, "Response missing 'answer'"
        assert "question" in data, "Response missing 'question'"
        assert "file_id" in data, "Response missing 'file_id'"

        # Verify content
        assert data["question"] == question
        assert data["file_id"] == uploaded_file_id
        assert isinstance(data["answer"], str)
        assert len(data["answer"]) > 0, "Answer is empty"

        print(f"✅ Test 20 PASSED - Question answered successfully")

    async def test_21_reference_in_conversation(
        self, async_client: AsyncClient, auth_token: str, uploaded_file_id: str
    ):
        """
        Test 21: Based on what we discussed and the uploaded doc, what should I prioritize?

        Verifies:
        - POST /api/v1/documents/reference works
        - Synthesizes document + conversation context
        - Auto-detects recent file if not specified
        """
        request_body = {
            "message": "Based on this document, what should I prioritize for testing?",
            "file_id": uploaded_file_id,
            "conversation_history": [
                {"role": "user", "content": "I need to improve my testing strategy"},
                {"role": "assistant", "content": "Let me help you with that"},
            ],
        }

        response = await async_client.post(
            "/api/v1/documents/reference",
            json=request_body,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 200, f"Reference failed: {response.text}"

        data = response.json()

        # Verify response structure
        assert "response" in data, "Response missing 'response'"
        assert "file_id" in data, "Response missing 'file_id'"
        assert "conversation_aware" in data, "Response missing 'conversation_aware'"

        # Verify content
        assert data["file_id"] == uploaded_file_id
        assert data["conversation_aware"] is True, "Should be conversation-aware"
        assert isinstance(data["response"], str)
        assert len(data["response"]) > 0, "Response is empty"

        print(f"✅ Test 21 PASSED - Conversational reference processed successfully")

    async def test_22_summarize_document(
        self, async_client: AsyncClient, auth_token: str, uploaded_file_id: str
    ):
        """
        Test 22: Summarize the uploaded research paper in 3 key points.

        Verifies:
        - POST /api/v1/documents/{file_id}/summarize works
        - Supports different format options
        - Returns structured summary
        """
        # Test bullet format
        response = await async_client.post(
            f"/api/v1/documents/{uploaded_file_id}/summarize",
            params={"format": "bullet"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 200, f"Summarize failed: {response.text}"

        data = response.json()

        # Verify response structure
        assert "summary" in data, "Response missing 'summary'"
        assert "file_id" in data, "Response missing 'file_id'"
        assert "format" in data, "Response missing 'format'"

        # Verify content
        assert data["file_id"] == uploaded_file_id
        assert data["format"] == "bullet"
        assert isinstance(data["summary"], str)
        assert len(data["summary"]) > 0, "Summary is empty"

        print(f"✅ Test 22 PASSED - Document summarized successfully")

    async def test_23_compare_documents(
        self,
        async_client: AsyncClient,
        auth_token: str,
        uploaded_file_id: str,
        second_uploaded_file_id: str,
    ):
        """
        Test 23: Upload 2+ documents, ask "Compare these and highlight differences".

        Verifies:
        - POST /api/v1/documents/compare works
        - Compares multiple documents
        - Returns structured comparison
        """
        response = await async_client.post(
            "/api/v1/documents/compare",
            params={"file_ids": [uploaded_file_id, second_uploaded_file_id]},
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 200, f"Compare failed: {response.text}"

        data = response.json()

        # Verify response structure
        assert "comparison" in data, "Response missing 'comparison'"
        assert "file_ids" in data, "Response missing 'file_ids'"
        assert "filenames" in data, "Response missing 'filenames'"

        # Verify content
        assert len(data["file_ids"]) == 2, "Should have 2 file IDs"
        assert uploaded_file_id in data["file_ids"]
        assert second_uploaded_file_id in data["file_ids"]
        assert isinstance(data["comparison"], str)
        assert len(data["comparison"]) > 0, "Comparison is empty"

        print(f"✅ Test 23 PASSED - Documents compared successfully")

    async def test_24_search_documents(
        self, async_client: AsyncClient, auth_token: str, uploaded_file_id: str
    ):
        """
        Test 24: Find the section about testing methodology in my uploaded docs.

        Verifies:
        - GET /api/v1/documents/search works
        - Returns relevant search results
        - Uses semantic search (ChromaDB)
        """
        response = await async_client.get(
            "/api/v1/documents/search",
            params={"q": "testing methodology"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 200, f"Search failed: {response.text}"

        data = response.json()

        # Verify response structure
        assert "query" in data, "Response missing 'query'"
        assert "results" in data, "Response missing 'results'"
        assert "count" in data, "Response missing 'count'"

        # Verify content
        assert data["query"] == "testing methodology"
        assert isinstance(data["results"], list)
        assert isinstance(data["count"], int)

        print(f"✅ Test 24 PASSED - Document search completed successfully")


@pytest.mark.integration
class TestDocumentProcessingEdgeCases:
    """Edge case tests for document processing"""

    async def test_analyze_nonexistent_file(self, async_client: AsyncClient, auth_token: str):
        """Verify 404 for non-existent file"""
        response = await async_client.post(
            "/api/v1/documents/00000000-0000-0000-0000-000000000000/analyze",
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 404, "Should return 404 for non-existent file"

    async def test_question_requires_auth(self, async_client: AsyncClient, uploaded_file_id: str):
        """Verify authentication required"""
        # the uploaded_file_id fixture logged in on THIS client — its auth
        # cookie would ride into the "unauthenticated" request (#1452: the
        # test asserted 401 but measured its own cookie's 200)
        async_client.cookies.clear()
        response = await async_client.post(
            f"/api/v1/documents/{uploaded_file_id}/question",
            params={"question": "test"},
        )

        assert response.status_code == 401, "Should require authentication"

    async def test_compare_requires_minimum_files(
        self, async_client: AsyncClient, auth_token: str, uploaded_file_id: str
    ):
        """Verify compare requires at least 2 files"""
        response = await async_client.post(
            "/api/v1/documents/compare",
            params={"file_ids": [uploaded_file_id]},
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 400, "Should require at least 2 files"
