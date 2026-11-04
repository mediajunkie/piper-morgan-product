"""Lead 11-03 20:05: served checks on alpha 63d486043a, one account (web-seed-1386), sequential.
  A   #2098 answer turn: draft, retitle (expect case 2), type the title (expect the capture line), then
      "file it as is" (the filed title must be the typed one).
  B   #2098 "no": draft, retitle, "no" (expect the keep line), then "file it as is" (the old title).
  C   #2098 "yes" to case 1: two held-turn retitle phrasings; on case 1 answer "yes" and file. If neither
      reaches case 1, nothing is filed and the transcript says so.
  Q   #2265: "What did we accomplish yesterday?" (expect "since the start of yesterday, Monday, November 2")
      and a rolling ask (expect "in the past 24 hours"), after the writes.
Each run's draft title carries a distinct suffix so the duplicate guard on #38/#39 stays out of the way.
The filed titles are read back with gh at the end.
Usage: python dev/2026/11/03/served-2098-2265-63d486043a.py <(cred file as key=value)>
"""

import json
import subprocess
import sys
import time
import uuid

import requests

B = "https://alpha.pipermorgan.ai"
REPO = "dinp-machine/piper-test-activity"
v = dict(line.strip().split("=", 1) for line in open(sys.argv[1]) if "=" in line)
s = requests.Session()
tok = s.post(
    B + "/api/v1/auth/login", data={"username": v["username"], "password": v["password"]}
).json()
s.headers["Authorization"] = "Bearer " + (tok.get("token") or tok.get("access_token"))
print("=== on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))

CASE1 = "Do you want the draft's title changed to"
CASE2 = "What should the draft's title be?"
TAG = time.strftime("%H%M")


def turn(label, sid, msg):
    t0 = time.time()
    r = s.post(B + "/api/v1/intent", json={"message": msg, "session_id": sid}, timeout=180)
    dt = time.time() - t0
    d = r.json()
    it = d.get("intent") or {}
    rep = d.get("message") or d.get("response") or ""
    print(
        f"\n--- {label} [{time.strftime('%H:%M:%S')}, {dt:.2f}s, http {r.status_code}] "
        f"route {it.get('category')}/{it.get('action')}\nUSER: {msg}\nPIPER: {rep}"
    )
    time.sleep(2)
    return rep


def draft(n):
    return f"Let's track this. Create a GitHub issue: 'Add search to the {n} page {TAG}'"


def new():
    return str(uuid.uuid4())


sid = new()
title = f"Full-text search across the reports page {TAG}"
print(f"\n## A: answer turn binds, session {sid[:8]}")
turn("A1", sid, draft("reports"))
rep = turn("A2", sid, f"Actually, change the title to '{title}'")
print("A2 case:", "1" if CASE1 in rep else "2" if CASE2 in rep else "neither")
rep = turn("A3", sid, title if CASE2 in rep else ("yes" if CASE1 in rep else title))
turn("A4", sid, "file it as is")

sid = new()
print(f"\n## B: 'no' keeps the old title, session {sid[:8]}")
turn("B1", sid, draft("billing"))
rep = turn("B2", sid, f"Actually, change the title to 'Full-text search across billing {TAG}'")
print("B2 case:", "1" if CASE1 in rep else "2" if CASE2 in rep else "neither")
turn("B3", sid, "no")
turn("B4", sid, "file it as is")

print("\n## C: 'yes' to case 1, if a held-turn phrasing reaches it")
for n, phr in enumerate(
    ["Rename it to 'Search across the {p} page {t}'", "Make the title 'Search on {p} {t}'"], 1
):
    sid = new()
    p = ["profile", "admin"][n - 1]
    turn(f"C{n}a", sid, draft(p))
    rep = turn(f"C{n}b", sid, phr.format(p=p, t=TAG))
    if CASE1 in rep:
        turn(f"C{n}c", sid, "yes")
        turn(f"C{n}d", sid, "file it as is")
        break
    print(f"C{n}: case 1 not reached ({'case 2' if CASE2 in rep else 'neither'}); nothing filed")

print("\n## Q: #2265 after the writes")
turn("Q7", new(), "What did we accomplish yesterday?")
turn("QR", new(), "What changed in the last day?")

out = subprocess.run(
    ["gh", "api", f"repos/{REPO}/issues?state=all&per_page=6&sort=created"],
    capture_output=True,
    text=True,
)
print("\n## newest test-repo issues")
for i in json.loads(out.stdout or "[]"):
    print(i["number"], i["created_at"], i["title"])
print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
