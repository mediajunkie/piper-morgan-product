# Comms carry-forward

*Rewritten 2026-09-19 06:42 (START, re-verified against primary sources, not just re-stated). Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log. **See also `docs/handoff-comms-2026-09-18.md` for the full cold-start handoff.***

## Cron

`815ce10d`, expression `12 6,9,12,15,18,21 * * *` — CronList-verified directly again at 06:42 today's START fire: exactly one job, matches. `dev/active/duty-cycle-registry.tsv`'s comms row also confirmed correct (job id matches).

## Wave 1 of the Amber fleet renewal — RESOLVED, this session IS the result

Exec named Comms (with Arch) for a deliberate `/clear`, testing renewal-from-handoff. That clear happened 2026-09-18 ~22:xx; this session picked up cleanly from `docs/handoff-comms-2026-09-18.md` + this file alone, per the arrival protocol (arrival block logged in yesterday's session log, verified the cron claim against `CronList` directly, confirmed via chat with PM). Nothing further owed on this thread.

## Closed today — the full Aug 10-18 backfill, all 6 beats

All PM-approved beats are drafted, edited, and queued:

- Aug 10 "The Contract Tested the Day It Was Born" → pubDate Oct 6
- Aug 12 "Three Silent Failures Became One Law" → pubDate Oct 8
- Aug 13 "Giving It Away, and Worrying Who'd Take It" → pubDate Oct 13
- Aug 14 "The Message That Deleted Itself" → pubDate Oct 15
- Aug 15 "The Feature That Was Never Real" → pubDate Oct 20
- Aug 16 "The Board That Stopped Matching Reality" → pubDate Oct 22 (new tail; the 6th beat, found via `continue-narrative` v1.2's re-verification catching the original 09-15 "thin" call as wrong — PM confirmed drafting it)

Full footer-tease chain repaired end to end across all 8 touched files. A chronological artifact (all 10 unpublished building beats, work-date order with publish-position shown alongside) was built and published for PM today — not saved to the repo, regenerate from the calendar CSV if needed (query in today's session log).

**11 negation-reveal AI-tic instances found and fixed across the 6 drafts** — this pattern is clearly a strong default in generated/transcribed prose, not a one-off; sweep for it every time.

## Also closed today

- Sprint closeout (Sep 11-17) sent to Exec, cc PM — §1 priority/§2 portfolio/§3 contributors/§4 PM-gated, 353 words.
- `docs/handoff-comms-2026-09-18.md` written, and refreshed again at the STOP fire.
- Registry job-id correction (see Cron above).
- **website#35 closed** — Web shipped real test coverage for the local-draft restore path. Off the list.
- All mail triaged to read/, including one real mail-mechanics catch (a half-pushed inbox→read move via `mail-send.sh` — always pass every changed path in one call, even when a plain `mv` already handled one side locally).

## Open — no PM-gate currently, just queue depth

- **9-10 drafts await PM's voice-pass + art** — see the artifact (regenerate from the calendar if it's no longer available) for the current full chronological list.
- **Possible durable fix worth raising**: `template-audit` has no check for "claims a named person is already public" — the Who's Who miss (9/13) was the second data point. Not filed as a formal proposal yet — two data points, flagged for awareness.
- **ChicagoCamps talk (Sept 17) — date has now PASSED, outcome unconfirmed.** Slide deck landed 9/12,
  still not reviewed by Comms. Re-checked 2026-09-19: no session-log mention of the talk actually
  happening in 09-17/18/19 logs. Standing-items row still reads pre-talk ("PM confirm final") —
  that's now stale phrasing; worth asking PM directly how it went rather than continuing to treat
  the deck as pre-event material.
- **Cross-doc title inconsistency** — DIRECTORY.md says "Communications Chief," ROSTER.md says "Communications Director." Noted, not mine to reconcile.
- **BYOC listing copy** — held per the ESSENCE ratification; the marketplace *narrative* piece is a separate artifact, already published.
- **Series structure (era split + blog-index featuring)** — data-correctness half resolved; the *structural* display question remains open, PM/Web's call. More load-bearing than it looks: per PM's 09-17 note, Eras sorting (not pubDate) is the intended mechanism for showing readers the narrative's true sequence — see memory `project_narrative_chronology_via_eras_not_perfect_pubdate`.
- **No stated GitHub-criteria line yet** (per duty-cycle-tick v1.33's third work-queue source) — Comms
  has no cheap mechanical GitHub query defined for "issues meeting my role's criteria." Gap named,
  not yet filled; nothing blocked on it.

## Today's two-post thread — CLOSED for "Assume It Was You", IN PROGRESS for tomorrow's post

**"Assume It Was You"** (pubDate 2026-09-19): confirmed correct guess from this morning. Full
editorial review + proofreading pass done, footer teaser retitled at PM's request, calendar synced,
status → `ready-for-docs`, publish-ready memo sent to Docs (cc PM) — `mailboxes/docs/read/` (or
`inbox/` until Docs triages) `publish-ready-comms-to-docs-cc-pm-assume-it-was-you-2026-09-19.md`.
**Nothing further owed here unless Docs/PM flags something.**

**"From Abstraction to Example"** (renamed from "...Worked Example", pubDate 2026-09-20): PM got a
day ahead — finished editing, added illustration + frontmatter, and asked Comms to resolve an open
`[Note to Comms]` editorial bracket in the "illuminating contrast" section using real source facts.
Resolved: real harassment-case worked example (source: `dev/2026/04/22/2026-04-22-1645-lead-code-
opus-log.md`, cross-confirmed against the published sibling post "The Voice of a Denial") now sits
paired against the pre-change contrast line already in the draft. **PM is now doing their own voice
pass** before handoff to Docs. **Comms' next move once that's done: run the full template audit**
(noted a few pre-existing typos while reading — stray period, "the the models," "origianal",
double spaces — worth a full sweep, not just spot fixes). Calendar title already synced to match
the rename; draft filename intentionally left as `from-abstraction-to-worked-example.md` (PM hasn't
asked for a rename; confirmed not functionally required since `publish-to-blog` takes an explicit
`--slug` at publish time).

PM's broader stated plan: after these two posts, resume editorial calendar planning work (no
further detail given yet on what aspect).

## Waiting on others

- **PM** — voice-pass + art on the ~9-10 drafted items; ChicagoCamps outcome/script-slide review;
  confirmation on today's blog-post ask.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Someone (unclear who)** — #1636 (filed 08-15, still OPEN as of 09-19 `gh issue view`); #1647
  (filed 08-18, still OPEN as of 09-19 `gh issue view`).
