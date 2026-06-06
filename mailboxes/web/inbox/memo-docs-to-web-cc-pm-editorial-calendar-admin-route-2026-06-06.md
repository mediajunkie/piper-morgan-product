---
from: Documentation Management (Docs)
to: Web (Unicorn Web Designer)
cc: PM (xian)
date: 2026-06-06
subject: Handoff — Editorial Calendar admin route on the website (always-current GUI) — #1161
priority: standard — PM-assigned feature
---

# Editorial Calendar admin route — handoff (#1161)

PM ratified assigning this to you. I built a v0.1 calendar GUI today (PM loves it); the ask is to make it **always-current** as an admin route on the website instead of a regenerate-to-refresh snapshot.

## What exists to reuse
- **UI v0.1** (yours to port): `docs/internal/planning/comms/editorial-calendar-view.html` — self-contained month-grid; click any day → detail panel (title/theme/status/dates/notes + blog/Medium/LinkedIn links); color-coded published/queued/drafted; today highlighted; collapsible unscheduled-drafts list. Render-verified headless (no JS errors).
- **Generator**: `scripts/build-editorial-calendar-view.py` (reads the CSV, embeds JSON). The snapshot limitation is what #1161 removes.
- **Data source**: `docs/internal/planning/comms/editorial-calendar.csv` (18 cols; canonical; this PRODUCT repo).

## Three pieces (all mirror your existing patterns)
1. **Data sync** — mirror the blog CSV→JSON pipeline (`sync-csv-to-json.js` / `csv-parser.js`) for the editorial calendar → `src/data/editorial-calendar.json`. The one genuinely-new bit is the **cross-repo read** (calendar CSV in product repo, site in website repo) — your publish pipeline already reads cross-repo, so there's precedent.
2. **Admin route** — add `src/app/admin/calendar/` (your `src/app/admin` section + auth/gating already exist).
3. **UI** — port the v0.1 month-grid/click-detail JS into a React component fed by the JSON.

## Recommendation + open decision
**Build-time sync** ("current as of last deploy"; the site rebuilds on push) is the pragmatic default and matches how blog data already flows — recommend starting there. **Truly-live** (runtime/serverless cross-repo read) is possible but more plumbing for marginal gain (the calendar doesn't change minute-to-minute). You + PM confirm the freshness bar.

Effort estimate (mine): ~half-day focused session — UI's done, sync + admin-route patterns exist. **I'm the calendar owner** — ping me anytime for data-shape / column-semantics questions (18-col schema, status/theme values, the workDate-vs-pubDate distinction).

— Docs, June 6
