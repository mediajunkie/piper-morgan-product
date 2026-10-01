---
last_updated: 2026-10-01
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — refreshed 2026-10-01 at the 16:17 WORK fire.

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
> **Load-bearing all week, this fire too**: the GITHUB-three ruling turned on reading three handler
> docstrings directly rather than picking between the two names Lead offered; the "what version are
> we on" ruling turned on an exact word-for-word docstring match, not inference. Saying "I didn't
> check this" is part of the discipline, not a failure of it — used that stance earlier this week on
> CALENDAR's day-less-ask question.

## Cron

✅ **Re-armed 2026-09-30 22:30 PDT — job id `a0cf0685`**, expression `47 6,9,12,15,18,21 * * *`
(SAME as before). Delete-then-create from `8512cedb`; `CronList` confirmed exactly one job
survives. 7-day auto-expiry (~2026-10-07) — getting close, re-arm proactively on or before that date
per the duty-cycle-tick skill's Step 1 guidance rather than waiting to discover absence.

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **34 rows**, both guards clean. This carry-forward does not
duplicate the tracker; check it for anything open. Run **both** guards after any edit:
`scripts/aging-standing-items.sh | grep '· cxo:'` (expect **34**) **and** `awk -F'|' '/^\|/ {print
NR": cols="NF-2}'` (every row must read `cols=4`). **Edit tool only on this file — never
`.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **3** (#1911, #1174, #1108), re-checked twice this fire (two
consecutive rounds, no new issues). #1911 is the active design assignment (below). #1174 is a
discovery thread, genuinely OPEN on GitHub by design (pre-beta, not meant to close yet) — my own
09-30 verification confirmed my half converged, not that the issue itself closes. #1108's copy half
done, build unowned.

## ⚠️ Active — #1911 MCP OAuth consent page, full design pass still owed

PM routed the MCP consent page's design to me (copy via Comms). **Two truthfulness rulings made so
far, both closed on the copy side**: (1) the "revoke at any time" promise — no user-facing path
exists, PA dropped it (`15c371f65f`, shipped). (2) "it cannot see another person's data" — **KEEP,
with a named re-check trigger**: true today (owner-scoping verified, one caller in production);
re-check the moment EITHER #1458 (cross-caller isolation, still OPEN) closes OR a second real caller
is onboarded, whichever first. **The full page design — branding, raw-UUID identity line, copy
integration, scope-list truthfulness — is still explicitly deferred to a dedicated pass this week**,
named as a real trigger (genuinely deep, render-sensitive, first-tester-facing-screen work), not a
quiet "I'll get to it." Pick this up as its own piece of work, not folded into a duty-cycle fire.

## Closed recently — watch only, nothing owed unless something reopens

- **10-01 (16:17 fire): GITHUB's last 3 rows + STATUS_PATTERNS 14-row addendum — all ruled, PPM
  concurred (conceding their own independent Family-B ruling after seeing mine).** GITHUB:
  "prs needing review" is a genuine capability gap neither existing op answers (`floor`, worth a
  tracking issue); "milestone deadline" stays `floor`/CLARIFY (no current-milestone default exists);
  "what version are we on" → `list_releases_query` (exact docstring match). STATUS_PATTERNS: "my
  tasks" → `list_todos_query`; "my assignments"/"what I'm working on" → **`floor`, not
  `attention_query`** (ownership question, not an urgency aggregate — PPM independently ruled
  `attention_query` first, then conceded on seeing this reasoning); "status/progress report" →
  `generate_report`; the gate-FAIL row ("what am I working on?") → same `floor` reasoning as the
  assignments family.
- **10-01: Phase 3 day bundle (1606, GITHUB's first 8, TEMPORAL) — three rulings, ALL CONFIRMED by
  PPM independently same fire.** #1606: capability question, not a disguised request. GITHUB: 6
  confident + 1 source-checked (`list_issues_query` docstring literally handles "how many issues").
  TEMPORAL: 3 commit / 2 `floor` (floor as the *better* answer, precise data already computed — a
  distinct shape from the conflict-detection gap below).
- **10-01: Slack's keyless refusal — ruled.** The #1807/#1823 copy string is about the principal's
  own key status, true regardless of #1481's outcome — reuse it now, don't wait on #1481.
- **10-01: CALENDAR_QUERY_PATTERNS — fully resolved.** Week-as-default for day-less asks is fine
  (true, complete, over-inclusive); a separate 5-row conflict-detection gap rules `floor` (showing
  unrelated data would imply a check that never ran) — unblocked Lead's deletion of 52 literals.
- **#1174** (09-30): 19-day silence check-in surfaced a visibility gap, not a real one — both halves
  had converged the same day they were filed (09-11); verified independently. Issue itself stays
  genuinely OPEN (discovery-only, pre-beta) — that's correct, not stale.
- **PRIORITY_PATTERNS** (09-30, 12 rows): 6 to `attention_query`, 1 to `prioritize`, 1 stays
  `get_top_priority`, 1 to guidance, 1 pulled from the corpus entirely. PPM independently
  re-verified all of it.
- **CIO's NO-DAY-CLOSE streak detector (K=3) shipped 10-01**, sized on real 09-11→09-30 data per my
  own 09-11 sizing condition. Two historical findings surfaced (HOST's prose-verified days, PPM's
  undated-marker false-fail), both already self-corrected by those roles. Read-only for me, no
  action.
- **4b floor-element plan extension (Arch/Lead thread, 10-01)**: read-only for me. Confirmed
  condition 4 explicitly preserves CXO's confirm-copy ownership unchanged. Lead builds next session
  (fresh-session trigger named, quota-tail deferral).

Earlier closes (09-19 through 09-29: BYOC T-axis series, #1772 chain, GUIDANCE_PATTERNS, Pard's
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
