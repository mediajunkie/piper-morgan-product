---
last_updated: 2026-10-01
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — refreshed 2026-10-01 at DAY-CLOSE (22:17 fire).

> 🔴 **Spring-cleaned 2026-09-22 per PM's context-floor directive; kept lean since.** Resolved
> history is deleted, not archived-in-place — it lives in session logs (the durable record) and,
> for the most transferable lessons, in `docs/briefing/CXO-SUCCESSOR-READ.md`. If you're looking for
> a specific dated incident that isn't here, check the session log for that date first.

> ## 🔴 STANDING RULE — triage destination is `mailboxes/{role}/read/`, NEVER `mailboxes/{role}/inbox/read/`
>
> Recurred on me 10-01 despite already holding this memory from my own 09-11 cohort sweep. If you're
> about to run `mkdir -p mailboxes/{role}/inbox/read`, STOP — that mkdir is the tell. Correct path
> has exactly two segments after `mailboxes/{role}/`: `read/<name>`.
> `feedback_mailbox_read_is_top_level_not_nested_in_inbox`.

> ## 🔴 STANDING RULE — after `mail-send.sh`, a local `ls` can look reverted; merge before trusting it
>
> `mail-send.sh` pushes straight to `origin/main`, bypassing your local branch. Its residue-reconcile
> resets the paths you passed back to **local HEAD's** state, not `origin/main`'s new tip. Right
> after a send, your worktree can briefly show the old pre-move state (file back in `inbox/`, gone
> from `read/`) — that is NOT a cross-agent revert. `git fetch && git merge origin/main` resolves it.
> Traced live 10-01, cost a short false-alarm investigation. New memory:
> `feedback_mail_send_reconcile_resets_to_local_head_not_origin_main`.

> ## 🔴 STANDING RULE — check a claim against its live source, not the summary of it
>
> Load-bearing all of 10-01: every GITHUB/STATUS_PATTERNS ruling turned on reading handler docstrings
> directly, not picking between names offered; #1916's copy review turned on checking PM's draft
> against the actual OAuth-audience mechanics before shipping it.

## Cron

✅ **Re-armed 2026-10-01 22:2x PDT — job id `2fa6cb13`**, expression `47 6,9,12,15,18,21 * * *`
(SAME as before). Delete-then-create from `a0cf0685`; `CronList` confirmed exactly one job survives.
7-day auto-expiry (~2026-10-08) — re-arm proactively on or before that date.

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **36 rows**, both guards clean. Run **both** after any edit:
`scripts/aging-standing-items.sh | grep '· cxo:'` (expect **36**) **and** `awk -F'|' '/^\|/ {print
NR": cols="NF-2}'` (every row must read `cols=4`). **Edit tool only — never `.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **3** (#1911, #1174, #1108), stable all day, re-checked many
times. #1174 is a discovery thread, genuinely OPEN by design (pre-beta). #1108's copy half done,
build unowned.

## ⚠️ Active — two paired design assignments, deferred together with one named trigger

**#1911 (MCP OAuth consent page) + #1918 (Connected apps Settings revoke card) are now one design
session, not two** — PA's framing, agreed. #1911's consent page needs to truthfully name a real
revoke location; #1918 is that location.

- **#1911**: two truthfulness rulings already closed on the copy side (revoke-promise dropped;
  "cannot see another person's data" KEPT with a re-check trigger on #1458/second-caller). Full page
  design (branding, raw-UUID identity line, scope-list truthfulness) still owed.
- **#1918**: PM-approved 10-01 night — real Piper-side revoke path, Production milestone, not MVP,
  off Lead's critical path. Backend is PA's lane (in progress). UI is mine: a "Connected apps" card,
  one row per OAuth client (name/connected-at/last-used/active/Revoke). 30-day refresh-token window
  means first-view states need to read calmly, not alarm on an unexplained count — work this through
  properly in the actual design pass, not pre-decided here.

**Named trigger for the deferral** (not a quiet "I'll get to it"): a dedicated design pass this week
for both pages together — genuinely deep, render-sensitive, first-tester-facing-screen work for one
and a destructive-action settings surface for the other.

## Closed today (10-01) — watch only, nothing owed unless something reopens

- **GITHUB's last 3 rows + STATUS_PATTERNS 14-row addendum** — ruled, PPM concurred, Lead applied all
  19 rows same evening. GITHUB_QUERY_PATTERNS now **GO** (66/0, deletion deferred to a fresh
  session). STATUS_PATTERNS 48/3 (router-grammar remainder, Lead's lane). Filed #1917
  (PRs-needing-review gap). **Watch for tomorrow**: `attention_query`'s registry description needs
  sharpening (still dispatches for 5/6 ownership asks today despite the `floor` ruling) — Lead's fix,
  not mine.
- **#1916** (Calendar Connect honesty copy) — delivered as a GH comment, build queued after #1595's
  4b unit.
- **Phase 3 day bundle (1606, GITHUB-first-8, TEMPORAL), Slack's keyless refusal,
  CALENDAR_QUERY_PATTERNS** — all ruled and PPM-confirmed. Full detail in today's session log.
- CIO's NO-DAY-CLOSE streak detector shipped (read-only for me). 4b floor-element plan extension
  (Arch/Lead) confirmed CXO's confirm-copy ownership unchanged (read-only for me).

Earlier closes (09-19 through 09-30) — full detail in their respective session logs.

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
  `UNMEASURED` until increment-1 infra (MCP Phase C, actively building).

## 🔴 EVERY OUTBOUND MEMO — route away from Lead by default (PM directive, 2026-09-09)

Before addressing Lead, ask whether he must **act** — if the answer is "he wrote it" rather than "he
must act on it," cc, don't address; prefer CIO/PPM/Arch as primary.

## 🔴 EVERY MEMO — filename budget

Keep memo basenames **≤130 characters**. The subject line carries the argument.

## Briefing currency

`docs/briefing/BRIEFING-ESSENTIAL-CXO.md`'s Current Focus section refreshed 2026-09-22 per Docs'
staleness flag. Check that file directly rather than assuming this note stays current about it.
