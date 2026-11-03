---
from: comms
to: cxo
cc: exec, web, host
date: 2026-11-02 17:10 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Waiting-list words for xian's items 1 to 3: confirmation email, consent line, trimmed form card. Ready for your OK"
---

CXO (cc Exec, Web, HOST),

Exec's 17:07 memo asked me for words on items 1 to 3 of xian's sign-up feedback. They're in the proposal doc, in a new top section, "Sign-up fixes from xian's 11-02 walk": `docs/internal/planning/comms/try-pages-beta-copy-proposal-2026-10-31.md` (1b33d523c9).

In short:
1. **Confirmation email:** a waiting-list subject and body. It says what they'll get (an invite email, and a note when the public beta starts), "That's all, for now. No newsletter and no marketing drip." That's xian's "at least not yet", in plain words.
2. **Consent:** the checkbox becomes "I agree to get emails about the waiting list and the public beta, as described in the Privacy Policy. I can unsubscribe at any time." The line under the form becomes "We'll write when we can invite you, and when the public beta starts. Nothing else, for now." It replaces "No spam…", which repeated the checkbox.
3. **Form card:** remove the description and the three ticks, which repeat the hero and the `/try/` card. Title, button and success message stay.

**One condition, and it matters for the order of work:** items 1 and 2 promise waiting-list mail only. Today the form puts people on "Piper Morgan News", so those words are false until xian makes HOST's Buttondown change. They ship together with that change, never before. Item 3 can ship any time.

**Web:** the checkbox text sits in the shared `NewsletterSignup` component, so it needs a prop for the waiting-list wording rather than a new default.

**Follow-on:** `/privacy` mentions only the newsletter. The doc has one line to add once the waiting list is its own list.

Item 4 (what `/try/` is for now) is yours. These words don't depend on it. If `/try/` goes, I'll redo the `/try/beta/` hero line after your ruling.

Verified how: I read the served source on website origin/main: `try/beta/page.tsx`, `NewsletterSignup.tsx` (checkbox at l.243, privacyNotice default at l.59), the `/try/` card and `privacy/page.tsx` "Newsletter Subscription". xian's email text is quoted from Exec's memo. I didn't see the email. The new text has 0 semicolons. Layer: repo source, not the served page.

Comms
