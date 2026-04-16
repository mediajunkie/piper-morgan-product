"""
PM-012: Real GitHub API Integration Tests
Tests that run against actual GitHub API when tokens are available
"""

import asyncio
import os
from typing import Any, Dict
from unittest.mock import Mock

import pytest

from services.domain.models import WorkItem
from tests.integration.test_pm012_github_real_api_config import (
    GitHubTestConfig,
    cleanup_test_issues,
    create_real_github_agent,
    generate_test_work_item,
    skip_if_no_real_api,
)


class TestPM012RealGitHubAPI:
    """Real GitHub API integration tests"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown for real API tests"""
        # Setup
        self.agent = create_real_github_agent()
        self.repository = GitHubTestConfig.get_test_repository()

        if self.agent is None:
            pytest.skip("Real GitHub API not available")

        yield

        # Teardown - cleanup any test issues created
        if hasattr(self, "created_issues"):
            for issue_data in self.created_issues:
                try:
                    # Note: GitHub API doesn't allow issue deletion, so we just log
                    print(f"Test issue created: {issue_data.get('url', 'Unknown')}")
                except Exception as e:
                    print(f"Cleanup warning: {e}")

    @pytest.mark.real_api
    @pytest.mark.asyncio
    async def test_real_github_connection(self):
        """Test real GitHub API connection"""
        result = self.agent.test_connection()

        assert result["success"] is True
        assert "user" in result
        assert "name" in result
        assert "repos_count" in result

        print(f"Connected to GitHub as: {result['user']} ({result['name']})")

    @pytest.mark.real_api
    @pytest.mark.asyncio
    async def test_real_repository_access(self):
        """Test access to test repository"""
        try:
            # Try to access the repository
            repo = self.agent.client.get_repo(self.repository)

            assert repo.name in self.repository
            assert repo.full_name == self.repository

            print(f"Successfully accessed repository: {repo.full_name}")
            print(f"Repository is private: {repo.private}")

        except Exception as e:
            pytest.fail(f"Cannot access repository {self.repository}: {e}")

    @pytest.mark.real_api
    @pytest.mark.asyncio
    async def test_real_issue_creation(self):
        """Test creating a real GitHub issue"""
        # Generate test work item
        work_item_data = generate_test_work_item(title="Real API Test Issue", issue_type="task")

        # Create work item object
        work_item = WorkItem(**work_item_data)

        # Create issue via GitHub API
        issue_data = await self.agent.create_issue_from_work_item(
            repo_name=self.repository, work_item=work_item.to_dict()
        )

        # Verify issue was created
        assert "id" in issue_data
        assert "number" in issue_data
        assert "title" in issue_data
        assert "url" in issue_data
        assert "state" in issue_data

        assert issue_data["title"] == work_item.title
        assert issue_data["state"] == "open"
        assert "github.com" in issue_data["url"]
        assert self.repository in issue_data["url"]

        print(f"Created issue #{issue_data['number']}: {issue_data['url']}")

        # Store for cleanup
        if not hasattr(self, "created_issues"):
            self.created_issues = []
        self.created_issues.append(issue_data)

    @pytest.mark.real_api
    @pytest.mark.asyncio
    async def test_real_issue_creation_with_labels(self):
        """Test creating a real GitHub issue with custom labels"""
        # Generate test work item with specific labels
        work_item_data = generate_test_work_item(
            title="Real API Test Issue with Labels", issue_type="bug"
        )
        work_item_data["labels"] = ["bug", "test", "piper-morgan", "integration"]

        # Create work item object
        work_item = WorkItem(**work_item_data)

        # Create issue via GitHub API
        issue_data = await self.agent.create_issue_from_work_item(
            repo_name=self.repository, work_item=work_item.to_dict()
        )

        # Verify issue was created with labels
        assert "labels" in issue_data
        assert len(issue_data["labels"]) >= 3  # Should have our custom labels

        # Check for specific labels
        label_names = [label for label in issue_data["labels"]]
        assert "bug" in label_names
        assert "test" in label_names
        assert "piper-morgan" in label_names

        print(f"Created issue #{issue_data['number']} with labels: {label_names}")

        # Store for cleanup
        if not hasattr(self, "created_issues"):
            self.created_issues = []
        self.created_issues.append(issue_data)

    @pytest.mark.real_api
    @pytest.mark.asyncio
    async def test_real_issue_content_validation(self):
        """Test that real issue content is properly formatted"""
        # Generate test work item with rich content
        work_item_data = generate_test_work_item(
            title="Real API Test Issue with Rich Content", issue_type="feature"
        )
        work_item_data["description"] = """## Description

This is a test feature request created by Piper Morgan for real API integration testing.

## Requirements

- Feature A: Implement new functionality
- Feature B: Add configuration options
- Feature C: Update documentation

## Acceptance Criteria

- [ ] Feature A works correctly
- [ ] Feature B is configurable
- [ ] Feature C is documented
- [ ] All tests pass

## Additional Context

This is part of the PM-012 GitHub integration testing suite.
"""

        # Create work item object
        work_item = WorkItem(**work_item_data)

        # Create issue via GitHub API
        issue_data = await self.agent.create_issue_from_work_item(
            repo_name=self.repository, work_item=work_item.to_dict()
        )

        # Verify issue content
        assert issue_data["title"] == work_item.title

        # Fetch the actual issue to verify content
        repo = self.agent.client.get_repo(self.repository)
        issue = repo.get_issue(issue_data["number"])

        # Verify markdown content is preserved
        assert "## Description" in issue.body
        assert "## Requirements" in issue.body
        assert "## Acceptance Criteria" in issue.body
        assert "Feature A: Implement new functionality" in issue.body
        assert "- [ ] Feature A works correctly" in issue.body

        print(f"Verified issue #{issue_data['number']} content formatting")

        # Store for cleanup
        if not hasattr(self, "created_issues"):
            self.created_issues = []
        self.created_issues.append(issue_data)

    @pytest.mark.real_api
    @pytest.mark.asyncio
    async def test_real_issue_fetching(self):
        """Test fetching a real GitHub issue"""
        # First create an issue
        work_item_data = generate_test_work_item(
            title="Real API Test Issue for Fetching", issue_type="task"
        )

        work_item = WorkItem(**work_item_data)

        # Create issue
        created_issue = await self.agent.create_issue_from_work_item(
            repo_name=self.repository, work_item=work_item.to_dict()
        )

        # Store for cleanup
        if not hasattr(self, "created_issues"):
            self.created_issues = []
        self.created_issues.append(created_issue)

        # Now fetch the issue
        fetched_issue = await self.agent.get_issue(
            repo_name=self.repository, issue_number=created_issue["number"]
        )

        # Verify fetched issue matches created issue
        assert fetched_issue["id"] == created_issue["id"]
        assert fetched_issue["number"] == created_issue["number"]
        assert fetched_issue["title"] == created_issue["title"]
        assert fetched_issue["url"] == created_issue["url"]
        assert fetched_issue["state"] == created_issue["state"]

        print(f"Successfully fetched issue #{fetched_issue['number']}")

    @pytest.mark.real_api
    @pytest.mark.asyncio
    async def test_real_issue_url_parsing(self):
        """Test parsing GitHub issue URLs"""
        # Create an issue first
        work_item_data = generate_test_work_item(
            title="Real API Test Issue for URL Parsing", issue_type="bug"
        )

        work_item = WorkItem(**work_item_data)

        # Create issue
        created_issue = await self.agent.create_issue_from_work_item(
            repo_name=self.repository, work_item=work_item.to_dict()
        )

        # Store for cleanup
        if not hasattr(self, "created_issues"):
            self.created_issues = []
        self.created_issues.append(created_issue)

        # Test URL parsing
        issue_url = created_issue["url"]
        parsed = self.agent.parse_github_url(issue_url)

        assert parsed is not None
        owner, repo, issue_number = parsed

        assert f"{owner}/{repo}" == self.repository
        assert issue_number == created_issue["number"]

        # Test fetching via URL
        fetched_via_url = await self.agent.get_issue_by_url(issue_url)

        assert fetched_via_url["id"] == created_issue["id"]
        assert fetched_via_url["number"] == created_issue["number"]
        assert fetched_via_url["title"] == created_issue["title"]

        print(f"Successfully parsed and fetched issue via URL: {issue_url}")

    @pytest.mark.real_api
    @pytest.mark.asyncio
    async def test_real_repository_listing(self):
        """Test listing accessible repositories"""
        repos = self.agent.list_repositories()

        assert isinstance(repos, list)
        assert len(repos) > 0

        # Verify repository structure
        for repo in repos:
            assert "name" in repo
            assert "full_name" in repo
            assert "private" in repo
            assert "url" in repo

        # Check if our test repository is accessible
        repo_names = [repo["full_name"] for repo in repos]
        if self.repository in repo_names:
            print(f"Test repository {self.repository} is accessible")
        else:
            print(f"Warning: Test repository {self.repository} not found in accessible repos")
            print(f"Available repos: {repo_names[:5]}...")  # Show first 5

    @pytest.mark.real_api
    @pytest.mark.asyncio
    async def test_real_error_handling(self):
        """Test real error handling scenarios"""
        # Test with non-existent repository
        with pytest.raises(ValueError, match="GitHub resource not found"):
            await self.agent.get_issue("non-existent/not-a-repo", 999)

        # Test with non-existent issue number
        with pytest.raises(ValueError, match="GitHub resource not found"):
            await self.agent.get_issue(self.repository, 999999)

        # Test with invalid URL
        with pytest.raises(ValueError, match="Invalid GitHub URL format"):
            await self.agent.get_issue_by_url("https://invalid-url.com")

        print("Successfully tested error handling scenarios")


class TestPM012RealAPIEndToEnd:
    """End-to-end tests with real GitHub API"""

    @pytest.mark.real_api
    @pytest.mark.asyncio
    async def test_real_end_to_end_workflow(self):
        """Test complete end-to-end workflow with real API"""
        from services.domain.models import Intent
        from services.orchestration.engine import OrchestrationEngine
        from services.orchestration.workflow_factory import WorkflowFactory
        from services.shared_types import IntentCategory, WorkflowType

        # Create real GitHub agent
        agent = create_real_github_agent()
        if agent is None:
            pytest.skip("Real GitHub API not available")

        # Create intent
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={
                "original_message": "Create a test issue for real API integration testing",
                "repository": GitHubTestConfig.get_test_repository(),
            },
        )

        # Create workflow
        factory = WorkflowFactory()
        workflow = await factory.create_from_intent(intent)

        assert workflow is not None
        assert workflow.type == WorkflowType.CREATE_TICKET

        # Create engine with real GitHub agent
        engine = OrchestrationEngine()
        engine.github_agent = agent

        # Execute workflow
        result = await engine.execute_workflow(workflow.id)

        # Verify success
        assert result["success"] is True
        assert "issue_number" in result["data"]
        assert "issue_url" in result["data"]

        print(f"End-to-end workflow created issue #{result['data']['issue_number']}")
        print(f"Issue URL: {result['data']['issue_url']}")


# Utility functions for test data
def create_test_project_with_github():
    """Create a test project with GitHub integration"""
    from services.domain.models import Project, ProjectIntegration
    from services.shared_types import IntegrationType

    github_integration = ProjectIntegration(
        type=IntegrationType.GITHUB,
        name="Test Repository",
        config={"repository": GitHubTestConfig.get_test_repository()},
    )

    return Project(
        id="test-project-real-api",
        name="Real API Test Project",
        description="Test project for real GitHub API integration",
        integrations=[github_integration],
        is_default=False,
    )


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-m", "real_api"])
