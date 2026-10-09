# Mail v4 pilot — operations

**Status**: LIVE 2026-10-08 (CIO built it after the weekly quota reset, the named trigger). Pilot roles:
**exec, cio**; **lead joins 2026-10-12**. Runs 2 weeks, review **2026-10-22**. Owner: CIO (mechanism),
Exec (audit and rollup). Design: `dev/2026/10/03/spec-eval/proposal-mail-v4-fan-out-on-read.md` (Spec;
PM approved 2026-10-03).

## What changes for a pilot role

| v3 (everyone else) | v4 (pilot roles, messages among pilot roles only) |
|---|---|
| `scripts/mail-send.sh` writes a copy per recipient + cc + sent mirror, pushed to this public repo | `scripts/mail4.py send` writes **one file** in the private repo `mediajunkie/piper-morgan-mail` |
| Read = `ls mailboxes/<role>/inbox/`, then move each to `read/` | Read = `scripts/mail4.py inbox` (a query over messages + your acks) |
| "Read" = a file move nobody can audit | Ack = `scripts/mail4.py ack <id> [read\|done\|declined]`, append-only, one writer per file |
| Misaddressed mail sits unread | Unknown role, PM, or a non-pilot recipient: the send **fails** |

**Nothing is written to both systems.** A message with any non-pilot participant goes through v3, and
`mail4.py send` refuses it with a pointer to `mail-send.sh`. So during the pilot a pilot role reads
**both** inboxes: v3 for everyone else, v4 for pilot peers.

## Setup (once per seat)

```bash
git clone git@github.com:mediajunkie/piper-morgan-mail.git ~/Development/piper-morgan-mail
```
The clone's working tree is never used; `mail4.py` reads and writes git objects against `origin/main`.
`PIPER_MAIL4_REPO` overrides the path.

## Daily use

```bash
scripts/mail4.py inbox [--show]                    # every wake, alongside the v3 inbox check
scripts/mail4.py read <ID>
scripts/mail4.py ack <ID> done --note "what I did"  # read | done | declined
scripts/mail4.py send --to exec --type task --subject "..." --body-file memo.md   # or body on stdin
scripts/mail4.py check --canary                    # once a day, at START
scripts/mail4.py stats                             # pilot instrumentation
```
Types: `fyi`, `task`, `decision-request`, `ruling-relay`, `reply` (`task` and `decision-request` require an
ack by default; `--due YYYY-MM-DD` sets the overdue date, otherwise overdue is after 1 day).
Your role comes from your branch (`claude/<role>-cycle`); `--as ROLE` overrides.

## Guarantees and how they were tested (2026-10-08, CIO seat)

| Guard | Test |
|---|---|
| Unknown role, PM, non-pilot recipient refused | `--to nobody`, `--to xian`, `--to lead`: each exit 2 with the reason |
| No bare all-clear | `check` on an empty repo: "0 messages scanned: nothing measured", exit 3 |
| Reader works (canary) | `check --canary`: sends to self, sees it in the inbox query, acks it, sees it leave: PASS |
| Concurrent writers can't collide | two simultaneous sends: both landed (the second rebuilt on the new tip) |
| Only recipients can ack | `ack <id> --as exec` on a cio-only message: exit 2 |

## Known limits (pilot)

- **No mail wake yet.** The automatic MAIL WAKE watches this repo's `mailboxes/`, not the private repo, so a
  v4 message is seen at the recipient's next scheduled wake. Asked Pard (owner of the watcher) to add it.
- No per-message search beyond `inbox` and `read`. `check` scans every message; fine at pilot volume.

## Success and stop criteria (from the proposal)

Success: zero missed required-ack messages in Exec's 20-message audit; all 14 daily canaries pass; ≥60%
fewer files per message than v3 (v4 is 1 by construction, v3 is about 3–5); inbox read cost no higher than v3;
no confusion reported. **Stop at once** if a decision request goes overdue without `check` flagging it, or
on any false all-clear. Rollback: the pilot roles go back to `mail-send.sh`; v4 messages stay readable as
plain markdown.
