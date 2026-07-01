"""
Document Analysis REST API Endpoints for Issue #290.

These routes provide direct API access to document operations,
following the pattern from files.py (#282).

All endpoints:
- Require JWT authentication
- Enforce user isolation
- Return structured JSON responses
- Handle errors gracefully
"""

from typing import List, Optional

import structlog
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from pydantic import BaseModel

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.intent_service.document_handlers import (
    handle_analyze_document,
    handle_compare_documents,
    handle_question_document,
    handle_reference_in_conversation,
    handle_search_documents,
    handle_summarize_document,
)
from services.llm.request_key import request_api_key  # #1185: per-user LLM key rail
from web.utils.llm_key import resolve_user_llm_key  # #1185

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])
logger = structlog.get_logger(__name__)


# Request models
class ReferenceRequest(BaseModel):
    """Request body for conversational reference (Test 21)"""

    message: str
    file_id: Optional[str] = None
    conversation_history: Optional[List[dict]] = None


@router.post("/{file_id}/analyze")
async def analyze_document(
    file_id: str,
    current_user: JWTClaims = Depends(get_current_user),
) -> dict:
    """
    Test 19: Analyze uploaded document.

    Calls DocumentAnalyzer to extract summary and key findings.

    Args:
        file_id: UUID of uploaded file
        current_user: Current authenticated user (from JWT token)

    Returns:
        JSON with summary and key_findings

    Raises:
        HTTPException 404: Document not found or access denied
        HTTPException 500: Server error during analysis

    Issue #290: CORE-ALPHA-DOC-PROCESSING (Test 19)
    """
    try:
        # #1185: bind the caller's stored Anthropic key for this request (header > stored
        # > server); else document analysis would silently use the server key, not theirs.
        resolved_key = await resolve_user_llm_key(None, current_user.sub)
        with request_api_key(resolved_key):
            result = await handle_analyze_document(file_id=file_id, user_id=current_user.user_id)
        logger.info(
            "Document analyzed",
            file_id=file_id,
            user_id=current_user.user_id,
        )
        return result

    except FileNotFoundError as e:
        logger.warning(
            "Document not found",
            file_id=file_id,
            user_id=current_user.user_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except Exception as e:
        logger.error(
            "Analysis failed",
            file_id=file_id,
            user_id=current_user.user_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}",
        )


@router.post("/{file_id}/question")
async def ask_question_about_document(
    file_id: str,
    question: str = Query(..., description="Question about the document"),
    current_user: JWTClaims = Depends(get_current_user),
) -> dict:
    """
    Test 20: Ask question about document content.

    Uses LLM Q&A with document context.

    Args:
        file_id: UUID of uploaded file
        question: User's question
        current_user: Current authenticated user (from JWT token)

    Returns:
        JSON with answer and question

    Raises:
        HTTPException 404: Document not found or access denied
        HTTPException 500: Server error during Q&A

    Issue #290: CORE-ALPHA-DOC-PROCESSING (Test 20)
    """
    try:
        # #1185: bind the caller's stored Anthropic key for this request.
        resolved_key = await resolve_user_llm_key(None, current_user.sub)
        with request_api_key(resolved_key):
            result = await handle_question_document(
                file_id=file_id, question=question, user_id=current_user.user_id
            )
        logger.info(
            "Question answered",
            file_id=file_id,
            user_id=current_user.user_id,
        )
        return result

    except FileNotFoundError as e:
        logger.warning(
            "Document not found",
            file_id=file_id,
            user_id=current_user.user_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except Exception as e:
        logger.error(
            "Question answering failed",
            file_id=file_id,
            user_id=current_user.user_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Question answering failed: {str(e)}",
        )


@router.post("/{file_id}/summarize")
async def summarize_document(
    file_id: str,
    format: str = Query("bullet", pattern="^(bullet|paragraph|detailed)$"),
    current_user: JWTClaims = Depends(get_current_user),
) -> dict:
    """
    Test 22: Summarize document in requested format.

    Args:
        file_id: UUID of uploaded file
        format: Output format (bullet, paragraph, detailed)
        current_user: Current authenticated user (from JWT token)

    Returns:
        JSON with summary in requested format

    Raises:
        HTTPException 404: Document not found or access denied
        HTTPException 500: Server error during summarization

    Issue #290: CORE-ALPHA-DOC-PROCESSING (Test 22)
    """
    try:
        # #1185: bind the caller's stored Anthropic key for this request.
        resolved_key = await resolve_user_llm_key(None, current_user.sub)
        with request_api_key(resolved_key):
            result = await handle_summarize_document(
                file_id=file_id, format=format, user_id=current_user.user_id
            )
        logger.info(
            "Document summarized",
            file_id=file_id,
            format=format,
            user_id=current_user.user_id,
        )
        return result

    except FileNotFoundError as e:
        logger.warning(
            "Document not found",
            file_id=file_id,
            user_id=current_user.user_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except Exception as e:
        logger.error(
            "Summarization failed",
            file_id=file_id,
            user_id=current_user.user_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Summarization failed: {str(e)}",
        )


@router.post("/compare")
async def compare_documents(
    file_ids: List[str] = Query(..., description="File IDs to compare (2-5)"),
    current_user: JWTClaims = Depends(get_current_user),
) -> dict:
    """
    Test 23: Compare multiple documents.

    Args:
        file_ids: List of file UUIDs (2-5 documents)
        current_user: Current authenticated user (from JWT token)

    Returns:
        JSON with comparison results

    Raises:
        HTTPException 400: Invalid number of files
        HTTPException 404: One or more documents not found
        HTTPException 500: Server error during comparison

    Issue #290: CORE-ALPHA-DOC-PROCESSING (Test 23)
    """
    try:
        if len(file_ids) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least 2 documents required for comparison",
            )

        if len(file_ids) > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum 5 documents can be compared at once",
            )

        # #1185: bind the caller's stored Anthropic key for this request.
        resolved_key = await resolve_user_llm_key(None, current_user.sub)
        with request_api_key(resolved_key):
            result = await handle_compare_documents(
                file_ids=file_ids, user_id=current_user.user_id
            )
        logger.info(
            "Documents compared",
            file_count=len(file_ids),
            user_id=current_user.user_id,
        )
        return result

    except FileNotFoundError as e:
        logger.warning(
            "Document not found during comparison",
            file_ids=file_ids,
            user_id=current_user.user_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        logger.error(
            "Comparison failed",
            file_ids=file_ids,
            user_id=current_user.user_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comparison failed: {str(e)}",
        )


@router.post("/reference")
async def reference_in_conversation(
    request: ReferenceRequest,
    current_user: JWTClaims = Depends(get_current_user),
) -> dict:
    """
    Test 21: Reference document in conversation.

    Synthesizes document content with conversation history.

    Request Body:
        message: User's message referencing document
        file_id: File UUID (optional, auto-detects most recent)
        conversation_history: Recent messages (optional)

    Args:
        request: Reference request with message and optional context
        current_user: Current authenticated user (from JWT token)

    Returns:
        JSON with synthesized response

    Raises:
        HTTPException 404: Document not found
        HTTPException 500: Server error during synthesis

    Issue #290: CORE-ALPHA-DOC-PROCESSING (Test 21)
    """
    try:
        # #1185: bind the caller's stored Anthropic key for this request.
        resolved_key = await resolve_user_llm_key(None, current_user.sub)
        with request_api_key(resolved_key):
            result = await handle_reference_in_conversation(
                message=request.message,
                file_id=request.file_id,
                user_id=current_user.user_id,
                conversation_history=request.conversation_history,
            )
        logger.info(
            "Conversational reference processed",
            file_id=request.file_id,
            user_id=current_user.user_id,
        )
        return result

    except FileNotFoundError as e:
        logger.warning(
            "Document not found for reference",
            file_id=request.file_id,
            user_id=current_user.user_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except Exception as e:
        logger.error(
            "Conversational reference failed",
            file_id=request.file_id,
            user_id=current_user.user_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Reference processing failed: {str(e)}",
        )


@router.get("/search")
async def search_documents(
    q: str = Query(..., description="Search query", min_length=1),
    current_user: JWTClaims = Depends(get_current_user),
) -> dict:
    """
    Test 24: Search across user's documents.

    Uses ChromaDB semantic search.

    Args:
        q: Search query
        current_user: Current authenticated user (from JWT token)

    Returns:
        JSON with search results

    Raises:
        HTTPException 500: Server error during search

    Issue #290: CORE-ALPHA-DOC-PROCESSING (Test 24)
    """
    try:
        result = await handle_search_documents(query=q, user_id=current_user.user_id)
        logger.info(
            "Documents searched",
            query=q,
            result_count=result.get("count", 0),
            user_id=current_user.user_id,
        )
        return result

    except Exception as e:
        logger.error(
            "Search failed",
            query=q,
            user_id=current_user.user_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}",
        )
