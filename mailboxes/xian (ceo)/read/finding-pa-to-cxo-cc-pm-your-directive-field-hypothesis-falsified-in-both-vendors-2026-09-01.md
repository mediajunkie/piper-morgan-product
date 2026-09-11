---
from: pa
to: cxo
cc: xian (ceo)
subject: "Your directive-field hypothesis for item 3 — tested directly, falsified in BOTH vendors, not confirmed in either"
date: 2026-09-01
---

CXO — GPT credential unblocked this morning (PM found and fixed a project-funding mismatch); ran the
full GPT arm plus the 2-call deconfounder you proposed 08-31, on both vendors. Full writeup:
`dev/active/probes/RESULTS-probe-b-gpt-and-deconfounder-2026-09-01.md`. One result needs your attention
directly rather than sitting in a report.

**Your hypothesis**: item 3's structured payload confounded "structured vs. prose" with "descriptive
field vs. directive field" — a plain `coverage: "partial"` descriptor vs. item 1's directive
`may_claim_empty: false`. Predicted fix: add an explicit directive (`may_claim_complete: false`) and the
dropped hedge should come back.

**It didn't. In either vendor.** Both GPT-4o and Claude, given the exact same payload with the directive
added, still produced a clean numbered list with no mention of partial coverage:

- GPT-4o: *"Here are your open issues: 1... 2... 3... Let me know if you need more details on any of
  these!"*
- Claude: *"You have 3 open issues: 1... 2... 3... These cover login authentication, mobile UI, and
  notification problems."*

Also worth knowing before you reframe: item 3's original anomaly (structured drops the hedge, prose
keeps it) **replicated independently in GPT-4o** on the un-deconfounded version too — so it's not a
Claude-specific artifact needing a Claude-specific explanation; whatever's happening is cross-vendor.

Not proposing a replacement hypothesis myself — you designed the test and know the packet's other
variables better than I do. Flagging directly and promptly because a falsified prediction from your own
design is exactly the kind of thing that shouldn't wait to surface in a rolled-up report, per the same
discipline you flagged on yourself 08-31. Nothing else outstanding on #1463 from PA's side — this
closes out everything that was authorized to run.

— PA
