"""CXO 11-04 asks, on alpha as web-seed-1386: (1) the Integrations GitHub card (#2279 "Connected as");
(2) a not-found write turn (#2188's flag): the reply as served, then the conversation's stored turns,
which the page reads on reload, to check the reply is still there and what it saved.
Usage: python dev/2026/11/04/served-2188-reload-and-card.py <(cred file as key=value)> N
"""

import json
import sys
import time
import uuid

import requests

B = "https://alpha.pipermorgan.ai"
v = dict(line.strip().split("=", 1) for line in open(sys.argv[1]) if "=" in line)
N = sys.argv[2]
s = requests.Session()
tok = s.post(
    B + "/api/v1/auth/login", data={"username": v["username"], "password": v["password"]}
).json()
s.headers["Authorization"] = "Bearer " + (tok.get("token") or tok.get("access_token"))
print("=== on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))

r = s.get(B + "/api/v1/integrations/health", timeout=60)
print(f"\n## Integrations card, http {r.status_code}")
body = r.json()
items = body.get("integrations") if isinstance(body, dict) else body
for it in items or []:
    if "github" in json.dumps(it).lower()[:200]:
        print(json.dumps(it, indent=1))

sid = str(uuid.uuid4())
msg = f"Close issue #{N} in dinp-machine/piper-test-activity"
r = s.post(B + "/api/v1/intent", json={"message": msg, "session_id": sid}, timeout=180)
d = r.json()
it = d.get("intent") or {}
print(f"\n## Not-found write, session {sid[:8]}, http {r.status_code}")
print("route", it.get("category"), "/", it.get("action"))
print("USER:", msg)
print("PIPER:", d.get("message") or d.get("response"))
print("response keys:", sorted(d.keys()))
for k in ("success", "status", "error", "conversation_id"):
    if k in d:
        print(f"{k}:", d[k])
cid = d.get("conversation_id") or sid
time.sleep(3)
r = s.get(B + f"/api/v1/conversations/{cid}/turns", timeout=60)
print(f"\n## Stored turns (what a reload reads), conversation {str(cid)[:8]}, http {r.status_code}")
try:
    for t in r.json():
        print(json.dumps(t, indent=1)[:1500])
except Exception:
    print(r.text[:800])
print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
