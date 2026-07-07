"""
PM-034: LLM-Based Intent Classification with Knowledge Graph Context

This module implements an advanced intent classifier that leverages:
1. LLM for natural language understanding
2. PM-040 Knowledge Graph for context enrichment
3. Multi-stage pipeline with confidence scoring
4. Graceful degradation to rule-based patterns
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import structlog

from services.api.errors import IntentClassificationFailedError, LowConfidenceIntentError
from services.domain.models import Intent, IntentCategory, KnowledgeNode
from services.intent_service.fuzzy_matcher import correct_common_typos
from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.knowledge.semantic_indexing_service import SemanticIndexingService
from services.shared_types import NodeType

logger = structlog.get_logger()


class LLMIntentClassifier:
    """
    Advanced intent classifier using LLM with Knowledge Graph context

    Features:
    - Multi-stage classification pipeline
    - Knowledge Graph context enrichment
    - Confidence scoring and validation
    - Performance tracking and learning
    - Graceful degradation to rule-based fallback
    """

    def __init__(
        self,
        llm_service=None,
        knowledge_graph_service: Optional[KnowledgeGraphService] = None,
        semantic_indexing_service: Optional[SemanticIndexingService] = None,
        confidence_threshold: float = 0.75,
        enable_learning: bool = True,
    ):
        """
        Initialize LLMIntentClassifier.

        Args:
            llm_service: LLM service instance (optional, will get from container if not provided)
            knowledge_graph_service: Optional Knowledge Graph service
            semantic_indexing_service: Optional Semantic Indexing service
            confidence_threshold: Minimum confidence score for classification
            enable_learning: Enable performance tracking and learning
        """
        self._llm = llm_service  # Accept via dependency injection
        self.knowledge_graph = knowledge_graph_service
        self.semantic_indexer = semantic_indexing_service
        self.confidence_threshold = confidence_threshold
        self.enable_learning = enable_learning

        # Performance tracking
        self.classification_metrics = {
            "total_requests": 0,
            "successful_classifications": 0,
            "low_confidence_fallbacks": 0,
            "average_latency_ms": 0,
        }

    @property
    def llm(self):
        """Lazy-load LLM service from ServiceContainer if not injected.

        DEPRECATION WARNING (Issue #322):
        Direct ServiceContainer() access is deprecated. Pass llm_service
        via constructor instead. This fallback will be removed when
        horizontal scaling is enabled.
        """
        if self._llm is None:
            import warnings

            from services.container import ServiceContainer

            warnings.warn(
                "LLMIntentClassifier: Direct ServiceContainer() access is deprecated. "
                "Pass llm_service via constructor. (Issue #322 - ARCH-FIX-SINGLETON)",
                DeprecationWarning,
                stacklevel=2,
            )
            container = ServiceContainer()
            self._llm = container.get_service("llm")
        return self._llm

    def _ensure_json_response_format(self, **kwargs):
        """Ensure response_format is always set for JSON responses"""
        if "response_format" not in kwargs:
            logger.warning("response_format missing - adding default JSON object format")
            kwargs["response_format"] = {"type": "json_object"}

        # Verify the format is correct
        format_val = kwargs.get("response_format")
        if not isinstance(format_val, dict) or format_val.get("type") != "json_object":
            logger.warning(f"Invalid response_format: {format_val} - correcting to json_object")
            kwargs["response_format"] = {"type": "json_object"}

        return kwargs

    async def classify(
        self,
        message: str,
        user_context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> Intent:
        """
        Classify user message into intent with multi-stage pipeline

        Args:
            message: User's natural language input
            user_context: Optional context about user/session
            session_id: Optional session identifier for context
            user_id: Optional resolved principal (ADR-075 D4) — scopes the
                classification system prompt to this user's personalization
                rather than the unscoped file, when provided.

        Returns:
            Intent with category, action, and confidence score
        """
        start_time = datetime.now()
        self.classification_metrics["total_requests"] += 1
        self.current_message = message  # Store for retry functionality
        self.current_user_id = user_id  # ADR-075 D4: same pattern, for the retry path's prompt

        try:
            # Stage 1: Pre-processing
            processed_message = await self._preprocess_message(message)

            # Stage 2: Knowledge Graph context enrichment
            context = await self._enrich_with_knowledge_graph(
                processed_message, user_context, session_id
            )

            # Stage 3: LLM classification
            classification_result = await self._llm_classify(processed_message, context)

            # Stage 4: Confidence validation
            validated_intent = await self._validate_confidence(
                classification_result, processed_message
            )

            # Stage 5: Performance tracking
            if self.enable_learning:
                await self._track_performance(validated_intent, start_time, success=True)

            self.classification_metrics["successful_classifications"] += 1
            return validated_intent

        except LowConfidenceIntentError:
            # Graceful degradation to rule-based fallback
            self.classification_metrics["low_confidence_fallbacks"] += 1
            logger.warning("Low confidence classification, using fallback")
            raise

        except Exception as e:
            logger.error(f"Intent classification failed: {e}")
            await self._track_performance(None, start_time, success=False)
            raise IntentClassificationFailedError(str(e))

    async def _preprocess_message(self, message: str) -> str:
        """Stage 1: Pre-process and clean user message"""
        # Remove extra whitespace
        cleaned = " ".join(message.split())

        # Validate non-empty (Issue #514: Empty messages should fail classification)
        if not cleaned:
            raise IntentClassificationFailedError("Cannot classify empty message")

        # Correct common typos
        corrected = correct_common_typos(cleaned)

        logger.debug(f"Preprocessed message: '{message}' -> '{corrected}'")
        return corrected

    async def _enrich_with_knowledge_graph(
        self,
        message: str,
        user_context: Optional[Dict[str, Any]],
        session_id: Optional[str],
    ) -> Dict[str, Any]:
        """Stage 2: Enrich context using Knowledge Graph"""
        context = {
            "message": message,
            "user_context": user_context or {},
            "timestamp": datetime.now().isoformat(),
        }

        if not self.knowledge_graph or not self.semantic_indexer:
            logger.debug("Knowledge Graph not available, using basic context")
            return context

        try:
            # Find similar intents from past interactions
            similar_intents = await self._find_similar_intents(message, session_id)
            context["similar_intents"] = similar_intents

            # Get user's recent interaction patterns
            if session_id:
                user_patterns = await self._get_user_patterns(session_id)
                context["user_patterns"] = user_patterns

            # Extract relevant domain knowledge
            domain_knowledge = await self._extract_domain_knowledge(message)
            context["domain_knowledge"] = domain_knowledge

            logger.debug(f"Enriched context with {len(similar_intents)} similar intents")

        except Exception as e:
            logger.warning(f"Knowledge Graph enrichment failed: {e}")
            # Continue with basic context

        return context

    async def _find_similar_intents(
        self, message: str, session_id: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Find similar intents from Knowledge Graph"""
        if not self.semantic_indexer:
            return []

        # Create a temporary node for the message
        query_node = KnowledgeNode(
            name=message[:50],  # Truncate for name
            node_type=NodeType.CONCEPT,
            metadata={"message": message, "type": "intent_query"},
            session_id=session_id,
        )

        # Search for similar nodes
        similar_nodes = await self.semantic_indexer.similarity_search(
            query_node=query_node,
            top_k=5,
            threshold=0.7,
            node_types=[NodeType.CONCEPT, NodeType.PROCESS],
        )

        # Extract intent patterns from similar nodes
        similar_intents = []
        for node, similarity in similar_nodes:
            if "intent" in node.metadata:
                similar_intents.append(
                    {
                        "intent": node.metadata["intent"],
                        "confidence": node.metadata.get("confidence", 0.0),
                        "similarity": similarity,
                    }
                )

        return similar_intents

    async def _get_user_patterns(self, session_id: str) -> Dict[str, Any]:
        """Get user's interaction patterns from Knowledge Graph"""
        if not self.knowledge_graph:
            return {}

        # Get recent nodes from this session
        recent_nodes = await self.knowledge_graph.get_nodes_by_type(
            node_type=NodeType.EVENT,
            session_id=session_id,
            limit=10,
        )

        # Analyze patterns
        patterns = {
            "recent_intents": [],
            "common_actions": {},
            "session_context": {},
        }

        for node in recent_nodes:
            if "intent" in node.metadata:
                patterns["recent_intents"].append(node.metadata["intent"])
            if "action" in node.metadata:
                action = node.metadata["action"]
                patterns["common_actions"][action] = patterns["common_actions"].get(action, 0) + 1

        return patterns

    async def _extract_domain_knowledge(self, message: str) -> Dict[str, Any]:
        """Extract relevant PM domain knowledge"""
        # This is a simplified version - in production, this would
        # query the Knowledge Graph for relevant PM concepts

        domain_indicators = {
            "project": ["timeline", "milestone", "deliverable"],
            "task": ["todo", "action item", "assignment"],
            "document": ["spec", "design", "requirements"],
            "analysis": ["metrics", "performance", "trends"],
        }

        detected_domains = []
        for domain, keywords in domain_indicators.items():
            if any(keyword in message.lower() for keyword in keywords):
                detected_domains.append(domain)

        return {
            "detected_domains": detected_domains,
            "pm_context": len(detected_domains) > 0,
        }

    async def _llm_classify(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 3: LLM-based classification with structured prompt"""

        # Build structured prompt
        prompt = self._build_classification_prompt(message, context)

        # Call LLM
        try:
            # Concurrent debugging: Log request parameters
            import threading
            import time

            request_id = f"{int(time.time())}-{threading.get_ident()}"
            response_format = {"type": "json_object"}

            logger.debug(f"[{request_id}] LLM request - task_type: intent_classification")
            logger.debug(f"[{request_id}] response_format parameter: {response_format}")
            logger.debug(f"[{request_id}] Prompt length: {len(prompt)} characters")

            # ADR-075 D4: resolve through the per-principal PersonalizationService
            # rather than the unscoped loader directly — #1366 leak closure.
            from services.configuration.personalization_service import (
                personalization_service,
            )

            system_prompt = await personalization_service.resolve_system_prompt_standalone(
                user_id
            )

            response = await self.llm.complete(
                task_type="intent_classification",
                prompt=prompt,
                response_format=response_format,
                system=system_prompt,
            )

            logger.debug(f"[{request_id}] LLM response received - length: {len(response)} chars")

            # Parse structured response using resilient parser
            result = await self._parse_llm_response_resilient_async(response)

            logger.debug(f"LLM classification result: {result}")
            return result

        except Exception as e:
            logger.error(f"LLM classification failed: {e}")
            raise

    def _build_classification_prompt(self, message: str, context: Dict[str, Any]) -> str:
        """Build structured prompt for LLM classification"""

        prompt_parts = [
            "You are an expert PM assistant classifying user intents.",
            "\nClassify the following message into an intent category and action.",
            f"\nMessage: {message}",
        ]

        # Add context if available
        if context.get("similar_intents"):
            prompt_parts.append("\nSimilar past intents:")
            for intent in context["similar_intents"][:3]:
                prompt_parts.append(
                    f"- {intent['intent']['category']}/{intent['intent']['action']} "
                    f"(confidence: {intent['confidence']:.2f})"
                )

        if context.get("domain_knowledge", {}).get("detected_domains"):
            prompt_parts.append(
                f"\nDetected PM domains: {', '.join(context['domain_knowledge']['detected_domains'])}"
            )

        # Add classification instructions
        # Issue #1124 Phase 4: ask for a canonical verb (closed vocabulary) + a
        # source_type slot in addition to the free-form action. The boundary in
        # _validate_confidence canonicalizes action from (verb, source_type) via the
        # transition shim when it maps; the free-form action remains the fallback.
        from services.intent_service.action_registry import Verb

        verb_vocab = ", ".join(v.value for v in Verb)
        prompt_parts.extend(
            [
                "\n\nProvide your classification in JSON format:",
                '{"category": "...", "verb": "...", "source_type": "...", '
                '"action": "...", "confidence": 0.0-1.0, "reasoning": "..."}',
                "\nCategories: execution, analysis, synthesis, strategy, learning, query, conversation, unknown",
                f"\nVerb (pick the single closest canonical verb): {verb_vocab}",
                "\nsource_type (what the verb acts on, when applicable; else null): "
                "text, conversation, github_issue, commit_range, document",
                '\nFor a summary request, emit verb="summarize" plus the source_type '
                '(e.g. "summarize github issue 42" -> verb=summarize, '
                "source_type=github_issue). Do NOT improvise a collapsed action name "
                'like "summarize_github_issue" — use the verb + source_type slot.',
                "\naction: a specific action name (used when no verb fits well).",
                "\nInclude a confidence score (0.0-1.0) and brief reasoning.",
            ]
        )

        return "\n".join(prompt_parts)

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured classification"""
        try:
            # Extract JSON from response
            json_start = response.find("{")
            json_end = response.rfind("}") + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                result = json.loads(json_str)

                # Validate required fields
                required_fields = ["category", "action", "confidence"]
                if all(field in result for field in required_fields):
                    return result

            # Fallback parsing if JSON extraction fails
            logger.warning("Failed to parse LLM response as JSON, using fallback")
            return {
                "category": "unknown",
                "action": "unclear",
                "confidence": 0.5,
                "reasoning": "Failed to parse LLM response",
            }

        except Exception as e:
            logger.error(f"Error parsing LLM response: {e}")
            return {
                "category": "unknown",
                "action": "unclear",
                "confidence": 0.0,
                "reasoning": f"Parse error: {str(e)}",
            }

    def _parse_llm_response_resilient(self, response_text: str, attempt: int = 1) -> Dict[str, Any]:
        """Parse LLM response with progressive fallback strategies

        Strategy progression:
        1. Direct JSON parse (works 95% of time)
        2. Fix common malformations (handles {category: "value"})
        3. Extract JSON from text response
        4. Retry with stronger prompt (if attempt < 3)
        5. Regex extraction fallback
        6. Final unknown intent fallback
        """
        import asyncio
        import re

        # Strategy 1: Direct JSON parse (works 95% of time)
        try:
            parsed = json.loads(response_text)
            logger.debug("Parse strategy 1 success: Direct JSON parse")
            return parsed
        except json.JSONDecodeError as e:
            logger.debug(f"Parse strategy 1 failed: {e}")
            pass

        # Strategy 2: Fix common malformations (handles {category: "value"})
        try:
            # Replace unquoted keys with quoted keys
            fixed_text = re.sub(r"(\w+):", r'"\1":', response_text)
            # Handle single quotes: {'category': 'value'} -> {"category": "value"}
            fixed_text = re.sub(r"'([^']*)'", r'"\1"', fixed_text)

            parsed = json.loads(fixed_text)
            logger.debug("Parse strategy 2 success: Fixed malformed JSON")
            return parsed
        except json.JSONDecodeError as e:
            logger.debug(f"Parse strategy 2 failed: {e}")
            pass

        # Strategy 3: Extract JSON from text response
        try:
            # LLM might return "Here's the JSON: {...}" or similar
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group()
                parsed = json.loads(json_text)
                logger.debug("Parse strategy 3 success: Extracted JSON from text")
                return parsed
        except json.JSONDecodeError as e:
            logger.debug(f"Parse strategy 3 failed: {e}")
            pass

        # Strategy 4: Retry with stronger prompt (if attempt < 3)
        if attempt < 3:
            logger.warning(
                f"All parsing strategies failed, retrying with stronger prompt (attempt {attempt + 1})"
            )
            # Note: Retry will be handled by the async caller, skip for now to avoid asyncio.run() in async context
            logger.warning("Skipping retry in sync context - proceeding to regex extraction")

        # Strategy 5: Regex extraction fallback
        try:
            category = self._extract_category_regex(response_text)
            action = self._extract_action_regex(response_text)
            confidence = self._extract_confidence_regex(response_text)

            if category and action:
                logger.warning(f"Parse strategy 5 success: Regex extraction - {category}/{action}")
                return {
                    "category": category,
                    "action": action,
                    "confidence": confidence,
                    "parse_method": "regex_fallback",
                }

        except Exception as e:
            logger.error(f"Parse strategy 5 failed: {e}")
            pass

        # Strategy 6: Final fallback - Unknown intent
        logger.error(f"All parsing strategies failed. Response text: {response_text[:200]}...")
        return {
            "category": "unknown",
            "action": "unclear",
            "confidence": 0.0,
            "parse_method": "failed",
            "original_response": response_text[:500],  # Keep sample for debugging
        }

    def _extract_category_regex(self, text: str) -> str:
        """Extract category using regex patterns"""
        import re

        patterns = [
            r'"?(?:category|intent)"?\s*:\s*"?([^",\}]+)"?',
            r"(EXECUTION|QUERY|ANALYSIS|UPDATE|SYNTHESIS|STRATEGY|LEARNING|CONVERSATION)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).upper()
        return "UNKNOWN"

    def _extract_action_regex(self, text: str) -> str:
        """Extract action using regex patterns"""
        import re

        patterns = [
            r'"?(?:action)"?\s*:\s*"?([^",\}]+)"?',
            r"(create_issue|list_projects|update_status|generate_report|create_milestone)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).lower()
        return "unknown"

    def _extract_confidence_regex(self, text: str) -> float:
        """Extract confidence using regex patterns"""
        import re

        patterns = [r'"?(?:confidence)"?\s*:\s*([0-9.]+)', r"confidence[^0-9]*([0-9.]+)"]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    conf = float(match.group(1))
                    return conf / 100.0 if conf > 1.0 else conf
                except ValueError:
                    pass
        return 0.7  # Default confidence for fallback parsing

    async def _retry_with_strict_json_prompt(self, attempt: int) -> Dict[str, Any]:
        """Retry with stronger JSON formatting instructions"""
        strict_prompt = f"""You are an intent classifier.
CRITICAL: Respond with valid JSON only. No additional text.
User message: "{getattr(self, 'current_message', 'message')}"
Response format: {{"category": "EXECUTION", "action": "create_issue", "confidence": 0.95}}
Valid categories: EXECUTION, QUERY, ANALYSIS, UPDATE, SYNTHESIS, STRATEGY, LEARNING, CONVERSATION
Respond only with valid JSON:"""

        try:
            # ADR-075 D4: same resolution as the primary attempt, keyed off the
            # user_id stashed in classify() (mirrors the existing
            # current_message retry-context pattern above).
            from services.configuration.personalization_service import (
                personalization_service,
            )

            system_prompt = await personalization_service.resolve_system_prompt_standalone(
                getattr(self, "current_user_id", None)
            )

            response = await self.llm.complete(
                task_type="intent_classification",
                prompt=strict_prompt,
                response_format={"type": "json_object"},
                system=system_prompt,
            )
            return await self._parse_llm_response_resilient_async(response, attempt)
        except Exception as e:
            logger.error(f"Retry attempt {attempt} failed: {e}")
            return self._parse_llm_response_resilient("", attempt + 10)  # Skip retry logic

    async def _parse_llm_response_resilient_async(
        self, response_text: str, attempt: int = 1
    ) -> Dict[str, Any]:
        """Async version of resilient parser with proper retry support"""
        import re

        # Strategy 1: Direct JSON parse (works 95% of time)
        try:
            parsed = json.loads(response_text)
            logger.debug("Parse strategy 1 success: Direct JSON parse")
            return parsed
        except json.JSONDecodeError as e:
            logger.debug(f"Parse strategy 1 failed: {e}")
            pass

        # Strategy 2: Fix common malformations (handles {category: "value"})
        try:
            # Replace unquoted keys with quoted keys
            fixed_text = re.sub(r"(\w+):", r'"\1":', response_text)
            # Handle single quotes: {'category': 'value'} -> {"category": "value"}
            fixed_text = re.sub(r"'([^']*)'", r'"\1"', fixed_text)

            parsed = json.loads(fixed_text)
            logger.debug("Parse strategy 2 success: Fixed malformed JSON")
            return parsed
        except json.JSONDecodeError as e:
            logger.debug(f"Parse strategy 2 failed: {e}")
            pass

        # Strategy 3: Extract JSON from text response
        try:
            # LLM might return "Here's the JSON: {...}" or similar
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group()
                parsed = json.loads(json_text)
                logger.debug("Parse strategy 3 success: Extracted JSON from text")
                return parsed
        except json.JSONDecodeError as e:
            logger.debug(f"Parse strategy 3 failed: {e}")
            pass

        # Strategy 4: Retry with stronger prompt (if attempt < 3)
        if attempt < 3:
            logger.warning(
                f"All parsing strategies failed, retrying with stronger prompt (attempt {attempt + 1})"
            )
            retry_result = await self._retry_with_strict_json_prompt(attempt + 1)
            return retry_result

        # Strategy 5: Regex extraction fallback
        try:
            category = self._extract_category_regex(response_text)
            action = self._extract_action_regex(response_text)
            confidence = self._extract_confidence_regex(response_text)

            if category and action:
                logger.warning(f"Parse strategy 5 success: Regex extraction - {category}/{action}")
                return {
                    "category": category,
                    "action": action,
                    "confidence": confidence,
                    "parse_method": "regex_fallback",
                }

        except Exception as e:
            logger.error(f"Parse strategy 5 failed: {e}")
            pass

        # Strategy 6: Final fallback - Unknown intent
        logger.error(f"All parsing strategies failed. Response text: {response_text[:200]}...")
        return {
            "category": "unknown",
            "action": "unclear",
            "confidence": 0.0,
            "parse_method": "failed",
            "original_response": response_text[:500],  # Keep sample for debugging
        }

    async def _validate_confidence(
        self, classification_result: Dict[str, Any], original_message: str
    ) -> Intent:
        """Stage 4: Validate classification confidence"""

        confidence = classification_result.get("confidence", 0.0)

        if confidence < self.confidence_threshold:
            logger.warning(
                f"Low confidence classification ({confidence:.2f}): "
                f"{classification_result.get('category')}/{classification_result.get('action')}"
            )
            raise LowConfidenceIntentError(
                f"Classification confidence {confidence:.2f} below threshold {self.confidence_threshold}"
            )

        # Issue #1124 Phase 4: the prompt now emits a canonical verb (+ source_type).
        # When the verb maps via the transition shim, canonicalize intent.action to
        # the legacy string consumers already branch on; otherwise keep the free-form
        # action (zero-regression fallback). source_type rides into intent.context
        # (where _handle_summarize reads it).
        from services.intent_service.action_registry import (
            Verb,
            verb_sourcetype_to_legacy_action,
        )

        action = classification_result["action"]
        source_type = classification_result.get("source_type")
        if isinstance(source_type, str):
            source_type = source_type.strip()
            if source_type.lower() in ("", "null", "none", "n/a"):
                source_type = None
        else:
            source_type = None

        verb_str = classification_result.get("verb")
        if verb_str:
            try:
                verb = Verb(str(verb_str).strip().lower())
            except ValueError:
                verb = None
            if verb is not None:
                legacy_action = verb_sourcetype_to_legacy_action(verb, source_type)
                if legacy_action:
                    action = legacy_action

        intent_context = {
            "reasoning": classification_result.get("reasoning", ""),
            "llm_classified": True,
        }
        if source_type:
            intent_context["source_type"] = source_type

        # Create Intent object
        try:
            intent = Intent(
                original_message=original_message,
                category=IntentCategory(classification_result["category"].lower()),
                action=action,
                confidence=confidence,
                context=intent_context,
            )

            # Store in Knowledge Graph if available
            if self.knowledge_graph and self.enable_learning:
                await self._store_classification(intent, classification_result)

            return intent

        except ValueError as e:
            logger.error(f"Invalid intent category: {classification_result.get('category')}")
            raise IntentClassificationFailedError(str(e))

    async def _store_classification(
        self, intent: Intent, classification_result: Dict[str, Any]
    ) -> None:
        """Store successful classification in Knowledge Graph for learning"""
        try:
            # Create node for this classification
            node = await self.knowledge_graph.create_node(
                name=f"intent_classification_{datetime.now().isoformat()}",
                node_type=NodeType.EVENT,
                metadata={
                    "intent": {
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    "message": intent.original_message,
                    "reasoning": classification_result.get("reasoning", ""),
                    "timestamp": datetime.now().isoformat(),
                },
                session_id=None,  # Intent doesn't have session_id field
            )

            logger.debug(f"Stored classification in Knowledge Graph: {node.id}")

        except Exception as e:
            logger.warning(f"Failed to store classification: {e}")
            # Continue without storing

    async def _track_performance(
        self,
        intent: Optional[Intent],
        start_time: datetime,
        success: bool,
    ) -> None:
        """Stage 5: Track classification performance"""

        # Calculate latency
        latency_ms = (datetime.now() - start_time).total_seconds() * 1000

        # Update running average
        total = self.classification_metrics["total_requests"]
        avg = self.classification_metrics["average_latency_ms"]
        self.classification_metrics["average_latency_ms"] = (avg * (total - 1) + latency_ms) / total

        # Log performance
        logger.info(
            "intent_classification_performance",
            success=success,
            latency_ms=latency_ms,
            category=intent.category.value if intent else None,
            action=intent.action if intent else None,
            confidence=intent.confidence if intent else None,
        )

    def get_metrics(self) -> Dict[str, Any]:
        """Get classification performance metrics"""
        metrics = self.classification_metrics.copy()

        # Calculate success rate
        if metrics["total_requests"] > 0:
            metrics["success_rate"] = (
                metrics["successful_classifications"] / metrics["total_requests"]
            )
            metrics["fallback_rate"] = (
                metrics["low_confidence_fallbacks"] / metrics["total_requests"]
            )
        else:
            metrics["success_rate"] = 0.0
            metrics["fallback_rate"] = 0.0

        return metrics
