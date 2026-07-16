from typing import Dict, Optional, Tuple

from services.database.repositories import ProjectRepository
from services.domain.models import Intent, Project
from services.llm.clients import LLMClient
from services.project_context.exceptions import AmbiguousProjectError, ProjectNotFoundError
from services.shared_types import IntentCategory


class ProjectContext:
    """Business logic for resolving project context from user intents"""

    def __init__(self, project_repo: ProjectRepository, llm_client: LLMClient):
        self.project_repo = project_repo  # Dependency injection
        self.llm_client = llm_client
        self._session_last_used: Dict[str, str] = {}  # session_id -> project_id

    async def resolve_project(
        self, intent: Intent, session_id: str, confirmed_this_session: bool = False
    ) -> Tuple[Project, bool]:
        """
        Resolve project following hierarchy:
        1. Explicit project_id in intent
        2. Session project and inference compared
        3. Default project
        Returns: (Project, needs_confirmation)
        """
        # 1. Explicit project_id in intent context
        project_id = intent.context.get("project_id")
        if project_id:
            project = await self.project_repo.get_by_id(project_id)
            if project:
                self._session_last_used[session_id] = project.id
                return project, False  # No confirmation needed
            else:
                raise ProjectNotFoundError(f"Project with ID '{project_id}' not found")

        # 2. Check session project and infer from message - compare if both exist
        last_project_id = self._session_last_used.get(session_id)
        session_project = None
        if last_project_id:
            session_project = await self.project_repo.get_by_id(last_project_id)

        # 3. Infer from message context using LLM
        inferred_project = None
        inferred_project_name = await self.llm_client.complete(
            f"Which project does this relate to: {intent.context.get('original_message', '')}"
        )
        if inferred_project_name == "UNCLEAR":
            projects = await self.project_repo.list_active_projects()
            project_names = [p.name for p in projects]
            raise AmbiguousProjectError(
                f"Multiple projects available but cannot determine which one to use: {project_names}"
            )
        elif inferred_project_name:
            projects = await self.project_repo.list_active_projects()
            for project in projects:
                if project.name.lower() == inferred_project_name.strip().lower():
                    inferred_project = project
                    break

        # Decision logic: inference wins if different from session
        if session_project and confirmed_this_session:
            # Session confirmed, use it
            return session_project, False
        elif inferred_project:
            # Use inferred project (needs confirmation if session exists and differs)
            self._session_last_used[session_id] = inferred_project.id
            needs_confirmation = (
                session_project is not None and session_project.id != inferred_project.id
            )
            return inferred_project, needs_confirmation
        elif session_project:
            # Fall back to session project if no inference
            return session_project, True

        # 4. Default project
        # #1421: this class has no principal in scope (and no production callers
        # today — census B item 31); pass None = fail-closed, never a global pick.
        default_project = await self.project_repo.get_default_project(None)
        if default_project:
            self._session_last_used[session_id] = default_project.id
            return default_project, False  # No confirmation needed for default fallback

        # If all else fails, raise error
        raise AmbiguousProjectError("Could not resolve project for intent.")
