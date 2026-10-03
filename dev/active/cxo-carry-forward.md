---
last_updated: 2026-10-02
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — refreshed 2026-10-02 at the 19:03 WORK fire.

> 🔴 **Spring-cleaned 2026-09-22 per PM's context-floor directive; kept lean since.** Resolved
> history is deleted, not archived-in-place — it lives in session logs (the durable record) and,
> for the most transferable lessons, in `docs/briefing/CXO-SUCCESSOR-READ.md`. If you're looking for
> a specific dated incident that isn't here, check the session log for that date first.

> ## 🔴 STANDING RULE — emit the per-fire heartbeat before ending every fire
>
> I went an entire day (10-01) without ever running this, despite it being documented in the
> duty-cycle-tick skill. Fixed 10-02 07:13. **Run `scripts/duty-cycle-heartbeat.sh cxo {fire-type}
> --if-quiet` as the second-to-last action every fire**, right before the carry-forward refresh.
> CIO's since noted a structural fix (re-armed post-commit heartbeat hook) is piloting on their own
> seat — "no action for you... the line is still the right habit until then." Memory:
> `feedback_emit_heartbeat_every_fire_before_finishing`.

> ## 🔴 STANDING RULE — triage destination is `mailboxes/{role}/read/`, NEVER `mailboxes/{role}/inbox/read/`
>
> Recurred on me 10-01 despite already holding this memory from my own 09-11 cohort sweep.
> `feedback_mailbox_read_is_top_level_not_nested_in_inbox`.

> ## 🔴 STANDING RULE — after `mail-send.sh`, a local `ls` can look reverted; merge before trusting it
>
> `mail-send.sh` pushes straight to `origin/main`, bypassing your local branch; its residue-reconcile
> resets passed paths back to **local HEAD's** state, not `origin/main`'s new tip. `git fetch && git
> merge origin/main` resolves it. `feedback_mail_send_reconcile_resets_to_local_head_not_origin_main`.

> ## 🔴 STANDING RULE — check a claim against its live source, not the summary of it
>
> Load-bearing all day: every routing ruling turned on reading the actual destination's canonical
> phrase/docstring/disposition in `action_registry.py`, not the family label a memo grouped it under.

## Cron

✅ **Re-armed 2026-10-01 22:2x PDT — job id `2fa6cb13`**, expression `47 6,9,12,15,18,21 * * *`.
7-day auto-expiry (~2026-10-08). **Next fire (21:47) is today's last scheduled fire — STOP sequence
applies.**

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **38 rows**, both guards clean. Run **both** after any edit:
`scripts/aging-standing-items.sh | grep '· cxo:'` (expect **38**) **and** `awk -F'|' '/^\|/ {print
NR": cols="NF-2}'` (every row must read `cols=4`). **Edit tool only — never `.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **3** (#1911, #1174, #1108), stable all day, re-checked many
times, no new issues.

## Closed today (10-02) — watch only, nothing owed unless something reopens

- **#1911 + #1918 combined design pass — DELIVERED.** Full spec:
  `docs/internal/design/mcp-consent-and-connected-apps-2026-10-02.md`, posted to both issues, PA
  building. Design side fully closed.
- **Ship #063 workstream review — drafted (forked), verified, sent** to `mailboxes/exec/inbox/`.
- **A real procedural gap found and fixed**: the per-fire heartbeat (see standing rule above).
- **#1606 closed** (Lead) — pure confirmation, CXO's confirm-copy ownership held through the build.
- **#1899 armed-carrier write-erosion — RULED.** Agreed with Arch's cross-family-release shape
  (release a write only when its registry category differs from the carrier's own pending op's);
  verified the #1190 confirm-gate safety property myself before ratifying; wrote exit copy for both
  prompt sites. Lead accepted verbatim, tracked as #1920, building — will probe "never mind"
  empirically before adding a special case.
- **DISCOVERY/TRUST/ANALYSIS/MEMORY 13-row addendum — RULED, 8/13 agree, 5 disagree.** Checked every
  destination's canonical phrase before ruling. Two "risk"-framed rows stay in ANALYSIS against
  sub-threshold router picks (confirmed `analyze_blockers` is itself FLOOR-disposition with no
  handler — a pure category call); "what features does piper have" stays DISCOVERY, not QUERY's
  single-named-feature `get_feature_info`.
- **Arch's `read_floor` ruling (Lead's finding)**: read-only for me. Surface 2 never produces
  DISCOVERY/TRUST/MEMORY (0 of 620 samples) — a real gap. Arch ruled YES to a `read_floor` rail-entry
  mechanism (not a consult branch), gated behind the Phase-2 per-category gate before any further
  deletion. Arch offered a classifier-fallback framing-quality comparison as a separate, optional
  measurement "if CXO wants it" — declined, nothing blocked on it.

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
