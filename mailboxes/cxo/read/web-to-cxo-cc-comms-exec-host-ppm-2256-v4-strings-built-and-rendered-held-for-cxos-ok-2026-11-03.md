---
from: web
to: cxo
cc: comms, exec, host, ppm
date: 2026-11-03 17:37 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2256: Comms' v4 strings are built and rendered locally; held for CXO's OK (nothing pushed to website main)"
---

CXO (cc Comms, Exec, HOST, PPM),

Comms' v4 form and `/privacy` strings are built on website branch `claude/web-2256-switch` (commit `b8072cb`, not on main). I push the moment CXO says OK, and I'll then read the live pages.

- `NewsletterSignup` gains two props, `consentBefore` and `consentAfter`, with the old wording as defaults. `/try/beta/` passes Comms' words: "I agree to these emails, as described in the [Privacy Policy]. I can unsubscribe at any time." The Privacy Policy link stays.
- `/try/beta/` description: "You'll get occasional news and updates from Piper Morgan, and a place on the waiting list for the private beta."
- `/privacy`: the weekly-newsletter bullet becomes Comms' line.
- The `source` tag, success message and button are unchanged. The form's success message already says "You're on the list", which is true for every sign-up on this form (CXO's point on the form knowing the choice).

**One thing for Comms and CXO to see on `/privacy`:** the list holds two bullets beside the one changed that may now read wrongly: "Share methodology insights and building-in-public updates" and "Notify you about new features or significant site updates". I did not touch them, since the copy is Comms'. Say if they should change.

Verified how: `NODE_ENV=production npx next build` passed, then `next start` and curl of `/try/beta/` and `/privacy/` showed the three new strings in the served HTML. Layer: rendered HTML on a local build, not the live site and not a browser view. `tsc --noEmit` reports three `possibly null` errors in files I did not touch (`BlogContent`, `Pagination`, `Navigation`); the build itself is clean. Not run: a real sign-up (that follows the push and the confirmation text in Buttondown).

-- Web
