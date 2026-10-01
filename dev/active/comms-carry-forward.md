# Comms carry-forward

**Spring-cleaned 2026-09-22** per today's context-floor-reduction plan (item 4a, PM directive via
Exec) — resolved items deleted, not archived with a `was:`/history trail. Full narrative for
anything below lives in the dated session log, not here.

## Cron: mid-migration, cascade seat 5 (PM-approved 10-01)

- **LaunchAgent `com.xian.pm-comms-cycle` armed by Pard, 6×/day at :19** (06–21). First fire
  10-01 12:19, landed on the minute. The prompt names both worktrees.
- **Session cron `4f4203ad` STAYS armed** (`12 6,9,12,15,18,21`, auto-expires ~10-07, re-arm at
  every STOP). Expect double fires (:19 LaunchAgent, ~:40 session cron). They're idempotent, and the
  second one should find nothing new.
- **Delete the session cron only when Pard confirms a `consumed` verdict** in his comms-cycle log.
  Then `CronDelete`, `CronList`-verify it's gone, flip the registry row, and tell Exec. After that,
  "No scheduled jobs" is NORMAL, not Gap-C. The duty-cycle-tick cron gate applies.
- Told Pard 10-01 (via Exec): fires take under 1 to about 2 min, the +28–30 is dispatch lateness
  (first-command `date` readings), and the prompt's `cron=` should become :19 after cutover.

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

- **10-04 gap FIXED 10-01 (PM chose option 2)**: Distribution → Sun 10-04, No Undo → Sat 10-10, NEW
  "Success Is Indistinguishable From Skipping" drafted for Sun 10-11 (943 words, self-audit clean,
  needs PM voice pass + art). 4 teases re-chained, and Docs was told Saturday's tease changed.
  **"Distribution" needs PM voice pass + art by Sat 10-03** (PM has the Nat Geo talk Fri).
- **Insight queue ends after 10-11**: Sat/Sun 10-17, 10-18, 10-24 and 10-25 are empty. Feed from the
  09-25 mining-pass insight list (top: "Convergent Claims Aren't Independent Evidence").
  Raised to PM 10-01.
- **"Described Is Not Running" (Sat 10-03) → ready-for-docs, publish-ready sent 10-01 (`a460b7460`).** Then Medium crosspost (PM).
- **Weekly Ship #062 → ready-for-docs, publish-ready memo sent 09-27.** Both review rounds closed:
  metrics (91/57, three independent confirmations) and art (header confirmed intentional by PM;
  found + fixed a separate real bug — the mid-post embed pointed at a stale Ship #061 asset,
  verified the correct live URL by pattern-match + direct `curl` check before fixing). Target
  publish Wed 09-30 — no action needed unless it doesn't land.
- **Drafts awaiting PM's voice-pass** — re-query the calendar fresh before quoting a count; a
  carried number went stale once already (09-20).
- **ChicagoCamps (09-17) CLOSED 10-01**: PM says it went great, it's now public (also on the Design
  in Product site), and there's no Granola transcript. **Nat Geo AI speaker series opener: Fri 10-02**, similar title.
  Both are Ship #064 External-relations material (the 10-02 talk falls in that window). Standing item:
  a talks & appearances hub on the Piper site.
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

- **A cascade/reshuffle must verify slot contiguity, not just the tease chain.** 09-08 I "pushed every
  insight back by one position" but jumped Distribution from 10/3 to 10/10, which left Sun 10/4 empty.
  My full-chain footer verification passed because it checks teases, not dates. PM noticed 10-01.
  After any reshuffle, list every Sat/Sun slot in range and confirm each is filled (or deliberately empty).

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

**Nothing owed as of 2026-10-01 09:40.** "What Piper Morgan Actually Is" was crossposted to Medium
by PM 10-01. **"Drained on Paper" is CLOSED as `not-syndicated`** (PM ruling 10-01, decisions.log): a
new terminal status meaning locked, neither crossposted nor pending. **I only ever write
`not-syndicated` on PM's explicit say-so for a specific post.** The default for a missed crosspost is
still a reminder to PM. Next owed: "Described Is Not Running" → Medium after it goes live 10-03.

## Waiting on others

- **PM/Web** — #1908 (narrative sequence-number field, PM "not urgent"). I added data 10-01: the existing Beat
  labels are per-arc, so they can't serve as a global sequence, and workDate is the viable backfill source.

- **PM** — voice-pass + art on other queued drafts; archive location for the
  workDate audit; a decision on the mining-pass recommendations report (sent 09-25, not
  auto-scheduled — see below).
- **HOST** — Agent 360 v0.5 synthesis (my response sent 09-27), ~4 weeks out.
- #1905 **closed by Web 09-29** (backfilled + `publish-post.js` now derives cluster from workDate, `e2baf72`; I verified 0/404 empty on website origin/main. Rendered Eras page unverified: client-rendered, curl can't see it). #1636 closed 09-29 with evidence (historical gap fixed by website#39). #1647 is closed.

## Recurring — biweekly editorial mining pass (PM-ratified 09-23, LIVE)

**First pass complete 2026-09-25.** 24 days surveyed (Sep 1-24), 24/24 mechanically verified (23
candidate / 1 thin), full recommendations report sent to PM's inbox
(`mailboxes/comms/sent/comms-mining-pass-2026-09-25.md`) — 13 chronological beat-candidates + 15
insight candidates, nothing auto-scheduled. **Next due: 2026-10-09** (steady 14-day cadence from
here). Full procedure in `comms-standing-items.md` § "Recurring practices."
