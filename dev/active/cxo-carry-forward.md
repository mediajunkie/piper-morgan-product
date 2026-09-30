---
last_updated: 2026-09-30
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — refreshed 2026-09-30 at the 07:17 START fire.

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
> Reinforced 09-29: verified Lead's landed fix against the actual diff rather than the closing
> commit message — both matched, but the discipline is to check even when the outcome is likely
> fine, not just when something feels off.

## Cron

✅ **Re-armed 2026-09-29 22:19 PDT — job id `8512cedb`**, expression `47 6,9,12,15,18,21 * * *`
(SAME as before). Delete-then-create from `248b31ca`; `CronList` confirmed exactly one job
survives. 7-day auto-expiry (~2026-10-06). Normal cadence, unresisted since the throttle directive
resolved 09-28.

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **28 rows**, both guards clean, unchanged today. This
carry-forward does not duplicate the tracker; check it for anything open. Run **both** guards after
any edit: `scripts/aging-standing-items.sh | grep '· cxo:'` (expect **28**) **and**
`awk -F'|' '/^\|/ {print NR": cols="NF-2}'` (every row must read `cols=4`).
**Edit tool only on this file — never `.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **2** (#1174, #1108), unchanged across every fire today and
yesterday. #1174 routed to HOST (welfare gate), waiting; #1108's copy half is done, build unowned.

## ⚠️ Active — #1174 check-in sent to HOST, 09-30

Opened both criteria-line issues directly rather than keep noting "unchanged." #1174: 19 days
silent (last comment 09-11, mine; nothing in HOST's own logs since 09-12) — sent a respectful
check-in, no deadline imposed, "still queued" is a fine answer. Watch for a reply; re-check if
another 1-2 weeks pass silent. #1108: different shape — my copy half is done, remaining build is
explicitly unowned/Fast-Follow, not blocked on a specific person; no action needed there.

## Closed recently — watch only, nothing owed unless something reopens

09-28/29: #1772 chain fully closed (guard live at 0/10 leaks; fallback-sentence grammar and
#1901's compound-question split both landed 09-28 evening, verified against the actual diff
09-29) · GUIDANCE_PATTERNS ruling (corrected Lead's setup-trio framing, router-grammar fix lifted
the corpus 73→80/92) · throttle-cadence thread (fully resolved, never touched this seat). Full
detail in the respective session logs if needed.

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

Nothing beyond the tracker above. Check `cxo-standing-items.md` for anything genuinely open — this
file is ephemeral session state, not a running history.

## Briefing currency

`docs/briefing/BRIEFING-ESSENTIAL-CXO.md`'s Current Focus section refreshed 2026-09-22 per Docs'
staleness flag — items verified against GitHub/tracker where possible, three items explicitly
flagged unverified rather than guessed. Check that file directly rather than assuming this note
stays current about it.
