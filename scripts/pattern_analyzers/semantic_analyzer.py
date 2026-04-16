"""
Semantic Analysis - Term emergence and concept evolution tracking.

Detects:
- New concept/terminology first appearance
- Growth rate of concept usage over time
- Context classification (ADR, omnibus, code, tests)
- Cross-validation (concepts appearing in multiple contexts)
- Concept clusters (related terms emerging together)
"""

import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from git import Repo

from .base import BaseAnalyzer, BreakthroughSignal


class SemanticAnalyzer(BaseAnalyzer):
    """
    Analyzes semantic patterns - what concepts emerge and how they evolve.

    Tracks term frequency over time, classifies context, and detects
    concept emergence as signals of methodological or architectural breakthroughs.
    """

    def __init__(self, project_root: Path):
        super().__init__(project_root)
        self.repo = Repo(project_root)

        # Key concept patterns to track (can be extended)
        self.key_concepts = {
            # Architectural patterns
            "ActionHumanizer",
            "EnhancedErrorMiddleware",
            "BreakthroughDetector",
            "SerenaPatternAnalyzer",
            "AsyncSessionFactory",
            "WorkflowFactory",
            # Methodological patterns
            "75% pattern",
            "archaeological investigation",
            "Phase -1",
            "Anti-80% Protocol",
            "completion matrix",
            "CODE ≠ DATA",
            # Coordination patterns
            "parallel execution",
            "multi-agent coordination",
            "cross-validation",
            "handoff pattern",
            # Spatial/intelligence patterns
            "spatial intelligence",
            "boundary enforcement",
            "granular adapter",
            # Quality patterns
            "systematic verification",
            "verification-first",
            "evidence-based",
        }

    async def analyze(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Run semantic analysis for specified time period.

        Returns:
            Dict with keys:
            - term_emergence: New concepts that appeared
            - term_evolution: How concept usage changed over time
            - context_classification: Where concepts appear
            - validation_scores: Cross-context validation
            - concept_clusters: Related concepts emerging together
        """
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=30)

        # Track term emergence and evolution
        term_timeline = self._build_term_timeline(start_date, end_date)

        # Detect new concepts (first appearances)
        term_emergence = self._detect_term_emergence(term_timeline, start_date)

        # Calculate growth rates
        term_evolution = self._analyze_term_evolution(term_timeline)

        # Classify contexts (ADR, omnibus, code, etc.)
        context_classification = self._classify_term_contexts(term_timeline)

        # Calculate validation scores (cross-context appearances)
        validation_scores = self._calculate_validation_scores(context_classification)

        # Detect concept clusters (related terms emerging together)
        concept_clusters = self._detect_concept_clusters(term_emergence, term_timeline)

        self.results = {
            "term_emergence": term_emergence,
            "term_evolution": term_evolution,
            "context_classification": context_classification,
            "validation_scores": validation_scores,
            "concept_clusters": concept_clusters,
            "analysis_period": {
                "start": self._format_date(start_date),
                "end": self._format_date(end_date),
            },
        }

        return self.results

    def _build_term_timeline(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Build timeline of term appearances across all text files.

        Returns:
            Dict mapping term -> list of occurrences with metadata
        """
        term_timeline = defaultdict(list)

        # Scan markdown files (omnibus logs, ADRs, session logs)
        md_files = list(self.project_root.glob("docs/**/*.md")) + list(
            self.project_root.glob("dev/**/*.md")
        )

        for file_path in md_files:
            try:
                content = file_path.read_text(encoding="utf-8")

                # Get file modification time as approximate date
                file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)

                # Skip files outside date range
                if not (start_date <= file_mtime <= end_date):
                    continue

                # Classify file context
                context = self._classify_file_context(file_path)

                # Search for key concepts
                for term in self.key_concepts:
                    # Case-insensitive search
                    pattern = re.compile(re.escape(term), re.IGNORECASE)
                    matches = pattern.findall(content)

                    if matches:
                        term_timeline[term].append(
                            {
                                "date": self._format_date(file_mtime),
                                "file": str(file_path.relative_to(self.project_root)),
                                "count": len(matches),
                                "context": context,
                            }
                        )

            except (UnicodeDecodeError, PermissionError):
                continue

        # Also scan Python files for architectural patterns
        py_files = list(self.project_root.glob("services/**/*.py")) + list(
            self.project_root.glob("web/**/*.py")
        )

        for file_path in py_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)

                if not (start_date <= file_mtime <= end_date):
                    continue

                # Only check architectural pattern terms in code
                architectural_terms = {
                    "ActionHumanizer",
                    "EnhancedErrorMiddleware",
                    "AsyncSessionFactory",
                    "WorkflowFactory",
                }

                for term in architectural_terms:
                    if term in content:
                        term_timeline[term].append(
                            {
                                "date": self._format_date(file_mtime),
                                "file": str(file_path.relative_to(self.project_root)),
                                "count": content.count(term),
                                "context": "code",
                            }
                        )

            except (UnicodeDecodeError, PermissionError):
                continue

        return term_timeline

    def _classify_file_context(self, file_path: Path) -> str:
        """
        Classify file into context type.

        Returns: "adr", "omnibus", "session_log", "doc", "code", "test"
        """
        path_str = str(file_path).lower()

        if "adr-" in path_str or "/adrs/" in path_str:
            return "adr"
        elif "omnibus-log" in path_str or "/omnibus-logs/" in path_str:
            return "omnibus"
        elif "-log.md" in path_str or "/dev/2025/" in path_str:
            return "session_log"
        elif path_str.endswith(".py"):
            if "/test" in path_str:
                return "test"
            return "code"
        elif path_str.endswith(".md"):
            return "doc"
        else:
            return "unknown"

    def _detect_term_emergence(
        self, term_timeline: Dict[str, List[Dict[str, Any]]], start_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Detect terms that first appeared in the analysis period.

        Returns:
            List of emerged concepts with first appearance data
        """
        emergent_terms = []

        for term, occurrences in term_timeline.items():
            if not occurrences:
                continue

            # Sort by date
            sorted_occurrences = sorted(occurrences, key=lambda x: x["date"])
            first_occurrence = sorted_occurrences[0]
            first_date = self._parse_date(first_occurrence["date"])

            # Check if first appearance is in our analysis period
            if first_date >= start_date:
                total_occurrences = sum(occ["count"] for occ in occurrences)
                contexts = set(occ["context"] for occ in occurrences)

                emergent_terms.append(
                    {
                        "term": term,
                        "first_seen": first_occurrence["date"],
                        "first_seen_in": first_occurrence["file"],
                        "first_context": first_occurrence["context"],
                        "total_occurrences": total_occurrences,
                        "spread": len(occurrences),  # Number of files
                        "contexts": list(contexts),
                    }
                )

        return sorted(emergent_terms, key=lambda x: x["total_occurrences"], reverse=True)

    def _analyze_term_evolution(
        self, term_timeline: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculate growth rate and evolution metrics for each term.

        Returns:
            Dict mapping term -> evolution metrics
        """
        evolution = {}

        for term, occurrences in term_timeline.items():
            if len(occurrences) < 2:
                continue

            # Sort by date
            sorted_occurrences = sorted(occurrences, key=lambda x: x["date"])

            # Calculate growth rate (early vs late occurrences)
            mid_point = len(sorted_occurrences) // 2
            early_count = sum(occ["count"] for occ in sorted_occurrences[:mid_point])
            late_count = sum(occ["count"] for occ in sorted_occurrences[mid_point:])

            if early_count > 0:
                growth_rate = (late_count - early_count) / early_count
            else:
                growth_rate = float("inf") if late_count > 0 else 0.0

            # Calculate spread velocity (files per day)
            first_date = self._parse_date(sorted_occurrences[0]["date"])
            last_date = self._parse_date(sorted_occurrences[-1]["date"])
            days = max(1, (last_date - first_date).days)
            spread_velocity = len(occurrences) / days

            evolution[term] = {
                "growth_rate": growth_rate,
                "spread_velocity": spread_velocity,
                "total_occurrences": sum(occ["count"] for occ in occurrences),
                "file_count": len(occurrences),
                "first_seen": sorted_occurrences[0]["date"],
                "last_seen": sorted_occurrences[-1]["date"],
                "trend": (
                    "rapid_growth"
                    if growth_rate > 2.0
                    else "growing"
                    if growth_rate > 0.5
                    else "stable"
                ),
            }

        return evolution

    def _classify_term_contexts(
        self, term_timeline: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Dict[str, int]]:
        """
        Count term appearances by context type.

        Returns:
            Dict mapping term -> {context: count}
        """
        classification = {}

        for term, occurrences in term_timeline.items():
            context_counts = Counter(occ["context"] for occ in occurrences)
            classification[term] = dict(context_counts)

        return classification

    def _calculate_validation_scores(
        self, context_classification: Dict[str, Dict[str, int]]
    ) -> Dict[str, float]:
        """
        Calculate validation scores based on cross-context appearances.

        A term appearing in multiple contexts (ADR + code + omnibus) is
        more validated than one appearing in only one context.

        Returns:
            Dict mapping term -> validation score (0.0 to 1.0)
        """
        scores = {}

        key_contexts = {"adr", "omnibus", "code"}

        for term, contexts in context_classification.items():
            # Count how many key contexts this term appears in
            present_contexts = set(contexts.keys()) & key_contexts
            score = len(present_contexts) / len(key_contexts)
            scores[term] = score

        return scores

    def _detect_concept_clusters(
        self,
        term_emergence: List[Dict[str, Any]],
        term_timeline: Dict[str, List[Dict[str, Any]]],
    ) -> List[Dict[str, Any]]:
        """
        Detect clusters of related concepts emerging together.

        Concepts appearing in the same files around the same time
        are likely related (e.g., "ActionHumanizer" + "EnhancedErrorMiddleware").

        Returns:
            List of concept clusters with member terms
        """
        clusters = []

        # Group emergent terms by date (within 7 days = same cluster)
        date_groups = defaultdict(list)

        for term_data in term_emergence:
            first_date = self._parse_date(term_data["first_seen"])
            date_key = first_date.date().isoformat()[:7]  # YYYY-MM
            date_groups[date_key].append(term_data["term"])

        # Create clusters for groups with 2+ terms
        for date_key, terms in date_groups.items():
            if len(terms) >= 2:
                # Find common files
                term_files = {
                    term: set(occ["file"] for occ in term_timeline[term]) for term in terms
                }

                # Calculate file overlap
                all_files = set.union(*term_files.values())
                common_files = set.intersection(*term_files.values())

                clusters.append(
                    {
                        "period": date_key,
                        "terms": terms,
                        "term_count": len(terms),
                        "common_files": list(common_files),
                        "cohesion": len(common_files) / len(all_files) if all_files else 0,
                    }
                )

        return sorted(clusters, key=lambda c: c["term_count"], reverse=True)

    def get_breakthrough_signals(self) -> Dict[BreakthroughSignal, Any]:
        """
        Extract breakthrough signals from semantic analysis.

        Returns:
            Dict mapping signal types to evidence
        """
        if not self.results:
            return {}

        signals = {}

        # Semantic emergence signal
        term_emergence = self.results.get("term_emergence", [])
        if term_emergence:
            # Significant if 3+ concepts emerged
            if len(term_emergence) >= 3:
                # Extract dates from emergent terms
                emergence_dates = [t["first_seen"].split("T")[0] for t in term_emergence]

                signals[BreakthroughSignal.SEMANTIC_EMERGENCE] = {
                    "count": len(term_emergence),
                    "concepts": [t["term"] for t in term_emergence],
                    "contexts": list(
                        set(ctx for t in term_emergence for ctx in t.get("contexts", []))
                    ),
                    "dates": emergence_dates,
                    "events": [
                        {"date": t["first_seen"], "term": t["term"]} for t in term_emergence
                    ],
                }

        # Architectural insight signal (high-validation terms)
        validation_scores = self.results.get("validation_scores", {})
        high_validation_terms = [
            term for term, score in validation_scores.items() if score >= 0.67
        ]  # 2+ contexts

        if high_validation_terms:
            # Get dates for high-validation terms from term_emergence
            term_dates = {t["term"]: t["first_seen"].split("T")[0] for t in term_emergence}
            insight_dates = [
                term_dates.get(term, "") for term in high_validation_terms if term in term_dates
            ]

            signals[BreakthroughSignal.ARCHITECTURAL_INSIGHT] = {
                "count": len(high_validation_terms),
                "validated_concepts": high_validation_terms,
                "avg_validation": sum(validation_scores[t] for t in high_validation_terms)
                / len(high_validation_terms),
                "dates": insight_dates if insight_dates else [],
                "events": [
                    {"date": term_dates.get(term, ""), "term": term}
                    for term in high_validation_terms
                    if term in term_dates
                ],
            }

        return signals
