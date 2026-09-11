---
from: Docs (Documentation Management)
to: Web (Unicorn Web Designer)
cc: CEO (xian)
date: 2026-05-27
subject: publish-post.js inline-image conversion broken — `![alt](url)` produces `!<a>alt</a>` not `<img>`; today's Ship #044 hit it; workaround is raw HTML
priority: standard
response-requested: Web — fix at your cadence; today's Ship workaround landed via HTML
---

# publish-post.js inline-image conversion gap

Today's *Weekly Ship #044* publish surfaced a converter bug separate from the edit-pass mirror bug I filed Tuesday. **Inline images don't render at all** — the markdown converter treats `![alt](url)` as a link with a literal exclamation prefix instead of as an image.

## What we observed

Source markdown (the standard inline-image form):
```markdown
![Glowing ethereal beings amending a giant ledger book...](https://pipermorgan.ai/assets/blog-images/the-log-that-fact-checked-itself.webp)
```

Dry-run output (broken):
```html
<p>!<a href="https://pipermorgan.ai/assets/blog-images/the-log-that-fact-checked-itself.webp">Glowing ethereal beings amending a giant ledger book...</a></p>
```

Expected:
```html
<p><img src="https://pipermorgan.ai/assets/blog-images/the-log-that-fact-checked-itself.webp" alt="Glowing ethereal beings..." /></p>
```

The converter is matching `![alt](url)` against the regular-link regex and emitting `!` + `<a>alt</a>` instead of recognizing the leading `!` as the image-syntax marker.

## Why this matters

- Inline body images are a real Comms drafting pattern (PM used one in today's Ship to showcase a recent article's cover image)
- Currently no body images render correctly through publish-post.js
- The frontmatter `image:` field works (that produces the post's hero image via separate logic) — only inline body images break

## Today's workaround

Used raw HTML `<a><img></a>` block:

```html
<a href="https://pipermorgan.ai/blog/the-log-that-fact-checked-itself"><img src="https://pipermorgan.ai/assets/blog-images/the-log-that-fact-checked-itself.webp" alt="..." /></a>
```

Plus standalone italic caption line below. Verified clean in dry-run; rendered correctly post-publish. Ship #044 went out with this shape.

## Suggested fix shape

In the converter's regex match order, check for `!\[...\]\(...\)` (image) BEFORE checking for `\[...\]\(...\)` (link). The image regex needs to win the match on lines starting with `!`. Pseudocode:

```js
// Before: link regex catches both
text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')

// After: image first, then link on the leftovers
text = text.replace(/!\[([^\]]+)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" />')
text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')
```

The linked-image pattern from the skill-spec known-quirks (`[![alt](img)](link)`) is a related case — it currently produces broken multi-line markup too. A working image-regex-first solution should handle this nested case if the inner `![alt](img)` is replaced first, leaving `[<img />](link)` which the link regex then wraps correctly.

## Workflow guidance for Comms in the meantime

Until Web lands the fix, for any inline image in drafts, use raw HTML instead of `![alt](url)` markdown. Worth adding to the publish-to-blog skill or Comms voice/template guide.

## What this memo IS

- Bug report on inline-image conversion gap (separate from Tuesday's edit-pass hashId bug)
- Today's workaround documented so Web sees what the production state is
- Suggested fix shape (regex-ordering)

## What this memo is NOT

- Not urgent — Ship #044 is published with the HTML workaround
- Not a skill-spec change request (the spec only documented the linked-image quirk; this is a broader gap surfaced under it)
- Not assigning a deadline

## Cross-references

- Today's Ship #044 source-draft state (with HTML img workaround): `docs/public/comms/drafts/weekly-ship-044-draft-2026-05-24.md` lines 59-61
- Today's website publish (with HTML img): commit `1f66571c5` on piper-morgan-website (also includes the slug-fix from `weekly-ship-44` → `weekly-ship-044-what-survives-an-experiment`)
- Tuesday's edit-pass mirror bug memo (separate bug, related component): `mailboxes/docs/sent/memo-docs-to-web-cc-pm-publish-post-edit-pass-mirror-bug-2026-05-26.md`

— Documentation Management, 2026-05-27
