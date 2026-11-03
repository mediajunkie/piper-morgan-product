"""#2230 part 2 and #2235 line 1 (standing item Q3), on the alpha promotion carrying e24cf93b00.
One login: read the GitHub card (/api/v1/integrations/health), then in one chat session ask to set the default
repo, decline the confirm, ask again and accept, so the set writes and the reply says whether it was validated.
Then P2 and P2e as a regression read (armed draft; answers "no", files nothing).
Usage: python dev/2026/11/02/setdefault-part2-2230.py <(cred file as key=value)>
"""

import json
import sys
import time
import uuid

import requests

B = "https://alpha.pipermorgan.ai"
v = dict(l.strip().split("=", 1) for l in open(sys.argv[1]) if "=" in l)
s = requests.Session()
tok = s.post(
    B + "/api/v1/auth/login", data={"username": v["username"], "password": v["password"]}
).json()
s.headers["Authorization"] = "Bearer " + (tok.get("token") or tok.get("access_token"))
print("=== on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
ASK = "Set my default GitHub repository to dinp-machine/piper-test-activity"


def turn(label, sid, msg):
    r = s.post(B + "/api/v1/intent", json={"message": msg, "session_id": sid}, timeout=180)
    d = r.json()
    it = d.get("intent") or {}
    rep = d.get("message") or d.get("response") or ""
    print(
        f"\n--- {label} [{time.strftime('%H:%M:%S')}, http {r.status_code}] route {it.get('category')}/{it.get('action')}\nUSER: {msg}\nPIPER: {rep}"
    )
    time.sleep(2)
    return rep


r = s.get(B + "/api/v1/integrations/health", timeout=60)
print(f"\n## GitHub card, http {r.status_code}")
body = r.json()
items = body.get("integrations") if isinstance(body, dict) else body
for it in items or []:
    if "github" in json.dumps(it).lower()[:200]:
        print(json.dumps(it, indent=1))

sid = str(uuid.uuid4())
print(f"\n## P1 confirm offered, declined, then accepted; session {sid[:8]}")
turn("P1a", sid, ASK)
turn("P1b", sid, "no")
turn("P1c", sid, ASK)
turn("P1d", sid, "yes")

sid = str(uuid.uuid4())
print(f"\n## P2 regression read after an armed draft, session {sid[:8]}")
turn("P2a", sid, "Let's track this. Create a GitHub issue: 'Probe draft 1720'")
turn("P2b", sid, ASK)
turn("P2e", sid, "What's in my draft?")
turn("P2d", sid, "no")
print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
