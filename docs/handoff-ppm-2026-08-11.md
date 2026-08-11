# PPM handoff — 2026-08-11 (Amber reboot, macOS 26.6)

**Role**: Principal Product Manager (PPM) · slug `ppm-code`
**Worktree**: `~/Development/piper-morgan-worktrees/ppm` (Model A) · branch `claude/ppm-cycle`
**Cron**: 🅿️ **PARKED DELIBERATELY 2026-08-11 07:20** (was `25f1a782`, `52 6,9,12,15,18,21`,
session-scoped). **`CronList` verified: no scheduled jobs.** ⚠️ **On resume it will still read zero —
that is expected and deliberate, NOT a Gap-C failure.** **Restore it from §6, which now holds the
schedule and the FULL prompt verbatim** (it previously held only a pointer to the job id, which no
longer exists).

**Written for the case where resume fails for me specifically.** A cold start can pick up from this
file plus `dev/active/ppm-carry-forward.md`.

---

## 1. Where things stand — nothing is in flight

**No work is half-done.** 2026-08-10 closed cleanly at 22:20 with its `DAY-CLOSED` sentinel; six clean
fires, fourth clean day running. **No 08-11 session had started when the notice arrived** — so there is
no open log for today and nothing parked mid-task.

**At last verification (08-10 STOP): working tree clean, 0 unpushed, 0 behind, inbox 0.**

---

## 2. 🔴 Open for PM — the only things actually waiting

1. **Bless the merged first-contact criterion** — `docs/internal/product/first-contact-criterion-merged-2026-08-10.md`. **Three items, not four.** ⛔ **Bless neither §7a as written nor #1536's ACs as written** — both had holes; the merged list is the artifact. All three items now stand on their own (item ③'s architectural block was discharged by Arch on 08-10).
2. **The (a)/(b) fork on #1510** — *does the user DEMONSTRATE the working model (inferred, months) or TELL Piper (declared, an afternoon)?* ⚠️ **Now has at least THREE consumers**: #1510 itself, #1511's standup preference, and the standup invitation's persistence. **Arch established the declared surface is safe to build under either answer**, so the fork blocks only the expensive half.
3. **Surface 1 in the 1.0 five**, and **name-or-strike Surface 3** — Surface 3 has exactly one corpus mention (`PDR-005:84`) and no name, doc, ADR or build lane. A "5 of 7" scope claim with one unidentifiable member.

---

## 3. Lanes and their state

| lane | state |
|---|---|
| **Jake FTUX conversion** | ✅ **COMPLETE.** #1536→MVP+Beta Blockers; #1537–#1540→Production/PUB (PM ruled 08-10). Register: `dev/active/jake-ftux-item-register-2026-08-08.md` — **4 filed → 9 filed, 1 held (row 5, pending Arch on tool-catalog naming), 2 preference-holds, 0 unfiled** |
| **#1511 two standups** | Spec filed on the issue; **Lead shipped the MVP slice 08-10** (name-addressable interview). **Production half** = first-run fallback + preference — ⛔ **must ride #1510's declaration surface, not grow its own store** |
| **Standup invitation design** | CXO's three properties adopted (report first/complete · invitation after and cheap to decline · **declining changes nothing else**). **My addition, sent 08-10 22:30**: the **EMPTY standup** is the exception PM named — *demonstrate-then-ask has nothing to demonstrate*, so honest-failure takes over. **Boundary caution: "empty" = genuinely nothing, NOT thin** |
| **Understanding-layer inversion** | My per-category ratchet input was **amended into Arch's ruling**. Watching only |
| **BYOC task force** | Lane taken: **a listing is honest at #1440's contract, not at a connector count.** ⚠️ **Slack cannot be listed while PM's #1481 hold stands** |
| **#1462 / PDR-006** | Production / PUB sprint (PM). CXO's #1463 retest gate is blocked on `services/mcp/server/` — **unbuilt, not undeployed** |

---

## 4. ⚠️ Standing corrections a cold start must not re-derive

- **The web UI is NOT going away.** The modeled UX is holistic, expressed per surface (phone, Slack, web, other-chat, **CLI all maintained**). *"Which surface survives"* is a **false question** — my sort key on that axis was withdrawn 08-08 after PM corrected it. **This error has been made twice; do not make it a third time.**
- **Milestone sequence**: **MVP → Production → Fast Follow.** *"Not MVP"* NEVER defaults to Fast Follow. **Production = required for PUBLIC beta**, worked in the PUB sprint. *"Out of alpha" = the PUBLIC beta.*
- **Beta moved back a month on 2026-08-08.** ⛔ **Do not carry a beta date in any prompt** — it has been wrong twice. The date is PM's.
- **Counts**: never a total without its parts. Use `scripts/sprint-truth.py` verbatim. ⚠️ **It is milestone-scoped — unmilestoned work is invisible to it by construction.** Report not-started AS not-started.
- **Proxies**: safe when the remainder is **ROUTED**, dangerous when merely **IMPLIED**. Say **"gateable fraction"**, never *"shadow"* — shadow implies substitution.
- **`mail-send.sh` can fail silently** — a transient `fetch origin/main failed` leaves the memo unsent with no other signal. **Read the tail of every send.**
- **Before re-asking PM anything: check GitHub.** Items have twice been answered by **action** rather than by answer.

---

## 5. Files a cold start should open, in order

1. `dev/active/ppm-carry-forward.md` — **the live state; read this first**
2. `dev/2026/08/10/2026-08-10-0722-ppm-code-log.md` — most recent full day
3. `docs/internal/product/first-contact-criterion-merged-2026-08-10.md` — awaiting PM
4. `dev/active/jake-ftux-item-register-2026-08-08.md` — the Jake lane, countable
5. `docs/briefing/ROLE-PORTFOLIO-PPM.md` — the portfolio §2 goals table

---

## 6. 🅿️ CRON DELIBERATELY PARKED — schedule + full prompt recorded here

**Mechanism: session-scoped `CronCreate` (`CronList` labels it `[session-only]`).** It dies with the
reboot and **leaves no trace** — so it was **cancelled deliberately at 07:20 on 2026-08-11**, per
Pard's second stand-down notice, rather than left to be killed silently.

**Two reasons it was parked rather than left running:**
1. **No scheduled fire arrives between the handoff being written and the reboot** — work done after
   this file was written would not be covered by it.
2. ⭐ **A schedule killed by a reboot is invisible afterwards.** The seat comes back looking healthy
   and quietly never fires again. **Parked-and-written-down survives; killed-and-forgotten doesn't.**

> ⚠️ **THIS SECTION IS THE ONLY COPY.** It previously said *"the prompt currently in `25f1a782`"* — a
> pointer to a job that **no longer exists.** The literal text is now inlined below, and the prompt was
> transcribed **before** the delete for exactly that reason.

### Schedule

```
52 6,9,12,15,18,21 * * *     (recurring, six fires/day)
```
First fire of the day = **START** · last (21:52) = **STOP** · all others = **WORK**.

### Prompt — restore verbatim

```
DUTY CYCLE TICK — role: PPM (Principal Product Manager), slug ppm-code.
Worktree: /Users/xian/Development/piper-morgan-worktrees/ppm (Model A, branch claude/ppm-cycle).
Cron: 52 6,9,12,15,18,21 — first fire of the day = START, last (21:52) = STOP, all others = WORK.

FIRST ACTION: emit the wake heartbeat — scripts/duty-cycle-heartbeat.sh ppm <TYPE> — passing this
fire's ACTUAL dispatch type. Check the CLOCK, not the tick order: past 21:52 is STOP even if earlier
fires were missed.

⛔ NO STANDING OWED WORK ITEM.
⚠️ RULE, earned twice: if you add an owed item here, DELETE IT THE FIRE IT COMPLETES. A stale
instruction in a prompt read six times a day is a standing order to redo finished work.

Read dev/active/ppm-carry-forward.md for current state. Then run the duty-cycle-tick skill exactly
(START / WATCH / WORK / STOP).

If SEVERAL ticks arrive stacked, that is ONE wake, not several. Run CronList: exactly one job means
the fires QUEUED, not a cron failure. A cohort-wide account freeze causes this too and is invisible
from inside a seat — do not diagnose the cause from your own vantage.

STEP 0: verify the PRIOR day's log carries its DAY-CLOSED sentinel before starting today's work.

RE-ARM RULE: at STOP, CronDelete-old THEN CronCreate-new, and verify with CronList that exactly ONE
job exists. If CronList shows ZERO at any fire, re-arm immediately and note it in the entry.

DATES: do not carry a beta date here. It has been wrong twice. Beta moved back a month 2026-08-08;
the date is PM's to set.

MILESTONE SEQUENCE (PM, 2026-08-09): MVP → Production → Fast Follow. "Not MVP" NEVER defaults to
Fast Follow. Production = required for PUBLIC beta, worked in the PUB sprint.

BEFORE RE-ASKING PM ANYTHING: check GitHub first. Items have twice been answered by ACTION not answer.

SURFACES: the web UI is NOT going away. The modeled UX is holistic, expressed per surface (phone,
Slack, web, other-chat, CLI — all maintained). "Which surface survives" is a false question.

COUNTS: never report a total without its parts. Use scripts/sprint-truth.py output verbatim. It is
milestone-scoped — unmilestoned work is invisible to it by construction.

AUDIT BIAS: when someone proposes elevating YOUR artifact, audit it before accepting. Unaudited is
not sound. Corrections are evidence of attention, not of fault.

GENERAL CONTRACTS: before citing one as closing your hole, check it actually reaches your case.

PROXIES: a proxy is safe when the remainder is ROUTED, dangerous when merely IMPLIED. Say "gateable
fraction", never "shadow" — shadow implies substitution and lets the remainder disappear.

MAIL-SEND CAN FAIL SILENTLY: a transient "fetch origin/main failed" leaves the memo unsent with no
other signal. Read the tail of every send; verify it landed before saying you sent it.
```

### On restore

**Re-arm with the above, then `CronList` to verify exactly ONE job exists.** ⛔ **Do not treat the
first post-reboot tick as evidence the schedule is armed** — a manually-delivered tick and a scheduled
fire look identical from inside the session. **Only `CronList` distinguishes them.**

---

## 7. Registry note

`dev/active/duty-cycle-registry.tsv` ppm row carries the 08-10 day-close. ⚠️ **If the reboot window
crosses a scheduled fire (06:52 or 09:52), the freeze-watchdog may see a genuine silence.** **That
silence is the reboot, not a stall** — this file is the referent.

---

**Stood down with nothing in flight.** — PPM, 2026-08-11
