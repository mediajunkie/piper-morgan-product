"""
PlaceService - Transform integration data into Place domain objects.

Issue #684: MUX-NAV-PLACES
ADR-045: Object Model (FEDERATED category)
ownership-metaphors.md: "I see this in {place}"

This service:
- Wraps existing integrations (GitHub, Calendar)
- Transforms raw data into consciousness-preserving Place objects
- Manages confidence based on data freshness
- Provides trust-gated filtering for visibility

Example:
    service = PlaceService(github_router, calendar_service)
    places = await service.get_visible_places(trust_stage=3)
    # Returns [Place(name="piper-morgan", summary="I see 3 PRs waiting", ...)]
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from services.domain.models import Place
from services.shared_types import HardnessLevel, PlaceConfidence, PlaceType, TrustStage


class PlaceService:
    """
    Transform integration data into Place domain objects.

    Responsibilities:
    - Query integrations for current state
    - Transform responses into Place objects with anti-flattening language
    - Calculate confidence based on freshness
    - Filter by trust stage for visibility
    """

    # Trust-gated visibility: PlaceType -> minimum HardnessLevel
    PLACE_HARDNESS: Dict[PlaceType, HardnessLevel] = {
        PlaceType.ISSUE_TRACKING: HardnessLevel.HARD,  # Stage 3+
        PlaceType.COMMUNICATION: HardnessLevel.MEDIUM,  # Stage 3+
        PlaceType.TEMPORAL: HardnessLevel.HARD,  # Stage 3+
        PlaceType.DOCUMENTATION: HardnessLevel.SOFT,  # Stage 4+
    }

    def __init__(
        self,
        github_router: Optional[Any] = None,
        calendar_service: Optional[Any] = None,
    ):
        """
        Initialize with integration services.

        Args:
            github_router: GitHubIntegrationRouter instance (optional)
            calendar_service: CalendarService instance (optional)
        """
        self.github_router = github_router
        self.calendar_service = calendar_service

    async def get_github_place(self, repo_name: Optional[str] = None) -> Optional[Place]:
        """
        Transform GitHub data into a Place.

        Issue #1042: ``repo_name`` no longer defaults to "piper-morgan". If
        not passed, the router resolves via ``repo_resolver`` and the
        Place's identifier reflects the resolved repo (or "github" generic).

        Args:
            repo_name: Repository name for identification (optional;
                router resolves if not provided)

        Returns:
            Place with ISSUE_TRACKING type, or None if unavailable
        """
        if not self.github_router:
            return None

        try:
            # Get open issues from GitHub (router resolves repo internally if
            # not passed via owner/repo kwargs)
            issues = await self.github_router.get_open_issues(limit=20)

            # Calculate summary using Piper's perspective
            issue_count = len(issues)
            if issue_count == 0:
                summary = "I see no open issues right now"
            elif issue_count == 1:
                summary = "I see 1 open issue"
            else:
                summary = f"I see {issue_count} open issues"

            # Try to get PR count if available
            try:
                prs = await self.github_router.get_open_prs(limit=20)
                pr_count = len(prs) if prs else 0
                if pr_count > 0:
                    summary += f" and {pr_count} PR{'s' if pr_count > 1 else ''} waiting for review"
            except (AttributeError, Exception):
                # PR method not available, skip
                pass

            # Build Place URL/name from resolved repo if available, else
            # fall back to a generic GitHub-place identity (Issue #1042: no
            # hardcoded mediajunkie/piper-morgan-product URL).
            resolved_name = repo_name or "github"
            if issues and isinstance(issues[0], dict) and issues[0].get("repository"):
                resolved_name = issues[0]["repository"]
            source_url = (
                f"https://github.com/{resolved_name}"
                if "/" in resolved_name
                else "https://github.com"
            )

            return Place(
                id=f"github-{resolved_name}",
                place_type=PlaceType.ISSUE_TRACKING,
                name=f"{resolved_name} repository" if "/" in resolved_name else "GitHub",
                confidence=PlaceConfidence.HIGH,
                summary=summary,
                source_url=source_url,
                hardness=self.PLACE_HARDNESS[PlaceType.ISSUE_TRACKING],
                details={"issues": issues[:5]},  # Include top 5 for expansion
                last_fetched=datetime.now(timezone.utc),
            )

        except Exception as e:
            # Return low-confidence Place on error (Issue #1042: no hardcoded
            # URL fallback)
            fallback_name = repo_name or "github"
            return Place(
                id=f"github-{fallback_name}",
                place_type=PlaceType.ISSUE_TRACKING,
                name=f"{fallback_name} repository" if "/" in fallback_name else "GitHub",
                confidence=PlaceConfidence.LOW,
                summary="I couldn't reach GitHub right now",
                source_url="https://github.com",
                hardness=self.PLACE_HARDNESS[PlaceType.ISSUE_TRACKING],
                details={"error": str(e)},
                last_fetched=datetime.now(timezone.utc),
            )

    async def get_calendar_place(self) -> Optional[Place]:
        """
        Transform Calendar data into a Place.

        Returns:
            Place with TEMPORAL type, or None if unavailable
        """
        if not self.calendar_service:
            return None

        try:
            # Get today's events
            events = await self.calendar_service.get_todays_events()

            # Calculate summary using Piper's perspective
            event_count = len(events) if events else 0
            if event_count == 0:
                summary = "I see no meetings on your calendar today"
            elif event_count == 1:
                summary = "I see 1 meeting on your calendar today"
            else:
                summary = f"I see {event_count} meetings on your calendar today"

            return Place(
                id="calendar-today",
                place_type=PlaceType.TEMPORAL,
                name="your calendar",
                confidence=PlaceConfidence.HIGH,
                summary=summary,
                source_url="https://calendar.google.com",
                hardness=self.PLACE_HARDNESS[PlaceType.TEMPORAL],
                details={"events": events[:5] if events else []},
                last_fetched=datetime.now(timezone.utc),
            )

        except Exception as e:
            return Place(
                id="calendar-today",
                place_type=PlaceType.TEMPORAL,
                name="your calendar",
                confidence=PlaceConfidence.LOW,
                summary="I couldn't reach your calendar right now",
                source_url="https://calendar.google.com",
                hardness=self.PLACE_HARDNESS[PlaceType.TEMPORAL],
                details={"error": str(e)},
                last_fetched=datetime.now(timezone.utc),
            )

    async def get_all_places(self) -> List[Place]:
        """
        Get all configured Places.

        Returns:
            List of Place objects from all available integrations
        """
        places = []

        github_place = await self.get_github_place()
        if github_place:
            places.append(github_place)

        calendar_place = await self.get_calendar_place()
        if calendar_place:
            places.append(calendar_place)

        return places

    def filter_by_trust(self, places: List[Place], trust_stage: TrustStage) -> List[Place]:
        """
        Filter Places by trust stage visibility.

        Uses HardnessLevel to determine minimum trust stage for visibility:
        - HARDEST (5): Always visible (Stage 1+)
        - HARD (4): Stage 3+
        - MEDIUM (3): Stage 3+
        - SOFT (2): Stage 4+
        - SOFTEST (1): Stage 4+

        Args:
            places: List of Places to filter
            trust_stage: Current user's trust stage

        Returns:
            Places visible at the given trust stage
        """
        visible = []
        for place in places:
            min_stage = self._get_min_trust_stage(place.hardness)
            if trust_stage.value >= min_stage:
                visible.append(place)
        return visible

    def _get_min_trust_stage(self, hardness: HardnessLevel) -> int:
        """
        Convert hardness to minimum trust stage.

        Matches logic from #419 (Home State) and #420 (Nav Utility).
        """
        if hardness.value >= 5:  # HARDEST
            return 1
        if hardness.value >= 4:  # HARD
            return 3
        if hardness.value >= 3:  # MEDIUM
            return 3
        # SOFT or SOFTEST
        return 4

    async def get_visible_places(self, trust_stage: TrustStage) -> List[Place]:
        """
        Get Places visible at the given trust stage.

        Convenience method combining get_all_places() and filter_by_trust().

        Args:
            trust_stage: Current user's trust stage

        Returns:
            Places visible to user at their trust level
        """
        all_places = await self.get_all_places()
        return self.filter_by_trust(all_places, trust_stage)
