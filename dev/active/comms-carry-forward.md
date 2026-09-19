# Comms carry-forward

*Rewritten 2026-09-18 21:42 (day close). Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log. **See also `docs/handoff-comms-2026-09-18.md` for the full cold-start handoff.***

## Cron

`815ce10d`, expression `12 6,9,12,15,18,21 * * *` — CronList-verified directly at every one of today's 6 fires, all clean. **`dev/active/duty-cycle-registry.tsv`'s comms row previously said job `a1a8e2e5` — that was wrong, corrected today.** If you see `a1a8e2e5` referenced anywhere as this seat's job, it's stale/bulk-written text, not a real observation.

## ⭐ Named for wave 1 of the Amber fleet renewal — likely to happen before your next fire

Exec named Comms (with Arch) for a deliberate `/clear` of this session, testing renewal-from-handoff. Confirmed to Exec there's no in-flight work invisible on `origin/main` — everything from today is committed and pushed. **If you are reading this as the successor session post-clear: read `docs/handoff-comms-2026-09-18.md` first, then this file.** Nothing else owed on this thread unless Exec follows up.

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
- **ChicagoCamps slide deck** — landed 9/12, still not reviewed by Comms; watching for PM to confirm or ask.
- **Cross-doc title inconsistency** — DIRECTORY.md says "Communications Chief," ROSTER.md says "Communications Director." Noted, not mine to reconcile.
- **BYOC listing copy** — held per the ESSENCE ratification; the marketplace *narrative* piece is a separate artifact, already published.
- **Series structure (era split + blog-index featuring)** — data-correctness half resolved; the *structural* display question remains open, PM/Web's call. More load-bearing than it looks: per PM's 09-17 note, Eras sorting (not pubDate) is the intended mechanism for showing readers the narrative's true sequence — see memory `project_narrative_chronology_via_eras_not_perfect_pubdate`.

## Tomorrow AM — PM's stated plan (2026-09-18 22:xx, in-conversation)

PM: "tomorrow am we'll have a blog post to work on. After that we can resume our editorial calendar
planning work." Likely candidate, verified against the calendar: **"Assume It Was You"**
(`docs/public/comms/drafts/assume-it-was-you.md`), status `drafted`, `pubDate` **2026-09-19** —
publishing tomorrow. Fully drafted + fact-checked (2026-07-09), but has **one open PM-input
bracket**: whether the "compaction hand-wave rejection" paragraph is PM's own words or the
Architect's account of PM. That bracket plus the voice-pass are the likely "work on" ask. Not yet
confirmed by PM which post they meant — flagged as the best-fit inference from calendar state, not
a certainty. After that: resume editorial calendar planning (no further detail given yet on what
aspect).

## Waiting on others

- **PM** — voice-pass + art on the ~9-10 drafted items; ChicagoCamps script/slide review.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Someone (unclear who)** — #1636 (filed 08-15); #1647 (filed 08-18).
