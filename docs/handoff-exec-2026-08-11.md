# Exec (Chief of Staff) — stand-down handoff, 2026-08-11

**Written**: 06:25 PT, ahead of Amber's ~07:30 reboot for macOS 26.6 · **Author**: the Exec session standing down
**Assumption**: resume via `claude --resume` restores this conversation. **This document exists for the case where it doesn't.** Written for a cold start, not as a summary for someone who already has the thread.

---

## 0. State at stand-down — all verified, none assumed

| | |
|---|---|
| Worktree | `~/Development/piper-morgan-worktrees/exec`, branch `claude/exec-cycle` (Model A, stable path) |
| Sync | **0 behind `origin/main`**, working tree clean |
| Yesterday's log | `dev/2026/08/10/2026-08-10-0902-exec-code-log.md` — **`DAY-CLOSED: 2026-08-10` verified** |
| Today's log | `dev/2026/08/11/2026-08-11-0621-exec-code-log.md` — open, records this stand-down |
| Cron | ⏸ **PARKED DELIBERATELY at 06:40 PT** — see §0a. Schedule to restore: **`32 8,20 * * *`**. **RE-ARM FIRST on resume.** |
| Registry row | `dev/active/duty-cycle-registry.tsv`, line `exec` — currently `active`. If the seat stays dark past a day, park it with a falsifiable clearing condition |
| Work in hand | **None.** Nothing parked mid-flight, nothing half-written |
| Inbox | **2 unread, both cc-only, deliberately not triaged** (see §4) |

## 0a. ⏸ YOUR SCHEDULE IS PARKED — restore it before anything else

**I cancelled my own duty-cycle schedule at 06:40 PT on 2026-08-11**, deliberately, before Amber's reboot. Two reasons, both from Pard's stand-down: no fire should arrive after the handoff was written (work done then isn't covered by it), and **a schedule killed by a reboot is invisible afterwards** — the seat comes back looking healthy and quietly never fires again.

**Mechanism**: session-scoped `CronCreate`. It is in-memory, never written to disk, and leaves **no trace** after the session ends. There is no file to inspect and nothing will remind you. **This paragraph is the only record.**

**Restore it as your first action on resume:**

```
CronCreate   cron: "32 8,20 * * *"   recurring: true
prompt: DUTY CYCLE TICK — Exec (Chief of Staff). Run the `duty-cycle-tick` skill and follow it
exactly. Constants: role=exec, worktree=/Users/xian/Development/piper-morgan-worktrees/exec,
branch=claude/exec-cycle, cron=32 8,20 * * *, model=Opus 5. End every fire with:
scripts/duty-cycle-heartbeat.sh exec {START|WATCH|WORK|STOP} --if-quiet
```

Then **`CronList` to verify exactly one job** — the delete-then-create discipline exists because a bare create stacks a duplicate on a job that may still be alive.

**Cadence context**: `32 8,20` is 2x/day, the run-lean throttle this role has carried since the migration hold. The pre-throttle expression is `32 6,9,12,15,18,21` (6x/day) — **do not restore that one without PM's word.** The registry row (`dev/active/duty-cycle-registry.tsv`, line `exec`) records `32 8,20` and a 13h threshold; it currently reads `active` and will be **wrong** for as long as the seat is dark. If the seat stays down beyond a day, park the row with a falsifiable clearing condition — *"clear only when a cron job is actually armed."*

**Not mine**: `com.designinproduct.janus-cycle` is the one host-level LaunchAgent on this machine. It belongs to Janus, survives the reboot on its own, and must not be touched by this seat.

## 1. Read these first, in this order

1. `dev/active/exec-carry-forward.md` — living state, rewritten each substantive fire
2. `dev/2026/08/10/2026-08-10-0902-exec-code-log.md` — yesterday in full; it was a dense day
3. `docs/internal/development/weekly-ship-process-guide.md` §canonical-cycle — **PM's ten-step weekly cycle**, the spine of this role's week
4. `.claude/skills/duty-cycle-tick/SKILL.md` — the fire procedure; follow it exactly

## 2. What this role is actually for

Cross-workstream synthesis, mailbox relay hub, Weekly Ship drafting, and — the part that matters most right now — **making PM's picture of the project honest**. PM moved beta back a month on 2026-08-08 saying *"we clearly have a lot more work still to do than anyone ever reported to me."* Most of the last week's work has been closing that gap.

**Delivery surfaces**: the attention rollup and reports go to PM as **claude.ai artifacts** (PM's explicit preference — preview pane, collection, shareable URL), with a canonical copy in `dev/active/`. Standing artifact URLs: rollup `117c1e44-5995-4488-ac50-42cb2aff43ad`, remaining-work `63344ce0-80d4-4a02-aca3-734a38732797`, weekly report `92c86a1c-3455-481a-ba4e-57a5e273e0ec`. **Republish the same file path to keep the URL.**

## 3. Open threads, in priority order

1. **#1511 standup disposition** — the report-vs-interview split. MVP disambiguation **shipped 8/10**; the Production half (first-run fallback, preference capture) is specced and **PPM owns it**. PM's own framing is the answer: *standups on demand by default; if there's nothing to report or it's never been done, go interactive.* **Nothing owed by Exec** — for the record and the rollup.
2. **The Sep 1 discovery contract — three parts still owed, and they are Exec's.** Lead pre-registered: *structural work should bend the curve down from 08-08; flat/rising at 09-01 ⇒ the hard conversation.* PM asked how we'd hold us to it. **Done**: baseline frozen at `dev/active/discovery-rate-baseline-2026-08-10.txt`; contract **amended to new-class rate** (Lead accepted — the raw rate couldn't distinguish success from PM testing less). **Still owed**: (a) a tracked issue carrying the Sep 1 date, (b) a *numeric* definition of "flat," ratified before anyone knows the answer, (c) **a named convener** — Exec offered to take it. Durable home is the recurring-task surface CIO/HOST are building.
3. **Ship #056** — kickoff Friday. **Use `draft-weekly-ship` v1.12 and follow Step 0's required kickoff wording verbatim** (PM corrected the deadline framing three times; the mechanism now lives in the skill). Ten roles get kickoffs: six leadership (progress vs. goals + milestone status) + four contributor (Lead/Docs/PA/Web — progress, setbacks, blockers; no milestone apparatus). Reports carry `sprint-truth.py` output on any progress claim.
4. **An `awaiting-decision` label** — moot at 0 unmilestoned tonight, returns with the next held item. PPM owns proposing it; it's one label from making a real distinction derivable.

## 4. The two unread memos — named so they aren't lost

Both cc-only, both from 08-10, both in `mailboxes/exec/inbox/`. **Not triaged because the stand-down said "nothing else."**

- `fifth-pa-to-host-comms-cio-cc-cohort-...-fifth-variant-confirmed-and-fixed...`
- `gap-ppm-to-cxo-lead-cc-pm-exec-...-the-EMPTY-standup-is-the-case-PM-named-and-demonstrate-then-ask-has-nothing-to-demonstrate` — **this one is substantive** and bears on thread §3.1: PPM appears to have found that demonstrate-then-ask fails for the empty-standup case, which is precisely the case PM named. Read it first.

## 5. Standing disciplines this seat has been corrected on — do not relearn these

- **Mail: a memo where you are in `to:` is read IN FULL before it moves.** cc may be skimmed for asks. Triaging by *moving* is what let a correction to Exec's own claim sit unread eight hours while PM acted on a wrong number. Detection must be format-agnostic (`^to:` frontmatter **and** `**To**:` header — 19% of memos use the latter).
- **Kickoff deadlines**: lead with *write now*; the date appears second as a nudge-threshold. Verbatim wording is in the skill.
- **Never report a bare number about sprint/backlog/roadmap.** Run `python3 scripts/sprint-truth.py` and paste its line. It has been corrected four times in four days — three by other roles — for missing truncation reconciliation, a board blind spot, the unmilestoned bucket, and a warning that fired on an empty set.
- **`gh issue view`/`gh project` is the source of truth, never a local doc.** Sourcing role-health dates from a local calendar produced a false "two months overdue" that reached PM.
- **Check whether a convenient hypothesis is the reason you believe it.** The one wrong call this seat made yesterday was the one that would have shrunk a number it was reporting.
- **Rate limits**: 5,000/hr GraphQL shared across all eleven agents. Board queries (`gh project`) exhaust it; issue queries (`gh issue`, REST) do not. `sprint-truth.py` fails loudly rather than returning a false zero — that's intended.

## 6. Mechanics

- **Mail**: `scripts/mail-send.sh "mail(exec): subject" <explicit paths>` — push-to-ref, lands on `main` directly. **Build the path list programmatically** (`git status --short -z`), never from memory.
- **Non-mail**: commit on `claude/exec-cycle`, then `git push origin HEAD:main`. On non-fast-forward: `git fetch && git rebase origin/main`, retry. **Never reuse a stale tree object.**
- **Never run destructive git in PM's main checkout** (`~/Development/piper-morgan-product`) — PM keeps uncommitted work there.
- **Janus** (cross-project hub): `~/Development/designinproduct/docs/mail/`, explicit-path adds, push to their `main`. Exec is the relay.
- **Heartbeat**: `scripts/duty-cycle-heartbeat.sh exec {START|WATCH|WORK|STOP} --if-quiet` at the end of every fire. START writes unconditionally.

## 7. If you are a cold start and resume failed

You have everything above plus ~1,100 memos in `mailboxes/exec/read/` and the full session-log history under `dev/2026/`. **The single most useful orienting move**: read yesterday's session log end to end, then run `python3 scripts/sprint-truth.py` and `python3 scripts/discovery-rate.py`. Those two commands plus that one log reconstruct the state of play faster than anything else here.

— Exec, standing down 2026-08-11 06:25 PT · **schedule parked 06:40 PT, restore per §0a**
