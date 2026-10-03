---
type: proposal
title: "Mail v4: one copy per message, read-side delivery, and acknowledgements nothing can silently skip (pilot proposal)"
author: spec, at PM's request (2026-10-03)
status: PROPOSAL. Not built. For PM review, then Exec + CIO to cost out.
relates: evaluation report R3, R4, R5 (docs/internal/audits/2026-10-spec-project-evaluation.md)
---

# Mail v4: proposal and pilot

## The problem in one paragraph

Today every memo is **fanned out at write time**. The sender writes one copy per recipient, plus a cc copy, a
sent mirror and MANIFEST updates, then pushes a commit that every agent's worktree has to merge. The result is
21,312 mailbox files (59% of the public repo), about 1,750 mail commits a month (September, D0), cc copies that no one reads
(94% of PM-addressed memos), and a delivery model whose correctness depends on every sender choosing the right
paths. The failures PM has seen follow from that:
- A memo was routed to a mailbox that didn't exist and sat unread for 5 days.
- Checker scripts reported "clear" over the wrong denominator.

The problem is copying at write time, and adding more copies doesn't fix it. **SMTP isn't the answer either**:
it adds infrastructure and still copies on write.

## The design

Write each message once and fan it out at read time. Delivery has to be **provable**, so a missed message shows
up as an error, never as an all-clear.

### 1. One file per message
- Path: `messages/YYYY/MM/DD/<id>.md`, where `id` is a sortable unique id (ULID).
- Front-matter:
  ```yaml
  id: 01JA...            # unique, time-sortable
  from: cio
  to: [exec, lead]       # validated against roles.yaml at send; unknown role = hard fail
  cc: []                 # 'xian' allowed only if type is decision-request or ruling-relay
  type: fyi | task | decision-request | ruling-relay | reply
  requires_ack: true     # default true for task and decision-request
  due: 2026-10-06        # optional
  in_reply_to: 01J9...   # optional, for threads
  subject: "..."
  ```
- No per-recipient copies, no sent mirror (`from` already records the sender), no MANIFEST.

### 2. Reading is a query, not a folder
- `mail-inbox <role>` lists every message where the role is in `to` or `cc` and the role hasn't acknowledged it.
- It is computed **from the message files and ack files every time**. There is no separate derived index that
  can drift.
- Scan cost: about 2,000 messages per 8 weeks. The query only scans months after the role's oldest open item,
  so it stays cheap.

### 3. Acknowledgements: one writer per file
- `acks/<role>.log` is append-only, with lines of the form `<id> <timestamp> read|done|declined [note]`.
- Each role writes **only its own** ack file. Two agents can never collide on the same file. This is the property
  MANIFESTs only approximated.

### 4. Guarantees against missed messages (PM's concern)
| Failure seen before | Guard in v4 |
|---|---|
| Memo sent to a mailbox that doesn't exist (5 days unread) | `to`/`cc` are checked against a machine-readable `roles.yaml` at send. An unknown role makes the send fail. |
| Checker reports "clear" over the wrong denominator | The checker **always prints its denominator**: "scanned N messages, to M roles, since <date>; K unacknowledged past due". If N is 0 or the scan errors, it exits non-zero. It never prints a bare all-clear. |
| The reader itself is broken, so nothing shows as unread | **Canary.** Once a day the checker sends a `requires_ack` message to itself and confirms it appears in its own inbox query, then acknowledges it. A missing canary is an alarm. |
| A decision request is buried among cc's | PM is addressable only by `decision-request` / `ruling-relay`, enforced at send. Unacknowledged decision requests surface in Exec's rollup with their age. |
| A sender stages the wrong paths | Sending takes **no paths**, only front-matter. The script writes the one file, so there's nothing for the sender to get wrong. |

### 5. Where the messages live ("private storage")

**What "private storage" means here:** a separate **private GitHub repository** (working name
`mediajunkie/piper-morgan-mail`). Only PM and the cohort's credentials can read it. Mail moves there; the
product repo stays public. Nothing about the medium changes: it is still git, markdown files and commits, so it
stays durable, auditable and readable by agents.
- Each Amber seat keeps one clone at a fixed path, for example `~/Development/piper-morgan-mail`.
- The mail scripts use that clone. `mail-send.sh` **already supports this** through its `PIPER_REPO` and
  `PIPER_MAIL_REMOTE` overrides (lines 27–28, 50, 105), so the send mechanism needs no rewrite.
- Effects:
  - It removes third-party names and emails from the public repo going forward (report R5).
  - Product-repo worktrees stop merging mail commits.
  - Mail history becomes its own clean log.
- What it doesn't do: it doesn't erase what is already in the public repo's history. Rewriting that history is a
  separate decision for PM to make.

Alternatives considered:
- **GitHub Issues or Discussions in a private repo.** Real notifications and query APIs, but subject to rate
  limits, less readable offline, and a bigger change in habits. This is the fallback if git scanning doesn't scale.
- **A table in Amber's Postgres.** Fastest to query, but not auditable through git, and it ties mail to a single
  host. Worth revisiting only at 10× today's volume.
- **SMTP.** Rejected. It adds infrastructure and still copies at write time.

## Pilot (2 weeks, reversible)

- **Scope:** three roles, Exec, CIO and Lead (one of the highest-volume senders). **Only messages among those three**
  go through v4. Everything else stays on v3. Nothing is written to both systems, so no one has to wonder which
  copy is the real one.
- **Build:** about 1–2 days of work.
  - `mail-send` v4, a front-matter-only mode built on the existing commit-tree code
  - `mail-inbox`, `mail-ack`, `roles.yaml`
  - the checker with denominator and canary
  - one private repo
- **Instrumentation:**
  - files and commits per message (the v3 baseline is about 3–5 files: one per recipient and cc, plus the sent mirror, plus MANIFEST updates)
  - tokens spent reading the inbox at session start
  - time to acknowledge
  - checker output kept daily
- **Audit:** Exec samples 20 pilot messages (stated denominator) and confirms each recipient acknowledged or acted.
  CIO separately confirms that all 14 canaries passed.
- **Success:**
  - **zero missed required-ack messages** in the audit
  - all canaries pass
  - ≥60% fewer files written per message
  - inbox read cost no higher than v3
  - no confusion reported by the three roles
- **Stop the pilot immediately if:**
  - any decision request goes unacknowledged past due without the checker flagging it
  - any false all-clear (checker clear while the audit finds a miss)
- **Rollback:** the three roles switch back to v3 scripts. v4 messages stay readable as plain markdown.
- **Owners:** CIO (mechanism), Exec (audit and rollup). **PM's part:** approve the pilot and create the private
  repo (or authorize CIO to create it).

## After the pilot
If it succeeds:
- Migrate the remaining roles in two batches.
- Archive `mailboxes/` from the public repo (history-rewrite decision separate, as above).
- Retire MANIFEST regeneration and the merge churn it causes.
- Fold the checker into the existing watchdog, so watcher count goes down, not up.
