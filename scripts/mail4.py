#!/usr/bin/env python3
"""mail4.py — mail v4 pilot: one file per message, read-side delivery, single-writer acks.

Design: dev/2026/10/03/spec-eval/proposal-mail-v4-fan-out-on-read.md (Spec, PM-approved 2026-10-03).
Ops doc: docs/internal/operations/mail-v4-pilot.md.

Messages live in the PRIVATE repo mediajunkie/piper-morgan-mail (clone at ~/Development/piper-morgan-mail,
override with PIPER_MAIL4_REPO). Every write is a commit built with commit-tree on top of a freshly
fetched origin/main (throwaway index, retried on a non-fast-forward), so the clone's working tree is
never read or written and two seats can't collide. Every read is from origin/main's objects.

  mail4.py send --to exec [--cc cio] --type fyi|task|decision-request|ruling-relay|reply \
                --subject "..." [--due YYYY-MM-DD[' HH:MM']|none] [--in-reply-to ID] [--body-file F | < body]
  mail4.py inbox [--role R] [--show|--ids]  unacknowledged messages addressed to R
  mail4.py read ID                          print one message
  mail4.py ack ID [read|done|declined] [--note "..."]
  mail4.py check [--canary]                 cohort-wide: denominator always printed, overdue listed
  mail4.py stats                            files and commits per message (pilot instrumentation)

Exit codes: 0 ok / clean; 1 overdue required-ack messages found; 2 canary failed or bad input;
3 could not measure (fetch error, no messages scanned). Never a bare all-clear: `check` always
prints what it scanned.

Pilot scope (the proposal's rule): only messages whose sender AND every recipient are pilot roles in
roles.yaml go through v4; anything else is refused with a pointer to scripts/mail-send.sh (v3).
PM ('xian') is never addressable (CLAUDE.md, PM ruling 2026-10-03): PM-bound items go to exec.

Cost: one fetch + one commit per send/ack. Benefit: none yet: measuring (pilot).
Review: 2026-10-22 done (dev/2026/10/22/mail-v4-pilot-review-2026-10-22.md); next 2026-11-05. Owner: CIO.
"""

import argparse
import datetime as dt
import os
import random
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

PT = ZoneInfo("America/Los_Angeles")
REPO = Path(os.environ.get("PIPER_MAIL4_REPO", str(Path.home() / "Development/piper-morgan-mail")))
TYPES = ("fyi", "task", "decision-request", "ruling-relay", "reply", "canary")
ACK_DEFAULT = {"task": True, "decision-request": True, "canary": True}
ACK_STATES = ("read", "done", "declined")
FORBIDDEN = ("xian", "pm", "ceo")
CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


class Unmeasured(Exception):
    pass


def git(*args, input=None, check=True):
    r = subprocess.run(
        ["git", "-C", str(REPO), *args],
        input=input,
        capture_output=True,
        text=isinstance(input, str) or input is None,
    )
    if check and r.returncode != 0:
        err = r.stderr if isinstance(r.stderr, str) else r.stderr.decode()
        raise RuntimeError(f"git {' '.join(args[:3])}: {err.strip()}")
    return r


def fetch_tip():
    if not (REPO / ".git").exists():
        raise Unmeasured(
            f"no clone at {REPO}: git clone git@github.com:mediajunkie/piper-morgan-mail.git {REPO}"
        )
    try:
        git("fetch", "-q", "origin", "main")
        return git("rev-parse", "origin/main").stdout.strip()
    except RuntimeError as e:
        raise Unmeasured(str(e))


def show(tip, path):
    r = git("show", f"{tip}:{path}", check=False)
    return r.stdout if r.returncode == 0 else None


def ls(tip, prefix):
    r = git("ls-tree", "-r", "--name-only", tip, "--", prefix, check=False)
    return [p for p in r.stdout.splitlines() if p]


def ulid():
    ms = int(time.time() * 1000)
    t = "".join(CROCKFORD[(ms >> (5 * i)) & 31] for i in reversed(range(10)))
    return t + "".join(random.choice(CROCKFORD) for _ in range(16))


def now_pt():
    return dt.datetime.now(PT)


def my_role():
    r = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
    b = r.stdout.strip()
    if b.startswith("claude/") and b.endswith("-cycle"):
        return b[len("claude/") : -len("-cycle")]
    return None


def load_roles(tip):
    txt = show(tip, "roles.yaml")
    if txt is None:
        raise Unmeasured("roles.yaml missing on origin/main of the mail repo")
    return (yaml.safe_load(txt) or {}).get("roles", {})


def commit(changes, message, attempts=6):
    """changes: {path: fn(old_text_or_None) -> new_text}. Rebuilt on the fresh tip every attempt."""
    for n in range(attempts):
        tip = fetch_tip()
        with tempfile.TemporaryDirectory() as td:
            env = dict(os.environ, GIT_INDEX_FILE=str(Path(td) / "index"))

            def g(*a, input=None):
                r = subprocess.run(
                    ["git", "-C", str(REPO), *a],
                    input=input,
                    capture_output=True,
                    text=True,
                    env=env,
                )
                if r.returncode != 0:
                    raise RuntimeError(f"git {a[0]}: {r.stderr.strip()}")
                return r.stdout.strip()

            g("read-tree", tip)
            for path, fn in changes.items():
                blob = g("hash-object", "-w", "--stdin", input=fn(show(tip, path)))
                g("update-index", "--add", "--cacheinfo", f"100644,{blob},{path}")
            tree = g("write-tree")
            c = g("commit-tree", tree, "-p", tip, "-m", message)
        r = git("push", "-q", "origin", f"{c}:refs/heads/main", check=False)
        if r.returncode == 0:
            return c
        time.sleep(1 + n)
    raise RuntimeError(f"push failed after {attempts} attempts")


def parse(text):
    if not text.startswith("---\n"):
        return {}, text
    head, _, body = text[4:].partition("\n---\n")
    return yaml.safe_load(head) or {}, body


def all_messages(tip):
    out = []
    for p in ls(tip, "messages"):
        if p.endswith(".md"):
            meta, body = parse(show(tip, p) or "")
            if meta.get("id"):
                meta["_path"] = p
                meta["_body"] = body
                out.append(meta)
    return out


def acks(tip, role):
    d = {}
    for line in (show(tip, f"acks/{role}.log") or "").splitlines():
        parts = line.split(" ", 3)
        if len(parts) >= 3:
            d.setdefault(parts[0], []).append(parts[2])
    return d


def last_ack(tip, role):
    # A seat can read and ack per message (`read ID`, `ack ID`) without ever running `inbox`, so a
    # missing canary alone doesn't mean unread mail (Exec, 10-28). Report the last non-canary ack too.
    days = []
    for line in (show(tip, f"acks/{role}.log") or "").splitlines():
        parts = line.split(" ", 3)
        if len(parts) >= 3 and not (len(parts) == 4 and parts[3].startswith("canary")):
            days.append(parts[1][:10])
    return max(days, default=None)


def recipients(m):
    return list(m.get("to") or []) + list(m.get("cc") or [])


def age_days(m):
    try:
        t = dt.datetime.fromisoformat(str(m["sent_at"]))
        return (now_pt() - t).total_seconds() / 86400
    except Exception:
        return 0.0


def parse_due(due):
    """A due is a date (overdue the day after) or a Pacific date and time (overdue after that minute)."""
    due = str(due).strip()
    if len(due) == 10:
        return dt.date.fromisoformat(due)
    return dt.datetime.fromisoformat(due.replace(" ", "T")).replace(tzinfo=PT)


def overdue(m):
    if not m.get("requires_ack"):
        return False
    due = m.get("due")
    if due:
        d = parse_due(due)
        if isinstance(d, dt.datetime):
            return now_pt() > d
        return now_pt().date() > d
    return age_days(m) > 1.0


# A subject that sets a deadline ("one reply by 23:00", "before Friday", "due 10-30"). Exec's 10-22 audit:
# two freeze asks said "by 23:00" only in the subject, with due null, so no check could see them go late.
DEADLINE = re.compile(
    r"\b(by|before|until|due|deadline|no later than)\b[^,;:]{0,12}?"
    r"(\d{1,2}:\d{2}|\d{4}-\d{2}-\d{2}|\d{1,2}-\d{2}\b|today|tonight|tomorrow|eod|noon|"
    r"mon|tue|wed|thu|fri|sat|sun)",
    re.I,
)


def cmd_send(a):
    sender = a.as_role or my_role()
    if not sender:
        print("send: can't infer your role from the branch; pass --as ROLE", file=sys.stderr)
        return 2
    tip = fetch_tip()
    roles = load_roles(tip)
    to, cc = a.to, a.cc or []
    everyone = [sender, *to, *cc]
    bad = [r for r in everyone if r in FORBIDDEN]
    if bad:
        print("send: PM is never addressable (CLAUDE.md 2026-10-03); address exec", file=sys.stderr)
        return 2
    unknown = [r for r in everyone if r not in roles]
    if unknown:
        print(f"send: unknown role(s) {unknown}; see roles.yaml in the mail repo", file=sys.stderr)
        return 2
    outside = [r for r in everyone if not (roles.get(r) or {}).get("pilot")]
    if outside:
        print(
            f"send: {outside} not in the v4 pilot. Use scripts/mail-send.sh (v3) for this message.",
            file=sys.stderr,
        )
        return 2
    if a.type == "canary" and (to != [sender] or cc):
        print("send: a canary goes only to yourself", file=sys.stderr)
        return 2
    due = a.due
    if due and due.lower() == "none":
        due = None
    elif due:
        try:
            parse_due(due)
        except ValueError:
            print(
                "send: --due takes YYYY-MM-DD or 'YYYY-MM-DD HH:MM' (Pacific), or none",
                file=sys.stderr,
            )
            return 2
    elif DEADLINE.search(a.subject):
        print(
            f"send: the subject sets a deadline ('{DEADLINE.search(a.subject).group(0)}') but there is no --due, "
            "so no check can see it go late. Pass --due 'YYYY-MM-DD HH:MM', or --due none if it isn't one.",
            file=sys.stderr,
        )
        return 2
    body = Path(a.body_file).read_text() if a.body_file else sys.stdin.read()
    if not body.strip():
        print("send: empty body", file=sys.stderr)
        return 2
    mid, t = ulid(), now_pt()
    meta = {
        "id": mid,
        "from": sender,
        "to": to,
        "cc": cc,
        "type": a.type,
        # A due date means someone is waiting, so it needs an ack whatever the type (--no-ack still wins).
        "requires_ack": (ACK_DEFAULT.get(a.type, False) or bool(due))
        if a.requires_ack is None
        else a.requires_ack,
        "due": due,
        "in_reply_to": a.in_reply_to,
        "subject": a.subject,
        "sent_at": t.isoformat(timespec="seconds"),
    }
    text = "---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + "---\n\n" + body
    path = f"messages/{t:%Y/%m/%d}/{mid}.md"
    c = commit({path: lambda _old: text}, f"msg({sender}): {a.subject[:72]}")
    print(f"sent {mid} → {', '.join(to + cc)}  ({path}, commit {c[:10]})")
    return 0


def cmd_inbox(a):
    role = a.role or my_role()
    tip = fetch_tip()
    msgs = all_messages(tip)
    mine = [m for m in msgs if role in recipients(m)]
    ack = acks(tip, role)
    open_ = [m for m in mine if m["id"] not in ack]
    if a.ids:
        # Machine form for watchers (Pard's mail-wake): unacknowledged IDs only, one per line.
        print("\n".join(m["id"] for m in sorted(open_, key=lambda m: m["sent_at"])))
        return 0
    rc = 0
    if role == my_role() and not canaried_today(msgs, role):
        # The daily canary used to be a START step that each seat had to remember. Over the pilot it ran on
        # 15 of 41 seat-days (review 2026-10-22), so the first inbox read of the day runs it instead.
        ok, mid = canary(role)
        print(f"canary {mid} for {role} (first inbox read today): {'PASS' if ok else 'FAIL'}")
        rc = 0 if ok else 2
    since = min((m["sent_at"] for m in msgs), default="—")
    print(
        f"mail4 inbox · role={role} · scanned {len(msgs)} messages since {since}; "
        f"{len(mine)} addressed to {role}; {len(open_)} unacknowledged"
    )
    for m in sorted(open_, key=lambda m: m["sent_at"]):
        flag = " OVERDUE" if overdue(m) else (" ack-required" if m.get("requires_ack") else "")
        print(f"  {m['id']}  {m['from']:>5} → {role}  {m['type']}{flag}  {m['subject']}")
        if a.show:
            print("    " + m["_body"].strip().replace("\n", "\n    ") + "\n")
    return rc


def canaried_today(msgs, role):
    today = now_pt().strftime("%Y-%m-%d")
    return any(
        m.get("type") == "canary" and m["from"] == role and m["sent_at"][:10] == today for m in msgs
    )


def last_canary(msgs, role):
    return max(
        (m["sent_at"][:10] for m in msgs if m.get("type") == "canary" and m["from"] == role),
        default=None,
    )


def cmd_read(a):
    tip = fetch_tip()
    for m in all_messages(tip):
        if m["id"] == a.id:
            print(show(tip, m["_path"]))
            return 0
    print(f"read: no message {a.id}", file=sys.stderr)
    return 2


def cmd_ack(a):
    role = a.as_role or my_role()
    tip = fetch_tip()
    m = next((m for m in all_messages(tip) if m["id"] == a.id), None)
    if not m:
        print(f"ack: no message {a.id}", file=sys.stderr)
        return 2
    if role not in recipients(m):
        print(f"ack: {role} is not a recipient of {a.id}", file=sys.stderr)
        return 2
    line = f"{a.id} {now_pt().isoformat(timespec='seconds')} {a.state}"
    if a.note:
        line += " " + a.note.replace("\n", " ")
    c = commit(
        {f"acks/{role}.log": lambda old: (old or "") + line + "\n"},
        f"ack({role}): {a.state} {a.id}",
    )
    print(f"acked {a.id} {a.state} as {role} (commit {c[:10]})")
    return 0


def canary(role):
    body = f"Daily canary from {role}'s checker, {now_pt():%Y-%m-%d %H:%M %Z}. Auto-acknowledged.\n"
    mid, t = ulid(), now_pt()
    meta = {
        "id": mid,
        "from": role,
        "to": [role],
        "cc": [],
        "type": "canary",
        "requires_ack": True,
        "due": None,
        "in_reply_to": None,
        "subject": "canary",
        "sent_at": t.isoformat(timespec="seconds"),
    }
    text = "---\n" + yaml.safe_dump(meta, sort_keys=False) + "---\n\n" + body
    commit({f"messages/{t:%Y/%m/%d}/{mid}.md": lambda _o: text}, f"canary({role})")
    tip = fetch_tip()
    seen = any(m["id"] == mid for m in all_messages(tip) if role in recipients(m))
    seen = seen and mid not in acks(tip, role)
    line = f"{mid} {now_pt().isoformat(timespec='seconds')} done canary\n"
    commit({f"acks/{role}.log": lambda old: (old or "") + line}, f"ack({role}): canary {mid}")
    gone = mid in acks(fetch_tip(), role)
    return seen and gone, mid


def cmd_check(a):
    tip = fetch_tip()
    roles = load_roles(tip)
    pilot = sorted(r for r, v in roles.items() if (v or {}).get("pilot"))
    rc = 0
    if a.canary:
        me = a.as_role or my_role()
        ok, mid = canary(me)
        print(
            f"canary {mid} for {me}: {'PASS' if ok else 'FAIL (not seen in inbox, or ack not applied)'}"
        )
        rc = 0 if ok else 2
        tip = fetch_tip()
    every = all_messages(tip)
    msgs = [m for m in every if m.get("type") != "canary"]
    today = now_pt().strftime("%Y-%m-%d")
    stale = [
        f"{r} {last_canary(every, r) or 'never'} (last ack {last_ack(tip, r) or 'never'})"
        for r in pilot
        if last_canary(every, r) != today
    ]
    late = []
    for r in pilot:
        ack = acks(tip, r)
        late += [(r, m) for m in msgs if r in recipients(m) and m["id"] not in ack and overdue(m)]
    since = min((m["sent_at"] for m in msgs), default="—")
    print(
        f"mail4 check · scanned {len(msgs)} messages (canaries excluded) to {len(pilot)} pilot roles "
        f"({', '.join(pilot)}) since {since}; {len(late)} required-ack overdue"
    )
    if stale:
        print(
            f"  no canary today from: {', '.join(stale)}; a seat's first inbox read of the day runs it, "
            "so a recent ack with no canary means per-message reads, not unread mail"
        )
    for r, m in late:
        print(f"  OVERDUE {r}: {m['id']} from {m['from']} ({age_days(m):.1f}d) {m['subject']}")
    if not msgs:
        print("  (0 messages scanned: nothing measured — exit 3, not an all-clear)")
        return rc or 3
    return rc or (1 if late else 0)


def cmd_stats(a):
    tip = fetch_tip()
    msgs = [m for m in all_messages(tip) if m.get("type") != "canary"]
    commits = git("rev-list", "--count", tip, "--", "messages").stdout.strip()
    ackc = git("rev-list", "--count", tip, "--", "acks").stdout.strip()
    print(
        f"mail4 stats · {len(msgs)} messages (excl. canaries), 1 file per message by construction; "
        f"commits touching messages/: {commits}, acks/: {ackc} (canaries included in commit counts)"
    )
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("send")
    s.add_argument("--to", nargs="+", required=True)
    s.add_argument("--cc", nargs="*")
    s.add_argument("--type", choices=TYPES, required=True)
    s.add_argument("--subject", required=True)
    s.add_argument("--due")
    s.add_argument("--in-reply-to")
    s.add_argument("--body-file")
    s.add_argument("--requires-ack", dest="requires_ack", action="store_true", default=None)
    s.add_argument("--no-ack", dest="requires_ack", action="store_false")
    s.add_argument("--as", dest="as_role")
    i = sub.add_parser("inbox")
    i.add_argument("--role")
    i.add_argument("--show", action="store_true")
    i.add_argument("--ids", action="store_true", help="unacknowledged IDs only (for watchers)")
    r = sub.add_parser("read")
    r.add_argument("id")
    k = sub.add_parser("ack")
    k.add_argument("id")
    k.add_argument("state", nargs="?", default="read", choices=ACK_STATES)
    k.add_argument("--note")
    k.add_argument("--as", dest="as_role")
    c = sub.add_parser("check")
    c.add_argument("--canary", action="store_true")
    c.add_argument("--as", dest="as_role")
    sub.add_parser("stats")
    a = p.parse_args()
    try:
        return {
            "send": cmd_send,
            "inbox": cmd_inbox,
            "read": cmd_read,
            "ack": cmd_ack,
            "check": cmd_check,
            "stats": cmd_stats,
        }[a.cmd](a)
    except Unmeasured as e:
        print(f"mail4: NOT MEASURED — {e}", file=sys.stderr)
        return 3
    except RuntimeError as e:
        print(f"mail4: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
