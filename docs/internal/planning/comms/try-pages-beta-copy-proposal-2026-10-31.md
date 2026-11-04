# /try pages after the beta started: proposal for xian (#2229)

**Drafted:** Comms, 2026-10-31 15:2x PT, after Exec 13:51 ("All beta invitations sent!", so beta wording is public-facing now).
**Read from:** website origin/main, `src/app/(public)/try/page.tsx`, `try/alpha/page.tsx`, `try/beta/page.tsx`, `get-involved/page.tsx`.
**Path:** xian picks → CXO OKs the copy → Web builds it and checks the served HTML (#2229 acceptance).

> **Web: build from the "Build copy" section only.** Everything below it is history. **Status 20:50:** CXO OK'd the build copy (20:49) **on one hard condition:** it goes live only after Exec names the waiting-list owner and that owner confirms they will send invitations in waves and the public-beta note. If xian wants it live sooner, use CXO's fallback on card 2, `/try/beta/` and the "Want in?" block: "Join the waiting list. We may invite you, and we'll tell you if we can." **CXO 20:56: the whole Build copy section is OK as written**, including the `/try/invite/` meta line. **xian, 21:14 via PPM: yes to one way in, and HOST keeps the waiting list.** Web builds once HOST confirms they'll send invitations in waves and the public-beta note. **HOST, 21:17:** accepts keeping the list, with two limits: (1) xian sends the invitations and the note, and HOST prepares them, so whether that meets CXO's condition is CXO's and Exec's call. (2) HOST can't read Buttondown yet and needs xian to paste the signups or grant access. The copy is true as long as xian sends. **PPM, 21:19:** xian sends each wave himself and will grant HOST read access to the list. PPM reads CXO's condition as met. **CXO, 21:27: condition met. Web may build.** **Live 21:40** (Web): 4 of 4 pages, 0 alpha, `/try/alpha/` 308 to `/try/invite/`. **CXO 21:48: served text PASSES.** Still open: the hero line above, and whether Buttondown actually sends the confirmation email (HOST or xian to check) before #2229 closes.
**Asked by:** xian via PPM, 10-31 18:50 ("can we ask Comms to propose updates and then Web can execute once I approve?"). Sent to Exec for xian's approval, cc CXO, Web, PPM.

## v4: one free newsletter for news plus the waiting list (xian 11-03 17:24 via Exec). Replaces the second-newsletter plan in v2 and v3

xian, verbatim: "For now, yes let's use one free newsletter. I will review the experience and revisit again in a bit." A second Buttondown newsletter costs +$29/month (Exec checked the pricing page), so the waiting list stays a tag (`beta-waitlist`) on the one newsletter. **Status: CXO OK'd v4 at 17:36 with one edit, the invitation sentence (applied below). Live on the site 17:48 (Web), and CXO PASSed the served strings at 17:57. #2256 closes on one real sign-up read end to end, after xian pastes the email.**

**What the site does today (website origin/main, read 11-03 17:3x).** There is no beta checkbox. The only sign-up form on the site is `/try/beta/`. It posts to the one newsletter with the hidden tag `source="beta-waitlist"`, so everyone who signs up on the site is on the waiting list. Its only checkbox is the consent box: "I agree to receive marketing communications…". That means the confirmation can't say "which one you chose" from a box. Someone can only land on the newsletter without the tag by using Buttondown's own hosted sign-up page.

**So the copy says both things, true for everyone:** everyone gets the news, and site sign-ups are also on the waiting list. No new checkbox, and no Web build beyond the strings.

### 1. Confirmation email (paste-ready, Settings > Subscribing > Confirmation)

- **Subject:** Confirm your email for Piper Morgan
- **Body** (keep Buttondown's own confirm link or button where its template puts it):

> Thanks for signing up. Please confirm this is your address.
>
> [confirm link]
>
> Once you confirm, you'll get occasional news and updates from Piper Morgan as we build it.
>
> If you signed up on our beta page, you're also on the waiting list for the private beta. We send invitations in waves and write to people personally. We can't say when yours will come.
>
> To stop getting our emails, use the unsubscribe link in any of them.
>
> If you didn't sign up, ignore this email and you won't hear from us.

**If Buttondown can show a paragraph only to tagged subscribers** (not verified: HOST or xian to check in the template editor), the fourth paragraph shows only to `beta-waitlist` and loses its "If you signed up on our beta page" opening: "You're also on the waiting list for the private beta. We send invitations in waves and write to people personally…". Everything else stays as it is.

### 2. `/try/beta/` form (Web, #2256)

- **Form description** (now empty): You'll get occasional news and updates from Piper Morgan, and a place on the waiting list for the private beta.
- **Consent checkbox** (shared component, needs a prop, not a new default): I agree to these emails, as described in the [Privacy Policy](/privacy). I can unsubscribe at any time.
- **Success message** (CXO 18:07, Web live 57bf516): Almost there. Check your email (and your spam folder) and confirm your address to join the list. *(was "You're on the list…", which came before the person had confirmed)*
- **Unchanged:** heading, the hero sentence ("…or just to hear when the public beta starts" is still true, since the news carries it), button, back link.

### 3. `/privacy` (needed with the checkbox change, since "weekly" isn't true)

- **"How We Use", Newsletter Communications:** "Send weekly newsletter content about AI-powered product management" becomes "Send occasional news and updates about Piper Morgan, and, if you joined the beta waiting list, your invitation to the private beta."
- **"Last updated"** becomes the month it ships.
- **The v3 "Beta Waiting List" headings and the separate removal line are dropped.** The existing newsletter unsubscribe lines already cover leaving the list.

### What v4 drops from v2 and v3

The "second newsletter" order of steps, the waiting-list-only subject line, and the "before the public beta is announced" promise in the email. xian's "hear first" model still holds. It isn't written into the email, so it stays a promise xian keeps, not one the copy makes.

## v3 amendment: the words for xian's waiting-list model (CXO 17:41, Comms agrees). Changed strings only. Everything else in v2 below stands

xian's model (Exec 17:30, verbatim in #2164): people on the list hear first, before the public beta is announced, and the list keeps metering onboarding after that. **Nothing live changes now.** Today's "hear when the public beta starts" is true, just weaker. Comms' first v3 draft (055c2cbf90) changed four live strings and dropped the "or just to hear" reason. CXO's 17:41 crossed with it, and CXO's reading is the one that stands. That reason is the second door, kept on purpose. The list's lifetime (beyond the public beta, until production) isn't promised anywhere, since there's no page for it yet.

**Live, restore only (CXO 17:41, Web):** `/try/` "Want in?" back to the OK'd v2 string: "Join the waiting list for an invitation, or just to hear when the public beta starts. We're sending invitations in waves, and we can't promise when yours will come."

**Rides the switch (CXO's three edits):**

| Where | At the switch |
|---|---|
| `/try/beta/` sentence, and `/try/` "Want in?" | "…or just to hear first when the public beta opens." |
| Confirmation email, the "Next" line | Next, we'll email you when we can invite you to the private beta, and before the public beta is announced. We'll tell you before sending anything else. |
| Form description | unchanged from v2 |
| `/privacy`, "How We Use", Beta Waiting List | We use your email address only to send the confirmation email, to invite you to the private beta, and to tell you about the public beta before it's announced. We'll tell you before sending anything else. (Comms, to match the email) |
| `/privacy`, removal (HOST's second-store point, CXO's requirement) | To leave the waiting list, use the unsubscribe link in any email from it. |

- **CXO OK'd this v3 amendment as written (17:51).** One check at the end-to-end read (HOST): does Buttondown's confirmation email carry an unsubscribe link? If it doesn't, the removal line becomes "To leave the waiting list, use the unsubscribe link in the emails we send you after you confirm." Nothing else changes.
- **The removal line is true only under option (a).** Buttondown handles unsubscribe. Under (b), a form and a sheet, I'll rewrite it as removal on request, which waits on privacy@ routing (that's on xian's open list).
- **Still held** until xian answers HOST's yes-or-no: the form description, the confirmation email and the `/privacy` lines. "Hear first" is xian's own point 3 and stays true while he does the sending.

## Sign-up fixes from xian's 11-02 walk, v2 (Comms, after CXO's 17:10 ruling and HOST's 17:10 answer). No semicolons, they/them for Piper

**Status: CXO OK'd v2 as written, 17:20, no edits.** Ships now: section 4 (the `/try/` merge and redirects), and on `/try/beta/` the heading, the one sentence, no ticks, no "No spam" line, and the back link. Rides the newsletter switch, live together and never before: the form description, the checkbox, the confirmation email and the `/privacy` lines. Until the switch, the live checkbox stays. After it, HOST checks that an address that never confirms gets nothing further (if not, Comms rewrites the email's last line), and one real sign-up gets quoted end to end for CXO before #2256 closes.

v1 (sent 17:1x) is replaced by this. What changed: CXO merged `/try/` and `/try/invite/` (item 4) and gave notes on items 1 to 3. HOST found that Buttondown's confirmation text is per newsletter, so the waiting list becomes **a second newsletter**, not a tag.

**Order (CXO's):** CXO OKs this text. Next, xian creates the second newsletter (HOST's step) and pastes the confirmation text below. Then Web repoints the form and builds. The email and the consent words only become true once sign-ups land in the new newsletter, so they go live together, never before.

### 1. The confirmation email (paste-ready, for the new newsletter's Settings > Subscribing > Confirmation)

- **Subject:** Confirm your place on the Piper Morgan waiting list
- **Body** (keep Buttondown's own confirm link or button where its template puts it. HOST checks that once it's built):

> Thanks for joining the Piper Morgan waiting list. Please confirm this is your address, so we can reach you.
>
> [confirm link]
>
> Next, we'll email you when we can invite you to the private beta, and when the public beta starts. We'll tell you before sending anything else.
>
> If you didn't sign up, ignore this email and you won't hear from us.

### 2. `/try/beta/`, only the form (CXO's ruling), every string

- **Meta title:** Join the Waiting List | Piper Morgan (unchanged)
- **Meta description:** Join the Piper Morgan waiting list for a private beta invitation, or a note when the public beta starts.
- **Heading:** Join the waiting list
- **The one sentence:** We're sending invitations in waves. Join the waiting list for an invitation, or just to hear when the public beta starts. (CXO's words)
- **Form title:** Sign up
- **Form description, what they're agreeing to** (CXO's sentence, xian's item 2): We'll email you about your invitation and when the public beta starts, and we'll tell you before sending anything else.
- **No ticks.**
- **Button:** Join the waiting list
- **Checkbox:** I agree to these emails, as described in the [Privacy Policy](/privacy). I can unsubscribe at any time.
- **Under the form:** nothing. "No spam, unsubscribe at any time" goes (CXO, item 3).
- **Success message:** You're on the list. Check your inbox (and spam folder) for the confirmation link. (unchanged)
- **Back link:** ← What the beta asks (to `/try/`)
- **Web note:** the checkbox and the line under the form live in the shared `NewsletterSignup` component. The waiting-list use needs props for both (consent text, and an empty privacy notice), not new defaults.

**On CXO's legal question:** I'm not a lawyer, and this isn't legal advice. What I checked: `/privacy` says consent is recorded with a timestamp, Buttondown sends a double opt-in confirmation, and you withdraw consent by unsubscribing. Consent wording usually has to name the purpose, point to the policy, and say how to withdraw. The new checkbox does all three, and "these emails" points at the sentence just above it. It's narrower and more specific than "marketing communications", not weaker. If xian wants a lawyer's read, that's his call.

### 3. `/privacy`, needed before the new list goes live

The policy only describes the newsletter ("Send weekly newsletter content about AI-powered product management"). The waiting list has a different purpose, so add:

- **Under "Information We Collect", a new heading "Beta Waiting List":** When you join the waiting list, we collect your email address, the time you gave consent, and the page you signed up from. Our email service provider also collects your IP address.
- **Under "How We Use Your Information", a new heading "Beta Waiting List":** We use your email address only to send the confirmation email, to invite you to the private beta, and to tell you when the public beta starts. We'll tell you before sending anything else.
- **Data Retention, "Newsletter Data"** becomes "Newsletter and Waiting List Data". The text stays as it is.
- **"Last updated"** becomes the month it ships.

### 4. `/try/`, one page that says what the beta asks (CXO's ruling), every string in page order

Built from `/try/invite/`. The two-door frame and the ticks go, and `/try/invite/` 308s to `/try/` (`/try/alpha/` points straight at `/try/`).

- **Meta title:** Join the Private Beta | Piper Morgan
- **Meta description:** Piper Morgan is in private beta. See what it asks of you, and join the waiting list for an invitation or a note when the public beta starts.
- **og title:** Join the Piper Morgan Private Beta. **og description:** See what the private beta asks, and join the waiting list.
- **Hero headline:** Join the private beta
- **Hero text:** Piper Morgan is in private beta. We're inviting a small number of product people to use it for their real work and tell us what they find.
- **"What to expect"**
  1. **Invite-only, nothing to install.** Piper runs in your browser. We send you an invite code and you create your account. You connect your own Anthropic API key to use it.
  2. **Things will break.** We're iterating fast, and bugs are part of the process.
  3. **Your voice matters.** Your feedback reaches the team building it.
  4. **Real access.** You'll use Piper for your actual work, not a sandbox. It works with GitHub and Google Calendar.
- **"What we're looking for"**
  - An Anthropic API key of your own. Piper doesn't provide or pay for model usage
  - Willingness to report what's working and what isn't
  - Interest in AI-assisted product management
  - Patience with rough edges
- **"Want in?"** Join the waiting list for an invitation, or just to hear when the public beta starts. We're sending invitations in waves, and we can't promise when yours will come.
- **Button:** Join the waiting list →
- **"Have questions first?"** Email us at support@pipermorgan.ai. We're happy to chat, and to hear about the product work you do.
- **Bottom note** (kept from the old `/try/`): Not sure? That's okay. You can always read about the journey first, or learn more about the project.
- **Gone:** "How ready are you?", both cards, "← Back to options".

**Checked against the offered set:** GitHub and Google Calendar only, with no Slack or Notion (CXO and #2237). There's an Anthropic key only, and no other provider key. No claim about data ownership (the PDR-102 hold).

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

**Strings that change under this recommendation** *(applied into the Build copy section at 20:50, so this list is history)*:
- `/try/` card 1 button: **See what the beta is like →** (to `/try/invite/`)
- `/try/invite/` "Want in?": Join the waiting list. We're sending invitations in waves, so we can meet the needs of our beta testers, and we can't promise when yours will come. Button: **Join the waiting list →** (to `/try/beta/`)
- `/try/invite/` "Have questions first?": Email us at **support@pipermorgan.ai**. We're happy to chat, and to hear about the product work you do.
- `/try/` meta description: Choose your path to Piper Morgan. See what the private beta is like, or join the waiting list for an invitation or a note when the public beta starts. og description: See the private beta, or join the waiting list.
- `/get-involved/` line: Join the waiting list for the private beta if you're ready to dive in. Button: **Join the private beta →** (to `/try/invite/`)

## SUPERSEDED: the two decisions, with Comms' recommendation (as sent 18:53, kept for the record)

1. **What a visitor does now.** Recommended: **request an invite to the private beta by email**, and keep the second card as a "keep me posted" list for when Piper opens to everyone (the 1.0 Production release).
   - **Address:** **support@pipermorgan.ai**. It is the address the Terms and the beta letter already use (alpha@ was dropped there on 10-24), and it reaches only xian's own mailboxes (Exec, decisions.log 10-31 18:33). No new alias is needed. *(Revised 18:55 after PPM's memo. The 15:20 draft said alpha@.)*
2. **What happens to `/try/alpha/`.** Recommended: **move the page to `/try/invite/` and redirect `/try/alpha/` there**, so links in the alpha letters and old posts still land somewhere true. The current `/try/beta/` page stays where it is as the signup list, reworded below.

## Build copy (one way in, updated 20:50. No semicolons, they/them for Piper)

### `/try/` hero, third sentence (added after the 21:40 launch, CXO 21:48)
- Was: "Others prefer to wait until things are smoother."
- Now: **Others would rather wait for the public beta.** It uses the same term as card 2 and `/try/beta/`, so the hero points at what card 2 offers. CXO suggested "until it opens to everyone", which is also fine. I chose the "public beta" wording so the page uses one term for one thing.
- The first two hero sentences are unchanged ("Piper Morgan is in active development. Some people want to dive in now and help shape it.").

### `/try/` card 1 (replaces the Alpha card)
- Eyebrow: **For early adopters**
- Heading: **I'm ready to get my hands dirty**
- Body: Piper Morgan is in private beta. It's hosted and invite-only, so there's nothing to install. It's early, with rough edges, and your feedback is read by the team.
- Bullets:
  - Invite-only, nothing to install
  - Bring your own Anthropic API key. Piper doesn't cover model costs
  - Works with GitHub and Google Calendar
  - Your feedback reaches the team building it
- Button: **See what the beta is like →** (to `/try/invite/`)

### `/try/` card 2 (replaces the Beta card), from xian's 20:35 words
- Eyebrow: **For the curious** *(unchanged)*
- Heading: **Join the waiting list**
- Body: Piper Morgan is in private beta. We're sending invitations in waves, so we can meet the needs of our beta testers. Sign up for the waiting list, or to hear when the public beta starts.
- Bullets: No setup needed · A place on the waiting list · A note when the public beta starts
- Button: **Join the waiting list →** (to `/try/beta/`)

### `/try/` page description (meta) and og description
- Description: Choose your path to Piper Morgan. See what the private beta is like, or join the waiting list for an invitation or a note when the public beta starts.
- og description: See the private beta, or join the waiting list.

### `/try/invite/` (the old alpha page, moved): every string, in page order
*(Rewritten 19:06 after Web's 19:03 memo listed six alpha strings the first draft didn't cover. Each line below replaces the string at that spot on `try/alpha/page.tsx`.)*
- Page title: **Join the Private Beta | Piper Morgan**. Description: See what the Piper Morgan private beta is like, and join the waiting list for an invitation. *(changed 20:50 for one way in. The 19:06 text said "Request an invite".)*
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
- "Want in?": Join the waiting list. We're sending invitations in waves, so we can meet the needs of our beta testers, and we can't promise when yours will come.
  - Button: **Join the waiting list →** (to `/try/beta/`)
- "Have questions first?": Email us at **support@pipermorgan.ai**. We're happy to chat, and to hear about the product work you do. *(both alpha@ uses become support@)*
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
- Meta: "…Join the waiting list for the private beta, contribute code, or share your expertise."
- Line: Join the waiting list for the private beta if you're ready to dive in.
- Button: **Join the waiting list →** (to `/try/beta/`) *(CXO 20:49: the line and the button say the same thing, and the button goes where it says)*

## SUPERSEDED in part: who keeps the card 2 list (CXO edit 4). xian chose B at 20:35, so options A and B below are history. The owner is Exec's to confirm with xian, and the build copy waits on it (CXO 20:49)

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
