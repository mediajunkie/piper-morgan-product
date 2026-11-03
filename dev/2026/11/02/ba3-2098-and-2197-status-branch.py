"""CXO 11-02 18:52 asks, on alpha: (1) Ba3 rerun alone (#2098 possible regression): a pending draft's
"change the title", twice as the bare pair and once with the original guidance turn first; files nothing.
(2) #2197 status branch: three milestone asks, each in a fresh session, with client-side latency.
Usage: python dev/2026/11/02/ba3-2098-and-2197-status-branch.py <(cred file as key=value)>
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

GUIDE = "I'm thinking through the search feature. Help me break it down."
DRAFT = "Let's track this. Create a GitHub issue: 'Add search functionality to navigation bar'"
RETITLE = (
    "Actually, change the title to 'Implement full-text search across nav and global search bar'"
)


def turn(label, sid, msg):
    t0 = time.time()
    r = s.post(B + "/api/v1/intent", json={"message": msg, "session_id": sid}, timeout=180)
    dt = time.time() - t0
    d = r.json()
    it = d.get("intent") or {}
    rep = d.get("message") or d.get("response") or ""
    print(
        f"\n--- {label} [{time.strftime('%H:%M:%S')}, {dt:.2f}s, http {r.status_code}] route {it.get('category')}/{it.get('action')}\nUSER: {msg}\nPIPER: {rep}"
    )
    time.sleep(2)


for n in (1, 2):
    sid = str(uuid.uuid4())
    print(f"\n## Ba3 pair alone, run {n}, session {sid[:8]}")
    turn(f"R{n}a", sid, DRAFT)
    turn(f"R{n}b", sid, RETITLE)
sid = str(uuid.uuid4())
print(f"\n## Ba original order (guidance, draft, retitle), session {sid[:8]}")
turn("O1", sid, GUIDE)
turn("O2", sid, DRAFT)
turn("O3", sid, RETITLE)

print("\n## #2197 status branch, fresh session each")
for i, q in enumerate(
    [
        "what's the progress on the Beta launch milestone?",
        "how is the Beta launch milestone going",
        "how is the Gamma milestone going",
    ],
    1,
):
    turn(f"S{i}", str(uuid.uuid4()), q)
print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
