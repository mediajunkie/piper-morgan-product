"""Local-git inspection (#1044).

Provides a thin wrapper over GitPython for read-only queries about the
server's working-tree state — current branch, dirty/clean status,
ahead/behind from upstream. Distinct from the GitHub integration which
queries remote state via REST API.

Deployment-context caveat: scoped to the server's working directory
(`os.getcwd()` by default). In local-Piper deployments (alpha, dev), this
is the user's git repo. In SaaS deployments, this would need to be
re-scoped to user-uploaded repos / configured paths — out of scope today.
"""

from services.integrations.local_git.inspector import (
    LocalGitInspector,
    LocalGitStatus,
)

__all__ = ["LocalGitInspector", "LocalGitStatus"]
