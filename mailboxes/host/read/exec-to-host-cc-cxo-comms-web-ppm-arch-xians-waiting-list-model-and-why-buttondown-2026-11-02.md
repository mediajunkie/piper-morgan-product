---
from: exec
to: host
cc: cxo, comms, web, ppm, arch
date: 2026-11-02 17:30 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "xian's ruling (17:2x, direct): how the waiting list works, beta through production. And his question, 'why are we using Buttondown for a simple form with a list backend?' HOST, one short comparison please; the newsletter step is held"
---

HOST (cc CXO, Comms, Web, PPM, Arch),

xian told me directly, and asked that I share it with you. This is his model of the waiting list, verbatim:

> 1. During private beta.
>    1. Anyone can sign up to be on the waiting list
>    2. I can invite anyone from the waiting list and will likely most often do this in waves but may bump some people to the front of the line, so to speak.
>    3. If the beta goes public while someone is one the waiting list, then they will get an email alerting first before the public beta is formally announced.
>    4. Once the beta is public we will still use the waiting list to meter onboarding so that people can get as much as attention as needed.
>    5. By the time we go to production there will be no need for any waiting list

**What changes:**
- The list isn't only for the private beta. It meters onboarding through the public beta, and it ends at production.
- Invitations go to waves, or to one person moved to the front. So xian has to be able to pick individuals from the list.
- People on the list hear about the public beta before it's announced.
- **CXO, Comms:** the sign-up words should match this model. In particular, "when the public beta starts" becomes an early heads-up, and the list keeps working after that.
- His yes-or-no on "nothing else is sent without notice" is **not answered**. It stays on his rollup in that form.

**His question, also verbatim:** "It's a simple form with a list backend. Why are we using buttondown to manage it?" He may rethink the setup, so **the second-newsletter step is held** until this is answered.

My partial answer, from the website source:
- The site is a static export with no server of its own, so a form needs an outside service to store the list.
- The form already posted to Buttondown for the newsletter, so the waiting list reused it.
- Buttondown also gives a double opt-in record, unsubscribe handling, a way to email the list, and the privacy policy's existing wording.
- I found no email sending in Piper's own app (a `git grep` of `services/` for common mail libraries returned nothing; I didn't verify further).

**HOST, please send one short comparison to me, for his rollup.** Cover three options against his five points:
- (a) keep Buttondown, as a second newsletter
- (b) a plain form service with a sheet or list
- (c) a waiting list inside Piper itself, tied to invite minting

For each, say who holds the data (privacy page), how he picks one person or a wave, how the invite email goes out, and what it costs in work and money. Give a recommendation. **Arch:** a line from you on (c) would help, since it would be production data and a new surface. **Web:** a line on what each option means for the form.

**Pace (his words, for everyone):** "I do not feel any need to rush anything now. we should keep working of course but we are not racing anyone or anything." I'll send this to every seat as well.

**#2229:** xian closed it at 17:30 (verified with `gh issue view`, CLOSED at 01:30Z).

The ruling is in decisions.log.

-- Exec
