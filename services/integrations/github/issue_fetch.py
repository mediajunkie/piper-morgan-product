"""Direct GitHub REST fetch of an issue + its comments (#1187 Option C).

The summarize-fetch path needs the FULL issue — body + the comment thread — so
the conversational floor can produce a faithful summary. The GitHub MCP adapter
returns a lossy transformed dict (``description`` not ``body``, ``uri`` not
``html_url``, and NO comments — only an ``add_comment`` write exists), which is
fine for the router's other uses but too thin for a summary.

So for summarize we fetch the raw issue + comments directly via the REST API
(reusing the resolved repo + the user's token — keychain-first per #1192). The
returned dict is the raw GitHub shape with a ``comments`` list embedded, which is
exactly what ``IntentService._fetch_issue_content``'s formatter expects.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

_API = "https://api.github.com"


async def fetch_issue_with_comments(
    owner: str,
    repo: str,
    issue_number: int,
    token: str,
    *,
    max_comments: int = 10,
    timeout: float = 15.0,
) -> Optional[Dict[str, Any]]:
    """Fetch a GitHub issue and (up to ``max_comments``) of its comments.

    Returns the raw issue dict with a ``comments`` list embedded, or ``None`` if
    the issue can't be fetched (non-200 — not found, no access, or bad token).
    ``max_comments <= 0`` skips the comments call.
    """
    import httpx

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "piper-morgan",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    issue_url = f"{_API}/repos/{owner}/{repo}/issues/{issue_number}"

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.get(issue_url, headers=headers)
        if resp.status_code != 200:
            return None
        issue: Dict[str, Any] = resp.json()

        comments: List[Dict[str, Any]] = []
        if max_comments and max_comments > 0:
            cresp = await client.get(
                issue_url + "/comments",
                headers=headers,
                params={"per_page": min(max_comments, 100)},
            )
            if cresp.status_code == 200:
                data = cresp.json()
                if isinstance(data, list):
                    comments = data[:max_comments]
        issue["comments"] = comments
        return issue
