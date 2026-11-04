"""#2258 F1 plus a close on a missing issue, for the alpha promotion carrying Lead's dbbb471671 (in-band 404)
and ad10279273 (CXO's write-turn sentence), one account (web-seed-1386).
  F1  a comment on a missing issue N1 (pass: "I couldn't find issue #N1 in dinp-machine/piper-test-activity, so
      nothing was changed. ...", never "There's no issue").
  C1  a close on a missing issue N2 (pass: the same sentence).
  Q1  "What changed in the last hour?" (pass: "I tried to comment on issue #N1, but it didn't go through.").
Pick fresh missing numbers each run (11-03 used 9999, 11-04 08:32 used 9998).
Usage: python dev/2026/11/04/served-f1-and-close-missing.py <(cred file as key=value)> N1 N2
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


N1, N2 = sys.argv[2], sys.argv[3]
turn(
    "F1", f"Add a comment to issue #{N1} in dinp-machine/piper-test-activity saying 'PA 1858 probe'"
)
turn("C1", f"Close issue #{N2} in dinp-machine/piper-test-activity")
turn("Q1", "What changed in the last hour?")
print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
