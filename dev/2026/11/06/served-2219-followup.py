"""Follow-up to served-2219-2293-todo-lists.py (11-06): the done-items header, the noun with a real reminder,
and the confirm after a numbered list. Same account (web-seed-1386, PA's own); every todo or reminder here is
made by PA. Starts from that script's end state (5 open todos, one per priority). Every confirm is declined.
Usage: python served-2219-followup.py <(cred file as key=value)>
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


def chat(sid, msg):
    r = s.post(B + "/api/v1/intent", json={"message": msg, "session_id": sid}, timeout=180)
    d = r.json()
    it = d.get("intent") or {}
    print(
        f"\n--- [{time.strftime('%H:%M:%S')}, http {r.status_code}] route {it.get('category')}/{it.get('action')}"
    )
    print("USER:", msg)
    print("PIPER:", d.get("message") or d.get("response"))
    time.sleep(2)


def state():
    rows = sorted(
        (t["status"], t["priority"], t["text"]) for t in s.get(B + "/api/v1/todos").json()["todos"]
    )
    print("STATE:", len(rows), "todos:", rows)


print("=== on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
todo = s.get(B + "/api/v1/todos").json()["todos"]
low = [t for t in todo if t["text"] == "low task"][0]
assert s.post(B + f"/api/v1/todos/{low['id']}/complete").status_code == 200
state()

print("\n\n========== A: the done-items header (one of 5 done)")
for msg in ("show my todos", "show all my todos including done ones", "show my completed todos"):
    chat(str(uuid.uuid4()), msg)

print("\n\n========== B: confirm after a numbered list (declined)")
sid = str(uuid.uuid4())
chat(sid, "show my todos")
chat(sid, "complete the first one")
chat(sid, "complete the first one")
chat(sid, "no")

print("\n\n========== C: the noun with a real reminder (declined)")
sid = str(uuid.uuid4())
chat(sid, "remind me to call mom tomorrow at 9am")
chat(sid, "show my reminders")
chat(sid, "delete the first one")
chat(sid, "no")
chat(sid, "show my todos")
chat(sid, "delete the first one")
chat(sid, "no")
state()
print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
