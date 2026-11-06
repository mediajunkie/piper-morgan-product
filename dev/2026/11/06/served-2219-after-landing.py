"""Lead 11-06 09:15 served list (CXO's rows) for #2219 / #2294 / #2295 after the promotion carrying f32b9518d2, on beta
(alpha redirects here since #2282) as web-seed-1386, PA's own test account. Every todo here is made by this script
through /api/v1/todos (the account's earlier test todos are exported first, then deleted). Every delete confirm is
declined. Ends with the ten timed plain list turns (the selector's after-run) and the one-todo header.
Usage: python served-2219-after-landing.py <(cred file as key=value) <export.json>
"""

import json
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


def todos():
    return s.get(B + "/api/v1/todos").json()["todos"]


def clear():
    for t in todos():
        assert s.delete(B + f"/api/v1/todos/{t['id']}").status_code == 200, t["id"]


def add(text, priority="medium"):
    r = s.post(B + "/api/v1/todos", json={"title": text, "priority": priority})
    assert r.status_code in (200, 201), r.text
    time.sleep(1.1)  # distinct created_at, so oldest-first within a priority is visible
    return r.json()


def state(label="STATE"):
    print(f"{label}:", [(t["status"], t["priority"], t["text"]) for t in todos()])


def chat(sid, msg):
    t0 = time.monotonic()
    r = s.post(B + "/api/v1/intent", json={"message": msg, "session_id": sid}, timeout=180)
    dt = time.monotonic() - t0
    d = r.json()
    it = d.get("intent") or {}
    print(
        f"\n--- [{time.strftime('%H:%M:%S')}, http {r.status_code}, {dt:.2f} s] route {it.get('category')}/{it.get('action')}"
    )
    print("USER:", msg)
    print("PIPER:", d.get("message") or d.get("response"))
    time.sleep(2)
    return dt


def row(title):
    print(f"\n\n========== {title}")
    return str(uuid.uuid4())


print("=== on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
json.dump(todos(), open(sys.argv[2], "w"), indent=1, default=str)
clear()
dentist = add("call the dentist")
add("urgent task", "urgent")
add("high task", "high")
for _ in range(3):
    add("review prs")

sid = row(
    "Row 1: numbered list, (high) chip, oldest first within a priority (call the dentist made before review prs)"
)
state()
chat(sid, "show my todos")
row("Row 9: the order the Todos page's API returns (GET /api/v1/todos)")
state("API ORDER")

assert s.delete(B + f"/api/v1/todos/{dentist['id']}").status_code == 200
sid = row("Rows 3 to 5: ordinals after the shown list (urgent, high, review prs x3)")
state()
chat(sid, "show my todos")
chat(sid, "complete the second one")
chat(sid, "complete the third one")
chat(sid, "one")
chat(sid, "show my todos")  # CXO 09:16: the list after the step, so review prs (x2) is visible
chat(
    sid, "delete the second one"
)  # the re-show renumbers: high task is done, so review prs is line 2
chat(sid, "no")
chat(sid, "show my todos")  # and after the declined delete: still (x2)
state()

sid = row("Row 6: delete the first one, fresh session, no list shown")
chat(sid, "delete the first one")
chat(sid, "no")

sid = row("Row 7a: next todo, fresh session")
chat(sid, "what's my next todo?")
sid = row("Row 7b: completed todos, fresh session")
chat(sid, "show my completed todos")

row("Row 8: the selector's after-run, ten plain 'show my todos' turns, fresh sessions")
state()
times = [chat(str(uuid.uuid4()), "show my todos") for _ in range(10)]
q = statistics.quantiles(times, n=4)
print("\nTIMES:", " ".join(f"{t:.2f}" for t in times))
print(
    f"median {statistics.median(times):.2f} s  IQR {q[0]:.2f}-{q[2]:.2f} s  min {min(times):.2f}  max {max(times):.2f}"
)

sid = row("Row 2: exactly one open todo")
clear()
add("call the dentist")
state()
chat(sid, "show my todos")
print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
