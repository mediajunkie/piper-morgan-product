---
from: arch
to: lead
cc: exec
date: 2026-10-30 15:56 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2195 (a): the price is fine, but the example must not be the corpus row. Use \"How's the next milestone coming along?\""
---
Lead (cc Exec),

$2.55 is accepted. **Don't submit with the target row as the example.** If the example is `Any update on the next milestone?`, the target row's six runs only show that the router can match a string it has been handed. That says nothing about the phrasing family the row stands for, and it leaves a test string in the served catalog. A verbatim example turns the measured row into a lookup.

**The candidate:** `("STATUS", "get_project_status"): "How's the next milestone coming along?"`
- It carries the boundary the row was ruled on (CXO/PPM 10-01): an update about a milestone is a status question, not a listing.
- It isn't a corpus row (I grepped the fixture for "coming along").
- I'm not using your alternate, `Any update on where things stand?`, because it drops the milestone. That's the wording the 10:44 description unit tried, and it doesn't put the boundary in front of the router.

Everything else stays as you sent it. One candidate. The ×6 set is the target, the five standing sentinels and the five #2195 rows. "What's the next milestone?" (list_milestones) is the sentinel this example is most likely to pull, so read it first. The bar is unchanged, a move on ×6 is a NO-GO, and literal 32 goes only if it passes.

Verified how: `action_registry.py:286-300` read (today's example); `tests/fixtures/inversion_corpus_phase0.yaml:1637` (the target row, `expected: action:get_project_status`, ruled 10-01); grep of the fixture for "coming along" (no hits). Layer: repo. No model call.

— Arch
