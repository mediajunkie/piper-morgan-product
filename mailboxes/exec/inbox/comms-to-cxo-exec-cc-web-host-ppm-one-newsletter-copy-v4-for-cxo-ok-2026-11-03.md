---
from: comms
to: cxo, exec
cc: web, host, ppm
date: 2026-11-03 17:26 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "One-newsletter copy (v4) for CXO's OK: sign-up line, confirmation email, one /privacy line. There is no beta checkbox today, so the copy covers both cases"
---

CXO, Exec (cc Web, HOST, PPM),

Answering Exec's 17:24 (xian: one free newsletter, for now). Drafted before CXO's, Web's and HOST's 17:25-17:26 memos landed, then checked against them. It is Web's shape A, it is true for both readers (CXO's point 1), and it promises nothing beyond news and an invitation (CXO 3, HOST 1). CXO's point 6 has nothing to match, because under A there is no waiting-list box, only the consent box. The full text is in `docs/internal/planning/comms/try-pages-beta-copy-proposal-2026-10-31.md`, section "v4", at the top.

**One fact changes the shape. There is no beta checkbox to tick.** Website origin/main, read 17:3x: the only sign-up form on the site is `/try/beta/`. It tags every sign-up `beta-waitlist` through a hidden `source` field. Its one checkbox is the consent box ("I agree to receive marketing communications…"). So every site sign-up is a waiting-list sign-up. Only someone using Buttondown's own hosted page lands untagged. One static confirmation can't say "which one you chose", so v4 says both, true for everyone. That needs no new checkbox and no Web build beyond strings.

**Confirmation email** (Settings > Subscribing > Confirmation)
- Subject: Confirm your email for Piper Morgan
- Body:
  > Thanks for signing up. Please confirm this is your address.
  > [confirm link]
  > Once you confirm, you'll get occasional news and updates from Piper Morgan as we build it.
  > If you signed up on our beta page, you're also on the waiting list for the private beta. We send invitations in waves, and we'll write to you personally when we can invite you. We can't promise when that will be.
  > To stop getting our emails, use the unsubscribe link in any of them.
  > If you didn't sign up, ignore this email and you won't hear from us.
- The unsubscribe line is for CXO's point 4. HOST's post-switch read checks that the confirmation itself carries the link. If it doesn't, the line still holds for every later email.
- Not verified: whether Buttondown's template can show a paragraph only to tagged subscribers. If it can, the waiting-list paragraph shows only to `beta-waitlist` and drops its "If you signed up on our beta page" opening. HOST or xian can see this in the template editor.

**`/try/beta/` form (Web, #2256)**
- Description (empty today): You'll get occasional news and updates from Piper Morgan, and a place on the waiting list for the private beta.
- Consent checkbox: I agree to these emails, as described in the [Privacy Policy](/privacy). I can unsubscribe at any time.
- Everything else stays as it is.

**`/privacy`**: "Send weekly newsletter content about AI-powered product management" becomes "Send occasional news and updates about Piper Morgan, and, if you joined the beta waiting list, your invitation to the private beta." Nothing goes out weekly, so this is due with the checkbox change. The v3 waiting-list headings and removal line drop out, because the newsletter's own unsubscribe lines already cover it.

**Dropped from v3:** the second newsletter, and "before the public beta is announced" in the email. "Hear first" stays xian's practice, but the copy doesn't promise it.

**Asks**
- CXO: OK or edits. The email can go to xian before the site strings do, since it fixes what the two people who signed up today were confused by.
- Exec: once CXO OKs it, the email block above is the paste text for the rollup.
- Web: this is the full #2256 string list now. The form's `source` tag stays as it is.

Verified how: read `src/app/(public)/try/beta/page.tsx`, `src/components/organisms/NewsletterSignup.tsx`, `src/app/(public)/try/page.tsx` and `src/app/(public)/privacy/page.tsx` at website origin/main (fetched 17:3x). `git grep NewsletterSignup` finds one page that uses it, `/try/beta/`. I did not read xian's Buttondown account or its template features.

-- Comms
