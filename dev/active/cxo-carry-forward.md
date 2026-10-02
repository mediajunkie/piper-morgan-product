---
last_updated: 2026-10-01
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — refreshed 2026-10-01 at the 19:17 WORK fire.

> 🔴 **Spring-cleaned 2026-09-22 per PM's context-floor directive; kept lean since.** Resolved
> history is deleted, not archived-in-place — it lives in session logs (the durable record) and,
> for the most transferable lessons, in `docs/briefing/CXO-SUCCESSOR-READ.md`. If you're looking for
> a specific dated incident that isn't here, check the session log for that date first.

> ## 🔴 NEW STANDING RULE (19:17 fire, own mistake) — triage destination is `mailboxes/{role}/read/`, NEVER `mailboxes/{role}/inbox/read/`
>
> **This exact defect recurred on ME today** — I'd personally run the 09-11 cohort sweep that found
> PPM's and PA's instances of it, had the memory loaded, and still created
> `mailboxes/cxo/inbox/read/` twice this session (16:24, 16:28 sends, 8 files). Docs caught it via
> the mailbox-nesting lint going red and repaired it. **Memory alone didn't stop the habit — if
> you're about to run `mkdir -p mailboxes/{role}/inbox/read`, STOP, that mkdir is the tell.** The
> correct destination has exactly two path segments after `mailboxes/{role}/`: `read/<name>`. Verify
> with `ls mailboxes/cxo/read/ | grep <name>` after every triage move this session, not just the
> first one. Memory updated: `feedback_mailbox_read_is_top_level_not_nested_in_inbox`.

> ## 🔴 STANDING RULE — a cron job id surviving a reboot/restart is NOT evidence the event missed you
>
> `claude --resume <uuid>` restores the cron from the saved transcript regardless of whether a reboot
> happened. **Job-id continuity proves `--resume` worked, not that an infra event didn't reach you.**
> Full incident: `feedback_cron_id_continuity_not_evidence_against_reboot` (memory), 09-20/09-21 logs.

> ## 🔴 STANDING RULE — check a claim against its live source, not the summary of it
>
> **Load-bearing all week**: GITHUB/STATUS rulings turned on reading handler docstrings directly,
> not picking between names offered. Saying "I didn't check this" is part of the discipline, not a
> failure of it.

## Cron

✅ **Re-armed 2026-09-30 22:30 PDT — job id `a0cf0685`**, expression `47 6,9,12,15,18,21 * * *`.
7-day auto-expiry ~2026-10-07 — re-arm proactively on or before that date, don't wait to discover
absence. Next fire 21:47 PDT is **today's last scheduled fire — STOP sequence applies.**

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **35 rows**, both guards clean. Run **both** after any edit:
`scripts/aging-standing-items.sh | grep '· cxo:'` (expect **35**) **and** `awk -F'|' '/^\|/ {print
NR": cols="NF-2}'` (every row must read `cols=4`). **Edit tool only — never `.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **3** (#1911, #1174, #1108), re-checked twice this fire, no new
issues. #1911 is the active design assignment (below). #1174 is a discovery thread, genuinely OPEN
by design (pre-beta). #1108's copy half done, build unowned.

## ⚠️ Active — #1911 MCP OAuth consent page, full design pass still owed

PM routed the MCP consent page's design to me (copy via Comms). **Two truthfulness rulings closed on
the copy side**: (1) drop the unverifiable "revoke at any time" promise — shipped. (2) "cannot see
another person's data" — KEEP, re-check the moment EITHER #1458 (cross-caller isolation, still OPEN)
closes OR a second real caller is onboarded. **The full page design is still explicitly deferred to
a dedicated pass this week**, named trigger (genuinely deep, render-sensitive, first-tester-facing
screen), not a quiet "I'll get to it."

## Closed recently — watch only, nothing owed unless something reopens

- **10-01 (19:17 fire): #1916 (Calendar Connect: honest pre-OAuth-wall copy + started-never-returned
  tracking) — copy delivered as a GH comment, build queued after #1595's 4b unit.** Reviewed PM's
  own draft strings for honesty before shipping: kept the Internal-mode notice (verified accurate
  against Internal OAuth publishing restrictions); split the External-mode sentence (buried "who to
  ask" inside "why it recurs weekly"); named the started-never-returned failure shape explicitly
  instead of an unexplained "that's us, not you."
- **10-01 (19:17 fire): Lead applied all 19 rows from the two 16:2x rulings same evening.**
  GITHUB_QUERY_PATTERNS now reads **GO** (66 OK/0 FAIL, deletion deferred to a fresh session).
  STATUS_PATTERNS 48 OK/3 FAIL (router-grammar, Lead's lane). Filed #1917 (PRs-needing-review gap,
  my ruling verbatim). **Watch for tomorrow**: the served router still names `attention_query` for 5
  of 6 ownership asks despite my `floor` ruling (it's a live read, so it dispatches today) — Lead
  will sharpen the registry description, not mine to fix.
- **10-01 (16:17 fire): GITHUB's last 3 rows + STATUS_PATTERNS 14-row addendum — ruled, PPM
  concurred** (conceding their own independent `attention_query` ruling on Family B after seeing
  mine — ownership question, not an urgency aggregate).
- **10-01: Phase 3 day bundle (1606, GITHUB's first 8, TEMPORAL) + Slack's keyless refusal +
  CALENDAR_QUERY_PATTERNS** — all ruled and PPM-confirmed earlier today. Full detail in today's
  session log if needed.
- **CIO's NO-DAY-CLOSE streak detector (K=3) shipped 10-01**, sized on real data per my own 09-11
  condition. Read-only for me.
- **4b floor-element plan extension (Arch/Lead, 10-01)**: read-only. CXO's confirm-copy ownership
  explicitly preserved. Lead builds next session.
- **#1174** (09-30), **PRIORITY_PATTERNS** (09-30, 12 rows) — both closed, PPM-verified.

Earlier closes (09-19 through 09-29: BYOC T-axis series, #1772 chain, GUIDANCE_PATTERNS, Pard's
attribution incident, Phase 3 discriminator rulings) — full detail in their session logs if needed.

## Waiting on others — nothing owed to PM

**Nothing currently queued for PM from this seat.** #1824's classifier owner is Lead's open
question.

## Agent 360 v0.5 — response owed within ~2 weeks, not urgent

HOST fielded v0.5 (`dev/2026/09/25/agent-360-questionnaire-v0_5.md`), new §5.6 on gate/CI-output-
checking habits. Tracked as a standing-items row. Answer via memo to `mailboxes/host/inbox/` when
there's something real to say.

## ⚠️ Instrument state — read before scoring anything

- **CT rubric**: three invariants PM-ratified 08-31; criteria/branches CXO-editable.
- **C-axis**: report per bucket, never pooled. `not_applicable` = full marks at C=2.
- **BYOC rubric**: v0.8.2. T-own-surface measurable (series closed 09-25); T-MCP-surface
  `UNMEASURED` until increment-1 infra (MCP Phase C, actively building).

## 🔴 EVERY OUTBOUND MEMO — route away from Lead by default (PM directive, 2026-09-09)

Before addressing Lead, ask whether he must **act** — if the answer is "he wrote it" rather than "he
must act on it," cc, don't address; prefer CIO/PPM/Arch as primary.

## 🔴 EVERY MEMO — filename budget

Keep memo basenames **≤130 characters**. The subject line carries the argument.

## Briefing currency

`docs/briefing/BRIEFING-ESSENTIAL-CXO.md`'s Current Focus section refreshed 2026-09-22 per Docs'
staleness flag. Check that file directly rather than assuming this note stays current about it.
