---
name: duty-cycle-tick
description: Execute one autonomous duty-cycle fire (START / WATCH / WORK / STOP) for a cycling agent. Invoked by the thin cron prompt on each fire. Use when a "DUTY CYCLE TICK" prompt fires, or to run a cycle fire manually. Holds the durable procedure so the cron prompt stays one-line.
scope: cross-role
version: 1.4
created: 2026-06-06
changelog: v1.4 (2026-06-09) — START Step-0 self-heal: verify the prior day STOPped (grep the `<!-- DAY-CLOSED: {date} -->` marker) + run its missed close if not (PM-ratified, Comms-surfaced — fixes the day-ends-without-STOP → session-log-never-closes gap); STOP now emits the canonical DAY-CLOSED marker. v1.3 (2026-06-07) — Step-1 Gap-C self-heal: re-arm if CronList shows zero crons (compaction can silently kill a session cron; durable=noop). Partial mitigation (heals on next turn); Routines watchdog is the cure. v1.2 (2026-06-07) — Step-3 overnight-window guard: state+hour hybrid so the continuous shape's ~2am WATCH doesn't mis-START (caught by CIO dogfood overnight 6/6→7); overnight branch checked first + hour-gated. v1.1 (2026-06-06) — Step-3 routes by STATE not clock-hour (HOST finding) for low-freq/Web shapes; Rule-2 keep-armed-default (PM). v1.0 — initial (CIO, gbrain thin-job-prompt adoption).
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

### Step 1 — Date + cron state (+ Gap-C self-heal)
Run `date "+%H:%M %Z (%A %Y-%m-%d)"` and `CronList`. Confirm exactly ONE cron job for your expression:
- **Duplicates** → CronDelete extras (CronList→CronDelete-old→CronCreate-new is the rotation).
- **ZERO crons for your expression** → **re-arm immediately** (`CronCreate` your expression) before doing anything else, and note it in the fire entry. This is the **Gap-C self-heal**: a compaction can silently kill a session-scoped cron (`durable:true` is a no-op here — PA verified 2026-06-07). *Caveat (honest scope): this only fires if the session got a turn at all — a fully-dead cron has no trigger, so this heals on the next turn the session happens to get (a human prompt, or a surviving fire), reducing the dead-window but not curing it. The cure is the external Routines watchdog (roadmap item 1); see `procedures/cron-lifecycle.md` Gap C.*

### Step 2 — Sync (Model A worktree)
```
git fetch origin main -q && git checkout -- mailboxes/*/inbox/MANIFEST.md mailboxes/*/read/MANIFEST.md 2>/dev/null
git merge origin/main --no-edit -q
```
Discard mailbox MANIFEST regen-noise. (Variant launch models — e.g. Web main-direct — skip the worktree dance per their registry row; see `cron-shape-experiments.md`.)

### Step 3 — Read carry-forward, then dispatch by STATE (shape-independent — HOST finding 2026-06-06)
Read the cycle-log tail + `{role}-carry-forward.md` so you know where you left off. Then dispatch by a **state + window hybrid** — *state* (session-log-today existence) gates START-vs-WORK; *hour* gates overnight-WATCH-vs-morning-START. (This is the v1.2 refinement: pure-state was *almost* right, but the continuous shape's ~2am WATCH fire also has no-session-log-today yet, so a bare "no-log→START" rule mis-STARTs it overnight. The overnight-window guard fixes that while keeping HOST's low-freq fix intact.) **Check the overnight branch FIRST:**

- **Overnight window (local hour ~0–4, pre-morning) + nothing urgent** → **quiet-hold / WATCH** — *regardless of whether a session-log-today exists yet*. No START, no CronDelete, leave armed. For the continuous shape the single ~2am fire is the **WATCH** (quick `ls mailboxes/{role}/inbox/`; **commit a one-line WATCH entry**; see `procedures/watch.md`); low-freq shapes' overnight fires are plain quiet-holds. *(This branch first — and hour-gated — so the 2am fire doesn't fall into the START rule below.)*
- **No session log exists for today AND past the overnight window (local hour ≥ ~4)** → **START**: **Step 0 FIRST — verify the prior day STOPped properly, and run the missed STOP tasks if not** (PM-ratified 2026-06-09, Comms-surfaced): `grep -l "DAY-CLOSED" dev/2026/<prior-day-path>/*{role}*log.md` — if the prior day's session log lacks the **`<!-- DAY-CLOSED: {date} -->`** marker, that day ended without a STOP (PM takeover, cron reshape, session-death, or engaged-past-STOP-window). **Run its missed close NOW before today's START**: reconstruct the prior day's wrap from its cycle log + commits — day-arc + the memory-eval 3-bucket + the sign-off checklist + the `DAY-CLOSED` marker. This is *self-healing* — it doesn't wait for Docs's merge-keeper sweep to catch it the next morning (that's the reactive net; this is the proactive source-catch). *Then* proceed: create today's session log (`create-session-log` skill) + fresh cycle log; mail-loop. **Commit a one-line START entry** (audit-visibility). *(Gating START on "no-session-log-today" — not a fixed "~04" — keeps HOST's fix: a low-freq agent whose first fire is ~06:37 still STARTs correctly. The `≥~4` guard only excludes the overnight-WATCH window, not the whole morning.)*
- **Session log exists + past ~11pm + PM idle + not yet STOPped today** → **STOP**: day-close; **LEAVE CRON ARMED** (re-CronCreate same expr as the final action — STOP is a day-close ritual, NOT a cron-teardown). **Wrap BOTH logs, not just the cycle log**: (a) cycle log gets the day-close entry; (b) **the session log gets its own wrap** — the memory-eval 3-bucket section (#974) *filled* + the sign-off checklist (`git status` clean / `@{u}..HEAD` empty / `main..HEAD` empty). *A cycle-log day-close ≠ a session-log sign-off* (Docs-flagged 2026-06-08: a retroactive close wrote the cycle log but left the session log's memory-eval as "(fill at wrap)" + no sign-off). **If the session spanned a day boundary without a STOP** (ran continuously / compacted overnight), the retroactive close MUST still wrap the *prior day's* session log (memory-eval + sign-off), not only its cycle log. **Emit the canonical close-out marker**: the session-log sign-off section MUST include a literal **`<!-- DAY-CLOSED: {YYYY-MM-DD} -->`** line — the grep-able sentinel that START's Step-0 self-heal (and the Lead-owned session-start hook) check for to detect "did a proper STOP happen?" (PM-ratified 2026-06-09; standardizes the close-out detection — prior close-outs varied: "DAY-CLOSE", "## STOP", prose).
- **else (session log exists, daytime, work to do)** → **WORK PARTS**: Mail Loop (drain inbox → read/ with disposition) → Task Loop (advance owed work; at (0,0) advance smallest-scope unblocked low-pri from standing-items, else quiet hold) → loop to (0,0).

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
- **Cron**: if this fire went substantive (>2min), you should have CronDelete'd FIRST (Rule 1); CronCreate the SAME expression back when returning to IDLE (incl. end of STOP). **Rule 2 (keep-armed-default, PM-ratified 2026-06-06)**: leave the cron ARMED during PM conversation (idle-suppression + presence-aware hold); a **pending PM question does NOT delete the cron and does NOT block other work** — keep advancing any other unblocked work, only hold the specific thread that needs PM's answer. The only positive CronDelete is Rule 1. A trivial one-line log fire needs no CronDelete. (This supersedes the old CronDelete-when-question-pending refinement, which caused silent-walk-away to miss overnight self-wake.)
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
- [ ] Cron in the correct state for what comes next (armed by default — incl. through PM conversation + overnight; deleted ONLY for Rule-1 substantive multi-step work, re-armed at IDLE)

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
