"""
Document Service - Handle file operations for knowledge base
Extracted from main.py to maintain proper abstraction layers
"""

import json
import logging
import os
import shutil
import tempfile
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import UploadFile

from services.database.session_factory import AsyncSessionFactory
from services.repositories.document_repository import DocumentRepository

from .ingestion import get_ingester

logger = logging.getLogger(__name__)


def _base_id(chunk_id: str) -> str:
    """ChromaDB chunk id ``pdf_<hash>_chunk_<i>`` → document base id ``pdf_<hash>``."""
    return chunk_id.rsplit("_chunk_", 1)[0]


class DocumentService:
    """Handle document upload and processing operations"""

    def __init__(self, session_scope=None, ingester=None):
        # ingester + session_scope are injectable for tests (avoid ChromaDB/embeddings
        # init and let the relational anchor write target an in-memory SQLite engine).
        self.ingester = ingester if ingester is not None else get_ingester()
        self._session_scope = session_scope or AsyncSessionFactory.session_scope

    async def upload_pdf(
        self,
        file: UploadFile,
        metadata: Dict[str, Any],
        owner_id: Any = None,
        is_global_pm_domain: bool = False,
    ) -> Dict[str, Any]:
        """
        Handle PDF upload (web/UploadFile path) with proper file management.

        #1238 (ADR-071 P2): writes the relational anchor row (owner_id +
        is_global_pm_domain) after ChromaDB ingest. Defaults are safe — a web
        upload is a user's private doc (owner-scoped, not global) unless the
        caller explicitly opts into the PM-domain by passing is_global_pm_domain=True.

        Args:
            file: Uploaded PDF file
            metadata: Document metadata (title, author, domain, etc.)
            owner_id: provenance principal (users.id); None = unknown (m-40 graceful)
            is_global_pm_domain: D1 exemption — readable by any principal when True
        """
        # Validate file type
        if not file.filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are currently supported")

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            try:
                # Copy uploaded file to temp location
                shutil.copyfileobj(file.file, tmp_file)
                tmp_file_path = tmp_file.name

                logger.info(
                    f"Processing document: {file.filename} into domain: {metadata.get('knowledge_domain')}"
                )

                # Ingest into ChromaDB + write the relational anchor row
                result = await self._ingest_and_anchor(
                    tmp_file_path,
                    metadata,
                    owner_id=owner_id,
                    is_global_pm_domain=is_global_pm_domain,
                    source=file.filename,
                )

                return {
                    "status": "success",
                    "message": f"Document '{metadata.get('title', file.filename)}' successfully processed",
                    "details": result,
                }

            except Exception as e:
                logger.error(f"Document upload failed: {e}")
                raise
            finally:
                # Always clean up temp file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)

    async def ingest_path(
        self,
        file_path: str,
        metadata: Dict[str, Any],
        owner_id: Any = None,
        is_global_pm_domain: bool = False,
    ) -> Dict[str, Any]:
        """
        Path-based ingest for the CLI (the operator already has a real file path).

        Replaces the previous CLI call to ``upload_pdf(file_path, ...)`` which passed
        a string to an ``UploadFile``-typed method (a no-op/crash). #1238 also writes
        the relational anchor row. CLI-ingested docs are PM-domain knowledge base, so
        the CLI passes ``is_global_pm_domain=True`` + the configured-PM ``owner_id``.
        """
        if not file_path.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are currently supported")
        result = await self._ingest_and_anchor(
            file_path,
            metadata,
            owner_id=owner_id,
            is_global_pm_domain=is_global_pm_domain,
            source=file_path,
        )
        return {
            "status": result.get("status", "success"),
            "message": f"Document '{metadata.get('title', file_path)}' successfully processed",
            "details": result,
        }

    async def _ingest_and_anchor(
        self,
        file_path: str,
        metadata: Dict[str, Any],
        owner_id: Any = None,
        is_global_pm_domain: bool = False,
        source: Any = None,
    ) -> Dict[str, Any]:
        """Ingest into ChromaDB, then write the relational anchor row (#1238)."""
        result = await self.ingester.ingest_pdf(file_path, metadata)
        base_id = result.get("document_id")
        if base_id:
            await self._anchor_document(
                chromadb_base_id=base_id,
                owner_id=owner_id,
                is_global_pm_domain=is_global_pm_domain,
                title=metadata.get("title"),
                source=source or file_path,
            )
        return result

    async def _anchor_document(
        self,
        chromadb_base_id: str,
        owner_id: Any,
        is_global_pm_domain: bool,
        title: Any,
        source: Any,
    ) -> None:
        """Write/refresh the relational anchor row for an ingested document (ADR-071 P2).

        Best-effort: ChromaDB and Postgres are not transactional together, so a failed
        anchor write logs + leaves the doc unanchored (fail-safe — it won't surface in
        scoped reads until re-ingested, which is idempotent) rather than rolling back a
        successful ChromaDB ingest.
        """
        try:
            async with self._session_scope() as session:
                repo = DocumentRepository(session)
                await repo.upsert_document(
                    chromadb_base_id,
                    owner_id=owner_id,
                    is_global_pm_domain=is_global_pm_domain,
                    title=title,
                    source=source,
                )
        except Exception as e:  # pragma: no cover - defensive (fail-safe, logged)
            logger.error(f"Document anchor write failed for {chromadb_base_id}: {e}")

    async def _readable_base_ids(self, owner_id: Any) -> set:
        """The set of ChromaDB base_ids the principal may read (#1238, ADR-071 P2).

        Readable = is_global_pm_domain OR owner_id == principal (None/non-UUID → global
        only, m-40 graceful). The 3 reads intersect ChromaDB results with this set —
        the marker lives on the documents row, not in ChromaDB metadata (Arch ruling).
        """
        async with self._session_scope() as session:
            return await DocumentRepository(session).get_readable_base_ids(owner_id)

    @staticmethod
    def _chunk_readable(results: Dict[str, Any], i: int, readable: set) -> bool:
        """True if the i-th ChromaDB result is an authorized (readable) document.

        Fail-closed: a result whose base_id can't be determined, or isn't in the
        readable set, is excluded — un-anchored/unauthorized content is never surfaced.
        """
        ids = results.get("ids") if isinstance(results, dict) else None
        if not ids or not ids[0] or i >= len(ids[0]):
            return False
        return _base_id(ids[0][i]) in readable

    async def list_for_user(self, user_id: Any) -> List[Dict[str, Any]]:
        """List the user's own documents (newest-first) for the Radar DocumentEntitySource (#1238).

        Owner-scoped (the user's own docs, not the global PM knowledge base). Returns plain
        detached dicts with the fields a Document RadarEntity needs (title, source, timestamps,
        chromadb_base_id as the ref).
        """
        async with self._session_scope() as session:
            rows = await DocumentRepository(session).list_for_owner(user_id)
            return [
                {
                    "chromadb_base_id": r.chromadb_base_id,
                    "title": r.title,
                    "source": r.source,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                    "updated_at": r.updated_at.isoformat() if r.updated_at else None,
                }
                for r in rows
            ]

    async def find_decisions(
        self, topic: str = "", timeframe: str = "last_week", owner_id: Any = None
    ) -> Dict[str, Any]:
        """Find decisions using existing ChromaDB vector search + metadata filtering

        Uses existing pm_knowledge collection and relationship analysis metadata
        to extract decisions from stored documents.
        """
        try:
            # Use existing ChromaDB collection from ingester
            collection = self.ingester.collection

            # Calculate timeframe for filtering
            now = datetime.now()
            if timeframe == "today":
                timeframe_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif timeframe == "yesterday":
                timeframe_start = now - timedelta(days=1)
            elif timeframe == "last_week":
                timeframe_start = now - timedelta(weeks=1)
            elif timeframe == "last_month":
                timeframe_start = now - timedelta(days=30)
            else:
                timeframe_start = now - timedelta(weeks=1)  # Default to last week

            timeframe_timestamp = timeframe_start.timestamp()

            # Query existing pm_knowledge collection
            if topic:
                # Semantic search for topic with metadata filtering
                results = collection.query(
                    query_texts=[f"decision about {topic}"],
                    n_results=20,
                    where={"analysis_timestamp": {"$gte": timeframe_timestamp}},
                )
            else:
                # Get all documents in timeframe, then filter for decisions
                results = collection.query(
                    query_texts=["decision", "decided", "agreed", "resolved"],
                    n_results=20,
                    where={"analysis_timestamp": {"$gte": timeframe_timestamp}},
                )

            decisions = []
            readable = await self._readable_base_ids(owner_id)  # #1238: owner-scope

            if results and "documents" in results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):  # ChromaDB returns nested lists
                    if not self._chunk_readable(results, i, readable):
                        continue  # #1238: skip docs the principal may not read
                    metadata = results["metadatas"][0][i] if "metadatas" in results else {}
                    distance = results["distances"][0][i] if "distances" in results else 1.0

                    # Extract decision content from document text
                    if doc and len(doc) > 0:
                        # Look for decision patterns in document content
                        lines = doc.split("\n")
                        decision_lines = []

                        for line in lines:
                            line_lower = line.lower().strip()
                            if any(
                                keyword in line_lower
                                for keyword in [
                                    "decision:",
                                    "decided",
                                    "agreed",
                                    "resolved",
                                    "concluded",
                                ]
                            ):
                                decision_lines.append(line.strip())

                        # If we found decision content, add to results
                        if decision_lines or (topic and topic.lower() in doc.lower()):
                            decisions.append(
                                {
                                    "topic": topic or "general",
                                    "decision": (
                                        decision_lines[0] if decision_lines else doc[:100] + "..."
                                    ),
                                    "date": metadata.get(
                                        "analysis_timestamp", datetime.now().isoformat()
                                    ),
                                    "document_title": metadata.get("title", "Untitled Document"),
                                    "confidence": max(
                                        0.1, 1.0 - distance
                                    ),  # Convert distance to confidence
                                    "context": doc[:200] + "..." if len(doc) > 200 else doc,
                                }
                            )

            return {
                "decisions": decisions,
                "topic": topic,
                "timeframe": timeframe,
                "count": len(decisions),
                "source": "chromadb_pm_knowledge",
            }

        except Exception as e:
            logger.error(f"Decision search failed: {e}")
            return {
                "decisions": [],
                "topic": topic,
                "timeframe": timeframe,
                "count": 0,
                "error": f"Decision search unavailable: {str(e)}",
                "fallback_mode": True,
            }

    async def get_relevant_context(
        self, timeframe: str = "yesterday", owner_id: Any = None
    ) -> Dict[str, Any]:
        """Get document context using existing ChromaDB temporal filtering

        Uses existing pm_knowledge collection and analysis_timestamp metadata
        to retrieve relevant documents within the specified timeframe.
        """
        try:
            # Use existing ChromaDB collection from ingester
            collection = self.ingester.collection

            # Calculate timeframe for filtering
            now = datetime.now()
            if timeframe == "today":
                timeframe_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif timeframe == "yesterday":
                timeframe_start = now - timedelta(days=1)
            elif timeframe == "last_week":
                timeframe_start = now - timedelta(weeks=1)
            elif timeframe == "last_month":
                timeframe_start = now - timedelta(days=30)
            else:
                timeframe_start = now - timedelta(days=1)  # Default to yesterday

            timeframe_timestamp = timeframe_start.timestamp()

            # Query existing pm_knowledge collection for documents in timeframe
            results = collection.query(
                query_texts=["context", "summary", "important", "key"],
                n_results=10,
                where={"analysis_timestamp": {"$gte": timeframe_timestamp}},
            )

            context_docs = []
            readable = await self._readable_base_ids(owner_id)  # #1238: owner-scope

            if results and "documents" in results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    if not self._chunk_readable(results, i, readable):
                        continue  # #1238: skip docs the principal may not read
                    metadata = results["metadatas"][0][i] if "metadatas" in results else {}
                    distance = results["distances"][0][i] if "distances" in results else 1.0

                    if doc and len(doc) > 0:
                        context_docs.append(
                            {
                                "id": f"doc_{i}",
                                "title": metadata.get("title", "Untitled Document"),
                                "summary": doc[:300] + "..." if len(doc) > 300 else doc,
                                "document_type": metadata.get("document_type", "unknown"),
                                "relevance": max(0.1, 1.0 - distance),
                                "created_at": metadata.get(
                                    "analysis_timestamp", datetime.now().isoformat()
                                ),
                                "topics": (
                                    json.loads(metadata.get("main_concepts", "[]"))
                                    if isinstance(metadata.get("main_concepts"), str)
                                    else metadata.get("main_concepts", [])[:3]
                                ),
                                "key_findings": (
                                    json.loads(metadata.get("related_keywords", "[]"))
                                    if isinstance(metadata.get("related_keywords"), str)
                                    else metadata.get("related_keywords", [])[:3]
                                ),
                            }
                        )

            # Sort by relevance
            context_docs.sort(key=lambda d: d["relevance"], reverse=True)

            return {
                "context_documents": context_docs,
                "timeframe": timeframe,
                "count": len(context_docs),
                "source": "chromadb_pm_knowledge",
            }

        except Exception as e:
            logger.error(f"Context retrieval failed: {e}")
            return {
                "context_documents": [],
                "timeframe": timeframe,
                "count": 0,
                "error": f"Context retrieval unavailable: {str(e)}",
                "fallback_mode": True,
            }

    async def suggest_documents(self, focus_area: str = "", owner_id: Any = None) -> Dict[str, Any]:
        """Suggest documents using existing vector similarity search

        Uses existing OpenAI embeddings and project/feature metadata
        to suggest relevant documents for review.
        """
        try:
            # Use existing ChromaDB collection from ingester
            collection = self.ingester.collection

            suggestions = []
            readable = await self._readable_base_ids(owner_id)  # #1238: owner-scope

            if focus_area:
                # Semantic search for focus area using existing embeddings
                results = collection.query(
                    query_texts=[focus_area],
                    n_results=5,
                    where={},  # No filtering, get best matches
                )

                if results and "documents" in results and results["documents"]:
                    for i, doc in enumerate(results["documents"][0]):
                        if not self._chunk_readable(results, i, readable):
                            continue  # #1238: skip docs the principal may not read
                        metadata = results["metadatas"][0][i] if "metadatas" in results else {}
                        distance = results["distances"][0][i] if "distances" in results else 1.0

                        if doc and len(doc) > 0:
                            relevance = max(0.1, 1.0 - distance)
                            suggestions.append(
                                {
                                    "id": f"suggestion_{i}",
                                    "title": metadata.get("title", "Untitled Document"),
                                    "reason": f"Relevant to {focus_area} (similarity: {relevance:.2f})",
                                    "priority": (
                                        "high"
                                        if relevance > 0.7
                                        else "medium"
                                        if relevance > 0.4
                                        else "low"
                                    ),
                                    "document_type": metadata.get("document_type", "unknown"),
                                    "last_accessed": metadata.get(
                                        "analysis_timestamp", datetime.now().isoformat()
                                    ),
                                }
                            )
            else:
                # General suggestions - get recent diverse documents
                results = collection.query(
                    query_texts=["important", "key", "summary"], n_results=5, where={}
                )

                if results and "documents" in results and results["documents"]:
                    for i, doc in enumerate(results["documents"][0]):
                        if not self._chunk_readable(results, i, readable):
                            continue  # #1238: skip docs the principal may not read
                        metadata = results["metadatas"][0][i] if "metadatas" in results else {}

                        if doc and len(doc) > 0:
                            suggestions.append(
                                {
                                    "id": f"general_{i}",
                                    "title": metadata.get("title", "Untitled Document"),
                                    "reason": "Recent document with relevant content",
                                    "priority": "medium",
                                    "document_type": metadata.get("document_type", "unknown"),
                                    "last_accessed": metadata.get(
                                        "analysis_timestamp", datetime.now().isoformat()
                                    ),
                                }
                            )

            return {
                "suggestions": suggestions,
                "focus_area": focus_area,
                "count": len(suggestions),
                "source": "chromadb_pm_knowledge",
            }

        except Exception as e:
            logger.error(f"Document suggestions failed: {e}")
            return {
                "suggestions": [],
                "focus_area": focus_area,
                "count": 0,
                "error": f"Document suggestions unavailable: {str(e)}",
                "fallback_mode": True,
            }


# Singleton instance
_document_service = None


def get_document_service() -> DocumentService:
    """Get document service instance"""
    global _document_service
    if _document_service is None:
        _document_service = DocumentService()
    return _document_service
