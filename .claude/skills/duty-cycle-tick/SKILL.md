---
name: duty-cycle-tick
description: Execute one autonomous duty-cycle fire (START / WATCH / WORK / STOP) for a cycling agent. Invoked by the thin cron prompt on each fire. Use when a "DUTY CYCLE TICK" prompt fires, or to run a cycle fire manually. Holds the durable procedure so the cron prompt stays one-line.
scope: cross-role
version: 1.0
created: 2026-06-06
---

# duty-cycle-tick

Execute one autonomous duty-cycle fire. This skill holds the **durable procedure** so the cron prompt can stay thin (role + worktree + cron-expr + "run this skill"). The genuinely-transient carry-forward lives in files this skill **reads at fire-time** — never frozen into the prompt.

## When to Use

- A `DUTY CYCLE TICK` cron prompt fires (the normal trigger).
- You want to run a cycle fire by hand (`/duty-cycle-tick`).
- After compaction, to re-establish the fire procedure without a fat prompt.

## What the thin cron prompt provides (the only per-agent constants)

The invoking prompt carries ONLY the irreducible per-agent constants:
- **ROLE** (e.g. CIO) + **role-slug** (e.g. cio)
- **WORKTREE** path (where the session launched; cwd anchors here — Model A)
- **CRON expression** (e.g. `7 2,4-23 * * *`) + offset
- **Launch model** (Model A worktree-cycle, or a registered variant — e.g. Web main-direct)

Everything else — what's owed, what's active, what's parked — this skill **reads** from the state files below. If you find yourself wanting to put state in the prompt, that's the smell this skill exists to kill (see Anti-Patterns).

## State files (read at fire-time; never frozen in the prompt)

| File | Holds | When |
|---|---|---|
| `dev/active/cycle-log-{role}-{today}.md` (tail) | the running per-fire record + most recent carry-forward | read every fire |
| `dev/active/{role}-carry-forward.md` | the ephemeral session state (active PM threads, parked items, current cron job-id) | read at START / every fire; **rewrite at end of every substantive fire** |
| `dev/active/{role}-standing-items.md` | durable owed/queued/blocked items (the Task List) | read in the Task Loop |
| `dev/active/duty-cycle-escalations-{role}.md` | what needs PM (attention surface) | update when something needs PM |

## Procedure

### Step 1 — Date + cron state
Run `date "+%H:%M %Z (%A %Y-%m-%d)"` and `CronList`. Confirm exactly ONE cron job for your expression (if duplicates: CronDelete extras — CronList→CronDelete-old→CronCreate-new is the rotation).

### Step 2 — Sync (Model A worktree)
```
git fetch origin main -q && git checkout -- mailboxes/*/inbox/MANIFEST.md mailboxes/*/read/MANIFEST.md 2>/dev/null
git merge origin/main --no-edit -q
```
Discard mailbox MANIFEST regen-noise. (Variant launch models — e.g. Web main-direct — skip the worktree dance per their registry row; see `cron-shape-experiments.md`.)

### Step 3 — Read carry-forward, then dispatch by local hour
Read the cycle-log tail + `{role}-carry-forward.md` so you know where you left off. Then route by hour:

- **~04 (new day)** → **START**: create today's session log (`create-session-log` skill) + fresh cycle log; mail-loop; IDLE. **Commit a one-line START entry** (audit-visibility).
- **~02 (post-STOP, pre-START)** → **WATCH**: quick `ls mailboxes/{role}/inbox/` only; nothing urgent → **commit a one-line WATCH entry**, leave cron armed, do NOT START. (See `procedures/watch.md`.)
- **~23 (past 11pm, PM idle)** → **STOP**: day-close (append close-out to session + cycle log); **LEAVE CRON ARMED** (re-CronCreate same expr as the final action — STOP is a day-close ritual, NOT a cron-teardown).
- **else 05–22** → **WORK PARTS**: Mail Loop (drain inbox → read/ with disposition) → Task Loop (advance owed work; at (0,0) advance smallest-scope unblocked low-pri from standing-items, else quiet hold) → loop to (0,0).

### Step 4 — Execute the dispatched part
Hold the discipline: holistic-not-tactical. Quiet hold beats manufactured busywork. Batch identical daytime no-op holds (don't commit a near-duplicate entry each fire) — but **WATCH and START always commit a one-line entry**.

### Step 5 — Log the fire
Append a fire entry to the cycle log (event-based: the log update rides with the work commit). If substantive work happened, the entry rides with that commit.

### Step 6 — Commit + push (verify it lands)
- **Non-mail** (logs, docs, design): commit on your cycle branch → `git push origin claude/{role}-cycle:main` (NEVER `git checkout main` in this worktree).
- **Mailbox writes**: via the MAIN-WORKTREE BRIDGE — `cd` to the main worktree → pull → write → commit **explicit paths only** → push → return. `check-branch.sh` hard-blocks mailbox commits on branches.
- **EXPLICIT-PATHS-ONLY** on every `git add`. Never `git add -A` / `git add .` / directory adds. **NEVER** unconditional `git stash pop`.
- **VERIFY the push landed on origin/main** — main is busy; fast-forward races happen. `git fetch origin main && git branch -r --contains HEAD | grep origin/main`; if rejected, `git merge origin/main` + re-push.

### Step 7 — Update carry-forward + manage cron, then brief status
- **Rewrite `{role}-carry-forward.md`** with current ephemeral state (this is what replaces the frozen prompt block).
- **Cron**: if this fire went substantive (>2min), you should have CronDelete'd FIRST (Rule 1); CronCreate the SAME expression back when returning to IDLE (incl. end of STOP). Model A: leave cron running during PM conversation (idle-suppression), BUT CronDelete-as-positive-action when a PM question is actively pending (Rule 2). A trivial one-line log fire needs no CronDelete.
- Give the user a brief status line.

## Anti-Patterns to Avoid

| Don't Do This | Why | Do This Instead |
|---|---|---|
| Freeze carry-forward state into the cron prompt | You hand-refresh it every re-arm (vigilance); copies drift across agents | Write it to `{role}-carry-forward.md`; the skill reads it (mechanism — m-36) |
| Put the procedure in the prompt | N agents carry N divergent copies | One versioned skill; the prompt invokes it |
| `git add -A` / directory adds | Sweeps other agents' working-tree state | Explicit paths only, every time |
| Commit a near-identical no-op hold every fire | Log churn | Batch daytime quiet-holds; only WATCH/START always commit |
| STOP by CronDelete-and-leave-deleted | No morning self-wake (Gap A) | STOP leaves the cron ARMED (re-CronCreate same expr) |
| Assume the push landed | main is busy; fast-forward races | Verify on origin/main; merge + re-push if rejected |

## Quality Checklist

After each fire:
- [ ] Exactly one cron job for your expression (no duplicates)
- [ ] Fire entry appended to the cycle log
- [ ] Work verified on origin/main (not just pushed to branch)
- [ ] `{role}-carry-forward.md` reflects current state (if substantive)
- [ ] WATCH/START committed a one-line entry (if applicable)
- [ ] Cron in the correct state for what comes next (armed for overnight; deleted if PM-question-pending)

## Examples

### Example 1: Quiet WORK fire (inbox zero, queue clear)
Date 14:07 → WORK PARTS. Sync clean, inbox zero, standing-items has no unblocked low-pri. → Quiet hold (batch if identical to last). No CronDelete (trivial). Brief status. Done.

### Example 2: Substantive WORK fire (mail to act on)
Date 10:09 → WORK PARTS. Inbox has a memo needing a reply. → CronDelete FIRST (Rule 1). Draft reply via main bridge (explicit paths), triage source → read/, log the fire, push + verify, rewrite carry-forward, CronCreate same expr back. Brief status.

### Example 3: STOP (day-close)
Date 23:37, PM idle → STOP. Final mail-check, append day-close to session + cycle log, commit + push + verify, rewrite carry-forward for tomorrow, **re-CronCreate same expr (leave armed)** as the final action. Brief status.

## Cross-references
- `docs/operations/duty-cycle design/procedures/cron-lifecycle.md` — Rule 0/1/2 + v0.6.3 in full
- `docs/operations/duty-cycle design/procedures/watch.md` / `stop.md` / `start.md` — the day-parts
- `docs/operations/duty-cycle design/canonical-cron-prompt-template-v0.7.md` — the (now thin) cron prompt
- `docs/operations/duty-cycle design/cron-shape-experiments.md` — per-lane cron-shape variants
- `.claude/skills/create-session-log/SKILL.md` — invoked by START on a new day
