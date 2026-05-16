# Web session — 2026-05-16 07:19

**Role**: Unicorn Web Designer (piper-morgan-website)
**Trigger**: Re-orient after ~6.5 week dormancy; PM asked for triage on the Mar 29 docs memo + scoping on a Publishing UI ask.

## Read

- `mailboxes/web/inbox/memo-docs-to-web-blog-first-fixes-2026-03-29.md` (Mar 29 docs memo, in full)
- `.claude/skills/publish-to-blog/SKILL.md` (v0.9, updated 5/15)
- Website: `scripts/fetch-blog-posts.js` (focus: 300-470, the merge/blog-first block)
- Website: `scripts/sync-csv-to-json.js` (focus: 19-80, the CSV destructure)
- Website: `scripts/csv-parser.js` (focus: field count + imageAlt/imageCaption handling)
- Website: `src/components/organisms/BlogPostContent.tsx` (full)
- Website: `src/components/molecules/BlogPostCard.tsx` (full)
- Website: `src/app/blog/page.tsx`, `src/app/blog/BlogContent.tsx` (1-100)
- Sampled: `src/data/medium-posts.json` — 33 blog-first entries present, all with `/blog/{slug}` URLs

## Verified (Mar 29 triage)

| Item | Status | Evidence |
|------|--------|----------|
| Critical: blog-first URL preservation | ✅ shipped | `fetch-blog-posts.js:313-470` builds blog-first posts fresh from CSV (line 442-459); syndicated RSS hits matched by slug are skipped (line 341-347). All 33 blog-first entries in current `medium-posts.json` carry `/blog/{slug}`. |
| "Published:" date display | ✅ working | BlogPostCard renders `publishedAt` ("May 14, 2026" format); blog-first dates flow from CSV `pubDate` via `formatDate()` in fetch-blog-posts.js:447. |
| Category filter counts | ✅ working | `BlogContent.tsx:83-84` computes building/insight counts from `allSortedPosts`. Category data flows through (sampled posts have `category: "building"` / `"insight"`). |
| Alt text rendering | ❌ not shipped | `BlogPostCard.tsx:77` and `BlogPostContent.tsx:161` both hardcode `alt={title}` / `alt={post.title}`. CSV has the column, csv-parser.js reads it, but `fetch-blog-posts.js:442-459` does not include `imageAlt` in the constructed post object; `BlogPost` interface doesn't declare it either. |
| Figcaption rendering | ⚠️ partial | `BlogPostContent.tsx:45-57` extracts caption from a `<figure>` in content HTML — works for Medium RSS posts that have figure markup, fails silently for blog-first posts (their content has no figure). CSV `imageCaption` is unused. |

## Latent bug noted (not in Mar 29 scope)

`scripts/sync-csv-to-json.js:62-73` destructures the CSV row into 11 fields, omitting `imageAlt`/`imageCaption`. The script currently only writes `cluster/category/featured/notes` back to JSON, so it functions — but the layout is stale relative to the canonical 13-column schema and will desync if anyone ever extends the script. Worth one-line fix when convenient; not urgent.

## Plan (this session)

1. Write triage memo to docs (this file, then memo).
2. No code changes this session — the ask is forward-looking triage + scoping.
3. Defer Publishing UI build until shape decision is in.

## Cross-repo automation — my read

Three options were named in the Mar 29 addendum: GH Action trigger, shared dir (submodule/subtree), API-based publish. My recommendation in the memo: **none of those three first**. The actual friction isn't the cross-repo hop — it's that the publish pipeline is encoded only in a skill (prose + Python snippets) rather than a single script. Codifying it as `scripts/publish-post.js` in piper-morgan-website (input: draft path + image path) gives ~80% of the relief at near-zero cost. Cross-repo automation becomes a thin wrapper later.

## Publishing UI — initial shape

Open shape question; my lean is to **start with a build-time admin dashboard** (e.g. `/admin/publish-queue`) generated from `editorial-calendar.csv`, gated noindex. Surface: drafts ready, recently published, syndication gaps, cross-post URLs. Zero new infra (static export friendly). Layer interactivity later via CLI wrapper around `scripts/publish-post.js`. Full reasoning in the memo.

## Next

- Send memo to docs (CC PM via mailbox routing).
- Wait for shape decision before committing to UI build.

---

## Work shipped (continued after PM standing instruction)

PM gave standing instruction at ~07:24: do unblocked work, batch questions, don't meter on availability for routine forward motion. Banked as feedback memory `feedback_unblocked_work_batched_questions.md`.

### Commit 1 — be0fd1329 `fix(blog): render imageAlt + imageCaption from CSV for blog-first posts`

Closes the Mar 29 outstanding ask. Threaded `imageAlt` and `imageCaption` from CSV → `medium-posts.json` → React props → `<img alt>` + `<figcaption>` (CSV-sourced caption preferred over HTML-extracted; falls back for Medium RSS posts).

Files: `scripts/fetch-blog-posts.js`, `src/app/blog/BlogContent.tsx`, `src/app/blog/[slug]/page.tsx` (subtitle TS cast), `src/components/molecules/BlogPostCard.tsx`, `src/components/organisms/BlogPostContent.tsx`, regenerated `medium-posts.json` + `blog-content.json` (RSS picked up 1 new syndicated post).

Verified: 32 blog-first posts now carry imageAlt and 41 carry imageCaption in the regenerated JSON. Type-check passes; build passes. Static-HTML verification limited because BlogPostContent is a client component (DOM creation happens at hydration), but serialized React payload contains both fields — strong indicator.

### Commit 2 — f320c6192 `fix(sync): correct sync-csv-to-json field destructure (11 → 13 cols)`

Adjacent latent-bug fix flagged in the triage memo. The destructure was off by 2 columns since the CSV grew from 11 → 13 fields (imageAlt/imageCaption added). Symptoms exposed when I re-ran the script:

- 307 posts had `cluster` set to a date string (actually pubDate from CSV col 8) instead of an era slug — silently breaking era filtering for non-blog-first posts
- 3 posts had `category` set to a date string (actually workDate from CSV col 7) instead of `building`/`insight`/`ship`

`fetch-blog-posts.js` was unaffected because it goes through `csv-parser.js` (which already had the right 13-field shape). Only this script's local destructure was stale.

Regenerated `medium-posts.json` + `backup-sync` reflect the corrections.

### Surprise finding (not yet fixed): blog-content.json syndication duplicates

Discovered during the alt-text fix verification. `fetch-blog-posts.js:updateBlogContent()` adds RSS posts to `blog-content.json` keyed by their Medium hashId, without checking whether they're syndication duplicates of an existing blog-first post (which lives under a different hashId). Result: 31 "fat" RSS-style entries in `blog-content.json`, 23 of which have titles matching existing blog-first entries.

Functionally harmless — `medium-posts.json` correctly points to the blog-first hashId, so the duplicate fat entries are never looked up. But the file is bloated and confusing during debug.

Not fixing this round — it's bigger than a one-liner and the right scope (fix root cause vs clean up existing vs both vs leave alone) is a PM call. Flagged in the follow-up memo.

## Outbox

- `mailboxes/docs/inbox/memo-web-to-docs-mar29-fix-shipped-and-new-findings-2026-05-16.md` — follow-up to morning's triage memo

## Stop point (intermediate)

Halting after two shipped fixes. Open items now batched for PM:
1. blog-content.json duplicate handling (fix root cause / clean up existing / both / leave)
2. Four questions from the morning's triage memo (publish-script direction, dashboard auth shape, CLI CWD, who the UI is for)

### PM responded (~07:50): both — "chance for a clean slate"

### Commit 3 — 381ba0026 `fix(blog): stop writing syndication duplicates to blog-content.json + clean up 25 existing`

Root-cause fix + one-shot cleanup, per PM's both-please call.

**Root cause** in `fetch-blog-posts.js:updateBlogContent()`: iterated `rssPosts` and wrote each to `blog-content.json` keyed by Medium hashId without checking against blog-first canonical slugs. `mergeArchive`'s slug-skip logic kept syndications out of `medium-posts.json` but never reached `updateBlogContent`. Fix: pass `mergedPosts` to `updateBlogContent`, build a blog-first slug set, skip RSS posts whose slug matches. Idempotent — safe on every fetch.

**One-shot cleanup**: new `scripts/cleanup-blog-content-duplicates.js`. Distinguishes fat syndication duplicates (canonicalLink slug matches a blog-first slug → remove) from fat standalone entries (RSS-only posts with no blog-first counterpart → keep, they're the canonical content). Idempotent.

**Result**: `blog-content.json` went 333 → 308 entries. 25 syndication duplicates removed. 6 fat entries remain (legitimate standalone RSS-only). 0 duplicate-title pairs.

Verified: re-running fetch after cleanup correctly reports "Skipped 10 syndication duplicate(s) of blog-first posts" without re-adding any. Cleanup script is idempotent (second run finds nothing to remove). Type-check + build pass.

## Stop point (intermediate, again)

Three shipped fixes today. All open Mar 29 items closed. blog-content.json clean slate achieved.

Still awaiting PM on the four publishing-UI questions. Will keep finding adjacent unblocked work when next active.

---

## 10:43 — Docs memo landed: `memo-docs-to-web-cc-pm-consolidated-feedback-on-triage-and-findings-memos-2026-05-16.md`

Docs's consolidated decisions with PM. Net: the publish-post.js + dashboard + CLI sequence is approved and queued as a ~2.5-day cohesive block for next week (not this week — publish cadence + voice-pass work crowds the calendar). CWD decision aligns with my recommendation: invoke from website repo, resolve cross-repo input paths. Agent-readiness specifics surfaced: structured stdout (JSON exit reports), semantic HTML + data-attributes, predictable prompts + non-interactive flags everywhere.

### Timing-gap finding (self-flagged)

Docs's memo carried **three caveats** on the (c) blog-content.json cleanup that I'd already shipped (commit `381ba0026` ~08:15, two hours before the memo landed):

- ❌ Caveat 1 (audit-before-delete): not honored. My script printed + removed in one run.
- ❌ Caveat 2 (recoverable quarantine): not honored. The 25 removed entries are recoverable from `git show 381ba0026^:src/data/blog-content.json` but not in a named quarantine surface.
- ✅ Caveat 3 (don't touch standalones): incidentally honored. The 6 standalone fat entries were preserved (note: Docs's memo says "8 standalones"; count drifted to 6 by the time I ran the cleanup because the RSS slug-set was slightly different).

Root cause of the gap: I treated PM's early "both — chance for a clean slate" reply as full approval and shipped, instead of waiting for the cohort discussion that PM had flagged would happen with Docs.

Lessons banked as memory `feedback_conservative_deletion_agent_ready_unique_info.md`:
- "Do unblocked work" doesn't override "be conservative about deletion"
- When in doubt on destructive ops, wait — cost of waiting is small, cost of mis-deletion is high
- Default to two-phase for any bulk-mutation script: print first, mutate only with explicit flag

### Surfaced to PM (Caveat 3 follow-through): the 6 standalones

Listed in chat with hashId, title, content length (5K–12K chars each), Medium URL. PM will pick these up as a separate repatriation-review project; explicitly NOT part of the cleanup.

### Offer pending: retroactive quarantine

Offered to extract the 25 removed entries from `381ba0026^` and write them to `src/data/blog-content-quarantine.json`. Git history *is* recoverable, but a named quarantine matches the principle better. Awaiting PM yes/no.

### PM responded: yes; plus de-duping concern + bias-to-immediate-action principle

PM greenlit the quarantine, flagged that the titles "match recent publications" (concern: some removed entries might carry edit-pass mirror divergences the blog-first canonicals didn't get), and added a standing principle: **schedules are theoretical; bias to act immediately on next ready thing**. Banked as `feedback_bias_to_immediate_action.md`.

### Commit 4 — 877c6731b `chore(blog): add blog-content-quarantine.json for 25 entries removed in 381ba0026`

Extracted the 25 removed entries from `381ba0026^` via `git show`, added a `_quarantine_reason` field to each, sorted by hashId for stable diff, wrote to `src/data/blog-content-quarantine.json`. Committed + pushed.

**Content-safety check** (per PM's de-duping concern): diffed all 25 quarantined entries against their blog-first canonical counterparts. Text diffs (HTML stripped, whitespace normalized, Medium tracking + footer removed):

- 22 of 25: diff -14 to -47 chars — pure normalization noise (smart quotes ↔ straight quotes, leading whitespace)
- 3 of 25 with diff > 50 chars: all attributable to (a) Medium auto-prepending date prefix that blog-first doesn't have, and (b) accumulated whitespace differences from char-11 onward

**Conclusion**: no edit-pass divergences. Blog-first canonicals have all substantive content. Quarantine is preservation-of-record, not material recovery. PM's instinct was right to check; the check came back clean.

### Memory updates

Three new memories saved:
- `feedback_conservative_deletion_agent_ready_unique_info.md` — three standing principles
- `project_2026_05_publishing_ui_block_queued.md` — next-week work item with agent-ready requirements per part
- `feedback_human_first_agent_aware_interfaces.md` (saved earlier at ~08:50) — PM's stance on Publishing UI scoping

## Final stop point (for now)

All shipped: alt-text + figcaption fix (`be0fd1329`), sync-csv destructure + data corrections (`f320c6192`), blog-content cleanup (`381ba0026`).

Awaiting PM on:
- Retroactive quarantine yes/no (small, immediate)
- Final go on next-week's UI block (already approved in principle, sequencing confirmed for week of 2026-05-17)

Will keep finding adjacent unblocked work when next active.



