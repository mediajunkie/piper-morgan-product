#!/usr/bin/env python3
"""github_app_token_check.py — #2174, ADR-081 D3's condition: do the deployed
github-mcp-server and GitHub's REST API accept a GitHub App USER ACCESS TOKEN for every
call Piper makes? Prints one row per call (``PASS`` / ``FAIL <status or error class>``) and
totals. Prints no token, no response body, no issue text.

The token is read from the environment variable ``GITHUB_CHECK_TOKEN`` only (never argv,
so it stays out of shell history and process lists). Run it from a checkout:

    GITHUB_CHECK_TOKEN=... venv/bin/python scripts/github_app_token_check.py \\
        --repo dinp-machine/piper-test-activity --mcp-url https://<the deployed server>/mcp

Reads only, by default. ``--writes`` also exercises the three write tools Piper calls
(create an issue, comment on it, close it), and refuses any repository but
``dinp-machine/piper-test-activity``. ``--uninstalled-private-repo`` names a private repository the
App is not installed on; its row passes only when GitHub refuses the read (the narrowing #2261
exists for).

The calls are the ones Piper makes today (``services/mcp/consumer/github_adapter.py``):
search_issues, search_pull_requests, search_repositories, list_issues, issue_read,
list_branches, list_releases, and with --writes issue_write (create, update) and
add_issue_comment; and the REST reads #2174 names: GET /user, the repo's milestones and
labels, and the account's repository list.

Concept: docs/internal/architecture/adrs/adr-081-github-identity-one-app-whose-token-serves-a-request.md
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

TOKEN_ENV = "GITHUB_CHECK_TOKEN"  # noqa: S105 - an env var name, not a value
# Arch 2026-11-04 20:21: --writes refuses any repository but the test one.
WRITES_ALLOWED_REPO = "dinp-machine/piper-test-activity"
REST = "https://api.github.com"


def rest_calls(owner: str, repo: str) -> List[Tuple[str, str]]:
    return [
        ("rest GET /user", "/user"),
        ("rest GET milestones", f"/repos/{owner}/{repo}/milestones?state=all&per_page=1"),
        ("rest GET labels", f"/repos/{owner}/{repo}/labels?per_page=1"),
        ("rest GET /user/repos", "/user/repos?per_page=1"),
    ]


def read_tools(owner: str, repo: str) -> List[Tuple[str, Dict[str, Any]]]:
    return [
        ("search_issues", {"query": f"repo:{owner}/{repo} is:issue", "perPage": 1}),
        ("search_pull_requests", {"query": f"repo:{owner}/{repo} is:pr", "perPage": 1}),
        ("search_repositories", {"query": "user:@me", "perPage": 1}),
        ("list_issues", {"owner": owner, "repo": repo, "state": "OPEN", "perPage": 1}),
        ("list_branches", {"owner": owner, "repo": repo, "perPage": 1}),
        ("list_releases", {"owner": owner, "repo": repo, "perPage": 1}),
    ]


async def run_narrowing(token: str, private_repo: str) -> List[Tuple[str, str]]:
    """Arch 20:21, the row #2261 exists for: a private repository the App is NOT installed
    on must be unreadable with this token. PASS here means GitHub refused it (404 or 403)."""
    import aiohttp

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    label = "narrowing: private repo not installed is refused"
    try:
        async with aiohttp.ClientSession(headers=headers) as s:
            async with s.get(f"{REST}/repos/{private_repo}") as r:
                if r.status in (403, 404):
                    return [(label, "PASS")]
                return [(label, f"FAIL readable ({r.status})")]
    except Exception as e:
        return [(label, f"FAIL {type(e).__name__}")]


async def run_rest(token: str, owner: str, repo: str) -> List[Tuple[str, str]]:
    import aiohttp

    rows = []
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    async with aiohttp.ClientSession(headers=headers) as s:
        for label, path in rest_calls(owner, repo):
            try:
                async with s.get(REST + path) as r:
                    rows.append((label, "PASS" if r.status == 200 else f"FAIL {r.status}"))
            except Exception as e:
                rows.append((label, f"FAIL {type(e).__name__}"))
    return rows


def _tool_ok(result: Any) -> bool:
    return not bool(getattr(result, "isError", False) or getattr(result, "is_error", False))


def _first_issue_number(result: Any) -> int | None:
    """The created issue's number from the MCP reply: a ``number`` field, else the
    ``/issues/N`` in its URL (xian's 11-07 run: github-mcp-server's create reply
    carried no ``number`` though #43 was created)."""
    import json
    import re

    def _from_url(value: Any) -> int | None:
        m = re.search(r"/issues/(\d+)", str(value or ""))
        return int(m.group(1)) if m else None

    for part in getattr(result, "content", []) or []:
        text = getattr(part, "text", "") or ""
        try:
            data = json.loads(text)
        except ValueError:
            m = re.search(r'"number"\s*:\s*(\d+)', text)
            return int(m.group(1)) if m else _from_url(text)
        if isinstance(data, dict):
            if "number" in data:
                return int(data["number"])
            for key in ("html_url", "url"):
                n = _from_url(data.get(key))
                if n is not None:
                    return n
    return None


def _server_version(client: Any) -> str:
    """``INFO <name> <version>`` as the server reported it, for the ADR's record."""
    info = getattr(client, "server_info", None)
    name = getattr(info, "name", None)
    version = getattr(info, "version", None)
    if not name and not version:
        return "INFO not reported"
    return f"INFO {name or '?'} {version or '?'}"


async def run_mcp(
    token: str, url: str, owner: str, repo: str, writes: bool, issue: int | None = None
) -> List[Tuple[str, str]]:
    from services.mcp.consumer.mcp_client import MCPClient

    rows: List[Tuple[str, str]] = []
    try:
        async with MCPClient.connect_http(url, headers={"Authorization": f"Bearer {token}"}) as c:
            rows.append(("mcp server (from its handshake)", _server_version(c)))
            for name, args in read_tools(owner, repo):
                try:
                    res = await c.call_tool(name, args)
                    rows.append((name, "PASS" if _tool_ok(res) else "FAIL tool-error"))
                except Exception as e:
                    rows.append((name, f"FAIL {type(e).__name__}"))
            created = None
            if writes and issue is not None:
                # --issue N: the write rows run against an existing issue, no new create.
                rows.append(("issue_write create", f"SKIPPED (--issue {issue})"))
                created = issue
            elif writes:
                try:
                    res = await c.call_tool(
                        "issue_write",
                        {
                            "method": "create",
                            "owner": owner,
                            "repo": repo,
                            "title": "D3 token check (safe to close)",
                            "body": "#2174 check; closed by the same run.",
                        },
                    )
                    ok = _tool_ok(res)
                    created = _first_issue_number(res) if ok else None
                    if not ok:
                        rows.append(("issue_write create", "FAIL tool-error"))
                    elif created is None:
                        # The create succeeded; only the reply's number was missing.
                        rows.append(("issue_write create", "OK, NO NUMBER (rerun with --issue N)"))
                    else:
                        rows.append(("issue_write create", "PASS"))
                except Exception as e:
                    rows.append(("issue_write create", f"FAIL {type(e).__name__}"))
            target = created
            if target is not None:
                for name, args in [
                    (
                        "issue_read get",
                        {"method": "get", "owner": owner, "repo": repo, "issue_number": target},
                    ),
                    (
                        "add_issue_comment",
                        {"owner": owner, "repo": repo, "issue_number": target, "body": "check"},
                    ),
                    (
                        "issue_write update (close)",
                        {
                            "method": "update",
                            "owner": owner,
                            "repo": repo,
                            "issue_number": target,
                            "state": "closed",
                        },
                    ),
                ]:
                    tool = name.split(" ")[0]
                    try:
                        res = await c.call_tool(tool, args)
                        rows.append((name, "PASS" if _tool_ok(res) else "FAIL tool-error"))
                    except Exception as e:
                        rows.append((name, f"FAIL {type(e).__name__}"))
            elif not writes:
                rows.append(("issue_read get", "SKIPPED (needs --writes for a known issue)"))
    except Exception as e:
        rows.append(("mcp connect", f"FAIL {type(e).__name__}"))
    return rows


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="#2174: does a GitHub App user token serve every call?")
    p.add_argument("--repo", required=True, help="owner/name of a TEST repository")
    p.add_argument("--mcp-url", required=True, help="the deployed github-mcp-server URL")
    p.add_argument(
        "--writes", action="store_true", help="also create, comment on and close one issue"
    )
    p.add_argument(
        "--issue",
        type=int,
        default=None,
        help="with --writes: read, comment on and close this EXISTING issue instead of creating one",
    )
    p.add_argument(
        "--uninstalled-private-repo",
        required=True,
        help="owner/name of a PRIVATE repository the App is NOT installed on (must be refused)",
    )
    ns = p.parse_args(argv)
    if ns.issue is not None and not ns.writes:
        print("refusing: --issue needs --writes")
        return 2
    if ns.writes and ns.repo != WRITES_ALLOWED_REPO:
        print(f"refusing: --writes only runs against {WRITES_ALLOWED_REPO}")
        return 2
    token = os.environ.get(TOKEN_ENV, "")
    if not token:
        print(f"refusing: set {TOKEN_ENV} (never pass a token on the command line)")
        return 2
    owner, _, repo = ns.repo.partition("/")
    if not owner or not repo:
        print("refusing: --repo must be owner/name")
        return 2
    rows = asyncio.run(run_rest(token, owner, repo))
    rows += asyncio.run(run_narrowing(token, ns.uninstalled_private_repo))
    rows += asyncio.run(run_mcp(token, ns.mcp_url, owner, repo, ns.writes, ns.issue))
    width = max(len(r[0]) for r in rows)
    for name, verdict in rows:
        print(f"{name.ljust(width)}  {verdict}")
    passed = sum(1 for _, v in rows if v == "PASS")
    failed = sum(1 for _, v in rows if v.startswith("FAIL"))
    calls = sum(1 for _, v in rows if not v.startswith("INFO"))
    print(f"--- {calls} calls: {passed} pass, {failed} fail")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
