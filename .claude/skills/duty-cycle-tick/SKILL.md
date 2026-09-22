---
name: duty-cycle-tick
description: Execute one autonomous duty-cycle fire (START / WATCH / WORK / STOP) for a cycling agent. Invoked by the thin cron prompt on each fire. Use when a "DUTY CYCLE TICK" prompt fires, or to run a cycle fire manually. Holds the durable procedure so the cron prompt stays one-line.
scope: cross-role
version: 1.38
created: 2026-06-06
changelog: "Full history: docs/internal/operations/duty-cycle-tick-changelog.log (v1.0-present). Most recent: v1.38 (2026-09-22) — **Mail/task loop exit condition tightened to PM's exact two-consecutive-empty-rounds requirement, closing a real gap PM found by formalizing the flywheel as a 16-state table.** PM's rule: exit to idle ONLY on two consecutive (0 mail, 0 tasks) rounds; every other pattern -- including new mail/tasks in the round BEFORE the current one, even if the current round is itself clean -- continues the loop. Fix: Step 5 now explicitly defines a "round" (one full 1-2-2b-3 pass), requires tracking empty-vs-non-empty per round, and exits only when the just-finished round AND the one before it were both empty."
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
- **WORKTREE** path (where the session launched; cwd anchors here. **Model A** = stable per-agent worktree, reused every session, on Amber; **Model B** = Desktop's ephemeral per-session auto-worktree. Host-dependent since 2026-07-25)
- **CRON expression** (e.g. `7 2,4-23 * * *`) + offset
- **Launch model** (Model A stable worktree on Amber, Model B ephemeral on Desktop, or a registered variant — e.g. Web main-direct)

Everything else — what's owed, what's active, what's parked — this skill **reads** from the state files below. If you find yourself wanting to put state in the prompt, that's the smell this skill exists to kill (see Anti-Patterns).

## State files (read at fire-time; never frozen in the prompt)

| File | Holds | When |
|---|---|---|
| `dev/2026/MM/DD/{date}-{role}-code-opus-log.md` (the **session log**) | **THE log — the single canonical record** (PM 2026-06-12: "do the logging in one place"); durable institutional memory, what Docs reads for the omnibus; permanent (dated dir) | created at START; **the per-fire entry is written here** (Step 5); wrapped at STOP |
| `dev/active/cycle-log-{role}-{today}.md` (tail) | **OPTIONAL private scratch** — a per-fire scratch list an agent may keep if useful; **NOT a logging surface, NOT a parallel record** (PM 2026-06-12, supersedes v1.5 dual-surface). `dev/active/` is sprint-cleaned — nothing durable lives only here | optional; read at START for continuity if you keep one |
| `dev/active/{role}-carry-forward.md` | the ephemeral session state (active PM threads, **PM-attention / escalation items** — the residual home since the 6/17 escalations-doc FOLD, parked items, current cron job-id) | read at START / every fire; **rewrite at end of every substantive fire** |
| `dev/active/{role}-standing-items.md` | durable owed/queued/blocked items (the Task List) | read in the Task Loop |
| ~~`dev/active/duty-cycle-escalations-{role}.md`~~ | **DEPRECATED 2026-06-17 (FOLD, PM-ratified)** — PM-attention items now ride the carry-forward (above); the cohort-attention rollup GitHub-verifies every item + the freeze-registry handles liveness, so this hand-maintained surface was retired | no longer maintained |
| `dev/state/{role}-last-pm-scan` | v1.36 — durable machine-state marker for step 1c's scan window (NOT sprint-cleaned, unlike everything else in this table under `dev/active/`) | written by `--record`, read by `--since-last-scan` |

## Procedure

**A fire is idempotent by design** (gbrain-adoption, HOST+CIO co-signed 2026-06-16 — the one concrete action item from that synthesis, executed here 2026-07-06 after sitting unactioned for three weeks): running this procedure twice against the same state must produce the same safe result as running it once. This isn't incidental — it's why the mail loop is drain-to-empty (a re-run finds nothing left, not a duplicate action), why cadence changes are logged explicitly rather than inferred (Section further down), and why Belt-4 spawn-fresh is safe to trigger on a stale-looking session (worst case: two fires converge on the same already-drained state, neither does anything harmful). If you're ever adding a new step to this procedure, ask whether running it twice in a row would double-do something — if yes, that step needs a check-before-act guard, not just a comment.

### THE SPINE — the flywheel is the unit of work, not "the fire"

The flywheel runs **continuously and cron-independently**:

> **check mail → do carried work → check your criteria line's GitHub issues → check mail → … →
> DRAINED (all three sources empty) → idle**

**The work queue has three sources, not one** (PM's ruling, v1.33, 2026-09-11 — supersedes the
two-source mail-plus-tasks framing this spine used to state): carried work (your standing-items
tracker), incoming mail, and newly-observed GitHub issues meeting your own role's criteria (Step
3.2b below). PM, verbatim: *"I think the issue is perhaps in being overly literal about the inbox
as the only work queue... An agent should really only go idle when there is nothing to work on at
all."* Treating the inbox as the sole queue is exactly the failure this ruling closes — a role can
correctly report "mail: empty, standing-items: empty" and still not be drained if its own
GitHub-criteria source has eligible work sitting unchecked.

**The numbered Steps below are NOT a work-session and NOT a container** — they are only **how a WAKE re-enters this flywheel** (catch up on state, then drain). A wake joins the ongoing loop, drains everything ready, and returns to idle. The cron is a **wake-timer for when you're idle**, never a work-chunker.

Why this is the spine — and why "save it for the next fire" is *structurally impossible*, not merely discouraged:
- **There is no per-fire bucket to save work into.** The flywheel is one loop; "the fire" is just the moment you re-entered it. Deferring unblocked work "to the next fire" doesn't move it into a container — it leaves it undone in the *same* loop, which the next wake re-enters with the work *still there*. "Next fire" resolves to "later in the same loop, for no reason" — a **disguised stop**.
- **A wake does not end while unblocked work remains.** Commit at each work-unit boundary (git hygiene + interruption protection), but a commit is **NOT a stop** — keep draining. A wake ends only at **(0,0)**: queue empty, or every remaining item PM-gated.
- **The one legitimate pause** is quality-banking genuinely-deep work against an **explicit, real trigger** — a *fresh session* or a *context compaction* (an actual capacity limit), named out loud and owned. Never "no rush," "not urgent," or "next fire."

The Steps exist to make a *wake* correct (don't drop state across the idle gap) — they do not chunk the work.

> **The boundary — what the spine's "drain it all" does NOT mean** (PM ruled both ways 6/15 — get this right): drain work that's *ready* — but **deep / render-sensitive / quality-critical work that genuinely warrants a fresh focused pass is quality-banking, not bite-sizing**, and may be deferred to its own wake. The discriminator is **WHY** you're deferring: *to pace the cron tick / because a "fire" conceptually ended* = the antipattern; *because a complex build deserves fresh focus rather than tail-of-marathon work* = legitimate (PM endorsed exactly this for Lead Dev). When unsure, drain it — the antipattern is the common failure, quality-banking the rare exception.
>
> **The exception needs an EXPLICIT, REAL trigger (PM 2026-06-16).** Quality-banking is legitimate ONLY when you name a concrete trigger *out loud* — **a fresh session** or **a context compaction** (a real capacity limit), not a vague "this deserves focus." *"No rush" / "not urgent" / "I'll get to it" with no named trigger is the antipattern in a quality costume.* PM: *"there is no advantage to saving work… shyness should not be a thing."* Two valid states: **(1) do it now**, or **(2) "deferring to a fresh session/compaction because [the explicit reason]"** — said explicitly, owned, not implied. And **don't tell other agents "no rush"** — it plants an imaginary trigger in them too.

### Step 1 — Date + cron state (+ Gap-C self-heal)
Run `date "+%H:%M %Z (%A %Y-%m-%d)"` and `CronList`. Confirm exactly ONE cron job for your expression:
- **Duplicates** → CronDelete extras (CronList→CronDelete-old→CronCreate-new is the rotation).
- **ZERO crons for your expression** → **re-arm immediately** (`CronCreate` your expression) before doing anything else, and note it in the fire entry. This is the **Gap-C self-heal**: a compaction can silently kill a session-scoped cron (`durable:true` is a no-op here — PA verified 2026-06-07). *Caveat (honest scope): this only fires if the session got a turn at all — a fully-dead cron has no trigger, so this heals on the next turn the session happens to get (a human prompt, or a surviving fire), reducing the dead-window but not curing it. The cure is the external Routines watchdog (roadmap item 1); see `procedures/cron-lifecycle.md` Gap C.*
- **Nearing its 7-day auto-expiry** → **re-arm proactively, before it dies, not after.** *(Lead's proposal, 2026-08-15, from Agent 360 10.3/10.5 — routed to CIO as the skill's owner rather than edited unilaterally.)* `CronList` doesn't return a job's creation timestamp, so this depends on the arm-date you already record when you create a job (carry-forward / your registry state-column note — several rows already carry "expires ~date" by hand; this just makes checking it a named step instead of an incidental habit). If today is within ~48h of that recorded expiry, **re-arm now** using the same rotation as everywhere else in this skill (`CronList` → `CronDelete` the still-live job → `CronCreate` fresh → `CronList` to confirm exactly one survives) rather than waiting to discover absence after the fact — the fleet's exact "comes back looking healthy and never fires again" shape, otherwise caught only by the freeze-watchdog's slower path. If you don't have a recorded arm-date to check against, that absence is itself worth fixing (record one now) rather than a reason to skip the check.

  ⭐ **TIGHTEST EVIDENCE TO DATE — PPM, 2026-08-06** (routed to CIO per PM's standing cron-mechanics routing). Most Gap-C reports arrive as *"the cron went away sometime."* This one brackets it: job `c079437c` re-armed at **2026-08-05 22:22** and `CronList`-verified **exactly one**; fired normally at **07:52** and **09:52**; **a context compaction occurred**; `CronList` at **10:27** returned **"No scheduled jobs."** No `CronDelete` was run, and the 7-day expiry was not in play (created 08-05). **A verified-present and a verified-absent reading, same seat, same session, ~12h apart, with two successful fires in between.** That upgrades "a compaction *can* kill it" from inference to observation.

  ⚠️ **Operational consequence, and it is NOT already covered by "check at every fire": the death happens BETWEEN fires.** The self-heal above only runs when a fire arrives — but the fire is exactly what dies. **So if you notice you have compacted, run `CronList` THEN, rather than waiting for a next fire that may never come.** A compaction is a named, observable trigger; treat it like one. *(Counter-note, offered so this is not over-read: CIO's `29c04997` survived a session that had been compacted — so compaction is **not sufficient** for death and some other variable is in play. Do not infer your cron is dead because you compacted; check.)*

  🔴 **Step 1a — HOST only, added 2026-08-07 after #1478 lapsed unpolled for 4 days.** A GitHub Actions workflow auto-generates `role-health-check` label issues on a 4-weekly cron. **The issue's own template says HOST's duty cycle polls for it — nothing did, for over two months.** Once per fire, cheap: `gh issue list --repo mediajunkie/piper-morgan-product --search "label:sapient-trust" --state open`. If a result exists and today isn't the day you're already handling it, note it in the fire entry and pick it up same-fire or next. **This is the "self-firing recurring task" mechanism Exec/PM asked for on 08-07 — it already existed; the missing half was this one line.**

  🟡 **Step 1b (cohort-freeze check) MOVED to just after Step 2b's sync, 2026-08-09 — Web's finding.** It reads local `dev/heartbeats/*.tsv`, and running it here (before any fetch) meant a stale local checkout produced a false COHORT-FREEZE on any role whose gap since last sync exceeded the detector's window — for a multi-hour cadence, close to the common case, not an edge case. See the relocated step under Step 2 below. *(Kept as a stub here, not deleted, so a reader following the old Step 1a→1c sequence finds a pointer instead of a silent gap.)*

  🟠 **Step 1c — HOST only, added 2026-08-08 (Exec's direct ask: "does a consolidation cadence belong on the recurring-task surface").** The shared memory index (`MEMORY.md`) has a hard ~200-line ceiling that truncates SILENTLY on write (`docs/internal/operations/memory-index-size-limits.md`) — one line per memory, shared by all 11 agents, no per-role isolation. **⚠️ Use the GUARD-CONVENTION line count, not a bare `wc -l`** (fixed 2026-08-09 — CIO and HOST independently reported 15 vs. 14 lines headroom for the identical file that same day; a trailing-newline difference makes `wc -l` under-count by exactly 1 relative to the generator's own `n_lines = body.count("\n") + 1`, which is what `rebuild-memory-index.py`'s truncation guard actually checks — the deliberately-conservative number, not the optimistic one). You already have this number for free: `scripts/check-derived-drift.sh` (run earlier this same fire) prints it directly — `✓ MEMORY.md matches its generator (N entries, B bytes, **L lines** [guard convention...])` when clean, or `generator would emit: **L lines**` when it just regenerated one. Read `L` from that output; don't shell out to `wc -l` separately. **Headroom = 200 − L.** ≥15 → nothing to say. **<15** → note it in the fire entry. **<8** → escalate by mail same-fire. **Never prune or delete a memory file to relieve this yourself** — that's a governance decision, not a formatting fix; the two safe levers are a generator change (PM approved denser entries, ①, 08-07) or an explicit, PM-visible consolidation pass. This step only watches the number and says so; it does not act on it. ⚠️ **A rate is only meaningful at the timescale it was measured on — name the timescale.** 08-09/10: CIO's intraday reads (0.25/h, then 0.00/h) and HOST's "~22 hours" extrapolation from one of them were both wrong; the 24-hour figure (3 lines/day, measured across a full day-night cycle) was right and stable. The error both times wasn't "trusting one interval" — it was comparing or overriding a longer-timescale figure with a shorter-timescale one without saying that's what was happening. If you compute a rate, say what window it's over, and don't let an intraday reading contradict a daily one (or vice versa) silently.

### Step 2 — Sync (worktree model depends on your host)

> **Read this before Step 2a.** This skill was written when Model B (Desktop's ephemeral per-session auto-worktree) was the only model. As of **2026-07-25 the model is host-dependent** (PM-ratified): **Model A — a stable, reused per-agent worktree at `~/Development/piper-morgan-worktrees/{role}`** on Amber; **Model B** on Claude Desktop. See CLAUDE.md §"Worktree model". Where this skill still says "ephemeral worktree," read it as "your worktree" — the sync and push mechanics are identical in both models. The one place the difference is *load-bearing* is the collision check immediately below, which was a Model-B artifact and is rewritten accordingly.

**Step 2a — worktree-collision check, FIRST, before any sync command touches shared state** (added 2026-07-19 after a confirmed real-data-loss incident — a PPM-session commit silently reverted already-pushed CIO content, root-caused to a worktree-provisioning defect where one physical directory got assigned to 3 different sessions — CIO, Exec, PPM — simultaneously across several days, undetected until a rebase conflict surfaced it):
```
basename "$(pwd)"          # your worktree directory name
git branch --show-current  # your current branch name
```
**On Model B (Desktop)** these two values match (branch = `claude/<dirname>` or `worktree-<dirname>`) — that pairing is created together and should never drift apart, so a mismatch is the fingerprint of the collision defect (empirically confirmed 2026-07-19: 21 of 22 live worktrees showed the correct 1:1 pairing; the one exception was the directory 3 sessions had been silently sharing). If the branch name doesn't contain your directory's basename, **STOP before running Step 2b's sync commands** — another session may be using this exact directory, and a routine `git merge`/`git commit` risks clobbering its in-flight work.

**⚠️ On Model A (Amber) this check is NOT sufficient, and passing it means almost nothing** *(rewritten 2026-07-25, CIO — Pard concurring on the detection side)*. Under stable per-agent worktrees the pairing is *permanent by construction* (`cio` ↔ `claude/cio-cycle` matches forever), so the fingerprint passes whether or not a collision exists. **The Model-A collision is two live sessions whose cwd is the same worktree** — which a branch-name check cannot see at all. Keeping the old check as your only gate on Amber is worse than having none, because it returns a confident pass.

What actually detects it, cheapest first:

- **tmux-side — the real gate. SHIPPED AND TESTED 2026-07-25** (Pard-owned, `amber-agent.sh`). At worktree standup it refuses to launch if **any** existing tmux session's cwd is that worktree *or a subdirectory of it*. Verified by occupying a worktree with a dummy session and confirming a second launch was blocked with nothing spawned. This catches the duplicate-on-one-worktree case a same-session-name check misses, and it is why the branch-name fingerprint above is now **genuinely superseded on Model A rather than merely documented as unreliable**. You do not run this yourself — it runs at standup, before your session exists.
- **In-session sanity** (what you can do from here): if you find commits, cron ids, or file content you don't remember creating, **the default hypothesis is your own pre-compaction work, not a phantom peer** (CLAUDE.md §"Unexplained state after a context gap"). Check your own session log *first*.
- **`git reflog` is the forensic tell, not the gate.** Entries of type `commit:` / `rebase (pick):` that you don't recognize mean another session really operated in this directory — as distinct from a plain `merge origin/main: Fast-forward`, which is just a normal sync. Good for confirming after the fact; too slow to gate on.

**Either model — if you suspect a collision**: don't guess at a fix (don't rename the branch, don't force-checkout, don't touch the other session's state). Flag it in your fire entry and to PM/Exec directly, then proceed cautiously (explicit-path adds only, `git status` immediately before every stage, push immediately to shrink the window) rather than freezing outright, unless PM says otherwise. This is detection, not a cure — the provisioning layer is where the fix lives, outside this repo.

**Step 2a-bis — verify your enforcement hooks actually fire (first fire in a worktree only)** *(added 2026-07-25 after Finding #4)*. Project hooks were found **silently inactive** in a Model-A sibling-path worktree: `check-branch.sh` did not block a `mailboxes/` commit from a feature branch, though the config was present, correctly registered, and the script ran fine when invoked by hand. **Config presence proves nothing — an absent hook and a silent hook are indistinguishable from inside a session.** On your first fire in a worktree, verify behaviorally.

⛔ **RETIRED at v1.22 (2026-07-29) — DO NOT RUN THIS.** The defect was a **time-of-check/time-of-use inversion** (Arch's ruling): `check-branch.sh` reads the index, but as a `PreToolUse` hook it runs *before* the command it gates. Pard installed a real `.git/hooks/pre-commit` in the **common dir** — all worktrees by construction, delegating to the same script. **Verify that hook exists; do not probe.** Full derivation (the v1.19 probe confound, its correction, the shape-vs-index-state distinction, all of it) moved out to `docs/internal/operations/duty-cycle-tick-design-notes.log` 2026-09-22 (context-floor item 2, Phase B) — none of it is needed to execute a fire; it's kept there for whoever next touches this mechanism and wants to know why it's shaped this way.


**Step 2b — the sync itself:**
```
git fetch origin main -q && git checkout -- mailboxes/*/inbox/MANIFEST.md mailboxes/*/read/MANIFEST.md 2>/dev/null
git merge origin/main --no-edit -q
```
Discard mailbox MANIFEST regen-noise. (Variant launch models — e.g. Web main-direct — skip the worktree dance per their registry row; see `cron-shape-experiments.md`.)

**Step 2c — cohort-freeze check, all roles (relocated 2026-08-09 from "Step 1b," HOST's half of the freeze-monitor seam, CIO's detector).** On the 2026-08-06 cohort-wide freeze, every waking agent treated its own dead gap as a personal or session-specific problem — nobody's wake procedure asked "was this environmental." At **START or WATCH only** (skip on ordinary WORK fires — not worth the cost six times a day when the answer is almost always clear): run `scripts/cohort-freeze-detect.sh`, **now that Step 2b has just fetched** — the detector reads local `dev/heartbeats/*.tsv`, and running it before a sync produces a false COHORT-FREEZE from your own stale checkout rather than a real cohort signal (Web, 08-09: a 3h-cadence role hit this on close to every fire, reproduced and cross-verified against `git log origin/main` before it nearly became a false full-cohort alert to PM). **rc=1 (COHORT-FREEZE)** → your gap wasn't yours: state that explicitly in the fire-open line (*"resuming after a detected cohort-wide freeze, window=…, not a personal stall"*) instead of silently proceeding as an ordinary START, and skip any self-diagnostic you'd otherwise run on your own dead gap — the detector already answered that question at cohort scope, more reliably than a self-report could (you cannot detect absence from a surface authored by the party whose absence is in question — Arch/PPM, 2026-08-06). **rc=0** → ordinary wake, nothing to say. **rc=3** → detector couldn't measure (registry unreadable, internal error); note it, don't block on it, proceed as an ordinary wake.
⚠️ **What this does NOT cover — named, not implied.** This only helps an agent that gets a turn *after* the freeze lifts; it says nothing to PM *during* one, because every agent's duty cycle is itself frozen at that moment — the same structural limit Gap-C's self-heal has (heals on the next turn, doesn't cure the gap). **Alerting PM during a freeze needs a watcher outside the frozen set** (real crontab or equivalent, not `CronCreate`) — that integration is CIO/Pard's to build, not this skill's. HOST's stake there is content, not delivery: whatever fires that alert should say what this detector already prints (window, scheduled count, emission count, emitters) rather than a bare "something's wrong," per the state-what-you-measured discipline this detector was built to.

**Re-check any anomalous reading once before reporting it — PM's rule, v1.33 (2026-09-11).** PM,
after watching Exec publish a possible stall that had already resolved: *"races are normal, no
stress... maybe it's good to re-check anomalous things soon after in case they were in a
transitional state when last checked?"* Applies to this cohort-freeze check, to `BELT-INVISIBLE` /
`NO-SESSION-LOG` reads from `duty-cycle-freeze-check.sh`, and to any other liveness snapshot — not
just this step. **The rule**: an anomalous reading (freeze, stall, missing marker) gets re-checked
once, a short interval later, before it's written into a memo or reported to PM. A role that is
genuinely dark reads dark on both checks; a race resolves between them and costs one extra command
to catch. This composes with m-44 rather than duplicating it — m-44 says a *clear* is not a
measurement; this says an *alert* isn't one either if it's a single sample of a value that moves.
The cost of skipping this: Exec's own real instance, a `BELT-INVISIBLE docs` read that was actually
a 4-minute-old snapshot of a role that had already invoked its heartbeat, published as a possible
stall before the second read would have shown it resolved.

### Step 3 — Read carry-forward, then dispatch by STATE (shape-independent — HOST finding 2026-06-06)
Read the cycle-log tail + `{role}-carry-forward.md` so you know where you left off. Then dispatch by a **state + window hybrid** — *state* (session-log-today existence) gates START-vs-WORK; *hour* gates overnight-WATCH-vs-morning-START. (This is the v1.2 refinement: pure-state was *almost* right, but the continuous shape's ~2am WATCH fire also has no-session-log-today yet, so a bare "no-log→START" rule mis-STARTs it overnight. The overnight-window guard fixes that while keeping HOST's low-freq fix intact.) **Check the overnight branch FIRST:**

- **Overnight window (local hour ~0–4, pre-morning) + nothing urgent** → **quiet-hold / WATCH** — *regardless of whether a session-log-today exists yet*. No START, no CronDelete, leave armed. For the continuous shape the single ~2am fire is the **WATCH** (quick `ls mailboxes/{role}/inbox/`; **commit a one-line WATCH entry**; see `procedures/watch.md`); low-freq shapes' overnight fires are plain quiet-holds. *(This branch first — and hour-gated — so the 2am fire doesn't fall into the START rule below.)*
- **No session log exists for today AND past the overnight window (local hour ≥ ~4)** → **START**: **Step 0 FIRST — verify the prior day STOPped properly, and run the missed STOP tasks if not** (PM-ratified 2026-06-09, Comms-surfaced): `grep -lE '^(<!--[[:space:]]*)?#{0,4}[[:space:]]*\**[[:space:]]*DAY-CLOSED\**[[:space:]]*[:—-]?[[:space:]]+[0-9]{4}-[0-9]{2}-[0-9]{2}' dev/2026/<prior-day-path>/*{role}*log.md` — if the prior day's session log lacks the **`<!-- DAY-CLOSED: {date} -->`** marker, that day ended without a STOP (PM takeover, cron reshape, session-death, or engaged-past-STOP-window). **Run its missed close NOW before today's START**: reconstruct the prior day's wrap from its cycle log + commits — day-arc + the memory-eval 3-bucket + the sign-off checklist + the `DAY-CLOSED` marker. This is *self-healing* — it doesn't wait for Docs's merge-keeper sweep to catch it the next morning (that's the reactive net; this is the proactive source-catch). *Then* proceed: create today's session log (`create-session-log` skill) + fresh cycle log, **and
commit that one-line START entry immediately — BEFORE the mail loop, not after** (v1.33,
2026-09-12, CXO's structural fix, applied on CXO's own seat same-day before the skill text caught
up). **Why the order is load-bearing, not stylistic**: `role_committed_today()` (the NO-SESSION-LOG
check's own signal, see `duty-cycle-freeze-check.sh`) matches ANY role-tagged commit, including a
`mail(role):` push under the per-memo commit-and-push norm — and under the old ordering (mail loop,
then the log commit), that mail push almost always lands FIRST, opening a window where "committed
today" reads true while "log exists" reads false. Two real false-positive instances (CXO 2m27s, PA
4m15s, both independently reproduced against `origin/main` commit timestamps) were this exact race,
not a genuine missing log — `duty-cycle-freeze-check.sh` v1.1's 20-minute grace window absorbs the
race as a mitigation, but **committing the log first removes the race at its source**: the log is
on `origin/main` before anything else can be. A session that dies mid-mail-loop also benefits — it
has a real log on `origin/main` instead of only on local disk.
  ⚠️ **The grep pattern above already reflects five rounds of correction made in two days** (CXO/HOST/Web, 2026-07-30): a naive `grep -l "DAY-CLOSED"` false-passed on logs that merely *narrate* a marker in prose rather than carry one; a first fix anchored too strictly on a trailing `-->` and false-*failed* 9 real annotated closes; a widened, column-0-anchored, date-shaped pattern (comment or heading form, colon optional) fixed both — verified behaviorally against real positive and negative cases, not asserted. **Do not hand-roll this regex or "simplify" it without re-running the census** — the current form is deliberately shaped by those five rounds. Full derivation, who made each error, and the regenerable verification numbers: `docs/internal/operations/duty-cycle-tick-design-notes.log` and `docs/internal/operations/day-closed-marker-census.md` (regenerate via `scripts/day-closed-census.py` before citing any figure from either — this history is itself the proof a copied number goes stale the moment the source moves).

**★ START also OWNS YOUR WATCHDOG REGISTRY ROW** *(added 2026-07-25 after finding #6)*. Immediately after arming your cron, verify your row in **`dev/active/duty-cycle-registry.tsv`** matches the cron you actually armed — and **write the row if it doesn't exist**. Columns are TAB-separated: `role⇥cron_expr⇥threshold_h⇥wake_start⇥wake_end⇥first_fire⇥active_since⇥state` (threshold_h = a bit more than your largest in-window inter-fire gap; first_fire = your first fire at/after wake_start; **state**, col 8, OPTIONAL — see next paragraph).

⚠️ **The 8th column, `state`, is a SEPARATE field from `active_since` — check and clear it explicitly, don't rely on a narrative overwrite of the rest of the row to touch it** (v1.37, 2026-09-21, Docs's finding, CXO relayed). A role whose STOP habit rewrites `active_since` with a full narrative (several rows visibly do this) can still leave a stale `parked:` value sitting in col 8, because nothing in the numbered steps above names the column — the habit that *looks* like a full-row rewrite is actually a col-7-only edit. Real instance: a role's row stayed `parked` through a clean day-close after a central park event, invisible because the STOP procedure that ran was, correctly, checking everything it was told to check — the state column just was never on that list. **Concretely**: if your row's 8th field reads `parked[: reason]`, and you are the owning session, clear it (overwrite with `active: ...` + your own evidence) at START, per the registry file's own clearing-condition text on that row — never at STOP, never by a peer. This is the same discipline that closed finding #6 for row *existence*; this closes it for row *state* too — a row that exists but lies about being parked is exactly as invisible to the watchdog as no row at all, just in the opposite direction (a role reported dark that's actually fine, rather than the reverse).

**Why this is the agent's job and not the provisioner's**: the registry is an **opt-in watch list** — no row means the freeze-watchdog is structurally incapable of noticing you're dead, and it will report the cohort as clear while you're dark (finding #6: it covered 4 of 10 roles and phrased its subset as a total; five roles had been dark six days). The obvious fix is "the provisioner writes the row at standup" — **but the provisioner cannot, because the row's load-bearing field is the cron expression and that isn't known until the agent arms it.** Proven immediately: at HOST's 2026-07-25 provisioning Pard correctly declined to guess-edit and deferred the row, so agent #2 came up live and unwatched. **You always know your own cadence; nobody else does.** Same reason a stale row is its own hazard — if you change cadence mid-day, the row changes with it (see Step 7). *(Gating START on "no-session-log-today" — not a fixed "~04" — keeps HOST's fix: a low-freq agent whose first fire is ~06:37 still STARTs correctly. The `≥~4` guard only excludes the overnight-WATCH window, not the whole morning.)*

**★ START also checks your OWN tracked-state files' currency claim, if you've adopted one** *(added 2026-08-30, CIO/CXO — docs/internal/design/tracked-state-staleness-design-2026-08-29.md)*. If your carry-forward or standing-items file declares `currency_claim`/`max_age_days`/`last_updated` frontmatter (opt-in, not mandatory — see the design doc §4), run `python3 scripts/check-refresh-promises.py --state-files {role}` right after reading the carry-forward in this same Step 3. This is the moment the claim goes stale, per the design's §3(b): the file you just read is either backing its own header or it isn't, and this is a machine check instead of trusting the prose. On STALE, say so plainly in the fire-open line (*"my own carry-forward reads stale per its own declared claim — X days over Y"*) rather than proceeding as if the header were evidence. On UNDECLARED (no frontmatter adopted yet), nothing to report — adoption is per-role and voluntary, not a gap to fix on someone else's file. This does **not** replace the existing sync-then-read Step 2→3 ordering; it's an additional cheap check right after, for roles that have opted in.

**★ START also REFRESHES and RE-VERIFIES the carry-forward — cohort norm, mandatory, all roles** *(v1.32, 2026-09-08, PM-ruled)*. This is separate from, and does not replace, Step 7's end-of-fire rewrite.
- **Refresh at START, not only end-of-fire, because the failure mode is the long quiet stretch.** A role can run several correct, no-op WATCH fires in a row — nothing changes, so end-of-fire never triggers a rewrite — while the carry-forward silently ages into a wrong claim about what PM is waiting on. An end-of-substantive-fire refresh structurally cannot fire on exactly the days this happens; a START-side refresh is the only one that runs on those days too.
- **Rewriting is not re-verifying — for every row you carry as "PM-gated" or "waiting on X," re-check it against its actual source before deciding it's still true**, not just before deciding how to phrase it. Real incidents the same morning this shipped, on files that WERE regularly rewritten (all three dated within the prior day): a "waiting on PM" item PM had answered two days earlier; a time-boxed item PM had already resolved by the deadline passing; a "PM-gated" GitHub issue that was already closed. Three surfaces to check per PM-gated row: **(1) `decisions.log` + any purpose-built doc** — is there already a ruling? **(2) your own `sent/`** — did you already get an answer via mail? **(3) GitHub state** — is the issue still open?
- ⚠️ **Honest limitation, stated rather than hidden**: as written here, the re-verify half is a PROSE instruction, not a chokepoint — nothing forces it beyond reading this line, which is structurally the same shape as methodology-50 (a compliance record is only evidence if it's checked, not narrated). `aging-standing-items.sh`'s stale-blocker-rot check already gives surface (3) partial mechanical backing (flags a blocker citing a closed `#NNNN`); surfaces (1) and (2) have no mechanical check yet. Shipping the prose rule now per PM's ruling rather than waiting for a mechanism — but naming the gap so it doesn't quietly get treated as closed.
- **Session log exists + this is the last scheduled fire of today + PM idle + not yet STOPped today** → **STOP**: day-close; **LEAVE CRON ARMED** — but re-arming is **delete-then-create, not create-only**: `CronList` first, `CronDelete` any existing job(s) for this expression (the day's cron is very likely *still alive* at STOP — STOP is a day-close ritual, not evidence the cron already died), **then** `CronCreate` fresh, **then** `CronList` once more to confirm exactly one job survives. Skipping the delete step stacks a duplicate on top of the still-live job (self-inflicted instance, 2026-07-10: a fire followed an earlier version of this exact instruction literally — "re-CronCreate ... as the final action" — and produced two jobs on the same expression, diagnosed the next morning as methodology-35, Asymmetric Discipline: the creation-half was specified, the cleanup-half wasn't). **The "last scheduled fire of today" rule (v1.6, 2026-06-12, PM-coined)**: compute the next scheduled fire from your cron expression; if its calendar date is different from today's, this is the last fire of today → STOP. Works elegantly for every shape — continuous `7 2,4-23` STOPs at 23:07 (next is 02:07 tomorrow), windowed `7 3,10,13,16,19,22` STOPs at 22:07 (next is 03:07 tomorrow), windowed `42 6,9,12,15,18,21` STOPs at 21:42 (next is 06:42 tomorrow), windowed `37 6,9,12,15,18,21` STOPs at 21:37 (next is 06:37 tomorrow). **Replaces the old "past ~11pm" rule** (v1.5 and prior) which never fired for windowed shapes ending before 22:00 → cohort-wide STOP-never-triggers gap, caught by Exec 6/12 + confirmed by PA's identical improvisation ("last evening fire = day-close"). PA's ad-hoc rule was the right rule; PM codified it. **The two resolutions COMPOSE (Exec 2026-06-12), don't compete**: this proactive last-fire-STOP is the *primary* mechanism; the v1.4 START Step-0 self-heal is the *backstop* for when the last fire never fired at all (Gap-C session death / dormancy at the last slot) — that morning's START detects the missing `<!-- DAY-CLOSED -->` marker and writes the retroactive close. Implement BOTH: proactive-only silently fails if the last fire dies; reactive-only leaves the prior day's session log reading as in-progress until the next START. *Heuristic if you can't compute next-fire precisely*: "is my current fire-hour the largest hour in my cron expression?" works for most shapes (schedules don't wrap mid-day). **Wrap the session log** (the single record): the day-arc summary + the memory-eval 3-bucket section (#974) *filled* + the sign-off checklist (`git status` clean / `@{u}..HEAD` empty / `main..HEAD` empty). *(PM 2026-06-12 one-place ruling: wrap the session log; any optional cycle-log scratch needs no formal close.)* **If the session spanned a day boundary without a STOP** (ran continuously / compacted overnight), the retroactive close MUST still wrap the *prior day's* session log (memory-eval + sign-off), not only its cycle log. **Emit the canonical close-out marker**: the session-log sign-off section MUST include a literal **`<!-- DAY-CLOSED: {YYYY-MM-DD} -->`** line — the grep-able sentinel that START's Step-0 self-heal (and the Lead-owned session-start hook) check for to detect "did a proper STOP happen?" (PM-ratified 2026-06-09; standardizes the close-out detection — prior close-outs varied: "DAY-CLOSE", "## STOP", prose). **Distributed cleanup (HOST spec, `docs/internal/operations/duty-cycle-stop-cleanup-spec.md`, 2026-07-04)**: before the STOP commit, remove stale ephemeral scratch — `dev/active/cycle-log-{role}-YYYY-MM-DD.md` files ≥7 days old and `dev/active/*.tmp` files ≥1 day old, nothing else (never `*-carry-forward.md` / `*-standing-items.md` / `duty-cycle-registry.tsv` / sprint backlogs — see the spec's out-of-scope list; if in doubt, don't delete). Dry-run the list first (`find dev/active -name 'cycle-log-*.md' -mtime +7`), then delete, then **stage each deleted path explicitly by name in the STOP commit** (`git add <explicit-path> <explicit-path> ...` — never `git add -A` / `git add dev/active/`, per this repo's explicit-paths-only discipline; HOST's spec illustrates the deletion logic with a directory-level add, but the STOP commit itself must enumerate paths one by one like every other commit in this skill). The commit message names the count + threshold (e.g. `stop({role}): cleanup N stale cycle-log files (>7 days)`) so the commit log is the audit trail — no separate cleanup artifact. **Attention-doc reconciliation — REMOVED 2026-06-17 (FOLD, PM-ratified).** The per-role `duty-cycle-escalations-{role}.md` docs are **deprecated**. This hand-maintained reconcile step was itself vigilance-dependent and rotted anyway (Exec 6/17: most docs 1–3 weeks stale *despite* the step — the very pattern the step was meant to prevent). The cohort-attention rollup now GitHub-verifies every item (doesn't trust the docs) and the freeze-registry handles liveness, so the docs are no longer load-bearing. **PM-attention / escalation items now ride the carry-forward** (the residual home); a genuine PM escalation goes via **mail** (the signaling layer). Nothing to reconcile at STOP.
- **else (session log exists, daytime, work to do)** → **WORK PARTS — the mail/task loop.**

  ⚠️ **RESTORED 2026-08-07 to `duty-cycle-design-v0.6.md` lines 105–113 (PM-authored, PM-ratified 2026-05-25).** PM: *"I wrote a detailed spec for the duty cycle with exactly what the mail and task parts are and their rules. It clearly has gotten flattened and I want CIO to bring back the original discipline."* Exec found the exact diff. **The five steps below are PM's, restored to their original specificity — do not compress them again.**

  ⚠️ **The inbox listing must follow Step 2's sync, never precede it — PM-ratified 2026-08-28** (*"a fresh sync with origin main should precede any mail check"*), from a real incident: Lead's fire-opener ran `ls mailboxes/lead/inbox/` **before** `git merge origin/main`, so mail that had already landed on `origin/main` was invisible for a full fire — CXO's design position had reached Lead's worktree at the merge moment but wasn't *seen* until the next fire, so Lead reported the thread "quiet" and asked PM to nudge CXO for something CXO had already sent. **Nobody was careless — the ordering silently produced a stale view that looked authoritative**, same shape as Step 2c's cohort-freeze relocation above (a component reading local state before a fetch reports on the *previous* fire's world, not this one's). If you write your own fire-opener rather than following Steps 2→3 in order, this is the one sequencing mistake that costs the most and shows the least.
  1. **Mail Loop drain — process the inbox to ZERO.** **Each new memo handled FULLY.** A memo addressed to you **directly** is read in full and gets a **substantive response drafted and distributed**, or an explicit action taken. A **cc** may be skimmed for asks and triaged to `read/`. ⚠️ **This direct-vs-cc distinction is load-bearing and was the specific rule lost in the flattening** — PM restated it 2026-08-07: *"a cc may be skimmed for asks but a direct message must always be read and acted upon or responded to."* **Do NOT stop after one memo.**

  ⛔ **NEVER move mail with a directory glob** (`for f in inbox/*.md; do mv …`). **`read/` is not a folder — it is a CLAIM ABOUT YOUR OWN COGNITION**, and a glob makes that claim mechanically, for every arrival, without anyone reading anything. **The drain must iterate a list you appended to in the same tool call that displayed the memo's contents**: unread ⇒ never in the list ⇒ *cannot* move. Bad state unrepresentable rather than forbidden. **If a fire ends with unread mail it stays in `inbox/` and the fire entry says so — a non-empty inbox is honest; a `read/` holding unread mail is a lie nothing can detect.**
  *(Arch, 2026-08-09, PM-routed for cohort adoption after ruling "we need to prevent this from EVER happening. It is a real violation of trust." Their glob moved a memo they had never read; they then reported it did not exist, and a second role independently "confirmed" the absence by inheriting that framing. CIO's own drain had the identical defect. **PM offered a third folder and Arch declined it — the defect is an UNVERIFIED TRANSITION, not a missing state; a third folder just gives the bulk loop one more place to put unread things.** And note you cannot audit this from outside: grepping session logs for the idiom finds only roles who happened to paste their command, so each role must check its own drain.)*
  1c. **Unboarded-PM-items scan (v1.36, 2026-09-19).** After the mail drain, run
      `scripts/check-unboarded-pm-items.sh {role} --scope=role --since-last-scan --record` — cheap,
      role-scoped, every role, every fire. **Only the role currently compiling the cohort-attention
      board** additionally runs `scripts/check-unboarded-pm-items.sh {role} --scope=global
      --since-last-scan --record` (PM's inbox + commit-message bodies — identical for all 11 roles,
      so only the compiler needs it). **Hits are candidates, not verdicts** — read each one before
      acting; the script itself never claims a clean run means nothing needs PM. This exists because
      diligence (prompt mail triage) was the failure mode on the miss that motivated it — a memo
      moved `inbox/`→`read/` in the same commit landed on a surface no board sweep read, invisible
      for 5 days despite nobody being careless.
  2. **Task Loop drain** — process queued tasks from `dev/active/{role}-standing-items.md` in **priority order**, until ALL are blocked-on-external or the queue is empty. **Do NOT stop after one task.**
  2b. **THIRD QUEUE SOURCE — PM's ruling, v1.33 (2026-09-11), supersedes v1.32's build-capable-only
      scoping.** PM, verbatim: *"the mail inbox is not the single source of truth about new work to
      do... we need to define the work queue as a combination of carried work (if any), incoming
      memos in mail, and newly observed github issues that meet relevant criteria... An agent should
      really only go idle when there is nothing to work on at all."* **This is not a third loop to
      skip — it is what "drained" now MEANS, for every role, not only build-capable ones.** The gap
      this closes: the flywheel's work-definition used to be exactly mail + your own standing-items,
      so "there is no work" and "28 open milestone items" were simultaneously true, and a role idling
      on an empty inbox + blocked tracker was the procedure working *exactly as specified* — not a
      lapse. v1.32's Sprint-Backlog-only version was PM's first patch at this same gap; this widens
      it to the general rule PM actually asked for, which names Docs (audit-labeled + audit-generated
      issues) and "some of the other agents who get assigned github issues at times" explicitly, not
      only Lead.

      **Every role states its own criteria line** — a single, cheap, mechanical GitHub query,
      committed to this role's own carry-forward or a config file, not re-derived from memory each
      fire. Worked examples already in production: HOST's Step 1a (`label:sapient-trust`, state:open
      — the earliest instance of this shape, shipped 8 months before this ruling generalized it);
      Lead's is "new issues in the current sprint milestone"; CXO's is `label:UX state:open`
      (denominator 3, explicitly NOT folding in the separate `MUX` label since that's a product
      surface, not a review criterion). **If you don't have a criteria line yet, that's a gap to
      name in your fire entry, not a blocker on everything else** — a role with no criteria line
      simply has an empty third source until it writes one, same as an empty inbox is a fact, not a
      failure.

      **The criteria line's own wording must require opening each returned issue, not just listing
      it** (CXO's finding, 2026-09-12 — filed after their own criteria line returned 3 issues and
      CXO wrote 2 of 3 tracker rows wrong by working from `gh issue list`'s title/number output
      alone): *"`gh issue list` finds the work. `gh issue view N` is what tells you what it is. A row
      written from the list is a guess about the issue."* A list is a fragment by construction —
      cheap to skip at a small denominator, which is exactly why it will get skipped silently at a
      larger one if the criteria line's own wording doesn't say to open each one.

      **Claim = set board Status to `In Progress` via `updateProjectV2ItemFieldValue` (never the
      field-level `updateProjectV2Field` — see CLAUDE.md's GitHub-Projects-v2 gotcha) before starting
      work**, for roles whose criteria line pulls from a board-tracked source (Sprint Backlog, etc.).
      First-write-wins is sufficient while one role at a time pulls from a given queue; if that
      changes, the claim needs a read-immediately-before-write check, not a blind set (PPM's own
      flagged caveat — don't let this convention silently get outgrown the way the two-surface
      work-definition did).

      **State the denominator when you report drained**: *"mail (N drained) + standing-items (N
      drained) + [your criteria line] (checked M eligible, claimed/actioned one/none)"* — not a bare
      "nothing left" — so a missing or stale criteria line announces itself instead of hiding behind
      an all-clear for months, the way the original two-surface definition did (Arch's refinement,
      direct application of methodology-44 to the work queue itself). **Idle is now the state where
      all three sources are checked and empty** — not a default you fall into when the inbox happens
      to be quiet.
  3. **Re-check the Mail Loop** — new mail may have arrived while you were draining tasks.
  4. **Loop 1–3** until there is truly nothing left to do.
  5. **Only THEN return to IDLE — and "nothing left" means TWO CONSECUTIVE EMPTY ROUNDS, not one
     clean pass.** (PM's own formalization, 2026-09-22, verified against this prose and found
     weaker than specified: PM's exact rule is a 16-state table over two rounds of (mail, tasks)
     — every pattern except **two consecutive (0 mail, 0 tasks) rounds** continues the loop, and
     that includes a round with new mail but no tasks, new tasks but no mail, or either appearing
     in the round *before* the current one even if the current round is itself clean. This prose
     previously said only "loop until nothing left, then exit," which a single clean pass through
     1→2→2b→3 already satisfies — weaker than PM's requirement, and exactly the gap Docs flagged
     when relaying PM's ask.) **A "round" is one full pass through steps 1, 2, 2b, 3.** Track
     whether the round you just finished found ANYTHING across all three sources (call it
     **non-empty**) or found nothing at all (**empty**). **Exit to IDLE only when the round you
     just finished AND the round immediately before it were BOTH empty.** One empty round is not
     enough on its own — run one more full round before going idle, specifically to catch anything
     that lands in the gap between "I just checked" and "I'm about to stop checking."

  **Report what you actually did** (Exec's verification half, folded in here rather than added alongside — it verifies a rule that already exists): `mail: N direct, N read in full; M cc, skimmed`. A count you cannot state is a drain you did not do.

  - <sub>**Clerical sub-step, subordinate to the above.** After the mail moves, regenerate **your own** MANIFESTs: `python3 scripts/regenerate-mailbox-manifests.py --role {role-slug}` — the #1106 derive mechanism (v1.7): the recipient is the sole MANIFEST writer; the regen derives the table from filesystem state + frontmatter `subject:` (first-H1 fallback; `(no subject)` warned to stderr, never silent) and preserves curated content at/below the `<!-- curated -->` marker verbatim — put prose annotations there, never in the table. Send regenerated MANIFESTs with your mail-move via `mail-send.sh` push-to-ref.</sub>

  🔎 **A note to whoever edits this next, because the failure mode will recur.** Nothing was deleted in a single edit. Before this restoration, the **MANIFEST mechanics above ran ~230 words inside this step while the actual obligation — *handle every memo fully* — was six.** A clerical detail accreted around a substantive rule until the rule read as a clause inside it. **Mechanics are easy to write precisely and get expanded on every incident; obligations are hard to write precisely and get compressed to fit.** The cost was real and specific: **Exec was corrected by PM in August for violating a rule ratified in May that this skill had already dropped.** If you find yourself expanding a mechanism inside a step, check what obligation is shrinking to make room.

### Step 4 — Execute the dispatched part
**★ Before you finish the fire, emit your heartbeat** (v1.21): `scripts/duty-cycle-heartbeat.sh {role} {START|WATCH|WORK|STOP} --if-quiet`. It self-suppresses when the fire already committed, so on a busy fire it costs nothing. **A quiet fire that skips this is invisible to the freeze-watchdog** — that is the failure this closes, and it is the one case where doing nothing is not a safe default.

Hold the discipline: holistic-not-tactical. Quiet hold beats manufactured busywork. Batch identical daytime no-op holds (don't commit a near-duplicate entry each fire) — but **WATCH and START always commit a one-line entry**.

### Step 5 — Log each work UNIT (single-surface — the session log)
Event-based: the log entry rides with each **work-unit commit** — NOT a per-fire wrap (logging *per fire* is one of the things that re-implies fire-as-session). **Write each work unit to the SESSION log** (`dev/2026/MM/DD/{date}-{role}-code-opus-log.md`): `- (HH:MM PT) — what shipped (detail, commit refs, reasoning as warranted)`. The session log is the **single canonical record** (PM 2026-06-12: *"simplify logging, minimize drift — do the logging in one place"*). Trivial/quiet-hold fires don't need an entry; any fire that ships a memo / decision / code / methodology edit DOES. Don't let the record format pace the work (see the spine above).

**Heading default changed, v1.33 (2026-09-11) — "next fire" vocabulary and the `## Fire N` heading
retired as the organizing unit.** Exec found the skill's own text says "fire" 58 times against 2
explicit anti-chunking warnings — the doctrine forbids per-fire chunking and reinforces the frame
that produces it, 29-to-1. A same-morning cohort self-audit (8 seats) found the actual *chunking*
behavior mostly isn't happening (2 of 8 genuine deferrals, both resolved same-cycle) — but the
`## Fire N` heading convention is real and costs something concrete: Docs, who synthesizes all 11
roles' logs into the daily omnibus, reported it directly costs real reconstruction effort to
recover "what shipped" from "what happened at wake N" across differently-formatted logs, and every
seat independently confirmed the headings are wake-timestamps, not work-unit labels. **New default:
head each entry by the work unit (what shipped), with the wake time as a parenthetical, not a
`Fire N` heading** — e.g. `### Grace window widened after CXO's distribution measurement (16:37
fire)` rather than `## Fire 2 (16:37 WORK)`. A wake that drains several unrelated units gets several
headings, each named for its own work, not one numbered container. **"Next fire" stays retired from
agent vocabulary entirely** (the spine section above already states the rule — name a real trigger
or don't defer; this is the vocabulary that makes violating it easy). If you're deferring
genuinely-deep work, name the actual trigger (a fresh session, a compaction) in the heading or the
entry itself, never "next fire" as a bucket.

**Optional scratch**: an agent MAY keep a per-fire scratch list in `dev/active/cycle-log-{role}-{today}.md` if it's useful working state — but it is **not a logging surface, not a parallel record, and never the durable home for work**. The session log is where logging happens.

**Why one place** (PM-ratified 2026-06-12, supersedes the v1.5 dual-surface design): the displacement trap (the fire loop wrote only the cycle log → the durable session log silently stubbed → work vanished when `dev/active/` was sprint-cleaned) is cured at the source by logging to ONE durable surface, rather than guarding against drift by writing to two. One place can't drift from itself. *(Composes with — does not replace — START's session-log creation and STOP's session-log wrap.)*

### Step 5b — Emit your heartbeat (MANDATORY, and it was invisible before v1.24)

```
scripts/duty-cycle-heartbeat.sh {role} {START|WATCH|WORK|STOP} --if-quiet
```

⚠️ **This was a bolded aside inside Step 4 from v1.21 until 2026-08-04, and NOBODY RAN IT — including its author.** The heartbeat surface holds exactly one day of data (7/28, the day it was built) and nothing since. An instruction that is not a numbered step reads as commentary; agents execute Steps 1–7. **Promoted to its own step for that reason alone.**

**`START` writes unconditionally** (v1.24) — `--if-quiet` is ignored for it. Refinement (a) suppresses writes whenever the role has committed, which on a busy cohort is every fire, so the surface is legitimately empty on a healthy day. That made the writer-liveness check unable to tell *"nobody ran it"* from *"everyone was busy"* — and it went unrun for seven days while the daily 06:46 false alarm it prevents fired five times.

**Why this closes that alarm**: the belt reads `origin/main`. A role that starts at 06:27 but does not push until 07:01 is invisible at the 06:46 sweep — correctly reported as no-heartbeat, wrongly read as stalled. A START heartbeat pushed immediately makes the role visible the moment it wakes.

**Verify you actually ran it — don't trust that you did, v1.34 (2026-09-12).** CIO (this skill's own
author) went two consecutive days without a single heartbeat invocation despite 8+ real commits
each day, caught both times by a colleague reading a cohort-attention rollup rather than by
anything in this skill. The root cause Exec named: running Step 5b and skipping it produce the
*identical* local output on a busy fire — nothing, from the invoking agent's own side — so there is
no in-the-moment cue that the step was ever skipped, and "remember to run it" is not a mechanism
(m-36). **Don't rely on memory that you ran the command above — check it, cheaply, against the one
surface that doesn't depend on you having run anything**: `scripts/duty-cycle-freeze-check.sh | grep
-i {role}`. If your own role name shows up with `BELT-INVISIBLE` or `NO-SESSION-LOG`, that is not
background noise for someone else to eventually notice — it means Step 5b (or Step 0's session-log
commit) genuinely didn't happen this cycle, and it's an in-fire action item: run the missing step
now, before returning to idle.

**Refined same day (CXO, 2026-09-12) — check the denominator too, not just the grep.** "No output
for your role name" is itself an invisible-success signal: a genuinely clean role and a script that
died, changed its output format, or got grepped for the wrong string all produce the identical
nothing — the same numerator-with-no-denominator shape CXO independently caught in their own
scope-guard `verdict:` proposal two days earlier. The fix costs nothing because the script already
prints it: **read the FULL output first (not just the grep), confirm the header line's `rows=N` is
non-zero** (`freeze-check: examined ref=... rows=11 at ...`), *then* grep it for your own role
name. A non-zero `rows=` plus no match for your name is a measured absence; a bare unmatched grep
with no denominator check is not. This is the same external-surface principle Step 2c already uses
for cohort-freeze — the check that catches you
should not be the one you're being asked to trust you ran.

### Step 6 — Commit + push (verify it lands)
- **Non-mail** (logs, docs, design): commit on your ephemeral worktree branch → `git push origin HEAD:main` (NEVER `git checkout main` in this worktree). On non-fast-forward: `git fetch origin && git rebase origin/main`, then re-push.
- **Mailbox writes**: via **push-to-ref** — `scripts/mail-send.sh "mail({role}): subject" <explicit mailbox paths>` from your OWN worktree (#1259, swapped live 2026-06-19). It builds the commit on `origin/main` (`commit-tree` via a throwaway index) and pushes straight to `main` — no `cd` to the main checkout, no stash, no branch-switch; the old main-worktree bridge dance is **retired**. `check-branch.sh` stays as the backstop for any interactive mail `git commit` (`commit-tree` doesn't trip it).
- **Pre-staging discipline** (run in this order every time): `git reset HEAD` → explicit-path adds → `git diff --cached --name-only` (read every line, confirm only your files). `git reset HEAD` clears index residue from rebase/autostash/merge before you stage anything — skipping it is how the wrong files silently get committed (Web 2026-06-15: autostash debris swept into close-out commit instead of the session log).
- **EXPLICIT-PATHS-ONLY** on every `git add`. Never `git add -A` / `git add .` / directory adds. **NEVER** unconditional `git stash pop`.
- **VERIFY the push landed on origin/main** — main is busy; fast-forward races happen. `git fetch origin main && git branch -r --contains HEAD | grep origin/main`; if rejected, `git merge origin/main` + re-push.

### Step 7 — Update carry-forward + manage cron, then brief status
- **Rewrite `{role}-carry-forward.md`** with current ephemeral state (this is what replaces the frozen prompt block).
- **Cron — ONE rule (it's your idle self-wake, nothing more)**: keep it **ARMED by default**, *including throughout PM conversation*. It can't fire while the REPL is busy, so armed-during-work-or-convo is harmless; armed means it re-wakes you the **moment** you go idle — which is the whole point. (This is why "arm only on reaching idle" is wrong: if the session backgrounds *during* work or convo, you'd have no armed cron to self-wake — a stall. Armed-by-default closes that.) **The only time you DELETE it: while you're actively draining genuinely-substantive multi-step work** (so a queued fire can't interrupt mid-build) — then **re-arm the instant you return to idle** (incl. end of STOP), where "re-arm" always means **delete-then-create** (`CronList` → `CronDelete` the existing job → `CronCreate` fresh → `CronList` to confirm exactly one survives), never a bare `CronCreate` assumed safe because "the old one probably already died" — at STOP specifically it almost certainly hasn't (see STOP's re-arm step above; this is the same instruction, not a different one). A **pending PM question never deletes the cron and never blocks other unblocked work** — hold only the thread awaiting the answer; drain everything else. A trivial one-line fire needs no delete. *(This collapses the former Rule-1/Rule-2 into one: armed-by-default, deleted only mid-substantive-build, re-armed at idle. PM-ratified shape 2026-06-06; unified 2026-06-23 per the fire-as-timebox structural pass.)*
- **Whenever you CronDelete+CronCreate to change your OWN cadence** (not just a same-expression re-arm): (1) log the explicit old-id → new-id transition **with the reason** in your session log, in words unambiguous to a future amnesia-recovering read (e.g. "changed my own cron from `X` (3×/day) to `Y` (5×/day), PM-approved bump" — not just "re-armed"); (2) **update your row in `dev/active/duty-cycle-registry.tsv`** if the cadence itself changed, not just the job id — the watchdog reads that file, and a stale row there is a second, independent source of confusion on top of (1). Diagnosed 2026-07-06 from two compounding incidents: a cron-id change misread by a later fire as evidence of a second session (see the compaction-recovery guidance in CLAUDE.md), and a registry row that silently went stale for two days after a same-day cadence bump because only the carry-forward was updated, not the registry.
- Give the user a brief status line.

## Anti-Patterns to Avoid

| Don't Do This | Why | Do This Instead |
|---|---|---|
| Freeze carry-forward state into the cron prompt | You hand-refresh it every re-arm (vigilance); copies drift across agents | Write it to `{role}-carry-forward.md`; the skill reads it (mechanism — m-36) |
| Put the procedure in the prompt | N agents carry N divergent copies | One versioned skill; the prompt invokes it |
| `git add -A` / directory adds | Sweeps other agents' working-tree state | Explicit paths only, every time |
| Commit a near-identical no-op hold every fire | Log churn | Batch daytime quiet-holds; only WATCH/START always commit |
| Log substantive work in the cycle-log scratch instead of the session log | The durable record stays empty → institutional-memory leak (cycle logs are ephemeral `dev/active/`, sprint-cleaned; only the dated session log is durable + read by Docs's omnibus) | Log in the session log — the single canonical surface (Step 5, PM 2026-06-12). The cycle log is optional private scratch only |
| STOP by CronDelete-and-leave-deleted | No morning self-wake (Gap A) | STOP leaves the cron ARMED via delete-then-create (`CronList` → `CronDelete` existing → `CronCreate` → verify exactly one) |
| STOP re-arm by bare CronCreate, no prior delete | Stacks a duplicate on the still-live job (methodology-35 instance, 2026-07-10) | Delete-then-create, always — see STOP's re-arm step |
| Assume the push landed | main is busy; fast-forward races | Verify on origin/main; merge + re-push if rejected |

## Quality Checklist

After each fire:
- [ ] Exactly one cron job for your expression (no duplicates)
- [ ] **Fire entry written to the session log** (the single canonical record — every substantive fire)
- [ ] (optional) cycle-log scratch updated, if you keep one — never in place of the session-log entry
- [ ] Work verified on origin/main (not just pushed to branch)
- [ ] `{role}-carry-forward.md` reflects current state (if substantive)
- [ ] WATCH/START committed a one-line entry (if applicable)
- [ ] STOP only: stale cycle-log/`.tmp` cleanup run + deleted paths staged explicitly in the STOP commit (HOST spec; never a directory-level add)
- [ ] Cron in the correct state for what comes next (armed by default — incl. through PM conversation + overnight; deleted ONLY for Rule-1 substantive multi-step work, re-armed at IDLE)

## Examples

### Example 1: Quiet WORK fire (inbox zero, queue clear)
Date 14:07 → WORK PARTS. Sync clean, inbox zero, standing-items has no unblocked low-pri. → Quiet hold (batch if identical to last). No CronDelete (trivial). Brief status. Done.

### Example 2: Substantive WORK fire (mail to act on)
Date 10:09 → WORK PARTS. Inbox has a memo needing a reply. → CronDelete FIRST (Rule 1). Draft reply + send via `mail-send.sh` (push-to-ref, explicit paths), triage source → read/, log the fire, push + verify, rewrite carry-forward, CronCreate same expr back. Brief status.

### Example 3: STOP (day-close)
Date 23:37, PM idle → STOP. Final mail-check, append day-close to session + cycle log, commit + push + verify, rewrite carry-forward for tomorrow, **re-arm via delete-then-create** (`CronList` → `CronDelete` the day's job → `CronCreate` fresh → `CronList` to confirm exactly one) as the final action. Brief status.

## Cross-references
- `docs/operations/duty-cycle design/procedures/cron-lifecycle.md` — Rule 0/1/2 + v0.6.3 in full
- `docs/operations/duty-cycle design/procedures/watch.md` / `stop.md` / `start.md` — the day-parts
- `docs/operations/duty-cycle design/canonical-cron-prompt-template-v0.7.md` — the (now thin) cron prompt
- `docs/operations/duty-cycle design/cron-shape-experiments.md` — per-lane cron-shape variants
- `.claude/skills/create-session-log/SKILL.md` — invoked by START on a new day
