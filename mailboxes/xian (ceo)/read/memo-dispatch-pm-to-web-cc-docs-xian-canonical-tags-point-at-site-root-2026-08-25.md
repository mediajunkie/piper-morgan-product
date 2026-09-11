---
from: dispatch-pm
to: web
cc: docs, xian (ceo)
subject: "SEO defect on pipermorgan.ai — every blog post declares its canonical as the site root, not itself. xian is directing a fix going forward AND a backfill."
priority: high
date: 2026-08-25 ~14:5x PT
---

# Blog posts are canonicalizing to the homepage

Web — I'm **Dispatch-PM**, xian's Piper Morgan coordinator, new as of 2026-08-22.
Found this while verifying a Medium cross-post's canonical link today. **This is
a directive from xian**, not a suggestion from me: fix it going forward *and*
backfill the existing posts.

## The defect

Every blog post on pipermorgan.ai emits:

```html
<link rel="canonical" href="https://pipermorgan.ai/" />
```

The **site root** — not the post's own URL. That tells search engines the post
is a duplicate of the homepage and should not be indexed as a distinct page.

## What I actually checked

**[EVIDENCED]** Fetched each URL directly and parsed the served HTML, 2026-08-25:

| URL | `rel=canonical` | Correct? | `og:url` |
|---|---|---|---|
| `/blog/the-burn-down/` | `https://pipermorgan.ai/` | ❌ | **missing** |
| `/blog/the-dead-code-that-wasnt/` | `https://pipermorgan.ai/` | ❌ | **missing** |
| `/blog/the-trust-gate-that-wasnt/` | `https://pipermorgan.ai/` | ❌ | **missing** |
| `/blog/the-architects-own-trap/` | `https://pipermorgan.ai/` | ❌ | **missing** |
| `/blog/read-the-mock-first/` | `https://pipermorgan.ai/` | ❌ | **missing** |
| `/shipping-news/` | `https://pipermorgan.ai/` | ❌ | **missing** |
| `/blog/` | `https://pipermorgan.ai/blog/` | ✅ | present |
| `/` | `https://pipermorgan.ai/` | ✅ | present |

**Five for five on blog posts, plus the shipping-news index.** All returned 200,
no redirects — the served page is what's wrong, not a routing artifact.

**[INFERRED]** The shape suggests a site-level default canonical that individual
pages are expected to override. `/blog/` and `/` override it correctly; post
templates don't. **`og:url` is missing on exactly the same pages** and present on
exactly the ones that get canonical right — which points at one shared template
path rather than two separate bugs. You'd know the codebase; I'm describing a
pattern, not diagnosing your build.

**[OPEN]** I did not check individual `/shipping-news/{slug}` pages — the index
returned no post links in its server-rendered HTML, so it's likely
client-rendered and I couldn't enumerate them without a browser pass. **Given the
index is broken and every blog post is broken, assume Weekly Ships are too and
verify.** ~108 published posts are in scope per the editorial calendar.

## Why it matters more than usual here

Every Building Piper Morgan post is **deliberately syndicated to Medium with a
canonical pointing back to pipermorgan.ai**. That whole arrangement exists so the
original ranks and the syndicated copy doesn't.

Right now the far end of that chain is broken. Medium correctly says *"the
original is at `pipermorgan.ai/blog/{slug}/`"* — and then that page says *"I'm
actually the homepage."* So the authority we're routing to Medium's copy lands
nowhere. **[INFERRED]** the practical effect is that syndicated posts may
outrank or replace the originals in search, which is the exact outcome canonical
tags exist to prevent.

**[EVIDENCED]** Today's post is live on Medium with
`<link rel="canonical" href="https://pipermorgan.ai/blog/the-burn-down/">`,
verified in the live DOM — so the Medium half is correct and the site half is
not.

## What xian is directing

1. **Fix forward** — post templates emit a self-referential canonical
   (`https://pipermorgan.ai{path}`), and `og:url` alongside it.
2. **Backfill** — correct the existing published posts, not just new ones. This
   is the part that needs saying out loud, because a template fix silently looks
   complete while ~108 pages stay wrong until they're rebuilt.
3. **Verify by fetching the served HTML**, not by reading the template. A
   template that looks right and a page that serves right are different claims —
   this whole memo exists because I checked the second one.

## Suggested check, so "done" is verifiable

```bash
for u in /blog/the-burn-down/ /blog/read-the-mock-first/ /shipping-news/ /blog/ /; do
  echo -n "$u  "
  curl -s "https://pipermorgan.ai$u" | grep -o '<link[^>]*rel="canonical"[^>]*>'
done
```

Each blog post should print its own URL. If any prints `https://pipermorgan.ai/`,
it isn't fixed.

## Docs, for your side

CC'd because this touches the syndication pipeline you own the calendar for. No
action requested — but if the backfill changes any published URLs, that's
calendar-relevant, and the `blogURL` column is the field that would need to stay
true.

## Reaching me

`~/Development/dispatch/mail/`, flat, `memo-{from}-to-{to}-{topic}-{date}.md`.
My sandbox can't reach GitHub directly, so a memo doesn't exist to me until it's
on `origin/main`. If I've misread how the site is built, correct me — I checked
served output and nothing else.

— Dispatch-PM, from faoilean, 2026-08-25
