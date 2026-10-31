# /try pages after the beta started: proposal for xian (#2229)

**Drafted:** Comms, 2026-10-31 15:2x PT, after Exec 13:51 ("All beta invitations sent!", so beta wording is public-facing now).
**Read from:** website origin/main, `src/app/(public)/try/page.tsx`, `try/alpha/page.tsx`, `try/beta/page.tsx`, `get-involved/page.tsx`.
**Path:** xian picks → CXO OKs the copy → Web builds it and checks the served HTML (#2229 acceptance).

## The two decisions, with Comms' recommendation

1. **What a visitor does now.** Recommended: **request an invite to the private beta by email**, and keep the second card as a "keep me posted" list for when Piper opens to everyone (the 1.0 Production release).
   - **Address:** keep **alpha@pipermorgan.ai** for now. It already reaches you. A new beta@ address only helps if you set up the alias first. Your call: say "beta@" and we use it once it exists.
2. **What happens to `/try/alpha/`.** Recommended: **move the page to `/try/invite/` and redirect `/try/alpha/` there**, so links in the alpha letters and old posts still land somewhere true. The current `/try/beta/` page stays where it is as the signup list, reworded below.

## Draft copy (no semicolons, they/them for Piper)

### `/try/` card 1 (replaces the Alpha card)
- Eyebrow: **For early adopters**
- Heading: **I'm ready to get my hands dirty**
- Body: Piper Morgan is in private beta. It's hosted and invite-only, so there's nothing to install. Most of the core is in place, and there are still rough edges. Your feedback goes straight into what we build next.
- Bullets:
  - Invite-only, nothing to install
  - Bring your own Anthropic API key. Piper doesn't cover model costs
  - Works with GitHub and Google Calendar
  - Direct influence on development
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
- Ask: Email **alpha@pipermorgan.ai** (or the address you choose) with a line about what you'd use Piper for. Subject line: "Beta invite request".

### `/try/beta/` (signup page) meta
Title: **Keep Me Posted | Piper Morgan**. Description: Leave your email and we'll tell you when Piper Morgan opens to everyone.

### `/get-involved/`
- Meta: "…Join the private beta, contribute code, or share your expertise."
- Line: Request a beta invite if you're ready to dive in.
- Button: **Request a beta invite →** (to `/try/invite/`)

## Checks before it goes to CXO
- Every claim matches the letter: hosted, invite-only, your own Anthropic key, GitHub and Google Calendar (not Slack or Notion, see #2237).
- "Bring your own LLM provider key" becomes "Anthropic API key", because the beta takes only an Anthropic key (the letter's setup step).
- Old "alpha" mentions that stay: none planned on these pages. Blog posts that say alpha are history and stay as they are.
