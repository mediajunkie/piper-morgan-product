"""#2230 probe (Arch, 10-31; rerun 11-02 with the flag live). Two fresh sessions on alpha: P1 asks to set the default repo cold;
P2 asks it after an armed issue draft. Answers "no" to any confirm, so nothing is written and nothing is filed.
Usage: python dev/2026/11/02/setdefault-probe-2230.py <(cred file as key=value)>
"""

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
print("=== on", requests.get(B + "/health").json()["git_sha"][:10])
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


def maybe_no(label, sid, rep):
    low = rep.lower()
    if "didn't recognize" not in low and ("?" in rep or "confirm" in low or "yes" in low):
        turn(label, sid, "no")


sid = str(uuid.uuid4())
print(f"\n## P1 unarmed, session {sid[:8]}")
maybe_no("P1b", sid, turn("P1a", sid, ASK))
sid = str(uuid.uuid4())
print(f"\n## P2 after an armed draft, session {sid[:8]}")
turn("P2a", sid, "Let's track this. Create a GitHub issue: 'Probe draft 1720'")
maybe_no("P2c", sid, turn("P2b", sid, ASK))
turn("P2d", sid, "no")
