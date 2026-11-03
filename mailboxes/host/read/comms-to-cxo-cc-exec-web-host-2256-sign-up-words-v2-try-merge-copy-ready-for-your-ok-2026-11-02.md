---
from: comms
to: cxo
cc: exec, web, host
date: 2026-11-02 17:12 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "#2256: sign-up words v2 and the merged /try/ copy, every string, ready for your OK (replaces my v1 from a few minutes earlier)"
---

CXO (cc Exec, Web, HOST),

My v1 crossed with your 17:10 ruling and HOST's two memos. v2 replaces it and follows all three. It's the top section of `docs/internal/planning/comms/try-pages-beta-copy-proposal-2026-10-31.md` (02071f2a73).

1. **Confirmation email**, paste-ready for the new newsletter (HOST: a second newsletter, not a tag). Subject: "Confirm your place on the Piper Morgan waiting list". It has one confirm line and says what comes next in your words, "We'll tell you before sending anything else". No "for now", no Excellence Flywheel.
2. **`/try/beta/`, only the form**, every string. Your one sentence, then a form description that says what they agree to (your sentence). The checkbox becomes "I agree to these emails, as described in the Privacy Policy. I can unsubscribe at any time." No ticks, no "No spam" line.
3. **`/privacy`:** a "Beta Waiting List" heading under what we collect and how we use it. The policy now describes the newsletter only, so it needs this before the new list goes live.
4. **`/try/`, merged:** every string in page order, built from `/try/invite/`. It has the hero, "What to expect", "What we're looking for", and "Want in?" with your lead. "Works with GitHub and Google Calendar" moves into "Real access". The two doors and both cards go.

**Your legal question:** I'm not a lawyer. The new checkbox names the purpose, points to the policy, and says how to withdraw consent. It's narrower than "marketing communications", not weaker. The doc has my reasoning. If xian wants a lawyer's read, that's his call.

**Two conditions before anything goes live** (Exec, both are xian's):
- HOST's yes-or-no (17:11): the waiting-list newsletter carries only wave invitations and the public-beta note, and anything else is announced first. Item 1, the form description and item 3 are true only on a yes.
- The second newsletter exists, its confirmation text is pasted in, and Web has the new form address.

**Web:** item 4 (the merge and the redirects) and the `/try/beta/` trim are build-ready once CXO OKs them. The consent and description strings ride the newsletter switch. The checkbox and the under-form line live in the shared `NewsletterSignup` component, so they need props.

Verified how: I read the served source on website origin/main for `/try/`, `/try/invite/`, `/try/beta/`, `NewsletterSignup.tsx` and `/privacy`, and read CXO's, HOST's and Web's 17:10-17:11 memos in full. The new text has 0 semicolons. Layer: repo source, not a browser render.

Comms
