---
last_updated: 2026-10-02
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — refreshed 2026-10-02 at DAY-CLOSE (22:17 fire).

> 🔴 **Spring-cleaned 2026-09-22 per PM's context-floor directive; kept lean since.** Resolved
> history is deleted, not archived-in-place — it lives in session logs (the durable record) and,
> for the most transferable lessons, in `docs/briefing/CXO-SUCCESSOR-READ.md`. If you're looking for
> a specific dated incident that isn't here, check the session log for that date first.

> ## 🔴 STANDING RULE — emit the per-fire heartbeat before ending every fire
>
> Run `scripts/duty-cycle-heartbeat.sh cxo {fire-type} --if-quiet` as the second-to-last action
> every fire, right before the carry-forward refresh. Fixed 10-02 after going an entire day (10-01)
> without ever running it. Memory: `feedback_emit_heartbeat_every_fire_before_finishing`. CIO's
> post-commit-hook pilot may eventually remove the need for this; "no action for you" until then.

> ## 🔴 STANDING RULE — triage destination is `mailboxes/{role}/read/`, NEVER `mailboxes/{role}/inbox/read/`
>
> `feedback_mailbox_read_is_top_level_not_nested_in_inbox`.

> ## 🔴 STANDING RULE — after `mail-send.sh`, a local `ls` can look reverted; merge before trusting it
>
> `feedback_mail_send_reconcile_resets_to_local_head_not_origin_main`.

> ## 🔴 STANDING RULE — check a claim against its live source, not the summary of it
>
> Load-bearing every day this week. Today's sharpest instance: conceded D1 to PPM only after
> reading the handler source myself (`intent_service.py:8617-8650`), not on citation trust in either
> direction.

## Cron

✅ **Re-armed 2026-10-02 22:2x PDT — job id `c006bc0e`**, expression `47 6,9,12,15,18,21 * * *`
(SAME as before). Delete-then-create from `2fa6cb13`; `CronList` confirmed exactly one job survives.
7-day auto-expiry (~2026-10-09) — re-arm proactively on or before that date.

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **38 rows**, both guards clean. Run **both** after any edit:
`scripts/aging-standing-items.sh | grep '· cxo:'` (expect **38**) **and** `awk -F'|' '/^\|/ {print
NR": cols="NF-2}'` (every row must read `cols=4`). **Edit tool only — never `.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **3** (#1911, #1174, #1108), stable all day, re-checked many
times. #1174 is a discovery thread, genuinely OPEN by design. #1108's copy half done, build unowned.

## Active — design closed, builds in flight (not mine to push forward)

- **#1911 + #1918** — combined design spec delivered 10-02, posted to both issues, PA building.
  Nothing owed from me unless the build surfaces a question.
- **#1899 armed-carrier write-erosion** — ruled, Lead accepted verbatim, tracked as #1920, building.
  Will probe "never mind" empirically before adding a special case.
- **`read_floor` mechanism** — built by Lead (5 ops, not flipped), Phase-2 gate clean. A real
  router-coverage gap found (TRUST 0/10 once declines count honestly) — Lead sharpening registry
  descriptions tomorrow. **The flip itself is PM's hand, deferred — PM was unwell 10-02.** Nothing
  for me to do; read-only.

## Closed/corrected today (10-02) — watch only, nothing owed unless something reopens

- **#1911 + #1918 combined design pass — DELIVERED.** Full spec:
  `docs/internal/design/mcp-consent-and-connected-apps-2026-10-02.md`.
- **Ship #063 workstream review** — drafted (forked), verified, sent to `mailboxes/exec/inbox/`.
- **A real procedural gap found and fixed**: the per-fire heartbeat (see standing rule above).
- **#1606 closed** (Lead) — CXO's confirm-copy ownership held through the build.
- **#1899 armed-carrier write-erosion — RULED.**
- **DISCOVERY/TRUST/ANALYSIS/MEMORY 13-row addendum — RULED, then CORRECTED same day.** PPM caught
  a real error in the D1 row (`session_activity_query` is keyed to the current session only — a
  prior-session question there produces a confident wrong answer, not an honest one). Checked the
  source myself, conceded in full. **Net: 12 of 13 agreed with PPM**, not my original 8/13 read —
  the correction matters more than the count; read the standing-items row for the full reasoning if
  this ever needs re-litigating.
- **Arch's `read_floor` ruling**: read-only. YES to rail entries, not a consult branch, gated behind
  the Phase-2 per-category gate.

## Waiting on others — nothing owed to PM

**Nothing currently queued for PM from this seat.** #1824's classifier owner is Lead's open
question. Note: PM was unwell 10-02 — don't expect the `read_floor` flip or anything else needing
PM's hand to move until that clears.

## Agent 360 v0.5 — response owed within ~2 weeks, not urgent

HOST fielded v0.5 (`dev/2026/09/25/agent-360-questionnaire-v0_5.md`). Tracked as a standing-items
row. Answer via memo to `mailboxes/host/inbox/` when there's something real to say.

## ⚠️ Instrument state — read before scoring anything

- **CT rubric**: three invariants PM-ratified 08-31; criteria/branches CXO-editable.
- **C-axis**: report per bucket, never pooled. `not_applicable` = full marks at C=2.
- **BYOC rubric**: v0.8.2. T-own-surface measurable (series closed 09-25); T-MCP-surface
  `UNMEASURED` until increment-1 infra.

## 🔴 EVERY OUTBOUND MEMO — route away from Lead by default (PM directive, 2026-09-09)

Before addressing Lead, ask whether he must **act** — if the answer is "he wrote it" rather than "he
must act on it," cc, don't address; prefer CIO/PPM/Arch as primary.

## 🔴 EVERY MEMO — filename budget

Keep memo basenames **≤130 characters**. The subject line carries the argument.

## Briefing currency

`docs/briefing/BRIEFING-ESSENTIAL-CXO.md`'s Current Focus section refreshed 2026-09-22 per Docs'
staleness flag. Check that file directly rather than assuming this note stays current about it.
