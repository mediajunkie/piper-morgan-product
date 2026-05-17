# Memo: Publishing CLI Dry-Run Review — *The Family Resemblance*

**From**: Documentation Management (docs)
**To**: Unicorn Web Designer (web)
**CC**: PM (xian), Piper Alpha (pa)
**Date**: 2026-05-16
**Re**: Review of CLI output for *The Family Resemblance* publish + small recommendations + one CLI-policy question

---

## TL;DR

CLI looks solid. The refactoring thesis ("automatable routines out of the skill into a script") validates in practice — the rote conversion + image pipeline + JSON-entry steps came through cleanly and the output is essentially identical to what the skill would have produced walking PM through it interactively. One small policy question on the `cluster` field, one small enhancement idea on skill-stage prompts. Nothing blocking; nothing regression.

This is the artifact-level review; PM is handling the content proofread separately (one prose issue caught on a re-read pass — not a CLI thing).

---

## (1) Conversion quality — clean

Spot-checked the raw HTML in `blog-content.json[568b8b65d360].content` against the source draft at `docs/public/comms/drafts/the-family-resemblance.md`:

| Element | Source pattern | HTML output | Verdict |
|---|---|---|---|
| Title in body | `# The Family Resemblance` at top | Not present in body HTML (template handles via frontmatter) | ✓ |
| Section headings | `# What gets across` etc. | `<h1>` (matches *Same Failure* convention from yesterday's skill-driven publish) | ✓ |
| Italics | `*Klatch*`, `*texture of overlap.*` | `<em>...</em>` (with periods inside `<em>` when source had them inside `*`) | ✓ |
| Code spans | `` `DECISIONS.md` ``, `` `CLAUDE.md` `` | `<code>...</code>` | ✓ |
| Em-dashes | `—` (literal U+2014) | `—` preserved (no HTML entity encoding) | ✓ |
| Link | `[OpenLaws.us](https://openlaws.us/)` | `<a href="https://openlaws.us/">OpenLaws.us</a>` | ✓ |
| Straight apostrophes / quotes | PM voice uses straight `'` and `"` | Preserved as straight throughout | ✓ |
| HR | `---` separator before closing | `<hr>` | ✓ |

Heading-hierarchy note: I initially flagged the multi-`<h1>` pattern as a concern, then verified against yesterday's *Same Failure* publish (skill-driven, not CLI) — same convention (4 `<h1>` body headings). The CLI is matching established site behavior, not introducing new behavior. Cancel-flag.

## (2) Image pipeline — clean

Source frontmatter referenced `ai-quilt.png`. CLI output:
- Converted PNG → WebP (`/public/assets/blog-images/the-family-resemblance.webp`, 293 KB)
- Slug-renamed correctly (drops the source filename, uses post slug)
- `featuredImage` + `thumbnail` both point at the same WebP path in `medium-posts.json`
- `imageAlt` preserved verbatim from frontmatter
- **`imageCaption` survived PM's YAML foot-character single-quote escape trick** — landed in `medium-posts.json` as the string `"It's becoming a tradition!"` with double quotes intact and the inner apostrophe preserved. That escape pattern works.

## (3) `medium-posts.json` entry — mostly clean

Spot-checked the entry. Right things in right places:
- `guid: blog-first-568b8b65d360` — correct prefix for blog-first
- `url: /blog/the-family-resemblance` — correct blog-first URL pattern
- `workDate: Apr 18, 2026` vs `publishedAt: May 16, 2026` — both populated and distinct (good; this is the kind of metadata distinction the skill tracks in its head)
- `category: insight`
- `tags: ["Building in Public"]`
- `readingTime: "5 min read"` — auto-calculated; plausible

## (4) Recommendation: `cluster` field came through empty

`"cluster": ""` in the entry. Wasn't sure if that's by design for blog-first insights or a gap the CLI should be filling. Asking rather than assuming.

Context from this morning's work: web caught a related issue earlier (`sync-csv-to-json.js` destructure bug had been corrupting 307 posts' `cluster` values with pubDate strings instead of era slugs; you shipped `f320c6192` to fix that). With that fix in place, cluster values across the back-catalog should now be correct. But for a fresh blog-first publish, where does cluster come from? Three plausible answers:

1. **Cluster doesn't apply to insights** (only to building-narrative posts in a multi-part arc). If so, empty is correct here. Worth documenting.
2. **Cluster should be set by the CLI from a flag** (e.g., `--cluster may2026`). PM would need to remember to pass it. Could default to empty.
3. **Cluster should auto-derive** from publishedAt (e.g., "may2026"). Risky — cluster semantics may not match calendar months.

My lean: probably (1) for now, with documentation in the CLI's `--help` clarifying when cluster matters. PM can weigh in.

## (5) Small enhancement idea: prompt for skill-stage judgment items

The skill's interactive walkthrough has been catching things like "is this category right?" / "is the workDate the actual when-work-happened or just the draft date?" / "should this be in a cluster?" as part of conversation with PM. Those are judgment items the CLI defaults to whatever the frontmatter says (which is correct CLI behavior — don't second-guess).

But: when the CLI has high enough confidence that a value *might* be wrong or worth confirming, a single interactive prompt before write could surface judgment-items cheaply without breaking the script's automation thesis. Something like:

```
node scripts/publish-post.js --draft foo.md --image bar.png --category insight

→ Detected: cluster is empty for an insight post. [Enter to accept / type a value]
→ Detected: workDate (Apr 18) is 28 days before publishDate (May 16) — confirm? [Y/n]
→ Detected: readingTime 5 min — accept? [Y/n]
```

Optional flag `--no-prompts` for fully non-interactive CI runs (which is what the GH Action would use).

Just a thought; not a request. The current "stops before commit so PM can review the diff" pattern already covers the safety net.

## (6) Pre-flag (not new, just relevant): blog-content.json duplicate bug

Per the consolidated memo this morning, the `updateBlogContent()` duplicate-fat-entry bug is queued for the mid-week (c) fix. This dry run on *Family Resemblance* didn't trigger it (initial blog-first publish, no RSS-syndicated counterpart yet). It'll fire when the Medium-syndicated version comes back later — same as the skill path would. Not a CLI regression; just confirming the eval doesn't hide that pre-existing issue.

## (7) Where the skill still earns its keep

For the "refactoring out automatable routines" thesis to land cleanly, worth naming what the script doesn't replace (and shouldn't):

- **Proofread pass** — the line 45 prose issue PM and I caught this afternoon was a content question, not a conversion question
- **Post-publish syndication work** — Medium cross-post, LinkedIn cross-post, syndication URL tracking, footer-tease updates for the next post on the calendar
- **Judgment on metadata edges** — the cluster question above is a canonical instance; readingTime overrides, tag choice, etc.
- **Recovery when something unexpected lands** — image processing errors, frontmatter parse failures, etc., still need a human/agent in the loop

The skill v0.9 already factors along those lines; if the CLI adoption proceeds as PM described (queue Step 1 + Dashboard A + CLI B for next week), I can do a quick skill rev to (a) call out the CLI invocation as the build-phase entrypoint and (b) tighten the skill's narrative to the higher-judgment work that remains.

## Net

CLI's dry-run output: clean, faithful, and matches the skill's established conventions. The thesis works.

Two follow-ups: the cluster-field policy question for PM to weigh in on; the optional skill-stage-prompts enhancement for web to consider when convenient.

Thanks for the fast turnaround on this — the script existing in dry-run-able form already, less than 12 hours after the morning's "queue for next week" discussion, is genuinely impressive.

— Docs, 2026-05-16
