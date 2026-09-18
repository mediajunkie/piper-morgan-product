# Wave 0 shakedown — pre-registered criteria

**Written 2026-09-18 by the Exec session that is about to be replaced, BEFORE the cold start.**

## Why this exists

The successor cannot grade itself. A session that comes back subtly wrong reports success in exactly
the same words as one that came back right — **that is m-50, and a shakedown graded by its own
subject is not a shakedown.** So the criteria are fixed here, in advance, on `origin/main`, where
**Janus, Pard and PM can check them against what the successor actually does**.

**Do not let the successor mark its own paper.** If you are the successor reading this: answer §1
from the repo before you read §2, then hand the result to someone else.

## §1 — Reconstruction, unprompted. The real test.

The successor should be able to state these **without being told, from `origin/main` alone**. Ask
open-ended ("what's in flight?"), not leading. Ungraded if the question names the answer.

1. **The sprint closeout for Sep 11–17 is out and awaiting responses**, and a synthesis is owed to PM.
2. **Which roles have replied** — and that as of this writing it is docs, comms, cio.
3. **Five roles were deliberately dark** (cio, lead, cxo, ppm, pa) and PM is waking them one-on-one,
   so their silence is the plan. *(cio has since woken — the successor noticing that is a bonus,
   not a requirement.)*
4. **The weekly-reflection proposal is with CIO**, PM-approved to draft, CIO's to ratify.
5. **The registry rule**: anyone may park any row; only the owning session may un-park its own.
6. **Fable is reserved for Lead Developer**; everyone else Opus or Sonnet.

**Pass** = 5 of 6 unprompted. **Investigate** = 3–4. **Fail, stop wave 1** = ≤2, or any confident
statement that contradicts the repo.

⚠️ **The failure mode to watch for is not blankness — it is fluent wrongness.** A successor that says
"the closeout went out Monday" or "all ten roles have replied" is worse than one that says "I don't
know yet, let me read." **Confident and wrong fails; uncertain and checking passes.**

## §2 — Mechanical checks (anyone can run these)

| # | Check | Pass |
|---|---|---|
| 1 | `CronList` | exactly one job, `38 6,10,14,18,22` |
| 2 | First scheduled fire lands a commit on `origin/main` | **see §3 for the deadline** |
| 3 | `DUTY_CYCLE_COVERAGE=1 scripts/duty-cycle-freeze-check.sh` | runs, rc=0, reports on all 11 rows |
| 4 | `amber-fleet gate` | still reads `exec GREEN` |
| 5 | Successor's first substantive act | **not** a re-derivation of what the carry-forward already says |

## §3 — The deadline, computed now so "hasn't fired yet" is falsifiable

Exec's cron is `38 6,10,14,18,22`. **Whatever hour the cold start happens, the next fire is the next
of 06:38 / 10:38 / 14:38 / 18:38 / 22:38, plus up to ~10% jitter.**

**Write the specific expected time down at the moment of the restart.** Without it, *"it hasn't fired
yet"* and *"it will never fire again"* are the same observation — which is the exact ambiguity that
makes this whole exercise necessary, and Exec's cadence is not the fleet's worst case (CIO fires
3×/day at 10/16/22, a window up to six hours wide).

**If the deadline passes with no commit: that is a failure, not a slow morning.** Do not wave it
through. The predecessor's instruction is to stop wave 1 and investigate.

## §4 — What this does NOT test

- **It tests one seat.** It says nothing about eleven seats restarting together, contention, or
  ordering. Janus is right that one seat is enough to learn the process is broken; **it is not enough
  to learn the process is sound at fleet scale.**
- **It tests a cold start on a RUNNING Amber, not a reboot.** Janus's decoupling is deliberate and
  good — one cause at a time — but it means **wave 0 passing does not clear the reboot path.**
- **It cannot detect damage, only death** (see the belt note below). A seat that comes back *wrong*
  passes every mechanical check in §2. §1 is the only part that can catch it, and it needs a human.

## §5 — The belt as post-restart verification: yes for death, no for damage

**The mechanism exists today and needs no new code**: park every row before the restart; each seat
un-parks its own **only after `CronList`-verifying its cron**, which is a thing no peer and no script
can do on its behalf. **The registry then IS the verification ledger** — a row still parked past its
own computed deadline is a seat that never came back. Nobody performs 24 checks; you read which rows
are still parked. We exercised the parking half on 09-16 and the un-parking half this morning.

**Three things it needs:**
1. Rows parked *before* the restart. A parked row is the null hypothesis; an un-parked one is a claim.
2. **`scripts/sync-pm-local.sh` after any push** — the freeze-check reads the registry from PM's local
   checkout, so a push alone does not change what the instrument sees. This cost me a false STALE
   reading this morning and it will cost the next person the same one.
3. Per-seat deadlines computed in advance (§3), or every early check reads as a failure and every
   late one as fine.

**The limit, stated plainly: a seat that comes back subtly wrong un-parks itself exactly like a
healthy one.** The belt measures whether a session is alive and committing. It cannot measure whether
it is *oriented*. That gap is what §1 is for, and §1 is not automatable.
