"""
GitHub Configuration Management for PM-123 Multi-User Support

Provides type-safe configuration for GitHub integration with user-specific
repository settings and PM number formatting.
"""

import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class GitHubConfiguration:
    """Type-safe GitHub configuration for multi-user PM-123 support"""

    default_repository: str
    owner: str
    pm_prefix: str = "PM-"
    pm_start: int = 1
    pm_padding: int = 3
    api_base: str = "https://api.github.com"
    default_labels: Optional[List[str]] = None

    def __post_init__(self):
        """Initialize default values and validate configuration"""
        if self.default_labels is None:
            self.default_labels = []

        # Validate repository format. #1212: an EMPTY default_repository means
        # "no default configured" — a valid, common state (e.g. a user who hasn't
        # set one) — NOT a malformed value. Raising on empty was the root of Q16:
        # create_issue constructs this config internally, the empty default threw
        # here, and it surfaced as the generic "Something unexpected happened."
        # Only a NON-empty value that isn't "owner/repo" is actually malformed.
        if self.default_repository and "/" not in self.default_repository:
            raise ValueError(
                f"Repository must be in 'owner/repo' format, got: {self.default_repository}"
            )

        # Validate PM prefix format
        if not self.pm_prefix:
            raise ValueError("PM prefix cannot be empty")

    def format_pm_number(self, number: int) -> str:
        """Format PM number according to user configuration

        Args:
            number: PM number to format (e.g., 140)

        Returns:
            Formatted PM number (e.g., "PM-140")
        """
        return f"{self.pm_prefix}{number:0{self.pm_padding}d}"

    def get_repository_parts(self) -> tuple[str, str]:
        """Get repository owner and name as separate values

        Returns:
            Tuple of (owner, repository_name)
        """
        if "/" in self.default_repository:
            return tuple(self.default_repository.split("/", 1))
        return self.owner, self.default_repository

    def validate_environment(self) -> bool:
        """Validate GitHub environment configuration

        Returns:
            True if environment is properly configured
        """
        # Check for GitHub token
        token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
        if not token:
            return False

        return True

    @classmethod
    def create_default(cls) -> "GitHubConfiguration":
        """Create default configuration with empty repo identifiers.

        Issue #1042: removed legacy hardcoded "mediajunkie/piper-morgan-product"
        / "mediajunkie" defaults (PM directive: "my github username does not
        belong in the core product"). Per-call resolution via
        ``repo_resolver`` fills in the values that used to be defaulted.

        Returns:
            Default GitHub configuration with empty repo + owner; downstream
            consumers must resolve via ``repo_resolver``.
        """
        return cls(
            default_repository="",
            owner="",
            pm_prefix="PM-",
            pm_start=1,
            pm_padding=3,
            default_labels=["enhancement"],
        )
