# Dashboard A — `/admin/publish-queue` — work checklist

**Started**: 2026-05-16 11:58 (started after PM greenlit the three Dashboard A leans)
**Scope**: Build-time admin page at `/admin/publish-queue` that surfaces editorial calendar state. v1 = read-only queue view; control surfaces deferred until CLI B exists. Human-first + agent-ready dual-purpose surface.
**Spec source**: my morning triage memo + Docs's consolidated feedback memo + [[publishing-ui-block-queued-2026-05]] memory.

## Decisions made (PM-confirmed)

1. **Data source**: prebuild script copies `editorial-calendar.csv` from product repo into website's `data/` dir. Symmetric with the existing `medium-posts.json` build-time fetch pattern.
2. **Route**: `/admin/publish-queue` (memorable, no obscure-slug). Noindex+nofollow meta + minimum-fuss path. Surface is read-only summary of data already in the public source repos.
3. **v1 surface**: queue state only. No control-surface stubs (no "publish this" buttons yet). Defer until CLI B exists.
4. **Agent-readiness**: data-attributes on every row + `<script type="application/json">` block with full structured state. Semantic HTML (proper `<table>` / `<thead>` / `<time datetime>` / `<a>` with rel attributes).

## Surface contents (v1)

Four sections, in order:

1. **Ready to publish** — rows with `status` in `{ready, queued, drafted}`, ordered by pubDate ascending. Shows: pubDate, status, theme, title, draftPath (if present), notes.
2. **Recently published** (last 14 days) — `status=published` with pubDate within 14 days of today, ordered by pubDate descending. Shows: pubDate, theme, title, blogURL, mediumURL, linkedinURL.
3. **Syndication gaps** — `status=published` AND `canonicalSite=distributed` AND (`mediumURL` empty OR `linkedinURL` empty). Ordered by pubDate descending. Shows: pubDate, theme, title, blogURL, which gap (medium/linkedin/both).
4. **Image-metadata gaps** (subtle agent value) — `status=published` AND (`altText` empty OR `caption` empty), last 30 days. The alt-text/caption work I did earlier today suggested this is a recurring quality issue worth surfacing.

Top of page: timestamp of last build (so freshness is visible), counts per section, link to "view raw data" (the embedded JSON).

## Subtasks (sub-commit checkpoints)

- [x] **1. Prebuild copy script** — `scripts/copy-editorial-calendar.js` reads from product repo via sibling-dir path, writes to `data/editorial-calendar.csv`. Idempotent; skips-with-warning if source missing (writes header-only placeholder).
- [x] **2. package.json prebuild chain** — chained: `copy-editorial-calendar → generate-publish-queue-data → fetch-linkedin-stats`.
- [x] **3. Typed parser** — `src/lib/editorial-calendar.ts` exports `loadCalendar()`, `readyToPublish()`, `recentlyPublished()`, `syndicationGaps()`, `imageMetadataGaps()`, types `CalendarEntry`, `SyndicationGap`. Uses existing csv-parse dep with `relax_quotes` + `relax_column_count` for resilience (real-data CSV has unescaped quotes in notes field).
- [x] **4. Page** — `src/app/admin/publish-queue/page.tsx`. Server-rendered RSC. Four sections + raw-data section. Noindex+nofollow+noarchive meta. Tailwind matching site style. Status + Theme badges with project color tokens.
- [x] **5. Data-attributes + embedded JSON + STATIC ENDPOINT** — every row carries `data-title`, `data-theme`, `data-status`, `data-pub-date`, `data-work-date`, `data-blog-path`, `data-canonical-site` (+ `data-missing` on gap rows). Embedded `<script type="application/json" id="publish-queue-data">` for in-page JS. **Plus** new `scripts/generate-publish-queue-data.js` emits `public/admin/publish-queue-data.json` at build time — agent-readable static endpoint that works without JS or RSC payload parsing (required because the site's ClientLayout boundary means the rendered DOM only exists post-hydration).
- [x] **6. Robots/sitemap exclusion** — page-level `robots: { index: false, follow: false, noarchive: true, nosnippet: true }`. Sitemap is generated separately and doesn't reference /admin/*.
- [x] **7. Smoke test** — `npm run build` succeeds, prebuild generates JSON endpoint with real data: 356 total entries → 14 ready, 9 recent, 19 syndication gaps, 4 image-metadata gaps. JSON validates as parseable; structure matches the page's section logic.
- [x] **8. Commit + push** — done: website `6780c6361`.

## Open questions for PM (none blocking — surfacing for awareness)

1. **ClientLayout boundary affects admin rendering.** The site's root layout wraps everything in a `<ClientLayout>`, so /admin/publish-queue renders as a serialized React Server Components payload in the static HTML; the DOM (including data-attributes) only materializes after JS hydration. I worked around this with the static JSON endpoint at `/admin/publish-queue-data.json`. **Alternative**: add a separate `src/app/admin/layout.tsx` that doesn't wrap in ClientLayout, giving /admin routes true SSR. Defer unless PM wants pure-HTML admin surfaces.
2. **No /admin index page.** Just /admin/publish-queue for v1. If we add more admin surfaces, an /admin landing page becomes useful. Defer until there's a second admin surface.

## Out of scope (v1)

- Interactive "publish this" buttons (defer until CLI B exists)
- Edit-in-place for calendar fields (use the existing `/update-calendar` skill)
- Auth (PM said no auth for v1)
- Notification / digest emails (out of project scope)
- Slack/external integrations
- Historical analytics (publish cadence, theme distribution, etc.) — could be Dashboard B later

## Checkpoint commits

- `piper-morgan-website@6780c6361` — `feat(admin): add /admin/publish-queue dashboard (Dashboard A)`
- `piper-morgan-product@<pending>` — Dashboard A checklist closure + session log update

## Status

**Done.** Dashboard A ready and deployed. Live URL: `https://pipermorgan.ai/admin/publish-queue/` (after Pages deploy completes). Static JSON endpoint: `https://pipermorgan.ai/admin/publish-queue-data.json`.
