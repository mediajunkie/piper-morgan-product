---
from: comms
to: xian (ceo)
cc: exec
subject: "Weekly Ship #062 draft ready — product-delta frame, awaiting your voice pass + art"
date: 2026-09-25
---

PM —

Ship #062 first draft is ready: `docs/public/comms/drafts/weekly-ship-062-draft-2026-09-25.md`
(also on the calendar, status `drafted`, workDate/endWorkDate set to the Sep 18-24 window).

**Structured on the new frame, per Exec's memo and your own synthesis line** — the "Shipped this
week" section leads with what a user or alpha tester can do today that they couldn't on Sep 18
(signup completing, offers that either work or say so honestly, chat surviving a key being added
mid-conversation, honest source-unavailable messages, timezone-correct dates, the persona file
finally loading, phrasing fixes, an injection fix), with everything else — hosting migration,
the credential-leak incident and its lesson, the two research threads that closed, the epic-risk
finding — below the line. Milestones still lead in the metrics section; the delta list is how I
tried to make that progress legible the way you described.

**One methodology note, since it affects how much I can vouch for the below-the-line material**:
Exec's synthesis artifact (the claude.ai link in their GO memo) wasn't shared with this seat, so I
read all 10 workstream reviews directly rather than working from the synthesis — slower, but it
meant catching one thing I could verify myself: Arch's review explicitly flagged that a real fix
(the honest-degrade landing) crossed into Friday morning, just outside the Thu 09-24 cutoff, so
I've held it for next week rather than claim it early, matching the window discipline from last
cycle. I also caught and fixed a factual slip of my own mid-draft — I'd written the overnight
gate-visibility incident as "35 pushes from seven different people," which is wrong on two counts
(it's roles/seats, not people, and I'd misremembered the count from a different draft pass) —
fixed to match Lead's and HOST's own reviews before this went out.

**What I didn't include**: Web's own website-deployment-size fix (240 MB removed, ~74% smaller
deploys) — real and Web-authored, but not user-facing and the draft was already running long; happy
to fold it in if you want it. Also didn't attempt a "vs. a week ago" milestone comparison — the
numbers I could find for Sep 18 didn't reconcile cleanly enough to state with confidence, so I left
this week's numbers standing on their own rather than guess at a comparison.

Word count: currently ~1,780 (last week's published Ship was ~1,400) — this was a genuinely denser
week (credential incident, hosting migration, signup blocker, two research threads closing, a real
structural risk PPM named) rather than padding; flagging the length rather than silently cutting
material you might want to keep, since you're doing the tightening pass anyway.

Ready for your voice pass whenever you get to it. Target publish: Wednesday 09-30.

— Comms
