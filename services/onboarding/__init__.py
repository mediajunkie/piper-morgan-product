# onboarding module
"""
Portfolio onboarding services for first-time user experience.

Issue #490: FTUX-PORTFOLIO - Project Portfolio Onboarding
Epic: FTUX (First Time User Experience)

This module provides:
- FirstMeetingDetector: Detects when user has no projects and should be offered onboarding
- PortfolioOnboardingManager: State machine for project setup conversation
- PortfolioOnboardingHandler: Turn-by-turn conversation handling

Grammar Components (Issue #626):
- OnboardingGrammarContext: Rich context for grammar-conscious responses
- OnboardingStage: Enum for onboarding stages
- OnboardingNarrativeBridge: Transform context into phrases
- Narrative helpers: get_welcome_message, acknowledge_project, etc.
"""

from services.onboarding.first_meeting_detector import FirstMeetingDetector

# Issue #626: Grammar-conscious response components
from services.onboarding.grammar_context import OnboardingGrammarContext, OnboardingStage
from services.onboarding.narrative_bridge import OnboardingNarrativeBridge
from services.onboarding.narrative_helpers import (
    acknowledge_project,
    celebrate_completion,
    create_onboarding_context,
    get_add_more_prompt,
    get_confirmation_prompt,
    get_more_projects_prompt,
    get_need_project_message,
    get_onboarding_formality,
    get_session_lost_message,
    get_unclear_response_prompt,
    get_welcome_message,
    handle_decline_warmly,
    is_warm_onboarding,
)
from services.onboarding.portfolio_handler import OnboardingResponse, PortfolioOnboardingHandler
from services.onboarding.portfolio_manager import (
    InvalidStateTransitionError,
    PortfolioOnboardingManager,
)
from services.onboarding.portfolio_service import (
    ARCHIVE_INSTEAD_PATTERNS,
    ARCHIVE_PATTERNS,
    DELETE_PATTERNS,
    PERMANENT_DELETE_PATTERNS,
    RESTORE_PATTERNS,
    PortfolioActionResult,
    PortfolioResult,
    PortfolioService,
    clean_project_name,
)

__all__ = [
    # Core onboarding
    "FirstMeetingDetector",
    "InvalidStateTransitionError",
    "OnboardingResponse",
    "PortfolioOnboardingHandler",
    "PortfolioOnboardingManager",
    # Grammar context
    "OnboardingGrammarContext",
    "OnboardingStage",
    "OnboardingNarrativeBridge",
    # Narrative helpers
    "get_welcome_message",
    "acknowledge_project",
    "get_more_projects_prompt",
    "get_confirmation_prompt",
    "celebrate_completion",
    "handle_decline_warmly",
    "get_session_lost_message",
    "get_need_project_message",
    "get_add_more_prompt",
    "get_unclear_response_prompt",
    "get_onboarding_formality",
    "is_warm_onboarding",
    "create_onboarding_context",
    # Portfolio service (#569)
    "ARCHIVE_INSTEAD_PATTERNS",
    "ARCHIVE_PATTERNS",
    "DELETE_PATTERNS",
    "PERMANENT_DELETE_PATTERNS",
    "RESTORE_PATTERNS",
    "PortfolioActionResult",
    "PortfolioResult",
    "PortfolioService",
    "clean_project_name",
]
