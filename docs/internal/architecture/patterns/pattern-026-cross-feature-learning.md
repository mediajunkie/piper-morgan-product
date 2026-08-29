# Pattern-026: Cross-Feature Learning Pattern

## Status

**Proven**

## Context

Modern applications with multiple features often develop isolated learning systems that cannot benefit from insights and patterns discovered in other parts of the system. Without cross-feature learning, each feature must rediscover patterns independently, leading to redundant learning efforts, inconsistent user experiences, and missed opportunities for intelligent automation. The Cross-Feature Learning Pattern addresses:

- What challenges does this solve? Enables learning systems to share patterns and insights across different features while maintaining feature isolation and providing confidence-based recommendations
- When should this pattern be considered? When building intelligent systems that need to learn from user behavior across multiple features and share insights
- What are the typical scenarios where this applies? User behavior pattern recognition, intelligent recommendations, cross-feature automation, adaptive user interfaces

## Pattern Description

The Cross-Feature Learning Pattern enables learning systems to share patterns and insights across different features while maintaining feature isolation and providing confidence-based recommendations. The pattern captures patterns from actual usage, tracks confidence levels, and enables cross-feature pattern discovery while preserving feature boundaries and user privacy.

Core concept:
- Centralized pattern repository for cross-feature knowledge sharing
- Confidence-based pattern recommendations with reliability indicators
- Feature isolation maintained while enabling pattern sharing
- Usage-driven learning from actual user behavior, not synthetic data

## Implementation

### Core Learning Framework

```python
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import uuid
import logging

class PatternType(Enum):
    USER_WORKFLOW = "user_workflow"
    COMMAND_SEQUENCE = "command_sequence"
    ERROR_RESOLUTION = "error_resolution"
    CONTEXTUAL_PREFERENCE = "contextual_preference"
    TIMING_PATTERN = "timing_pattern"
    COLLABORATION_PATTERN = "collaboration_pattern"

@dataclass
class LearnedPattern:
    """Represents a learned pattern that can be shared across features"""
    pattern_id: str
    pattern_type: PatternType
    source_feature: str
    pattern_data: Dict[str, Any]
    confidence: float
    usage_count: int = 1
    success_count: int = 0
    failure_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_used_at: datetime = field(default_factory=datetime.utcnow)
    last_updated_at: datetime = field(default_factory=datetime.utcnow)
    applicable_features: List[str] = field(default_factory=list)

    def update_confidence(self, success: bool):
        """Update confidence based on usage success/failure"""
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1

        self.usage_count += 1
        total_outcomes = self.success_count + self.failure_count

        if total_outcomes > 0:
            success_rate = self.success_count / total_outcomes
            # Adjust confidence based on success rate and usage volume
            volume_factor = min(total_outcomes / 10, 1.0)  # Cap at 10 uses
            self.confidence = (success_rate * 0.8 + self.confidence * 0.2) * volume_factor

        self.last_used_at = datetime.utcnow()
        self.last_updated_at = datetime.utcnow()

    def decay_confidence(self, decay_factor: float = 0.95):
        """Apply time-based confidence decay for outdated patterns"""
        self.confidence *= decay_factor
        self.last_updated_at = datetime.utcnow()

    def is_applicable_to_feature(self, feature_name: str) -> bool:
        """Check if pattern is applicable to a specific feature"""
        if not self.applicable_features:
            return True  # No restrictions
        return feature_name in self.applicable_features

class CrossFeatureLearningEngine:
    """Learning system that captures and shares patterns across features"""

    def __init__(self, pattern_repository, confidence_threshold: float = 0.3):
        self.pattern_repository = pattern_repository
        self.confidence_threshold = confidence_threshold
        self.logger = logging.getLogger(__name__)

        # Feature isolation settings
        self.feature_boundaries = {}
        self.privacy_settings = {}

        # Pattern decay settings
        self.decay_schedule = {
            PatternType.USER_WORKFLOW: 0.98,      # Slow decay
            PatternType.COMMAND_SEQUENCE: 0.95,   # Medium decay
            PatternType.ERROR_RESOLUTION: 0.99,   # Very slow decay
            PatternType.CONTEXTUAL_PREFERENCE: 0.96,  # Medium decay
            PatternType.TIMING_PATTERN: 0.94,     # Faster decay
            PatternType.COLLABORATION_PATTERN: 0.97   # Slow decay
        }

    async def learn_pattern(
        self,
        pattern_type: PatternType,
        source_feature: str,
        pattern_data: Dict[str, Any],
        initial_confidence: float = 0.5,
        metadata: Optional[Dict] = None,
        applicable_features: Optional[List[str]] = None
    ) -> LearnedPattern:
        """Learn a new pattern from usage"""

        # Check for existing similar patterns
        existing_pattern = await self._find_similar_pattern(
            pattern_type, source_feature, pattern_data
        )

        if existing_pattern:
            # Update existing pattern instead of creating new one
            existing_pattern.usage_count += 1
            existing_pattern.last_used_at = datetime.utcnow()

            # Merge pattern data if beneficial
            merged_data = self._merge_pattern_data(existing_pattern.pattern_data, pattern_data)
            existing_pattern.pattern_data = merged_data

            await self.pattern_repository.update_pattern(existing_pattern)
            return existing_pattern

        # Create new pattern
        pattern = LearnedPattern(
            pattern_id=str(uuid.uuid4()),
            pattern_type=pattern_type,
            source_feature=source_feature,
            pattern_data=pattern_data,
            confidence=initial_confidence,
            metadata=metadata or {},
            applicable_features=applicable_features or []
        )

        # Store pattern for cross-feature sharing
        await self.pattern_repository.create_pattern(pattern)

        self.logger.info(f"Learned new {pattern_type.value} pattern from {source_feature}")
        return pattern

    async def get_patterns_for_feature(
        self,
        feature_name: str,
        pattern_type: Optional[PatternType] = None,
        min_confidence: Optional[float] = None,
        limit: int = 10
    ) -> List[LearnedPattern]:
        """Get learned patterns applicable to a specific feature"""

        effective_confidence = min_confidence or self.confidence_threshold

        patterns = await self.pattern_repository.get_patterns(
            pattern_type=pattern_type,
            min_confidence=effective_confidence,
            limit=limit * 2  # Get more to filter for feature applicability
        )

        # Filter for feature applicability
        applicable_patterns = [
            pattern for pattern in patterns
            if pattern.is_applicable_to_feature(feature_name)
        ]

        # Sort by confidence and relevance
        applicable_patterns.sort(
            key=lambda p: (p.confidence, p.usage_count, p.last_used_at),
            reverse=True
        )

        return applicable_patterns[:limit]

    async def get_cross_feature_insights(
        self,
        target_feature: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Get insights from other features that might apply to target feature"""

        insights = {
            "target_feature": target_feature,
            "recommendations": [],
            "patterns_analyzed": 0,
            "confidence_summary": {}
        }

        # Get patterns from all features
        all_patterns = await self.pattern_repository.get_patterns(
            min_confidence=self.confidence_threshold * 0.8,  # Slightly lower threshold
            limit=50
        )

        insights["patterns_analyzed"] = len(all_patterns)

        # Analyze patterns for cross-feature applicability
        for pattern in all_patterns:
            if pattern.source_feature == target_feature:
                continue  # Skip same-feature patterns

            if not pattern.is_applicable_to_feature(target_feature):
                continue

            recommendation = await self._create_recommendation(pattern, target_feature, context)
            if recommendation:
                insights["recommendations"].append(recommendation)

        # Create confidence summary
        if insights["recommendations"]:
            confidences = [r["confidence"] for r in insights["recommendations"]]
            insights["confidence_summary"] = {
                "average": sum(confidences) / len(confidences),
                "highest": max(confidences),
                "count_high_confidence": len([c for c in confidences if c > 0.7]),
                "count_medium_confidence": len([c for c in confidences if 0.4 <= c <= 0.7])
            }

        return insights

    async def record_pattern_usage(
        self,
        pattern_id: str,
        feature_name: str,
        success: bool,
        context: Dict[str, Any] = None
    ):
        """Record usage of a learned pattern for confidence updates"""

        pattern = await self.pattern_repository.get_pattern_by_id(pattern_id)
        if not pattern:
            self.logger.warning(f"Pattern {pattern_id} not found for usage recording")
            return

        # Update pattern confidence
        pattern.update_confidence(success)

        # Record cross-feature usage if applicable
        if pattern.source_feature != feature_name:
            if "cross_feature_usage" not in pattern.metadata:
                pattern.metadata["cross_feature_usage"] = {}

            if feature_name not in pattern.metadata["cross_feature_usage"]:
                pattern.metadata["cross_feature_usage"][feature_name] = {
                    "usage_count": 0,
                    "success_count": 0,
                    "first_used": datetime.utcnow().isoformat()
                }

            pattern.metadata["cross_feature_usage"][feature_name]["usage_count"] += 1
            if success:
                pattern.metadata["cross_feature_usage"][feature_name]["success_count"] += 1

        await self.pattern_repository.update_pattern(pattern)

        self.logger.info(f"Recorded pattern usage: {pattern_id} in {feature_name}, success: {success}")

    async def apply_pattern_decay(self):
        """Apply time-based decay to pattern confidence"""

        cutoff_date = datetime.utcnow() - timedelta(days=1)  # Daily decay
        old_patterns = await self.pattern_repository.get_patterns_older_than(cutoff_date)

        for pattern in old_patterns:
            decay_factor = self.decay_schedule.get(pattern.pattern_type, 0.95)
            pattern.decay_confidence(decay_factor)

            # Remove patterns that have decayed too much
            if pattern.confidence < 0.1:
                await self.pattern_repository.delete_pattern(pattern.pattern_id)
                self.logger.info(f"Removed decayed pattern: {pattern.pattern_id}")
            else:
                await self.pattern_repository.update_pattern(pattern)

    async def _find_similar_pattern(
        self,
        pattern_type: PatternType,
        source_feature: str,
        pattern_data: Dict[str, Any]
    ) -> Optional[LearnedPattern]:
        """Find existing similar patterns to avoid duplication"""

        existing_patterns = await self.pattern_repository.get_patterns(
            pattern_type=pattern_type,
            source_feature=source_feature,
            limit=20
        )

        for existing in existing_patterns:
            similarity = self._calculate_pattern_similarity(existing.pattern_data, pattern_data)
            if similarity > 0.8:  # High similarity threshold
                return existing

        return None

    def _calculate_pattern_similarity(self, data1: Dict[str, Any], data2: Dict[str, Any]) -> float:
        """Calculate similarity between two pattern data structures"""

        # Simple similarity calculation based on common keys and values
        keys1 = set(data1.keys())
        keys2 = set(data2.keys())

        common_keys = keys1.intersection(keys2)
        total_keys = keys1.union(keys2)

        if not total_keys:
            return 0.0

        key_similarity = len(common_keys) / len(total_keys)

        # Check value similarity for common keys
        value_matches = 0
        for key in common_keys:
            if data1[key] == data2[key]:
                value_matches += 1

        value_similarity = value_matches / len(common_keys) if common_keys else 0

        # Weighted combination
        return (key_similarity * 0.4) + (value_similarity * 0.6)

    def _merge_pattern_data(self, existing_data: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[str, Any]:
        """Merge new pattern data with existing data"""

        merged = existing_data.copy()

        # Add new keys
        for key, value in new_data.items():
            if key not in merged:
                merged[key] = value
            elif isinstance(value, list) and isinstance(merged[key], list):
                # Merge lists, avoiding duplicates
                merged[key] = list(set(merged[key] + value))
            elif isinstance(value, dict) and isinstance(merged[key], dict):
                # Merge dictionaries recursively
                merged[key] = {**merged[key], **value}

        return merged

    async def _create_recommendation(
        self,
        pattern: LearnedPattern,
        target_feature: str,
        context: Dict[str, Any] = None
    ) -> Optional[Dict[str, Any]]:
        """Create a recommendation based on a learned pattern"""

        # Calculate applicability score
        applicability_score = self._calculate_applicability(pattern, target_feature, context)

        if applicability_score < 0.3:
            return None

        # Adjust confidence based on cross-feature usage
        adjusted_confidence = pattern.confidence
        if "cross_feature_usage" in pattern.metadata:
            cross_usage = pattern.metadata["cross_feature_usage"].get(target_feature, {})
            if cross_usage.get("usage_count", 0) > 0:
                success_rate = cross_usage.get("success_count", 0) / cross_usage["usage_count"]
                adjusted_confidence = (adjusted_confidence + success_rate) / 2

        final_confidence = adjusted_confidence * applicability_score

        return {
            "pattern_id": pattern.pattern_id,
            "pattern_type": pattern.pattern_type.value,
            "source_feature": pattern.source_feature,
            "confidence": final_confidence,
            "applicability_score": applicability_score,
            "usage_count": pattern.usage_count,
            "description": self._generate_recommendation_description(pattern),
            "suggested_action": self._generate_suggested_action(pattern, target_feature),
            "metadata": {
                "created_at": pattern.created_at.isoformat(),
                "last_used": pattern.last_used_at.isoformat(),
                "pattern_data_preview": self._summarize_pattern_data(pattern.pattern_data)
            }
        }

    def _calculate_applicability(
        self,
        pattern: LearnedPattern,
        target_feature: str,
        context: Dict[str, Any] = None
    ) -> float:
        """Calculate how applicable a pattern is to a target feature"""

        base_score = 0.5

        # Feature similarity boost
        if pattern.source_feature and target_feature:
            if pattern.source_feature == target_feature:
                base_score += 0.3
            elif self._features_are_related(pattern.source_feature, target_feature):
                base_score += 0.2

        # Context relevance boost
        if context and pattern.pattern_data:
            context_relevance = self._calculate_context_relevance(pattern.pattern_data, context)
            base_score += context_relevance * 0.3

        # Usage history boost
        if pattern.usage_count > 5:
            base_score += 0.1

        return min(base_score, 1.0)

    def _features_are_related(self, feature1: str, feature2: str) -> bool:
        """Determine if two features are related"""

        # Simple relatedness check based on feature names
        feature_groups = [
            ["issues", "github", "project"],
            ["cli", "command", "terminal"],
            ["workflow", "automation", "orchestration"],
            ["query", "search", "find"]
        ]

        for group in feature_groups:
            if any(f in feature1.lower() for f in group) and any(f in feature2.lower() for f in group):
                return True

        return False

    def _calculate_context_relevance(self, pattern_data: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Calculate relevance of pattern data to current context"""

        common_keys = set(pattern_data.keys()).intersection(set(context.keys()))
        if not common_keys:
            return 0.0

        matching_values = 0
        for key in common_keys:
            if pattern_data[key] == context[key]:
                matching_values += 1

        return matching_values / len(common_keys)

    def _generate_recommendation_description(self, pattern: LearnedPattern) -> str:
        """Generate human-readable description for a recommendation"""

        descriptions = {
            PatternType.USER_WORKFLOW: f"Users typically follow a workflow pattern involving {len(pattern.pattern_data.get('steps', []))} steps",
            PatternType.COMMAND_SEQUENCE: f"Common command sequence with {pattern.usage_count} recorded uses",
            PatternType.ERROR_RESOLUTION: f"Proven error resolution pattern with {pattern.success_count} successful applications",
            PatternType.CONTEXTUAL_PREFERENCE: f"User preference pattern observed in {pattern.source_feature}",
            PatternType.TIMING_PATTERN: f"Timing pattern with {pattern.confidence:.1%} confidence",
            PatternType.COLLABORATION_PATTERN: f"Collaboration pattern from {pattern.source_feature} feature"
        }

        return descriptions.get(pattern.pattern_type, f"Learned pattern from {pattern.source_feature}")

    def _generate_suggested_action(self, pattern: LearnedPattern, target_feature: str) -> str:
        """Generate suggested action based on pattern"""

        actions = {
            PatternType.USER_WORKFLOW: "Consider implementing similar workflow steps",
            PatternType.COMMAND_SEQUENCE: "Suggest this command sequence to users",
            PatternType.ERROR_RESOLUTION: "Apply this resolution strategy for similar errors",
            PatternType.CONTEXTUAL_PREFERENCE: "Adapt interface based on this preference pattern",
            PatternType.TIMING_PATTERN: "Optimize timing based on this pattern",
            PatternType.COLLABORATION_PATTERN: "Enable similar collaboration features"
        }

        return actions.get(pattern.pattern_type, "Consider applying insights from this pattern")

    def _summarize_pattern_data(self, pattern_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of pattern data for recommendations"""

        summary = {}

        for key, value in pattern_data.items():
            if isinstance(value, list):
                summary[key] = f"List with {len(value)} items"
            elif isinstance(value, dict):
                summary[key] = f"Object with {len(value)} properties"
            elif isinstance(value, str) and len(value) > 50:
                summary[key] = value[:47] + "..."
            else:
                summary[key] = value

        return summary
```

### Pattern Repository Implementation

```python
class PatternRepository:
    """Repository for storing and retrieving learned patterns"""

    def __init__(self, database_session_factory):
        self.session_factory = database_session_factory

    async def create_pattern(self, pattern: LearnedPattern) -> LearnedPattern:
        """Store a new learned pattern"""
        async with self.session_factory.session_scope() as session:
            # Convert to database model and save
            db_pattern = self._to_db_model(pattern)
            session.add(db_pattern)
            await session.flush()
            return pattern

    async def get_patterns(
        self,
        pattern_type: Optional[PatternType] = None,
        source_feature: Optional[str] = None,
        min_confidence: float = 0.0,
        limit: int = 50
    ) -> List[LearnedPattern]:
        """Retrieve patterns based on criteria"""
        async with self.session_factory.session_scope() as session:
            query = session.query(LearnedPatternModel)

            if pattern_type:
                query = query.filter(LearnedPatternModel.pattern_type == pattern_type.value)

            if source_feature:
                query = query.filter(LearnedPatternModel.source_feature == source_feature)

            query = query.filter(LearnedPatternModel.confidence >= min_confidence)
            query = query.order_by(LearnedPatternModel.confidence.desc())
            query = query.limit(limit)

            db_patterns = await query.all()
            return [self._from_db_model(p) for p in db_patterns]

    async def update_pattern(self, pattern: LearnedPattern):
        """Update an existing pattern"""
        async with self.session_factory.session_scope() as session:
            db_pattern = await session.get(LearnedPatternModel, pattern.pattern_id)
            if db_pattern:
                self._update_db_model(db_pattern, pattern)

    async def delete_pattern(self, pattern_id: str):
        """Delete a pattern"""
        async with self.session_factory.session_scope() as session:
            db_pattern = await session.get(LearnedPatternModel, pattern_id)
            if db_pattern:
                await session.delete(db_pattern)

    def _to_db_model(self, pattern: LearnedPattern):
        """Convert LearnedPattern to database model"""
        # Implementation depends on your ORM
        pass

    def _from_db_model(self, db_pattern) -> LearnedPattern:
        """Convert database model to LearnedPattern"""
        # Implementation depends on your ORM
        pass
```

### Usage Examples

```python
# Initialize cross-feature learning system
learning_engine = CrossFeatureLearningEngine(
    pattern_repository=PatternRepository(session_factory),
    confidence_threshold=0.4
)

# Learn a pattern from user workflow
async def learn_from_user_action(feature_name: str, user_action: Dict[str, Any]):
    """Learn pattern from user action"""

    # Extract pattern from user action
    pattern_data = {
        "action_sequence": user_action.get("sequence", []),
        "context": user_action.get("context", {}),
        "timing": user_action.get("timing_ms", 0),
        "outcome": user_action.get("outcome", "unknown")
    }

    # Learn the pattern
    pattern = await learning_engine.learn_pattern(
        pattern_type=PatternType.USER_WORKFLOW,
        source_feature=feature_name,
        pattern_data=pattern_data,
        initial_confidence=0.6,
        metadata={"user_id": user_action.get("user_id")}
    )

    return pattern

# Get recommendations for a feature
async def get_feature_recommendations(feature_name: str, context: Dict[str, Any]):
    """Get cross-feature recommendations"""

    # Get learned patterns for this feature
    patterns = await learning_engine.get_patterns_for_feature(
        feature_name=feature_name,
        min_confidence=0.4,
        limit=5
    )

    # Get cross-feature insights
    insights = await learning_engine.get_cross_feature_insights(
        target_feature=feature_name,
        context=context
    )

    return {
        "feature_patterns": patterns,
        "cross_feature_insights": insights,
        "total_recommendations": len(patterns) + len(insights["recommendations"])
    }

# Record pattern usage and success
async def record_pattern_success(pattern_id: str, feature_name: str, success: bool):
    """Record whether a pattern recommendation was successful"""

    await learning_engine.record_pattern_usage(
        pattern_id=pattern_id,
        feature_name=feature_name,
        success=success,
        context={"timestamp": datetime.utcnow().isoformat()}
    )

# Periodic maintenance
async def maintain_learning_system():
    """Perform periodic maintenance on learning system"""

    # Apply pattern decay
    await learning_engine.apply_pattern_decay()

    # Clean up old patterns (implementation specific)
    # await learning_engine.cleanup_old_patterns(days_old=90)
```

## Usage Guidelines

### Learning Design Principles

- **Capture from Real Usage**: Learn patterns from actual user behavior, not synthetic or test data
- **Confidence Indicators**: Use confidence scores to indicate pattern reliability and success rates
- **Feature Isolation**: Maintain feature boundaries while enabling pattern sharing across features
- **Usage Validation**: Track pattern usage and success rates for continuous improvement
- **Pattern Decay**: Implement time-based decay for outdated patterns that may no longer be relevant

### Integration Best Practices

- **User Action Learning**: Learn from user actions and decisions, not just data patterns
- **Confidence-Based Recommendations**: Provide confidence indicators with all pattern recommendations
- **Cross-Feature Discovery**: Enable pattern discovery across feature boundaries while respecting privacy
- **Feedback Loops**: Support pattern refinement through success/failure feedback
- **Privacy Preservation**: Ensure user privacy is maintained in cross-feature pattern sharing

### Pattern Management

- **Similarity Detection**: Avoid duplicate patterns by detecting and merging similar patterns
- **Applicability Scoring**: Calculate how applicable patterns are to different features and contexts
- **Regular Maintenance**: Apply periodic pattern decay and cleanup to maintain system health
- **Performance Monitoring**: Track learning system performance and pattern recommendation effectiveness

## Benefits

- Enables intelligent automation and recommendations across feature boundaries
- Reduces redundant learning efforts by sharing insights between features
- Provides confidence-based recommendations for reliable pattern application
- Maintains feature isolation while enabling cross-feature knowledge transfer
- Adapts to changing user behavior through continuous learning and pattern decay
- Improves user experience through intelligent pattern recognition and automation

## Trade-offs

- Additional complexity in pattern storage, retrieval, and management systems
- Privacy considerations when sharing patterns across feature boundaries
- Performance overhead from pattern similarity detection and confidence calculations
- Need for careful tuning of confidence thresholds and decay parameters
- Storage requirements for maintaining pattern history and metadata
- Complexity in determining cross-feature pattern applicability

## Anti-patterns to Avoid

- ❌ **Synthetic Data Learning**: Learning from synthetic, test, or artificially generated data
- ❌ **High Confidence Without Evidence**: Assigning high confidence scores without sufficient usage data
- ❌ **Feature Silos**: Creating isolated learning systems that prevent beneficial cross-learning
- ❌ **Patterns Without Confidence**: Providing pattern recommendations without confidence indicators
- ❌ **Missing Feedback Loops**: Not implementing mechanisms for pattern validation and refinement
- ❌ **Privacy Violations**: Sharing sensitive user data across features without proper safeguards

## Related Patterns

- [Pattern-025: Canonical Query Extension Pattern](pattern-025-canonical-query-extension.md) - Learning system integration for query enhancement
- [Pattern-023: Query Layer Patterns](pattern-023-query-layer-patterns.md) - A/B testing and learning integration
- [Pattern-012: LLM Adapter Pattern](pattern-012-llm-adapter.md) - Provider-agnostic learning and adaptation
- [Pattern-021: Development Session Management Pattern](pattern-021-development-session-management.md) - Learning from development patterns

## References

- **Implementation**: CrossFeatureLearningEngine with pattern repository and confidence tracking
- **Usage Evidence**: Pattern learning from actual user workflows and cross-feature insights
- **Performance Monitoring**: Pattern decay, confidence updates, and applicability scoring
- **Related ADR**: Learning system architecture and cross-feature data sharing policies

## Migration Notes

*Consolidated from:*
- `pattern-catalog.md#26-cross-feature-learning-pattern` - Complete learning framework with confidence-based recommendations
- Pattern sharing across feature boundaries while maintaining isolation
- Usage-driven learning from actual user behavior with feedback loops
- Cross-feature insight generation and pattern applicability scoring

*Last updated: September 15, 2025*
