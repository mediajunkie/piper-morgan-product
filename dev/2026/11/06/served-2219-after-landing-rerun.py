"""Rerun of two rows from served-2219-after-landing.py (11-06), on beta as web-seed-1386 (PA's own test account):
row 3, "complete the second one" on a one-copy line, which asked instead of completing; and CXO's exact row 5,
"delete the third one" on the grouped line, right after a shown list. Fresh state made through /api/v1/todos. Every
delete confirm is declined.
Usage: python served-2219-after-landing-rerun.py <(cred file as key=value)>
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


def todos():
    return s.get(B + "/api/v1/todos").json()["todos"]


def reset():
    for t in todos():
        assert s.delete(B + f"/api/v1/todos/{t['id']}").status_code == 200
    for text, p in [("urgent task", "urgent"), ("high task", "high")] + [
        ("review prs", "medium")
    ] * 3:
        assert s.post(B + "/api/v1/todos", json={"title": text, "priority": p}).status_code in (
            200,
            201,
        )
        time.sleep(1.1)
    print("STATE:", [(t["status"], t["priority"], t["text"]) for t in todos()])


def chat(sid, msg):
    t0 = time.monotonic()
    r = s.post(B + "/api/v1/intent", json={"message": msg, "session_id": sid}, timeout=180)
    d = r.json()
    it = d.get("intent") or {}
    print(
        f"\n--- [{time.strftime('%H:%M:%S')}, http {r.status_code}, {time.monotonic() - t0:.2f} s] "
        f"route {it.get('category')}/{it.get('action')}"
    )
    print("USER:", msg)
    print("PIPER:", d.get("message") or d.get("response"))
    time.sleep(2)


print("=== on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
for attempt in (1, 2):
    print(
        f"\n\n========== Row 3, attempt {attempt}: complete the second one (one-copy line), fresh session"
    )
    reset()
    sid = str(uuid.uuid4())
    chat(sid, "show my todos")
    chat(sid, "complete the second one")
    print("STATE:", [(t["status"], t["priority"], t["text"]) for t in todos()])

print("\n\n========== Row 5: delete the third one (grouped line), fresh session, declined")
reset()
sid = str(uuid.uuid4())
chat(sid, "show my todos")
chat(sid, "delete the third one")
chat(sid, "no")
chat(sid, "show my todos")
print("STATE:", [(t["status"], t["priority"], t["text"]) for t in todos()])

print("\n\n========== Row 5b: delete the second one (one-copy line), fresh session, declined")
sid = str(uuid.uuid4())
chat(sid, "show my todos")
chat(sid, "delete the second one")
chat(sid, "no")
print("STATE:", [(t["status"], t["priority"], t["text"]) for t in todos()])
print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
