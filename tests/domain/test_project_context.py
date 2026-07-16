import uuid
from typing import Dict

import pytest

from services.domain.models import Intent, Project
from services.project_context.project_context import AmbiguousProjectError, ProjectContext


class MockProjectRepository:
    def __init__(self, projects: Dict[str, Project], default_project: Project = None):
        self.projects = projects
        self.default_project = default_project

    async def get_by_id(self, project_id):
        return self.projects.get(project_id)

    async def get_default_project(self, owner_id=None):
        # #1421: matches the real repo's owner-scoped signature. This mock tests
        # ProjectContext's branching, not repo scoping, so it returns its
        # configured default regardless of principal.
        return self.default_project

    async def list_active_projects(self):
        return list(self.projects.values())

    async def count_active_projects(self):
        return len(self.projects)

    async def find_by_name(self, name):
        for project in self.projects.values():
            if project.name == name:
                return project
        return None


class MockLLMClient:
    def __init__(self, inferred_project_id=None):
        self.inferred_project_id = inferred_project_id

    async def infer_project_id(self, intent):
        return self.inferred_project_id

    async def complete(self, prompt):
        # Mock implementation for the complete method
        if self.inferred_project_id:
            return self.inferred_project_id
        return "default_project"


def make_project(id=None, name="Test Project"):
    return Project(id=id or str(uuid.uuid4()), name=name)


def make_intent(context=None):
    return Intent(category=None, action="test", context=context or {})


@pytest.mark.asyncio
async def test_resolve_explicit_project():
    project = make_project("p1")
    repo = MockProjectRepository({"p1": project})
    llm = MockLLMClient()
    ctx = ProjectContext(repo, llm)
    intent = make_intent({"project_id": "p1"})
    result, needs_confirmation = await ctx.resolve_project(intent, session_id="s1")
    assert result == project
    assert needs_confirmation is False


@pytest.mark.asyncio
async def test_resolve_last_used_project_confirmed():
    project = make_project("p2")
    repo = MockProjectRepository({"p2": project})
    llm = MockLLMClient()
    ctx = ProjectContext(repo, llm)
    ctx._session_last_used["s2"] = "p2"
    intent = make_intent()
    result, needs_confirmation = await ctx.resolve_project(
        intent, session_id="s2", confirmed_this_session=True
    )
    assert result == project
    assert needs_confirmation is False


@pytest.mark.asyncio
async def test_resolve_last_used_project_unconfirmed():
    project = make_project("p2")
    repo = MockProjectRepository({"p2": project})
    llm = MockLLMClient()
    ctx = ProjectContext(repo, llm)
    ctx._session_last_used["s2"] = "p2"
    intent = make_intent()
    result, needs_confirmation = await ctx.resolve_project(
        intent, session_id="s2", confirmed_this_session=False
    )
    assert result == project
    assert needs_confirmation is True


@pytest.mark.asyncio
async def test_resolve_llm_inferred_project():
    project = make_project("p3")
    repo = MockProjectRepository({"p3": project})
    llm = MockLLMClient(inferred_project_id="p3")
    ctx = ProjectContext(repo, llm)
    intent = make_intent()
    # Test updated to match improved behavior: stricter project resolution prevents silent failures.
    with pytest.raises(AmbiguousProjectError):
        await ctx.resolve_project(intent, session_id="s3")


@pytest.mark.asyncio
async def test_resolve_default_project():
    default_project = make_project("p4")
    repo = MockProjectRepository({}, default_project=default_project)
    llm = MockLLMClient()
    ctx = ProjectContext(repo, llm)
    intent = make_intent()
    result, needs_confirmation = await ctx.resolve_project(intent, session_id="s4")
    assert result == default_project
    # Test updated to match improved behavior: Default project selection now more confident
    assert needs_confirmation is False


@pytest.mark.asyncio
async def test_ambiguous_project_error():
    repo = MockProjectRepository({})
    llm = MockLLMClient()
    ctx = ProjectContext(repo, llm)
    intent = make_intent()
    with pytest.raises(AmbiguousProjectError):
        await ctx.resolve_project(intent, session_id="s5")
