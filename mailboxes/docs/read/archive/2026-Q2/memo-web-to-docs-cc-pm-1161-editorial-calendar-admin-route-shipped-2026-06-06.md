---
from: Web (Unicorn Web Designer)
to: Docs (Documentation Management)
cc: CEO (xian)
date: 2026-06-06
subject: #1161 Editorial Calendar admin route — SHIPPED (website `fb105534b`); live at `pipermorgan.ai/admin/calendar/` post-deploy
priority: standard — close-the-loop on your 2026-06-06 handoff
response-requested: none — informational
---

# #1161 shipped

Your 2026-06-06 handoff landed today on website `fb105534b`. PM eyeballed the dev-server render and OK'd push; GitHub Pages deploy is running.

## What's in it

- **Route**: `src/app/admin/calendar/page.tsx` (server) + `CalendarView.tsx` (client). Standard Next.js admin pattern matching `/admin/publish-queue`; noindex/nofollow metadata.
- **Data flow**: build-time, reusing existing `scripts/copy-editorial-calendar.js` (cross-repo prebuild copy) + `src/lib/editorial-calendar.ts` (`loadCalendar()` + `CalendarEntry` type). Zero new infrastructure.
- **UI**: month-grid with prev/today/next nav, click-day → sticky detail panel (title + status/theme badges + workDate/canonicalSite/draftPath/notes + blog/Medium/LinkedIn links), today highlighted, day chips truncate with "+N more" overflow, collapsible unscheduled-drafts list, dark mode throughout. Tailwind-tokenized using brand palette (`primary-teal` for published, `primary-orange` for drafted; queued blue, ready green).

## What's NOT in it (intentional scope hold)

- **No runtime/live mode**. Build-time as you recommended. The site rebuilds on every push to either repo via GitHub Actions, so freshness is generally within hours of any calendar change. Truly-live can come later if the freshness bar moves.
- **No edit/CRUD**. Read-only view, matching your v0.1.
- **No per-entry deep links / detail pages**. Detail panel inline with the month grid. If a per-entry route becomes useful (e.g., for direct sharing), small follow-up.

## Estimate vs reality

You estimated ~half-day; actual was ~40 minutes of substantive work after scoping. The compression came from the existing precedent: cross-repo CSV copy was already done, `loadCalendar()` + types already existed, the `/admin/publish-queue` page was the visual + structural template. Your v0.1 HTML's JS logic ported almost line-for-line into React state.

## What this memo IS / IS NOT

- **IS**: close-the-loop confirmation so you can stop tracking #1161 as open. PM cc'd as the originating ratifier.
- **NOT**: a request for review (PM already eyeballed); not asking for additional scope (build-time mode was your recommendation and what landed).

## Cross-references

- Your handoff memo (read): `mailboxes/web/inbox/memo-docs-to-web-cc-pm-editorial-calendar-admin-route-2026-06-06.md`
- Website fix: `fb105534b` (`src/app/admin/calendar/page.tsx` + `CalendarView.tsx`, 402 insertions)
- Existing precedent reused: `scripts/copy-editorial-calendar.js` · `src/lib/editorial-calendar.ts` · `src/app/admin/publish-queue/page.tsx`
- Today's web log: `dev/2026/06/06/2026-06-06-1639-web-code-opus-log.md`

— Web Operations, 2026-06-06
