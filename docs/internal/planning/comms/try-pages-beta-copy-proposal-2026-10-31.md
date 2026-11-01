# /try pages after the beta started: proposal for xian (#2229)

**Drafted:** Comms, 2026-10-31 15:2x PT, after Exec 13:51 ("All beta invitations sent!", so beta wording is public-facing now).
**Read from:** website origin/main, `src/app/(public)/try/page.tsx`, `try/alpha/page.tsx`, `try/beta/page.tsx`, `get-involved/page.tsx`.
**Path:** xian picks → CXO OKs the copy → Web builds it and checks the served HTML (#2229 acceptance).
**Asked by:** xian via PPM, 10-31 18:50 ("can we ask Comms to propose updates and then Web can execute once I approve?"). Sent to Exec for xian's approval, cc CXO, Web, PPM.

## The two decisions, with Comms' recommendation

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

### `/try/` card 2 (replaces the Beta card)
- Eyebrow: **For the curious**
- Heading: **Keep me posted**
- Body: Not ready to try it yet? Leave your email and we'll tell you when Piper opens to everyone. There's no date yet, and we'd rather tell you when it's real than guess.
- Bullets: No setup needed · A note when Piper opens to everyone · Occasional updates on what we're building
- Button: **Keep me posted →** (to `/try/beta/`)

### `/try/` page description (meta)
Choose your path to Piper Morgan. Request an invite to the private beta, or leave your email and we'll tell you when it opens to everyone.

### `/try/invite/` (the old alpha page, moved)
- Title: **Join the Private Beta**
- Intro: Piper Morgan is in private beta. We're inviting a small number of product people to use it for their real work and tell us what they find.
- "What you'll need": An Anthropic API key of your own (Piper doesn't provide or pay for model usage) · Willingness to tell us what's working and what isn't · Interest in AI-assisted product management · Patience with rough edges
- Ask: Email **support@pipermorgan.ai** with a line about what you'd use Piper for. Subject line: "Beta invite request". We're sending invites a few at a time, so we can't promise one.

### `/try/beta/` (signup page) meta
Title: **Keep Me Posted | Piper Morgan**. Description: Leave your email and we'll tell you when Piper Morgan opens to everyone.

### `/get-involved/`
- Meta: "…Join the private beta, contribute code, or share your expertise."
- Line: Request a beta invite if you're ready to dive in.
- Button: **Request a beta invite →** (to `/try/invite/`)

## Open: who keeps the card 2 list (CXO edit 4, for xian)

CXO asked who keeps the "Keep me posted" list and sends the note. **Nobody does today.** The `/try/beta/` form posts to the Buttondown list (`NewsletterSignup`, tag `beta-waitlist`, website origin/main read 19:05). Web's 09-20 audit found that list dormant: 0-1 subscribers and nothing ever sent (`dev/active/web-standing-items.md` row 3a). On 10-02 xian took the /blog form off that list for the same reason and pointed it at LinkedIn and Medium. The preference-based signup that would fix it (row 3b) is waiting on xian's review of Web's straw plan.

Two options for xian:
- **A (Comms' recommendation): follow the /blog precedent.** Card 2 becomes "Follow along": "Not ready to try it yet? Follow the build on LinkedIn or Medium. We'll post there when Piper opens to everyone." The button goes to `/blog`, and `/try/beta/` redirects there too. That takes no email it can't answer, and the posts do go out.
- **B: CXO's interim wording.** Keep the form, and say "leave your email and we may tell you when Piper opens to everyone" until someone owns the list. It is true, but it still collects addresses for a list nothing sends from.

## CXO review (19:01): OK with four edits
Edits 1 and 3 applied as written. Edit 2 applied as "Your feedback reaches the **team** building it" instead of "the people building it", because the team is xian and his agents, and agents aren't people in public prose. Edit 4 is the open item above.

## Checks before it goes to CXO
- Every claim matches the letter: hosted, invite-only, your own Anthropic key, GitHub and Google Calendar (not Slack or Notion, see #2237).
- "Bring your own LLM provider key" becomes "Anthropic API key", because the beta takes only an Anthropic key (the letter's setup step).
- Old "alpha" mentions that stay: none planned on these pages. Blog posts that say alpha are history and stay as they are.
