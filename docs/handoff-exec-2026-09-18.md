# Handoff — Exec (Chief of Staff), 2026-09-18

**Written for the Amber restart.** Assume you are a fresh or freshly-compacted Exec session with no
memory of the last three weeks. This file plus `dev/active/exec-carry-forward.md` is what you have.
Everything here is verifiable from `origin/main`; nothing depends on chat history.

## Who you are and what you own

Chief of Staff. Cross-role synthesis, sprint and epic progress tracking, weekly Ship coordination,
the cohort attention rollup. Tier-1 leadership. Worktree `~/Development/piper-morgan-worktrees/exec`,
branch `claude/exec-cycle`, Model A. Briefing: `docs/briefing/BRIEFING-ESSENTIAL-CHIEF-STAFF.md`.

## Cron

`38 6,10,14,18,22 * * *` — five fires/day, max 4h apart, 06:00–22:00. PM set this 2026-09-11.
Job `d070a7df` armed 2026-09-18 07:1x, expires ~09-25. **`CronList` at every fire; it dies silently
on session exit and at 7 days.** If zero jobs, re-arm immediately.

## The single most important thing in flight

**Sprint closeout for the week of Sep 11–17 is OUT and responses are pending.** I sent it
2026-09-18 07:3x to all ten roles (`mailboxes/exec/sent/closeout-exec-to-leadership-*-2026-09-18.md`).
It asks each leadership role for ONE top priority or primary goal, progress, on-track yes/no, next
steps — plus portfolio and contributor updates, capped at ~400 words. **PM is expecting a synthesis
from me once they come in.** Nudge threshold Sunday 09-20.

⚠️ **Five roles were dark when it was sent** (cio, lead, cxo, ppm, pa) and PM is waking roles
one-on-one as each is first needed. **Their copies are sitting unread by design, not lost.** Do not
re-send; do not read the silence as non-compliance. Check the registry's parked rows for who is still
dark before chasing anybody.

## State of the milestone

`python3 scripts/sprint-truth.py` is the only legitimate denominator — **run it fresh, never quote
this line as current**. At time of writing: `MVP: 56 not done (33 Sprint Backlog, 3 In Progress,
6 In Review, 14 Product Backlog); 1176 done. PLUS 0 unmilestoned. 33 NOT STARTED.`

Epic ordering lives in `dev/active/mvp-epic-order-2026-09-09.md` — **11 epics** after epic 12 was
retired and epic 2 reopened on PM's override. When counting epic membership, **exclude each section's
explicitly-not-folded caveat block** — a regex that counts every issue *mentioned* over-reports.

## Open items PM is parked on — all in the carry-forward, read it

The ruleset decision (parks Arch **and** CXO, and **my framing of it was incomplete — classic branch
protection already enforces the required check; see the carry-forward's corrected item 3**), Vercel
storage (Web hard-blocked), PA's BYOC sequencing answer, Janne Lammi's alpha invite (technical
blocker #1814 cleared), #1747 triage.

## How this seat gets things wrong — read this part twice

These are mine, earned, and each one cost real rework:

- **Verify the artifact the instrument reads, not the one you edited.** The freeze-check reads PM's
  local checkout, so a push alone doesn't change what it sees. `scripts/sync-pm-local.sh` is part of
  the operation.
- **Read the whole history before declaring a state never existed.** A row that reads `active` now
  may have been parked in between two commits you skimmed.
- **A present-tense claim about a shared mutable file goes stale the moment someone else commits.**
  Say "as of `<sha>`", not "all eleven rows carry X".
- **Check every surface before concluding, not the first one that answers.** I read `amber-agent.sh`,
  saw a fresh launch, and nearly told PM the restart would not resume transcripts — `amber-fleet.sh`
  resumes by default. One script answered; two scripts existed.
- **`echo` after `||` asserts nothing.** Verify a push by re-reading `origin/main`.
- **`closedAt` is UTC.** Compute in Pacific with `zoneinfo` and name the timezone.
- **zsh does not word-split `$VAR`.** Build path lists as arrays: `typeset -a P` / `"${P[@]}"`.
- **Cadence-blindness.** Check a role's actual cron before calling it dark. And when a
  correctly-calibrated instrument flags exactly one role, that is not a reason to go find seven.

## Cohort facts that are easy to get wrong

- **Leadership is 7** (exec, arch, cxo, ppm, cio, host, comms). **Staff is 4** (lead, pa, docs, web).
  Lead Developer is Tier 2 — surprising, and `docs/briefing/ROSTER.md` is the authority.
- **Model allocation, PM 2026-09-18: Fable reserved for Lead Developer; everyone else Opus or
  Sonnet.** Sub-agent dispatches inherit the dispatcher's model unless set explicitly — that
  inheritance exhausted the Fable tier on 09-13 and refused two roles' fires.
- **Registry authority: anyone may PARK any row; only the owning session may UN-PARK its own.**
  The failure modes are not symmetric — an un-parked dark role generates alerts nobody can act on.
- Mail goes via `scripts/mail-send.sh` (push-to-ref straight to `main`). Pass **every** changed path
  in ONE call — a split multi-call rename can delete both sides (#1746).

## Verified how

`CronList` → one job `d070a7df` (not a config read). Closeout delivery → 12 copies present under
`git ls-tree origin/main`. Registry state → `DUTY_CYCLE_COVERAGE=1 scripts/duty-cycle-freeze-check.sh`
returning 5 PARKED / 0 STALE. Restart-resume behavior → read from `amber-fleet.sh:215`, **a source
read, not an observed reboot**. Denominator: 11 registry rows, which is the opt-in watch list and
**not** the 24-resident fleet the reboot gate covers.
