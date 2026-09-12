---
image: ''
alt: ''
caption: ''
---

# Piper Morgan Eras

*September 2026*

On the Piper Morgan website where this blog appears canonically (before some posts are syndicated to the Building Piper Morgan newsletter on LinkedIn or the Medium publication of the same name, or both), the navigation includes a working "eras" structure that clusters the posts into seven chronological periods, each with a description, each applying to a set of posts that belong to that era. 

The concept requires periodic review and refactoring by its very nature, and it's been through four iterations and redesigns, but the first attempts failed in various ways that all boiled down to: we designed a scheme, an agent built it, and then we never verified that the posts actually landed where the scheme said they would.

# One Sunday, twelve episodes

Back on October 12, 2025, this project's founder sat down at 7:01 in the morning with a numbered priority list that included, at item seven: "group the narrative posts into named periods," so 156 scattered posts would read as a story instead of a pile. By 9:01 that night, the work was done: twelve episodes, each a dated window, each with a name. Things like *Genesis & Architecture. The Complexity Reckoning. Reflection & Evolution.*

This twelve-episode scheme held for about a month. By November (I was still posting daily updates then), the most recent (*Production Transformation*) had already swollen to 31 posts while its neighbors sat at eight or nine, so an AI-run analysis proposed rebalancing, and the count of episodes went to fifteen. So far so good.

# Backwards down the number line

By March 2026 the blog had 275 posts. The fifteen-episode scheme was still sitting in the code, present in every page that referenced it but along the way the organization refreshed and design updates had completed detached the posts from their episode assignments. Now. each of the episodes matched **zero** of those 275 posts. The episode definitions and the actual post data had drifted apart so completely that the connection between them had stopped existing in practice, while every page kept rendering as though it still worked.

Posts kept publishing through the normal pipeline. The episode assignments just never got extended alongside them. A scheme that isn't checked against the data it's supposed to organize fails with a whimper, not a bang. It sat that way till I actually looked at it again.

The fix this time was a full refactor and a full rebuild: five non-overlapping eras, spanning the whole timeline from May 2025 forward, all 275 posts reassigned by actual work date. 

1. The Build. 
2. The Methodology. 
3. The Reflection. 
4. The Foundation. 
5. The Sprint. 

This time the assignment was mechanical — computed from the data, not maintained by hand — which is exactly the property the fifteen-episode scheme had been missing.

# Stale again in August

Five eras covered the story through March 2026 but the project didn't stop in March. By mid-August, five months of work had been added to the blog's narrative with no era at assigned, for the same underlying reason as before: the scheme had a fixed endpoint and no process for extendinfg it.

My communicatons chief agent (Comms) proposed two new eras to close the gap — The Mechanism and The Alpha — argued from two events a reader could actually recognize: the move to always-on infrastructure (when I put all my agents on semi-autonomous duty cycles), and the point the hosted alpha opened to real outside testers. It took me four days to realize that Comms was waiting for my approval and I green-lit it on the spot. Comms built the update that same evening: two new eras added to the code, a hundred-plus posts reassigned, catching a fix along the way: the newest era had no end date yet, and the code had been representing that with a placeholder that would eventually go stale, so Comms changed it to render "Present" instead of pretending to know a date nobody could know yet.

# The inevitable bug.

The fix Comms implemented itself had an error in it.

When they extended the assignment to the two new eras, they checked their work against every post already correctly categorized, and it matched perfectly. What they didn't do was step back and ask whether the *method* would generalized to posts they hadn't touched yet. Weeks later, filling in the remaining gaps, the "unicorn" web designer / developer agent (Web) found that roughly 260 older posts were sitting with no era at all or a leftover pre-migration label, and diagnosed it as a judgment call: something that would need a person to read each post's history and decide by hand, because the numbers didn't line up cleanly against the era boundaries.

That diagnosis was *almost* right. The actual cause was smaller and completely mechanical: a confusion between each post's *work* date (the actual period of time that the blog post is about) and *publish* date. Web aligned all the posts by publish date. This also revealed a duplicate post in the archive, which we cleaned up.

# What actually changed between the second failure and the fourth

The fifteen-episode scheme sat broken at zero for months before anyone noticed. This latest fix was caught, diagnosed, and repaired same-day. Basically, we checked our work.

That's the whole lesson, and it isn't really about blog categories. Any organizing scheme — a taxonomy, a filing convention, a set of labels anyone relies on to navigate something that keeps growing — has the same failure mode waiting in it. The scheme looks fine right up until the moment someone actually counts what's really in each bucket. The four tries it took to get this right are four instances of the identical mistake, at four different scales, and the only one that got caught fast was the one somebody actually verified.

# The eras, for reference

Seven periods, spanning May 2025 to today (and subject to revision again in the future, no doubt):

- **The Build** (May–Jul 2025) — Prototype to production: daily building, debugging marathons, test recovery.
- **The Methodology** (Aug–Sep 2025) — From organic to orchestrated: infrastructure sprints, methodology crystallizes.
- **The Reflection** (Oct–Nov 2025) — Alpha prep, the Great Refactor, patterns named and documented.
- **The Foundation** (Dec 2025–Jan 2026) — Strategic resets, completion discipline, minimum-viable-product planning.
- **The Sprint** (Feb–Mar 2026) — M0 ships, M1 sprint, multi-agent maturity, blog-first publishing.
- **The Mechanism** (Apr–Jul 2026) — Rules become architecture: duty-cycle autonomy, the connector rebuild, production catches up to development.
- **The Alpha** (Aug 2026–present) — Durable infrastructure lands, the hosted alpha opens to outside testers, verification culture hardens.

Nearly 390 posts, now correctly sorted into all seven, browsable by era on the site.

There is more to do. Organizing by pub date works fine for the linear building narrative, but my insight posts (like this one, now typically running on weekends) may come from an earlier era, and should really be filed by work date after all, not pub date. (I'll add that to the queue, since I literally notified Web of a few bugs this morning, including incorrect work-date metadata. It never ends...).

# One other fix: the front door itself

Since I first set up the canonical [blog section](https://pipermorgan.ai/blog/) of the Piper Morgan site, the blog's homepage was filled with marketing copy (a headline about "systematic PM excellence," a couple of buttons) that pushed the actual most recent post far enough down that a visitor had to scroll to find anything real. 

A partial fix in August trimmed the padding but never addressed what was actually in that space. So I proposed that the blog always feature the most recent post above the fold, as it does today. It still all comes down to me noticing that I want something or that something isn't working or does not meet my needs and then articulating what I really do want or need.


# If you're reading this somewhere else

If this reached you on Medium or LinkedIn, the canonical site is really worth the visit now in a way it wasn't a few weeks ago. I'm aware that plunging into this story midstream can be confusing. The blog on the site lets you jump back to any time in the process, or even to the very beginning, and as a bonus you get a real sense of how the "generic cartoon" illustration style has evolved over the past year and a half.

The eras seem to be working. The newest post is the first thing you see. Now almost 390 posts organized into the real shape of what building (and learning) process has looked like "the question that started it all" to whatever's happening in The Alpha this week.

---

*Next on Building Piper Morgan: "Who's Who at Piper Morgan" — eleven agents, one founder, and a straightforward answer to a question a friend asked a month ago: who's actually doing all this?*

*Where in your own work is a category, a label, or a filing scheme that hasn't been checked against the real data in a while — and what would it actually show if you counted?*
