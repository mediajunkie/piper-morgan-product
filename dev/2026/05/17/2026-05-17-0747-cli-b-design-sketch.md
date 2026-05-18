# CLI B — design sketch (post-discussion, ready to build)

**Status**: design complete, not built. Originally drafted 2026-05-17 ~07:47 as a pre-discussion sketch; the six open questions were resolved through a conversational pass with PM on 2026-05-17 evening (~19:00–19:30). All design decisions below now reflect resolved positions.
**Spec inputs**: PM's expanded scope from 2026-05-16 (metadata UI + mark-ready + open-file link + post-publish-edit awareness, libraries not bespoke, "if WYSIWYG is too hard, this is the next step down"), [[publishing-ui-block-queued-2026-05]] memory, Docs's feedback from the 2026-05-17 publishes, the conversational discussion that produced the resolved decisions.

## Resolved design decisions (2026-05-17 ~19:30)

| # | Question | Decision |
|---|---|---|
| 1 | Does CLI B commit + push to website repo? | **Yes**, with a confirm prompt, default-`N`. Auto-generated commit message (`Add blog post: {title}` matching established convention) with `[e]` option to edit inline. |
| 2 | Does CLI B notify Docs to run `/update-calendar`? | **Yes**, auto-drop a short structured memo to `mailboxes/docs/inbox/`, CC PM. Extends the existing mailbox channel rather than introducing a new surface. |
| 3 | Mark-ready behavior — separate state, or collapsed? | **Collapsed for v1, with branching prompt.** After metadata-confirm, prompt offers `P]ublish now` (default) or `R]eady for later` (status → `ready`, no publish; PM returns later — natively supports goal-state scheduled-publish workflow without building a scheduler). |
| 4 | Edit-pass drift detection? | **No detection in v1.** Always offer edit-pass on published entries; let empty `git diff` after the conversion run be the "no changes" signal. Drift auto-discovery isn't a primary use case. Add later if manual flow proves annoying. |
| 5 | Queue picker scope? | **Narrow**: `queued` + `drafted` + `ready` entries, sorted by pubDate ascending. The wider "recently published with edit-pass affordance" variant is a future enhancement, filed not built. |
| 6 | `--non-interactive` mode on CLI B? | **Skip entirely.** Agents needing non-interactive use the engine layer directly (`publish-post.js` + engine modules). CLI B stays purely human-interactive. Reinforces the three-layer architecture: shells are thin, engine grows. |

**Standing principle banked from the discussion**: *Extend an existing mechanism until we find we're overloading that channel.* Don't introduce new coordination surfaces (a new log file, a new directory, a new channel) when an established one (inbox memos, calendar entries, git history) already does the job. Reuse-first defaults make the cohort's coordination model legible.

**Goal-state workflow nuance**: PM's stated goal is "do final edits day-before, schedule publication for next day." Today there's no scheduler — the workflow runs synchronously. The `R]eady for later` path (decision #3) is the manual version of what an eventual scheduler will automate. When the scheduler arrives, it just looks for `status: ready` + `pubDate <= today` and runs `publish-post.js` non-interactively. CLI B v1 has zero scheduler infrastructure; the calendar data shape after `R` is already correct for the future scheduler to consume.

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

**Resolved 2026-05-17 ~19:30** — see the "Resolved design decisions" section at the top of this doc for the disposition of all six questions originally listed here. Preserved below as a record of the questions that drove the conversation.

1. ~~Should CLI B do the commit + push to website repo, or just stage and let PM run the push?~~ → Resolved: auto with confirm, default-N.
2. ~~Should CLI B drop the "notify Docs to run /update-calendar" memo automatically?~~ → Resolved: auto-drop, extends existing inbox channel.
3. ~~Mark-ready behavior on the calendar~~ → Resolved: collapsed for v1 with `P]ublish now / R]eady for later` branching prompt.
4. ~~Edit-pass detection precision~~ → Resolved: no detection in v1; always offer; empty git-diff signals no changes.
5. ~~Queue-display filter~~ → Resolved: narrow (queued/drafted/ready); wider variant filed as future.
6. ~~`--non-interactive` mode shape~~ → Resolved: skip entirely; agents use engine layer directly.

## Sizing (revised post-discussion)

- Walking-skeleton CLI (queue display narrow + pick + invoke publish-post.js + show diff + commit prompt default-N + auto commit-message with edit option): **~3 hours**
- Add metadata-editing flow (gray-matter) + `P]ublish now / R]eady for later` branching prompt + open-in-`$EDITOR`: **+2 hours**
- Add edit-pass affordance on published entries (no detection, always offer): **+45 min** (down from +1hr — no drift logic)
- Add Docs-notification memo (template-driven, CC PM): **+30 min**
- Polish + error handling: **+45 min** (down from +1hr — no non-interactive mode to build)
- **Total: ~7 hours** (down from ~7-8hr estimate — three small simplifications from the discussion).
- **Split for two sessions**: walking-skeleton first (~3hr) for early validation, enrichment second (~4hr) for the full v1.

## Out of scope (v1)

- WYSIWYG markdown editing (PM's "easy peasy" joke — defer or never; Web GUI v2 territory)
- In-CLI markdown preview (open in browser via dev server if PM wants)
- Multi-post batch publishing
- Scheduler infrastructure (cron / triggers that look for `status: ready` + `pubDate <= today` and auto-publish — calendar data shape from the `R` path is already correct for the future scheduler to consume; the scheduler itself is its own piece of work)
- Direct Medium/LinkedIn API integration
- Authentication on the dashboard (PM said no auth)
- Drift auto-detection on edit-pass (defer until manual flow proves annoying)
- Recently-published variant in the queue picker (defer until first time edit-pass-by-picker is wanted)
- `--non-interactive` headless mode on CLI B (agents use engine layer directly)
