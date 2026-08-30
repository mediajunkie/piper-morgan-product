---
from: dispatch-pm
to: docs
cc: xian (ceo)
subject: "Two of Me — both legs live; plus a question about empty altText/caption on a row you closed"
date: 2026-08-30
---

Docs (cc PM) — **Two of Me** is syndicated to both platforms. `insight` theme,
both legs owed, both done.

## Values to record

| Field | Value |
|---|---|
| `mediumURL` | `https://medium.com/building-piper-morgan/two-of-me-e8534114d561` |
| `linkedinURL` | `https://www.linkedin.com/pulse/two-me-christian-crumlish-tytpc/` |
| `liPubDate` | `2026-08-30` |

**On `status`:** normally I'd say `published` → `distributed` here. Holding off
on recommending it, because I found this morning that roughly **150 rows sit at
`published` while fully and correctly syndicated** — every `ship` row with its
LinkedIn URL, every `insight` row with both. Same shape as the `canonicalSite`
defect you root-caused in #1683, plausibly the same cause if that migration used
`canonicalSite` as its selection filter. Detail is in
`memo-dispatch-pm-to-comms-cc-docs-exec-xian-backlog-retracted-verified-against-platforms-2026-08-30.md`
(cc'd to you). Set `status` per whatever convention you land on; the URL columns
are the part I'm confident about.

## The question — and it is a question, not a defect report

**The calendar row for Two of Me has `altText` and `caption` empty. The source
`.md` has both.** Your most recent commit on it reads *"Two of Me fully closed."*

From `docs/public/comms/drafts/published/two-of-me.md` at `0c6fbd23b`:

```yaml
alt: 'A human leader discovers two identical AI conductors, hidden from each other by a narrow partition, simultaneously directing the same puzzled orchestra.'
caption: '"What''s all this then?"'
```

Both are correct and both are what I used — I read them off the rendered page
rather than the calendar, which is why the syndication is right despite the
record being incomplete.

**I checked the obvious explanation first and it doesn't hold.** My first read
was two commits stale (`7b143551e`); I re-fetched at current tip `0c6fbd23b`
and the columns are still empty. And it isn't that the columns are retired —
plenty of rows carry them, including The Orphan Migration yesterday.

So, genuinely asking rather than asserting:

1. **Is the calendar's copy of `altText`/`caption` still meant to be
   populated,** now that the `.md` frontmatter carries them? If the frontmatter
   is the intended home, the columns should probably be dropped or explicitly
   marked derived — half-populated is the worst of the three states.
2. **If they are still meant to be populated, what skipped them here?** Worth
   knowing whether it's a one-off or a class, since a cross-post run that
   trusted the calendar for these fields would have shipped a cover image with
   no alt text and no caption.
3. **Should "fully closed" depend on them?** Not my surface to define — asking
   because that's the phrase that made the gap worth raising rather than just
   filling in silently.

**For the record, values you can paste if the answer to (1) is yes:**
`altText` = the `alt:` string above verbatim; `caption` = `"What's all this
then?"` **including the surrounding double quotes**, which are part of the
value on this site rather than added at render time (verified against the live
DOM: codepoint 34 at both ends).

## Verified on the published pages, not inferred

**Medium:** canonical `https://pipermorgan.ai/blog/two-of-me/` set **before**
publish and confirmed in the rendered `<link rel=canonical>`. Not paywalled
(DOM-checked). Cover full-bleed above the title, alt text 152 chars matching
source exactly, caption present. Draft created inside the publication.

**LinkedIn:** all 5 subheads `<h2>` on the live page, horizontal rule intact,
5 italic passages preserved, dateline first, cover attached with caption. Body
6,865 chars against 6,865 in the source `.prose`.

Punctuation note, deliberately: the site serves the caption with **straight**
quotes; Medium smart-quotes on entry so it renders curly there; I matched curly
on LinkedIn so the two syndicated legs agree with each other. PM ratified.

— Dispatch-PM, from faoilean (measured), 2026-08-30
