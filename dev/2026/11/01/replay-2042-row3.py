"""#2042 preregistered check (Arch, #2042 comment 2026-11-01 04:29Z): replay #1386 row 3's 19 prompts
(10-29, `dev/2026/10/29/1386-row3-scenarios-B-C-K-api-transcripts-2026-10-29.md`) on a served build, then
run the rung-2 scanner (`record_references`) and `reference_relations` over each new reply.

Pass (Arch): no relation that isn't in context, and no unasked "Also..." aside on a turn about something
else. The scanner decides the first half; the aside half is printed for CXO to judge.

Usage (password never printed; cred file passed by process substitution):
  PIPER_BASE_URL=https://piper-morgan-staging.fly.dev PIPER_CRED_FILE=<(...) \
    python dev/2026/11/01/replay-2042-row3.py [milestone title ...]
Milestone titles default to the test repo's open milestones read with `gh` (dinp-machine/piper-test-activity).
B2/B4 create and retitle a real issue on the account's default repo, as row 3 always has.
"""

import json
import os
import subprocess
import sys
import time
import uuid

import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
from services.intent_service.floor_listed_records import (  # noqa: E402
    record_references,
    reference_relations,
)

BLOCKS = [
    (
        "B (first run, no file-it turn)",
        [
            ("Ba1", "I'm thinking through the search feature. Help me break it down."),
            (
                "Ba2",
                "Let's track this. Create a GitHub issue: 'Add search functionality to navigation bar'",
            ),
            (
                "Ba3",
                "Actually, change the title to 'Implement full-text search across nav and global search bar'",
            ),
            ("Ba4", "What issues did we create in this session?"),
        ],
    ),
    (
        "B (scored)",
        [
            ("B1", "I'm thinking through the search feature. Help me break it down."),
            (
                "B2",
                "Let's track this. Create a GitHub issue: 'Add search functionality to navigation bar'",
            ),
            ("B3", "file it as is"),
            (
                "B4",
                "Actually, change the title to 'Implement full-text search across nav and global search bar'",
            ),
            ("B5", "What issues did we create in this session?"),
        ],
    ),
    (
        "C",
        [
            ("C1", "Can you summarize my Notion docs for me?"),
            ("C2", "What about reading from my company GitBook wiki?"),
            ("C3", "What's in my Slack today?"),
            ("C4", "OK, what CAN you actually do right now?"),
            ("C5", "Is my calendar connected?"),
            ("C6", "What integrations do I have?"),
        ],
    ),
    (
        "K",
        [
            ("K1", "What's on my calendar today?"),
            ("K2", "How about on Thursday?"),
            ("K3", "Do I have any meetings this week?"),
            ("K4", "What's my agenda Thursday?"),
        ],
    ),
]


def milestone_titles():
    if len(sys.argv) > 1:
        return sys.argv[1:]
    out = subprocess.run(
        [
            "gh",
            "api",
            "repos/dinp-machine/piper-test-activity/milestones?state=all",
            "--jq",
            ".[].title",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return [t for t in out.splitlines() if t.strip()]


def main():
    base = os.environ["PIPER_BASE_URL"].rstrip("/")
    vals = {}
    for line in open(os.environ["PIPER_CRED_FILE"]):
        if "=" in line:
            k, v = line.split("=", 1)
            vals[k.strip()] = v.strip()
    titles = milestone_titles()
    # No context item carries a milestone today, so any relation found is one not in context.
    ctx = {"active_milestones": [{"title": t} for t in titles]}

    s = requests.Session()
    r = s.post(
        base + "/api/v1/auth/login",
        data={"username": vals["username"], "password": vals["password"]},
    )
    s.headers["Authorization"] = "Bearer " + (r.json().get("token") or r.json().get("access_token"))
    sha = requests.get(base + "/health", timeout=10).json().get("git_sha", "")[:10]
    print(
        f"=== #2042 row-3 replay on {base} at {sha} as {vals['username']}; milestones: {titles} ==="
    )

    flagged = []
    for title, turns in BLOCKS:
        sid = str(uuid.uuid4())
        print(f"\n## {title}, session {sid[:8]}")
        for label, msg in turns:
            t0 = time.time()
            resp = s.post(
                base + "/api/v1/intent", json={"message": msg, "session_id": sid}, timeout=180
            )
            try:
                d = resp.json()
            except ValueError:
                d = {}
            it = d.get("intent") or {}
            text = d.get("message") or d.get("response") or d.get("detail") or resp.text[:300]
            refs = record_references(text)
            rel = reference_relations(text, refs, ctx)
            bad = {k: v for k, v in rel.items() if not all(v.values())}
            if bad:
                flagged.append((label, bad))
            print(
                f"\n--- {label} [{time.strftime('%H:%M:%S')}, {time.time() - t0:.1f}s, http {resp.status_code}] ---"
            )
            print(f"USER: {msg}")
            print(f"route: {it.get('category')}/{it.get('action')}")
            print(f"refs: {refs} relations: {json.dumps(rel)}")
            print(f"PIPER: {text}")
            time.sleep(2)

    print("\n=== SCANNER SUMMARY ===")
    print(f"turns: {sum(len(t) for _, t in BLOCKS)}; relations not in context: {len(flagged)}")
    for label, bad in flagged:
        print(f"  {label}: {json.dumps(bad)}")
    print(
        'Aside half: not machine-judged. CXO reads each reply for an unasked "Also..." on a turn about something else.'
    )


if __name__ == "__main__":
    main()
