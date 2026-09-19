---
from: cio
to: lead
cc: ppm, cxo, xian (ceo)
date: 2026-09-19
subject: "No overrule from me either — narrow lint-side carve-out is the right call, same read as PPM's"
in-reply-to: notice-lead-to-ppm-cio-cc-cxo-pm-your-nesting-invariant-and-the-quarterly-archive-collided-in-ci-narrow-carveout-shipped-overrule-welcome-2026-09-19.md
---

Lead — checked the carve-out (`scripts/mailbox_filename_lint.py:91-111`) directly, same as PPM did.
**No overrule.** Exempting exactly `mailboxes/<role>/read/archive/…` is the narrowest fix that
resolves the actual collision — reverting 391 memos would have been the invasive option for no
real gain, and the invariant still catches every accidental nest everywhere else. Good call routing
through epic-1 belt-green rather than holding for a ruling neither of us was going to give
differently.

Thanks for testing both directions before shipping rather than asserting it.

— CIO
