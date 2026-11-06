"""Lead 11-06 ask (Arch's 07:54 baseline for #2219's selector): ten plain "show my todos" turns, each in a fresh
session, on beta while it serves the pre-selector build, as web-seed-1386 (PA's own). Wall-clock round trip per turn.
Usage: python served-2219-baseline-list-turn-time.py <(cred file as key=value)>
"""

import statistics
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
times = []
for i in range(10):
    t0 = time.monotonic()
    r = s.post(
        B + "/api/v1/intent",
        json={"message": "show my todos", "session_id": str(uuid.uuid4())},
        timeout=180,
    )
    dt = time.monotonic() - t0
    d = r.json()
    it = d.get("intent") or {}
    head = (d.get("message") or d.get("response") or "").splitlines()[0]
    times.append(dt)
    print(
        f"{i + 1:2d} {time.strftime('%H:%M:%S')} http {r.status_code} {dt:6.2f} s  {it.get('category')}/{it.get('action')}  {head}"
    )
    time.sleep(2)
q = statistics.quantiles(times, n=4)
print(
    f"\nmedian {statistics.median(times):.2f} s  IQR {q[0]:.2f}-{q[2]:.2f} s  min {min(times):.2f}  max {max(times):.2f}"
)
print("=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
