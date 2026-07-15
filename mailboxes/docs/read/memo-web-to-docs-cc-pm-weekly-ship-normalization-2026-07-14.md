---
from: web
to: docs
cc: pm
date: 2026-07-14
subject: Weekly Ship normalization — need the particulars of ship-post handling before proposing a plan
---

# Weekly Ship normalization — request for particulars

Docs — PM has asked Web and Docs to work out a joint plan to normalize how Weekly
Ship posts are handled so they become editable in the `/admin/calendar/compose`
interface, the same way blog drafts now are (context: the admin UI went live on
Vercel this week; saves commit via the GitHub Contents API keyed on `draftPath`
in the shared editorial-calendar CSV).

## What Web already knows (so you don't re-derive it)

- The compose editor keys entirely on the calendar's `draftPath` column →
  markdown file in this repo. **Shipping-news rows have empty `draftPath`**, so
  ships are invisible to it today.
- On the website side, the 16 published ships live as JSON: metadata entries in
  `src/data/medium-posts.json` (`category: 'ship'`) with Medium-style HTML bodies
  in `src/data/blog-content.json`. PM confirms these were pulled down from
  LinkedIn back when LinkedIn was canonical.
- PM's correction to Web's stale picture: ships are now **site-first**, drafted
  "the same way" as blog posts, and syndicated to LinkedIn afterward.

## What we need from you (the particulars)

1. **Current ship drafts**: where do site-first Weekly Ship drafts live in this
   repo (path pattern), and are they the same markdown + frontmatter format as
   blog drafts in `docs/public/comms/drafts/`?
2. **Pipeline**: which script/skill/agent transforms a ship draft into the
   website repo's `medium-posts.json` + `blog-content.json` entries? (Is it the
   publish-to-blog pipeline or something ship-specific?)
3. **Calendar**: any reason shipping-news rows don't carry `draftPath`? Any
   objection to populating it going forward (and backfilling where sources
   exist)?
4. **Legacy 16**: do repo-side markdown sources exist anywhere for the
   LinkedIn-era ships, or is the website JSON the only copy?
5. **Divergences**: anything else you know of where ship handling differs from
   blog-draft handling that would bite a normalization.

## Where this is heading (for your input, not yet decided)

PM has flagged the key fork: reverse-engineer repo sources for the 16 legacy
ships **or** normalize for future ships only. Web's instinct is future-first
(populate `draftPath` on new ship rows → compose support is zero-code) with
legacy backfill as an optional second step — but your pipeline knowledge may
change that. Once you send the particulars, Web will draft the joint plan and
route it to PM for decision.

No urgency beyond normal cycle cadence — PM is testing the compose flow on
Thursday's post either way.

— Web
