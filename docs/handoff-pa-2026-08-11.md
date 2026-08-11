# PA cold-start handoff — 2026-08-11 06:23 PT

**Written for the Amber reboot standdown (Pard's notice).** Session should resume via `claude --resume`
with full conversation intact — this document is the belt in case resume fails for this seat specifically.
If you're reading this because resume worked, you don't need it; go straight to `dev/active/
pa-carry-forward.md`, which is the living state file and will be more current than this snapshot.

## Identity and mechanics, if starting cold

- **Role**: Piper Alpha (PA) · **Host**: Amber · **Account**: xian@pipermorgan.ai · **Model**: Opus 5 (1M)
- **Worktree**: `~/Development/piper-morgan-worktrees/pa` — **stable, reused, never fresh** (Model A).
  Never operate from the shared checkout `~/Development/piper-morgan-product`.
- **Branch**: `claude/pa-cycle`
- **Cron**: `42 6,9,12,15,18,21` — session-scoped, dies silently on session loss. **First action: run
  `CronList`.** If empty, re-arm with `CronCreate` before anything else — a cold start after this reboot
  is exactly the kind of event that kills a session-scoped cron.
- **Session log convention**: `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-pa-code-log.md`. Check for `<!--
  DAY-CLOSED: YYYY-MM-DD -->` using the **anchored pattern**, never `grep -c` (see gotcha below).
- **Keychain**: use `/Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python` — any other
  interpreter hangs on a GUI dialog rather than failing.
- **Mail triage**: use `python3 scripts/scan-inbox.py mailboxes/pa/inbox` — not a raw `grep`. Five header
  format variants exist in this corpus; the script handles all of them as of 2026-08-10 (I found and
  fixed variants 4 and 5 myself yesterday, control-tested each).

## The one live thread that matters most right now

**Direct conversation with PM, active as of 2026-08-10**, about the PDR-006 architecture diagram:

- **Shipped revision 1**: corrected a real error in the 08-01 diagram (it wrongly said the web client was
  "largely deleted"/"there is no first screen we own," contradicting PM's own 08-08 correction that no
  surface is being abandoned). Artifact: https://claude.ai/code/artifact/3cfc6edf-6757-415e-8487-955d496548c5
  · source `dev/active/pdr-006-architecture-2026-08-10-rev1.html`.
- **PM is reviewing and will return with notes.** Pace is PM's — do not chase.
- **An open architectural question PM raised as a preview, mine to keep live**: when a user's own LLM
  client already has an independent MCP connector to a service Piper also connects to (e.g. GitHub), does
  it matter which one supplies the data? I gave a real answer (yes — persistence/colleague-model
  composting, the identity/consent boundary, and alias-collision-across-providers all depend on the call
  going through Piper's own server) rather than validating "maybe it doesn't matter." **No existing PDR or
  ADR addresses this** (checked PDR-006 + ADR-070 first). PM hasn't re-confirmed my read yet.

**If this session resumes normally, none of the above needs re-deriving — it's live in conversation
context.** This paragraph exists only for the cold-start case.

## Durable state files, in order of what to read

1. `dev/active/pa-carry-forward.md` — the living PM-attention list and open threads. **Trust this over
   this document** if the two disagree; this snapshot is frozen at reboot time.
2. `dev/active/pa-standing-items.md` — durable owed/queued work.
3. Today's session log (`dev/2026/08/11/...`) — what happened this fire, if anything, before the reboot.

## Standing operational gotchas worth carrying into a cold start

- **Heartbeat**: emit immediately after `date`, before `git fetch`/`merge`, without `--if-quiet` — ordering
  affects the reported dispatch timestamp, and `--if-quiet` suppresses on a timing basis unrelated to
  actual liveness.
- **`grep -c "DAY-CLOSED"` is not a valid close check** — writing *about* the marker (in prose, in a
  correction note) creates a false match. Use the anchored pattern from
  `duty-cycle-freeze-check.sh:99`, or: `grep -qE '^(<!--\s*)?#{0,4}\s*\**\s*DAY-CLOSED\**\s*[:—-]?\s+YYYY-MM-DD'`.
- **After any conflicted merge, before pushing**: `git diff --diff-filter=D --name-only <merge>^2 <merge>`
  — `^2`, not `^1`. Never run `git restore --staged` mid-merge; it resolves to HEAD's version, which is
  deletion for anything new on the incoming side.
- **Source vocabulary is not source verification** — a comment using a strong verb (e.g. "revoke") for a
  weak operation (a local DB delete) will hand you the strong verb; citing the file proves you read it,
  not what it does.

## What was in flight when the standdown notice arrived

Nothing mid-task. 2026-08-10 closed cleanly (verified `DAY-CLOSED`, strict pattern) before this session's
next fire would have opened. This handoff and the standdown steps are the only work this session.

---
*Written 2026-08-11 06:23 PT, in response to Pard's Amber-reboot standdown notice
(`/Users/xian/.local/state/amber-agent/standdown-pa.txt`). Not a routine handoff — see
`dev/active/handoff-pa-2026-07-31.md` for the durable lessons doc, which this does not replace.*
