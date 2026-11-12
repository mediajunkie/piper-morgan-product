#!/usr/bin/env python3
"""github_app_refresh_check.py: ADR-081 D3's refresh check as ONE command (#2341).

For the person who holds the secrets (xian). It asks for each secret once with the
input hidden, does every step itself, and prints only the block to paste back.

    venv/bin/python scripts/github_app_refresh_check.py --issue 43 \\
        --uninstalled-private-repo OWNER/PRIVATE-REPO

What it does, in order:

1. Asks for the App's client ID, its client secret, the ``ghr_`` refresh token and
   the old ``ghu_`` access token. Nothing typed is shown.
2. Refreshes the token with GitHub.
3. Checks the OLD access token is now refused (``GET /user`` answers 401).
4. Starts ``fly proxy`` to the github-mcp sidecar itself (with
   ``FLY_NO_UPDATE_CHECK=1``; flyctl's self-upgrade check kills a pinned flyctl),
   unless ``--mcp-url`` names a server that is already reachable.
5. Runs ``github_app_token_check.py`` with the NEW token.
6. Stops the proxy.
7. Prints the paste-back block: the refresh result, the 401 line and the table.
8. Offers, apart from that block, to show the new refresh token once so it can be
   saved. A refresh replaces the refresh token; the old one stops working.

Secrets: read with ``getpass`` only. They are never placed in argv (so ``ps`` cannot
see them), never written to a file and never logged. The new access token reaches the
check through its environment. Nothing secret is in the paste-back block.

Concept: docs/internal/architecture/adrs/adr-081-github-identity-one-app-whose-token-serves-a-request.md
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import socket
import subprocess  # noqa: S404 - runs flyctl and the sibling check script, fixed argv
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
CHECK_SCRIPT = ROOT / "scripts" / "github_app_token_check.py"
TOKEN_URL = "https://github.com/login/oauth/access_token"  # noqa: S105 - an endpoint
USER_URL = "https://api.github.com/user"
SIDECAR_APP = "piper-morgan-gh-mcp"
SIDECAR_PORT = 8082
DEFAULT_REPO = "dinp-machine/piper-test-activity"
BLOCK_START = "===== paste this block back ====="
BLOCK_END = "===== end of block ====="

# (prompt, required). Order is the order asked.
PROMPTS: List[Tuple[str, str, bool]] = [
    ("client_id", "GitHub App client ID", True),
    ("client_secret", "GitHub App client secret", True),
    ("refresh_token", "Refresh token (ghr_…)", True),
    ("old_token", "OLD access token (ghu_…), or Enter to skip the 401 check", False),
]


def ask_secrets(ask: Callable[[str], str] = getpass.getpass) -> Dict[str, str]:
    """Ask for each secret once, hidden. A required one left empty is asked again once."""
    out: Dict[str, str] = {}
    for key, label, required in PROMPTS:
        value = ask(f"{label} (input hidden): ").strip()
        if required and not value:
            value = ask(f"{label} is needed (input hidden): ").strip()
        if required and not value:
            raise SystemExit(f"stopped: no {label.lower()} given")
        out[key] = value
    return out


def _post_form(url: str, fields: Dict[str, str]) -> Tuple[int, Dict[str, object]]:
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(  # noqa: S310 - fixed https endpoint
        url, data=data, headers={"Accept": "application/json", "User-Agent": "d3-refresh-check"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "{}")
        except ValueError:
            return e.code, {}


def _get_status(url: str, token: str) -> int:
    req = urllib.request.Request(  # noqa: S310 - fixed https endpoint
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "d3-refresh-check",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
            return int(resp.status)
    except urllib.error.HTTPError as e:
        return int(e.code)


def refresh(
    secrets: Dict[str, str],
    post: Callable[[str, Dict[str, str]], Tuple[int, Dict[str, object]]] = _post_form,
) -> Tuple[Optional[Dict[str, object]], str]:
    """Refresh the token. Returns (the reply or None, a line that carries no secret)."""
    status, body = post(
        TOKEN_URL,
        {
            "client_id": secrets["client_id"],
            "client_secret": secrets["client_secret"],
            "grant_type": "refresh_token",
            "refresh_token": secrets["refresh_token"],
        },
    )
    if status != 200 or "access_token" not in body:
        # GitHub's error code (for example bad_refresh_token) names no secret.
        code = str(body.get("error") or f"HTTP {status}")
        return None, f"refresh                      FAIL {code}"
    hours = int(body.get("expires_in") or 0) / 3600
    days = int(body.get("refresh_token_expires_in") or 0) / 86400
    return body, (
        "refresh                      PASS "
        f"(new access token good for {hours:.0f} h, new refresh token for {days:.0f} days)"
    )


def old_token_line(old_token: str, get: Callable[[str, str], int] = _get_status) -> str:
    if not old_token:
        return "old token GET /user          SKIPPED (no old token given)"
    status = get(USER_URL, old_token)
    verdict = "PASS" if status == 401 else "FAIL"
    return f"old token GET /user          {verdict} (HTTP {status}; 401 means it was revoked)"


def _port_open(port: int) -> bool:
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def start_proxy(port: int = SIDECAR_PORT, wait_s: float = 20.0) -> subprocess.Popen:
    """Start ``fly proxy`` to the sidecar and wait until the local port answers."""
    env = dict(os.environ, FLY_NO_UPDATE_CHECK="1")
    proc = subprocess.Popen(  # noqa: S603,S607 - fixed argv, no secret in it
        ["fly", "proxy", f"{port}:{SIDECAR_PORT}", "-a", SIDECAR_APP],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    deadline = time.monotonic() + wait_s
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise SystemExit(
                "stopped: `fly proxy` exited at once. Run `fly auth login` and try again."
            )
        if _port_open(port):
            return proc
        time.sleep(0.25)
    stop_proxy(proc)
    raise SystemExit(f"stopped: `fly proxy` did not open port {port} in {wait_s:.0f} s")


def stop_proxy(proc: Optional[subprocess.Popen]) -> None:
    if proc is None or proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def check_argv(ns: argparse.Namespace, mcp_url: str) -> List[str]:
    """The check's command line. It carries no secret; the token goes in the environment."""
    argv = [
        sys.executable,
        str(CHECK_SCRIPT),
        "--repo",
        ns.repo,
        "--mcp-url",
        mcp_url,
        "--uninstalled-private-repo",
        ns.uninstalled_private_repo,
    ]
    if ns.issue is not None:
        argv += ["--writes", "--issue", str(ns.issue)]
    return argv


def run_check(ns: argparse.Namespace, mcp_url: str, new_token: str) -> Tuple[int, str]:
    env = dict(os.environ, GITHUB_CHECK_TOKEN=new_token)
    done = subprocess.run(  # noqa: S603 - fixed argv built above, token in env only
        check_argv(ns, mcp_url), env=env, capture_output=True, text=True, cwd=str(ROOT)
    )
    table = [
        line
        for line in done.stdout.splitlines()
        if "  PASS" in line
        or "  FAIL" in line
        or "  SKIPPED" in line
        or "  INFO" in line
        or "  OK, NO NUMBER" in line
        or line.startswith("--- ")
        or line.startswith("refusing:")
    ]
    if not table:
        table = [f"the check printed no table (exit {done.returncode})"]
    return done.returncode, "\n".join(table)


def scrub(text: str, secrets: List[str]) -> str:
    """Belt and braces: no secret this run held can appear in what is printed."""
    for s in secrets:
        if s:
            text = text.replace(s, "[hidden]")
    return text


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="ADR-081 D3 refresh check as one command (#2341)")
    p.add_argument("--repo", default=DEFAULT_REPO, help="the TEST repository (owner/name)")
    p.add_argument(
        "--uninstalled-private-repo",
        required=True,
        help="owner/name of a PRIVATE repository the App is NOT installed on",
    )
    p.add_argument(
        "--issue",
        type=int,
        default=None,
        help="also read, comment on and close this EXISTING issue in the test repository",
    )
    p.add_argument(
        "--mcp-url",
        default=None,
        help="a github-mcp-server that is already reachable; omit to start `fly proxy`",
    )
    ns = p.parse_args(argv)

    secrets = ask_secrets()
    reply, refresh_line = refresh(secrets)
    lines = [refresh_line]
    code = 1
    held = list(secrets.values())
    if reply is not None:
        new_token = str(reply["access_token"])
        new_refresh = str(reply.get("refresh_token") or "")
        held += [new_token, new_refresh]
        lines.append(old_token_line(secrets["old_token"]))
        proxy = None
        try:
            if ns.mcp_url:
                mcp_url = ns.mcp_url
            else:
                proxy = start_proxy()
                mcp_url = f"http://localhost:{SIDECAR_PORT}/mcp"
            code, table = run_check(ns, mcp_url, new_token)
            lines.append(table)
        finally:
            stop_proxy(proxy)
        if "FAIL" in lines[1]:
            code = code or 1

    print()
    print(BLOCK_START)
    print(scrub("\n".join(lines), held))
    print(BLOCK_END)

    if reply is not None and reply.get("refresh_token"):
        print()
        print("The refresh REPLACED your refresh token. The old one no longer works.")
        answer = input("Show the new refresh token once, to save it? Not part of the block. [y/N] ")
        if answer.strip().lower() in ("y", "yes"):
            print("----- new refresh token (save it, then clear the screen) -----")
            print(str(reply["refresh_token"]))
            print("----- end -----")
        else:
            print("Not shown. It is gone when this command ends; a new sign-in mints another.")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
