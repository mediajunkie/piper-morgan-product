---
last_updated: 2026-09-28
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — refreshed 2026-09-28 at the 10:17 WORK fire.

> 🔴 **Spring-cleaned 2026-09-22 per PM's context-floor directive; kept lean since.** Resolved
> history is deleted, not archived-in-place — it lives in session logs (the durable record) and,
> for the most transferable lessons, in `docs/briefing/CXO-SUCCESSOR-READ.md`. If you're looking for
> a specific dated incident that isn't here, check the session log for that date first.

> ## 🔴 STANDING RULE — a cron job id surviving a reboot/restart is NOT evidence the event missed you
>
> `claude --resume <uuid>` restores the cron from the saved transcript regardless of whether a reboot
> happened. **Job-id continuity proves `--resume` worked, not that an infra event didn't reach you.**
> Full incident: `feedback_cron_id_continuity_not_evidence_against_reboot` (memory), 09-20/09-21 logs.

> ## 🔴 STANDING RULE — check a claim against its live source, not the summary of it
>
> **Applied both directions all week**: to others' claims about my own commit history/rubric, and to
> my own rulings before shipping them (read the actual discriminator code, the actual canonical-
> phrase table). 09-27's clearest instance: Arch's re-verification of my Phase 3 ruling found I'd
> under-scoped my own denominator — verification isn't just confirming, it's catching what the
> author didn't check.

## ✅ RESOLVED (effectively moot) — cron cadence thread, throttle window ends Tuesday

Exec ruled 09-28: "through Monday" meant all of Monday stays throttled, reverting at **Tuesday
09-29's first scheduled fire**. Docs had reverted early on a different reading and is
re-throttling to land consistently. **I never actually reduced my cadence** (blocked Friday by the
permission classifier, stayed at 6x/day the whole time) — I'm already sitting at exactly the state
everyone lands on tomorrow. **No further action needed on this thread**: not worth attempting a
same-day cadence-cut-then-immediate-revert for less than one day of runway. The fresh-session
retry plan is now moot too — normal cadence resumes tomorrow regardless of whether a fresh session
ever arrives.

## Cron

⚠️ **Re-armed 2026-09-27 22:20 PDT — job id `bcf93853`**, expression `47 6,9,12,15,18,21 * * *`
(SAME as before, cadence unchanged — see the box above). Delete-then-create from `c3b2e35b`;
`CronList` confirmed exactly one job survives. 7-day auto-expiry (~2026-10-04).

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **28 rows**, both guards clean (added the GUIDANCE ruling row
this fire). This carry-forward does not duplicate the tracker; check it for anything open. Run
**both** guards after any edit: `scripts/aging-standing-items.sh | grep '· cxo:'` (expect **28**)
**and** `awk -F'|' '/^\|/ {print NR": cols="NF-2}'` (every row must read `cols=4`).
**Edit tool only on this file — never `.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **2** (#1174, #1108), unchanged across every fire today.
#1174 routed to HOST (welfare gate), waiting; #1108's copy half is done, build unowned.

## ⚠️ Active — three Lead-owned builds queued behind rulings from this seat, none landed yet

- **#1772 residual guard** (ruled 09-25): still open, 7 comments, unchanged since the ruling.
- **Phase 3 reads-only release + corpus re-score** (ruled 09-27, concurred by Arch/PPM same day):
  must apply at BOTH discriminator sites (`todo_handlers.py`/#1654 and `first_contact.py`/#1688).
- **GUIDANCE destination rows** (ruled 09-28): 10 of 12 rows should stay as guidance (a real
  correction on the 3-row setup trio, which is guidance's own purpose-built territory, not
  `manage_portfolio` as first framed); 2 re-score. Deletion itself stays moot until a guidance wave
  is planned, per Lead's own memo — this is the baseline for when that happens, not an urgent build.

Worth a closer look at the first two if they stay quiet much longer — not urgent yet, just noting
three build-side items are now stacked behind rulings from this seat.

## Closed 2026-09-25/26/27/28 — watch only, nothing owed unless something reopens

09-25: BYOC T-axis series (rubric v0.8.2) · #1772 mechanism/copy · Ship #062 review · MCP Phase C
Q2 + rubric correction. 09-26: Pard's commit-attribution incident, verified clean twice. 09-27:
both Phase 3 rulings, concurred independently by Arch and PPM. 09-28: throttle-cadence thread
resolved as moot (see above); GUIDANCE rows ruled. Full detail in the respective session logs.

## Waiting on others — nothing owed to PM

**Nothing currently queued for PM from this seat** beyond the cron-cadence thread above, which is
already PM's fallback if a fresh-session retry fails — not a new ask. #1824's classifier owner is
Lead's open question.

## Agent 360 v0.5 — response owed within ~2 weeks, not urgent

HOST fielded v0.5 (`dev/2026/09/25/agent-360-questionnaire-v0_5.md`), new §5.6 on gate/CI-output-
checking habits from the credential-incident cluster. Tracked as a standing-items row. Answer via
memo to `mailboxes/host/inbox/` when there's something real to say — Time Lord backstop.

## ⚠️ Instrument state — read before scoring anything

- **CT rubric**: three invariants PM-ratified 08-31; criteria/branches CXO-editable. Open the file
  for its version — no version numbers in briefings.
- **C-axis**: report per bucket, never pooled. `not_applicable` = full marks at C=2; the
  C=2-clustering diagnostic applies to the `required` bucket only.
- **BYOC rubric**: v0.8.2. T split into T-own-surface (measurable, series closed 09-25) /
  T-MCP-surface (`UNMEASURED` until increment-1 infra — MCP Phase C, actively building, is that
  infra; watch for the first real chance to measure it).

## 🔴 EVERY OUTBOUND MEMO — route away from Lead by default (PM directive, 2026-09-09)

Before addressing Lead, ask whether he must **act** — if the answer is "he wrote it" rather than "he
must act on it," cc, don't address; prefer CIO/PPM/Arch as primary. This binds me, not just Exec.

## 🔴 EVERY MEMO — filename budget

Keep memo basenames **≤130 characters** (measured budget is 150; this is 20 chars of headroom). The
subject line carries the argument; the filename only has to be findable.

## Usage throttle-back — window ends Tuesday 09-29's first fire, per Exec's 09-28 ruling

Asks (2) and (3) (hold non-essential dispatches; route non-essential updates through the rollup)
still apply through end of today. Ask (1)'s status is the resolved-as-moot cron box above. Nothing
further to track here after tomorrow's first fire.

## Live threads (watch only)

Nothing beyond the tracker and the active-item boxes above. Check `cxo-standing-items.md` for
anything genuinely open — this file is ephemeral session state, not a running history.

## Briefing currency

`docs/briefing/BRIEFING-ESSENTIAL-CXO.md`'s Current Focus section refreshed 2026-09-22 per Docs'
staleness flag — items verified against GitHub/tracker where possible, three items explicitly
flagged unverified rather than guessed. Check that file directly rather than assuming this note
stays current about it.
