# CLI B — design sketch (pre-discussion)

**Status**: draft, not built. Written 2026-05-17 ~07:47 to give the PM discussion concrete options to react to rather than a blank-page conversation.
**Spec inputs**: PM's expanded scope from 2026-05-16 (metadata UI + mark-ready + open-file link + post-publish-edit awareness, libraries not bespoke, "if WYSIWYG is too hard, this is the next step down"), [[publishing-ui-block-queued-2026-05]] memory, Docs's feedback-pending from today's publish.

## Architectural premise (PM-confirmed 2026-05-17)

Three-layer architecture: **Engine** (mechanical, agent-callable, stable) → **CLI shell** (terminal-first, ships first, proves the interaction model) → **Web GUI** (browser-first, extends CLI's proven methods, gets WYSIWYG affordances). CLI B is the second layer. Web GUI is the eventual third.

**Implementation principle**: keep shells thin, engine grows. Anything more than presentation belongs in the engine layer. CLI B's interaction handlers should call engine functions, not inline-mutate state.

Specifically for CLI B: the **calendar-mutation logic** (mark-ready, status flips, syndication URL backfill stubs), **queue-shape computation**, **draft-metadata read/write**, and **post-publish-edit detection** should each be a module in `piper-morgan-website/src/lib/` (or `scripts/lib/`) that CLI B calls AND that the future Web GUI v2 can call. CLI B becomes a relatively thin presenter layer. This prevents the Web GUI v2 from being a re-implementation.

Suggested module shape:
- `scripts/lib/calendar-mutations.js` — `markReady(slug)`, `updateStatus(slug, status)`, `backfillSyndicationUrls(slug, urls)`
- `scripts/lib/draft-metadata.js` — `readFrontmatter(path)`, `writeFrontmatter(path, fm)` (gray-matter wrapped)
- `scripts/lib/queue.js` — `getQueue()`, `getRecentlyPublished()`, `findBySlug(slug)`
- `scripts/lib/post-publish-detect.js` — `hasDraftDriftedFromPublished(slug)` → boolean

CLI B is then ~150 lines of inquirer prompts that wire these together. Web GUI v2 is ~similar lines of React forms that wire the same modules.

## Premise

CLI B is the **human-interactive layer** that sits on top of `scripts/publish-post.js` (the mechanical engine). The script stays non-interactive, agent-callable, JSON-reportable. CLI B adds:
- Queue browsing (which drafts are ready?)
- Metadata editing (frontmatter inspect + tweak)
- "Mark ready" — flip status in editorial-calendar.csv
- Open-in-editor handoff (spawn `$EDITOR draft.md`, return when saved)
- Invoke publish-post.js with the right flags
- Post-publish: show diff, confirm commit, run commit + push
- Post-publish-edit awareness (if draft has changed since publish, offer edit-pass)

CLI B does **not** add WYSIWYG markdown editing. PM's stated preference: "open in my own markdown editor."

## Library decisions (all open-source, no bespoke)

- **`@inquirer/prompts`** (modern Inquirer) — interactive prompts. Industry-standard, agent-friendly because it has non-interactive equivalents.
- **`gray-matter`** — YAML frontmatter parse + write. Already implicit in publish-post.js's parser; using the lib in CLI B avoids re-implementing and handles edge cases (escaped quotes, multi-line strings) more robustly than my hand-rolled parser.
- **`csv-parse` + `csv-stringify`** — already in package.json deps. Editorial-calendar mutations need round-trip-safe CSV handling.
- **`chalk`** or just ANSI escapes — minimal styling for queue/status display.
- **`diff`** or shell out to `git diff --stat` — diff display before commit.

No new heavy deps. The footprint stays modest.

## CLI shape (one entry point per PM's #5 lean: avoid optional complexity)

```bash
npm run publish
# Or: node scripts/publish-cli.js
```

Walks through:

```
$ npm run publish
📋 Editorial Queue:
  > [1] The Voice of a Denial (queued, pubDate 2026-05-21, building)
    [2] The Omnibus That Found Its Own Drift (queued, pubDate 2026-05-19, building)
    [3] [open draft path manually]
    [q] Quit

? Pick a draft to publish: 1

📄 Loaded: docs/public/comms/drafts/the-voice-of-a-denial.md
   title: "The Voice of a Denial"
   theme: building
   workDate: 2026-04-26
   pubDate: 2026-05-21

📷 Image metadata:
   image:   voice-of-a-denial.png
   alt:     [empty]
   caption: [empty]

? Image metadata is incomplete. Open draft in $EDITOR to fix? (Y/n)
   → spawns $EDITOR, waits for save

[after save, re-reads metadata]
   image:   voice-of-a-denial.png
   alt:     "An AI being firmly declining a request..."
   caption: "No."

? Cluster is empty. Set explicitly? (Y/n/skip)  [skip]
? Mark draft as 'ready' in editorial-calendar.csv? (Y/n) [Y]
   ✅ Calendar updated

? Run publish-post.js dry-run first? (Y/n) [Y]
   [runs --dry-run, shows HTML preview]
   ✅ Dry-run clean

? Proceed with real publish? (Y/n) [Y]
   [calls: node scripts/publish-post.js --draft ... --image ... --slug ... --category ... --report=json]
   ✅ 5 files mutated; hashId f740e2165b6d
   → /blog/the-voice-of-a-denial

📋 git diff --stat on website repo:
   data/blog-metadata.csv                |   1 +
   src/data/blog-content.json            |   4 +
   src/data/medium-posts.json            |  22 ++
   public/assets/blog-images/the-voice-of-a-denial.webp  | bin

? Commit + push? (y/N) [Y]
   Commit message: "Add blog post: The Voice of a Denial" [edit/accept]
   ✅ Committed (a7c34d1) and pushed

✨ Live at https://pipermorgan.ai/blog/the-voice-of-a-denial/ after deploy.

? Next: notify Docs to run /update-calendar for syndication URLs? (Y/n) [Y]
   → drops a memo in mailboxes/docs/inbox/
```

Every prompt has a non-interactive flag equivalent. The same script can run with `--non-interactive --slug ... --category ... --commit --push` for automation.

## Edit-pass mode (post-publish-edit awareness)

If PM picks a slug that's already published (status=published in calendar):

```
? "The Family Resemblance" is already published.
  - View live post
  - Apply post-publish edits (calls publish-post.js --mode=edit-pass)
  - Cancel
```

The "Apply post-publish edits" path:
- Re-reads the draft
- Diffs current HTML conversion against current blog-content.json[hashId].content
- If differs: calls publish-post.js --mode=edit-pass, shows the diff, prompts commit
- If identical: "No changes to apply"

This is the "if it gets edited again after publication" PM mentioned.

## Architecture notes

- **Lives in**: `piper-morgan-website/scripts/publish-cli.js`. Same dir as publish-post.js. Matches conventions.
- **Invoked from**: either repo CWD; resolves cross-repo paths the same way publish-post.js does.
- **Reads from**: 
  - `data/editorial-calendar.csv` (queue + status — note: this is copied from product repo at prebuild, so for CLI B's purposes we read directly from `../piper-morgan-product/docs/internal/planning/comms/editorial-calendar.csv` to get live state, not the build-time snapshot)
  - draft files in `../piper-morgan-product/docs/public/comms/drafts/`
- **Writes to**:
  - `../piper-morgan-product/docs/internal/planning/comms/editorial-calendar.csv` (mark-ready + status flip)
  - Draft files in `../piper-morgan-product/docs/public/comms/drafts/` (frontmatter edits via `gray-matter`)
  - Shells out to `node scripts/publish-post.js` for the mechanical pipeline
  - Shells out to `git add/commit/push` for the website repo
- **Does NOT do**:
  - Voice-pass / quality scrub (skill, PM)
  - Medium / LinkedIn syndication (skill, PM)
  - Drafts folder archival (skill, manual or future automation)
  - Editorial-calendar URL backfill after syndication (Docs's `/update-calendar` skill)

## Open questions for PM discussion

1. **Should CLI B do the commit + push to website repo, or just stage and let PM run the push?** Yesterday I asked something similar; PM said "probably yes, but trial-and-error fine." Confirming with a real flow in hand.
2. **Should CLI B drop the "notify Docs to run /update-calendar" memo automatically, or is that overstepping into Docs's territory?** The Family Resemblance flow yesterday was: I committed + pushed; PM took it to Docs verbally; Docs handled steps 6-9. If CLI B drops a memo automatically, it's the right shape but it may collide with how Docs prefers to be cued.
3. **Mark-ready behavior on the calendar**: should it bump only `status: queued → ready`, or also stamp something else (pubDate to today, etc.)? Need to align with Docs's `/update-calendar` skill conventions.
4. **Edit-pass detection precision**: my proposed "diff current HTML against stored HTML" is rough. Better signal: track a draft-mtime or content-hash field in blog-content.json. Defer until needed.
5. **Queue-display filter**: show only queued/drafted, or also recent published with edit-pass affordance? My lean: queued/drafted by default, with a flag to include published-with-changes.
6. **`--non-interactive` mode shape**: should the non-interactive equivalent be a separate CLI (`publish-noninteractive.js`) or a flag on `publish-cli.js`? Flag is simpler but introduces a "headless mode" code path that's secondary. Defer; agents will mostly call `publish-post.js` directly anyway.

## Sizing

- Walking-skeleton CLI (queue display + pick + invoke publish-post.js + show diff + commit prompt): **~3 hours**
- Add metadata-editing flow + mark-ready + open-in-editor: **+2 hours**
- Add edit-pass mode: **+1 hour**
- Add Docs-notification memo: **+30 min**
- Polish + error handling + non-interactive flags: **+1 hour**
- **Total: ~7-8 hours** — bigger than my earlier "~1 day" estimate because of the metadata-editing scope expansion. Could be split across two sessions: walking skeleton first, then enrichment.

## Out of scope (v1)

- WYSIWYG markdown editing (PM's "easy peasy" joke — defer or never)
- In-CLI markdown preview (open in browser via dev server if PM wants)
- Multi-post batch publishing
- Schedule-publish (cron triggers etc.)
- Direct Medium/LinkedIn API integration
- Authentication on the dashboard (PM said no auth)
