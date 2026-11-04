"""Second #2098 pass on alpha 63d486043a. The first pass (served-2098-2265-63d486043a.py) showed that
"change the title to 'X'" on a held draft now applies directly, so it never reached the title question;
"Rename it to 'X'" did reach case 2. This pass uses that phrasing to reach the answer turn.
  D   case 2, type the title (expect the capture line), "file it as is" (filed title = the typed one).
  E   case 2, "no" (expect the keep line), "file it as is" (filed title = the original).
Usage: python dev/2026/11/03/served-2098-answer-turn-63d486043a.py <(cred file as key=value)>
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


for run, page, ans in (("D", "inbox", None), ("E", "calendar", "no")):
    sid = str(uuid.uuid4())
    typed = f"Search across the {page} page {TAG}"
    print(
        f"\n## {run}: answer {'the typed title' if ans is None else repr(ans)}, session {sid[:8]}"
    )
    turn(
        f"{run}1",
        sid,
        f"Let's track this. Create a GitHub issue: 'Add search to the {page} page {TAG}'",
    )
    rep = turn(f"{run}2", sid, f"Rename it to '{typed}'")
    if CASE2 not in rep:
        print(f"{run}2: case 2 not reached; nothing filed")
        continue
    turn(f"{run}3", sid, typed if ans is None else ans)
    turn(f"{run}4", sid, "file it as is")

out = subprocess.run(
    ["gh", "api", f"repos/{REPO}/issues?state=all&per_page=4&sort=created"],
    capture_output=True,
    text=True,
)
print("\n## newest test-repo issues")
for i in json.loads(out.stdout or "[]"):
    print(i["number"], i["created_at"], i["title"])
print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
