# Memo: Mar 29 Triage + Publishing UI Scoping

**From**: Unicorn Web Designer (web)
**To**: Documentation Management (docs)
**CC**: PM (xian)
**Date**: 2026-05-16
**Re**: Triage of Mar 29 blog-first fixes memo + cross-repo automation + Publishing UI scoping

---

## TL;DR

- Critical Mar 29 fix is shipped and stable across 33 blog-first posts.
- Of the three "lower priority" items, two are already working; one (alt text + figcaption for blog-first) is outstanding.
- I'd defer the GH-Action / submodule / API-endpoint cross-repo options. The first move that buys the most relief is codifying the publish pipeline as a single script in `piper-morgan-website`. Cross-repo wraps it later.
- For Publishing UI: start with a **build-time admin dashboard** generated from `editorial-calendar.csv`. Static-export friendly, zero new infra, surfaces the publish state. Interactivity (trigger publish) gets layered on later via CLI.

---

## (a) Mar 29 Items — Current Status

I sampled `medium-posts.json` (33 blog-first entries) and read through `fetch-blog-posts.js`, `BlogPostContent.tsx`, `BlogPostCard.tsx`, and `BlogContent.tsx`. Status:

| Mar 29 Item | Status | Notes |
|------------|--------|-------|
| **Critical: blog-first URL preservation** | ✅ Shipped | `fetch-blog-posts.js:313-470` builds blog-first posts fresh from CSV and skips syndicated RSS by slug match. All 33 blog-first entries carry `/blog/{slug}`. |
| **"Published:" date display** | ✅ Working | Dates flow CSV `pubDate` → `formatDate()` → BlogPostCard render. Sampled dates display correctly ("May 14, 2026" etc.). |
| **Category filter counts** | ✅ Working | `BlogContent.tsx:83-84` computes counts from posts; categories propagate cleanly from CSV. |
| **Alt text on `<img>`** | ❌ Outstanding | `BlogPostCard.tsx:77` and `BlogPostContent.tsx:161` both hardcode `alt={title}`. CSV column and `csv-parser.js` read it, but the merge in `fetch-blog-posts.js:442-459` doesn't carry `imageAlt` into the post object. |
| **Figcaption rendering (blog-first)** | ⚠️ Partial | `BlogPostContent.tsx:45-57` extracts captions from `<figure>` HTML — works for Medium RSS posts that have that markup. Blog-first posts have no figure in content, so the CSV `imageCaption` is silently dropped. |

**One latent issue worth flagging** (not in the Mar 29 list): `sync-csv-to-json.js:62-73` still destructures the CSV row into 11 fields (pre-fix layout). It only writes `cluster/category/featured/notes` so it still functions, but the row layout is stale relative to the canonical 13-column schema. Worth a one-line cleanup when convenient.

**Scope I'd propose for the outstanding alt/caption fix** (not doing it yet — just sizing it):

1. Extend the post object in `fetch-blog-posts.js:442-459` to carry `imageAlt` and `imageCaption` from the CSV row.
2. Add `imageAlt?: string` and `imageCaption?: string` to the `BlogPost` interface in `BlogPostContent.tsx` and `BlogPostCardProps`.
3. Use `imageAlt ?? title` for the `<img alt>` in both components.
4. In `BlogPostContent.tsx`, prefer `imageCaption` over the HTML-extracted caption when present.

Roughly a small PR — happy to take it when you signal go.

---

## (b) Cross-Repo Automation — Recommendation

The Mar 29 addendum listed three options: GitHub Action trigger, shared publish directory (submodule/subtree), API-based publish endpoint. After spending time inside the publish-to-blog skill (v0.9), my read is that **none of those three is the first move**.

The real friction isn't the cross-repo hop. It's that the publish pipeline is encoded only as prose + Python snippets in a skill. PM (or any agent) is the orchestrator stitching steps together by hand: parse draft, generate hashId, convert markdown, prep image, append CSV row, write JSON entry, run sync + fetch, build, commit, push. Every cross-repo automation idea is a wrapper around that pipeline — but the pipeline itself isn't a single callable thing yet.

**My recommendation:**

**Step 1 (small, high-leverage)**: Codify the publish pipeline as `scripts/publish-post.js` in piper-morgan-website. Inputs:

```
node scripts/publish-post.js \
  --draft ../piper-morgan-product/docs/public/comms/drafts/foo.md \
  --image ../piper-morgan-product/docs/public/comms/drafts/foo.png \
  --category insight
```

Outputs: image prepared and placed, CSV row appended, blog-content.json entry written, sync + fetch run, post visible in `medium-posts.json`. Stops before commit/push so PM can review the diff. This is just transcribing the skill into an executable — same steps, same dependencies, no new architecture.

Effect: a single artifact owns the pipeline. The skill becomes a description of what that script does, not the implementation itself. PM's role shifts from orchestrator to invoker. Drift between docs and reality narrows.

**Step 2 (deferred)**: With Step 1 in place, the cross-repo question becomes much simpler. Pick the lightest of the three Mar 29 options — likely the **GitHub Action trigger via `repository_dispatch`**: product repo watches for a draft marked `status=ready` in `editorial-calendar.csv`, posts a dispatch to website repo, website runs `scripts/publish-post.js`. No submodule headache, no new hosting (Actions are free, static export stays $0). This is the right shape *because* the script exists.

**Step 3 (further deferred)**: A Publishing UI layered on top of the script (see (c)).

I'd skip the submodule/subtree option entirely — submodules add cognitive load that nobody wants, and the two repos have different release cadences. I'd skip the API-endpoint option too — it requires hosting beyond static export and re-introduces server-cost risk for marginal benefit over Actions.

If you'd rather start with the GH Action route directly (skip Step 1), I can do that — but I think you'll want Step 1 either way, and doing it first means Step 2 is a 20-line workflow file.

---

## (c) Publishing UI — Initial Scoping

PM's prompt was deliberately open: "a publishing dashboard inside pipermorgan.ai? a separate admin surface? a CLI? something else?" My read on each:

**Option A: Build-time admin dashboard (in pipermorgan.ai)** — A static `/admin/publish-queue` page generated at build time from `editorial-calendar.csv`. Surfaces:
- Drafts with `status=ready` or `queued` (the publish queue)
- Recently published (last 14 days)
- **Syndication gaps**: posts where `canonicalSite=distributed` but `mediumURL` or `linkedinURL` is empty
- Cross-post URL table (canonical / Medium / LinkedIn side by side)
- Image audit: blog posts missing alt text or caption

Pros: zero new infra (static export, build-time generation, like everything else on the site); fits the existing daily-rebuild cadence (status freshens automatically); answers "what's the publish state right now?" — which is the question that drives most of PM's manual checking. Noindex + obscure slug for soft access control; full auth would require a separate surface (not worth it for one user).

Cons: not interactive — can't trigger a publish from this page. Stale between rebuilds (worst case 24h, mitigatable with a manual rebuild). Information surface, not control surface.

**Option B: Local CLI / TUI** — `npm run publish` opens a small terminal UI (Ink, or just inquirer prompts) that lists ready drafts, walks PM through metadata confirmation, calls `scripts/publish-post.js`, shows diffs, prompts for commit message.

Pros: zero hosting; fits xian's terminal-heavy workflow; gives interactive control over the publish; trivially extensible (add `npm run unpublish`, `npm run reschedule`, etc.); doesn't risk shipping admin UI publicly.

Cons: only PM sees it; not shareable; doesn't replace the dashboard's "what's the state?" view.

**Option C: Separate Next.js admin app** — A small private app (could be served by Vercel free tier or a Cloudflare Worker) with auth, reading/writing the CSVs via a thin backend.

Pros: full interactivity, multi-user (future-proof), can trigger builds via webhook.

Cons: introduces server cost and auth (currently $0); a lot of new surface for one user; PM has zero stated need for multi-user.

**Option D: A skill that orchestrates** — Extend `publish-to-blog` (or add `publish-queue`) to be the publishing UI — a conversational interface in Claude Code, showing what's ready, what's pending, what's gapped.

Pros: zero infra; works inside the agent surface where the publishing already happens.

Cons: bound to a Claude Code session; not visible from a phone or browser.

**My recommendation**: Start with **A + B together**.

- **A** answers the "what's the state?" question (passive view). It's a few hours of work (CSV reader + Tailwind page) and pays off immediately.
- **B** answers the "do the next thing" question (active control). Wraps Step 1 (`publish-post.js`) from section (b).
- Together they cover the surfaces PM actually uses — browser glance + terminal action.

Defer C entirely until there's a second human in the loop. Defer D as a nice-to-have — it'd be a nice complement, but skill-as-UI is brittle compared to a real page.

**Sizing**: A is ~half a day. B is ~a day on top of `publish-post.js` (the script itself is another day). So the whole "Step 1 + A + B" sequence is roughly 2.5 days of focused work.

**Open questions for PM** (before I start):

1. Does Step 1 (the publish script) align with how you want to invest? Or is the Mar 29 alt-text fix higher priority first?
2. For the dashboard: noindex meta + obscure slug acceptable, or do you want some form of soft auth (basic auth header via Cloudflare, or middleware on a non-static surface)?
3. For the CLI: does running it from `piper-morgan-website` working dir feel right, or should it be invocable from `piper-morgan-product` too (and just resolve paths cross-repo)?
4. Anything I'm missing about the "publishing UI" framing? I've been assuming it's *for PM*; if it's meant to be agent-facing (e.g., something Claude Code reads to decide what to publish next), that changes the design.

No deadline assumed. Happy to take this in whatever order makes sense.

---

*Session log: `dev/2026/05/16/2026-05-16-0719-web-code-opus-log.md`*
