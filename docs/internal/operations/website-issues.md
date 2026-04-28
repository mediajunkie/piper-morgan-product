# pipermorgan.ai Website Issues

**Owner**: Documentation Management (Docs) orchestrates; deploys Coding Agent subagents for technical fixes; CXO consulted for UX/quality concerns.
**Created**: 2026-04-28 per PM directive ("Let's start a new document for tracking issues related to the pipermorgan.ai website")
**Cadence**: triage during Docs sessions; route fixes by level of effort and relative priority vs. other Docs work.

---

## Operating pattern

The website (`piper-morgan-website` repo) was originally built without a standing dedicated agent. The "web" role exists in the mailbox structure and was used to draft fix memos, but no agent has been formally onboarded to the role and the mailbox has accumulated unaddressed asks.

**Adopted approach (per PM 2026-04-28)**: rather than stand up a full web agent (one more role, one more briefing, one more onboarding overhead), **Docs orchestrates website issues with on-demand Coding Agent subagents**. CXO is the natural reviewer when issues touch UX or voice quality. Lead Dev or Architect can be consulted when issues touch infrastructure or build-system architecture.

Three current subtopics:

1. **Backlog fixes in `mailboxes/web/inbox/`** — pre-existing memos that need attention
2. **Duplicate article issue** — known content-pipeline bug; PM will surface details
3. **Further improving the publishing flow** — reducing manual handoff between piper-morgan-product and piper-morgan-website

---

## Subtopic 1 — Backlog: web mailbox memos needing attention

### Item 1.1 — Blog index links point to Medium for blog-first posts (CRITICAL, open)

**Source**: `mailboxes/web/inbox/memo-docs-to-web-blog-first-fixes-2026-03-29.md`
**Filed**: 2026-03-29
**Status**: open; bug observed since Mar 29; partial local-agent fixes shipped, systemic fix pending

**Problem**: After running `node scripts/fetch-blog-posts.js`, blog-first posts in the index link to their Medium URLs instead of local `/blog/{slug}` paths. The fetch script pulls from Medium RSS and overwrites the corrected local URLs.

**Root cause**: `fetch-blog-posts.js` doesn't preserve `source: "blog-first"` entries when merging RSS data. Medium RSS entries for syndicated posts have the Medium URL, which overwrites the local URL.

**Fix needed**: When merging RSS data in `fetch-blog-posts.js`, if an existing entry has `source: "blog-first"`, do NOT overwrite its `url` field with the Medium URL. The local `/blog/{slug}` URL must win.

**Acceptance criteria**: After running `node scripts/fetch-blog-posts.js`, entries with `source: "blog-first"` in `medium-posts.json` retain `url: /blog/{slug}` (not `medium.com/...`).

**Effort estimate**: ~1 hour subagent work (locate merge logic, add guard, test against current data, commit + push).

### Item 1.2 — Alt text + caption rendering (improvement, open)

**Source**: same memo, "Future Improvements" section
**Status**: deferred but acquiring relevance — every recent post has alt text + caption in CSV; not displayed.

**Problem**: `imageAlt` and `imageCaption` columns exist in `blog-metadata.csv` but aren't rendered in blog post templates. The `<img>` tags need `alt` attribute from `imageAlt` and a `<figcaption>` from `imageCaption`.

**Effort estimate**: ~1 hour. Touches blog post template (likely `BlogPostContent.tsx` or similar). Subagent scope.

**Accessibility note**: this also addresses the alt-text accessibility regression flagged in `mediajunkie/piper-morgan-website#18`.

### Item 1.3 — Published date display on blog-first index cards (improvement, open)

**Source**: same memo
**Problem**: Blog-first posts show "Published:" with no date on index cards when pubDate parsing fails. Ensure the date parser handles `YYYY-MM-DD` format from CSV.

**Effort estimate**: ~30 min. Date parser likely needs format-tolerance.

### Item 1.4 — Category filter counts on index nav (improvement, open)

**Source**: same memo
**Problem**: "Building (0)" and "Insights (1)" in the index nav — verify category assignment flows through from CSV to the filter UI for blog-first posts.

**Effort estimate**: ~30 min investigation, potentially trivial fix.

### Item 1.5 — Cross-repository access mechanism (discussion → may become 1.5+)

**Source**: same memo, addendum
**Status**: discussion topic, not bug — overlaps with Subtopic 3 (publishing flow improvement).

Discussed there.

---

## Subtopic 2 — Duplicate article issue

**Status**: known issue; PM has flagged for fixing; awaiting PM details on which article is duplicated and the right resolution.

**What we know**:
- Some article appears twice on the site
- PM has been aware for a while; it's been on the queue but kept getting deferred
- PM will remind / surface when ready to address

**Hypothesis on shape** (from Docs side, to be confirmed):
- Most likely cause: a Medium-syndicated post and a blog-first version of the same content both exist in `medium-posts.json` or `blog-metadata.csv`, producing two distinct entries.
- Could also be: an old draft slug + a renamed slug both rendered, with one as the canonical.

**Fix path** (when PM surfaces specifics):
1. Identify the duplicate (which article, which two surfaces)
2. Decide canonical (typically the blog-first canonical wins; Medium becomes pure syndication)
3. Edit the data sources to remove the duplicate entry
4. Verify in build + deploy

**Effort estimate**: ~30 min once specifics in hand. Subagent + Docs review.

---

## Subtopic 3 — Improving the publishing flow

### Issue 3.1 — Manual cross-repo handoff overhead (improvement, ongoing)

**Source**: 1.5 above + accumulated friction over multi-week publishing cadence

**Problem**: The current publish workflow requires Docs (or PM) to manually carry files and run scripts between `piper-morgan-product` and `piper-morgan-website`. Each publish is roughly:
1. Generate hashId
2. Read draft, parse metadata
3. Convert markdown → HTML
4. Process image (sips + cwebp)
5. CSV append in website repo
6. JSON write in website repo
7. Build website
8. Push website

Step 5–7 happen in the website repo's working tree. Each publish is ~5–10 minutes of orchestration plus build time. As cadence increases (currently Sat/Sun insights + Tue/Thu narratives + Wed Ship = 5 posts/week), the per-publish friction compounds.

**Three approaches in original memo**:
1. **GitHub Action trigger**: workflow in piper-morgan-product that pushes publish packages to piper-morgan-website via GitHub API (`create_or_update_file`)
2. **Shared publish directory**: git submodule or subtree linking the two repos' publish surfaces
3. **API-based publish**: lightweight endpoint or Action in piper-morgan-website accepting a POST with slug, HTML, metadata, image URL

**Effort estimate**: medium (multi-day). #1 is probably most tractable for a Coding Agent subagent if PM wants to land it; needs Lead Dev or Architect consultation on auth + secrets.

### Issue 3.2 — `publish-to-blog` skill brittleness (improvement)

**Status**: emerging — observed today (Apr 28).

**Problem**: the publish-to-blog skill expects metadata as YAML frontmatter at the very top of the draft. Today's "The Deeper Why" had metadata after the title, which broke the regex match. I patched the publish script in-flight to handle either ordering, but the skill spec hasn't been updated.

**Plus**: `cwebp` path resolution. My in-flight script defaulted to `cwebp` on PATH; subprocess context didn't have `/opt/homebrew/bin` on PATH. Hardcoded the absolute path.

**Fix needed**:
- Update `publish-to-blog` skill spec to handle metadata at top OR after title
- Document `cwebp` path requirement (`/opt/homebrew/bin/cwebp` on macOS Homebrew install)

**Effort estimate**: ~30 min Docs work to update skill spec.

### Issue 3.3 — Image preprocessing automation (improvement)

**Status**: speculative; flagging.

**Problem**: PM creates source PNG, then publish pipeline does:
1. `sips -Z 1200 source.png` (in-place resize)
2. `cwebp -q 80 source.png -o dest.webp`

Both steps are deterministic; could be wrapped in a single Docs-side preprocessor that takes a source path + slug and outputs the webp. Not blocking; nice to have.

**Effort estimate**: ~30 min if pursued.

### Issue 3.4 — `medium-posts.json.backup-sync` artifact

**Status**: noted Apr 26 during Verify the Paraphrase publish; not investigated.

**Problem**: a `medium-posts.json.backup-sync` file gets auto-created during build/publish and lands in the website repo commit. Doesn't break anything but adds noise.

**Fix needed**: identify what creates it (probably `sync-csv-to-json.js` or similar); decide whether to gitignore or to fix the script.

**Effort estimate**: ~30 min investigation.

---

## Triage queue (current)

By rough effort × priority (Docs's ordering — open to PM input):

| # | Item | Effort | Priority | Notes |
|---|---|---|---|---|
| 1 | 1.2 alt text + caption rendering | 1h | medium | accessibility regression #18; touches every post |
| 2 | 1.1 blog index Medium-link bug | 1h | medium | bug since Mar 29; affects index UX |
| 3 | 2 duplicate article fix | 30m once PM specifies | high (PM-flagged) | gated on PM detail |
| 4 | 3.2 publish-to-blog skill spec | 30m | low | quality-of-life for me |
| 5 | 1.3 + 1.4 date display + category counts | 30m each | low | nice-to-have |
| 6 | 3.4 backup-sync artifact | 30m | low | noise reduction |
| 7 | 3.3 image preprocessing automation | 30m | low | speculative |
| 8 | 3.1 cross-repo handoff overhaul | multi-day | high (long-term) | needs Lead Dev/Architect; biggest payoff |

---

## How to update this doc

- When a new issue surfaces: add to relevant subtopic with status, problem, fix needed, effort estimate.
- When an issue is resolved: move to a "Resolved" section at the bottom (created when first item resolves) with commit hash + date.
- When PM raises a new subtopic: add it as a new top-level section.
- When effort or priority changes: update the triage queue.
- Keep the doc agent-neutral so any future agent (a real "web" role, or any role consulted) can pick it up.

---

*Created 2026-04-28 by Documentation Management per PM directive.*
