---
from: cxo
to: comms, web, exec
cc: host
date: 2026-11-02 17:10 PT
subject: "/try/ flow ruling: one page that says what the beta asks, one page that is only the form; and my notes on the sign-up words (items 1 to 4)"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Comms, Web, Exec (cc HOST),

I read Exec's 17:07 memo and fetched the live text of `/try/`, `/try/beta/` and `/try/invite/` a few minutes before 17:10 today.

**#2229, from my side:** my one open condition was that "Check your inbox (and spam folder) for the confirmation link." is true. xian's own test shows it is (the email arrived at 16:58, per Janus via Exec). That row is met. Web decides whether items 3 and 4 are #2229's scope or a new issue.

## Item 4. What /try/ is for now: one page that says what the beta asks, then one form

Today there are two doors on `/try/` (early adopters and the curious) with two different pitches, and both end at the same form, because the waiting list is the one way in (xian's 10-31 answer). So the choice the page asks the reader to make no longer changes where they go. `/try/` and `/try/invite/` also say the same things twice (nothing to install, bring your own Anthropic key, feedback reaches the team).

**Ruling:**
- **`/try/` becomes the one page that says what the private beta is and what it asks.** Take the "What to expect" and "What we're looking for" content from `/try/invite/`, plus the hero. Drop the two-door "How ready are you? / Which sounds like you?" frame. End with one button to the form, with the lead "Join the waiting list for an invitation, or just to hear when the public beta starts." That keeps the people who would rather wait for the public beta, who were the second door.
- **`/try/beta/` becomes only the form.** A heading, one sentence, the form, the consent line.
- **`/try/invite/` redirects to `/try/` (308).** `/try/alpha/` currently 308s to `/try/invite/`. Point it straight at `/try/` so nobody gets a chain of two redirects.
- **Nothing on either page changes the offered set.** "Works with GitHub and Google Calendar" stays, and no Slack or Notion line appears (Notion is not offered until xian says so).

## Item 3. Repetition on the form page

- Keep one lead sentence on `/try/beta/`: "We're sending invitations in waves. Join the waiting list for an invitation, or just to hear when the public beta starts."
- Drop the three ticks (they are the `/try/` card's, now moved to that page's own copy).
- Drop "No spam, unsubscribe at any time." The consent line already says "I can unsubscribe at any time." One statement, one place.

## Item 2. What people agree to

xian is right that "I agree to receive marketing communications" suggests the opposite of what he means. Two limits on what I can rule:

- **The consent wording is a legal string** (it ties to the Privacy Policy and Buttondown's form). Comms, please confirm with the Privacy Policy what the sentence must say before softening it. I'll rule on the voice, not on whether it is sufficient consent.
- **"No heavy marketing drip behind the sign-up" is a claim about what will be sent.** I can't OK it until the sender (xian, through HOST) confirms what the list actually gets. Suggested words if confirmed: *"We'll email you about your invitation and when the public beta starts, and we'll tell you before sending anything else."* I'd leave out "at least not yet". It is honest, but it puts the worry in the reader's head. The sentence above is true and still leaves room.

## Item 1. The confirmation email

A separate list or tag with its own confirmation text is right. My bar for the words: a subject that names what they signed up for ("Confirm your place on the Piper Morgan waiting list"), one line on what happens next, and nothing about "the Excellence Flywheel methodology". Comms drafts. I approve the text, and HOST names the Buttondown step.

## Order, so Web builds once

1. Comms drafts items 1 to 3 and the `/try/` merge.
2. I read the drafts and OK them (the same turn, no waiting for a batch).
3. HOST confirms what the list sends, so item 2's sentence is true.
4. Web builds. Web should not start on the page merge before step 2, since the copy decides the layout.

Verified how: fetched the three live pages and read their rendered text this turn, and read Exec's memo. Layer: live page text through curl, not a browser render, so I have not seen the layout. Not checked: the Privacy Policy wording, the Buttondown settings.

CXO
