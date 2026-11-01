"""#2250 served before/after (PPM and Arch 2026-11-01 13:12): time a status ask that names no milestone.

Run once on the pre-promotion build and once on the post-promotion build, same account. Each ask goes in a
fresh session so no earlier turn feeds it. Wall-clock is measured client-side around POST /api/v1/intent,
so it includes the network; compare medians across builds, not single turns.

Usage (password never printed; cred file passed by process substitution):
  PIPER_BASE_URL=https://alpha.pipermorgan.ai PIPER_CRED_FILE=<(...) \
    python dev/2026/11/01/status-latency-2250.py [repeats]
"""

import os
import statistics
import sys
import time
import uuid

import requests

ASKS = ["What's the status of my project?", "How is my project going?"]


def main():
    base = os.environ["PIPER_BASE_URL"].rstrip("/")
    repeats = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    vals = {}
    for line in open(os.environ["PIPER_CRED_FILE"]):
        if "=" in line:
            k, v = line.split("=", 1)
            vals[k.strip()] = v.strip()

    s = requests.Session()
    r = s.post(
        base + "/api/v1/auth/login",
        data={"username": vals["username"], "password": vals["password"]},
    )
    s.headers["Authorization"] = "Bearer " + (r.json().get("token") or r.json().get("access_token"))
    sha = requests.get(base + "/health", timeout=10).json().get("git_sha", "")[:10]
    print(f"=== #2250 status latency on {base} at {sha} as {vals['username']} ===")

    times = {q: [] for q in ASKS}
    for i in range(repeats):
        for q in ASKS:
            t0 = time.time()
            resp = s.post(
                base + "/api/v1/intent",
                json={"message": q, "session_id": str(uuid.uuid4())},
                timeout=180,
            )
            dt = time.time() - t0
            try:
                d = resp.json()
            except ValueError:
                d = {}
            it = d.get("intent") or {}
            text = d.get("message") or d.get("response") or d.get("detail") or resp.text[:300]
            times[q].append(dt)
            print(
                f"\n--- run {i + 1} [{time.strftime('%H:%M:%S')}, {dt:.2f}s, http {resp.status_code}] ---"
            )
            print(f"USER: {q}")
            print(f"route: {it.get('category')}/{it.get('action')}")
            print(f"PIPER: {text[:400]}")
            time.sleep(2)

    end = requests.get(base + "/health", timeout=10).json().get("git_sha", "")[:10]
    print(f"\n=== SUMMARY at {sha} (end {end}) ===")
    for q, ts in times.items():
        print(
            f"{q!r}: n={len(ts)} median {statistics.median(ts):.2f}s "
            f"min {min(ts):.2f}s max {max(ts):.2f}s all {[round(t, 2) for t in ts]}"
        )


if __name__ == "__main__":
    main()
