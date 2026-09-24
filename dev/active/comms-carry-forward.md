# Comms carry-forward

**Spring-cleaned 2026-09-22** per today's context-floor-reduction plan (item 4a, PM directive via
Exec) — resolved items deleted, not archived with a `was:`/history trail. Full narrative for
anything below lives in the dated session log, not here.

## Cron

`b000b025` — re-armed at 21:42 STOP 09-23 via delete-then-create (f2ae5d96 → b000b025, same
cadence), CronList-verified exactly one job survives. Registry row updated to match. Next fire:
2026-09-24 06:12. **Friday 09-25's START fire is the first editorial mining pass** — see the
recurring section below.

## Open — no PM-gate, just queue depth

- **Drafts awaiting PM's voice-pass** — re-query the calendar fresh before quoting a count; a
  carried number went stale once already (09-20).
- **ChicagoCamps talk (Sept 17) outcome still unconfirmed.** No session-log mention it happened.
  Ask PM directly.
- **`template-audit` gap, 2 data points**: no check for "claims a named person is already public."
  Third instance = file it properly.
- **Cross-doc title inconsistency** — DIRECTORY.md "Communications Chief" vs. ROSTER.md
  "Communications Director." Not mine to reconcile.
- **Series structure (era split + blog-index featuring)** — structural display question open,
  PM/Web's call. Eras sorting (not pubDate) is the intended sequencing per PM's 09-17 note.
- **No stated GitHub-criteria line yet** (duty-cycle-tick v1.33's third work-queue source).
- **Language-governance mechanism, part 2**: HOST named Comms for eventual reconciliation once
  Exec/CIO build the internal-reports check (#1834 item 2).
- **HTML calendar view has no `planned`-status CSS case** (falls back to `drafted` styling) —
  cosmetic, low priority.
- **workDate accuracy audit** — broader pass still blocked on PM naming where the archive lives.

## This seat's standing errors (deduplicated)

- **Verify a heartbeat push landed directly** (`git show origin/main:...`), not just an empty
  `origin/main..HEAD` — that diff can read clean mid-race and hide a genuinely failed push.
- **Two draft copies (`dev/active/` vs `docs/public/comms/drafts/`) can silently diverge** when two
  edits land on different copies — diff them directly before trusting either, especially after
  someone else's edit. Same class hit Ship #058 and #061. **Prevention side, per PM 09-22**: sync
  before editing a shared draft, not just diff after — Ship #061's split traced to Exec editing
  `dev/active/` without first checking whether the `docs/public/comms/drafts/` copy had moved.
  Applies to me too whenever I'm not the only one touching a draft that week.
- **A surviving cron job id across a suspected reboot is not evidence the reboot didn't happen** —
  `--resume` restores state from the saved transcript regardless.

## Waiting on others

- **PM** — voice-pass + art on queued drafts; ChicagoCamps outcome; archive location for the
  workDate audit.

## Model tier — currently Fable 5.1, not by allocation; PM/Pard's call, not mine

Switched from Sonnet 5 at ~12:45 PDT 09-23, coincident with the usage-wall rate-limit. Exec
confirmed with one instrument (transcript `model` field, 11/11 seats): comms, exec, pa all drifted
to Fable-family in the same window; 7 seats unchanged. Fable ≈ 3.3× Sonnet cost at our mix.
Mechanism and stickiness unknown. **Routed to Pard (relaunch/stickiness) and PM (allocation) — do
not self-relaunch or change tier on my own initiative.** Just keep the log header honest about
which model is observed, and watch for their ruling.

## Recurring — biweekly editorial mining pass (PM-ratified 09-23, LIVE)

**Next due: Friday 2026-09-25** (first pass, a catch-up). Full procedure in
`comms-standing-items.md` § "Recurring practices" — the Friday START fire checks that section's
**Next due** date and drains the pass if due. First-pass scope: Aug 30 → Sept 17 (coverage
currently stops at workDate Aug 29), plus Sept 18-24 only if its Thursday omnibus is on disk at
fire time. Deliverable: a written recommendations report to PM, **not** auto-scheduled — it's input
to a joint decision. Steady state after: every 14 days.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Someone (unclear who)** — #1636 (filed 08-15), #1647 (filed 08-18) — both still OPEN.
