# Web session — 2026-06-06 16:39

**Role**: Unicorn Web Designer (piper-morgan-website)
**Trigger**: PM check-in 4:39 PM, Saturday. PM wants to talk through the launch steps because they're "reduced to the point that I don't understand them anymore."
**Mode**: substrate + walk through launch with PM in detail.

## Re-orient (16:39)

### Mail (2 fresh, both important)
1. **CIO 6/5 — Variant RATIFIED** ([memo](../../mailboxes/web/inbox/memo-cio-to-web-cc-pm-pa-variant-ratified-explicit-paths-is-the-condition-2026-06-05.md)). My main-direct 2×/day variant is registered in `cron-shape-experiments.md` as the **5th registered shape + first main-direct one**. Explicit-paths-only on `git add` is named the load-bearing condition / falsification tripwire. CIO accepted all three reasons (separate-repo decisive; tiny product-main footprint; `check-branch.sh` forces mail to main anyway). Closing language: "No further action needed from you; goes live whenever PM operator-launches."
2. **Docs 6/6 — Editorial Calendar admin route (#1161)** ([memo](../../mailboxes/web/inbox/memo-docs-to-web-cc-pm-editorial-calendar-admin-route-2026-06-06.md)). PM-assigned feature. Half-day estimate. Three pieces:
   - **Data sync**: mirror the blog CSV→JSON pipeline for editorial-calendar.csv (cross-repo read: product → website build).
   - **Admin route**: `src/app/admin/calendar/` (admin section already exists).
   - **UI port**: take the v0.1 HTML from `docs/internal/planning/comms/editorial-calendar-view.html` (product repo) into a React component.
   - Recommended: **build-time sync** ("current as of last deploy"), matching how blog data already flows. Truly-live (runtime serverless) is possible but marginal gain for a calendar that doesn't change minute-to-minute.

### Repo state
- Website main: top `7ebcf5787` *Be Prepared* (insight; workDate 2025-12-09). publish-post.js with workDate-from-dateline working. Tree dirty only with build artifact.
- Product main: ~237 cohort commits since 6/5.
- Worktree `claude/web-cycle`: still at 5/29 substrate-prep state (now deprecated — variant uses main-direct, no worktree).

### Status: variant is fully ready and ratified
- Cron prompt: `dev/active/web-cron-prompt-v0.7.md` (main-direct 9:57am START + 11:57pm STOP).
- CIO ratification: done (6/5 16:40 PT).
- Registry: web is row 5.
- Launch: pending operator action — **PM wants to talk through this clearly before doing it**.

## This session — planned

1. **Wrap 6/5 + open this log + refresh inbox MANIFEST** (in progress; this commit).
2. **Walk PM through the launch steps in detail** — surface the over-compression and give a step-by-step the PM can actually act on.
3. After launch is clear: queue or schedule the **#1161 editorial calendar admin route** as the next substantive PM-handoff session (half-day; PM-handoff appropriate).

### Outstanding (carried + new)
- **#1161 calendar admin route** — substantive, half-day, PM-handoff appropriate. NEW today.
- All prior PM-react-gated queues unchanged (visual-scan, obs-pass, walkthrough, lint, CLI B trial-run, Formspree form).

## Shipped this session — cycle stand-down + #1161 scoping

### Cycle stand-down (PM directive)
PM asked: "I have not had to set up doppleganger sessions for any other agents, so something may be getting lost in translation." Standing down on the cycle launch — substrate stays in repo (no harm), variant remains registered as row 5 in `cron-shape-experiments.md`, mail-awareness reverts to manual (web checks inbox when PM convenes). PM wants to revisit "daily mail check" mechanism once substantive backlog clears.

Filed memo to CIO (cc PM): `mailboxes/cio/inbox/memo-web-to-cio-cc-pm-mental-model-mismatch-on-cycle-session-launch-2026-06-06.md` — summarizes my probable mental-model error on how cohort sessions launch + clarification request (no urgency).

### #1161 scoping — way more precedent than expected

Existing infrastructure already in place (Docs's "half-day" estimate is generous):
- **`scripts/copy-editorial-calendar.js`** — already runs as prebuild; copies product `editorial-calendar.csv` → website `data/`. Graceful fallback.
- **`src/lib/editorial-calendar.ts`** — already exists with `CalendarEntry` type (all 18 fields), `loadCalendar()`, `sortByPubDate`, `readyToPublish`, `recentlyPublished`, `syndicationGaps`, `imageMetadataGaps`. Uses `csv-parse/sync` (dep present).
- **`src/app/admin/publish-queue/page.tsx`** — existing sibling admin page; established server-component pattern reading the calendar at build time.
- **v0.1 UI logic** (157 lines vanilla JS in the HTML) — clear month-grid + click-detail + nav + unscheduled list logic to port.

**What I actually need to build (3 things)**:
1. **`src/app/admin/calendar/page.tsx`** (server component) — reads `loadCalendar()`, groups by pubDate, splits unscheduled, passes to client component. ~30 min.
2. **`src/app/admin/calendar/CalendarView.tsx`** (client component) — port v0.1 JS to React state (`useState` for current month + selected day); Tailwind styles matching the v0.1 palette but consistent with site tokens. ~1-1.5 hr.
3. **Quick test pass + Tailwind-token polish + build verify** — ~30 min.

**Revised estimate**: 2-3 hours, not half-day.

**Open design decisions surfaced to PM** before implementing.