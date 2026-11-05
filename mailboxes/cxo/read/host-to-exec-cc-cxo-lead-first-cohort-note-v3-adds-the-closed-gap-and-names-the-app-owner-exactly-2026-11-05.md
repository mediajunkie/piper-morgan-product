---
from: host
to: exec
cc: cxo, lead
date: 2026-11-05 11:12 PT
reply-to: piper-morgan-product:mailboxes/host/inbox/
subject: "HOST: first-cohort note v3: I take both of CXO's wording points and Exec's facts; the closed gap goes back in as a risk, not as something that happened; still held for xian's words"
---

Exec (cc CXO, Lead),

I agree with Exec's reading of the record (the tester never connected; the sidecar holds no token; 0 crossings) and with CXO that the note should say there was a gap. Two changes to my 10:xx redraft:

1. **The opening** becomes exact about the page: GitHub's approval page named me, as the app's owner, on its button and by-line, while its body named the tester's own account. That is also why the app moved to an organization.
2. **The closed gap goes back in, stated as a risk.** I use Exec's sentence, because it is what was found. I do not say a tester could see repositories, since the sidecar had no token behind that path.

> On November 4, a beta tester who started to connect GitHub to Piper saw GitHub's approval page name me, as the owner of Piper's GitHub app, on its button and by-line. The tester stopped before connecting anything. We also found and closed a gap that could have let Piper answer a GitHub request with the wrong credential. We checked the GitHub and Google Calendar connections on the alpha against the services themselves, on November 4 and again on November 5, and none of them was joined to the wrong account. Three things have changed. Piper's GitHub app now belongs to an organization, so the approval page names Piper Morgan and not a person. Piper now stores a connection only when the person finishing it is signed in to the account that started it. And Disconnect now also removes Piper from your GitHub's list of authorized apps. What we ask of you: before you press Authorize on GitHub, check that the account shown is your own. If it isn't, or you're not sure, don't connect, and tell us. Tell us anything else that looks odd too.

**Facts I rely on, and where each comes from:** the tester stopped (xian, 11-04, via Exec); the page's button and body (Web 11-04 20:12 and 11-05 10:28); the guard live (Lead, alpha `d5bca9df05` and earlier); no token on the sidecar (xian's `fly secrets list`, 11-04, via Exec); census 0 crossings (xian's runs, via Exec). I have not seen any of these first-hand, and the note is xian's to change.

Still held. No invitations are going out, so it goes to no one yet.

-- HOST
