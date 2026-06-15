# Web session — 2026-06-14 15:19

**Role**: Unicorn Web Designer (piper-morgan-website)
**Trigger**: PM check-in 3:19 PM, Sunday. "Yes this is a huge improvement. Let's ship it." (blog type-scale change from 6/13 dev-server eyeball). Also new task: explore the GitHub project board (PAT now has Projects access; board at https://github.com/users/mediajunkie/projects/2/views/2 is "somewhat moribund"; PM thinks stale issues exist, e.g. form signup).
**Mode**: substrate close-out + project-board exploration with `gh` tool.

## Re-orient (15:19)

### Mail
- Inbox: empty (Docs's 6/13 tidy-up triaged this fire as already-addressed).

### Repo state
- Website main: top `2263e89ba` fix(blog) type-scale rebalance — JUST SHIPPED this fire; Pages deploy running.
- Product main: cohort active; nothing affecting web directly.

### Outstanding queues
- Visual-scan re-walk still PM-react gated (will now benefit from type-scale change deploying too).
- All other PM-react-gated queues unchanged.

## This session — planned

1. Close 6/13 + open this log + triage Docs tidy-up + commit substrate batch (in progress; commit imminent).
2. **Explore the GitHub Projects board** (`gh project ...`) — get the lay of what's been tracked, identify stale items (form signup mentioned by PM as likely candidate), surface for PM discussion.

### Notes on project board exploration
- PM granted PAT scope today; this is the first time I can see the board.
- "Somewhat moribund" framing means PM expects to find more there than is currently active — surface old open items, mark obvious closes, ask about ambiguous ones.
- Form-signup is explicitly called out by PM as a likely stale item. Worth checking what's there about it.
- Will report findings inline rather than make changes unilaterally on the board (PM still owns issue triage on a board that's been quiet a while).

## Shipped this session — type-scale + board audit

### 1. Blog type-scale rebalance (shipped — see 6/13 log close-out)
Website `2263e89ba`; live and deployed. PM eyeballed dev render: "huge improvement."

### 2. Project board audit + revival
PM picked: backfill recent + forward / verify-close #17 + leave #18 open with note / file form-signup as new issue.

**Findings on the original 18-item board:**
- 16 CLOSED (entire SITE-001 → SITE-009 sprint-01 series from Aug-Sep 2025).
- 2 OPEN bugs from April 2026: #17 dedup + #18 alt text.

**Actions taken on existing issues:**
- **#17 CLOSED** with verification comment. Empirically verified: 0 prefix-match duplicates in current data; 0 Medium-only posts in merged set; dedup architecturally hardened beyond the equality-only check the bug described (now uses editorial-calendar.csv correspondence + slug-match fallback).
- **#18 commented + LEFT OPEN**. Code fix is in (`fetch-blog-posts.js` reads `metadata.imageAlt`/`imageCaption`). Coverage: 55/330 (16%) blog-first posts have alt; 275 historical posts still need backfill. Open as backfill tracker.

**New issues filed:**
- **#19 OPEN** — Newsletter signup form provider decision (Formspree vs stay on ConvertKit). PM-decision blocked. Captures the standing-items TODO that wasn't on the board.
- **#20 CLOSED** — Tailwind v4 @config fix (5/29 `0d406ad3f`).
- **#21 CLOSED** — publish-post.js inline-image + edit-pass hashId reuse (5/29 `b097a997e`; two bugs in one commit).
- **#22 CLOSED** — publish-post.js converter gaps (`*`/`+` bullets + fenced code; 6/1 `d2f5b9394`).
- **#23 CLOSED** — publish-post.js workDate silent-default (6/3 `c17c43fc4`).
- **#24 CLOSED** — Editorial Calendar admin route #1161 (6/6 `fb105534b`).
- **#25 CLOSED** — Blog type-scale rebalance (6/14 `2263e89ba`).

**All 7 added to project board.** Total items now 25 (was 18).

**Board state, post-revival:**
- 23 CLOSED (16 historical sprint-01 + 6 recent retroactive + #17 fresh-closed today)
- 2 OPEN with clear status:
  - #18 — code fixed, awaiting historical backfill (275 posts × manual alt text, ~25-45hr)
  - #19 — PM-decision-blocked (Formspree vs ConvertKit)

## Pending PM
- #19 Newsletter signup form provider decision (board-tracked now).
- #18 historical alt-text backfill — substantial editorial work; defer/scope as PM's call.
- Visual-scan re-walk still PM-react gated.
- All other PM-react-gated queues unchanged.

## Shipped this session (continued) — production CSS cascade bug

PM screenshot at 18:28: site nav + hero CTA buttons rendering as empty teal rectangles (text invisible). Diagnosed: CSS Cascade Layers ordering bug in globals.css.

**Root cause**: globals.css base rules (including `a { color: var(--primary-teal); }`) were OUTSIDE any `@layer`. Tailwind v4 utilities live in `@layer utilities`. Per cascade-layers semantics, unlayered rules win over layered rules REGARDLESS of specificity. So `.text-white` (utility) lost to `a {}` (unlayered), making white-on-teal text render as teal-on-teal = invisible. Latent since the @config bridge (5/29) — that fix made bg-primary-teal render at all; this counterpart bug made the text invisible on top of it.

**Fix**: wrapped globals.css base rules in `@layer base { ... }`. Now utilities win as Tailwind v4 intends. Verified via cascade-tracking on built CSS.

**Shipped**: website `6e1364524`. Pages deploy propagating.

**Issue #26 filed retroactively**: closed-as-done, added to project board. Discipline pattern continues — production-visible web work goes on the board even when shipped same-fire.

## Project board count update
Now **26 items total** (was 25 after the earlier audit). Going forward: file board issues for production-visible web work as it lands.

## Close-out (appended 2026-06-15 07:30, re-applied after botched 06:54 commit)

Productive 6/14 session — type-scale rebalance ship + project board revival (8 issues touched) + production CTA-invisible-text cascade-layers fix shipped same-day.

**Gap to 6/15 (~6/14 19:01 → 6/15 06:54, ~12 hours)**:
- 1 new memo (Lead 6/14 lane reconciliation; PM asking via Lead for current focus + repo note)
- Website main: no commits
- Product main: cohort activity

**Re-apply note**: A close-out + MANIFEST updates I attempted in the 06:54 fire didn't actually commit — the staging silently caught cohort autostash debris instead of my files. Docs's omnibus pass flagged it at ~07:26. Re-applying this fire. See 6/15 log for the full diagnosis.

Signed off — Web. End of session 2026-06-14.