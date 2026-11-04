"""#2042 follow-up on b0f774aabb: a guidance turn, then a work turn whose op adds the due-reminder line
(list_todos_query is in DUE_REMINDER_LINE_OPS; list_reminders_query is too, but its own answer shows the
reminders and adds no line), then the same work turn again, which should not mention them a second time.
Usage: python dev/2026/11/03/cxo-recheck-2042-guidance-then-todos.py <(cred file as key=value)>
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
print(
    "=== on",
    requests.get(B + "/health").json()["git_sha"][:10],
    "as",
    v["username"],
    time.strftime("%H:%M:%S"),
)


def turn(label, sid, msg):
    t0 = time.time()
    r = s.post(B + "/api/v1/intent", json={"message": msg, "session_id": sid}, timeout=180)
    dt = time.time() - t0
    d = r.json()
    it = d.get("intent") or {}
    rep = d.get("message") or d.get("response") or ""
    print(
        f"\n--- {label} [{time.strftime('%H:%M:%S')}, {dt:.2f}s, http {r.status_code}] "
        f"route {it.get('category')}/{it.get('action')}\nUSER: {msg}\nPIPER: {rep}"
    )
    time.sleep(2)


sid = str(uuid.uuid4())
print(f"\n## guidance, then todos twice, session {sid[:8]}")
turn("H1", sid, "I'm thinking through the search feature. Help me break it down.")
turn("H2", sid, "What's on my todo list?")
turn("H3", sid, "What's on my todo list?")
print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
