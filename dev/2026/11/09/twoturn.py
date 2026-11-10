"""One sign-in on beta, then N chat turns on the same token a few seconds apart (Lead's #2334 served check)."""
import sys, time, requests
B = "https://beta.pipermorgan.ai"
v = dict(line.strip().split("=", 1) for line in open(sys.argv[1]) if "=" in line)
sid, out, gap, msgs = sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5:]
s = requests.Session()
lr = s.post(B + "/api/v1/auth/login", data={"username": v["username"], "password": v["password"]})
tok = lr.json()
s.headers["Authorization"] = "Bearer " + (tok.get("token") or tok.get("access_token"))
sha = requests.get(B + "/health").json()["git_sha"][:10]
blocks = [f"\n# one sign-in at {time.strftime('%H:%M:%S')} on {sha}: login http {lr.status_code}; every turn below reuses that one token"]
for i, msg in enumerate(msgs):
    if i: time.sleep(gap)
    t0 = time.monotonic()
    r = s.post(B + "/api/v1/intent", json={"message": msg, "session_id": sid}, timeout=180)
    d = r.json(); it = d.get("intent") or {}
    blocks.append(f"\n--- [{time.strftime('%H:%M:%S')}, {sha}, http {r.status_code}, {time.monotonic() - t0:.2f} s] "
                  f"route {it.get('category')}/{it.get('action')}\nUSER: {msg}\nPIPER: {d.get('message') or d.get('response') or d}\n")
open(out, "a").write("".join(blocks)); print("".join(blocks))
