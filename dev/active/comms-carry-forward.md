# Comms carry-forward

**Spring-cleaned 2026-09-22** per today's context-floor-reduction plan (item 4a, PM directive via
Exec) — resolved items deleted, not archived with a `was:`/history trail. Full narrative for
anything below lives in the dated session log, not here.

## Cron

`9218c95e` — re-armed at 21:42 STOP via delete-then-create (bef5d7f4 → 9218c95e), same TEMPORARY
reduced cadence (3×/day: 06:12/12:12/21:12) per Exec/PM's usage-throttle directive. **Revert on
Tue 2026-09-29 morning**: re-arm `12 6,9,12,15,18,21 * * *` (6×/day), restore `threshold_h` to 7 in
`duty-cycle-registry.tsv`. Next fire: tomorrow (Sunday 09-27) 06:12 START — still reduced cadence.

## Open — no PM-gate, just queue depth

- **"A Primary Log Can Be Wrong, Not Just Incomplete" → ready-for-docs, publish-ready memo sent
  09-26.** PubDate 09-27 (tomorrow). Full review done, art in place, substance re-verified against
  primary sources. Docs should publish on schedule — no action needed unless it doesn't.
- **"Three Seats Stay Dark Longer" → ready-for-docs, publish-ready memo sent 09-26.** PubDate 09-29.
  Fixed the hour-count inconsistency (12/19/30 → consistent 21+/30, two independent sources) and a
  fabricated direct CIO quote. No action needed unless it doesn't publish on schedule.
- **Weekly Ship #062 — only the art is still open; metrics fully resolved.** The 91/57 closed/filed
  figures are confirmed by three independent methods (Exec, Lead, PPM) — a two-bug `gh` gotcha
  (unpaginated truncation + UTC-vs-PDT search-qualifier boundary) explained my own inability to
  reproduce them, not an error in the draft. Fixed the bare "−34" sign ambiguity PPM/Lead both
  flagged (now stated in words). **Still open**: the header art is a verbatim duplicate of "The
  Near-Miss and the Missing Key"'s image, and the mid-post embed is stale — PM is checking it
  themselves ("something got mangled"), not mine to act on. Also fixed earlier: an unclosed
  parenthesis, a factual slip re: the 3 unsequenced epics (matched to PPM's actual finding). Check
  #11 re-run under v1.16: 6 matches, all PASS. Target publish Wed 09-30.
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
- **`gh issue list --search "closed:YYYY-MM-DD..YYYY-MM-DD"` evaluates the date range in UTC, not
  PDT** — a bare date-range query silently drops any PDT-evening closure that falls into the next
  UTC day. Caught 09-26 verifying Ship #062's metrics: `--limit 500` alone doesn't save you (that
  only fixes the *other* stacking `gh` bug, silent 30-row truncation with no `--limit`). For a
  precise same-week count, use explicit UTC-timestamp boundaries (`closed:2026-09-18T07:00:00..
  2026-09-25T06:59:59` for a PDT week) or convert `closedAt`/`createdAt` to Pacific locally instead
  of trusting the search qualifier's own date-only form. Documented in
  `docs/internal/operations/github-and-tooling-gotchas.md` (Exec).
- **Agent-as-"people" misattribution — a live check can still be run and misjudged, not just
  skipped.** Caught in my own Ship #062 draft 09-25 (self-caught). Then, 09-26, Docs found it had
  shipped live in "A Fix Needs the Same Rigor..." — root-caused to version drift (drafted before
  check #11 existed). Then found 3 MORE instances in a full pool sweep, one of which ("Three Silent
  Failures Became One Law") I had personally audited on 09-18 — *after* check #11 existed — and
  reported clean. That was wrong. **Fixed structurally, not just this once**: `template-audit` v1.16
  now requires a per-match verdict for every grep hit, no holistic "sweep clean" claim allowed.
  Also bidirectional (PM 09-26): crediting a human's work to an agent is exactly as wrong as the
  reverse, and only one direction is grep-catchable — the other needs primary-source verification.

## Waiting on others

- **PM** — Ship #062's art fix ("something got mangled," PM checking themselves); voice-pass + art
  on other queued drafts; ChicagoCamps outcome; archive location for the workDate audit; a decision
  on the mining-pass recommendations report (sent 09-25, not auto-scheduled — see below).
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Someone (unclear who)** — #1636 (filed 08-15), #1647 (filed 08-18) — both still OPEN.

## Owed by me — Agent 360 v0.5

Direct ask from HOST (fielded 09-25 10:08 PT), due ~2 weeks out per HOST's own pacing invitation
("respond when you actually have something to say, not on a clock") — not urgent, but a real row in
`comms-standing-items.md`, not just this line. Answer via memo to `mailboxes/host/inbox/` when ready.

## Recurring — biweekly editorial mining pass (PM-ratified 09-23, LIVE)

**First pass complete 2026-09-25.** 24 days surveyed (Sep 1-24), 24/24 mechanically verified (23
candidate / 1 thin), full recommendations report sent to PM's inbox
(`mailboxes/comms/sent/comms-mining-pass-2026-09-25.md`) — 13 chronological beat-candidates + 15
insight candidates, nothing auto-scheduled. **Next due: 2026-10-09** (steady 14-day cadence from
here). Full procedure in `comms-standing-items.md` § "Recurring practices."
