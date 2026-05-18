# Web Publishing Admin — Canonical Plan

**Owner**: Unicorn Web Designer (web)
**Stakeholders**: PM (xian) for direction + decisions; Docs as primary operator of the publish flow + the publish-to-blog skill
**Created**: 2026-05-17
**Last refresh**: 2026-05-17 18:12

## What this is

The canonical reference for the web publishing admin work — architecture, status, queued work, open decisions, and where each piece lives. This is a **map**, not a copy: links out to the underlying memory files, dev/ checklists, design sketches, code, and the publish-to-blog skill. When something changes, update the underlying artifact + this snapshot.

If you (or any future session) ever ask "what's the plan for the publishing admin?", read this file first.

## Why this exists

Today's tooling work has produced ~6 documents (memory files + dev/ checklists + design sketches + the skill) plus a memo trail across mailboxes. No single doc consolidated them, which made the question "where's the plan?" hard to answer without enumerating sources. This doc fixes that.

## Architecture

Three-layer publishing tooling — confirmed by PM 2026-05-17:

| Layer | Audience | Status | Where |
|---|---|---|---|
| **Engine** — mechanical, agent-callable, stable | Agents + both human shells | Shipped | `piper-morgan-website/scripts/publish-post.js`, `scripts/copy-editorial-calendar.js`, `scripts/generate-publish-queue-data.js`, `scripts/validate-blog-content.js`, `scripts/cleanup-blog-content-duplicates.js`, `src/lib/editorial-calendar.ts` |
| **CLI shell** ("CLI B") — terminal-first interactive surface | PM + agents wanting guided invocation | **Pending — next major build** | Design sketch: `dev/2026/05/17/2026-05-17-0747-cli-b-design-sketch.md` |
| **Web GUI** ("Dashboard B" — evolves from current Dashboard A) — browser-first writable surface | PM, eventually other humans | Read-only v1 shipped; writable v2 is deferred until CLI B proves the interaction model | Current: `src/app/admin/publish-queue/page.tsx` + `/admin/publish-queue-data.json` static endpoint. Future writable: requires local API runtime decision. |

**Principle**: keep shells thin, engine grows. Shared modules (calendar-mutations, draft-metadata, queue-shape, post-publish-edit detection) live in the engine layer; CLI B and the future Web GUI v2 both call them. Prevents Web GUI v2 from being a re-implementation.

Background memory: [`project_three_layer_publishing_architecture.md`](file:///Users/xian/.claude/projects/-Users-xian-Development-piper-morgan-piper-morgan-website/memory/project_three_layer_publishing_architecture.md).

## Status snapshot

| Item | Status | Commit / Doc |
|---|---|---|
| `publish-post.js` (Engine) | ✅ Shipped 2026-05-16 | website `0179571a0` + later `411025f7b` (backtick fix) |
| Dashboard A (Web GUI v1, read-only) | ✅ Shipped 2026-05-16 | website `6780c6361` |
| Route-group refactor — admin layout SSR | ✅ Shipped 2026-05-17 | website `b8b0892f0` |
| publish-to-blog skill aligned with script | ✅ v0.10 → v0.13 | product `9b1e668e` + later Docs updates |
| validate-blog-content invariant checker | ✅ Shipped 2026-05-16 | website `ee80de1d6` |
| blog-content.json clean slate + quarantine | ✅ Shipped 2026-05-16 | website `381ba0026` + `877c6731b` |
| Type-safety pass (60 explicit-any casts) | ✅ Shipped 2026-05-16 | website `219c4de0a` |
| **CLI B** (CLI shell — interactive picker, metadata edit, mark-ready, edit-pass) | 🟡 Sketched, awaiting build go-ahead | sketch: `dev/2026/05/17/2026-05-17-0747-cli-b-design-sketch.md` |
| **Web GUI v2** (writable dashboard with WYSIWYG affordance) | 🔵 Deferred — depends on CLI B proving interaction model | — |
| Numbered-list `<ol>/<li>` conversion gap in publish-post.js | 🟠 Queued (surfaced 2026-05-17 from Protocol publish) | tracked here |
| Blog-index syndication-duplicate filter (RSS slug mismatch — separate from yesterday's content-store dedupe) | 🟠 Queued (surfaced 2026-05-17 during admin refactor smoke test) | tracked here; details in [Open issues](#open-issues) |
| 8/6 standalone fat-entry repatriation review | 🟣 PM-driven, not web | — |
| `react/no-unescaped-entities` lint policy (74 remaining) | 🟡 Awaiting PM decision (disable rule vs mechanically escape) | tracked here |

## CLI B (next major build) — design at a glance

Full sketch: [`dev/2026/05/17/2026-05-17-0747-cli-b-design-sketch.md`](../2026/05/17/2026-05-17-0747-cli-b-design-sketch.md).

**What it adds on top of the engine**: queue browsing → metadata inspect/edit → mark-ready → open-in-`$EDITOR` handoff → dry-run preview → real publish via `publish-post.js` → diff → commit/push prompt → edit-pass mode for post-publish-edit awareness.

**Libraries**: `@inquirer/prompts` (prompts), `gray-matter` (frontmatter parse/write), `csv-parse` + `csv-stringify` (already in deps), no new heavy deps.

**Engine modules CLI B will introduce** (these are the "shared shell substrate" for Web GUI v2):
- `scripts/lib/calendar-mutations.js` — `markReady(slug)`, `updateStatus(slug, status)`, `backfillSyndicationUrls(slug, urls)`
- `scripts/lib/draft-metadata.js` — frontmatter read/write via gray-matter
- `scripts/lib/queue.js` — `getQueue()`, `getRecentlyPublished()`, `findBySlug(slug)`
- `scripts/lib/post-publish-detect.js` — `hasDraftDriftedFromPublished(slug)`

**Sizing**: ~7-8 hours total. Split: walking-skeleton (queue display + pick + invoke publish-post.js + show diff + commit prompt) ~3hr, then enrichment (metadata edit + mark-ready + open-in-editor + edit-pass + Docs-notification) ~4-5hr.

**Open questions for PM** (from the sketch — flagged so the build doesn't sit waiting for permission later):
1. Should CLI B do the commit + push to website repo automatically, or stage and let PM run the push?
2. Should CLI B drop the "notify Docs to run /update-calendar" memo automatically, or is that overstepping?
3. Mark-ready behavior on the calendar — just status flip, or also stamp pubDate/anything else?
4. Edit-pass detection precision — diff HTML rough, or track a content-hash field for precision?
5. Queue-display filter — queued/drafted only, or include recent-published with edit-pass affordance?
6. `--non-interactive` mode shape — separate CLI or a flag?

## Open issues

### Numbered-list conversion gap in `publish-post.js`
Surfaced 2026-05-17 during the *From Protocol to Infrastructure* publish (referenced in skill v0.13). Markdown numbered lists (`1.` `2.` etc.) get rendered as `<p>` with `<br />` line joins instead of `<ol>/<li>`. Same class of issue as the inline-backtick gap fixed at `411025f7b`. ~30 min fix in `renderInline`-adjacent logic; should land before CLI B if there are more publishes in between.

### Blog-index syndication-duplicate filter
Surfaced 2026-05-17 in the admin refactor smoke check: `medium-posts.json` contains both the canonical blog-first entry AND the RSS-syndicated duplicate as separate cards on `/blog/`. Root cause: `fetch-blog-posts.js`'s slug-skip logic does exact slug-match, but blog-first uses short hand-chosen slugs while Medium auto-derives long title-slugs. Proper fix: tie syndication detection to `editorial-calendar.csv`'s `mediumURL` field (the calendar already records the correspondence after Docs's `/update-calendar` runs); the calendar is already copied to the website at prebuild. Sizing: ~1 hour for the fix + audit-before-delete + quarantine one-shot cleanup of existing duplicates. Different class than the 2026-05-16 `blog-content.json` cleanup at `381ba0026` (which fixed a different storage layer).

### Lint policy: `react/no-unescaped-entities`
74 remaining lint warnings, almost entirely stylistic apostrophe/quote escapes in marketing copy. Two options: disable rule project-wide (1-line eslint config change) or mechanically escape (touches every marketing page). PM call.

### Repatriation review (PM-led, not web)
6 standalone fat entries in `blog-content.json` may be unrepatriated content (5K–12K char articles each). PM has the list; not web's project to triage.

## Cross-cutting principles

These shape every decision and should be honored by future work:

- [`feedback_human_first_agent_aware_interfaces.md`](file:///Users/xian/.claude/projects/-Users-xian-Development-piper-morgan-piper-morgan-website/memory/feedback_human_first_agent_aware_interfaces.md) — PM is the primary user; architect for agents too.
- [`feedback_conservative_deletion_agent_ready_unique_info.md`](file:///Users/xian/.claude/projects/-Users-xian-Development-piper-morgan-piper-morgan-website/memory/feedback_conservative_deletion_agent_ready_unique_info.md) — quarantine > rm, audit before delete, build agent-ready from start.
- [`feedback_unblocked_work_batched_questions.md`](file:///Users/xian/.claude/projects/-Users-xian-Development-piper-morgan-piper-morgan-website/memory/feedback_unblocked_work_batched_questions.md) — do unblocked work; batch questions; surface critical/unclear.
- [`feedback_bias_to_immediate_action.md`](file:///Users/xian/.claude/projects/-Users-xian-Development-piper-morgan-piper-morgan-website/memory/feedback_bias_to_immediate_action.md) — schedules are theoretical; act on next ready thing.
- [`feedback_deferral_requires_pm_approval.md`](file:///Users/xian/.claude/projects/-Users-xian-Development-piper-morgan-piper-morgan-website/memory/feedback_deferral_requires_pm_approval.md) — never unilaterally defer; surface with reason + recommended trigger.

## Where things live (quick-reference map)

| Artifact | Path |
|---|---|
| **This plan** | `dev/active/web-publishing-admin-plan.md` |
| Architecture memory | `~/.claude/projects/-Users-xian-Development-piper-morgan-piper-morgan-website/memory/project_three_layer_publishing_architecture.md` |
| UI block memory | `~/.claude/projects/.../memory/project_2026_05_publishing_ui_block_queued.md` |
| CLI B design sketch | `dev/2026/05/17/2026-05-17-0747-cli-b-design-sketch.md` |
| publish-post.js checklist | `dev/2026/05/16/2026-05-16-1058-publish-post-checklist.md` (closed) |
| Dashboard A checklist | `dev/2026/05/16/2026-05-16-1158-dashboard-a-checklist.md` (closed) |
| publish-to-blog skill | `.claude/skills/publish-to-blog/SKILL.md` (v0.13, Docs's operational ref) |
| Engine code | `piper-morgan-website/scripts/publish-post.js`, `scripts/copy-editorial-calendar.js`, `scripts/generate-publish-queue-data.js`, `scripts/validate-blog-content.js`, `scripts/cleanup-blog-content-duplicates.js` |
| Web GUI v1 (Dashboard A) | `piper-morgan-website/src/app/admin/publish-queue/page.tsx` + `src/lib/editorial-calendar.ts` |
| Memo trail | `piper-morgan-product/mailboxes/web/inbox/`, `mailboxes/docs/inbox/` |
| Session logs | `piper-morgan-product/dev/2026/05/16/2026-05-16-0719-web-code-opus-log.md`, `dev/2026/05/17/2026-05-17-0739-web-code-opus-log.md` |

## Decisions log

Reverse-chronological. Captures PM signals that govern the work.

- **2026-05-17 18:08** — PM: merge the route-group refactor; ship as foundation. Done at website `b8b0892f0`.
- **2026-05-17 ~09:32** — PM: confirmed CLI proves the concept, Web GUI extends successful methods later. Engine stays constant across both shells.
- **2026-05-17 ~07:47** — PM: pick up where we left off — designs CLI B with Docs's publish-feedback in hand; admin refactor still pending (later merged).
- **2026-05-16 ~22:04** — End-of-day session close; pickup state banked as memory for next-session re-orientation.
- **2026-05-16 ~17:47** — PM: greenlit cluster=empty for insight posts, prompts policy (CLI B not script), confirmed bias-to-action principle.
- **2026-05-16 ~10:58** — PM: start `publish-post.js` immediately; bias to act on next ready thing; batch questions.
- **2026-05-16 ~10:43** — Docs's consolidated feedback memo: script + dashboard + CLI sequence approved; queued (originally) for week of 2026-05-17 — actual delivery accelerated to that-same-day-and-next.
- **2026-05-16 ~08:50** — PM standing instruction: do unblocked work, batch questions, don't meter on availability.
- **2026-05-16 ~07:35** — Mar 29 alt-text fix triage; sync-csv destructure surprise; cleanup queue scoped.

## Maintenance

When something material changes — a piece ships, a decision lands, a new issue surfaces — update this file in the same commit (or the immediately-following commit). The point is to keep this doc current so a fresh session reading it gets accurate state. The underlying artifacts (memory, sketches, checklists) remain the source of truth for their respective scopes; this doc is the map.
