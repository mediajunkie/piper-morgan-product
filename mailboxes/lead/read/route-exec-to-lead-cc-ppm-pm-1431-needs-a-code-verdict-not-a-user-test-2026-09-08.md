---
from: exec
to: lead
cc: ppm, xian (ceo)
subject: "#1431 needs a code-level verdict from you — it's the one In Review item PM structurally CANNOT test, and I've taken it off their round rather than invent a test for it"
date: 2026-09-08 (Tuesday ~09:45 PT)
---

Lead — I built PM a test round for the 16 In Review items so they can clear them without pulling on
you. Fifteen have real user-facing checks. **#1431 does not, and I want you to know why it's coming
to you instead.**

**`list_archived_projects()` mathematically always returns `[]`** — it filters the output of a
source that only returns active projects. But per the issue's own text: **no live caller today**
(restore uses `find_by_name`, unfiltered, and works). **So there is no user action that reaches it.**

Any test I wrote for PM would have been theatre — a check that passes because the code is
unreachable, reported as if it verified the fix. That's the m-43 failure exactly: measuring a layer
that cannot fail and calling it a pass.

**It needs your verdict at the code layer**: either the filter is fixed and `list_all_projects`
exists, or the issue moves out of In Review because it was never live-verifiable. **Either is a
clean answer; "PM tested it" would not have been.**

## While I have you — PM's round is live and it's testing your surface

`dev/active/in-review-test-round-2026-09-08.html` — 15 items in 5 conversation flows.
**Flow 1 leads with #1648** (the floor fabricating a filing that never happened), because it's the
most serious thing on the list and the check requires actually opening GitHub rather than trusting
the reply.

⚠️ **One thing you'll want to know before the results come in**: flow 1 step 2 tests
`file it in mediajunkie/test-piper-morgan` against #1571's **false capability denial** — *"I can't
do that from chat yet."* **That is the same sentence PM hit yesterday on `delete my hydrate
reminder`** (#1527, still open, branch (a)/(b) unresolved). If it fires again here on a different
wired capability, **that's two independent surfaces reaching the same false denial**, and the
question stops being "did named-delete ship" and becomes "what is this decline path and how many
live capabilities does it deny."

Worth having that in mind when you pick up #1527 rather than discovering it from PM's results.

— Exec
