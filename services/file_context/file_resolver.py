"""Intelligent file reference resolution"""

import logging
import os
import re
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from services.domain.models import Intent, UploadedFile
from services.repositories.file_repository import FileRepository

from .exceptions import AmbiguousFileReferenceError, NoFilesFoundError

# Import centralized configuration service
try:
    from services.infrastructure.config.mcp_configuration import get_config

    CONFIG_SERVICE_AVAILABLE = True
except ImportError:
    CONFIG_SERVICE_AVAILABLE = False

logger = logging.getLogger(__name__)


# Filename-shaped tokens a user types to name a specific document
# ("summarize artifact-8b029c94.md", "summarize q3-roadmap.pdf"). Extension
# list is deliberately conservative — only types the product actually stores
# or projects (#1657).
_FILENAME_TOKEN_RE = re.compile(
    r"(?<![\w.-])[\w-]+\.(?:pdf|docx?|txt|md|markdown|csv|tsv|xlsx?|pptx?|json)(?![\w.-])",
    re.IGNORECASE,
)


class FileResolver:
    """Intelligent file reference resolution

    #1657: resolution candidates are the SAME set the Files listing shows —
    uploaded_files ∪ the owner's generated artifacts (#355: /files is a view
    over both). Pass an ArtifactRepository to include artifacts; without one
    the resolver is uploads-only (legacy callers/tests unchanged).
    """

    def __init__(self, file_repository: FileRepository, artifact_repository=None):
        self.repo = file_repository
        self.artifact_repo = artifact_repository

        # File type preferences for different intent actions
        self.file_type_preferences = {
            "analyze_report": [
                "application/pdf",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ],
            "analyze_data": [
                "text/csv",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "application/json",
            ],
            "review_document": [
                "application/pdf",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "text/plain",
            ],
            "process_spreadsheet": [
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "text/csv",
            ],
            "create_presentation": [
                "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                "application/vnd.ms-powerpoint",
            ],
            "ingest_generic": [],  # No preference, accept any
        }

    async def resolve_file_reference(
        self, intent: Intent, session_id: str
    ) -> Tuple[Optional[str], float]:
        """
        Resolve file reference with confidence score
        Returns: (file_id, confidence) or (None, 0.0)
        """
        original_message = intent.context.get("original_message", "").lower()

        # Check for temporal references that might span sessions
        temporal_patterns = [
            r"\b(few days ago|days ago|yesterday|last week|earlier|previously|before|recently)\b",
            r"\b(uploaded.*ago|uploaded.*earlier|uploaded.*before|uploaded.*recently)\b",
            r"\b(just uploaded|I uploaded|I just uploaded|the file I uploaded)\b",
            r"\b(that file|the file|my file)\b",
        ]

        is_temporal_reference = any(
            re.search(pattern, original_message) for pattern in temporal_patterns
        )

        if is_temporal_reference:
            # For temporal references, search across sessions (but scoped to this user)
            files = await self.repo.get_recent_files_all_sessions(session_id, days=7)
            files = files + await self._artifact_candidates(session_id, days=7)
        else:
            # Get all files for the current session
            files = await self.repo.get_files_for_session(session_id, limit=20)
            files = files + await self._artifact_candidates(session_id)

        if not files:
            return None, 0.0

        # EXPLICIT FILENAME (#1657): the user typed a stored filename verbatim
        # ("summarize artifact-8b029c94.md"). An exact, unique match wins
        # outright — never routed through fuzzy scoring, where a hash-shaped
        # name loses to recency/type noise. And if the message names a
        # filename-shaped token that matches NO candidate, answer honestly
        # (None) instead of summarizing the best-scoring OTHER document.
        exact_matches = [
            f for f in files if f.filename and self._filename_in_message(f.filename, original_message)
        ]
        if len(exact_matches) == 1:
            return exact_matches[0].id, 0.98
        if len(exact_matches) > 1:
            raise AmbiguousFileReferenceError(exact_matches[:3], [0.98] * min(len(exact_matches), 3))
        if _FILENAME_TOKEN_RE.search(original_message):
            # A specific filename was named and nothing the user owns bears it.
            return None, 0.0

        # SPECIAL CASE: If only one file in session and explicit reference
        # ("the file", "that file", "file I uploaded"), use it with high confidence
        explicit_references = [
            "the file",
            "that file",
            "file i",
            "document i",
            "what i uploaded",
            "just uploaded",
        ]

        if len(files) == 1 and any(ref in original_message for ref in explicit_references):
            # Single file with explicit reference = no ambiguity
            return files[0].id, 0.95  # Very high confidence

        # Score each file
        scored_files = []
        for file in files:
            score = self._calculate_score(file, intent)
            scored_files.append((file, score))

        # Sort by score (highest first)
        scored_files.sort(key=lambda x: x[1], reverse=True)

        # Get the best match
        if not scored_files:
            return None, 0.0

        best_file, best_score = scored_files[0]

        # Check for ambiguity (multiple files with similar scores)
        if len(scored_files) > 1:
            second_best_score = scored_files[1][1]
            if best_score - second_best_score < 0.2:  # Close scores indicate ambiguity
                raise AmbiguousFileReferenceError(
                    [f for f, _ in scored_files[:3]],  # Top 3 candidates
                    [s for _, s in scored_files[:3]],
                )

        # Return result with confidence
        return best_file.id, best_score

    async def _artifact_candidates(self, owner_id: str, days: Optional[int] = None):
        """The owner's generated artifacts, projected into UploadedFile shape (#1657).

        Same owner-scoped set the /files listing shows (files.py #355 block:
        list_for_owner(owner, source_type="generated")) — never widened. With
        ``days``, mirrors the temporal path's recency cutoff.
        """
        if self.artifact_repo is None:
            return []
        from services.file_context.artifact_view import artifact_as_file_view

        try:
            artifacts = await self.artifact_repo.list_for_owner(
                owner_id, source_type="generated", limit=20
            )
        except Exception as e:
            # The listing degrades the same way (files.py: artifacts = []) —
            # an artifact-store hiccup must not take uploads resolution down.
            logger.error(f"Artifact candidate fetch failed for {owner_id}: {e}")
            return []
        views = [artifact_as_file_view(a) for a in artifacts]
        if days is not None:
            from services.utils.datetime_utils import ensure_utc, utc_now

            cutoff = utc_now() - timedelta(days=days)
            views = [
                v for v in views if v.upload_time and ensure_utc(v.upload_time) > cutoff
            ]
        return views

    @staticmethod
    def _filename_in_message(filename: str, message: str) -> bool:
        """True when the stored filename appears verbatim in the message,
        bounded so 'report.pdf' never matches inside 'old-report.pdf' (#1657)."""
        pattern = r"(?<![\w.-])" + re.escape(filename.lower()) + r"(?![\w.-])"
        return re.search(pattern, message.lower()) is not None

    def _calculate_score(self, file: UploadedFile, intent: Intent) -> float:
        """Multi-factor scoring algorithm with optional content relevance"""
        total_score = 0.0
        components = {}

        # Check if MCP content scoring is enabled
        if CONFIG_SERVICE_AVAILABLE:
            config = get_config()
            mcp_enabled = config.mcp_enabled
        else:
            mcp_enabled = os.getenv("ENABLE_MCP_FILE_SEARCH", "false").lower() == "true"

        if mcp_enabled:
            # With MCP content scoring: adjust weights to include content relevance
            # Factor 1: Recency (max 0.25)
            recency_score = self._calculate_recency_score(file.upload_time)
            components["recency"] = recency_score
            total_score += recency_score * 0.25

            # Factor 2: File type relevance (max 0.25)
            type_score = self._calculate_type_score(file.file_type, intent.action)
            components["type"] = type_score
            total_score += type_score * 0.25

            # Factor 3: Filename matching (max 0.15)
            name_score = self._calculate_name_score(file.filename, intent)
            components["name"] = name_score
            total_score += name_score * 0.15

            # Factor 4: Usage history (max 0.15)
            usage_score = self._calculate_usage_score(file)
            components["usage"] = usage_score
            total_score += usage_score * 0.15

            # Factor 5: Content relevance (max 0.2) - NEW
            content_score = self._calculate_content_score(file, intent)
            components["content"] = content_score
            total_score += content_score * 0.2
        else:
            # Without MCP: use original scoring weights
            # Factor 1: Recency (max 0.3)
            recency_score = self._calculate_recency_score(file.upload_time)
            components["recency"] = recency_score
            total_score += recency_score * 0.3

            # Factor 2: File type relevance (max 0.3)
            type_score = self._calculate_type_score(file.file_type, intent.action)
            components["type"] = type_score
            total_score += type_score * 0.3

            # Factor 3: Filename matching (max 0.2)
            name_score = self._calculate_name_score(file.filename, intent)
            components["name"] = name_score
            total_score += name_score * 0.2

            # Factor 4: Usage history (max 0.2)
            usage_score = self._calculate_usage_score(file)
            components["usage"] = usage_score
            total_score += usage_score * 0.2

        final_score = min(total_score, 1.0)  # Cap at 1.0

        # Debug logging
        logger.debug(f"Scoring {file.filename}: total={final_score:.3f}, components={components}")

        return final_score

    def _calculate_recency_score(self, upload_time: datetime) -> float:
        """Calculate recency score (0.0 to 1.0)"""
        if not upload_time:
            return 0.0

        # Issue #771: Use UTC for comparison - database now uses timestamptz
        from services.utils.datetime_utils import ensure_utc, utc_now

        now = utc_now()
        upload_utc = ensure_utc(upload_time)
        age = now - upload_utc

        # Last 5 minutes: full score
        if age <= timedelta(minutes=5):
            return 1.0

        # Decay over 1 hour
        if age <= timedelta(hours=1):
            minutes_old = age.total_seconds() / 60
            return max(0.0, 1.0 - (minutes_old / 60))

        # Very old files get minimal score
        return 0.1

    def _calculate_type_score(self, file_type: str, intent_action: str) -> float:
        """Calculate file type relevance score"""
        if not file_type or not intent_action:
            return 0.5  # Neutral score

        preferred_types = self.file_type_preferences.get(intent_action, [])

        if not preferred_types:
            return 0.5  # No preference, neutral score

        if file_type in preferred_types:
            return 1.0  # Perfect match

        # Check for partial matches (e.g., "pdf" in "application/pdf")
        file_extension = file_type.split("/")[-1] if "/" in file_type else file_type
        for preferred in preferred_types:
            if file_extension in preferred or preferred in file_type:
                return 0.7  # Partial match

        return 0.2  # Poor match

    def _calculate_name_score(self, filename: str, intent: Intent) -> float:
        """Calculate filename relevance score"""
        if not filename:
            return 0.0

        # Extract keywords from intent context and action
        keywords = []

        # Add action keywords
        action_keywords = intent.action.split("_")
        keywords.extend(action_keywords)

        # Add context keywords
        if intent.context:
            # Get the original message specifically, not the whole context dict
            original_message = intent.context.get("original_message", "")
            if original_message:
                context_text = original_message.lower()
                # Extract meaningful words (Unicode-aware regex)
                words = re.findall(r"\b\w{3,}\b", context_text)
                keywords.extend(words)

        if not keywords:
            return 0.5  # No keywords, neutral score

        # Check filename against keywords
        filename_lower = filename.lower()
        matches = 0
        for keyword in keywords:
            if keyword.lower() in filename_lower:
                matches += 1

        if matches == 0:
            return 0.1  # No matches

        # Score based on match ratio
        match_ratio = matches / len(keywords)
        return min(match_ratio, 1.0)

    def _calculate_usage_score(self, file: UploadedFile) -> float:
        """Calculate usage history score"""
        if not file.reference_count:
            return 0.5  # No usage history, neutral score

        # Recent references worth more
        recency_bonus = 0.0
        if file.last_referenced:
            # Issue #771: Use UTC for comparison - database now uses timestamptz
            from services.utils.datetime_utils import ensure_utc, utc_now

            now = utc_now()
            last_ref_utc = ensure_utc(file.last_referenced)
            age = now - last_ref_utc
            if age <= timedelta(hours=1):
                recency_bonus = 0.3
            elif age <= timedelta(hours=24):
                recency_bonus = 0.1

        # Base score from reference count (capped)
        base_score = min(file.reference_count / 10.0, 0.7)

        return min(base_score + recency_bonus, 1.0)

    def _calculate_content_score(self, file: UploadedFile, intent: Intent) -> float:
        """Calculate content relevance score using MCP (if enabled)"""
        # Check if MCP is enabled through configuration service
        if CONFIG_SERVICE_AVAILABLE:
            config = get_config()
            mcp_enabled = config.mcp_enabled
        else:
            mcp_enabled = os.getenv("ENABLE_MCP_FILE_SEARCH", "false").lower() == "true"

        if not mcp_enabled:
            return 0.5  # Neutral score if MCP disabled

        try:
            # Extract keywords from intent for content matching
            keywords = self._extract_content_keywords(intent)
            if not keywords:
                return 0.5  # Neutral score if no keywords

            # For now, use filename as proxy for content relevance
            # This is a simplified implementation that could be enhanced
            # with actual content analysis via MCP
            filename_lower = file.filename.lower()

            # Simple content relevance based on keyword matching
            keyword_matches = 0
            for keyword in keywords:
                if keyword.lower() in filename_lower:
                    keyword_matches += 1

            if keyword_matches == 0:
                return 0.2  # Low relevance

            # Score based on keyword density
            relevance_score = min(keyword_matches / len(keywords), 1.0)

            # Boost for exact matches
            if any(keyword.lower() == filename_lower.split(".")[0] for keyword in keywords):
                relevance_score = min(relevance_score * 1.5, 1.0)

            logger.debug(
                f"Content score for {file.filename}: {relevance_score:.3f} (matches: {keyword_matches})"
            )
            return relevance_score

        except Exception as e:
            logger.error(f"Content scoring failed for {file.filename}: {e}")
            return 0.5  # Neutral score on error

    def _extract_content_keywords(self, intent: Intent) -> List[str]:
        """Extract meaningful keywords from intent for content matching"""
        keywords = []

        # Extract from intent action
        if intent.action:
            action_words = intent.action.split("_")
            keywords.extend([word for word in action_words if len(word) > 2])

        # Extract from intent context
        if intent.context:
            original_message = intent.context.get("original_message", "")
            if original_message:
                # Extract meaningful words (3+ characters, alphanumeric)
                words = re.findall(r"\b[a-zA-Z0-9]{3,}\b", original_message.lower())

                # Filter out common words
                stop_words = {
                    "the",
                    "and",
                    "for",
                    "are",
                    "but",
                    "not",
                    "you",
                    "all",
                    "can",
                    "had",
                    "her",
                    "was",
                    "one",
                    "our",
                    "out",
                    "day",
                    "get",
                    "has",
                    "him",
                    "his",
                    "how",
                    "man",
                    "new",
                    "now",
                    "old",
                    "see",
                    "two",
                    "way",
                    "who",
                    "boy",
                    "did",
                    "its",
                    "let",
                    "put",
                    "say",
                    "she",
                    "too",
                    "use",
                    "with",
                    "that",
                    "this",
                    "have",
                    "from",
                    "they",
                    "know",
                    "want",
                    "been",
                    "good",
                    "much",
                    "some",
                    "time",
                    "very",
                    "when",
                    "come",
                    "here",
                    "just",
                    "like",
                    "long",
                    "make",
                    "many",
                    "over",
                    "such",
                    "take",
                    "than",
                    "them",
                    "well",
                    "were",
                }

                meaningful_words = [word for word in words if word not in stop_words]
                keywords.extend(meaningful_words)

        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for keyword in keywords:
            if keyword not in seen:
                unique_keywords.append(keyword)
                seen.add(keyword)

        return unique_keywords[:10]  # Limit to top 10 keywords

    async def get_resolution_suggestions(
        self, session_id: str, reference: str
    ) -> List[Tuple[UploadedFile, float]]:
        """Get file suggestions for ambiguous references"""
        files = await self.repo.get_files_for_session(session_id, limit=10)

        if not files:
            return []

        # Simple scoring based on filename similarity
        scored_files = []
        for file in files:
            # Simple fuzzy matching
            filename_lower = file.filename.lower()
            reference_lower = reference.lower()

            score = 0.0
            if reference_lower in filename_lower:
                score = 0.8
            elif any(word in filename_lower for word in reference_lower.split()):
                score = 0.5

            scored_files.append((file, score))

        # Sort by score and return top matches
        scored_files.sort(key=lambda x: x[1], reverse=True)
        return scored_files[:5]  # Top 5 suggestions
