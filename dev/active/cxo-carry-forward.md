---
last_updated: 2026-10-02
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — refreshed 2026-10-02 at the 07:03 WORK fire.

> 🔴 **Spring-cleaned 2026-09-22 per PM's context-floor directive; kept lean since.** Resolved
> history is deleted, not archived-in-place — it lives in session logs (the durable record) and,
> for the most transferable lessons, in `docs/briefing/CXO-SUCCESSOR-READ.md`. If you're looking for
> a specific dated incident that isn't here, check the session log for that date first.

> ## 🔴 STANDING RULE — emit the per-fire heartbeat before ending every fire
>
> **I personally went an entire day (10-01, 3-4 fires, 16 commits) without ever running this**,
> despite it being documented in the duty-cycle-tick skill. Exec caught it via CIO's freeze-check
> corroborating logic (real commits after a stale marker → correctly read as "not a stopped role,"
> not a false alarm — but a near-miss, not proof the step is optional). Fixed 10-02 07:13. **Run
> `scripts/duty-cycle-heartbeat.sh cxo {fire-type} --if-quiet` as the second-to-last action every
> fire, right before the carry-forward refresh.** Memory:
> `feedback_emit_heartbeat_every_fire_before_finishing`.

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
> after a send, your worktree can briefly show the old pre-move state — that is NOT a cross-agent
> revert. `git fetch && git merge origin/main` resolves it. Memory:
> `feedback_mail_send_reconcile_resets_to_local_head_not_origin_main`.

> ## 🔴 STANDING RULE — check a claim against its live source, not the summary of it
>
> Load-bearing again today: the `what_piper_knows_about_me` tool looked like a scope-list drift risk
> for #1911 until actually reading its description and `register_tools`' docstring guard — it's a
> pure composition of the same three resources, no drift. Checking first avoided a false alarm.

## Cron

✅ **Re-armed 2026-10-01 22:2x PDT — job id `2fa6cb13`**, expression `47 6,9,12,15,18,21 * * *`.
7-day auto-expiry (~2026-10-08) — re-arm proactively on or before that date.

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **36 rows**, both guards clean. Run **both** after any edit:
`scripts/aging-standing-items.sh | grep '· cxo:'` (expect **36**) **and** `awk -F'|' '/^\|/ {print
NR": cols="NF-2}'` (every row must read `cols=4`). **Edit tool only — never `.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **3** (#1911, #1174, #1108), stable, re-checked many times
today, no new issues. #1174 is a discovery thread, genuinely OPEN by design (pre-beta). #1108's copy
half done, build unowned.

## Closed today (10-02)

- **#1911 + #1918 combined design pass — DELIVERED.** Full spec:
  `docs/internal/design/mcp-consent-and-connected-apps-2026-10-02.md`, posted to both issues, PA
  notified. #1918 (Connected apps card) and #1911's identity/branding fixes can build now, in
  parallel — backend for #1918 already fully built and verified matching the AC. #1911's exact
  revoke-path sentence is gated on #1918 shipping first (sequencing, not a new truthfulness
  question). Checked for scope-list drift from the new `what_piper_knows_about_me` tool — none, it's
  a pure composition of the same three existing resources. Checked for a dark theme — none exists
  anywhere in the repo, so that AC line is satisfied by its own conditional. **Design side is fully
  closed; watch for the build.**
- **Ship #063 workstream review — drafted (forked), verified, sent.** Covers Fri 09-25 → Thu 10-01.
  Honest framing: almost all of the week's CXO work was routing/design rulings not yet user-visible
  (deletions and builds still queued); named #1859's misdiagnosis-and-correction and the mailbox-
  nesting recurrence as the window's two real self-corrections; named the mailbox-nesting lint hit
  for Exec's "main went red" question; named #1824 as still-blocked. Sent to
  `mailboxes/exec/inbox/`, cc PM, archived in `cxo/sent`.
- **A real procedural gap found and fixed**: had never been running the per-fire heartbeat command
  (see standing rule above). Caught by Exec, fixed same fire, memory written.
- **#1606 closed** (Lead, 4b floor-elements live on v163) — pure confirmation for my lane: "the
  floor's capability answer is the floor's own wording; nothing of yours was rewritten." Arch's
  condition 4 (CXO's confirm-copy ownership) held through the real build. No action needed.

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
