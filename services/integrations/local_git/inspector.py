"""Local-git inspector (#1044).

Read-only queries against the server's working-tree git state.

Per Pattern-073 discipline: returns bounded observations, not categorical
claims. Errors (not a git repo / GitPython unavailable) surface as
structured states, not exceptions to the user-facing layer.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LocalGitStatus:
    """Read-only snapshot of working-tree git state.

    All fields are best-effort observations. `error` is set when the
    inspector couldn't gather state (e.g., not a git repo, GitPython
    unavailable). When `error` is set, other fields are None.
    """

    current_branch: Optional[str] = None
    is_clean: Optional[bool] = None
    uncommitted_files_count: Optional[int] = None
    untracked_files_count: Optional[int] = None
    commits_ahead: Optional[int] = None
    commits_behind: Optional[int] = None
    upstream: Optional[str] = None
    error: Optional[str] = None


class LocalGitInspector:
    """Inspect a local git working tree.

    Defaults to the server's current working directory. Callers may pass
    an explicit path (for testing or for SaaS-deployment future where the
    path is user-uploaded).
    """

    def __init__(self, repo_path: Optional[str] = None) -> None:
        self.repo_path = repo_path or os.getcwd()

    def get_status(self) -> LocalGitStatus:
        """Return a snapshot of the working-tree state.

        Errors are caught and surfaced via the `error` field — never raised
        to the caller. This keeps the handler-layer code simple and lets
        the formatter render a structured error state.
        """
        try:
            import git  # GitPython
        except ImportError:
            return LocalGitStatus(error="GitPython not available in this environment")

        try:
            repo = git.Repo(self.repo_path, search_parent_directories=True)
        except (git.InvalidGitRepositoryError, git.NoSuchPathError):
            return LocalGitStatus(error=f"No git repository found at {self.repo_path}")
        except Exception as e:
            return LocalGitStatus(error=f"Unable to open git repo: {e}")

        # Current branch — detached-HEAD case returns the commit hash short form
        try:
            if repo.head.is_detached:
                current_branch = f"(detached at {repo.head.commit.hexsha[:8]})"
            else:
                current_branch = repo.active_branch.name
        except Exception as e:
            current_branch = f"(unknown — {e})"

        # Dirty / clean state
        try:
            is_dirty = repo.is_dirty(untracked_files=False)
            uncommitted = len(repo.index.diff(None)) + len(repo.index.diff("HEAD"))
            untracked = len(repo.untracked_files)
        except Exception:
            is_dirty = None
            uncommitted = None
            untracked = None

        # Upstream / ahead-behind
        upstream_name: Optional[str] = None
        ahead: Optional[int] = None
        behind: Optional[int] = None
        try:
            if not repo.head.is_detached:
                tracking = repo.active_branch.tracking_branch()
                if tracking is not None:
                    upstream_name = tracking.name
                    # iter_commits returns iterators; len() not available, count via list
                    ahead = len(
                        list(repo.iter_commits(f"{tracking.name}..{repo.active_branch.name}"))
                    )
                    behind = len(
                        list(repo.iter_commits(f"{repo.active_branch.name}..{tracking.name}"))
                    )
        except Exception:
            # Leave as None — bounded observation: we couldn't determine ahead/behind
            pass

        return LocalGitStatus(
            current_branch=current_branch,
            is_clean=(not is_dirty) if is_dirty is not None else None,
            uncommitted_files_count=uncommitted,
            untracked_files_count=untracked,
            commits_ahead=ahead,
            commits_behind=behind,
            upstream=upstream_name,
        )
