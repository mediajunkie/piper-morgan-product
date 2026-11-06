"""One chat turn on beta as web-seed-1386 (PA's own test account), in a named session, appended to a transcript.
For reproductions where the next message depends on Piper's last reply (#2271, 11-06).
Usage: python turn.py <(cred file as key=value) <session-id> <transcript> "<message>"
"""

import sys
import time

import requests

# alpha 308s /api/v1/* to beta since #2282 (11-05), and requests drops the auth header across hosts
B = "https://beta.pipermorgan.ai"
v = dict(line.strip().split("=", 1) for line in open(sys.argv[1]) if "=" in line)
sid, out, msg = sys.argv[2], sys.argv[3], sys.argv[4]
s = requests.Session()
tok = s.post(
    B + "/api/v1/auth/login", data={"username": v["username"], "password": v["password"]}
).json()
s.headers["Authorization"] = "Bearer " + (tok.get("token") or tok.get("access_token"))
sha = requests.get(B + "/health").json()["git_sha"][:10]
t0 = time.monotonic()
r = s.post(B + "/api/v1/intent", json={"message": msg, "session_id": sid}, timeout=180)
d = r.json()
it = d.get("intent") or {}
block = (
    f"\n--- [{time.strftime('%H:%M:%S')}, {sha}, http {r.status_code}, {time.monotonic() - t0:.2f} s] "
    f"route {it.get('category')}/{it.get('action')}\nUSER: {msg}\nPIPER: {d.get('message') or d.get('response')}\n"
)
open(out, "a").write(block)
print(block)
