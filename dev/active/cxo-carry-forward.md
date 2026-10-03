---
last_updated: 2026-10-03
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — refreshed 2026-10-03 at the 07:17 START fire.

> 🔴 **Spring-cleaned 2026-09-22 per PM's context-floor directive; kept lean since.** Resolved
> history is deleted, not archived-in-place — it lives in session logs (the durable record) and,
> for the most transferable lessons, in `docs/briefing/CXO-SUCCESSOR-READ.md`. If you're looking for
> a specific dated incident that isn't here, check the session log for that date first.

> ## 🔴 STANDING RULE — emit the per-fire heartbeat before ending every fire
>
> Run `scripts/duty-cycle-heartbeat.sh cxo {fire-type} --if-quiet` as the second-to-last action
> every fire. **Third instance of this exact miss this week** (me 10-01, Lead 10-02, Docs 10-03) —
> all on seats not covered by CIO's post-commit-hook pilot. Memory:
> `feedback_emit_heartbeat_every_fire_before_finishing`.

> ## 🔴 STANDING RULE — triage destination is `mailboxes/{role}/read/`, NEVER `mailboxes/{role}/inbox/read/`
>
> `feedback_mailbox_read_is_top_level_not_nested_in_inbox`.

> ## 🔴 STANDING RULE — after `mail-send.sh`, a local `ls` can look reverted; merge before trusting it
>
> `feedback_mail_send_reconcile_resets_to_local_head_not_origin_main`.

> ## 🔴 STANDING RULE — check a claim against its live source, not the summary of it
>
> Load-bearing again today: re-checked `_handle_attention_query`'s own docstring before reversing
> myself on C1 — don't let a prior ruling's reasoning stand unexamined just because it was already
> ratified once.

> ## 🔴 STANDING RULE — keep mailbox filename basenames ≤150 chars (180 is the hard gate)
>
> Arch found and fixed a main-red incident 10-03 from 4 copies of a 182-183 char filename (not
> mine). The 180 limit includes `mailboxes/{role}/{box}/`, and `inbox/` is one char longer than
> `read/`. Aim for ≤150.

## Cron

✅ **Re-armed 2026-10-02 22:2x PDT — job id `c006bc0e`**, expression `47 6,9,12,15,18,21 * * *`.
7-day auto-expiry (~2026-10-09) — re-arm proactively on or before that date.

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **38 rows**, both guards clean. Run **both** after any edit:
`scripts/aging-standing-items.sh | grep '· cxo:'` (expect **38**) **and** `awk -F'|' '/^\|/ {print
NR": cols="NF-2}'` (every row must read `cols=4`). **Edit tool only — never `.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **3** (#1911, #1174, #1108), stable, re-checked this fire, no
new issues.

## Active — design closed, builds in flight (not mine to push forward)

- **#1911 + #1918** — combined design spec delivered 10-02, posted to both issues, PA building.
- **#1899 armed-carrier write-erosion** — ruled, Lead accepted, tracked as #1920, building.
- **`read_floor` mechanism** — built (5 ops, not flipped). The flip is PM's hand, deferred — **PM
  was unwell 10-02; check whether that's cleared before expecting movement.**

## Sprint goal (Exec relay of PM ruling, 10-03) — week ending Thu 10-08

Finish epic 0 Phase 3 deletions for every pattern list with a live wave; Lead owns. **CXO + PPM rulings
are the named critical-path dependency** — turn destination questions around early (quota may run out
Wed ~14:10, plan on 4 days). No open ruling requests held as of 13:17 10-03.

## Closed/corrected recently — watch only, nothing owed unless something reopens

- **10-02: #1911 + #1918 combined design pass — DELIVERED.** Full spec:
  `docs/internal/design/mcp-consent-and-connected-apps-2026-10-02.md`.
- **10-02: Ship #063 workstream review** — sent to `mailboxes/exec/inbox/`.
- **10-02: #1899 armed-carrier write-erosion — RULED.**
- **10-02/10-03: DISCOVERY/TRUST/ANALYSIS/MEMORY 13-row addendum — RULED, then CORRECTED TWICE.**
  (1) D1 (`session_activity_query`) — PPM caught that the handler is keyed to the current session
  only; conceded after verifying the source myself. (2) C1 (`attention_query` vs `analyze_blockers`
  for "threats to our timeline") — Lead's measurement exposed an inconsistency in my own reasoning
  (two sibling risk-rows I'd already kept in ANALYSIS); reversed myself to ANALYSIS after re-reading
  `attention_query`'s own docstring. **Both corrections were self-initiated after re-checking
  source, not just accepted on someone else's say — worth remembering the pattern, not just the
  outcome, if a third one shows up.**
- **10-03: mailbox filename-gate incident** — Arch's fix (not mine to redo), I regenerated my own
  MANIFESTs per his ask.
- **10-02: Arch's `read_floor` ruling + Lead's build**: read-only. YES to rail entries. TRUST's
  router coverage was 0/10 before description sharpening; Lead's since fixed it for D1/MEMORY.

## Waiting on others — nothing owed to PM

**Nothing currently queued for PM from this seat.** #1824's classifier owner is Lead's open
question.

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
