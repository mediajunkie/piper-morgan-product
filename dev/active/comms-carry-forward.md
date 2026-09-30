# Comms carry-forward

**Spring-cleaned 2026-09-22** per today's context-floor-reduction plan (item 4a, PM directive via
Exec) — resolved items deleted, not archived with a `was:`/history trail. Full narrative for
anything below lives in the dated session log, not here.

## Cron

`4dcca958`, re-armed at the 2026-09-29 21:42 STOP (delete-then-create from `96576287`, which was
armed 11:12 on the fresh `claude-opus-5-5` session). CronList-verified exactly one job. Full 6x/day cadence
(`12 6,9,12,15,18,21 * * *`), `threshold_h` 7. **Auto-expires ~2026-10-06 (7 days from 09-29 21:42);
re-arm proactively by 10-04** (delete-then-create). Fires today have been arriving ~30 min late (09:42, 12:42), within
tolerance but worth noticing if it grows.

## GitHub criteria line (third work-queue source, duty-cycle-tick v1.33), written 2026-09-29

```
gh issue list --repo mediajunkie/piper-morgan-product --state open --limit 500 \
  --search 'blog OR editorial OR calendar OR "weekly ship" OR comms OR narrative in:title' \
  --json number,title
```
No comms label exists, so this matches on title. **Open each hit with `gh issue view`**: the list
only finds candidates. **48 hits on 2026-09-29 15:42** (the "~15" I wrote at 12:42 came from a narrower
query, before calendar/narrative were added). Most belong to Web/Docs/Arch. Per-fire check = the delta:
any hit with `createdAt` after the last check (newest at 15:42 was #1892, 09-25). Mine or
co-owned: #1683 (calendar syndication residuals, waiting on PM to check Medium), #1905 (empty-cluster
regression, closed by Web same day), #1834 item 2 (language governance, waiting on Exec/CIO).

## Open — no PM-gate, just queue depth

- **"What Piper Morgan Actually Is" (Thu 10-01) → ready-for-docs, publish-ready memo sent 09-29 ~22:15, Docs acked 23:3x (will re-audit fresh on 10-01).**
  All PM calls resolved in conversation. Nothing owed unless it doesn't publish on 10-01. Then remind
  PM to crosspost to Medium.
- **Weekly Ship #062 → ready-for-docs, publish-ready memo sent 09-27.** Both review rounds closed:
  metrics (91/57, three independent confirmations) and art (header confirmed intentional by PM;
  found + fixed a separate real bug — the mid-post embed pointed at a stale Ship #061 asset,
  verified the correct live URL by pattern-match + direct `curl` check before fixing). Target
  publish Wed 09-30 — no action needed unless it doesn't land.
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
- **Language-governance mechanism, part 2**: HOST named Comms for eventual reconciliation once
  Exec/CIO build the internal-reports check (#1834 item 2).
- **HTML calendar view has no `planned`-status CSS case** (falls back to `drafted` styling) —
  cosmetic, low priority.
- **workDate accuracy audit** — broader pass still blocked on PM naming where the archive lives.

## This seat's standing errors (deduplicated)

- **Search my own logs before asking PM to verify something.** 09-29 I asked PM to check whether
  "Drained on Paper" was on Medium. My own 08-30 log already held Dispatch-PM's platform-level
  answer (confirmed unsyndicated). `grep -ri "<title>" dev/2026/` first. PM's attention is the scarce resource.

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

## Syndication owed (PM crossposts by hand; remind PM in conversation, not by memo)

Re-verified 2026-09-30 06:39 against the calendar. Docs owns the mechanical re-check (Step 1f).
- **"Drained on Paper" (08-07) → Medium: CONFIRMED UNSYNDICATED**, not a record gap. The 08-30
  platform check by Dispatch-PM is in my own 08-30 log. Docs flagged it to PM 09-29. Owed: PM crossposts.
- **Weekly Ship #062** (09-30, today) → LinkedIn, once live.
- **"What Piper Morgan Actually Is"** (10-01) → Medium, once live.
- Resolved 09-29/30: "Three Seats" (Medium URL recorded), Ship #058 (LinkedIn ran 09-02, URL was
  never recorded, Docs filled it in).

## Waiting on others

- **PM** — voice-pass + art on other queued drafts; ChicagoCamps outcome; archive location for the
  workDate audit; a decision on the mining-pass recommendations report (sent 09-25, not
  auto-scheduled — see below).
- **HOST** — Agent 360 v0.5 synthesis (my response sent 09-27), ~4 weeks out.
- #1905 **closed by Web 09-29** (backfilled + `publish-post.js` now derives cluster from workDate, `e2baf72`; I verified 0/404 empty on website origin/main. Rendered Eras page unverified: client-rendered, curl can't see it). #1636 closed 09-29 with evidence (historical gap fixed by website#39). #1647 is closed.
- **PM** — #1683: crosspost "Drained on Paper" to Medium (confirmed missing). "Building for Learning" is still unchecked (historical, low stakes).

## Recurring — biweekly editorial mining pass (PM-ratified 09-23, LIVE)

**First pass complete 2026-09-25.** 24 days surveyed (Sep 1-24), 24/24 mechanically verified (23
candidate / 1 thin), full recommendations report sent to PM's inbox
(`mailboxes/comms/sent/comms-mining-pass-2026-09-25.md`) — 13 chronological beat-candidates + 15
insight candidates, nothing auto-scheduled. **Next due: 2026-10-09** (steady 14-day cadence from
here). Full procedure in `comms-standing-items.md` § "Recurring practices."
