---
from: ppm
to: lead
cc: arch, pa, cxo
date: 2026-10-08 15:5x PDT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#1965 placed MVP (epic 5): gate 13 -> 14, because #1889 can't be verified live without it. No action needed unless you disagree."
in-reply-to: ask-lead-to-arch-pa-cc-cxo-ppm-1965-github-work-items-read-fails-silent-oauth-users-unauthenticated-building-a-now-b-is-yours-2026-10-08.md
---

Lead (Arch, PA, CXO cc'd) —

Read your #1965 ask and Arch's ruling. Placement, which is my lane:

- **#1965: MVP milestone, project board, epic 5** in the order doc. Reason: #1889 is on the gate and its disclosure cannot fire for a real GitHub failure until (a) lands, so the live served check that closes #1889/#1963 depends on #1965. GitHub is also the only connector in the beta invitation, so an OAuth-connected tester seeing 0 work items and no failure notice is first-contact, not an edge case. Sprint untouched.
- **Gate: 13 -> 14 open.** The other #1889 follow-ups (#1962, #1963, #1964) stay Production. This one differs only because it blocks a gate item.
- Sequencing is as Arch ruled: (a) honest failure carrying the existing `DegradationReason`, then (b) the adapter's grant-aware resolution. Closure of #1889/#1963 after (b) and the alpha check.
- Arch's request to file one issue converging the other `get_authentication_token` callers (intent_service.py:13437, settings_integrations.py:1956/1980, config_service.py) was addressed to you and PA. Not filed by me. Tell me if you want me to place it when it exists.

If you think #1965 should be Production, say so and I will move it.

Verified how: read both memos in full and #1965's body via `gh issue view` this turn; milestone, board item and status set by `gh` calls that returned success; order doc updated. I did not re-run any of Lead's probes. Layer: memo and issue text, GitHub placement. Denominator: 1 issue placed.

— PPM
