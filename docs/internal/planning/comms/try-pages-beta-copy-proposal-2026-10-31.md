# /try pages after the beta started: proposal for xian (#2229)

**Drafted:** Comms, 2026-10-31 15:2x PT, after Exec 13:51 ("All beta invitations sent!", so beta wording is public-facing now).
**Read from:** website origin/main, `src/app/(public)/try/page.tsx`, `try/alpha/page.tsx`, `try/beta/page.tsx`, `get-involved/page.tsx`.
**Path:** xian picks → CXO OKs the copy → Web builds it and checks the served HTML (#2229 acceptance).
**Asked by:** xian via PPM, 10-31 18:50 ("can we ask Comms to propose updates and then Web can execute once I approve?"). Sent to Exec for xian's approval, cc CXO, Web, PPM.

## xian's answers (via PPM, 10-31 20:35)

1. **Invite path:** "that may be ok for now but sync with Web on how we already have a signup and a way to show interest on the site today and how to update that." **Open.** Web is listing every signup and interest path. Comms then reconciles the invite line so a visitor has one clear path. Note the overlap this has to settle: card 1 asks for an invite by email, and the card 2 waiting list is also a way to get an invitation.
2. **`/try/alpha/`:** "Yes, move and redirect." **Decided.**
3. **Card 2 and `/try/beta/`:** keep the form, with new words: "we are in private beta. we are sending invitations in waves to ensure we meet the needs of beta testers. sign up for waiting list or to be notified when public beta starts." **Drafted below. Needs CXO's OK.** The list owner is for Exec to confirm with xian (PPM suggests HOST).

## Answer 1 reconciled: one way in (Comms, 20:37, after Web's 20:36 list)

Web's list (memo 20:36) shows two intake lists in two places today: invite requests by email (alpha@, which forwards to xian) and waiting-list signups in Buttondown (`beta-waitlist`, never sent from). xian's 20:35 words make the waiting list the way invitations go out ("we are sending invitations in waves… sign up for waiting list or to be notified when public beta starts"). So an email ask on card 1 would be a second, parallel way to the same invitation.

**Recommendation: the waiting-list form is the one way in. Email is for questions.**
- A visitor who wants in, or just wants the public-beta note, joins the same list. One list holds everyone, and whoever owns it sends invitations in waves from it, then the public-beta note to everyone left.
- `/try/invite/` stays as the page that says what the beta is like (no install, your own Anthropic key, rough edges). Its button goes to the form instead of opening an email.
- support@ stays on `/try/invite/` for "Have questions first?". That's also where someone can tell us about their work if they want to.
- The cost, which Web named: the form doesn't capture "what you'd use Piper for". If xian wants that line, the alternative is to keep the email ask on `/try/invite/` and accept two lists that the owner checks.
- Not changed by #2229: `contribute@` on `/get-involved/` and `privacy@` on `/privacy/`. Web marked both routes unverified. I'm sending that to Exec separately from this copy.

**Strings that change under this recommendation** (they replace the matching lines below):
- `/try/` card 1 button: **See what the beta is like →** (to `/try/invite/`)
- `/try/invite/` "Want in?": Join the waiting list. We're sending invitations in waves, so we can meet the needs of our beta testers, and we can't promise when yours will come. Button: **Join the waiting list →** (to `/try/beta/`)
- `/try/invite/` "Have questions first?": Email us at **support@pipermorgan.ai**. We're happy to chat, and to hear about the product work you do.
- `/try/` meta description: Choose your path to Piper Morgan. See what the private beta is like, or join the waiting list for an invitation or a note when the public beta starts. og description: See the private beta, or join the waiting list.
- `/get-involved/` line: Join the waiting list for the private beta if you're ready to dive in. Button: **Join the private beta →** (to `/try/invite/`)

## The two decisions, with Comms' recommendation (as sent 18:53, kept for the record)

1. **What a visitor does now.** Recommended: **request an invite to the private beta by email**, and keep the second card as a "keep me posted" list for when Piper opens to everyone (the 1.0 Production release).
   - **Address:** **support@pipermorgan.ai**. It is the address the Terms and the beta letter already use (alpha@ was dropped there on 10-24), and it reaches only xian's own mailboxes (Exec, decisions.log 10-31 18:33). No new alias is needed. *(Revised 18:55 after PPM's memo. The 15:20 draft said alpha@.)*
2. **What happens to `/try/alpha/`.** Recommended: **move the page to `/try/invite/` and redirect `/try/alpha/` there**, so links in the alpha letters and old posts still land somewhere true. The current `/try/beta/` page stays where it is as the signup list, reworded below.

## Draft copy (no semicolons, they/them for Piper)

### `/try/` card 1 (replaces the Alpha card)
- Eyebrow: **For early adopters**
- Heading: **I'm ready to get my hands dirty**
- Body: Piper Morgan is in private beta. It's hosted and invite-only, so there's nothing to install. It's early, with rough edges, and your feedback is read by the team.
- Bullets:
  - Invite-only, nothing to install
  - Bring your own Anthropic API key. Piper doesn't cover model costs
  - Works with GitHub and Google Calendar
  - Your feedback reaches the team building it
- Button: **Request a beta invite →** (to `/try/invite/`)

### `/try/` card 2 (replaces the Beta card), from xian's 20:35 words
- Eyebrow: **For the curious** *(unchanged)*
- Heading: **Join the waiting list**
- Body: Piper Morgan is in private beta. We're sending invitations in waves, so we can meet the needs of our beta testers. Sign up for the waiting list, or to hear when the public beta starts.
- Bullets: No setup needed · A place on the waiting list · A note when the public beta starts
- Button: **Join the waiting list →** (to `/try/beta/`)

### `/try/` page description (meta) and og description
- Description: Choose your path to Piper Morgan. Request an invite to the private beta, or join the waiting list and hear when the public beta starts.
- og description: Request a beta invite, or join the waiting list.
- *(The first half may change when the invite path is reconciled, answer 1.)*

### `/try/invite/` (the old alpha page, moved): every string, in page order
*(Rewritten 19:06 after Web's 19:03 memo listed six alpha strings the first draft didn't cover. Each line below replaces the string at that spot on `try/alpha/page.tsx`.)*
- Page title: **Join the Private Beta | Piper Morgan**. Description: Request an invite to the Piper Morgan private beta and help shape AI-assisted product management.
- og title: **Join the Piper Morgan Private Beta**. og description: unchanged ("Help shape the future of AI-assisted product management.").
- Hero headline: **Join the private beta**
- Hero subline: Piper Morgan is in private beta. We're inviting a small number of product people to use it for their real work and tell us what they find.
- "What to expect"
  1. **Invite-only, nothing to install.** Piper runs in your browser. We send you an invite code and you create your account. You connect your own Anthropic API key to use it.
     *(The alpha page's second paragraph, about the plugin in Claude, Cowork and Claude Code, is cut. The beta letter names only the hosted app and an Anthropic key, and the plugin is distributed with 1.0 (decisions.log 10-31 09:48).)*
  2. **Things will break.** We're iterating fast, and bugs are part of the process. *(unchanged apart from the semicolon)*
  3. **Your voice matters.** Your feedback reaches the team building it. *(was "Alpha feedback directly influences what we build next", a promise per CXO's edits 1 and 2)*
  4. **Real access.** You'll use Piper for your actual work, not a sandbox. *(unchanged)*
- "What we're looking for": An Anthropic API key of your own. Piper doesn't provide or pay for model usage · Willingness to report what's working and what isn't · Interest in AI-assisted product management · Patience with rough edges
- "Want in?": Email us with a line about the product work you do and what you'd use Piper for. We're sending invites a few at a time, so we can't promise one.
  - Button: **Request an invite →** to `mailto:support@pipermorgan.ai?subject=Beta%20invite%20request`
- "Have questions first?": Email us at **support@pipermorgan.ai**. We're happy to chat before you commit. *(the em dash becomes a full stop, and both alpha@ uses become support@)*
- Back link "← Back to options": unchanged.

Expected "alpha" matches on the served `/try/invite/` page after this: 0 in copy. Any match left in the HTML should be a framework or path artifact, for Web to justify.

### `/try/beta/` (the waiting-list page), every string, from xian's 20:35 words
- Page title: **Join the Waiting List | Piper Morgan**. Description: Piper Morgan is in private beta, with invitations going out in waves. Join the waiting list, or hear when the public beta starts.
- Hero headline: **Join the waiting list** *(was "Join the waitlist")*
- Hero subline: Piper Morgan is in private beta. We're sending invitations in waves, so we can meet the needs of our beta testers. *(was "isn't open to everyone yet… we'll reach out when beta opens")*
- Form title: **Sign up** *(was "Get early access")*
- Form description: Join the waiting list for an invitation, or to hear when the public beta starts.
- Benefits: A place on the waiting list · A note when the public beta starts · No setup needed *(drops "First access when beta opens", since the beta is open, and "Weekly updates on what we're building", since nothing sends weekly from this list)*
- Button: **Join the waiting list** *(was "Join Waitlist")*
- Success message: You're on the list. Check your inbox (and spam folder) for the confirmation link. *(drops "We'll reach out personally when beta opens")*
- Back link: unchanged.

### `/get-involved/`
- Meta: "…Join the private beta, contribute code, or share your expertise."
- Line: Request a beta invite if you're ready to dive in.
- Button: **Request a beta invite →** (to `/try/invite/`)

## Who keeps the card 2 list (CXO edit 4). xian chose B at 20:35, so the owner is now Exec's to confirm with xian

CXO asked who keeps the "Keep me posted" list and sends the note. **Nobody does today.** The `/try/beta/` form posts to the Buttondown list (`NewsletterSignup`, tag `beta-waitlist`, website origin/main read 19:05). Web's 09-20 audit found that list dormant: 0-1 subscribers and nothing ever sent (`dev/active/web-standing-items.md` row 3a). On 10-02 xian took the /blog form off that list for the same reason and pointed it at LinkedIn and Medium. The preference-based signup that would fix it (row 3b) is waiting on xian's review of Web's straw plan.

Two options for xian:
- **A (Comms' recommendation): follow the /blog precedent.** Card 2 becomes "Follow along": "Not ready to try it yet? Follow the build on LinkedIn or Medium. We'll post there when Piper opens to everyone." The button goes to `/blog`, and `/try/beta/` redirects there too. That takes no email it can't answer, and the posts do go out.
- **B: CXO's interim wording.** Keep the form, and say "leave your email and we may tell you when Piper opens to everyone" until someone owns the list. It is true, but it still collects addresses for a list nothing sends from.

## CXO review (19:01): OK with four edits
Edits 1 and 3 applied as written. Edit 2 applied as "Your feedback reaches the **team** building it" instead of "the people building it", because the team is xian and his agents, and agents aren't people in public prose. Edit 4 is the open item above.

**CXO, 19:10:** accepted "team", OK'd every `/try/invite/` string as written, and backs option A for card 2. The copy now waits only on xian's three calls.

## Checks before it goes to CXO
- Every claim matches the letter: hosted, invite-only, your own Anthropic key, GitHub and Google Calendar (not Slack or Notion, see #2237).
- "Bring your own LLM provider key" becomes "Anthropic API key", because the beta takes only an Anthropic key (the letter's setup step).
- Old "alpha" mentions that stay: none planned on these pages. Blog posts that say alpha are history and stay as they are.
