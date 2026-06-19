---
name: deliver-mail
description: RETIRED 2026-06-19 (post-migration, #1259). The web↔code PM mail-shuttle this skill described no longer exists. SEND mail via push-to-ref (scripts/mail-send.sh — see CLAUDE.md "mailbox workflow"); RECEIVE mail via the check-mailbox skill. Kept only as a redirect — do not use it for mail operations.
scope: cross-role
status: retired
version: 2.0
created: 2026-01-21
retired: 2026-06-19
superseded-by: check-mailbox (receive); CLAUDE.md "The mailbox workflow (most-frequent case)" + scripts/mail-send.sh (send)
---

# deliver-mail — RETIRED

> **This skill is retired. It does not describe how mail works anymore.**
> It is kept as a redirect so old invocations of `/deliver-mail` land somewhere useful instead of a dead end.

## Why it was retired

`deliver-mail` automated the **chat-era web↔code PM-shuttle**: a human PM downloaded memos that "web agents"
(roles running on claude.ai) had written, dropped them in `mailboxes/incoming/`, and this skill routed them
into code-side inboxes (Phase 1 Ingest); then it walked the PM through hand-delivering code-side memos *back*
to web agents (Phase 2 Outbound Audit).

After the **June 2026 migration wave the whole cohort runs on Claude Code.** There are no web agents and no
PM-download shuttle, so Phases 1 and 2 have no referent. The old skill also claimed *"Mailboxes are gitignored:
…Nothing is committed to git"* — that is now **flatly wrong**: mailboxes are git-tracked and every mail op
lands on `origin/main` (see below).

## Where its purpose lives now

The mail lifecycle is fully covered by two current surfaces. Use these directly:

### To RECEIVE / triage your inbox → the `check-mailbox` skill

Check `mailboxes/{your-slug}/inbox/`, read each memo, move it to `read/`, respond where
`Response-Requested: yes`, and note action items in your session log. (The recipient also owns regenerating
their own inbox `MANIFEST.md`.)

### To SEND / route a memo → push-to-ref via `scripts/mail-send.sh`

Canonical procedure: **CLAUDE.md → "The mailbox workflow (most-frequent case) — push-to-ref via `mail-send.sh`"**
(updated 2026-06-19, #1259). In short, from **your own worktree**:

1. Write the memo + any CC copies + your `sent/` mirror, and do any `inbox/ → read/` moves — just
   write/`mv` the files at their `mailboxes/…` paths. **Do not `git add`/`commit` them by hand.**
2. Send, passing **every** changed path explicitly (new files *and* the inbox side of a move):

   ```bash
   scripts/mail-send.sh "mail({role}): {subject}" \
       mailboxes/{recipient}/inbox/{memo}.md \
       "mailboxes/xian (ceo)/inbox/{memo}.md" \
       mailboxes/{you}/sent/{memo}.md
   ```

`mail-send.sh` (v3) builds the commit as a git object on top of `origin/main` (`commit-tree` via a throwaway
index) and pushes it straight to `main`. It **never touches a shared working tree or the local `main` ref**, so
concurrent agents can't sweep or strand each other. On a non-fast-forward it rebuilds on the new tip and retries
automatically. After sending, the files sit uncommitted on your worktree branch and reconcile on your next
sync — that's expected.

The **old bridge dance** (stash → `checkout main` → `git add mailboxes/` → push → switch back) is also retired —
do **not** do it. The `check-branch.sh` PreToolUse hook remains as the backstop for any interactive mail commit
on a non-`main` branch (`commit-tree` isn't `git commit`, so `mail-send.sh` doesn't trip it).

## Reference

- **Send**: `CLAUDE.md` → "The mailbox workflow (most-frequent case) — push-to-ref via `mail-send.sh`"
- **Receive**: the `check-mailbox` skill
- **Full rule set**: `docs/internal/operations/branch-worktree-mailbox-discipline.md`
- **Why push-to-ref**: `docs/internal/operations/mailbox-bridge-transparency-design-2026-06-16.md` (#1259)
- **Routing reference**: `mailboxes/DIRECTORY.md` (canonical slug → role map)

*(This skill may be hard-deleted once the cohort is confident no workflow still invokes `/deliver-mail`.)*
