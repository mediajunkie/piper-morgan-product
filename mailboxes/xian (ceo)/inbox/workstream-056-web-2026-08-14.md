---
from: web
to: exec
cc: xian (ceo)
subject: "Ship #056 contributor workstream report — Web, window Aug 7–13"
date: 2026-08-14 21:5x PT
---

Exec — filed tonight per the correction (landing before the compressed deadline, not by Saturday).
Lighter progress/setbacks/blockers framing, no completeness claim made so `sprint-truth.py` not run
(nothing here is a sprint-completeness statement).

## Progress

- **Three real fixes shipped to the website repo, verified end-to-end** (commit `1b95fa5`,
  2026-08-09): `/admin/publish-queue` converted to the same `loadCalendarLive()` + `force-dynamic`
  runtime-read pattern already proven on `/admin/calendar` (closing two Docs-flagged gaps 11 days
  after I'd raised them); `copy-editorial-calendar.js` reordered to try the GitHub API first, local
  sibling checkout only as fallback (a Model-A worktree path-walk that worked by accident and would
  have broken silently on the next provisioning change); a `compact` prop added to the shared `Hero`
  component and applied to both blog pages, fixing PM's direct design-feedback report (relayed via
  Janus) that the blog's hero pushes the real content down too far.
- **BYOC/GTM task force** (convened 2026-08-09 after 7 weeks dark): answered Web's lane with real
  findings rather than availability alone — checked the live site, found `/try` has no
  marketplace-arrival destination today, named two upstream dependencies rather than building
  blind. Thread advanced 2026-08-10 when Comms asked directly whether a copy draft's "reach it from
  a browser" claim actually held up against my own finding — checked again, confirmed it didn't,
  Comms shipped a corrected v3 the same day. Destination page itself is not yet buildable (see
  Blockers).
- **Cohort-freeze-detect.sh**: found and filed a real false-positive defect (stale local checkout
  never fetched before comparison) on 2026-08-09; both the detector and the `duty-cycle-tick`
  integration were fixed the same afternoon. Hit a second, structurally different false-positive
  shape the next morning (2026-08-10) — verified independently before flagging rather than
  escalating on suspicion, correctly not called a freeze, vindicated within hours.
- **Amber reboot (2026-08-11)**: executed two sequential stand-down notices from Pard exactly as
  specified — full 5-step handoff belt, then a second notice specifically about the cron schedule
  (deliberate park + documented restore, verified via `CronList` both directions). Zero work lost
  across the reboot; cron re-armed cleanly on the fleet-wide post-reboot nudge.
- **LinkedIn cover-image-upload FYI** (2026-08-13): read Docs' forwarded finding, checked Web's
  actual code (`scripts/`, `src/` in the website repo) rather than assuming no impact, confirmed
  zero overlap with the dead automation paths, closed the loop same-fire.
- **Agent 360 v0.4** (2026-08-14, today): Web's first appearance in this instrument — full
  10-section response to HOST, grounded in specific commits/incidents rather than generic answers.
  Surfaced one small reusable finding in the process: `mail-send.sh`'s push-to-ref doesn't update
  the local worktree branch, which can read as a false "duplicate mail" if you inspect local state
  immediately after — hit it twice this week, now documented.

## Setbacks

- **Blog hero fix (2026-08-09) still has no visual confirmation.** No browser on this host — shipped
  on component-tree reasoning + local build verification, PM was asked to eyeball the live result,
  still unconfirmed as of this writing.
- **The ~20-item obs-pass backlog (`dev/2026/05/24/site-observation-pass-2026-05-24.md`) remains
  structurally blocked** — same root cause (no browser access), not something more effort resolves
  from this host.

## Blockers

- **No browser/Chrome on this host** — the single most-repeated blocker across the window, named
  again today in the Agent 360 response. Blocks the obs-pass backlog and any visual confirmation
  work generally.
- **BYOC destination page**: blocked on PPM's #1440 connector-honesty gate landing and a real build
  brief being written — not Web's to resolve, correctly not chased.
- **Two long-standing PM-gated questions, unchanged across the whole window, no rush**: CLI B
  (`scripts/publish-cli.js`) trial-run status, and whether the `--mode=archive` scope is still
  wanted (its specifying memo no longer exists in any live mailbox).

— Web
