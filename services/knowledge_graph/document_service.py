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

from .ingestion import get_ingester

logger = logging.getLogger(__name__)


class DocumentService:
    """Handle document upload and processing operations"""

    def __init__(self):
        self.ingester = get_ingester()

    async def upload_pdf(self, file: UploadFile, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle PDF upload with proper file management

        Args:
            file: Uploaded PDF file
            metadata: Document metadata (title, author, domain, etc.)

        Returns:
            Dict with upload results and document info
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

                # Process the document
                result = await self.ingester.ingest_pdf(tmp_file_path, metadata)

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

    async def find_decisions(self, topic: str = "", timeframe: str = "last_week") -> Dict[str, Any]:
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

            if results and "documents" in results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):  # ChromaDB returns nested lists
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

    async def get_relevant_context(self, timeframe: str = "yesterday") -> Dict[str, Any]:
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

            if results and "documents" in results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
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

    async def suggest_documents(self, focus_area: str = "") -> Dict[str, Any]:
        """Suggest documents using existing vector similarity search

        Uses existing OpenAI embeddings and project/feature metadata
        to suggest relevant documents for review.
        """
        try:
            # Use existing ChromaDB collection from ingester
            collection = self.ingester.collection

            suggestions = []

            if focus_area:
                # Semantic search for focus area using existing embeddings
                results = collection.query(
                    query_texts=[focus_area],
                    n_results=5,
                    where={},  # No filtering, get best matches
                )

                if results and "documents" in results and results["documents"]:
                    for i, doc in enumerate(results["documents"][0]):
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
