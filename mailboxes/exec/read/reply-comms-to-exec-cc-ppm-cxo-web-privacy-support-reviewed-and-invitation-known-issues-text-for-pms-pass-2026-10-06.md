---
from: comms
to: exec
cc: ppm, cxo, web
date: 2026-10-06
subject: "For PM's final pass (both pieces): (1) privacy/support wording reviewed, 4 plain-language edits, facts unchanged; (2) the invitation's known-issues text, 3 lines, verified against issue state"
---

Exec —

Both pieces, for PM's single pass.

## 1. Privacy and support wording: reviewed, edited in place

`docs/legal/mcp-privacy-and-support-proposal-2026-10-05.md` (commit "privacy/support proposal — plain-language
pass"). **Facts unchanged. No address inserted. The revoke gate is untouched.**
- "Only with your approval… **and only read-only**:" → "With your approval, given on a Piper sign-in page,
  the assistant can read:" (the stacked "only"; "cannot change anything" already says read-only).
- Dropped **"your colleague model:"** (internal jargon). The item now reads "the things Piper has confirmed
  with you about how you work".
- "Piper does not run its own AI model" → "**No AI model runs on Piper's side of this connection.**" Same
  fact, and it avoids "it" for Piper (PM's 10-06 they/them ruling).
- Support page: "that's **honest**, not broken… little in its colleague model" → "that's **expected**, not
  broken. Piper only reports what's actually there, and a new account doesn't have much yet." (PM strips
  "honest-" stems.)

**Before publishing (Web):** the **[bracketed source notes]** in section A (e.g. "[The server exposes three
read-only resources…]", "[PDR-006…]", the code identifiers) are for PM's review, not the page, so strip
them. Same for "*(see the gate above)*" on the support page.

## 2. Beta invitation: known issues (final text)

> **Known issues in this beta**
> We know about these, so there's no need to report them.
>
> - **Connectors.** The initial beta release supports only the GitHub connector, and during the beta
>   testing period we expect to add support for additional connectors before the 1.0 production release.
>   Slack and Google can't be connected yet.
> - **Reminders on the Radar.** If you complete a reminder in chat, it may stay pinned at the top of the
>   Radar until you reload the page. Reloading clears it.
> - **iPad.** Piper isn't tuned for iPad yet. In Safari on iPad, the layout can push the message box or
>   the Send button off-screen, and dates on Radar cards may show as raw timestamps. A laptop or desktop
>   browser works as intended.

Notes:
- **The connector sentence is PM's verbatim**, with one plain instruction after it so nobody tries Slack/Google.
- Built on CXO's three lines (each says what you'll see, then what to do instead of reporting it). No
  issue numbers, and no "we're aware".
- **Verified this fire** (`gh issue view`): the Radar issue OPEN/Production, iPad OPEN/Production (the
  symptoms are the ones its title records; the composer pushed off-screen is the one that blocks use, so I
  added it), the Slack/Google redirect issue OPEN/Production. Not reproduced, so the layer is issue state.
- **Struck**: the mono-font issue (CLOSED 10-06, per CXO). **Held**: add-a-project-without-a-name (OPEN,
  MVP, pending PM's gate-or-Production call). If PM moves it to Production, CXO's line is ready, but its
  workaround clause is unverified until someone runs it. **Not listed**: the "which reminder?" dead end
  (Lead fixing). The personality-settings question needs a live check first (CXO's note), so no line
  either way.

— Comms
