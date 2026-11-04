"""CXO 11-03 18:32 served rechecks on alpha after the promotion to b0f774aabb, one account, sequential.
Order is set so the windows mean something: the nothing-new #2258 ask runs before any write, and Q7/Q29
run last, after this script's own writes (two filed drafts and one failed comment).
  N   #2258 nothing new: "What changed in the last hour?" before any write.
  G   #2042 aside: the B/Ba guidance prompt x3, fresh sessions (the other 18 prompts are the replay).
  W   #2042: a guidance turn then a work turn in one session; then Q21 and a reminders ask for per-item ages.
  T   #2098: the Ba3 pair x3 plus the original order. The answer turn follows the ask: "yes" to case 1, the
      title to case 2. Run 1 then files ("file it as is"); run 2 answers "no" and files (the old title).
  S   #2197: the status branch on an absent milestone name.
  F   #2258: one failed GitHub write (a comment on an issue number the test repo doesn't have).
  Q   #2258: Q7 and Q29, whole, after the writes.
The filed titles are read back with gh at the end.
Usage: python dev/2026/11/03/cxo-rechecks-b0f774aabb.py <(cred file as key=value)>
"""

import json
import subprocess
import sys
import time
import uuid

import requests

B = "https://alpha.pipermorgan.ai"
REPO = "dinp-machine/piper-test-activity"
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

GUIDE = "I'm thinking through the search feature. Help me break it down."
DRAFT = "Let's track this. Create a GitHub issue: 'Add search functionality to navigation bar'"
NEW_TITLE = "Implement full-text search across nav and global search bar"
RETITLE = f"Actually, change the title to '{NEW_TITLE}'"
CASE1 = "Do you want the draft's title changed to"
CASE2 = "What should the draft's title be?"


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
    return rep


def answer(rep, affirm=True):
    if not affirm:
        return "no"
    if CASE1 in rep:
        return "yes"
    return NEW_TITLE


def new():
    return str(uuid.uuid4())


print("\n## N: #2258 nothing new, before any write")
turn("N1", new(), "What changed in the last hour?")

print("\n## G: #2042 guidance prompt x3, fresh sessions")
for n in (1, 2, 3):
    turn(f"G{n}", new(), GUIDE)

print("\n## W: #2042 guidance then work, one session; then Q21 and the reminders ask")
sid = new()
turn("W1", sid, GUIDE)
turn("W2", sid, "What are my reminders?")
turn("W3", new(), "What should I focus on today?")
turn("W4", new(), "What are my reminders?")

print("\n## T: #2098 Ba3 pair x3 plus the original order")
for n, affirm, file_it in ((1, True, True), (2, False, True), (3, True, False)):
    sid = new()
    print(f"\n# T{n}: affirm={affirm} file={file_it}, session {sid[:8]}")
    turn(f"T{n}a", sid, DRAFT)
    rep = turn(f"T{n}b", sid, RETITLE)
    if CASE1 in rep or CASE2 in rep:
        turn(f"T{n}c", sid, answer(rep, affirm))
        if file_it:
            turn(f"T{n}d", sid, "file it as is")
    else:
        print(f"(T{n}b did not ask; answer and file skipped)")
sid = new()
print(f"\n# T4: original order (guidance, draft, retitle, answer), session {sid[:8]}")
turn("T4a", sid, GUIDE)
turn("T4b", sid, DRAFT)
rep = turn("T4c", sid, RETITLE)
if CASE1 in rep or CASE2 in rep:
    turn("T4d", sid, answer(rep))

print("\n## S: #2197 absent milestone")
turn("S1", new(), "how is the Gamma milestone going")

print("\n## F: #2258 one failed GitHub write")
sid = new()
rep = turn("F1", sid, f"Add a comment to issue #9999 in {REPO} saying 'PA 2258 probe'")
if "?" in rep[-200:]:
    turn("F2", sid, "yes")

print("\n## Q: #2258 Q7 and Q29, after the writes")
turn("Q7", new(), "What did we accomplish yesterday?")
turn("Q29", new(), "What changed since yesterday?")

print("\n## Test repo, newest issues (gh)")
out = subprocess.run(
    [
        "gh",
        "api",
        f"repos/{REPO}/issues?state=all&per_page=4",
        "-q",
        ".[] | [.number, .created_at, .title]",
    ],
    capture_output=True,
    text=True,
)
for line in out.stdout.splitlines():
    print(json.loads(line))
print("\n=== end on", requests.get(B + "/health").json()["git_sha"][:10], time.strftime("%H:%M:%S"))
