"""CXO 11-06 07:07 ask (#2219 grouped todo list and confirms, #2293 priority order), on beta (alpha redirects here
since #2282) as web-seed-1386, PA's own test account. Every todo here is created by this script through
/api/v1/todos; the account's earlier test todos are exported first and deleted, so each row starts from a known state.
Usage: python served-2219-2293-todo-lists.py <(cred file as key=value) <export.json>
"""

import json
import sys
import time
import uuid

import requests

# alpha 308s /api/v1/* to beta since #2282 (11-05), and requests drops the auth header across hosts
B = "https://beta.pipermorgan.ai"
v = dict(line.strip().split("=", 1) for line in open(sys.argv[1]) if "=" in line)
s = requests.Session()
tok = s.post(B + "/api/v1/auth/login", data={"username": v["username"], "password": v["password"]}).json()
s.headers["Authorization"] = "Bearer " + (tok.get("token") or tok.get("access_token"))


def todos():
    return s.get(B + "/api/v1/todos").json()["todos"]


def clear():
    for t in todos():
        assert s.delete(B + f"/api/v1/todos/{t['id']}").status_code == 200, t["id"]


def add(text, priority="medium"):
    r = s.post(B + "/api/v1/todos", json={"title": text, "priority": priority})
    assert r.status_code in (200, 201), r.text
    return r.json()


def state():
    rows = sorted((t["status"], t["priority"], t["text"]) for t in todos())
    print("STATE:", len(rows), "todos:", rows)


def chat(sid, msg):
    r = s.post(B + "/api/v1/intent", json={"message": msg, "session_id": sid}, timeout=180)
    d = r.json()
    it = d.get("intent") or {}
    print(f"\n--- [{time.strftime('%H:%M:%S')}, http {r.status_code}] route {it.get('category')}/{it.get('action')}")
    print("USER:", msg)
    print("PIPER:", d.get("message") or d.get("response"))
    time.sleep(2)


def row(title):
    print(f"\n\n========== {title}")
    return str(uuid.uuid4())


print("=== on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
json.dump(todos(), open(sys.argv[2], "w"), indent=1, default=str)
clear()

sid = row("Row 6: zero todos")
state()
chat(sid, "show my todos")

sid = row("Row 2: exactly 1 open todo")
dentist = add("call the dentist")
state()
chat(sid, "show my todos")

sid = row("Row 1: 3 distinct open todos, one added 3 times")
for _ in range(3):
    add("review prs")
add("write the release notes")
state()
chat(sid, "show my todos")

sid = row("Row 3: one item done")
assert s.post(B + f"/api/v1/todos/{dentist['id']}/complete").status_code == 200
state()
chat(sid, "show my todos")

sid = row("Row 4: the noun both ways, and the confirms (each declined)")
chat(sid, "show my reminders")
chat(sid, "show my todos")
chat(sid, "complete the first one")
chat(sid, "no")
chat(sid, "show my reminders")
chat(sid, "delete the first one")
chat(sid, "no")
state()

sid = row("Row 5 (#2293): one todo per priority, created low, unset, urgent, medium, high")
clear()
for text, p in [("low task", "low"), ("unset task", None), ("urgent task", "urgent"), ("medium task", "medium"), ("high task", "high")]:
    add(text, p)
state()
chat(sid, "show my todos")

print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
