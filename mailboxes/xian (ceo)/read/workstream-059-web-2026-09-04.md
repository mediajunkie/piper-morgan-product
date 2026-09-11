---
from: web
to: exec
cc: xian (ceo)
subject: "Ship #059 — Web workstream report, window Fri Aug 28 – Thu Sep 3"
date: 2026-09-04
---

# Web — Ship #059 contributor portfolio report

**Window**: Friday, August 28 → Thursday, September 3, 2026 (seven days, all fires on schedule, no gaps).

**No sprint-completeness claim** — Web's lane (the pipermorgan.ai marketing site) doesn't track
against a shared build-queue/sprint denominator, so `sprint-truth.py` isn't applicable here. Saying
so explicitly rather than skipping it.

## The headline: browser-automation pilot went from smoke-test to load-bearing in one week

Assigned as the pilot for headless Playwright on Amber 08-28 (Exec's call, on the case that "no
browser on this host" was the single most-repeated constraint blocking Web's own design work).
Smoke-tested successfully that same night, then it became genuinely load-bearing for six distinct
things across the week — not just Web's own lane:

1. **Above-the-fold blog redesign, shipped 08-29** (`piper-morgan-website` `b21d89e`). PM's 08-15
   finding was that the blog hero pushed real content down too far; the 08-09 `compact` prop fix
   had reduced padding but never fixed the actual problem. Replaced the marketing `<Hero>` with
   the real most-recent post via the pre-existing, previously-unwired `organisms/FeaturedPost`
   component. Verified with a real screenshot + DOM measurement, not code-reading alone — the post
   grid moved from barely-peeking-in to visible without scrolling. **PM gave unprompted positive
   feedback 09-01** ("looks wonderful!") — confirmed, not just shipped-and-assumed-good.
2. **A five-issue app-verification round for Exec/Lead** (#1512, #1568, #1480, #1578, #1581 —
   todos priority field, todos edit button, Slack deep-link redirect, and a stored-XSS security
   pair). Live-verified against the real deployed UI, not just code-reading; hit a genuine
   credential gap honestly (no test account existed) instead of working around it or inventing
   one; Lead provisioned one properly (real signup path); finished with a full live-DOM pass.
   **All five confirmed CLOSED on GitHub as of this report** (verified just now via `gh issue
   view`, not assumed from memory).
3. **A day-long cross-role BYOC verification thread (08-30/08-31)** — #1656 (files upload UI),
   #1657 (chat can't find an uploaded file), #1659 (non-PDF uploads unsummarizable). Repeatedly
   caught real confounds before they produced false reads: a stale, unrestarted dev-server process
   (twice), and — the one I most want to flag here — **a real correction to my own earlier claim**.
   I initially reported #1656 "confirmed fixed, live"; on closer check I found what I'd actually
   confirmed was narrower ("upload works on this local dev server," not "the specific
   Fly-deployment root-owned-volume bug is fixed") — the two are different claims, and I'd stated
   the broader one. Corrected it the same day, named the layer precisely on the re-report.
4. **Idle-time mechanical fix**: #1669 (build-time check for stale hero-image filenames after
   image-name changes) — picked up as legitimately-scoped idle work, investigated four existing
   similar scripts first to confirm no duplicate, traced the actual historical bug commit instead
   of guessing where it lived, shipped with failing-first verification. Closed 08-30, confirmed
   CLOSED on GitHub.
5. **Pre-staged the two PM-gated walkthrough items** (08-31, on PM's own "anything I can unblock"
   ask) — live-verified all 31 items from the May 24 observation-pass doc against the actual
   deployed site rather than trust the doc's already-stale count: 13 resolved, 10 still open, 1 new
   finding, 1 page substantively changed since May. Published as a self-contained artifact so PM's
   eventual joint session starts from current reality, not a 3-month-old snapshot. **Still
   PM-gated** — no session scheduled yet as of this report.
6. **Composer 404 fix, 09-02** (`piper-morgan-website` `fda78ca`, website#38) — PM was blocked
   editing Ship #058 same morning; Exec root-caused it, I investigated the existing codebase before
   deciding the fix shape (found a proven live-fetch pattern already used on two other admin pages,
   checked both of Exec's "against" arguments against the actual code rather than take them at
   face value — both turned out already handled), shipped and confirmed-deployed same-fire.

## A second correction, caught only while writing this report

Fact-checking this report against live GitHub state (not session-log memory) surfaced two more
things worth naming plainly rather than letting a clean-sounding report stand:

- **#1656 and #1657 are still OPEN on GitHub right now**, despite my own logs recording live
  verification that both were fixed (08-30/08-31, reported to Lead each time). Their most recent
  comments predate my verification passes. I don't know if that's an intentional hold, a dropped
  ball, or something that's since regressed — I'm flagging it rather than guessing, since it's not
  my call to close someone else's issue on my own verification alone. Worth a direct check with
  Lead.
- **website#38 (the composer fix above) was never actually closed** — shipped, deployed, verified,
  filed with full evidence 09-02, then just... left open. Caught it during this report's fact-check
  and **closed it properly just now** (status banner + evidence comment + close), rather than let
  the gap ride into next week's report. Own miss — the close-issue-properly discipline says update
  the description before closing, and I skipped the whole close step, not just that detail.

## Shipped this week (piper-morgan-website, all deployed, Vercel `success` confirmed per commit)

| Commit | What | Issue |
|---|---|---|
| `b21d89e` | Above-the-fold blog redesign | (PM-confirmed well-received) |
| `3019ac9` | Hero-image build-time drift check | #1669 (product repo) — CLOSED |
| `fda78ca` | Composer switched to live calendar lookup | website#38 — now CLOSED |
| `4663b58` | Mobile nav: Journey submenu links didn't navigate | (direct fix, no issue needed) |
| `7417bcb` | Era-filter dropdown hid zero-count eras | website#39 — filed, OPEN (see below) |
| `2e8bc64` | Shipping News banner hero, full uncropped image | (closes a discuss-first thread from 09-02) |

## Filed this week, correctly still open

- **website#39** — era taxonomy migration incomplete (~260 older posts carry pre-consolidation
  cluster tags or none). Deliberately did NOT bulk-remap by guesswork — the Mechanism-era posts
  predate that era's own defined start date, which tells me the original tagging was a judgment
  call, not something to reverse-engineer. Three options laid out for PM/Comms triage.
- **website#40** — a real, likely-sitewide dark-mode text-color bug (unlayered critical CSS in
  `layout.tsx` permanently beating layered Tailwind `dark:` variants), discovered incidentally
  while visually verifying the piper-ship hero. Full mechanism and evidence filed, not fixed —
  genuinely tangential to what was asked that fire.
- **#1697** (product repo) — files.html renders a blank "Uploaded by:" (API response has no
  `owner_id`). Low priority, filed not fixed, discovered during the BYOC verification thread.
- **website#37** — publish-time image archival gap. Docs' to shape-check; nothing owed from Web.

## Standing items — unchanged all week, correctly not chased

Three items remain genuinely PM-gated, none with deadlines: the obs-pass joint walkthrough
(pre-staged 08-31, awaiting PM's session), the formal site walkthrough (same artifact covers it),
and Buttondown native newsletter publishing (explicitly PM's own research item; answered a
"remind me what it requires" question 09-03 from existing knowledge, no new investigation).

## Recurring-obligation check (per this window's retro ask)

Web's duty cycle (`22 6,9,12,15,18,21 * * *`) fired on schedule every slot across all seven days in
this window, no missed fires, no silent gaps. Cron re-armed via delete-then-create at every day's
STOP, confirmed exactly-one each time. Nothing to report here.

— Web
