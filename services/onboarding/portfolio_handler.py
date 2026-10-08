"""
Issue #490: Portfolio onboarding conversation handler.

Epic: FTUX (First Time User Experience)

Handles turn-by-turn conversation for portfolio onboarding,
following the pattern established by StandupConversationHandler (Epic #242).

Responsible for:
- Starting onboarding conversations
- Processing user responses
- Extracting project information from natural language
- Generating appropriate prompts
"""

import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from services.onboarding.narrative_helpers import (
    acknowledge_project,
    celebrate_completion,
    get_add_more_prompt,
    get_confirmation_prompt,
    get_more_projects_prompt,
    get_need_project_message,
    handle_decline_warmly,
)
from services.onboarding.portfolio_manager import PortfolioOnboardingManager
from services.shared_types import PortfolioOnboardingState

logger = logging.getLogger(__name__)


@dataclass
class OnboardingResponse:
    """Response from the onboarding handler."""

    message: str
    state: PortfolioOnboardingState
    is_complete: bool = False
    captured_projects: Optional[list] = None
    metadata: Optional[Dict[str, Any]] = None


class PortfolioOnboardingHandler:
    """
    Issue #490: Handles portfolio onboarding conversation turns.

    Processes user messages, extracts project information, and generates
    appropriate responses based on conversation state.

    Follows StandupConversationHandler pattern from Epic #242.
    """

    # Patterns indicating user wants to decline
    DECLINE_PATTERNS = [
        r"\b(no|nope|not now|later|skip|cancel|never mind|nevermind)\b",
        r"\bno thanks\b",
        r"\bmaybe later\b",
        r"\bnot right now\b",
        r"\bi('m| am) (good|fine|ok|okay)\b",
    ]

    # Patterns indicating user is done adding projects
    DONE_PATTERNS = [
        r"\b(that'?s? (all|it)|done|finished|no more|nothing else)\b",
        r"\bjust (that one|the one|this one|those|these|those two|them)\b",
        r"\bonly (that|this|one|those|these|two)\b",
        r"\bnope,? (that'?s? it|nothing else)\b",
        r"\bfor now\b",  # "just those two for now", "that's all for now"
        r"\b(that|those) (is|are) (it|all)\b",  # "those are all", "that is it"
    ]

    # Patterns indicating user wants to confirm
    CONFIRM_PATTERNS = [
        r"\b(yes|yeah|yep|sure|correct|right|looks good|perfect|great)\b",
        r"\bsave (it|them)\b",
        r"\bthat'?s? (correct|right)\b",
    ]

    # Issue #863: Repo-linking patterns for GATHERING_REPOS state
    REPO_FORMAT_PATTERN = re.compile(r"^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$")

    SKIP_REPO_PATTERNS = [
        r"\b(skip|no repo|no repository|none|pass|next)\b",
        r"\bdon'?t have (a |one|any)?",
        r"\bno$",
    ]

    SKIP_ALL_REPOS_PATTERNS = [
        r"\bskip (all|everything|the rest|repos|repositories)\b",
        r"\bno repos?\b",
        r"\bnone of them\b",
    ]

    def __init__(self, manager: PortfolioOnboardingManager):
        """
        Initialize the handler.

        Args:
            manager: PortfolioOnboardingManager for state management
        """
        self.manager = manager

    # #1886: the OFFERED-state greeting-offer method that used to live here
    # was Rule-0 deleted (2026-10-07). Zero production callers — its only
    # caller, the ConversationHandler's greeting-time onboarding-offer
    # check, was itself Rule-0 deleted in the same pass (its call site was
    # already commented out under ADR-059). Full grep evidence: #1886
    # session log.

    def handle_offer_response(
        self, session_id: str, user_message: str
    ) -> Optional[OnboardingResponse]:
        """
        Handle the user's response to the onboarding offer.

        Issue #888: Called when we detect a user has an OFFERED session and
        sends a new message. Checks for acceptance or decline.

        Args:
            session_id: The onboarding session ID (in OFFERED state)
            user_message: User's response to the offer

        Returns:
            OnboardingResponse if accepted/declined, None if message
            doesn't clearly indicate either (treat as decline-by-ignoring).
        """
        session = self.manager.get_session(session_id)
        if not session or session.state != PortfolioOnboardingState.OFFERED:
            return None

        message_lower = user_message.lower()

        # Check for acceptance
        if self._matches_patterns(message_lower, self.ACCEPTANCE_PATTERNS):
            # Transition OFFERED → INITIATED → GATHERING_PROJECTS
            self.manager.transition_state(session.id, PortfolioOnboardingState.INITIATED)
            self.manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)

            response_message = (
                "Great! Let's get you set up. Tell me about the projects you're "
                "working on. You can mention one at a time — project name and a "
                "quick description of what it is."
            )
            self.manager.add_turn(session.id, user_message, response_message)

            return OnboardingResponse(
                message=response_message,
                state=session.state,
                is_complete=False,
                metadata={"onboarding_id": session.id},
            )

        # Check for explicit decline
        if self._matches_patterns(message_lower, self.DECLINE_PATTERNS):
            self.manager.transition_state(session.id, PortfolioOnboardingState.DECLINED)
            response_message = (
                "No problem! Whenever you're ready to tell me about your projects, "
                "just say 'set up my projects' and we can do this then. "
                "What can I help you with today?"
            )
            self.manager.add_turn(session.id, user_message, response_message)

            return OnboardingResponse(
                message=response_message,
                state=session.state,
                is_complete=False,
                metadata={"onboarding_id": session.id},
            )

        # Neither clear accept nor decline — treat as implicit decline
        # (user is just diving in, per PPM direction: "accept 'no' gracefully")
        self.manager.transition_state(session.id, PortfolioOnboardingState.DECLINED)
        # Return None so the message gets handled by normal classification
        return None

    # #1886: the legacy direct-start method ("retained for backward
    # compatibility") that used to live here was Rule-0 deleted (2026-10-07).
    # Confirmed ZERO callers anywhere in services/ or web/ (grep, not just
    # "commented out"). Fully orphaned. Full grep evidence: #1886 session
    # log.

    def handle_turn(
        self,
        onboarding_id: str,
        user_message: str,
    ) -> OnboardingResponse:
        """
        Process a user message and return appropriate response.

        Args:
            onboarding_id: Onboarding session ID
            user_message: User's input

        Returns:
            OnboardingResponse with next prompt or completion
        """
        session = self.manager.get_session(onboarding_id)
        if not session:
            logger.error(f"Onboarding session not found: {onboarding_id}")
            return OnboardingResponse(
                message="I'm sorry, I lost track of our conversation. Would you like to start over?",
                state=PortfolioOnboardingState.INITIATED,
                is_complete=False,
            )

        # Route based on current state
        if session.state == PortfolioOnboardingState.INITIATED:
            return self._handle_initiated(session, user_message)
        elif session.state == PortfolioOnboardingState.GATHERING_PROJECTS:
            return self._handle_gathering(session, user_message)
        elif session.state == PortfolioOnboardingState.CONFIRMING:
            return self._handle_confirming(session, user_message)
        elif session.state == PortfolioOnboardingState.GATHERING_REPOS:
            return self._handle_gathering_repos(session, user_message)
        else:
            # Terminal state - shouldn't receive turns
            return OnboardingResponse(
                message="This onboarding session has already ended.",
                state=session.state,
                is_complete=True,
            )

    def _handle_initiated(
        self,
        session,
        user_message: str,
    ) -> OnboardingResponse:
        """Handle response to initial onboarding offer."""
        message_lower = user_message.lower()

        # Check if user declined
        if self._matches_patterns(message_lower, self.DECLINE_PATTERNS):
            self.manager.transition_state(session.id, PortfolioOnboardingState.DECLINED)
            response_message = (
                "No problem! Whenever you're ready to tell me about your projects, "
                "just say 'set up my projects' and we can do this then. "
                "What can I help you with today?"
            )
            self.manager.add_turn(session.id, user_message, response_message)
            return OnboardingResponse(
                message=response_message,
                state=PortfolioOnboardingState.DECLINED,
                is_complete=True,
            )

        # User accepted - transition to gathering
        self.manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)
        response_message = "Great! What are you working on right now?"
        self.manager.add_turn(session.id, user_message, response_message)

        return OnboardingResponse(
            message=response_message,
            state=PortfolioOnboardingState.GATHERING_PROJECTS,
            is_complete=False,
        )

    def _handle_gathering(
        self,
        session,
        user_message: str,
    ) -> OnboardingResponse:
        """Handle project info gathering."""
        message_lower = user_message.lower()

        # Check if user is done adding projects
        if self._matches_patterns(message_lower, self.DONE_PATTERNS):
            if not session.captured_projects:
                # No projects captured yet - prompt for at least one
                response_message = get_need_project_message()
                self.manager.add_turn(session.id, user_message, response_message)
                return OnboardingResponse(
                    message=response_message,
                    state=PortfolioOnboardingState.GATHERING_PROJECTS,
                    is_complete=False,
                )
            else:
                # Transition to confirming
                return self._transition_to_confirming(session, user_message)

        # Check for decline
        if self._matches_patterns(message_lower, self.DECLINE_PATTERNS):
            if session.captured_projects:
                # Have some projects - ask to confirm what we have
                return self._transition_to_confirming(session, user_message)
            else:
                # No projects - decline
                self.manager.transition_state(session.id, PortfolioOnboardingState.DECLINED)
                response_message = handle_decline_warmly(had_projects=False)
                self.manager.add_turn(session.id, user_message, response_message)
                return OnboardingResponse(
                    message=response_message,
                    state=PortfolioOnboardingState.DECLINED,
                    is_complete=True,
                )

        # Check if user is affirming they want to add more projects
        # (e.g., "Yes, I have another project to tell you about")
        # Issue #841: Also attempt extraction — user may embed project name
        # in confirmation (e.g., "Yes, I have another one called Dynamic Atlas")
        if self._matches_patterns(message_lower, self.CONFIRM_PATTERNS):
            # Try extraction — confirmation may contain a project name
            project_info = self._extract_project_info(user_message)
            # Only treat as submission if extraction found a named pattern match
            # (not the fallback which just uses the raw message text)
            if project_info.get("source") == "pattern":
                project_name = project_info.get("name", "your project")
                self.manager.add_project(session.id, project_info)
                is_first = len(session.captured_projects) <= 1
                ack = acknowledge_project(project_name, is_first_project=is_first)
                more_prompt = get_more_projects_prompt()
                response_message = f"{ack} {more_prompt}"
                self.manager.add_turn(session.id, user_message, response_message)
                return OnboardingResponse(
                    message=response_message,
                    state=PortfolioOnboardingState.GATHERING_PROJECTS,
                    is_complete=False,
                )
            # Bare confirmation — just prompt for more
            response_message = get_add_more_prompt()
            self.manager.add_turn(session.id, user_message, response_message)
            return OnboardingResponse(
                message=response_message,
                state=PortfolioOnboardingState.GATHERING_PROJECTS,
                is_complete=False,
            )

        # Extract project info from message
        project_info = self._extract_project_info(user_message)
        self.manager.add_project(session.id, project_info)

        # Acknowledge project with context-aware response (first vs. additional)
        project_name = project_info.get("name", "your project")
        is_first = len(session.captured_projects) <= 1
        ack = acknowledge_project(project_name, is_first_project=is_first)
        more_prompt = get_more_projects_prompt()
        response_message = f"{ack} {more_prompt}"
        self.manager.add_turn(session.id, user_message, response_message)

        return OnboardingResponse(
            message=response_message,
            state=PortfolioOnboardingState.GATHERING_PROJECTS,
            is_complete=False,
        )

    def _handle_confirming(
        self,
        session,
        user_message: str,
    ) -> OnboardingResponse:
        """Handle confirmation of captured projects and main-project designation."""
        message_lower = user_message.lower()
        project_names = self._get_project_names(session)

        # Check if user is designating a main project (response to "which is your main focus?")
        # Only relevant when we asked about main project (multiple projects captured)
        if len(session.captured_projects) > 1:
            designated = self._try_designate_main_project(message_lower, session)
            if designated is not None:
                # User named a project or declined — proceed to repo linking
                return self._transition_to_repo_gathering(session, user_message)

        # Check for confirmation (save portfolio)
        if self._matches_patterns(message_lower, self.CONFIRM_PATTERNS):
            return self._transition_to_repo_gathering(session, user_message)

        # User wants to add more
        if "more" in message_lower or "another" in message_lower or "add" in message_lower:
            self.manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)
            response_message = get_add_more_prompt()
            self.manager.add_turn(session.id, user_message, response_message)

            return OnboardingResponse(
                message=response_message,
                state=PortfolioOnboardingState.GATHERING_PROJECTS,
                is_complete=False,
            )

        # Check for decline/cancel
        if self._matches_patterns(message_lower, self.DECLINE_PATTERNS):
            self.manager.transition_state(session.id, PortfolioOnboardingState.DECLINED)
            response_message = handle_decline_warmly(had_projects=bool(session.captured_projects))
            self.manager.add_turn(session.id, user_message, response_message)

            return OnboardingResponse(
                message=response_message,
                state=PortfolioOnboardingState.DECLINED,
                is_complete=True,
            )

        # Unclear response — for multi-project, the user might be naming their main project
        # For single project, re-prompt for confirmation
        if len(session.captured_projects) > 1:
            # Treat unclear response as possible project designation attempt
            designated = self._try_designate_main_project(message_lower, session, fuzzy=True)
            if designated is not None:
                return self._transition_to_repo_gathering(session, user_message)

        # Re-prompt
        response_message = get_confirmation_prompt(project_names)
        self.manager.add_turn(session.id, user_message, response_message)

        return OnboardingResponse(
            message=response_message,
            state=PortfolioOnboardingState.CONFIRMING,
            is_complete=False,
        )

    def _transition_to_confirming(self, session, user_message: str) -> OnboardingResponse:
        """Transition to confirming state and generate confirmation prompt.

        For single project: asks to confirm saving.
        For multiple projects: asks which is their main focus (with opt-out),
        which also serves as the confirmation step.
        """
        self.manager.transition_state(session.id, PortfolioOnboardingState.CONFIRMING)

        project_names = self._get_project_names(session)

        if len(project_names) == 1:
            # Single project — just confirm (will auto-set as default)
            response_message = get_confirmation_prompt(project_names)
        else:
            # Multiple projects — ask which is main focus (once, here)
            project_summary = self._format_project_list(project_names)
            response_message = (
                f"I have {project_summary}. "
                f"Which would you call your main focus right now? "
                f"(Or just say 'save' to add them all without a primary.)"
            )

        self.manager.add_turn(session.id, user_message, response_message)

        return OnboardingResponse(
            message=response_message,
            state=PortfolioOnboardingState.CONFIRMING,
            is_complete=False,
        )

    def _complete_onboarding(self, session, user_message: str) -> OnboardingResponse:
        """Complete the onboarding, marking the single project as default if applicable."""
        self.manager.transition_state(session.id, PortfolioOnboardingState.COMPLETE)

        # Auto-set single project as default
        if len(session.captured_projects) == 1:
            session.captured_projects[0]["is_default"] = True

        project_names = self._get_project_names(session)
        response_message = celebrate_completion(project_names)

        # Append primary designation info if one was set
        default_project = next(
            (p.get("name") for p in session.captured_projects if p.get("is_default")),
            None,
        )
        if default_project and len(session.captured_projects) > 1:
            response_message += f" {default_project} is set as your primary."

        self.manager.add_turn(session.id, user_message, response_message)

        return OnboardingResponse(
            message=response_message,
            state=PortfolioOnboardingState.COMPLETE,
            is_complete=True,
            captured_projects=session.captured_projects,
        )

    def _try_designate_main_project(
        self, message_lower: str, session, fuzzy: bool = False
    ) -> Optional[str]:
        """Try to match user's message to a captured project name for default designation.

        Args:
            message_lower: Lowercase user message
            session: Onboarding session
            fuzzy: If True, try substring matching against project names

        Returns:
            Project name if designated, empty string if user declined, None if no match.
        """
        # Check if user is declining to designate a primary
        no_primary_patterns = [
            r"\b(save|just save|save them|no primary|no preference|none|all equal)\b",
            r"\bdon'?t (need|want) a (primary|main|default)\b",
        ]
        for pattern in no_primary_patterns:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return ""  # Empty string = declined designation, but still proceed

        # Try to match a project name
        for project in session.captured_projects:
            name = project.get("name", "").lower()
            if not name:
                continue
            # Exact name mention
            if name in message_lower:
                project["is_default"] = True
                return project.get("name", "")
            # Fuzzy: check if any word in the project name appears
            if fuzzy:
                words = name.split()
                if any(w in message_lower for w in words if len(w) > 2):
                    project["is_default"] = True
                    return project.get("name", "")

        return None  # No match found

    def _get_project_names(self, session) -> List[str]:
        """Get list of project names from session."""
        return [p.get("name", "unnamed") for p in session.captured_projects]

    @staticmethod
    def _format_project_list(names: List[str]) -> str:
        """Format project names as natural language list."""
        if not names:
            return ""
        if len(names) == 1:
            return names[0]
        if len(names) == 2:
            return f"{names[0]} and {names[1]}"
        return ", ".join(names[:-1]) + f", and {names[-1]}"

    def _extract_project_info(self, message: str) -> Dict[str, Any]:
        """
        Extract project name and description from user message.

        Simple extraction for MVP - looks for patterns like:
        - "called X" / "named X"
        - "project is X" / "main project is X"
        - "Another project is X"
        - "working on X" / "work on X"
        - "X project" (fallback pattern)
        - Just uses the whole message as name if no pattern found

        Args:
            message: User's message describing their project

        Returns:
            Dict with 'name', optionally 'description', and 'source' indicating
            extraction method ('pattern' for named patterns, 'fallback' otherwise)
        """
        message = message.strip()

        # Try to extract name with "called" or "named"
        called_match = re.search(
            r"(?:called|named)\s+['\"']?([^'\",.]+)['\"']?", message, re.IGNORECASE
        )
        if called_match:
            name = called_match.group(1).strip()
            description = message
            return {"name": name, "description": description, "source": "pattern"}

        # Try to extract "[main/my/the] project is X" pattern - check this BEFORE "X project"
        project_is_match = re.search(
            r"(?:my|the|main|a)\s+(?:project|app|application)\s+is\s+([^,.\n]+?)(?:\.|,|$)",
            message,
            re.IGNORECASE,
        )
        if project_is_match:
            name = project_is_match.group(1).strip()
            description = message
            return {"name": name, "description": description, "source": "pattern"}

        # Try to extract "another project is X" or "one project is X" pattern
        another_match = re.search(
            r"(?:another|one)\s+(?:project|app|application)\s+(?:is|called|named)\s+([^,.\n]+?)(?:\.|,|$)",
            message,
            re.IGNORECASE,
        )
        if another_match:
            name = another_match.group(1).strip()
            description = message
            return {"name": name, "description": description, "source": "pattern"}

        # Try to extract from "I'm building/working on X" or "I work on X" or "I also work on X"
        # Note: handles both "working on" and "work on"
        building_match = re.search(
            r"(?:building|work(?:ing)?\s+on|developing|creating)\s+(?:a|an|the)?\s*([^,.\n]+?)(?:\.|,|$)",
            message,
            re.IGNORECASE,
        )
        if building_match:
            name = building_match.group(1).strip()
            # Clean up trailing words
            name = re.sub(
                r"\s+(?:right now|currently|at the moment|too|as well|also)$",
                "",
                name,
                flags=re.IGNORECASE,
            )
            description = message
            return {"name": name, "description": description, "source": "pattern"}

        # Try to extract "X project" pattern (e.g., "a task management project")
        # This is a fallback pattern since it's less specific
        project_match = re.search(
            r"(?:a|an|my|the)\s+([^,.\n]+?)\s+(?:project|app|application|system|platform)",
            message,
            re.IGNORECASE,
        )
        if project_match:
            name = project_match.group(1).strip()
            description = message
            return {"name": name, "description": description, "source": "pattern"}

        # Fallback - use first sentence or whole message as name
        first_sentence = message.split(".")[0].strip()
        if len(first_sentence) > 50:
            # Too long - just use first few words
            words = first_sentence.split()[:5]
            name = " ".join(words)
        else:
            name = first_sentence

        return {"name": name, "description": message, "source": "fallback"}

    def _matches_patterns(self, text: str, patterns: list) -> bool:
        """Check if text matches any of the given regex patterns."""
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    # -----------------------------------------------------------------
    # Issue #863: Repo-gathering methods
    # -----------------------------------------------------------------

    def _transition_to_repo_gathering(self, session, user_message: str) -> OnboardingResponse:
        """Transition from confirming to repo gathering: ask about first project's repo."""
        # Auto-set single project as default
        if len(session.captured_projects) == 1:
            session.captured_projects[0]["is_default"] = True

        self.manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_REPOS)
        session.repo_project_index = 0

        project_name = session.captured_projects[0].get("name", "your project")
        response_message = self._get_repo_prompt(project_name, is_first=True)
        self.manager.add_turn(session.id, user_message, response_message)

        return OnboardingResponse(
            message=response_message,
            state=PortfolioOnboardingState.GATHERING_REPOS,
            is_complete=False,
        )

    def _handle_gathering_repos(self, session, user_message: str) -> OnboardingResponse:
        """Handle repo linking for each project during onboarding."""
        message_lower = user_message.lower().strip()
        current_index = session.repo_project_index
        current_project = session.captured_projects[current_index]

        # Check for "skip all" — skip remaining projects and complete
        if self._matches_patterns(message_lower, self.SKIP_ALL_REPOS_PATTERNS):
            return self._complete_onboarding(session, user_message)

        # Check for "skip" (this project only)
        if self._matches_patterns(message_lower, self.SKIP_REPO_PATTERNS):
            return self._advance_repo_gathering(session, user_message)

        # Try to extract repo from message
        repo_input = user_message.strip()
        if self.REPO_FORMAT_PATTERN.match(repo_input):
            # Valid format — store it
            current_project["repo"] = repo_input
            return self._advance_repo_gathering(session, user_message)

        # Invalid format — re-prompt with hint
        project_name = current_project.get("name", "your project")
        response_message = (
            f"That doesn't look like a repo format. "
            f"Please enter it as owner/repo-name "
            f"(e.g., mediajunkie/healthtrack), or say 'skip' to move on."
        )
        self.manager.add_turn(session.id, user_message, response_message)

        return OnboardingResponse(
            message=response_message,
            state=PortfolioOnboardingState.GATHERING_REPOS,
            is_complete=False,
        )

    def _advance_repo_gathering(self, session, user_message: str) -> OnboardingResponse:
        """Move to the next project's repo prompt, or complete if all done."""
        next_index = session.repo_project_index + 1

        if next_index >= len(session.captured_projects):
            # All projects asked about — complete
            return self._complete_onboarding(session, user_message)

        # Move to next project
        session.repo_project_index = next_index
        next_project = session.captured_projects[next_index]
        project_name = next_project.get("name", "your project")

        response_message = self._get_repo_prompt(project_name, is_first=False)
        self.manager.add_turn(session.id, user_message, response_message)

        return OnboardingResponse(
            message=response_message,
            state=PortfolioOnboardingState.GATHERING_REPOS,
            is_complete=False,
        )

    def _get_repo_prompt(self, project_name: str, is_first: bool) -> str:
        """Generate the prompt asking about a project's repo."""
        if is_first:
            return (
                f"Great! One more optional step — would you like to link a GitHub "
                f"repository to **{project_name}**? Enter it as owner/repo-name "
                f"(e.g., mediajunkie/healthtrack), or say 'skip'."
            )
        return (
            f"How about **{project_name}** — any GitHub repo to link? "
            f"(owner/repo-name, or 'skip')"
        )
