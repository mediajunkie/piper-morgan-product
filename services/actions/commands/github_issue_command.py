"""Command for creating GitHub issues.

Issue #695 (WIRE-GH-ISSUE): replaced placeholder ``mock-123`` return with a
real ``GitHubDomainService.create_issue`` call. The command sits in the
action-registry execution path; the user-approval gate happens upstream
(``web/api/routes/learning.py::execute_pattern`` is triggered by an explicit
"Execute Now" click), so by the time we get here the user has consented.

Depends on the #1112 fix to ``GitHubDomainService.create_issue`` (forwarding
kwargs to the router after #1042 made owner/repo_name kw-only); both ship
together in the WIRE-* PR.
"""

from typing import Any, Dict, Optional

from services.api.errors import GitHubAuthFailedError, GitHubRateLimitError

from .base_command import BaseCommand


class GithubIssueCommand(BaseCommand):
    """Create a GitHub issue via ``GitHubDomainService``.

    Required params:
        title: Issue title (default: "Action item from standup")
        repo: ``owner/name`` slug, or bare ``name`` (router resolves owner).
            Falls back to ``context["repo"]`` if not in params.

    Optional params:
        body: Issue body (default: empty).
        labels: List of label names (default: ["standup", "action-item"]).
        assignees: List of GitHub usernames (default: empty list).

    Context (injection point for tests):
        github_service: Pre-built ``GitHubDomainService`` (else lazy-construct).
        user_id, pattern_id: Used by upstream dispatch; not consumed here.
    """

    async def execute(self) -> Dict[str, Any]:
        """Create a GitHub issue and return the action-registry result envelope."""
        try:
            # Pull params with sensible defaults
            title = self.params.get("title", "Action item from standup")
            body = self.params.get("body", "")
            labels = self.params.get("labels", ["standup", "action-item"])
            assignees = self.params.get("assignees", [])
            repo = self.params.get("repo") or self.context.get("repo")

            if not repo:
                return {
                    "status": "error",
                    "action": "create_github_issue",
                    "error": (
                        "No repo specified. Pass 'repo' in params (owner/name slug "
                        "or bare name) or include in context."
                    ),
                }

            github_service = self._get_github_service()
            issue_data = await github_service.create_issue(
                repo_name=repo,
                title=title,
                body=body,
                labels=labels,
                assignees=assignees,
            )

            # Result envelope: real issue identity replaces mock-123.
            # Router returns dicts containing `number`, `html_url` per PyGithub
            # Issue object shape; defensive-extract in case integration shape
            # differs across surfaces.
            return {
                "status": "success",
                "action": "create_github_issue",
                "issue_id": issue_data.get("number") or issue_data.get("id"),
                "issue_url": issue_data.get("html_url") or issue_data.get("url"),
                "repo": repo,
                "title": title,
                "labels": labels,
                "message": f"Created issue: {title}",
            }

        except GitHubAuthFailedError as e:
            return {
                "status": "error",
                "action": "create_github_issue",
                "error": "GitHub authentication failed",
                "detail": str(e),
            }
        except GitHubRateLimitError as e:
            return {
                "status": "error",
                "action": "create_github_issue",
                "error": "GitHub rate limit exceeded",
                "detail": str(e),
            }
        except Exception as e:
            return {
                "status": "error",
                "action": "create_github_issue",
                "error": str(e),
            }

    def _get_github_service(self):
        """Return the ``GitHubDomainService`` instance to use.

        Resolution order:
        1. ``context["github_service"]`` if present (test injection point)
        2. Lazy-constructed singleton cached on the command instance

        The lazy construction avoids importing the integration layer at module
        load (which transitively pulls in aiohttp + PyGithub even when the
        command is never executed) — matches the deferred-import pattern used
        elsewhere in services/actions.
        """
        injected = self.context.get("github_service")
        if injected is not None:
            return injected
        if getattr(self, "_github_service_cache", None) is None:
            from services.domain.github_domain_service import GitHubDomainService

            self._github_service_cache: Optional[Any] = GitHubDomainService()
        return self._github_service_cache
