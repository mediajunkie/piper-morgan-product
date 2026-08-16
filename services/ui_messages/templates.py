# Create a new module for centralized message templates

from typing import Dict, Optional, Tuple
from uuid import UUID

from services.shared_types import IntentCategory, WorkflowType
from services.ui_messages.action_humanizer import ActionHumanizer

# Import personality enhancement if available
try:
    from services.personality.personality_profile import (
        PersonalityProfile,
        ResponseContext,
        ResponseType,
    )

    PERSONALITY_AVAILABLE = True
except ImportError:
    PERSONALITY_AVAILABLE = False
    ResponseType = None

# Primary templates keyed by (category, action)
INTENT_BASED_TEMPLATES = {
    # ANALYSIS intents
    ("analysis", "investigate_issue"): "Here's my analysis of the reported issue:",
    ("analysis", "investigate_crash"): "Here's my analysis of the reported issue:",
    ("analysis", "performance_analysis"): "Here's my performance analysis:",
    ("analysis", "performance_investigation"): "Here's my performance analysis:",
    ("analysis", "analyze_metrics"): "Here's my analysis of the metrics:",
    ("analysis", "analyze_document"): "Here's my analysis of {filename}:",
    ("analysis", "analyze_file"): "Here's my analysis:",
    # SYNTHESIS intents
    # #1624: the ("synthesis", "summarize_document") / ("synthesis",
    # "summarize_file") rows were DELETED — they templated a #290 chat flow
    # that never fired (the dispatch shipped only in a guidance doc, 2025-11);
    # the real chat summarize (workflow rail, 2026-08) renders its own message.
    # History: summarize-intent-forensics-2026-08-15.md, "vestige pair".
    ("synthesis", "generate_report"): "Here's the generated report:",
    # EXECUTION intents
    (
        "execution",
        "create_ticket",
    ): "✅ Successfully created GitHub issue #{issue_number}:",
    ("execution", "create_task"): "✅ Successfully created task:",
    ("execution", "create_feature"): "✅ Successfully created feature:",
    # QUERY intents
    ("query", "list_projects"): "Here are your projects:",
    ("query", "count_projects"): "Project count:",
    # LEARNING intents
    ("learning", "learn_pattern"): "Here's what I learned:",
    ("learning", "extract_insights"): "Key insights discovered:",
}

# Fallback templates by workflow type
WORKFLOW_BASED_TEMPLATES = {
    WorkflowType.GENERATE_REPORT: "Here's my analysis:",
    WorkflowType.CREATE_TICKET: "✅ Task completed successfully:",
    WorkflowType.ANALYZE_FILE: "Here's my file analysis:",
    # Add more as needed
}

# Generic fallbacks
DEFAULT_TEMPLATES = {
    "success": "Workflow completed successfully!",
    "in_progress": "Working on your request...",
    "failed": "I encountered an issue: {error}",
}


def get_message_template(
    intent_category: Optional[str] = None,
    intent_action: Optional[str] = None,
    workflow_type: Optional[WorkflowType] = None,
) -> str:
    """Get appropriate message template based on context"""
    # Try intent-based template first
    if intent_category and intent_action:
        key = (intent_category, intent_action)
        if key in INTENT_BASED_TEMPLATES:
            return INTENT_BASED_TEMPLATES[key]
    # Fall back to workflow type
    if workflow_type and workflow_type in WORKFLOW_BASED_TEMPLATES:
        return WORKFLOW_BASED_TEMPLATES[workflow_type]
    # Default fallback
    return DEFAULT_TEMPLATES["success"]


class TemplateRenderer:
    """Enhanced template rendering with action humanization and personality enhancement"""

    def __init__(self, humanizer: Optional[ActionHumanizer] = None):
        self.humanizer = humanizer
        self._personality_enhancer = None

    async def render_template(
        self,
        template: str,
        intent_action: str,
        intent_category: Optional[str] = None,
        personality_profile: Optional["PersonalityProfile"] = None,
        user_id: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Render template with humanized action and personality enhancement"""

        # Humanize the action if it appears in the template
        try:
            if template and isinstance(template, str) and "{human_action}" in template:
                if self.humanizer:
                    human_action = await self.humanizer.humanize(intent_action, intent_category)
                else:
                    # Fallback when humanizer not available
                    human_action = intent_action
                kwargs["human_action"] = human_action
        except (TypeError, AttributeError) as e:
            # Handle template type errors gracefully
            import logging

            logging.getLogger(__name__).warning(f"Template humanization check failed: {e}")

        # Always preserve the original action
        kwargs["action"] = intent_action

        # Format template with error handling
        try:
            if template is None:
                # Handle None template gracefully
                rendered = f"Response for {intent_action}"
                import logging

                logging.getLogger(__name__).warning("Template was None, using fallback")
            elif not isinstance(template, str):
                # Handle non-string templates gracefully
                rendered = f"Response for {intent_action}"
                import logging

                logging.getLogger(__name__).warning(
                    f"Template was not a string ({type(template)}), using fallback"
                )
            else:
                rendered = template.format(**kwargs)
        except (KeyError, ValueError, TypeError, AttributeError) as e:
            # Handle template formatting errors gracefully
            rendered = template if isinstance(template, str) else f"Response for {intent_action}"
            import logging

            logging.getLogger(__name__).warning(
                f"Template formatting failed: {e}, using original template"
            )

        # Apply personality enhancement using the new ResponsePersonalityEnhancer
        if PERSONALITY_AVAILABLE and user_id:
            try:
                # Import the new personality system
                from services.personality.cache import ProfileCache
                from services.personality.personality_profile import ResponseContext, ResponseType
                from services.personality.repository import PersonalityProfileRepository
                from services.personality.response_enhancer import ResponsePersonalityEnhancer

                # Create enhancer instance (in production, this would be dependency injected)
                repository = PersonalityProfileRepository()
                cache = ProfileCache()
                enhancer = ResponsePersonalityEnhancer(repository, profile_cache=cache)

                # Create response context from template rendering context
                context = ResponseContext(
                    response_type=self._determine_response_type(intent_category, intent_action),
                    intent_confidence=kwargs.get("intent_confidence", 0.7),  # Default confidence
                    intent_category=intent_category or "general",
                    intent_action=intent_action,
                    original_message=template,
                )

                # Enhance the rendered content
                enhancement_result = await enhancer.enhance_response(
                    content=rendered, context=context, user_id=user_id
                )

                # Use enhanced content if successful
                if enhancement_result.success and enhancement_result.enhanced_content != rendered:
                    return enhancement_result.enhanced_content

            except Exception as e:
                # Graceful degradation - log error but continue with original
                import logging

                logging.getLogger(__name__).warning(f"Personality enhancement failed: {e}")

        return rendered

    def _determine_response_type(self, intent_category: Optional[str], intent_action: str):
        """Determine response type from intent information"""
        if not PERSONALITY_AVAILABLE or not ResponseType:
            return None

        # ResponseType is for interface types, not content types
        # Default to CLI for main.py context, could be enhanced with actual interface detection
        return ResponseType.CLI
