---
from: comms
to: exec
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Workstream review #069, Comms. Window Nov 6 to Nov 12. User-facing: readers got 5 posts, all live and distributed, every one xian's prose checked against its sources. No product-copy change this week"
date: 2026-11-13 05:10 PT
---

# Workstream review #069: Communications

**Window:** Fri Nov 6 to Thu Nov 12, 2026.

## What a user can do now that they couldn't last week

**Nothing new in the product from this lane.** No product copy (site, beta page, letters, listing) changed this week. The newsletter confirmation email (#2256) still waits on xian's paste into Buttondown.

**Readers got five posts, all live and all distributed.** Each one is xian's prose, written in the admin UI on or the evening of its day. Comms checked each against its sources, applied fixes only on his OK, ran the 16-check template audit, and sent the publish-ready memo to Docs.

- Sat 11-07: "At Long Last, Beta" (insight)
- Sun 11-08: "When Accuracy Scores Worse" (insight)
- Tue 11-10: "Never Green in a Thousand Runs" (building)
- Wed 11-11: Weekly Ship #068, "Whose Connection Is It, Anyway?"
- Thu 11-12: "The Server Has No Key" (building)

## Shipped, found, corrected

- **Facts the review changed in xian's posts (all on his OK):**
  - Sun: "the five were actually false" became "five needed fixing". CXO's 10-22 entry held five held rows, and the sources name only two as false.
  - Tue: "four of the many, many tests" became "four of our seven test workflows". "Over a thousand runs" became "in a thousand runs", matching the source.
  - Ship #068: "50 problem places" became "flagged 50 places to check (!). Most were fine, and the list is now down to 11". Arch had ruled most of the 50 system-only. The outage cause became exceeding Vercel's free tier.
  - Thu: a quote that joined two separate decisions.log lines was split back into the reasoning and the clearing condition.
- **Title locks asked ahead of time.** Each footer teases the next post, and the audit fails on a working title. I asked xian for Tue's and Thu's final titles a day early, so neither was the last thing waiting.
- **Mining pass, Oct 23 to Nov 5** (11-06), in the planning doc: four cross-month themes and candidates A–I. xian picked candidate 8 for Sat 11-14 and titled it "Which Agent Did It?". Its scaffold is written, with every quote re-opened at source and the commit authorship measured (192 of the last 200 commits on main are authored by xian's account).
- **Ship forms for two-week sprints** (11-06): the progress and final-score forms are in `draft-weekly-ship` v1.15.
- **Publish pipeline after Web's Ignored Build Step:** closed on 11-07. "At Long Last, Beta" deployed with Production `success`.
- **Agent 360 response** to HOST (11-06). The Comms briefing's three stale lines that CIO's re-run found are fixed, and the carry-forward went from 452 to 189 lines.

**My own errors, owned:**
- **11-07:** my memo, the scaffold and the publish-ready all called "At Long Last, Beta" a building post. Weekend posts are insights. Docs fixed the category on xian's word. Every publish-ready memo now states the category, checked against the weekday.
- **11-08 and 11-10:** two estimated times ("22:1x", "23:3x") in a memo and a log. The log one was corrected to the commit's 23:27. The memo's fact stood.

## Needs PM (no new asks)
- Sat 11-14 "Which Agent Did It?": prose, image, and what its footer teases (nothing is on the calendar after Sat except Ships).
- The editorial-strategy talk, still not held (pacing, beat merges, scaffold format).
- The confirmation-email paste into Buttondown (#2256).

## Next week (11-13 to 11-19)
- Land Sat 11-14 and whatever xian slots next: review, fact-check, audit, publish-ready. Ship #069 External fact-check on the draft.
- Next mining pass is Fri 11-20. After the talk: put the scaffold format into `draft-blog-post`.

Blocked only on xian's writing and decisions.

**Verified how:**
- Publication list read from `editorial-calendar.csv` this turn: pubDate 11-06 to 11-12, 5 rows, all `distributed`, each with a blog URL.
- All 5 blog URLs return 200 by `curl -sL` this turn (HTTP layer, not a rendered-page check).
- The edits, title locks, errors and dates come from my 11-06 to 11-12 session logs. The authorship count was measured by `git log` on 11-12 at 22:15 and not re-run today.
- Denominator: this lane only.

— Comms
