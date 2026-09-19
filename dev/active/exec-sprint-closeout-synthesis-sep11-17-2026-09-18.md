# Sprint closeout synthesis — week of Sep 11–17

**Exec, 2026-09-18.** All **10 of 10** roles filed. Nine report on track; one reports not, deliberately.

**Denominator**: `sprint-truth.py`, run fresh at compile: `MVP: 56 not done (33 Sprint Backlog, 3 In
Progress, 6 In Review, 14 Product Backlog); 1176 done. PLUS 0 unmilestoned. 33 NOT STARTED.`
Nothing moved on the board during the 09-16→09-18 standdown, which checks out. **42 days to 30 Oct.**

---

## The one thing to take away

**The week's constraint was not throughput. It was decision bandwidth — yours.**

Nine of ten roles carry at least one item waiting on you. Lead is the only exception, and Lead is the
one who shipped ~45 issues. The others aren't short of work; they're holding at a gate.

| role | waiting on you | since |
|---|---|---|
| Arch | scope-guard delivery (#1744) · Q5 · Bets 001–003 | 09-10 · 09-11 · 08-30 |
| Web | Vercel access · website#35 · a workDate you'd recall | 09-09 · 09-12 · 09-09 |
| HOST | Janne's invite — ready, unsent | 09-15 |
| PPM | epics 9/10: keep, or revert to a short list | 09-14 |
| PA | T1 reply | **09-03 — fifteen days** |
| CIO | cron→LaunchAgent: cost + provisioning | 09-10 |
| Comms | 9–10 drafts queued on your voice pass | ongoing |
| CXO | `PIPER_FTUX_INTERVIEW` (actually PPM's to lift) | 09-03 |
| Exec | ruleset ruling · #1747 · memory-export cadence | 09-10 |
| **Lead** | **nothing** | — |

**Four of those had never reached an attention board.** That is my routing failure, traced and
partly fixed today; the causes are in the board's own §"Why these were missed."

---

## What actually got done

**The alpha gate held under real pressure, and that is the week's most consequential outcome.**
Janne Lammi is our first real external tester. The invite was cleared 09-13, held when #1810
surfaced, **re-held 09-15 when #1814 landed directly on the invite's own first instruction** — it
tells him to configure his key, and #1814 was the wall he'd have hit doing exactly that. Both holds
cleared on **observed, driven flows, never a test pin** — a bar HOST set, Arch tried once to lower,
HOST refused, and Arch conceded same-day. Lead supplied the observations both times.

**We caught a tester-facing blocker before the tester did.** That is the system working at the only
moment it matters.

**Lead's week**: ~45 issues closed, all verified at a named layer; the BYOC key chain done end to end
(#1807/#1810/#1814/#1815/#1816); the belt from five unexplained reds to zero; **E2E green for the
first time in its recorded history**; both credential rotations.

**Others**: epic 2 reopened on your override and run to six more closures under live stakes (PPM);
four published posts each with a real independent catch (Docs); the Aug 10–18 narrative gap found
and fully drafted, plus a mechanical safeguard that caught a real miss on its first use (Comms); the
WYSIWYG toggle shipped, its P0 regression caused and fixed same-day, and the missing test net built
(Web); m-53 and m-54 filed, `duty-cycle-tick` to v1.35 (CIO); ESSENCE enforcement now roughly
half-built — three ratchets live (Arch).

---

## Three themes worth your attention

### 1. Self-correction is running unusually well, and it is the strongest signal in the ten

Nearly every closeout contains its author correcting themselves, unprompted:

- **CXO chose to report their unhealthy goal** rather than a healthy one, and said so in the subject
  line.
- **Web led with having caused the worst bug in their own surface** — a caret regression that
  reversed every typed character and corrupted your draft text — before describing the fix.
- **HOST** corrected a colleague's error, then corrected *their own report* of that correction.
- **CIO** found a false claim in its own registry row and fixed it against its own committed log.
- **PPM** had epic 12 overruled by you and owned the call publicly rather than defending it.
- **PA** found 30 of their own memos in the wrong mailbox path and fixed them same-day.
- **Arch** conceded twice to Lead, and named the general shape rather than just the instance.

**Nobody had to catch most of these.** A cohort that self-reports its own errors is worth more than
one that reports clean weeks, and this is the clearest week of it we've had.

### 2. Verification discipline held when the instruments failed

**CXO's and PA's `sprint-truth.py` runs both failed** — a GraphQL rate limit and a board-query error.
Neither invented a number. Both quoted my line **and attributed it to me**, and both stated plainly
that they were making no completeness claim. CXO quoted the script's own warning: *"This check
measured NOTHING — do not read its silence as a clear."*

That is m-44 working exactly as designed, twice, independently, under time pressure.

### 3. Rulings are outpacing mechanisms — and I measured how badly

Arch names this about their own lane unprompted: two conditions they set this week exist as prose in
memos rather than as ratchets. CIO carries four standing items described as *"genuinely open,
unblocked, carried forward — not stalled, just not yet scheduled"*; two are 132 and 26 days old.

I measured the general case today, after you asked whether we actually fix routing issues as we
detect them: **29 check-shaped scripts in `scripts/`, and the ones that catch this class —
`aging-standing-items.sh`, `duty-cycle-freeze-check.sh`, `check-refresh-promises.py` — are wired into
CI zero times and into hooks zero times.** They fire only when an agent chooses to run them.

**We build the detector and then route its invocation through prose.** That is a bolt-on in m-53's
terms, and it is the mechanism behind most of this week's routing misses.

---

## What didn't move, by the roles' own accounting

- **CXO's T axis** — `PENDING-PROBE`, cannot issue a pass, and **ESSENCE commitment 7 is ratified law
  that cites it.** The probe's window is open only while #1688's MCP arm has no build commits.
  *(Live update: PA has since run it — six runs, one fire, did not reproduce #1717. CXO and PA are
  mid-exchange; this may close between them.)*
- **Production observation** — CXO reports three separate times this week their work ended at
  *"nobody can see this in prod."* Worth watching as a pattern, not an incident.
- **Arch's epic-6 provenance threading** — awaiting a board turn, correctly.
- ~~**Lead's usage-per-account capture** owed to Dispatch — taken 09-15, nothing written~~ →
  ✅ **CLEARED 2026-09-19**: written (`dev/active/usage-per-account-capture-2026-09-19.md`), Dispatch
  copy dropped, and the one Dispatch-answerable question called out. Shape: append-only daily TSV per
  account, **written from OUTSIDE the seat fleet** — a ceiling-refused seat cannot self-report, the
  same watcher-outside-the-frozen-set argument as the freeze-watchdog. **Two unknowns are PM's, not
  Lead's**: the seat→account mapping, and where the authoritative number is read.
- ~~**Docs' routing-memo offer to Lead** from 09-13 — still unanswered~~ → ⚠️ **I had the recipient
  wrong. Docs corrected it 2026-09-19: the 09-13 offer was to PM, not to Lead, and nothing is
  missing.** My row implied Lead was sitting on something they were never sent. Corrected here
  rather than left to stand, since the synthesis is the artifact PM reads.
- **Two days of the window** — the standdown and the account ceiling before it. Real, and it cost PA
  and CXO most of their week.

---

## What I'd do next

1. **Drain the decision queue.** Four of the five blockers take under a minute each. The queue is
   the constraint; adding capacity to a constrained system doesn't raise output.
2. **Send Janne's invite**, or say what's missing. It's been ready three days and the technical
   blocker is verifiably cleared.
3. **Decide whether Ship #061 exists.** It would cover this exact week and **has no calendar row.**
4. **Rule on the ruleset**, because it parks three roles at once and it's the only item here that
   needs real thought rather than a sentence.

**Verified how**: all ten closeouts read in full from `mailboxes/exec/` at 15:0x–15:1x today, not
summarized from a prior pass. The PM-gated table is built from each role's own §4, cross-checked
against `decisions.log` and each recipient's `sent/` — **and one item (PA's BYOC sequencing) was
struck after PA's closeout showed you had answered it in conversation on 09-15, which none of those
three surfaces records.** The wiring counts are `grep -rl` over `.github/workflows/`,
`.claude/settings.json` and `.claude/hooks/`. Milestone line from `sprint-truth.py` at compile time.
**Layer: self-reported closeouts plus my own verification of the PM-gated half. I did not
independently verify each role's portfolio claims** — 10 lanes is beyond what one pass can check, and
I'd rather name that than imply coverage I don't have.
