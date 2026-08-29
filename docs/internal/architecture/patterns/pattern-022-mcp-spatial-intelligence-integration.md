# Pattern-022: MCP+Spatial Intelligence Integration Pattern

## Status

**Proven**

## Context

Modern development environments require integration with multiple external tools and services (Linear, GitHub, Slack, etc.) while maintaining rich contextual awareness for intelligent routing and search. Traditional integration approaches often result in shallow connections that lose important dimensional context, making it difficult to provide meaningful cross-system insights. The MCP+Spatial Intelligence Integration Pattern addresses:

- What challenges does this solve? Enables external tool integration through MCP (Model Context Protocol) with 8-dimensional spatial intelligence analysis for enhanced context awareness
- When should this pattern be considered? When building federated search capabilities that need rich contextual understanding across multiple external systems
- What are the typical scenarios where this applies? Cross-system search, intelligent routing, contextual recommendations, multi-tool workflows

## Pattern Description

The MCP+Spatial Intelligence Integration Pattern enables external tool integration through MCP (Model Context Protocol) combined with 8-dimensional spatial intelligence analysis to create rich, contextually-aware connections between systems. The pattern provides a standardized framework for analyzing external system data across multiple dimensions to enhance search capabilities and enable intelligent routing.

Core concept:

- 8-dimensional spatial analysis framework for rich context extraction
- MCP adapter pattern for standardized external tool integration
- Federated search capabilities with spatial enhancement
- Performance-optimized parallel processing of dimensional analyses

## Implementation

### Core Spatial Intelligence Framework

```python
from typing import Dict, Any, List, Optional
import asyncio
from abc import ABC, abstractmethod

class SpatialContext:
    """Rich spatial context with 8-dimensional analysis"""

    def __init__(self, territory_id: str, room_id: str, path_id: str,
                 attention_level: float, emotional_valence: float,
                 navigation_intent: str, external_system: str,
                 external_context: Dict[str, Any]):
        self.territory_id = territory_id
        self.room_id = room_id
        self.path_id = path_id
        self.attention_level = attention_level  # 0.0 - 1.0
        self.emotional_valence = emotional_valence  # -1.0 to 1.0
        self.navigation_intent = navigation_intent
        self.external_system = external_system
        self.external_context = external_context
        self.created_at = datetime.utcnow()

class LinearSpatialIntelligence:
    """MCP+Spatial pattern for Linear integration with 8-dimensional analysis"""

    def __init__(self):
        """Initialize with MCP adapter and 8-dimensional analysis"""
        self.mcp_adapter = LinearMCPSpatialAdapter()

        # 8-dimensional analysis functions
        self.dimensions = {
            "HIERARCHY": self.analyze_issue_hierarchy,
            "TEMPORAL": self.analyze_timeline,
            "PRIORITY": self.analyze_priority_signals,
            "COLLABORATIVE": self.analyze_team_activity,
            "FLOW": self.analyze_workflow_state,
            "QUANTITATIVE": self.analyze_metrics,
            "CAUSAL": self.analyze_dependencies,
            "CONTEXTUAL": self.analyze_project_context,
        }

    async def create_spatial_context(self, issue: Dict[str, Any]) -> SpatialContext:
        """Create full 8-dimensional spatial context"""
        # Run all dimensional analyses in parallel
        dimension_results = await asyncio.gather(
            *[func(issue) for func in self.dimensions.values()],
            return_exceptions=True
        )

        # Process results into dimensional dictionary
        dimension_dict = {}
        for i, key in enumerate(self.dimensions.keys()):
            if isinstance(dimension_results[i], Exception):
                dimension_dict[key] = {"error": str(dimension_results[i])}
            else:
                dimension_dict[key] = dimension_results[i]

        # Extract key dimensions for spatial context
        priority = dimension_dict.get("PRIORITY", {})
        temporal = dimension_dict.get("TEMPORAL", {})
        flow = dimension_dict.get("FLOW", {})
        contextual = dimension_dict.get("CONTEXTUAL", {})

        # Create spatial context with attention/valence/intent
        return SpatialContext(
            territory_id="linear",
            room_id=contextual.get("team_key", "unknown"),
            path_id=f"issues/{issue.get('number', 'unknown')}",
            attention_level=self._determine_attention(priority, temporal),
            emotional_valence=self._determine_valence(priority, flow),
            navigation_intent=self._determine_intent(priority, flow),
            external_system="linear",
            external_context=dimension_dict
        )

    async def analyze_issue_hierarchy(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze HIERARCHY dimension - Issue/project relationships, team structures"""
        hierarchy_data = {
            "project_level": issue.get("project", {}).get("name", "unknown"),
            "team_level": issue.get("team", {}).get("name", "unknown"),
            "epic_relationship": None,
            "parent_issue": None,
            "child_issues": [],
            "hierarchy_depth": 0
        }

        # Analyze parent/child relationships
        if issue.get("parent"):
            hierarchy_data["parent_issue"] = {
                "id": issue["parent"]["id"],
                "title": issue["parent"]["title"],
                "url": issue["parent"]["url"]
            }
            hierarchy_data["hierarchy_depth"] += 1

        # Check for epic relationship
        if issue.get("project", {}).get("milestone"):
            hierarchy_data["epic_relationship"] = {
                "milestone": issue["project"]["milestone"]["name"],
                "milestone_url": issue["project"]["milestone"]["url"]
            }

        return hierarchy_data

    async def analyze_timeline(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze TEMPORAL dimension - Created/updated patterns, cycle timelines"""
        timeline_data = {
            "created_at": issue.get("createdAt"),
            "updated_at": issue.get("updatedAt"),
            "age_days": 0,
            "last_activity_days": 0,
            "cycle_info": {},
            "timeline_pattern": "unknown"
        }

        if timeline_data["created_at"]:
            created = datetime.fromisoformat(timeline_data["created_at"].replace('Z', '+00:00'))
            timeline_data["age_days"] = (datetime.utcnow().replace(tzinfo=timezone.utc) - created).days

        if timeline_data["updated_at"]:
            updated = datetime.fromisoformat(timeline_data["updated_at"].replace('Z', '+00:00'))
            timeline_data["last_activity_days"] = (datetime.utcnow().replace(tzinfo=timezone.utc) - updated).days

        # Analyze cycle information
        if issue.get("cycle"):
            timeline_data["cycle_info"] = {
                "cycle_name": issue["cycle"]["name"],
                "cycle_starts_at": issue["cycle"]["startsAt"],
                "cycle_ends_at": issue["cycle"]["endsAt"],
                "in_active_cycle": True
            }

        # Determine timeline pattern
        if timeline_data["last_activity_days"] == 0:
            timeline_data["timeline_pattern"] = "active_today"
        elif timeline_data["last_activity_days"] <= 7:
            timeline_data["timeline_pattern"] = "active_week"
        elif timeline_data["last_activity_days"] <= 30:
            timeline_data["timeline_pattern"] = "active_month"
        else:
            timeline_data["timeline_pattern"] = "stale"

        return timeline_data

    async def analyze_priority_signals(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze PRIORITY dimension - Priority levels, cycles, milestones"""
        priority_data = {
            "priority_level": issue.get("priority", 0),
            "priority_label": issue.get("priorityLabel", "None"),
            "is_urgent": False,
            "milestone_priority": None,
            "computed_priority_score": 0.0
        }

        # Determine urgency based on multiple signals
        priority_level = priority_data["priority_level"]
        if priority_level >= 4:  # High/Urgent priority
            priority_data["is_urgent"] = True

        # Check milestone-based priority
        if issue.get("project", {}).get("milestone"):
            priority_data["milestone_priority"] = {
                "milestone": issue["project"]["milestone"]["name"],
                "is_active": True
            }

        # Compute priority score (0.0 - 1.0)
        base_score = min(priority_level / 4.0, 1.0)
        milestone_boost = 0.2 if priority_data["milestone_priority"] else 0.0
        priority_data["computed_priority_score"] = min(base_score + milestone_boost, 1.0)

        return priority_data

    async def analyze_team_activity(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze COLLABORATIVE dimension - Assignees, subscribers, comments"""
        collaborative_data = {
            "assignee": None,
            "subscribers_count": 0,
            "comments_count": 0,
            "collaboration_level": "low",
            "team_engagement": 0.0
        }

        # Assignee information
        if issue.get("assignee"):
            collaborative_data["assignee"] = {
                "name": issue["assignee"]["name"],
                "email": issue["assignee"]["email"],
                "avatar_url": issue["assignee"]["avatarUrl"]
            }

        # Subscriber and comment metrics
        collaborative_data["subscribers_count"] = len(issue.get("subscribers", []))
        collaborative_data["comments_count"] = issue.get("commentCount", 0)

        # Determine collaboration level
        total_engagement = collaborative_data["subscribers_count"] + collaborative_data["comments_count"]
        if total_engagement >= 10:
            collaborative_data["collaboration_level"] = "high"
            collaborative_data["team_engagement"] = 1.0
        elif total_engagement >= 5:
            collaborative_data["collaboration_level"] = "medium"
            collaborative_data["team_engagement"] = 0.6
        elif total_engagement >= 1:
            collaborative_data["collaboration_level"] = "low"
            collaborative_data["team_engagement"] = 0.3
        else:
            collaborative_data["collaboration_level"] = "none"
            collaborative_data["team_engagement"] = 0.0

        return collaborative_data

    async def analyze_workflow_state(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze FLOW dimension - Status workflows, state transitions"""
        flow_data = {
            "current_state": issue.get("state", {}).get("name", "unknown"),
            "state_type": issue.get("state", {}).get("type", "unknown"),
            "workflow_stage": "unknown",
            "is_blocked": False,
            "flow_velocity": 0.0
        }

        # Determine workflow stage based on state
        state_name = flow_data["current_state"].lower()
        if state_name in ["backlog", "triage", "todo"]:
            flow_data["workflow_stage"] = "planning"
        elif state_name in ["in progress", "in development", "in review"]:
            flow_data["workflow_stage"] = "development"
        elif state_name in ["in testing", "qa", "staging"]:
            flow_data["workflow_stage"] = "testing"
        elif state_name in ["done", "completed", "closed"]:
            flow_data["workflow_stage"] = "completed"
        elif state_name in ["blocked", "on hold"]:
            flow_data["workflow_stage"] = "blocked"
            flow_data["is_blocked"] = True

        # Estimate flow velocity based on recent state changes
        # This would typically require additional API calls to get state history
        if flow_data["workflow_stage"] == "development":
            flow_data["flow_velocity"] = 0.8
        elif flow_data["workflow_stage"] == "testing":
            flow_data["flow_velocity"] = 0.6
        elif flow_data["workflow_stage"] == "planning":
            flow_data["flow_velocity"] = 0.2
        elif flow_data["workflow_stage"] == "blocked":
            flow_data["flow_velocity"] = 0.0
        else:
            flow_data["flow_velocity"] = 0.4

        return flow_data

    async def analyze_metrics(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze QUANTITATIVE dimension - Counts, velocities, estimates, metrics"""
        metrics_data = {
            "estimate": issue.get("estimate", 0),
            "story_points": issue.get("estimate", 0),  # Same as estimate in Linear
            "cycle_metrics": {},
            "team_metrics": {},
            "velocity_indicators": {}
        }

        # Cycle-based metrics
        if issue.get("cycle"):
            cycle_issues = await self.mcp_adapter.get_cycle_issues(issue["cycle"]["id"])
            metrics_data["cycle_metrics"] = {
                "total_issues": len(cycle_issues),
                "completed_issues": sum(1 for i in cycle_issues if i.get("state", {}).get("type") == "completed"),
                "cycle_progress": 0.0
            }
            if metrics_data["cycle_metrics"]["total_issues"] > 0:
                metrics_data["cycle_metrics"]["cycle_progress"] = (
                    metrics_data["cycle_metrics"]["completed_issues"] /
                    metrics_data["cycle_metrics"]["total_issues"]
                )

        # Team velocity indicators
        if issue.get("team"):
            metrics_data["team_metrics"] = {
                "team_id": issue["team"]["id"],
                "team_name": issue["team"]["name"],
                "estimated_completion_weeks": max(1, metrics_data["estimate"] // 5) if metrics_data["estimate"] else 1
            }

        return metrics_data

    async def analyze_dependencies(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze CAUSAL dimension - Dependencies, blocked issues, relations"""
        causal_data = {
            "blocking_issues": [],
            "blocked_by_issues": [],
            "related_issues": [],
            "dependency_chains": [],
            "impact_radius": 0
        }

        # Get issue relations (this would require additional API calls)
        relations = await self.mcp_adapter.get_issue_relations(issue["id"])

        for relation in relations:
            if relation["type"] == "blocks":
                causal_data["blocking_issues"].append({
                    "id": relation["relatedIssue"]["id"],
                    "title": relation["relatedIssue"]["title"],
                    "state": relation["relatedIssue"]["state"]["name"]
                })
            elif relation["type"] == "blocked_by":
                causal_data["blocked_by_issues"].append({
                    "id": relation["relatedIssue"]["id"],
                    "title": relation["relatedIssue"]["title"],
                    "state": relation["relatedIssue"]["state"]["name"]
                })
            elif relation["type"] == "related":
                causal_data["related_issues"].append({
                    "id": relation["relatedIssue"]["id"],
                    "title": relation["relatedIssue"]["title"]
                })

        # Calculate impact radius
        causal_data["impact_radius"] = (
            len(causal_data["blocking_issues"]) * 2 +  # Blocking has higher impact
            len(causal_data["blocked_by_issues"]) +
            len(causal_data["related_issues"]) * 0.5
        )

        return causal_data

    async def analyze_project_context(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze CONTEXTUAL dimension - Project, team, workspace context"""
        contextual_data = {
            "workspace": issue.get("team", {}).get("organization", {}).get("name", "unknown"),
            "project_context": {},
            "team_context": {},
            "workspace_context": {},
            "team_key": "unknown"
        }

        # Project context
        if issue.get("project"):
            contextual_data["project_context"] = {
                "id": issue["project"]["id"],
                "name": issue["project"]["name"],
                "description": issue["project"]["description"],
                "url": issue["project"]["url"],
                "state": issue["project"]["state"]
            }

        # Team context
        if issue.get("team"):
            contextual_data["team_context"] = {
                "id": issue["team"]["id"],
                "name": issue["team"]["name"],
                "key": issue["team"]["key"],
                "description": issue["team"]["description"]
            }
            contextual_data["team_key"] = issue["team"]["key"]

        return contextual_data

    def _determine_attention(self, priority: Dict, temporal: Dict) -> float:
        """Determine attention level based on priority and temporal signals"""
        base_attention = priority.get("computed_priority_score", 0.0)

        # Boost attention for recent activity
        last_activity_days = temporal.get("last_activity_days", 0)
        if last_activity_days == 0:
            base_attention += 0.3
        elif last_activity_days <= 1:
            base_attention += 0.2
        elif last_activity_days <= 7:
            base_attention += 0.1

        return min(base_attention, 1.0)

    def _determine_valence(self, priority: Dict, flow: Dict) -> float:
        """Determine emotional valence based on priority and flow state"""
        # Start neutral
        valence = 0.0

        # Positive valence for progress
        if flow.get("workflow_stage") == "completed":
            valence += 0.8
        elif flow.get("workflow_stage") == "development":
            valence += 0.4
        elif flow.get("workflow_stage") == "testing":
            valence += 0.2

        # Negative valence for problems
        if flow.get("is_blocked"):
            valence -= 0.6
        elif priority.get("is_urgent") and flow.get("workflow_stage") == "planning":
            valence -= 0.4

        return max(-1.0, min(1.0, valence))

    def _determine_intent(self, priority: Dict, flow: Dict) -> str:
        """Determine navigation intent based on priority and flow state"""
        if flow.get("is_blocked"):
            return "unblock_issue"
        elif priority.get("is_urgent"):
            return "expedite_work"
        elif flow.get("workflow_stage") == "development":
            return "monitor_progress"
        elif flow.get("workflow_stage") == "testing":
            return "review_quality"
        elif flow.get("workflow_stage") == "completed":
            return "verify_completion"
        else:
            return "plan_work"
```

### MCP Adapter Implementation

```python
class BaseSpatialAdapter(ABC):
    """Base class for MCP spatial adapters"""

    @abstractmethod
    async def search_issues(self, query: str, limit: int = 10) -> List[Dict]:
        """Search issues in external system"""
        pass

    @abstractmethod
    async def get_issue_relations(self, issue_id: str) -> List[Dict]:
        """Get issue relationships/dependencies"""
        pass

class LinearMCPSpatialAdapter(BaseSpatialAdapter):
    """MCP adapter for Linear GraphQL API with spatial enhancement"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.graphql_endpoint = "https://api.linear.app/graphql"
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=60,
            expected_exception=RequestException
        )

    async def search_issues(self, query: str, limit: int = 10) -> List[Dict]:
        """Search Linear issues via GraphQL with spatial mapping"""
        search_query = """
        query SearchIssues($query: String!, $first: Int!) {
            issues(filter: {or: [
                {title: {containsIgnoreCase: $query}},
                {description: {containsIgnoreCase: $query}}
            ]}, first: $first, orderBy: updatedAt) {
                nodes {
                    id
                    number
                    title
                    description
                    url
                    createdAt
                    updatedAt
                    priority
                    priorityLabel
                    estimate
                    state {
                        id
                        name
                        type
                    }
                    assignee {
                        id
                        name
                        email
                        avatarUrl
                    }
                    team {
                        id
                        name
                        key
                        description
                    }
                    project {
                        id
                        name
                        description
                        url
                        state
                        milestone {
                            id
                            name
                            url
                        }
                    }
                    cycle {
                        id
                        name
                        startsAt
                        endsAt
                    }
                    parent {
                        id
                        title
                        url
                    }
                    subscribers {
                        nodes {
                            id
                            name
                        }
                    }
                    commentCount
                }
            }
        }"""

        try:
            result = await self.circuit_breaker.call(
                self._call_linear_api,
                search_query,
                {"query": query, "first": limit}
            )
            return result.get("issues", {}).get("nodes", [])
        except Exception as e:
            logger.error(f"Linear search failed: {e}")
            return []

    async def get_issue_relations(self, issue_id: str) -> List[Dict]:
        """Get issue relationships and dependencies"""
        relations_query = """
        query GetIssueRelations($id: String!) {
            issue(id: $id) {
                relations {
                    nodes {
                        id
                        type
                        relatedIssue {
                            id
                            title
                            state {
                                name
                                type
                            }
                        }
                    }
                }
            }
        }"""

        try:
            result = await self.circuit_breaker.call(
                self._call_linear_api,
                relations_query,
                {"id": issue_id}
            )
            return result.get("issue", {}).get("relations", {}).get("nodes", [])
        except Exception as e:
            logger.error(f"Linear relations fetch failed: {e}")
            return []

    async def get_cycle_issues(self, cycle_id: str) -> List[Dict]:
        """Get all issues in a cycle for metrics calculation"""
        cycle_query = """
        query GetCycleIssues($id: String!) {
            cycle(id: $id) {
                issues {
                    nodes {
                        id
                        state {
                            type
                        }
                        estimate
                    }
                }
            }
        }"""

        try:
            result = await self.circuit_breaker.call(
                self._call_linear_api,
                cycle_query,
                {"id": cycle_id}
            )
            return result.get("cycle", {}).get("issues", {}).get("nodes", [])
        except Exception as e:
            logger.error(f"Linear cycle issues fetch failed: {e}")
            return []

    async def _call_linear_api(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Make GraphQL API call to Linear"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "query": query,
            "variables": variables
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.graphql_endpoint,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                response.raise_for_status()
                result = await response.json()

                if "errors" in result:
                    raise Exception(f"GraphQL errors: {result['errors']}")

                return result.get("data", {})
```

### QueryRouter Integration

```python
class FederatedSearchWithSpatial:
    """Enhanced federated search with spatial intelligence"""

    def __init__(self, query_router, spatial_adapters: Dict[str, Any]):
        self.query_router = query_router
        self.spatial_adapters = spatial_adapters
        self.performance_monitor = PerformanceMonitor()

    async def federated_search_with_spatial(self, query: str) -> Dict[str, Any]:
        """Enhanced federated search with spatial intelligence"""
        start_time = time.time()

        # Get base federated search results
        results = await self.query_router.federated_search(query)

        # Add spatial-enhanced external system searches
        spatial_tasks = []
        for system_name, adapter in self.spatial_adapters.items():
            if adapter and hasattr(adapter, 'search_issues'):
                task = self._search_with_spatial_enhancement(system_name, adapter, query)
                spatial_tasks.append(task)

        if spatial_tasks:
            spatial_results = await asyncio.gather(*spatial_tasks, return_exceptions=True)

            for i, (system_name, result) in enumerate(zip(self.spatial_adapters.keys(), spatial_results)):
                if not isinstance(result, Exception) and result:
                    results[f"{system_name}_results"] = result
                    if result.get("issues"):
                        results["sources"].append(f"{system_name}_mcp")

        # Record performance metrics
        total_time = time.time() - start_time
        self.performance_monitor.record_search_time(total_time)

        # Add spatial context summary
        results["spatial_context"] = await self._create_search_spatial_context(results)

        return results

    async def _search_with_spatial_enhancement(self, system_name: str, adapter, query: str) -> Dict[str, Any]:
        """Search external system with spatial enhancement"""
        try:
            # Get basic search results
            issues = await adapter.search_issues(query, limit=10)

            if not issues:
                return {"issues": [], "spatial_contexts": []}

            # Create spatial contexts for each result
            spatial_contexts = []
            if hasattr(adapter, 'spatial_intelligence'):
                spatial_tasks = [
                    adapter.spatial_intelligence.create_spatial_context(issue)
                    for issue in issues[:5]  # Limit spatial analysis for performance
                ]
                spatial_contexts = await asyncio.gather(*spatial_tasks, return_exceptions=True)
                spatial_contexts = [ctx for ctx in spatial_contexts if not isinstance(ctx, Exception)]

            return {
                "issues": issues,
                "spatial_contexts": spatial_contexts,
                "system": system_name
            }
        except Exception as e:
            logger.error(f"Spatial search failed for {system_name}: {e}")
            return {"issues": [], "spatial_contexts": [], "error": str(e)}

    async def _create_search_spatial_context(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create aggregated spatial context for search results"""
        total_attention = 0.0
        total_results = 0
        systems_with_results = []

        for key, value in results.items():
            if key.endswith("_results") and isinstance(value, dict):
                spatial_contexts = value.get("spatial_contexts", [])
                for ctx in spatial_contexts:
                    if hasattr(ctx, 'attention_level'):
                        total_attention += ctx.attention_level
                        total_results += 1

                if value.get("issues"):
                    systems_with_results.append(value.get("system", key.replace("_results", "")))

        return {
            "average_attention": total_attention / max(total_results, 1),
            "total_results_with_spatial": total_results,
            "systems_engaged": systems_with_results,
            "cross_system_insights": len(systems_with_results) > 1
        }
```

## Usage Guidelines

### When to Use MCP+Spatial Intelligence Integration

- **Multi-System Federated Search**: When building search capabilities that span multiple external tools
- **Rich Context Requirements**: When simple API integration doesn't provide enough contextual understanding
- **Intelligent Routing**: When decisions need to be made based on deep analysis of external system data
- **Cross-System Insights**: When correlations between different tools provide valuable information

### Implementation Best Practices

- **8-Dimensional Analysis**: Implement all 8 dimensions for consistent spatial intelligence across integrations
- **Performance Optimization**: Use parallel processing for dimensional analyses and set performance targets (<150ms per tool)
- **Circuit Breaker Protection**: Include circuit breaker patterns and graceful degradation for external system failures
- **Comprehensive Testing**: Test with mocked external APIs to ensure reliability and performance
- **GraphQL Preference**: Use GraphQL for modern APIs, REST for legacy systems
- **Error Handling**: Log failures appropriately and provide fallback mechanisms

### Integration Architecture

- **MCP Adapter Pattern**: Follow exact pattern structure for new tool integrations
- **Spatial Context Creation**: Create rich spatial contexts for external system data
- **QueryRouter Integration**: Integrate with existing federated search infrastructure
- **Performance Monitoring**: Track performance metrics and optimize based on usage patterns

## Benefits

- Provides rich, multi-dimensional context awareness for external system integration
- Enables intelligent routing and decision-making based on comprehensive data analysis
- Supports federated search capabilities with spatial enhancement
- Maintains performance targets through parallel processing and optimization
- Offers standardized integration pattern for multiple external tools
- Facilitates cross-system insights and correlations

## Trade-offs

- Increased complexity in integration implementation and maintenance
- Performance overhead from 8-dimensional analysis processing
- Dependency on external system availability and API reliability
- Need for comprehensive error handling and circuit breaker patterns
- Storage and processing requirements for spatial context data
- Complexity in testing and mocking external system interactions

## Anti-patterns to Avoid

- ❌ **Skipping Dimensional Analysis**: Implementing "simple" integrations without full spatial intelligence
- ❌ **Blocking on Tool Failures**: Allowing single tool failures to block entire federated search operations
- ❌ **Hard-coding Tool Logic**: Embedding tool-specific logic directly in QueryRouter instead of using adapters
- ❌ **Missing Performance Monitoring**: Not tracking performance metrics and timeout handling
- ❌ **Incomplete Error Handling**: Failing to implement proper circuit breaker patterns and graceful degradation
- ❌ **Shallow Integration**: Creating basic API connections without leveraging rich contextual capabilities

## Related Patterns

- [Pattern-004: CQRS-lite Pattern](pattern-004-cqrs-lite.md) - Query routing architecture foundation
- [Pattern-012: LLM Adapter Pattern](pattern-012-llm-adapter.md) - Adapter pattern for external service integration
- [Pattern-017: Background Task Error Handling Pattern](pattern-017-background-task-error-handling.md) - Error handling for async operations
- [Pattern-014: Error Handling Pattern (API Contract)](pattern-014-error-handling-api-contract.md) - Error handling for external API calls

## References

- **Implementation**: LinearSpatialIntelligence (425 lines), LinearMCPSpatialAdapter (372 lines)
- **Performance Evidence**: <150ms additional latency per tool validated
- **Test Coverage**: 448 lines covering all dimensions and performance targets
- **Related ADR**: ADR-008 (MCP connection pooling and circuit breaker patterns)

## Migration Notes

_Consolidated from:_

- `pattern-catalog.md#22-mcp-spatial-intelligence-integration-pattern` - Complete 8-dimensional analysis framework
- `archive/PATTERN-INDEX-legacy.md#mcp-integration-patterns` - MCP connection pooling and circuit breaker patterns
- QueryRouter integration examples and federated search enhancement

_Last updated: September 15, 2025_
