"""CXO 11-05 ask (#2262's nothing-new line), on beta (alpha redirects here since #2282) as web-seed-1386 (no Notion, nothing written lately):
"what's changed?" and the #2258 phrasing "What changed in the last hour?", each in a fresh session.
Usage: python dev/2026/11/05/served-2262-nothing-new.py <(cred file as key=value)>
"""

import sys
import time
import uuid

import requests

# alpha 308s /api/v1/* to beta since #2282 (11-05), and requests drops the auth header across hosts
B = "https://beta.pipermorgan.ai"
v = dict(line.strip().split("=", 1) for line in open(sys.argv[1]) if "=" in line)
s = requests.Session()
tok = s.post(
    B + "/api/v1/auth/login", data={"username": v["username"], "password": v["password"]}
).json()
s.headers["Authorization"] = "Bearer " + (tok.get("token") or tok.get("access_token"))
print("=== on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
for msg in ("what's changed?", "What changed in the last hour?"):
    r = s.post(
        B + "/api/v1/intent", json={"message": msg, "session_id": str(uuid.uuid4())}, timeout=180
    )
    d = r.json()
    it = d.get("intent") or {}
    print(
        f"\n--- [{time.strftime('%H:%M:%S')}, http {r.status_code}] route {it.get('category')}/{it.get('action')}"
    )
    print("USER:", msg)
    print("PIPER:", d.get("message") or d.get("response"))
    time.sleep(2)
print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
