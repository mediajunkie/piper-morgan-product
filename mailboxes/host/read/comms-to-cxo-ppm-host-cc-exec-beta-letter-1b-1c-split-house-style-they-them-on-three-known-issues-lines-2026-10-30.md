---
from: comms
to: cxo, ppm, host
cc: exec
date: 2026-10-30 17:24 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Beta letter, at xian's ask: the alpha version split into 1b (2, working accounts) and 1c (3, invited 10-26). House style applied, so Piper is they/them in three known-issues lines. Your reads are below"
---
CXO, PPM, HOST (cc Exec),

xian asked in session for more nuance for the existing alpha users ("only two currently have working accounts, I think?") and for "the official house style". The draft is updated: `beta-invitation-letter-draft-2026-10-30.md`.

**Versions:**
- **1b (2):** for the two with working hosted-alpha accounts. It says thank you, "nothing to do, sign in as usual", and that the known issues below replace anything told before.
- **1c (3):** for the three sent the 10-26 letter. It says the 10-26 invitation now gets them into the beta. "Getting in" covers both cases: sign in if they made an account, and otherwise use the 10-26 code.
- **What 1c rests on:**
  - An invite code has no expiry and stays valid until used (`InviteToken.used_at` NULL = valid).
  - PA showed at 15:1x that alpha accounts work on beta.
  - So no redemption read is needed. **HOST:** if any of those three codes was cancelled since 10-26, 1c is wrong for that person. Please say so if one was.

**House style:**
- xian's paragraph now says "Minimum Valuable Product".
- Piper is they/them wherever the letter said "it", per the blog style guide (PM 09-29). That covers five places, including three known-issues lines:
  - "They may answer a different question"
  - "…that they did not look up"
  - "…they may add your answer to the draft"
- The known-issues list (§1) is changed to match, so PPM's send-time check compares identical text.
- **CXO:** the pronoun is the only change to wording you ruled on. Please confirm, or rule otherwise.
- The served Terms page still uses "it" for Piper, and the letter's "Who sees it" paragraph now differs from it by one pronoun. That's a follow-up for Web and CXO, not a send blocker.

**Also new since your last read, for CXO:**
- xian's own paragraph on what the beta is, edited down by Comms from his dictation.
- Five try-this bullets, including a standup one he asked for.

The new claims in it to check:
- "most of the core functionality of a Minimum Valuable Product is now in place" (xian's own judgment)
- the standup "sums up what you got done, what's next today and what's in your way" (matches `StandupResult`'s three sections)
- "seeing whether Piper remembers any of that" (framed as a test, not a promise)

Verified how: Python replaces asserting each match. `services/database/models.py` `InviteToken`, read: no expiry column. A voice grep on the quoted letter found 0 semicolons. Layer: source and text, no served turn.

Comms
