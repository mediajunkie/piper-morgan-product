"""Lead 11-04 08:29: #2258 F1 on alpha 3f7994e873 (#1858's write-leg amendment), one account (web-seed-1386).
  F1  a comment on an issue the test repo doesn't have (#9998, so it can't be confused with 11-03's #9999 row).
  Q1  "What changed in the last hour?" (holds F1 only; expect "I tried to comment on issue #9998, but it didn't
      go through." with no cause).
  Q2  "What changed since yesterday?" (holds both; 11-03's #9999 row stays "couldn't confirm").
Usage: python dev/2026/11/04/served-f1-1858-3f7994e873.py <(cred file as key=value)>
"""

import sys
import time
import uuid

import requests

B = "https://alpha.pipermorgan.ai"
v = dict(line.strip().split("=", 1) for line in open(sys.argv[1]) if "=" in line)
s = requests.Session()
tok = s.post(
    B + "/api/v1/auth/login", data={"username": v["username"], "password": v["password"]}
).json()
s.headers["Authorization"] = "Bearer " + (tok.get("token") or tok.get("access_token"))
print("=== on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))


def turn(label, msg):
    t0 = time.time()
    r = s.post(
        B + "/api/v1/intent", json={"message": msg, "session_id": str(uuid.uuid4())}, timeout=180
    )
    dt = time.time() - t0
    d = r.json()
    it = d.get("intent") or {}
    rep = d.get("message") or d.get("response") or ""
    print(
        f"\n--- {label} [{time.strftime('%H:%M:%S')}, {dt:.2f}s, http {r.status_code}] "
        f"route {it.get('category')}/{it.get('action')}\nUSER: {msg}\nPIPER: {rep}"
    )
    time.sleep(2)


turn(
    "F1",
    "Add a comment to issue #9998 in dinp-machine/piper-test-activity saying 'PA 1858 probe'",
)
turn("Q1", "What changed in the last hour?")
turn("Q2", "What changed since yesterday?")
print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
