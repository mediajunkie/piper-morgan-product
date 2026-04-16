"""
Notion Spatial Intelligence

Notion integration with full 8-dimensional spatial intelligence.
Built from day one following ADR-013 MCP + Spatial Intelligence pattern.

This class provides comprehensive spatial analysis of Notion entities,
mapping them to Piper Morgan's spatial metaphor system for enhanced
understanding and navigation of knowledge spaces.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

logger = logging.getLogger(__name__)


class NotionSpatialIntelligence:
    """
    Notion integration with full 8-dimensional spatial intelligence.

    Maps Notion entities to spatial positions using the established
    spatial metaphor system, providing cognitive understanding of:
    - Workspace structure and hierarchy
    - Content relationships and dependencies
    - Temporal patterns and workflows
    - Collaborative dynamics and priorities
    """

    def __init__(self):
        self.mcp_adapter = NotionIntegrationRouter()
        self._workspace_cache: Dict[str, Any] = {}
        self._database_cache: Dict[str, Any] = {}
        self._page_cache: Dict[str, Any] = {}
        self._spatial_analytics: Dict[str, Any] = {
            "workspaces_analyzed": 0,
            "databases_mapped": 0,
            "pages_processed": 0,
            "spatial_relationships": 0,
            "temporal_patterns": 0,
            "collaborative_insights": 0,
        }

        # 8-dimensional spatial analysis functions
        self.dimensions = {
            "HIERARCHY": self.analyze_page_structure,  # Nested pages/databases
            "TEMPORAL": self.analyze_timestamps,  # Last edited, created
            "PRIORITY": self.analyze_tags_status,  # Priority properties
            "COLLABORATIVE": self.analyze_authors,  # Who edited
            "FLOW": self.analyze_workflow_props,  # Status workflows
            "QUANTITATIVE": self.analyze_metrics,  # Number properties
            "CAUSAL": self.analyze_relations,  # Relation properties
            "CONTEXTUAL": self.analyze_workspace,  # Workspace context
        }

        logger.info("NotionSpatialIntelligence initialized")

    async def connect(self, integration_token: str) -> bool:
        """Connect to Notion workspace"""
        try:
            success = await self.mcp_adapter.connect(integration_token)
            if success:
                logger.info("NotionSpatialIntelligence connected successfully")
                # Initialize workspace analysis
                await self._analyze_workspace_structure()
            return success
        except Exception as e:
            logger.error(f"Error connecting NotionSpatialIntelligence: {e}")
            return False

    async def _analyze_workspace_structure(self):
        """Analyze workspace structure for spatial mapping"""
        try:
            workspace_info = await self.mcp_adapter.get_workspace_info()
            if workspace_info:
                self._workspace_cache = workspace_info
                self._spatial_analytics["workspaces_analyzed"] += 1
                logger.info(
                    f"Workspace structure analyzed: {workspace_info.get('workspace_name', 'Unknown')}"
                )
        except Exception as e:
            logger.error(f"Error analyzing workspace structure: {e}")

    async def analyze_page_structure(self, page_id: str) -> Dict[str, Any]:
        """
        Analyze page structure and hierarchy (HIERARCHY dimension)

        Maps Notion pages to spatial hierarchy:
        - Territory: Workspace
        - Room: Database or parent page
        - Path: Page hierarchy (parent-child relationships)
        - Object: Individual page with properties
        """
        try:
            page = await self.mcp_adapter.get_page(page_id)
            if not page:
                return {}

            # Get parent context
            parent_id = (
                page.get("properties", {}).get("Parent", {}).get("relation", [{}])[0].get("id")
            )
            parent_page = None
            if parent_id:
                parent_page = await self.mcp_adapter.get_page(parent_id)

            # Analyze hierarchy levels
            hierarchy_analysis = {
                "page_id": page_id,
                "page_title": page.get("title", "Untitled"),
                "hierarchy_level": 0,
                "parent_id": parent_id,
                "parent_title": parent_page.get("title", "Root") if parent_page else "Root",
                "has_children": False,  # Would need to query for children
                "spatial_position": {
                    "territory_id": self._workspace_cache.get("workspace_id"),
                    "room_id": parent_id or "root",
                    "path_id": page_id,
                    "object_position": None,
                },
            }

            # Map to spatial position
            spatial_context = {
                "territory_id": hierarchy_analysis["spatial_position"]["territory_id"],
                "room_id": hierarchy_analysis["spatial_position"]["room_id"],
                "path_id": hierarchy_analysis["spatial_position"]["path_id"],
                "attention_level": "medium",
                "navigation_intent": "explore",
            }

            position = self.mcp_adapter.map_to_position(page_id, spatial_context)
            hierarchy_analysis["spatial_position"]["object_position"] = position.position

            return hierarchy_analysis

        except Exception as e:
            logger.error(f"Error analyzing page structure for {page_id}: {e}")
            return {}

    async def analyze_timestamps(self, page_id: str) -> Dict[str, Any]:
        """
        Analyze temporal patterns (TEMPORAL dimension)

        Maps Notion timestamps to spatial temporal understanding:
        - Creation time patterns
        - Last edited frequency
        - Due date urgency
        - Temporal relationships between content
        """
        try:
            page = await self.mcp_adapter.get_page(page_id)
            if not page:
                return {}

            created_time = datetime.fromisoformat(
                page.get("created_time", "").replace("Z", "+00:00")
            )
            last_edited = datetime.fromisoformat(
                page.get("last_edited_time", "").replace("Z", "+00:00")
            )

            # Calculate temporal metrics
            time_since_creation = (datetime.now(created_time.tzinfo) - created_time).days
            time_since_edit = (datetime.now(last_edited.tzinfo) - last_edited).days

            # Analyze temporal patterns
            temporal_analysis = {
                "page_id": page_id,
                "created_time": page.get("created_time"),
                "last_edited_time": page.get("last_edited_time"),
                "time_since_creation_days": time_since_creation,
                "time_since_edit_days": time_since_edit,
                "edit_frequency": (
                    "high" if time_since_edit <= 1 else "medium" if time_since_edit <= 7 else "low"
                ),
                "content_freshness": (
                    "recent"
                    if time_since_edit <= 3
                    else "stale"
                    if time_since_edit > 30
                    else "current"
                ),
                "temporal_urgency": (
                    "high" if time_since_edit <= 1 else "medium" if time_since_edit <= 7 else "low"
                ),
            }

            # Check for due dates in properties
            properties = page.get("properties", {})
            if "Due Date" in properties:
                due_date = properties["Due Date"].get("date", {}).get("start")
                if due_date:
                    due_datetime = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
                    days_until_due = (due_datetime - datetime.now(due_datetime.tzinfo)).days
                    temporal_analysis["due_date"] = due_date
                    temporal_analysis["days_until_due"] = days_until_due
                    temporal_analysis["due_urgency"] = (
                        "overdue"
                        if days_until_due < 0
                        else "urgent"
                        if days_until_due <= 3
                        else "upcoming"
                    )

            return temporal_analysis

        except Exception as e:
            logger.error(f"Error analyzing timestamps for {page_id}: {e}")
            return {}

    async def analyze_tags_status(self, page_id: str) -> Dict[str, Any]:
        """
        Analyze priority and status signals (PRIORITY dimension)

        Maps Notion properties to spatial priority understanding:
        - Status properties (in progress, complete, etc.)
        - Priority levels (high, medium, low)
        - Importance tags and labels
        - Milestone significance
        """
        try:
            page = await self.mcp_adapter.get_page(page_id)
            if not page:
                return {}

            properties = page.get("properties", {})

            # Extract status and priority information
            status = properties.get("Status", {}).get("select", {}).get("name", "unknown")
            priority = properties.get("Priority", {}).get("select", {}).get("name", "medium")
            tags = properties.get("Tags", {}).get("multi_select", [])
            milestone = properties.get("Milestone", {}).get("checkbox", False)

            # Analyze priority signals
            priority_analysis = {
                "page_id": page_id,
                "status": status,
                "priority": priority,
                "tags": [tag.get("name") for tag in tags],
                "is_milestone": milestone,
                "priority_score": self._calculate_priority_score(status, priority, tags, milestone),
                "attention_required": self._determine_attention_level(status, priority, milestone),
                "workflow_stage": self._map_status_to_workflow(status),
            }

            return priority_analysis

        except Exception as e:
            logger.error(f"Error analyzing tags/status for {page_id}: {e}")
            return {}

    async def analyze_authors(self, page_id: str) -> Dict[str, Any]:
        """
        Analyze collaborative dynamics (COLLABORATIVE dimension)

        Maps Notion authorship to spatial collaborative understanding:
        - Content creators and editors
        - Team collaboration patterns
        - Review and approval workflows
        - Collaborative engagement levels
        """
        try:
            page = await self.mcp_adapter.get_page(page_id)
            if not page:
                return {}

            properties = page.get("properties", {})

            # Extract collaborative information
            created_by = properties.get("Created by", {}).get("people", [])
            last_edited_by = properties.get("Last edited by", {}).get("people", [])
            assignees = properties.get("Assignees", {}).get("people", [])
            reviewers = properties.get("Reviewers", {}).get("people", [])

            # Analyze collaborative patterns
            collaborative_analysis = {
                "page_id": page_id,
                "created_by": [person.get("name") for person in created_by],
                "last_edited_by": [person.get("name") for person in last_edited_by],
                "assignees": [person.get("name") for person in assignees],
                "reviewers": [person.get("name") for person in reviewers],
                "collaboration_level": self._determine_collaboration_level(
                    created_by, last_edited_by, assignees, reviewers
                ),
                "team_size": len(
                    set([p.get("id") for p in created_by + last_edited_by + assignees + reviewers])
                ),
                "ownership_clarity": (
                    "clear"
                    if len(assignees) == 1
                    else "shared"
                    if len(assignees) > 1
                    else "unassigned"
                ),
                "review_status": (
                    "pending"
                    if reviewers and not any(r.get("name") == "Approved" for r in reviewers)
                    else "approved"
                ),
            }

            return collaborative_analysis

        except Exception as e:
            logger.error(f"Error analyzing authors for {page_id}: {e}")
            return {}

    async def analyze_workflow_props(self, page_id: str) -> Dict[str, Any]:
        """
        Analyze workflow state and flow (FLOW dimension)

        Maps Notion workflow properties to spatial flow understanding:
        - Task states and transitions
        - Approval workflows
        - Development stages
        - Process flow patterns
        """
        try:
            page = await self.mcp_adapter.get_page(page_id)
            if not page:
                return {}

            properties = page.get("properties", {})

            # Extract workflow information
            status = properties.get("Status", {}).get("select", {}).get("name", "unknown")
            stage = properties.get("Stage", {}).get("select", {}).get("name", "unknown")
            phase = properties.get("Phase", {}).get("select", {}).get("name", "unknown")
            approval = properties.get("Approval", {}).get("select", {}).get("name", "pending")

            # Analyze workflow state
            workflow_analysis = {
                "page_id": page_id,
                "current_status": status,
                "current_stage": stage,
                "current_phase": phase,
                "approval_status": approval,
                "workflow_progress": self._calculate_workflow_progress(status, stage, phase),
                "next_actions": self._determine_next_actions(status, stage, phase, approval),
                "blockers": self._identify_potential_blockers(status, stage, approval),
                "flow_efficiency": self._assess_flow_efficiency(status, stage, phase),
            }

            return workflow_analysis

        except Exception as e:
            logger.error(f"Error analyzing workflow properties for {page_id}: {e}")
            return {}

    async def analyze_metrics(self, page_id: str) -> Dict[str, Any]:
        """
        Analyze quantitative metrics (QUANTITATIVE dimension)

        Maps Notion numeric properties to spatial quantitative understanding:
        - Size and scope metrics
        - Progress indicators
        - Performance metrics
        - Resource allocation
        """
        try:
            page = await self.mcp_adapter.get_page(page_id)
            if not page:
                return {}

            properties = page.get("properties", {})

            # Extract quantitative information
            story_points = properties.get("Story Points", {}).get("number", 0)
            progress = properties.get("Progress", {}).get("number", 0)
            effort = properties.get("Effort", {}).get("number", 0)
            complexity = properties.get("Complexity", {}).get("select", {}).get("name", "medium")

            # Analyze metrics
            metrics_analysis = {
                "page_id": page_id,
                "story_points": story_points,
                "progress_percentage": progress,
                "effort_hours": effort,
                "complexity_level": complexity,
                "size_category": self._categorize_size(story_points, effort),
                "progress_status": self._categorize_progress(progress),
                "effort_distribution": self._analyze_effort_distribution(effort, story_points),
                "completion_estimate": self._estimate_completion_time(
                    progress, effort, story_points
                ),
            }

            return metrics_analysis

        except Exception as e:
            logger.error(f"Error analyzing metrics for {page_id}: {e}")
            return {}

    async def analyze_relations(self, page_id: str) -> Dict[str, Any]:
        """
        Analyze causal relationships (CAUSAL dimension)

        Maps Notion relation properties to spatial causal understanding:
        - Linked issues and dependencies
        - Related content and references
        - Impact and dependency chains
        - Causal relationships
        """
        try:
            page = await self.mcp_adapter.get_page(page_id)
            if not page:
                return {}

            properties = page.get("properties", {})

            # Extract relation information
            dependencies = properties.get("Dependencies", {}).get("relation", [])
            blockers = properties.get("Blockers", {}).get("relation", [])
            related = properties.get("Related", {}).get("relation", [])
            parent = properties.get("Parent", {}).get("relation", [])

            # Analyze relationships
            relations_analysis = {
                "page_id": page_id,
                "dependencies": [dep.get("id") for dep in dependencies],
                "blockers": [blocker.get("id") for blocker in blockers],
                "related_items": [rel.get("id") for rel in related],
                "parent_item": parent[0].get("id") if parent else None,
                "dependency_count": len(dependencies),
                "blocker_count": len(blockers),
                "relationship_complexity": self._assess_relationship_complexity(
                    dependencies, blockers, related
                ),
                "impact_level": self._determine_impact_level(dependencies, blockers),
                "dependency_chain_depth": self._calculate_dependency_depth(dependencies),
            }

            return relations_analysis

        except Exception as e:
            logger.error(f"Error analyzing relations for {page_id}: {e}")
            return {}

    async def analyze_workspace(self, page_id: str) -> Dict[str, Any]:
        """
        Analyze workspace context (CONTEXTUAL dimension)

        Maps Notion workspace context to spatial contextual understanding:
        - Project and team associations
        - Workspace organization patterns
        - Contextual relevance and scope
        - Environmental factors
        """
        try:
            page = await self.mcp_adapter.get_page(page_id)
            if not page:
                return {}

            properties = page.get("properties", {})

            # Extract contextual information
            project = properties.get("Project", {}).get("select", {}).get("name", "general")
            team = properties.get("Team", {}).get("select", {}).get("name", "general")
            area = properties.get("Area", {}).get("select", {}).get("name", "general")
            sprint = properties.get("Sprint", {}).get("select", {}).get("name", "current")

            # Analyze workspace context
            context_analysis = {
                "page_id": page_id,
                "project": project,
                "team": team,
                "area": area,
                "sprint": sprint,
                "context_relevance": self._assess_context_relevance(project, team, area),
                "scope_alignment": self._assess_scope_alignment(project, team, area),
                "temporal_context": self._assess_temporal_context(sprint),
                "organizational_context": self._assess_organizational_context(project, team),
            }

            return context_analysis

        except Exception as e:
            logger.error(f"Error analyzing workspace context for {page_id}: {e}")
            return {}

    async def get_comprehensive_spatial_analysis(self, page_id: str) -> Dict[str, Any]:
        """Get comprehensive spatial analysis across all 8 dimensions"""
        try:
            analysis_results = {}

            # Analyze each dimension
            for dimension_name, analysis_func in self.dimensions.items():
                analysis_results[dimension_name] = await analysis_func(page_id)

            # Add spatial positioning
            spatial_context = {
                "territory_id": self._workspace_cache.get("workspace_id"),
                "room_id": "notion_workspace",
                "path_id": page_id,
                "attention_level": "medium",
                "navigation_intent": "analyze",
            }

            position = self.mcp_adapter.map_to_position(page_id, spatial_context)

            analysis_results["SPATIAL_POSITIONING"] = {
                "position": position.position,
                "spatial_context": spatial_context,
                "mapping_stats": self.mcp_adapter.get_mapping_stats(),
            }

            return analysis_results

        except Exception as e:
            logger.error(f"Error getting comprehensive spatial analysis for {page_id}: {e}")
            return {}

    # Helper methods for analysis calculations
    def _calculate_priority_score(
        self, status: str, priority: str, tags: List[str], milestone: bool
    ) -> int:
        """Calculate priority score based on various factors"""
        score = 0

        # Status scoring
        status_scores = {"not_started": 1, "in_progress": 2, "review": 3, "complete": 0}
        score += status_scores.get(status.lower(), 1)

        # Priority scoring
        priority_scores = {"low": 1, "medium": 2, "high": 3, "urgent": 4}
        score += priority_scores.get(priority.lower(), 2)

        # Tag scoring
        if any("critical" in tag.lower() for tag in tags):
            score += 2
        if any("important" in tag.lower() for tag in tags):
            score += 1

        # Milestone scoring
        if milestone:
            score += 2

        return min(score, 10)  # Cap at 10

    def _determine_attention_level(self, status: str, priority: str, milestone: bool) -> str:
        """Determine attention level required"""
        if priority.lower() == "urgent" or milestone:
            return "high"
        elif priority.lower() == "high" or status.lower() == "review":
            return "medium"
        else:
            return "low"

    def _map_status_to_workflow(self, status: str) -> str:
        """Map status to workflow stage"""
        status_mapping = {
            "not_started": "planning",
            "in_progress": "execution",
            "review": "review",
            "complete": "completed",
        }
        return status_mapping.get(status.lower(), "unknown")

    def _determine_collaboration_level(
        self, created_by: List, last_edited_by: List, assignees: List, reviewers: List
    ) -> str:
        """Determine level of collaboration"""
        total_participants = len(
            set([p.get("id") for p in created_by + last_edited_by + assignees + reviewers])
        )

        if total_participants == 1:
            return "individual"
        elif total_participants <= 3:
            return "small_team"
        elif total_participants <= 6:
            return "medium_team"
        else:
            return "large_team"

    def _calculate_workflow_progress(self, status: str, stage: str, phase: str) -> float:
        """Calculate workflow progress percentage"""
        # Simplified progress calculation
        progress_mapping = {
            "not_started": 0.0,
            "planning": 0.25,
            "in_progress": 0.5,
            "review": 0.75,
            "complete": 1.0,
        }

        return progress_mapping.get(status.lower(), 0.0)

    def _categorize_size(self, story_points: float, effort: float) -> str:
        """Categorize work size"""
        if story_points <= 3 and effort <= 4:
            return "small"
        elif story_points <= 8 and effort <= 16:
            return "medium"
        elif story_points <= 13 and effort <= 40:
            return "large"
        else:
            return "epic"

    def _categorize_progress(self, progress: float) -> str:
        """Categorize progress status"""
        if progress == 0:
            return "not_started"
        elif progress < 25:
            return "early_stage"
        elif progress < 75:
            return "in_progress"
        elif progress < 100:
            return "near_completion"
        else:
            return "complete"

    def get_spatial_analytics(self) -> Dict[str, Any]:
        """Get spatial intelligence analytics"""
        return {
            **self._spatial_analytics,
            "mcp_adapter_stats": self.mcp_adapter.get_mapping_stats(),
            "workspace_info": self._workspace_cache,
        }

    async def close(self):
        """Clean up resources"""
        try:
            await self.mcp_adapter.close()
            logger.info("NotionSpatialIntelligence resources cleaned up")
        except Exception as e:
            logger.error(f"Error closing NotionSpatialIntelligence: {e}")

    def __del__(self):
        """Destructor to ensure cleanup"""
        if hasattr(self, "mcp_adapter"):
            asyncio.create_task(self.close())
