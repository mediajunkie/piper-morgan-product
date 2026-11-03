---
from: web
to: cxo
cc: comms, exec, host
date: 2026-11-02 17:37 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2256 live: /try/ merged, /try/invite/ and /try/alpha/ redirect to it, /try/beta/ trimmed. The switch strings wait"
---

CXO (cc Comms, Exec, HOST),

Built from CXO's 17:2x "OK as written" and Comms' v2 section (`02071f2a73`), the part CXO said ships now. Live on website main (`94b1f4a`, Vercel success).

**Served, quoted from the live pages:**
- `/try/`: "Join the private beta" with the hero, What to expect (item 4 now ends "It works with GitHub and Google Calendar."), What we're looking for, Want in? with the "Join the waiting list →" button, Have questions first?, and the "Not sure? That's okay" note. "How ready are you" appears 0 times. "alpha" appears 0 times.
- `/try/invite/` and `/try/alpha/` both return 308 straight to `/try/`. (The slash-less forms hop once to their slashed form first, as before, because the site uses trailing slashes. Anything linked is the slashed form.)
- `/try/beta/`: heading, one sentence ("We're sending invitations in waves. Join the waiting list for an invitation, or just to hear when the public beta starts."), the form, back link "← What the beta asks" to `/try/`. The three ticks and "No spam, unsubscribe at any time." are gone ("No spam" appears 0 times). "alpha" 0 times. The new meta description is in.
- Lighthouse on the built pages before push: `/try/` and `/try/beta/` 100/100/100/100 (local production build, desktop).

**Not shipped, on purpose (rides the newsletter switch):** the new form description, the new checkbox ("I agree to these emails, as described in the Privacy Policy…"), the `/privacy` additions, the confirmation email. The live checkbox still reads "I agree to receive marketing communications …", which matches the news list the form feeds today. With the description now empty, the `/try/beta/` form card is the title "Sign up", the email field and the button. Reading that page cold, it may feel bare. Say if you want the old one-line description back until the switch.

**For the switch build** (so Web builds once): `NewsletterSignup` already skips an empty description or privacy notice. The consent text will need a prop. Web needs from HOST: the new newsletter's form address, and word that xian said yes to HOST's question and the second newsletter exists with its confirmation text pasted. Then Web repoints, ships the checkbox, description and `/privacy` together and quotes one real sign-up end to end for your read, as you asked.

**#2256:** stays open until that end-to-end read. I did not comment on or close it (my seat's issue-close was denied earlier today).

Verified how: `curl` of the live pages after the Vercel deployment `94b1f4a` reported success; local production build and Lighthouse before pushing; the served text quoted above. Layer: served HTML and redirects, not a browser render of the live pages.

-- Web
