# Handoff — Comms (Communications Director), 2026-09-18

**Written for the Amber restart.** Assume you are a fresh or freshly-compacted Comms session with no
memory of the last three weeks. This file plus `dev/active/comms-carry-forward.md` is what you have.
Everything here is verifiable from `origin/main`; nothing depends on chat history.

## Who you are and what you own

Communications Director. Editorial calendar, blog drafting (building-narrative/insight/Ship variants),
voice-pass support, publish-ready handoff to Docs. Tier-1 leadership. Worktree
`~/Development/piper-morgan-worktrees/comms`, branch `claude/comms-cycle`, Model A. Briefing:
`docs/briefing/BRIEFING-ESSENTIAL-COMMS.md`.

## Cron

`12 6,9,12,15,18,21 * * *` — 6 fires/day, windowed 06:12–21:12, last fire of the day is STOP.
Job **`815ce10d`**, CronList-verified directly (not read from the registry) at two separate fires
today. **The registry's `dev/active/duty-cycle-registry.tsv` comms row said job `a1a8e2e5` this
morning — that id is wrong, corrected in the same commit as this file.** See "How this seat gets
things wrong" below; it's the same shape of error, not a one-off.

## The single most important thing in flight

**The Aug 10–18 building-narrative backfill is drafted and queued, all 6 beats, as of today.** PM
caught (09-15) that a 09-01 slate-planning survey had missed real material in that window; a
dispatched re-read found 5 strong candidates, PM approved them 09-16, drafting held until after the
09-17 usage-reset per PM's own token-budget instruction. Drafted today (09-18): Aug 10/12/13/14/15,
plus a 6th (Aug 16) found on an independent re-verification pass that caught the *first* pass's "thin"
call as wrong — see `continue-narrative` v1.2 below. All 6 are `status=drafted` on the calendar,
pubDates Oct 6 through Oct 22 (the next open queue slots — they publish *after* the already-scheduled
Aug 21–31 beats, not before; see PM's 09-17 note under "cohort facts" below). Full trail:
`dev/2026/09/18/2026-09-18-0642-comms-code-log.md`.

**10 building-theme drafts total are now unpublished and awaiting PM's voice-pass + art** — the 6
backfill beats plus 4 already-queued before it (Near-Miss Aug25, Alarm Aug26, Three-Seats-Dark
Aug27-29, What-PM-Actually-Is Aug29-31). A chronological artifact of all 10 was generated for PM
today (not saved to the repo — it was a published Artifact page, ephemeral by nature; regenerate from
the calendar if needed, query is in today's session log).

## `continue-narrative` v1.2 — read this before any narrative-front survey

The skill (`.claude/skills/continue-narrative/SKILL.md`) now **requires** a per-calendar-day ledger
(machine-parseable, embedded in the session log) before any slate reaches PM, enforced by
`scripts/check-narrative-survey-coverage.py`. This exists because a broad-window survey returning an
aggregate mood ("rich everywhere") let a real gap go unnoticed *twice in the same PM-driven session*
(Aug 21-26, then Aug 10-18). **First real use of the mechanism (today) caught a genuine third
instance** — Aug 16 was wrongly marked "thin" on 09-15, corrected today. Don't skip the ledger step to
save time; it is the thing that has actually caught real misses, not ceremony.

## Sprint closeout — check whether it's been sent

Exec's Sep 11-17 closeout request (`mailboxes/comms/inbox/closeout-exec-*`) asks every leadership role
for one priority/goal + progress + portfolio + contributor update, ~400 words, due by Sunday 09-20 but
"as soon as possible" preferred. **If you're reading this because the restart happened before I sent
mine, it still needs sending** — check `mailboxes/exec/inbox/` for a reply from comms; if absent, write
it. `python3 scripts/sprint-truth.py` for the current MVP denominator if you cite sprint completeness.

## Open items — no PM-gate, just queue depth

- 9 drafts await PM's voice-pass + art (the 10 above, minus whichever have moved by the time you read
  this). Nothing blocking beyond PM's own bandwidth.
- ChicagoCamps slide deck (landed 09-12) still not reviewed by Comms — watching for PM to confirm/ask.
- `template-audit` has no check for "claims a named person is already public" (the Who's Who miss,
  09-13, was the second data point) — flagged for awareness twice now, never filed as a formal
  proposal. If it recurs a third time, that's probably the signal to just fix it.
- Series structure (era split + blog-index featuring) — data-correctness half resolved; the
  *structural* display question is still open, PM/Web's call. **More load-bearing than it looks**: PM
  said 09-17 that Eras sorting, not pubDate order, is the intended mechanism for showing readers the
  narrative's true sequence — see cohort facts below.

## How this seat gets things wrong — read this part twice

- **A shared registry/tracker file can be quietly wrong even when it reads confidently.** Today's
  `a1a8e2e5` case: identical boilerplate text, including the same fabricated-sounding job id, was
  copy-pasted across at least five different roles' rows (comms, cxo, ppm, pa, docs) by whoever ran a
  mass "unpark" pass this morning — a calendar-date test ("the reset passed"), not a per-role
  `CronList` check. **Always verify your own row's cron claim against your own `CronList` output before
  trusting or repeating it**, even when the row looks recently and confidently updated.
- **Mailbox writes go through `mail-send.sh`, never a direct `git commit` on your feature branch** —
  even for a trivial inbox→read triage move with no new content. Tried the direct-commit shortcut once
  today; `check-branch.sh` correctly blocked it. Redo via `mail-send.sh`, don't fight the hook.
- **A footer-tease chain touches more files than the one you're editing.** Inserting or removing a beat
  from the narrative queue means checking the file *before* your insertion point too (its outbound
  tease needs to change), not just the files you're actively adding. Missed this reflex once early in
  today's session and had to go back for it — now it's the first thing I check on any queue edit.
- **The negation-reveal AI tic ("X isn't Y. It's Z.", leading with the denial) is not a one-off
  mistake to fix once — it's a strong default in freshly-generated prose.** Found and fixed 4-9
  instances per draft across two separate editorial passes today, from two different sources (my own
  transcription and 6 different subagent drafts). Sweep for it every single time, don't assume a clean
  pass means it won't be there next time.
- **Verify day-of-week and date-math programmatically, never by mental arithmetic**, before it goes
  into a calendar row or a scheduling decision — cheap to check, expensive to be wrong about once 5+
  rows depend on it.
- **An internal codename/methodology-ID can leak into public prose during transcription, not just
  drafting.** Caught myself doing this once today (an agent-returned draft had named an internal
  pattern by its methodology number; I was mid-transcribe and almost let it through) — the
  four-category opacity sweep applies to *every* touch of a draft, not just the first pass.

## Cohort facts that are easy to get wrong

- **PM's 09-17 framing, durable and directly relevant to Comms' work**: the building narrative's
  *publish* order has never been perfectly chronological and PM has explicitly accepted that — Eras
  sorting (not pubDate) is meant to carry true sequence for readers, contingent on `workDate` accuracy
  across the calendar. Saved as memory `project_narrative_chronology_via_eras_not_perfect_pubdate`.
  Don't treat a publish-order gap as a crisis; do treat `workDate` accuracy as higher-stakes than it
  used to read.
- **Weekly usage-limit standdown**: hit 09-15, PM-directed stand-down via Exec's memo, reset Thursday
  09-17 ~22:00. Normal operation resumed 09-18. Some roles were still legitimately dark this morning
  (PM waking them one-on-one) — don't read a dark peer as a stalled one.
- **Model allocation this week (PM, 09-18)**: Fable reserved for Lead Developer; everyone else Opus or
  Sonnet. Sub-agent dispatches inherit the dispatcher's model unless set explicitly — that's what
  exhausted the Fable tier once already.
- **Amber restart is imminent** (today or tomorrow, PM + Pard) — this file exists because of a fleet
  reboot gate that reads `origin/main` for a dated handoff per resident; filename pattern is
  load-bearing (`docs/handoff-comms-2026-09-18.md`, exactly).

## Continuity files

| file | holds |
|---|---|
| `dev/active/comms-carry-forward.md` | current state as of today — rewrite it, don't trust it stale |
| `dev/2026/09/18/2026-09-18-0642-comms-code-log.md` | today's full session log, including the v1.2 ledger |
| `docs/internal/planning/comms/editorial-calendar.csv` | the schedule — source of truth |
| `.claude/skills/continue-narrative/SKILL.md` | v1.2 — read before any narrative-front survey |
| `.claude/skills/template-audit/SKILL.md` | pre-publish mechanical checklist |
| `scripts/check-narrative-survey-coverage.py` | the new completeness gate |

## Verified how

Cron: `CronList` directly, twice today (not a registry read). Registry correction: `git diff` against
what I originally read, cross-checked with what landed from another role's concurrent edit before
merging. Draft/calendar state: `scripts/reconcile-drafts-calendar.py` (exit 0, 17 files linked) and a
whole-file CSV field-count + semantic-anchor scan, both re-run after every edit today. Push state:
`git log --oneline origin/main..HEAD` after every commit, empty each time. Denominator: this file
covers Comms' own lane only, not the other 23 residents the reboot gate also watches.
