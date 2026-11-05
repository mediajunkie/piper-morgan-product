"""CXO/Lead 11-04 degrade-alone check, for the window between xian's revoke of Piper under dinp-machine
and Web's reconnect (step d): on the account bound to dinp-machine, read the Integrations card, ask
"show my open issues" in a fresh session, then read the stored turns a reload restores.
Pass bar (CXO 19:06 memo): the reply is exactly the stale line and nothing else; the stored turn holds it.
Usage: python dev/2026/11/04/served-degrade-alone-window.py <(cred file as key=value)>
"""

import json
import sys
import time
import uuid

import requests

B = "https://alpha.pipermorgan.ai"
STALE = (
    "Your GitHub connection needs re-authorizing. Reconnect GitHub in Settings, under Integrations."
)
v = dict(line.strip().split("=", 1) for line in open(sys.argv[1]) if "=" in line)
s = requests.Session()
tok = s.post(
    B + "/api/v1/auth/login", data={"username": v["username"], "password": v["password"]}
).json()
s.headers["Authorization"] = "Bearer " + (tok.get("token") or tok.get("access_token"))
print("=== on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))


def card():
    r = s.get(B + "/api/v1/integrations/health", timeout=60)
    body = r.json()
    items = body.get("integrations") if isinstance(body, dict) else body
    for it in items or []:
        if it.get("name") == "github":
            print(f"card, http {r.status_code}:", json.dumps(it, indent=1))


print("\n## Card before the chat read")
card()
sid = str(uuid.uuid4())
msg = "show my open issues"
r = s.post(B + "/api/v1/intent", json={"message": msg, "session_id": sid}, timeout=180)
d = r.json()
rep = d.get("message") or d.get("response") or ""
print(f"\n## Chat read, session {sid[:8]}, http {r.status_code}")
print("intent:", json.dumps(d.get("intent"), indent=1))
print("USER:", msg)
print("PIPER:", rep)
print("exactly the stale line:", rep.strip() == STALE)
print("response keys:", sorted(d.keys()))
time.sleep(3)
r = s.get(B + f"/api/v1/conversations/{d.get('conversation_id') or sid}/turns", timeout=60)
print(f"\n## Stored turns (what a reload reads), http {r.status_code}")
print(json.dumps(r.json(), indent=1)[:2000])
print("\n## Card after the chat read")
card()
print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
