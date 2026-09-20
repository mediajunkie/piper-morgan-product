# Comms carry-forward

*Rewritten 2026-09-19 21:42 (day close). Ephemeral session state only — durable owed/queued items
live in `comms-standing-items.md`; the canonical record is the session log
(`dev/2026/09/19/2026-09-19-0642-comms-code-log.md`).*

## Cron

`d904b1d9`, expression `12 6,9,12,15,18,21 * * *` — re-armed at 21:42 STOP via delete-then-create
(815ce10d → d904b1d9, same cadence), CronList-verified exactly one job survives. Registry row
updated to match. Next fire: 2026-09-20 06:12.

## Closed today — both queued blog posts

- **"Assume It Was You"** (pubDate 09-19): full editorial review, proofreading, footer teaser
  retitled at PM's request, calendar → `ready-for-docs`, publish-ready memo sent. Docs published +
  distributed it same-day (crossed with PM handing it to them directly) — independently ran the same
  template audit, got 16/16, same result. **Fully closed, nothing owed.**
- **"From Abstraction to Example"** (renamed from "...Worked Example", pubDate 09-20): resolved an
  open `[Note to Comms]` bracket by tracking down the real April 22 source material (session log +
  a published sibling post cross-check), then a full template audit after PM's voice pass — 16/16
  clean. **Published overnight by Docs** — confirmed live at `/blog/from-abstraction-to-example/`,
  calendar status `published`, draft archived to `drafts/published/`. **Fully closed, nothing owed.**

## Closed today — calendar mechanism: `planned` status + pre-seeded Ship slots

PM's ask (via Exec): pre-populate the Wednesday Ship slot so an empty one is a real signal, not the
default pre-draft state. Introduced a new status value, **`planned`** — verified `drafted`/`queued`
would have broken `reconcile-drafts-calendar.py`'s draft-required assumption; documented the
exclusion in both scripts and the `update-calendar` skill. Pre-seeded **Ships #061 (Sept 23) through
#073 (Dec 16)**, one quarter. **Validated same-day**: Exec's duplicate guard caught the #061
placeholder before creating a parallel row; verifying their edit caught a real defect (`draftPath`
pointing at `dev/active/` instead of `docs/public/comms/drafts/` — same class as a documented Ship
#058 mistake), fixed. Exec will edit pre-seeded rows directly going forward (confirmed fine). Known
minor cosmetic gap, not fixed: the HTML calendar view has no `planned` CSS case yet (falls back to
`drafted` styling).

## Closed today — two issues

- **#1406** (calendar `canonicalSite` legacy stale values) — investigated rather than assumed,
  found already resolved by an earlier reconciliation pass. Closed with evidence.
- **#1834 build-item 1** (HOST's ruling: agents are never "person"/"people," any register) — picked
  up same-day rather than deferred. `template-audit` check #11 was missing singular "person"
  entirely; fixed, v1.15. Issue left open for build-item 2 (Exec's/CIO's, PM-facing internal
  reports).

## Watching for — no action yet

- **Attention-rollup gap**: flagged to Exec that my "9-10 drafts awaiting PM voice-pass" item wasn't
  visible in the 12:55 rollup snapshot, even though it's in this file (a canonical rollup source).
  Watch whether it shows up in the next regen.
- **Language-governance mechanism, part 2**: HOST ruled the "people" question and named Comms for
  eventual reconciliation against the existing public-prose convention
  (`feedback_agent_naming_convention_in_public_prose`) if/when Exec/CIO build the internal-reports
  check (#1834 item 2). Nothing to do until that lands.

## Open — no PM-gate currently, just queue depth

- **~7-8 drafts still await PM's voice-pass + art** (down from 9-10 — two closed today). Regenerate
  the chronological artifact from the calendar if a current list is needed.
- **ChicagoCamps talk (Sept 17) — outcome still unconfirmed.** No session-log mention of it
  happening in any 09-17/18/19 log. Ask PM directly rather than keep treating the deck as pre-event.
- **`template-audit` gap, still just flagged (2 data points)**: no check for "claims a named person
  is already public." Third instance = file it properly.
- **Cross-doc title inconsistency** — DIRECTORY.md "Communications Chief" vs. ROSTER.md
  "Communications Director." Not mine to reconcile.
- **Series structure (era split + blog-index featuring)** — data-correctness half resolved,
  structural display question open, PM/Web's call. Eras sorting (not pubDate) is the intended
  sequencing mechanism per PM's 09-17 note — see memory
  `project_narrative_chronology_via_eras_not_perfect_pubdate`.
- **No stated GitHub-criteria line yet** (duty-cycle-tick v1.33's third work-queue source) — gap
  named at this morning's START, still unfilled, nothing blocked on it.

## Waiting on others

- **PM** — voice-pass + art on ~7-8 drafted items; ChicagoCamps outcome; editorial calendar planning
  session (PM's stated next step after today's two posts, no detail yet on scope).
- **HOST** — Agent 360 synthesis, ~4 weeks out; #1834 build-item 2 is Exec's/CIO's, not HOST's, but
  HOST authored the ruling it depends on.
- **Someone (unclear who)** — #1636 (filed 08-15, OPEN as of 09-19); #1647 (filed 08-18, OPEN as of
  09-19).
