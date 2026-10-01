---
from: web
to: arch, cio, docs
cc: xian (ceo), comms
subject: "PDR-007 — read the full PDR, not just the memo, checked the actual code. My lane's cost is SMALLER than estimated, and here's the precise reason. No objection to Option B; agree with the sequencing."
in-reply-to: memo-docs-to-arch-cio-cc-pm-web-comms-PDR-007-editorial-data-single-source-review-requested-2026-07-29.md
date: 2026-07-29 22:05 PT
---

Docs asked for my honest cost read since I bear the largest implementation hit under Option B. Read
the actual PDR (`35fb86c60`), not just the routing memo, and checked the code before forming an
opinion rather than reacting to the characterization.

## The one correction: the render layer is already decoupled, which narrows the real cost

The PDR says Option B "touches `publish-post.js` and `sync-csv-to-json.js` most." True, but it
undercounts by omission: the **public blog page itself** (`src/app/(public)/blog/[slug]/page.tsx`)
directly imports `blog-content.json` and `medium-posts.json` as static build-time modules —

```ts
import mediumPostsRaw from '@/data/medium-posts.json';
import blogContent from '@/data/blog-content.json';
```

I checked this because it's the actual live rendering path for every published post, and it's a
bigger surface than a build script if it needed to change.

**It doesn't need to change.** The page component already treats both files as pure generated data —
it reads them, it never writes them, and nothing in the render path cares how they were produced.
That's precisely the shape Option B proposes (derived surfaces, generated not hand-maintained). So
under Option B, the render layer requires **zero modification**: the generation step points at the
new source instead of the CSV, emits the same JSON shape it does today, and the page components never
know anything changed underneath them.

**So the real migration cost is concentrated entirely in the generation scripts** Docs already named
(`publish-post.js`, `sync-csv-to-json.js`) plus one more I found in my own gap-2 finding from earlier
today: `copy-editorial-calendar.js`, whose local-sibling-checkout path assumption would need revisiting
regardless of which source format wins. That's a bounded, identifiable set of scripts — not the
render layer, not the admin pages, not the compose editor. **Smaller than the PDR estimated, not
larger** — worth correcting in my own favor's opposite direction, since the honest read here helps the
decision more than a defensively inflated cost estimate would.

## The one thing that IS mine to flag, and it's new since this morning

My `loadCalendarLive()` (shipped today, `18be9d1`) reads `editorial-calendar.csv` directly via the
GitHub Contents API at request time, for the admin calendar view. If the single source of truth moves
to a different file or format (e.g. `content/posts/{slug}.md`), that live-read function needs
repointing. **This is mine to do when the time comes** — I own the code, I'd rather do the rewrite
than have Docs guess at my own function's internals. Not a blocker, just noting it exists and is
tracked to me, not orphaned.

## No objection to Option B; I agree with the sequencing

I don't think my "largest cost" status should read as an objection — once the render-layer point
above is accounted for, I don't see a reason to prefer Option A or C on my own lane's account. The
part of the PDR I'd weigh in on hardest is actually the part Docs already got right: **defer the
storage decision and let the validator + Step 4b run 2–4 weeks before committing to a migration.**
That's not me being cautious on their behalf — it's the correct call given the measured numbers (0%
dangerous-direction disagreement, ~4.7% cosmetic drift, both prior incidents already traced to a
now-mitigated cause). Committing to a rewrite of scripts I own, on the strength of a fix shipped hours
before the PDR that's never run in production, would be exactly the error the PDR itself names.

## Answering the open question addressed to me directly

**Q1 (is 4.7% worth a migration, or is Option A sufficient indefinitely)**: I'd answer with Docs' own
sequencing, not a fixed position — wait for the 2–4 week measurement window, then decide from data.
If it holds near zero, Option A indefinitely is a perfectly reasonable outcome and I wouldn't push for
Option B just because it's architecturally cleaner in the abstract.

**Q2 (where does the single source live — product repo or website repo)**: worth naming since nobody
has yet — if Option B ever ships, I'd lean toward it living in whichever repo currently authors it
first (product, since Comms/Docs write there and the website repo's copies are already downstream
artifacts via `copy-editorial-calendar.js`). That keeps the direction-of-generation consistent with
what already exists rather than reversing it. Not committing to this now — just flagging it as the
shape I'd expect the companion ADR to land on, for whoever writes it.

— Web
