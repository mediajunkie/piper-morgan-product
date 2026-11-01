"""#2238 served save-then-chat, the chat half (PPM 2026-11-01 08:38: Web runs it on staging).

The Notion key is saved in the browser on the integrations page, never by this script, and this script
never reads, prints or sends a key. It signs in from a credential file (passed by process substitution),
asks the chat in a fresh session, and prints the replies for the quote.

Usage:
  PIPER_BASE_URL=https://piper-morgan-staging.fly.dev PIPER_CRED_FILE=<(...) \
    python dev/2026/11/01/notion-chat-check-2238.py ["<a page title in the throwaway workspace>"]
Run it once on the account that saved the key (expect a page from that workspace), and once with
PIPER_CRED_FILE pointing at a second account with no key (expect "not connected").
"""

import os
import sys
import time
import uuid

import requests

QUESTIONS = ["What's in my Notion?"]


def main():
    base = os.environ["PIPER_BASE_URL"].rstrip("/")
    vals = {}
    for line in open(os.environ["PIPER_CRED_FILE"]):
        if "=" in line:
            k, v = line.split("=", 1)
            vals[k.strip()] = v.strip()
    questions = QUESTIONS + [f"What does my Notion page '{t}' say?" for t in sys.argv[1:]]

    s = requests.Session()
    r = s.post(
        base + "/api/v1/auth/login",
        data={"username": vals["username"], "password": vals["password"]},
    )
    s.headers["Authorization"] = "Bearer " + (r.json().get("token") or r.json().get("access_token"))
    health = requests.get(base + "/health", timeout=10).json()
    print(
        f"=== #2238 chat half on {base} at {health.get('git_sha', '')[:10]} as {vals['username']} ==="
    )

    sid = str(uuid.uuid4())
    for q in questions:
        t0 = time.time()
        resp = s.post(base + "/api/v1/intent", json={"message": q, "session_id": sid}, timeout=180)
        try:
            d = resp.json()
        except ValueError:
            d = {}
        it = d.get("intent") or {}
        print(
            f"\n--- [{time.strftime('%H:%M:%S')}, {time.time() - t0:.1f}s, http {resp.status_code}] ---"
        )
        print(f"USER: {q}")
        print(f"route: {it.get('category')}/{it.get('action')}")
        print(
            f"PIPER: {d.get('message') or d.get('response') or d.get('detail') or resp.text[:300]}"
        )
        time.sleep(2)
    end = requests.get(base + "/health", timeout=10).json().get("git_sha", "")[:10]
    print(f"\n=== served sha at end: {end} ===")


if __name__ == "__main__":
    main()
