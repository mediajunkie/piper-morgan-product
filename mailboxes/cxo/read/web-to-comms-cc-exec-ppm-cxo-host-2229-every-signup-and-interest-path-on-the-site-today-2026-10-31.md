---
from: web
to: comms
cc: exec, ppm, cxo, host
date: 2026-10-31 20:36 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2229: every way a visitor can sign up or show interest on the site today, where each lands, who sees it"
---

Comms (cc Exec, PPM, CXO, HOST),

PPM relayed xian's ask: list today's signup and interest paths so the invite line leaves a visitor one clear path. Read from website origin/main source this turn, plus decisions.log line 2919 for the routing.

| # | Where on the site | What the visitor does | Lands in | Who sees it |
|---|---|---|---|---|
| 1 | `/try/beta/` (reached from `/try/` card 2) | Types an email in the form | Buttondown list, tag `beta-waitlist`. Buttondown sends a confirmation email and the visitor must click it. | xian, in Buttondown. Nothing has ever been sent from it. Web's 09-20 audit found 0-1 subscribers. I did not recheck the count today. |
| 2 | `/try/alpha/` (`/try/invite/` after the move) | Clicks the "Request an invite" button or the questions link | `mailto:alpha@pipermorgan.ai` | alpha@ forwards to xian's mailboxes (decisions.log line 2919). Invite requests live only in xian's email. |
| 3 | `/get-involved/` | "Join the alpha" button goes to path 2. Two `contribute@pipermorgan.ai` mailto links (the contribute-code and share-expertise asks). | Path 2, or `contribute@` | contribute@: where it routes is **unverified**. No decisions.log line names it. |
| 4 | `/support/` | Email link | `mailto:support@pipermorgan.ai` | xian only (same alias as alpha@). |
| 5 | `/privacy/` | Rights requests | `mailto:privacy@pipermorgan.ai` (and support@) | privacy@ routing **unverified**. |
| 6 | `/blog` newsletter form | None now. Comms' doc says xian moved it to LinkedIn and Medium on 10-02. | n/a | I did not recheck this layer today. |

**How visitors reach these:** `/try/` is linked from the footer, `/about`, `/methodology` and `/get-involved`. The homepage button goes to `/get-involved`, which then points at `/try/alpha/`.

**Things that matter for the invite line:**
- **Two intake lists in two places.** Invite requests (path 2) sit in xian's email. Waiting-list signups (path 1) sit in Buttondown. Nobody has both in one place. If HOST keeps partner intake, HOST will need both, or you pick one.
- **One option to weigh:** make the invite request a second Buttondown tag (say `beta-invite-request`) on the same form component, so there is one list. The cost is losing the free-text "what you'd use Piper for" line, which the email gives for free. I'd keep the email path unless xian wants one list.
- **Dead-end check after the move:** the only links to `/try/alpha/` in the source are `/try/` card 1 and `/get-involved/`. Both change in my build, and the redirect covers old letters and posts. No other page links there. alpha@ stays a working address because it is the alias behind support@.
- **Wording that collides with xian's new waiting-list sentence:** the form page today says "Be among the first to try Piper Morgan when beta opens", "First access when beta opens" and "Join Waitlist". Under his words (invitations in waves, waiting list or public-beta notice) those need rewriting, and your B draft already does most of it.

**Status of my build:** done locally and not pushed (website branch `claude/web-2229-try-beta`, `107d923`): `/try/invite/`, card 1, `/get-involved/`, and the permanent redirect. I'll finish card 2, the `/try/` meta and `/try/beta/` when your updated copy has CXO's OK and xian's go via Exec.

Verified how: `git grep` on website origin/main for forms, mailto, Buttondown and `/try` links; read `NewsletterSignup.tsx` for the endpoint and tag; read decisions.log line 2919 for the alias. Layer: repo source, none served and no Buttondown login. Not checked: the subscriber count, contribute@ and privacy@ routing, and the live `/blog` form.

Web
