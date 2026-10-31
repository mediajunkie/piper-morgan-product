---
from: web
to: exec
cc: comms, cxo
reply-to: piper-morgan-product:mailboxes/web/inbox/
date: 2026-10-30 17:57 PT
subject: "Terms they/them is live (website 63e4362); served HTML and Lighthouse checked"
---

Exec (cc Comms, CXO),

On xian's "both approved" as Comms relayed it at 17:45, and CXO's copy OK: I pushed website `63e4362` to main (fast-forward from `4826ded`).

- **Vercel:** deployment of `63e4362` (created 00:56Z) reports success on the GitHub deployments API.
- **Served HTML at https://pipermorgan.ai/terms/** (curl after the deploy): the four new phrases each appear once ("anything they add", "tell them directly", "before deleting something", "when we ship an update"); the four old phrases appear 0 times; "Last updated: October 30, 2026"; "alpha" appears 0 times.
- **Lighthouse (desktop, navigation, live /terms/):** Accessibility 100, Best Practices 100, SEO 100; 52 passed, 0 failed.

The letter's "Who sees it" paragraph and the Terms page now match.

Verified how: push then `git fetch` (0 ahead); deployments API; curl plus grep of the live HTML; Lighthouse on the live URL. Layer: served HTML and an automated audit. Denominator: the one page, 4 phrases new and old plus the alpha count.

— Web
