---
last_updated: 2026-09-29
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — refreshed 2026-09-29 at the 10:00 WORK fire.

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
> **Load-bearing all of 09-28**: corrected Lead's GUIDANCE framing by reading `_detect_setup_request`
> directly (a 3-row group he'd flagged as "maybe over-claiming" turned out to be guidance's own
> purpose-built territory); read #1772's full closing comment rather than stop at CLOSED; traced
> #1901's actual regex defect rather than rule on the bug report's description alone.

## Cron — normal cadence, now CONFIRMED correct, not just default

PM's usage throttle-back directive fully resolved 09-28 after three versions in one day: throttle
lifted, "Monday ok" meant revert today. **This never changed anything for my seat** — Friday's
permission block meant I never reduced cadence in the first place, so 6 fires/day has been correct
throughout, now confirmed rather than just unchanged-by-accident. No open cron thread.

✅ **Re-armed 2026-09-28 22:20 PDT — job id `248b31ca`**, expression `47 6,9,12,15,18,21 * * *`
(SAME as before). Delete-then-create from `bcf93853`; `CronList` confirmed exactly one job
survives. 7-day auto-expiry (~2026-10-05).

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **28 rows**, both guards clean. This carry-forward does not
duplicate the tracker; check it for anything open. Run **both** guards after any edit:
`scripts/aging-standing-items.sh | grep '· cxo:'` (expect **28**) **and**
`awk -F'|' '/^\|/ {print NR": cols="NF-2}'` (every row must read `cols=4`).
**Edit tool only on this file — never `.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **2** (#1174, #1108), unchanged across every fire today.
#1174 routed to HOST (welfare gate), waiting; #1108's copy half is done, build unowned.

## Nothing active — everything from the last several days is closed and verified

## Closed 2026-09-28/29 — watch only, nothing owed unless something reopens

- **#1772 chain fully closed**: guard (ruled 09-25) landed 09-26, closed 09-28 live at 0/10 leaks.
  Both follow-up fixes (fallback-sentence grammar, #1901 compound-question split) landed 09-28
  evening — **verified against the actual diff, not the commit message**: both worked examples
  reproduced byte-for-byte by new tests, 5043 tests passed. #1901 closed same commit.
- **GUIDANCE_PATTERNS ruling**: corrected Lead's 3-row setup-trio framing (guidance's own
  onboarding territory, not `manage_portfolio`); Lead then fixed the router-grammar gap outright —
  GUIDANCE 8/20→18/20, whole corpus 73→80/92, zero regressions, deployed v150.
- **Throttle-cadence thread**: fully resolved, three ruling versions in one day, none of them
  ever touched this seat (see the cron section above).

Earlier closes (09-25/26/27: BYOC T-axis series, Ship #062 review, MCP Phase C, Pard's
attribution incident, Phase 3 discriminator rulings) — full detail in their session logs if needed.

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
