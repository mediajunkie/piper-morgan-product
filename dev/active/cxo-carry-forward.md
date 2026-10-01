---
last_updated: 2026-10-01
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — refreshed 2026-10-01 at the 07:17 START fire.

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
> **Load-bearing both directions today**: verified HOST's claim about my own document (checked out);
> declined to assert a floor-behavior verification I hadn't actually run (CALENDAR's day-less-ask
> question), naming the gap rather than guessing to sound decisive. Saying "I didn't check this" is
> part of the discipline, not a failure of it.

## Cron

✅ **Re-armed 2026-09-30 22:30 PDT — job id `a0cf0685`**, expression `47 6,9,12,15,18,21 * * *`
(SAME as before). Delete-then-create from `8512cedb`; `CronList` confirmed exactly one job
survives. 7-day auto-expiry (~2026-10-07).

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **30 rows**, both guards clean. This carry-forward does not
duplicate the tracker; check it for anything open. Run **both** guards after any edit:
`scripts/aging-standing-items.sh | grep '· cxo:'` (expect **30**) **and**
`awk -F'|' '/^\|/ {print NR": cols="NF-2}'` (every row must read `cols=4`).
**Edit tool only on this file — never `.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **2** (#1174, #1108), unchanged across every fire today.
#1174 routed to HOST, closed (visibility gap, not real); #1108's copy half done, build unowned.

## Nothing active — CALENDAR's open question resolved this morning, board clear

## Closed recently — watch only, nothing owed unless something reopens

- **10-01: CALENDAR_QUERY_PATTERNS — fully resolved.** PPM traced static evidence (pointed toward
  "silently assumes," explicitly not the live-turn check still needed); Lead then ran the actual
  live turn — the floor never sees day-less asks, the router picks a scope. Ruled two distinct
  product questions: week-as-default for plain day-less asks is fine (true, complete, over-
  inclusive, not a false claim); a SEPARATE 5-row conflict-detection gap rules `floor`, not a week
  dump that implies a check never performed — this unblocked Lead's deletion of 52 literals today.
  Also confirmed the urgent/critical/focus family extends the attention_query ruling, and a
  TODO_QUERY row move matches 09-27's reasoning. Registered (not re-ruled over) that this week's
  Phase 3 numbers were scored on the wrong model (gpt-4o-mini vs. alpha's actual Haiku).
- **#1174** (09-30): 19-day silence check-in surfaced a visibility gap, not a real one — both
  halves had converged the same day they were filed (09-11); verified independently.
- **PRIORITY_PATTERNS** (09-30, 12 rows): 6 to `attention_query`, 1 to the write verb `prioritize`,
  1 stays `get_top_priority` (router-grammar gap), 1 re-scores to guidance, 1 pulled from the
  corpus entirely (PPM confirmed no sprint-priority feature exists). PPM independently re-verified
  all of it same evening.

Earlier closes (09-25 through 09-29: BYOC T-axis series, #1772 chain, GUIDANCE_PATTERNS, Pard's
attribution incident, Phase 3 discriminator rulings, the throttle-cadence thread) — full detail in
their respective session logs if needed.

## Waiting on others — nothing owed to PM

**Nothing currently queued for PM from this seat.** #1824's classifier owner is Lead's open
question.

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

## Live threads (watch only)

Nothing beyond the tracker and the active-item box above. Check `cxo-standing-items.md` for
anything genuinely open — this file is ephemeral session state, not a running history.

## Briefing currency

`docs/briefing/BRIEFING-ESSENTIAL-CXO.md`'s Current Focus section refreshed 2026-09-22 per Docs'
staleness flag — items verified against GitHub/tracker where possible, three items explicitly
flagged unverified rather than guessed. Check that file directly rather than assuming this note
stays current about it.
