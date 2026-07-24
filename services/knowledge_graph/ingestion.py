"""
Document ingestion for knowledge base with relationship analysis
PM-007 Enhancement: Dynamic knowledge hierarchy and relationships
"""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import chromadb
import pypdf
import structlog
from chromadb.utils import embedding_functions

from services.configuration.piper_config_loader import piper_config_loader
from services.infrastructure.keychain_service import KeychainService

logger = structlog.get_logger()


class DocumentIngester:
    """Handles document upload and processing into vector database with relationship analysis"""

    def __init__(self, chroma_path: str = "./data/chromadb"):
        self.chroma_path = chroma_path
        self.client = chromadb.PersistentClient(path=chroma_path)
        # #1452: embedding function + collection are LAZY. Eager construction
        # raised in keyless environments (OpenAIEmbeddingFunction requires a
        # key at __init__), and DocumentIngester sits in the dependency graph
        # of surfaces that never embed (radar's build_entity_sources ->
        # DocumentService) — a keyless server 500'd its whole radar feed.
        # Same operation-boundary principle as the document_handlers fix.
        self._embedding_function = None
        self._collection = None

    @property
    def embedding_function(self):
        if self._embedding_function is None:
            # Get OpenAI API key from keychain (not environment variables)
            keychain = KeychainService()
            api_key = keychain.get_api_key("openai")

            # Use OpenAI embeddings
            self._embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                api_key=api_key, model_name="text-embedding-ada-002"
            )
        return self._embedding_function

    @property
    def collection(self):
        if self._collection is None:
            # Create or get the PM knowledge collection
            self._collection = self.client.get_or_create_collection(
                name="pm_knowledge",
                embedding_function=self.embedding_function,
                metadata={
                    "description": "Product Management knowledge base with relationships"
                },
            )
            logger.info(
                f"Knowledge collection initialized with {self._collection.count()} documents"
            )
        return self._collection

    @property
    def llm(self):
        """Lazy-load LLM service from ServiceContainer if not injected.

        DEPRECATION WARNING (Issue #322):
        Direct ServiceContainer() access is deprecated. Pass llm_service
        via constructor instead. This fallback will be removed when
        horizontal scaling is enabled.
        """
        if not hasattr(self, "_llm") or self._llm is None:
            import warnings

            from services.container import ServiceContainer

            warnings.warn(
                "DocumentIngester: Direct ServiceContainer() access is deprecated. "
                "Pass llm_service via constructor. (Issue #322 - ARCH-FIX-SINGLETON)",
                DeprecationWarning,
                stacklevel=2,
            )
            container = ServiceContainer()
            self._llm = container.get_service("llm")
        return self._llm

    async def _analyze_document_relationships(self, content: str, existing_metadata: Dict) -> Dict:
        """Use LLM to analyze document relationships and hierarchy"""

        prompt = f"""Analyze this PM document and extract relationship metadata.

Document content (first 800 chars): {content[:800]}

Return JSON with:
{{
    "main_concepts": ["concept1", "concept2"],
    "document_type": "bug_report|user_story|architecture|process|meeting_notes|requirements|retrospective",
    "project_area": "specific project or feature name",
    "hierarchy_level": 1-4,
    "related_keywords": ["keyword1", "keyword2"],
    "stakeholder_types": ["developers", "users", "product", "design", "qa"],
    "complexity_level": "low|medium|high",
    "urgency_indicators": ["urgent", "critical", "nice-to-have"],
    "feature_areas": ["authentication", "ui", "api", "performance"]
}}

Hierarchy levels:
1 = General PM practices/methodology
2 = Business/project context
3 = Feature/component specific
4 = Implementation details

Be specific and concise. Extract real concepts from the content."""

        try:
            response = await self.llm.complete(
                task_type="relationship_analysis",
                prompt=prompt,
                context=existing_metadata,
                system=piper_config_loader.get_system_prompt(),
            )

            parsed = json.loads(response)

            # Merge with existing metadata
            relationship_metadata = {
                **existing_metadata,
                "main_concepts": parsed.get("main_concepts", []),
                "document_type": parsed.get("document_type", "unknown"),
                "project_area": parsed.get("project_area", "general"),
                "hierarchy_level": parsed.get("hierarchy_level", 2),
                "related_keywords": parsed.get("related_keywords", []),
                "stakeholder_types": parsed.get("stakeholder_types", []),
                "complexity_level": parsed.get("complexity_level", "medium"),
                "urgency_indicators": parsed.get("urgency_indicators", []),
                "feature_areas": parsed.get("feature_areas", []),
                "relationship_analysis_version": "1.0",
                "analysis_timestamp": datetime.now().isoformat(),
            }

            logger.info(
                f"Relationship analysis complete. Type: {relationship_metadata['document_type']}, Level: {relationship_metadata['hierarchy_level']}"
            )
            return relationship_metadata

        except Exception as e:
            logger.warning(f"Relationship analysis failed, using basic metadata: {e}")
            return {
                **existing_metadata,
                "hierarchy_level": 2,  # Default to project level
                "document_type": "unknown",
                "main_concepts": [],
                "related_keywords": [],
                "relationship_analysis_version": "fallback",
            }

    async def ingest_pdf(self, file_path: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Ingest a PDF document into the knowledge base with relationship analysis

        Args:
            file_path: Path to the PDF file
            metadata: Additional metadata (title, author, source_type, etc.)

        Returns:
            Summary of ingestion results
        """
        start_time = datetime.now()
        metadata = metadata or {}

        # Extract text from PDF
        logger.info(f"Starting PDF ingestion with relationship analysis: {file_path}")
        chunks = self._extract_pdf_chunks(file_path)

        # NEW: Analyze first chunk for document-level relationships

        enhanced_metadata = metadata

        if chunks:
            logger.info("Analyzing document relationships...")

            enhanced_metadata = await self._analyze_document_relationships(chunks[0], metadata)

        # Generate document ID based on content hash
        doc_hash = hashlib.md5(open(file_path, "rb").read()).hexdigest()[:8]
        base_id = f"pdf_{doc_hash}"

        # NEW: Analyze first chunk for document-level relationships
        enhanced_metadata = metadata
        if chunks:
            logger.info("Analyzing document relationships...")
            enhanced_metadata = await self._analyze_document_relationships(chunks[0], metadata)

        # Prepare documents for ChromaDB
        documents = []
        metadatas = []
        ids = []

        for i, chunk in enumerate(chunks):
            # Skip empty chunks
            if not chunk.strip():
                continue

            # Serialize list metadata for ChromaDB compatibility
            serialized_metadata = {}
            for key, value in enhanced_metadata.items():
                if value is None:
                    serialized_metadata[key] = ""  # Convert None to empty string
                elif isinstance(value, list):
                    serialized_metadata[key] = json.dumps(value)
                else:
                    serialized_metadata[key] = value

            chunk_metadata = {
                **serialized_metadata,  # Use serialized enhanced metadata
                "source": file_path,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "ingested_at": datetime.now().isoformat(),
            }

            documents.append(chunk)
            metadatas.append(chunk_metadata)
            ids.append(f"{base_id}_chunk_{i}")

        # Add to ChromaDB
        if documents:
            self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
            logger.info(f"Added {len(documents)} chunks with enhanced metadata to knowledge base")

        # Return summary
        duration = (datetime.now() - start_time).total_seconds()
        return {
            "status": "success",
            "file": file_path,
            "chunks_created": len(documents),
            "document_id": base_id,
            "duration_seconds": duration,
            "metadata": enhanced_metadata,
            "relationship_analysis": {
                "document_type": enhanced_metadata.get("document_type", "unknown"),
                "hierarchy_level": enhanced_metadata.get("hierarchy_level", 2),
                "main_concepts": enhanced_metadata.get("main_concepts", []),
                "project_area": enhanced_metadata.get("project_area", "general"),
            },
        }

    def _extract_pdf_chunks(self, file_path: str, chunk_size: int = 1000) -> List[str]:
        """Extract text from PDF and split into chunks"""
        chunks = []

        try:
            with open(file_path, "rb") as file:
                pdf_reader = pypdf.PdfReader(file)

                # Extract text from all pages
                full_text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    full_text += text + "\n"

                # Split into chunks with overlap
                words = full_text.split()
                chunk_overlap = 200  # words

                for i in range(0, len(words), chunk_size - chunk_overlap):
                    chunk = " ".join(words[i : i + chunk_size])
                    chunks.append(chunk)

        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            raise

        return chunks

    async def search_with_context(
        self,
        query: str,
        project_filter: str = None,
        hierarchy_preference: int = None,
        n_results: int = 5,
    ) -> List[Dict]:
        """Context-aware search using relationship metadata"""

        # Build filter criteria
        where_clause = {}
        if project_filter:
            where_clause["project_area"] = project_filter
        if hierarchy_preference:
            where_clause["hierarchy_level"] = {"$lte": hierarchy_preference}

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results * 2,  # Get more, then filter
            where=where_clause if where_clause else None,
        )

        # Score results by relevance + relationship strength
        scored_results = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i] if results["metadatas"] else {}

                # Calculate relationship score
                rel_score = self._calculate_relationship_score(query, metadata)

                scored_results.append(
                    {
                        "content": doc,
                        "metadata": metadata,
                        "distance": (results["distances"][0][i] if results["distances"] else 0),
                        "relationship_score": rel_score,
                        "combined_score": (1 - results["distances"][0][i]) * rel_score,
                        "id": results["ids"][0][i] if results["ids"] else "",
                    }
                )

        # Sort by combined score and return top results
        scored_results.sort(key=lambda x: x["combined_score"], reverse=True)
        return scored_results[:n_results]

    def _calculate_relationship_score(self, query: str, metadata: Dict) -> float:
        """Calculate relationship relevance score"""
        score = 1.0

        query_lower = query.lower()

        # Boost for concept matches
        concepts = metadata.get("main_concepts", [])
        for concept in concepts:
            if concept.lower() in query_lower:
                score += 0.3

        # Boost for keyword matches
        keywords = metadata.get("related_keywords", [])
        for keyword in keywords:
            if keyword.lower() in query_lower:
                score += 0.2

        # Boost for feature area matches
        feature_areas = metadata.get("feature_areas", [])
        for area in feature_areas:
            if area.lower() in query_lower:
                score += 0.25

        # Hierarchy preference (more specific = higher score for specific queries)
        hierarchy = metadata.get("hierarchy_level", 2)
        if len(query.split()) > 5:  # Specific query
            score += (4 - hierarchy) * 0.1
        else:  # General query
            score += (hierarchy - 1) * 0.1

        return min(score, 2.0)  # Cap at 2x

    async def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Legacy search method - maintained for backward compatibility
        Now uses enhanced search with context
        """
        return await self.search_with_context(query, n_results=n_results)


# Create singleton instance - but lazy initialize
_ingester = None


def get_ingester():
    """Lazy initialization of DocumentIngester"""
    global _ingester
    if _ingester is None:
        _ingester = DocumentIngester()
    return _ingester
