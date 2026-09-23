"""
PM-081: Todo Knowledge Graph Integration Service

Provides integration between Todo system and PM-040 Knowledge Graph for:
- Semantic todo classification and similarity
- Todo relationship discovery
- Context-aware todo recommendations
- Learning from todo patterns
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

import structlog

from services.domain.models import KnowledgeNode, Todo
from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.knowledge.semantic_indexing_service import SemanticIndexingService
from services.shared_types import NodeType
from services.utils.datetime_utils import utc_now

logger = structlog.get_logger()


class TodoKnowledgeService:
    """Service for Todo-Knowledge Graph integration"""

    def __init__(
        self,
        knowledge_graph_service: KnowledgeGraphService,
        semantic_indexing_service: Optional[SemanticIndexingService] = None,
    ):
        self.knowledge_graph = knowledge_graph_service
        self.semantic_indexer = semantic_indexing_service

    async def create_todo_knowledge_node(
        self,
        todo: Todo,
        user_id: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[KnowledgeNode]:
        """Create Knowledge Graph node for todo with semantic metadata"""
        try:
            # Build semantic metadata for the todo
            metadata = {
                "todo_id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "status": todo.status if isinstance(todo.status, str) else todo.status.value,
                "priority": (
                    todo.priority if isinstance(todo.priority, str) else todo.priority.value
                ),
                "tags": todo.tags,
                "context": todo.context,
                "creation_intent": todo.creation_intent,
                "intent_confidence": todo.intent_confidence,
                "estimated_minutes": todo.estimated_minutes,
                "project_id": todo.project_id,
                "owner_id": todo.owner_id,
                "created_at": todo.created_at.isoformat(),
                "node_type": "todo",
                "semantic_content": f"{todo.title} {todo.description}".strip(),
            }

            # Add context if provided
            if context:
                metadata["context_data"] = context

            # Create node in Knowledge Graph
            node = await self.knowledge_graph.create_node(
                name=f"todo_{todo.id}",
                node_type=NodeType.CONCEPT,
                metadata=metadata,
                session_id=user_id,  # Use user_id as session for user-specific learning
            )

            # Update todo with Knowledge Graph reference
            todo.knowledge_node_id = node.id

            logger.info(
                "Created Knowledge Graph node for todo",
                todo_id=todo.id,
                node_id=node.id,
                user_id=user_id,
            )

            return node

        except Exception as e:
            logger.warning(
                "Failed to create Knowledge Graph node for todo",
                todo_id=todo.id,
                error=str(e),
            )
            return None

    async def find_similar_todos(
        self,
        todo: Todo,
        user_id: str,
        limit: int = 5,
        similarity_threshold: float = 0.7,
    ) -> List[Tuple[str, float]]:
        """Find similar todos using semantic search"""
        if not self.semantic_indexer:
            logger.debug("Semantic indexing not available for todo similarity")
            return []

        try:
            # Create temporary node for similarity search
            query_node = KnowledgeNode(
                name=f"temp_todo_query_{todo.id}",
                node_type=NodeType.CONCEPT,
                metadata={
                    "semantic_content": f"{todo.title} {todo.description}".strip(),
                    "tags": todo.tags,
                    "context": todo.context,
                    "priority": (
                        todo.priority if isinstance(todo.priority, str) else todo.priority.value
                    ),
                    "node_type": "todo",
                },
                session_id=user_id,
            )

            # Search for similar todo nodes
            similar_nodes = await self.semantic_indexer.similarity_search(
                query_node=query_node,
                top_k=limit,
                threshold=similarity_threshold,
                node_types=[NodeType.CONCEPT],
                session_id=user_id,  # User-specific search
            )

            # Extract todo IDs from similar nodes
            similar_todos = []
            for node, similarity in similar_nodes:
                if (
                    node.metadata.get("node_type") == "todo"
                    and node.metadata.get("todo_id")
                    and node.metadata.get("todo_id") != todo.id  # Exclude self
                ):
                    similar_todos.append((node.metadata["todo_id"], similarity))

            logger.debug(
                "Found similar todos",
                query_todo_id=todo.id,
                similar_count=len(similar_todos),
                user_id=user_id,
            )

            return similar_todos

        except Exception as e:
            logger.warning(
                "Failed to find similar todos",
                todo_id=todo.id,
                error=str(e),
            )
            return []

    async def get_todo_recommendations(
        self,
        user_id: str,
        context: Optional[str] = None,
        project_id: Optional[str] = None,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """Get todo recommendations based on user patterns and context"""
        try:
            # Get user's recent todo patterns from Knowledge Graph
            recent_nodes = await self.knowledge_graph.get_nodes_by_type(
                node_type=NodeType.CONCEPT,
                session_id=user_id,
                limit=50,  # Analyze more nodes for patterns
            )

            # Filter for todo nodes
            todo_nodes = [node for node in recent_nodes if node.metadata.get("node_type") == "todo"]

            if not todo_nodes:
                return []

            # Analyze patterns
            patterns = self._analyze_todo_patterns(todo_nodes, context, project_id)

            # Generate recommendations based on patterns
            recommendations = []

            # 1. Context-based recommendations
            if context and patterns.get("common_contexts"):
                for ctx, count in patterns["common_contexts"].items():
                    if ctx == context and count > 2:  # Frequent context
                        recommendations.append(
                            {
                                "type": "context_pattern",
                                "suggestion": f"Common {context} tasks you might want to add",
                                "context": context,
                                "frequency": count,
                                "confidence": min(count / 10, 0.9),
                            }
                        )

            # 2. Project-based recommendations
            if project_id and patterns.get("project_patterns"):
                project_pattern = patterns["project_patterns"].get(project_id)
                if project_pattern and project_pattern["count"] > 3:
                    recommendations.append(
                        {
                            "type": "project_pattern",
                            "suggestion": f"Based on your {project_pattern['common_tags']} work",
                            "project_id": project_id,
                            "common_tags": project_pattern["common_tags"],
                            "confidence": min(project_pattern["count"] / 15, 0.8),
                        }
                    )

            # 3. Time-based recommendations (e.g., daily routines)
            if patterns.get("time_patterns"):
                current_hour = utc_now().hour
                for time_range, pattern in patterns["time_patterns"].items():
                    if self._is_in_time_range(current_hour, time_range) and pattern["count"] > 5:
                        recommendations.append(
                            {
                                "type": "time_pattern",
                                "suggestion": f"Your usual {time_range} tasks",
                                "time_range": time_range,
                                "common_actions": pattern["common_actions"],
                                "confidence": min(pattern["count"] / 20, 0.7),
                            }
                        )

            # Sort by confidence and limit
            recommendations.sort(key=lambda x: x["confidence"], reverse=True)
            return recommendations[:limit]

        except Exception as e:
            logger.warning(
                "Failed to get todo recommendations",
                user_id=user_id,
                error=str(e),
            )
            return []

    async def update_todo_relationships(
        self,
        todo: Todo,
        related_todo_ids: List[str],
        relationship_type: str = "related",
    ) -> None:
        """Update relationships between todos in Knowledge Graph"""
        if not todo.knowledge_node_id:
            return

        try:
            for related_id in related_todo_ids:
                # Find the Knowledge Graph node for related todo
                related_nodes = await self.knowledge_graph.get_nodes_by_type(
                    node_type=NodeType.CONCEPT,
                    session_id=todo.owner_id,
                    limit=100,
                )

                related_node = None
                for node in related_nodes:
                    if node.metadata.get("todo_id") == related_id:
                        related_node = node
                        break

                if related_node:
                    # Create edge between todos
                    await self.knowledge_graph.create_edge(
                        source_node_id=todo.knowledge_node_id,
                        target_node_id=related_node.id,
                        edge_type=relationship_type,
                        weight=0.8,  # Default relationship strength
                        metadata={
                            "relationship_type": relationship_type,
                            "created_by": "todo_system",
                            "created_at": utc_now().isoformat(),
                        },
                    )

            logger.debug(
                "Updated todo relationships",
                todo_id=todo.id,
                related_count=len(related_todo_ids),
            )

        except Exception as e:
            logger.warning(
                "Failed to update todo relationships",
                todo_id=todo.id,
                error=str(e),
            )

    def _analyze_todo_patterns(
        self,
        todo_nodes: List[KnowledgeNode],
        context: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Analyze patterns in user's todo history"""
        patterns = {
            "common_contexts": {},
            "common_tags": {},
            "project_patterns": {},
            "time_patterns": {},
            "priority_patterns": {},
        }

        for node in todo_nodes:
            metadata = node.metadata

            # Context patterns
            node_context = metadata.get("context")
            if node_context:
                patterns["common_contexts"][node_context] = (
                    patterns["common_contexts"].get(node_context, 0) + 1
                )

            # Tag patterns
            tags = metadata.get("tags", [])
            for tag in tags:
                patterns["common_tags"][tag] = patterns["common_tags"].get(tag, 0) + 1

            # Project patterns
            node_project = metadata.get("project_id")
            if node_project:
                if node_project not in patterns["project_patterns"]:
                    patterns["project_patterns"][node_project] = {
                        "count": 0,
                        "common_tags": [],
                    }
                patterns["project_patterns"][node_project]["count"] += 1
                patterns["project_patterns"][node_project]["common_tags"].extend(tags)

            # Time patterns (simplified - could be more sophisticated)
            created_at = metadata.get("created_at")
            if created_at:
                try:
                    dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    hour = dt.hour
                    time_range = self._get_time_range(hour)

                    if time_range not in patterns["time_patterns"]:
                        patterns["time_patterns"][time_range] = {
                            "count": 0,
                            "common_actions": [],
                        }
                    patterns["time_patterns"][time_range]["count"] += 1

                    # Extract action from title (simple heuristic)
                    title = metadata.get("title", "")
                    if title:
                        action = title.split()[0].lower() if title.split() else ""
                        patterns["time_patterns"][time_range]["common_actions"].append(action)

                except Exception:
                    pass  # Skip if datetime parsing fails

            # Priority patterns
            priority = metadata.get("priority")
            if priority:
                patterns["priority_patterns"][priority] = (
                    patterns["priority_patterns"].get(priority, 0) + 1
                )

        # Clean up project patterns - get most common tags
        for project_id, pattern in patterns["project_patterns"].items():
            tag_counts = {}
            for tag in pattern["common_tags"]:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

            # Keep top 3 most common tags
            top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            pattern["common_tags"] = [tag for tag, _ in top_tags]

        # Clean up time patterns - get most common actions
        for time_range, pattern in patterns["time_patterns"].items():
            action_counts = {}
            for action in pattern["common_actions"]:
                if action:  # Skip empty actions
                    action_counts[action] = action_counts.get(action, 0) + 1

            # Keep top 3 most common actions
            top_actions = sorted(action_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            pattern["common_actions"] = [action for action, _ in top_actions]

        return patterns

    def _get_time_range(self, hour: int) -> str:
        """Convert hour to time range string"""
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"

    def _is_in_time_range(self, current_hour: int, time_range: str) -> bool:
        """Check if current hour is in the given time range"""
        ranges = {
            "morning": (6, 12),
            "afternoon": (12, 17),
            "evening": (17, 21),
            "night": (21, 6),  # Wraps around midnight
        }

        start, end = ranges.get(time_range, (0, 24))

        if time_range == "night":
            return current_hour >= start or current_hour < end
        else:
            return start <= current_hour < end
