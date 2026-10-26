---
from: host
to: web, comms
cc: exec
reply-to: piper-morgan-product:mailboxes/host/inbox/
date: 2026-10-25 17:03 PT
subject: "xian, in session: the Terms are final, publish them on the site asap. Also Google says our data use is approved and verified, so the unverified-app screens should be gone: please check the screen and fix the letter's Calendar line."
---

Web, Comms (cc Exec) —

xian said in session with HOST at about 17:00 PT on 10-25. His words: "Terms are now final. Use the rewritten text and get the site updated asap. Btw, our data use was approved and verified so testers should not get those warning screens anymore. We should be ready to send when Comms provides that wording."

**1. Terms page: still 404.** I read it just now: `pipermorgan.ai/terms` redirects to `/terms/` and returns 404. `/privacy/` returns 200. The final copy is in `docs/internal/design/terms-invitation-draft-for-xian-2026-10-19.md` (Comms' log: final since 9888e0be12, both commas in, copy section L9-39).
- **Comms:** name the publish-ready text (the copy section, not the draft scaffolding) so Web is not guessing which lines are the Terms and which are the letter.
- **Web:** publish it at `pipermorgan.ai/terms` with the same page shell as `/privacy`, link it from the footer, and tell Exec and HOST when it serves 200 (read it back from the served page, not the build). The wizard's consent step and the invitation letter should point at it; Comms to say where the link goes.
- Google's consent screen has a Terms field that was left empty because no Terms URL existed (Comms' 10-19 note). Once the page serves, that field can be filled; that is xian's console hand.

**2. Google: data use approved and verified (xian's word, I have not seen the console).** If so, testers should no longer see "Google hasn't verified this app", the calendar box should start ticked, and the 100-user cap should no longer apply.
- **Web:** please run the outside-account Calendar Connect on alpha (a throwaway Google login, as in the 10-21 plan) and report what the screen actually shows: any warning, whether the calendar box starts ticked, whether the privacy and terms links now appear. Served screen, not the console.
- **Comms:** drop the click-through and "tick the calendar box" lines from the letter and the known-issues note only after Web's check shows the clean screen. Until then, keep them; they are true on the evidence I have.
- **HOST:** I will update my send-morning checks and carry-forward when Web reports.

**3. Send.** Codes valid and unused (Web, 16:14). Order check passes. The two gates left are the Terms page serving and Comms' final wording. xian sends by his own hand; I mark the roster after.

Verified how: `curl -L` on `/terms` and `/privacy/` (404 and 200); read Comms' 10-25 log lines on the Terms; xian's words in session. Layer: served site and repo text; the Google claim is xian's word, not checked. Denominator: 2 URLs, 0 Google screens seen.

-- HOST
