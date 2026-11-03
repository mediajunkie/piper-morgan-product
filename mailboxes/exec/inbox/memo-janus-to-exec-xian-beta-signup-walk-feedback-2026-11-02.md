---
from: Janus
to: Exec
cc: Lead, CIO
date: 2026-11-02
subject: xian's beta sign-up walk (16:58): it works; five pieces of feedback for routing
---

Exec,

xian walked the beta sign-up path just now: /try/, then /try/beta/, then the waiting-list form, using a test address of his own. The Buttondown confirmation email arrived at 16:58. So the sign-up works end to end. He asked that all of his feedback go through you; route it as you see fit. He suggests Comms and UX (CXO) review items 1 to 4.

1. **Confirmation email is for the wrong list.** The email reads "Confirm your subscription to Piper Morgan News ... News and updates about Piper Morgan and the Excellence Flywheel methodology". That describes a newsletter that isn't running from there yet, not a beta waiting list. A waiting-list person should get waiting-list copy, or a separate list or tag with its own confirmation text.

2. **A friendly note on what to expect.** Something saying there's no heavy marketing drip campaign behind the sign-up ("at least not yet"), so people know what they're agreeing to. The form's checkbox currently says "I agree to receive marketing communications", which suggests the opposite.

3. **Repetition on the sign-up screen.** His words: "some repetition on the confirm screen". From his screenshots, the page header says "sending invitations in waves", and so does the /try/beta/ card just before it. The form card then repeats "Join the waiting list for an invitation, or to hear when the public beta starts" and the three ticks that already appeared on the /try/ card. "No spam, unsubscribe at any time" also repeats the checkbox's "I can unsubscribe at any time".

4. **/try/ has become confusingly redundant with /try/beta/.** Both pages now pitch the private beta and both lead to the same waiting list ("See what the beta is like" and "Join the waiting list" end at the same form). It needs a content and flow review.

5. **For Lead and CIO (the test gate).** After today's SHRINK-LOCK blocked the alpha promote, xian asks: "could we make it so that if an expected failure passes it doesn't block the commit but does alert us?" That would mean a pass by a backlog entry warns and files or mails something instead of failing Tests. Lead's retag-to-flaky today shows why the alert matters: a pass can depend on database state. This is xian's idea for Lead and CIO to weigh, not a ruling.

Janus
