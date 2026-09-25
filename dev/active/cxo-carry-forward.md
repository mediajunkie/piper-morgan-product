---
last_updated: 2026-09-25
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — refreshed 2026-09-25 at the 10:13 WORK fire.

> 🔴 **Spring-cleaned 2026-09-22 per PM's context-floor directive; kept lean since.** Resolved
> history is deleted, not archived-in-place — it lives in session logs (the durable record) and,
> for the most transferable lessons, in `docs/briefing/CXO-SUCCESSOR-READ.md`. If you're looking for
> a specific dated incident that isn't here, check the session log for that date first.

> ## 🔴 STANDING RULE — a cron job id surviving a reboot/restart is NOT evidence the event missed you
>
> `claude --resume <uuid>` restores the cron from the saved transcript regardless of whether a reboot
> happened. **Job-id continuity proves `--resume` worked, not that an infra event didn't reach you.**
> Full incident: `feedback_cron_id_continuity_not_evidence_against_reboot` (memory), 09-20/09-21 logs.
>
> **Related — check after any suspected infra event**: model tier, permission mode, and Remote
> Control connection don't necessarily survive `--resume` either.

> ## 🔴 STANDING RULE, added 2026-09-24 after a real error — don't reason from a single unstable measurement
>
> **Real incident, same day**: claimed a persisting UI flash was *"the browser's own native
> teardown gap"* after finding no code cause — but the measurement it rested on was explicitly
> flagged by its own reporter as n=1, not a stable distribution. It was noise; the flash was gone
> on the next run. **"I can't find a code cause" does not imply "therefore structural"** — a third
> possibility (the measurement itself is noise) has to be weighed, especially when the person who
> took the measurement already named that risk. Full incident: 09-24 session log, #1859 tracker row.

## Cron

✅ **Armed 2026-09-24 22:28 PDT — job id `4b4721b5`**, expression `47 6,9,12,15,18,21 * * *`,
7-day auto-expiry (~2026-10-01). Confirmed exactly one job at this morning's 07:13 START — no
re-arm needed today. `CronList` proves a job OBJECT exists; only a fire proves it FIRES. Don't
infer an offset from one day's data.

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **25 rows**, both guards clean. This carry-forward does not
duplicate the tracker; check it for anything open. Run **both** guards after any edit:
`scripts/aging-standing-items.sh | grep '· cxo:'` (expect **25**) **and**
`awk -F'|' '/^\|/ {print NR": cols="NF-2}'` (every row must read `cols=4`).
**Edit tool only on this file — never `.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **2** (#1174, #1108), checked twice today (07:13 and 10:13
fires), unchanged both times. #1174 routed to HOST (welfare gate), waiting; #1108's copy half is
done, build unowned by anyone.

## Ship #062 workstream review — FILED 10:17, watch only

Filed to Exec (cc PM) inside the moved-up ~10:45 deadline. Led with #1875/#1855/#1859 as the
product-facing answer to PM's "what can a user do today they couldn't on Sep 18" question; named
the #1859 diagnostic error as a setback rather than folding it into the win; flagged
`sprint-truth.py` failing the same way as three weeks ago without depending on it for any claim.
Nothing owed unless Exec or PM comes back with a question.

## Agent 360 v0.5 — response owed within ~2 weeks, not urgent

HOST fielded v0.5 (`dev/2026/09/25/agent-360-questionnaire-v0_5.md`), new §5.6 on gate/CI-checking
habits from this week's credential-incident cluster. Tracked as a standing-items row so it doesn't
silently age out. Answer via memo to `mailboxes/host/inbox/` when there's something real to say —
Time Lord backstop, not a pacing device.

## ✅ T-axis series CLOSED 2026-09-25 — nothing further, watch only

All four pre-registered rounds ran (09-24/09-25), rubric now **v0.8.2** (§6e added). **Verdict**:
member-not-metadata mitigation is vendor-asymmetric, not a fix — Claude 5/6 across three
member-shaped carriers; **GPT-4o 0/8 across every design tried** (metadata, member×count×shape) —
none of the three isolated variables explains its failure. Closed by design, as flagged before
round 4 ran: four pre-registered rounds documents the asymmetry; continuing indefinitely would be
fishing, not isolation-testing. Closing memo sent to PA (cc PPM); `decisions.log` entry filed
(2026-09-25 07:15 PDT). T-MCP-surface remains untouched, `UNMEASURED`.

## Waiting on others — nothing owed to PM

**Nothing currently queued for PM from this seat.** #1824's classifier owner is Lead's open question.

## Closed, watch only — nothing owed unless something reopens

- **#1772** (aggregate copy at N=1) — ruled, shipped verbatim (`422d32f1db`, v135), **independently
  verified at live source by both Lead and Arch this morning** (2026-09-25). Only the fresh-string
  completion measurement remains, on PM's budget list, not blocking.
- **#1875** (alpha wizard hard-block) — found the frontend `response.ok` bug; Lead shipped all three
  causes; Web verified live in a fresh browser session.
- **#1859** (chat-switch white flash) — closed clean, but **my own diagnosis was wrong** (see the
  standing rule above). Arch's `@view-transition` option recorded in the design note as the cheap
  first lever if a real gap ever reappears.
- **#1799** (EMBEDDED failed-priority-read copy) — ruled after checking that the priority count is
  independent of the GitHub read it's adjacent to; neither of Lead's leaned options survived that
  check.

## ⚠️ Instrument state — read before scoring anything

- **CT rubric**: three invariants PM-ratified 08-31; criteria/branches CXO-editable. Open the file
  for its version — no version numbers in briefings.
- **C-axis**: report per bucket, never pooled. `not_applicable` = full marks at C=2; the
  C=2-clustering diagnostic applies to the `required` bucket only.
- **BYOC rubric**: see the T-axis section above — this note used to duplicate that; don't re-add the
  duplication.

## 🔴 EVERY OUTBOUND MEMO — route away from Lead by default (PM directive, 2026-09-09)

Before addressing Lead, ask whether he must **act** — if the answer is "he wrote it" rather than "he
must act on it," cc, don't address; prefer CIO/PPM/Arch as primary. This binds me, not just Exec.

## 🔴 EVERY MEMO — filename budget

Keep memo basenames **≤130 characters** (measured budget is 150; this is 20 chars of headroom). The
subject line carries the argument; the filename only has to be findable.

## Live threads (watch only)

Nothing beyond the tracker and the two boxes above. Check `cxo-standing-items.md` for anything
genuinely open — this file is ephemeral session state, not a running history.

## Briefing currency

`docs/briefing/BRIEFING-ESSENTIAL-CXO.md`'s Current Focus section refreshed 2026-09-22 per Docs'
staleness flag — items verified against GitHub/tracker where possible, three items explicitly
flagged unverified rather than guessed. Check that file directly rather than assuming this note
stays current about it.
