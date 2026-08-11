# CIO handoff — 2026-08-11 Amber reboot (macOS 26.6)

**Written 06:2x PT, before the ~07:30 reboot.** Session is expected to resume via `claude --resume` with
conversation intact. **This document assumes resume FAILS** — everything needed for a cold start is here
or pointed at from here.

**Role**: Chief Innovation Officer · slug `cio` · Amber · account `pipermorgan.ai`
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/cio`, branch `claude/cio-cycle`, upstream
`origin/main` (Model A — stable path, **reuse it, never create a fresh one**; never work in the shared
checkout `~/Development/piper-morgan-product`).

---

## 🔴 FIRST ACTION AFTER RESUME OR COLD START — re-arm the cron

> ## ⛔ THE SCHEDULE IS PARKED. I CANCELLED IT DELIBERATELY AT 06:3x ON 2026-08-11.
> **This is not a cron that died — it is one I killed on purpose**, per Pard's second stand-down notice,
> so that no fire could arrive after this handoff was written and therefore land outside its coverage.
> **`CronList` returning "No scheduled jobs" is the EXPECTED state right now, not a fault.**
>
> ### The exact schedule to restore — this line is the whole point of parking it
> ```
> CronCreate   cron: "7 10,16,22 * * *"   recurring: true
> ```
> **LEAN cadence, PM-approved.** Three fires daily at 10:07 / 16:07 / 22:07 PT. *(Fires arrive ~+30 min
> after the cron minute — that is measured scheduler dispatch latency, not a fault.)* The prompt body to
> restore is the one in the 2026-08-10 STOP entry of `dev/2026/08/10/2026-08-10-1037-cio-code-log.md`;
> if that is unreachable, a thin prompt naming role + worktree + cadence + "run the `duty-cycle-tick`
> skill" is sufficient, because **the procedure lives in the skill, not the prompt.**

**Why this was worth doing rather than letting the reboot take it**: `CronCreate` jobs are session-scoped
and do not survive a process exit — **resume restores the conversation, not the scheduler.** A schedule
killed by a reboot is **invisible afterwards**: the fleet comes back looking healthy and quietly never
fires again. **Parking it deliberately and writing the cadence down here means restoring it depends on
this file rather than on anyone's memory surviving the reboot** — including mine.

After re-arming: **update the `state` column of the `cio` row in `dev/active/duty-cycle-registry.tsv`**
with the new job id and a ~7-day expiry, and **clear the parked note there** (see below). The registry
records **intended cadence, not a live job** — only the owning agent can verify it, because `CronList` is
session-scoped.

**The full fire procedure is the `duty-cycle-tick` skill** (`.claude/skills/duty-cycle-tick/SKILL.md`).
Do not reconstruct it from memory; it is versioned and has been corrected many times.

## State at stand-down — all green

| | |
|---|---|
| working tree | **clean** (only `dev/active/probe-userpromptsubmit-cio.log`, gitignored scratch) |
| unpushed | **0** — `origin/main..HEAD` empty |
| 2026-08-10 session log | **closed**, `DAY-CLOSED` marker present |
| 2026-08-11 | no fire had occurred before this notice; no work in hand, nothing parked mid-flight |
| inbox | **0** |
| freeze detector | `rc=0` at last run |

## Where the durable state lives — read these first, in this order

1. **`dev/active/cio-carry-forward.md`** — open threads, PM-attention items, watch list. **Rewritten at
   every substantive fire; current as of the 08-10 STOP.**
2. **`dev/active/cio-standing-items.md`** — durable owed/queued work.
3. **`dev/2026/08/10/2026-08-10-1037-cio-code-log.md`** — the last full day's record.
4. **`docs/briefing/ROLE-PORTFOLIO-CIO.md`** — what this lane is for (refreshed 08-07).

## ⏸ Open with PM — not to-dos, awaiting a ruling

1. **Memory-index hybrid packing.** `MEMORY.md` is at **185 lines / 178 entries / headroom 15** (`wc -l`
   convention; the generator's guard convention reads one higher, 186/14 — **state which you mean**).
   ⚠️ **Report a BOUND, not a forecast**: two full 24h cycles measured **+3 and +0**, so **≥5 days and no
   supportable upper estimate.** *(Three point estimates were issued across three days, in both
   directions, before this was clear. Do not issue a fourth.)*
   **Proposed fix**: pack the **127 of 178 self-describing slugs** (≥5-word slugs) at 4/line, keep the
   ~48 terse ones described → **185 → ~90 lines**. **Lead has offered to build the generator change on
   PM's ruling.** ⚠️ **PM's chosen option ① (denser entry text) does NOT relieve the binding limit** —
   the limit is LINES and denser text saves BYTES, which have ~28 entries of headroom.
   🛑 **NEVER delete memory files to make the index fit.** The index is derived; the files are the source;
   memory is **not under version control** and deletion is irreversible. Five agents have refused this
   correctly. Full arithmetic: `docs/internal/operations/memory-index-size-limits.md`.
2. **Innovation agenda §6** (`dev/active/cio-innovation-agenda-2026-08-02.md`) — should this lane shift
   from *building mechanisms* to *protecting a property*? Awaiting PM's read since 08-02.
3. **Short-period cron experiment** — the only way to decompose the ~30-min dispatch latency, because the
   documented `CronCreate` jitter term **saturates at 15 min on all eleven seats**. Cost stated: ~3 extra
   fires on my seat. **Not started without a yes.**

## Oldest open PM ask

**Recurring-instrument self-firing (PM, 08-07, CIO+HOST).** Evidence is in: **Role Health has a working
GitHub workflow** (I fixed a 14-minute boundary bug in it on 08-07 that had silently eaten a whole cycle
while reporting success). **Agent 360 and the skill-candidates review have NO workflow at all.** The
answer is to **copy the now-correct role-health pattern**, not design a framework —
⚠️ **and verify any clone by reading STEP-LEVEL conclusions, never the run's green tick.**

## Things others now depend on — do not silently change these

- **`scripts/cohort-freeze-detect.sh`** — PM-approved freeze monitor. **LIVE**: Pard wired it into the
  host crontab watchdog (`freeze-watchdog-amber.sh`, `46 */6`) on 08-10 and fired the positive branch in
  production. ⚠️ **The cron executes the copy in the MAIN CHECKOUT, not this worktree.** Corrected four
  times in four days (local→`origin/main` read · crash exit-code · dispatch-lag denominator · an alert
  that asserted a cause it cannot measure). Exit codes are load-bearing: **0 clear · 1 freeze · 3 cannot
  measure — a crash must never look like a finding.**
- **`.claude/skills/duty-cycle-tick/SKILL.md`** — cohort-wide. Contains PM's mail/task-loop spec
  (restored 08-07 after being flattened) and the glob-drain ban (Arch, PM-routed 08-09).
- **`CLAUDE.md`** — the **SCOPE IS NOT DIRECTION** rule (added 08-08 after a `git checkout HEAD -- <path>`
  destroyed work while complying with every existing rule).
- **`scripts/cohort-status.sh`**, **`scripts/duty-cycle-heartbeat.sh`**, **`scripts/duty-cycle-freeze-check.sh`**.

## Methodology corpus — CIO owns it

`docs/internal/development/methodology-core/`. Recent, all earned from incidents:
**m-43** right property/wrong object · **m-44** a "clear" is emitted identically whether it measured,
measured wrong, measured partially, or never ran · **m-45** agreement is not replication · **m-47** a
claim *about* a claim is still a claim (applies to your own prior work **and to retractions**) ·
**m-48** a proxy count is not the quantity (a correction count measures *attention*, not fault).

**One candidate, deliberately not filed** (needs a second instance): *a completeness check keyed on the
field that is never absent can never report incompleteness* — Comms's phrasing, 08-10.

## Standing corrections to myself, carried deliberately

- **Every significant fix I have shipped contained the defect it was written to fix, and all were caught
  by someone other than the author.** Including, on 08-10, a defect I had already fixed in a *different
  file* five days earlier — **"I already fixed this class" is precisely what stops you looking.**
- **A correction that stops at the mailbox has not happened** — it must reach the artifact.
- **Prefer a bound to a forecast.**

## Environment gotchas that cost real time

- `zsh` does **not** word-split `for f in $FILES` — use `while IFS= read -r`.
- **`shuf` does not exist** on this host — use `awk 'NR%N==k'`.
- **Backticks inside a double-quoted `git commit -m` are command substitution** — use `-F <file>`.
- **After `scripts/mail-send.sh`, run `git merge origin/main`** before counting the inbox; the drain
  lands on `main` and the worktree is behind until merged.
- **Five mail-header variants exist.** Triage with `scripts/scan-inbox.py`; **if a row shows a BLANK
  sender, that memo is unparsed regardless of the summary counter.**

— CIO, 2026-08-11 06:2x PT
