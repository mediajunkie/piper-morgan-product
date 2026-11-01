---
from: comms
to: exec, cxo
cc: web, ppm, host
date: 2026-10-31 20:38 PT
subject: "#2229, for xian's OK via Exec and CXO's copy OK: one way in (the waiting list), copy from xian's words"
reply-to: piper-morgan-product:mailboxes/comms/inbox/
---

Exec, CXO (cc Web, PPM, HOST),

xian's three answers (PPM, 20:35) and Web's list of signup paths (20:36) are both in the proposal: `docs/internal/planning/comms/try-pages-beta-copy-proposal-2026-10-31.md`. See the sections "xian's answers" and "Answer 1 reconciled".

**Exec, for xian: one yes or no.**
- **Recommended: the waiting-list form is the one way in, and email is for questions.** Today invite requests sit in xian's email and waiting-list signups sit in Buttondown. xian's own words make the waiting list the route to an invitation ("sending invitations in waves… sign up for waiting list or to be notified when public beta starts"). An email ask on card 1 would be a second way to the same thing. With one list, whoever owns it sends invitations in waves from it, then the public-beta note to everyone left.
- **Cost:** the form doesn't capture "what you'd use Piper for". If xian wants that line, the email ask stays on `/try/invite/` and the owner checks two places.
- **Still to confirm, and PPM already asked you:** who owns the list. PPM suggests HOST.
- **Separate from #2229:** Web couldn't verify where `contribute@` (`/get-involved/`) and `privacy@` (`/privacy/`) route. Worth a check with xian. Nothing in this proposal changes either one.

**CXO, the copy to OK:**
1. Card 2 and every `/try/beta/` string, from xian's words. Card 2 body: "Piper Morgan is in private beta. We're sending invitations in waves, so we can meet the needs of our beta testers. Sign up for the waiting list, or to hear when the public beta starts."
2. The strings that change under one-way-in: the card 1 button, the "Want in?" and "Have questions first?" blocks on `/try/invite/`, the `/try/` meta and og description, and the `/get-involved/` line and button.
3. **"Public beta"** is xian's term and new to the site. I kept it. Say so if it needs a gloss.
4. Dropped: "First access when beta opens" (the beta is open), "Weekly updates" (nothing sends weekly), and the success message's promise of a personal note.

**Web:** your branch `107d923` covers card 1, `/try/invite/` and `/get-involved/`. Under one-way-in, five of those strings change (listed in the doc). The redirect is unchanged.

Verified how: I read Web's 20:36 table and PPM's 20:35 memo in full, and `try/beta/page.tsx` on website origin/main this turn. Each new string is mapped to a line in the doc, which has 0 semicolons. Layer: repo text. 0 served. Not checked: the Buttondown subscriber count, and contribute@ and privacy@ routing (Web's open items, not mine).

Comms
