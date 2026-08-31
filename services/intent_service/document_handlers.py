"""
Document Operation Handlers for Issue #290.

These handlers wire existing DocumentService and DocumentAnalyzer
into the chat/intent system. Follows separation of concerns pattern
(architectural guidance 2025-11-01).

Each handler:
- Calls EXISTING services (DocumentService, DocumentAnalyzer)
- Enforces user isolation
- Returns structured results for Tests 19-24
"""

from pathlib import Path
from typing import Dict, List, Optional
from uuid import UUID

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.analysis.document_analyzer import DocumentAnalyzer, extract_document_text
from services.database.connection import db
from services.database.models import UploadedFileDB
from services.database.session_factory import AsyncSessionFactory
from services.file_context.storage import read_file_from_storage  # #1306: the single byte-read seam
from services.knowledge_graph.document_service import get_document_service
from services.llm.clients import llm_client

logger = structlog.get_logger(__name__)

# #1452: DocumentService construction reaches OpenAIEmbeddingFunction, which
# RAISES without an API key — eager module-level init made this whole module
# (and the Documents API router importing it) fail to import in keyless
# environments. Use the service module's existing lazy getter at the
# operation boundary instead.
_doc_analyzer = DocumentAnalyzer(llm_client=llm_client)


async def _get_uploaded_file(
    file_id: str, user_id: str, session: AsyncSession
) -> Optional[UploadedFileDB]:
    """
    Retrieve uploaded file with user isolation.

    Args:
        file_id: File UUID
        user_id: User UUID (ownership isolation)
        session: Database session

    Returns:
        UploadedFileDB record or None

    Note:
        Ownership is owner_id (UUID FK to users) since the #1312 ownership
        migration — the old session_id convention this file assumed is gone
        (it silently 500'd the beta analyze route until #1452 surfaced it).
    """
    stmt = select(UploadedFileDB).where(
        UploadedFileDB.id == file_id, UploadedFileDB.owner_id == user_id
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def _get_owned_artifact(file_id: str, user_id: str, session: AsyncSession):
    """Owner-scoped artifact fetch (#1657).

    The /files view is uploads ∪ generated artifacts (#355), so an id resolved
    from "the user's documents" may be an artifact. Scoping matches
    _get_uploaded_file exactly: owner only, no admin bypass here — a
    cross-owner id returns None and the caller raises FileNotFoundError, same
    as an unowned upload.
    """
    from services.database.repositories import ArtifactRepository

    return await ArtifactRepository(session).get_by_id(file_id, owner_id=user_id)


async def handle_analyze_document(file_id: str, user_id: str) -> Dict:
    """
    Test 19: Analyze uploaded document.

    Calls existing DocumentAnalyzer.analyze() method.

    Args:
        file_id: UUID of uploaded file
        user_id: UUID of user (for isolation)

    Returns:
        Dict with summary and key_findings

    Raises:
        FileNotFoundError: If file doesn't exist or user doesn't own it
    """
    logger.info("Analyzing document", file_id=file_id, user_id=user_id)

    # 1. Retrieve file metadata with user isolation
    async with AsyncSessionFactory.session_scope_fresh() as session:  # Issue #442 fix
        file_record = await _get_uploaded_file(file_id, user_id, session)

        if not file_record:
            # #1657: not an upload — maybe the user's saved artifact (the
            # /files view's other half). Owner-scoped; content lives in the
            # artifacts row, so it goes through the analyzer's text path.
            artifact = await _get_owned_artifact(file_id, user_id, session)
            if artifact is not None:
                from services.file_context.artifact_view import artifact_filename

                analysis_result = await _doc_analyzer.analyze_text(
                    artifact.content or "", source_id=artifact.id
                )
                return {
                    "file_id": artifact.id,
                    "filename": artifact_filename(
                        (artifact.payload or {}).get("title"), artifact.id
                    ),
                    "summary": analysis_result.summary if analysis_result.summary else "",
                    "key_findings": analysis_result.key_findings or [],
                    "analyzed_at": analysis_result.generated_at.isoformat(),
                }
            raise FileNotFoundError(
                f"Document {file_id} not found or access denied for user {user_id}"
            )

        # 2. Get file path from storage (stored in database)
        file_path = file_record.storage_path

        if not file_path or not Path(file_path).exists():
            raise FileNotFoundError(f"File not found in storage: {file_path}")

        # 3. Call existing analyzer — passing the stored MIME type + original
        # filename so it dispatches per file type (#1659) instead of running
        # pypdf on everything.
        analysis_result = await _doc_analyzer.analyze(
            str(file_path),
            file_type=file_record.file_type,
            filename=file_record.filename,
        )

        # 4. Return formatted result
        return {
            "file_id": file_id,
            "filename": file_record.filename,
            "summary": analysis_result.summary if analysis_result.summary else "",
            "key_findings": analysis_result.recommendations or [],
            "analyzed_at": analysis_result.generated_at.isoformat(),
        }


async def handle_question_document(file_id: str, question: str, user_id: str) -> Dict:
    """
    Test 20: Answer question about document.

    Uses existing DocumentService + LLM Q&A.

    Args:
        file_id: UUID of uploaded file
        question: User's question about the document
        user_id: UUID of user (for isolation)

    Returns:
        Dict with answer, question, and file_id

    Raises:
        FileNotFoundError: If file doesn't exist or user doesn't own it
    """
    logger.info("Answering question about document", file_id=file_id, user_id=user_id)

    # 1. Retrieve document with user isolation
    async with AsyncSessionFactory.session_scope_fresh() as session:  # Issue #442 fix
        file_record = await _get_uploaded_file(file_id, user_id, session)

        if not file_record:
            raise FileNotFoundError(
                f"Document {file_id} not found or access denied for user {user_id}"
            )

        # 2. Get file path and read content
        file_path = file_record.storage_path

        if not file_path or not Path(file_path).exists():
            raise FileNotFoundError(f"File not found in storage: {file_path}")

        # 3. Extract text content — type-dispatched (#1659): plain text reads
        # directly, PDFs via pypdf; unsupported types raise with an honest
        # message naming the real type, never a wrong 'corrupted PDF' claim.
        # #1306: bytes via the decrypt seam, never a raw open()
        text_content = extract_document_text(
            read_file_from_storage(file_path),
            file_type=file_record.file_type,
            filename=file_record.filename,
        )

        # 4. Build Q&A prompt
        prompt = f"""You are answering a question about a document.

Document content:
{text_content[:4000]}  # Limit to avoid token overflow

User question: {question}

Answer based ONLY on the document content above.
Cite specific sections when possible.
If the answer is not in the document, say so clearly."""

        # 5. Call LLM
        answer = await llm_client.complete(task_type="question_answering", prompt=prompt)

        return {
            "file_id": file_id,
            "filename": file_record.filename,
            "question": question,
            "answer": answer,
        }


async def handle_summarize_document(file_id: str, format: str, user_id: str) -> Dict:
    """
    Test 22: Summarize document.

    Reuses DocumentAnalyzer.analyze() with specific format.

    Args:
        file_id: UUID of uploaded file
        format: Output format ("bullet", "paragraph", "detailed")
        user_id: UUID of user (for isolation)

    Returns:
        Dict with summary in requested format

    Raises:
        FileNotFoundError: If file doesn't exist or user doesn't own it
    """
    logger.info("Summarizing document", file_id=file_id, format=format, user_id=user_id)

    # 1. Call analyze (same as handle_analyze_document)
    analysis = await handle_analyze_document(file_id, user_id)

    # 2. Format based on requested style
    summary_text = analysis["summary"]

    if format == "bullet":
        # Convert to bullet points if not already
        if not summary_text.startswith("•") and not summary_text.startswith("-"):
            # Extract sentences and bulletize
            sentences = [s.strip() for s in summary_text.split(".") if s.strip()]
            summary_text = "\n".join([f"• {sent}" for sent in sentences[:5]])

    elif format == "detailed":
        # Include key findings
        detailed = f"{summary_text}\n\nKey Findings:\n"
        detailed += "\n".join([f"- {finding}" for finding in analysis["key_findings"]])
        summary_text = detailed

    # format == "paragraph" uses summary as-is

    return {
        "file_id": file_id,
        "filename": analysis["filename"],
        "summary": summary_text,
        "format": format,
    }


async def handle_compare_documents(file_ids: List[str], user_id: str) -> Dict:
    """
    Test 23: Compare multiple documents.

    Uses existing DocumentService + comparison prompt.

    Args:
        file_ids: List of file UUIDs to compare
        user_id: UUID of user (for isolation)

    Returns:
        Dict with comparison results

    Raises:
        FileNotFoundError: If any file doesn't exist or user doesn't own it
        ValueError: If fewer than 2 files provided
    """
    logger.info("Comparing documents", file_ids=file_ids, user_id=user_id)

    if len(file_ids) < 2:
        raise ValueError("At least 2 documents required for comparison")

    # 1. Retrieve all documents with user isolation
    documents = []
    async with AsyncSessionFactory.session_scope_fresh() as session:  # Issue #442 fix
        for file_id in file_ids[:5]:  # Limit to 5 docs to avoid token overflow
            file_record = await _get_uploaded_file(file_id, user_id, session)

            if not file_record:
                raise FileNotFoundError(
                    f"Document {file_id} not found or access denied for user {user_id}"
                )

            # Get file content
            file_path = file_record.storage_path

            if not file_path or not Path(file_path).exists():
                raise FileNotFoundError(f"File not found in storage: {file_path}")

            # Extract text — type-dispatched (#1659), honest on unsupported types
            # #1306: bytes via the decrypt seam, never a raw open()
            text_content = extract_document_text(
                read_file_from_storage(file_path),
                file_type=file_record.file_type,
                filename=file_record.filename,
            )

            documents.append(
                {
                    "file_id": file_id,
                    "filename": file_record.filename,
                    "content": text_content[:2000],  # Limit per doc
                }
            )

    # 2. Build comparison prompt
    doc_summaries = "\n\n".join(
        [
            f"Document {i+1} ({doc['filename']}):\n{doc['content']}"
            for i, doc in enumerate(documents)
        ]
    )

    prompt = f"""Compare these documents:

{doc_summaries}

Provide a structured comparison:
1. Key similarities
2. Key differences
3. Complementary information
4. Conflicting information (if any)
"""

    # 3. Call LLM
    comparison = await llm_client.complete(task_type="document_comparison", prompt=prompt)

    return {
        "file_ids": file_ids,
        "filenames": [doc["filename"] for doc in documents],
        "comparison": comparison,
    }


async def handle_search_documents(query: str, user_id: str) -> Dict:
    """
    Test 24: Search across user's documents.

    Calls existing DocumentService.find_decisions() (uses ChromaDB).

    Args:
        query: Search query
        user_id: UUID of user (for isolation)

    Returns:
        Dict with search results

    Note:
        DocumentService.find_decisions() is owner-scoped (#1238, ADR-071 P2):
        passing owner_id filters results to documents the principal may read
        (owner == principal OR is_global_pm_domain). The user_id here is the principal.
    """
    logger.info("Searching documents", query=query, user_id=user_id)

    # #1238: owner-scoped — pass the principal so another user's private docs
    # aren't surfaced (global PM-domain docs remain readable via the marker).
    results = await get_document_service().find_decisions(topic=query, owner_id=user_id)

    return {
        "query": query,
        "results": results.get("decisions", []),
        "count": len(results.get("decisions", [])),
    }


async def handle_reference_in_conversation(
    message: str,
    file_id: Optional[str],
    user_id: str,
    conversation_history: Optional[List[Dict]] = None,
) -> Dict:
    """
    Test 21: Reference document in conversation context.

    Merges document content with conversation history for LLM synthesis.

    Args:
        message: User's message referencing document
        file_id: UUID of referenced file (or None to find from recent uploads)
        user_id: UUID of user (for isolation)
        conversation_history: Recent conversation messages (optional)

    Returns:
        Dict with synthesized response combining document and conversation

    Raises:
        FileNotFoundError: If file doesn't exist or user doesn't own it
    """
    logger.info(
        "Processing conversational document reference",
        file_id=file_id,
        user_id=user_id,
    )

    # 1. If no file_id provided, try to find recently uploaded file
    if not file_id:
        async with AsyncSessionFactory.session_scope_fresh() as session:  # Issue #442 fix
            # Get most recently uploaded file for this owner
            stmt = (
                select(UploadedFileDB)
                .where(UploadedFileDB.owner_id == user_id)
                .order_by(UploadedFileDB.upload_time.desc())
                .limit(1)
            )
            result = await session.execute(stmt)
            file_record = result.scalar_one_or_none()

            if not file_record:
                return {
                    "error": "No document found. Please upload a document first.",
                    "requires_clarification": True,
                }

            file_id = file_record.id
            logger.info(
                "Auto-detected recent document",
                file_id=file_id,
                filename=file_record.filename,
            )

    # 2. Retrieve document content
    async with AsyncSessionFactory.session_scope_fresh() as session:  # Issue #442 fix
        file_record = await _get_uploaded_file(file_id, user_id, session)

        if not file_record:
            raise FileNotFoundError(
                f"Document {file_id} not found or access denied for user {user_id}"
            )

        # Get file path
        file_path = file_record.storage_path

        if not file_path or not Path(file_path).exists():
            raise FileNotFoundError(f"File not found in storage: {file_path}")

        # Extract text content — type-dispatched (#1659), honest on unsupported
        # types. PDF branch keeps the first-5-pages cap to avoid token overflow.
        # #1306: bytes via the decrypt seam, never a raw open()
        text_content = extract_document_text(
            read_file_from_storage(file_path),
            file_type=file_record.file_type,
            filename=file_record.filename,
            max_pages=5,
        )

    # 3. Build conversation context
    conversation_context = ""
    if conversation_history:
        recent_messages = conversation_history[-5:]  # Last 5 messages
        conversation_context = "\n".join(
            [f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in recent_messages]
        )

    # 4. Build synthesis prompt
    prompt = f"""You are helping a user by synthesizing information from a document and conversation history.

Document ({file_record.filename}):
{text_content[:3000]}  # Limit document content

Recent Conversation:
{conversation_context if conversation_context else "(No prior conversation)"}

User's Current Message: {message}

Provide a helpful response that:
1. References relevant information from the document
2. Considers the conversation history
3. Directly answers the user's question
4. Cites specific sections from the document when applicable

Format your response naturally, as if continuing the conversation."""

    # 5. Call LLM for synthesis
    response = await llm_client.complete(task_type="conversational_reference", prompt=prompt)

    return {
        "response": response,
        "file_id": file_id,
        "filename": file_record.filename,
        "conversation_aware": bool(conversation_history),
        "message": message,
    }
