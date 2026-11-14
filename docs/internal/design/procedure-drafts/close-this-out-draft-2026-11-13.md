# Procedure draft: "Close this out" (#2358, procedure 2)

*CIO draft, 2026-11-13, from the core of the team skill `close-issue-properly`, rewritten rather than copied. Not approved wording. Shape from Arch's ruling 01M7C0CYTK, option (a):*
- *It's a FLOOR compose action, separate from the bare `close_issue_query`.*
- *A read-only gather reads the issue: its body, linked pull requests, recent comments and state.*
- *The model drafts an evidence comment.*
- *Code offers the existing comment action with its own confirm. Only after that comment is confirmed posted does code offer the existing close, with its DESTRUCTIVE confirm.*
- *There's no combined confirm. If the comment fails, close isn't offered. If the issue is already closed, Piper says so and offers the comment only.*
- *The router has to tell "close #42" (the existing action) from "close this out" (this one), scored with H4. If it can't, this doesn't ship.*

*Write fields (Arch 01M7C0QSG0):*
- *The compose call returns the comment's `body` as structured output.*
- *Code renders the shown comment from it and arms the comment offer from the same value (pinned byte for byte).*
- *Code writes and stores the ask line.*
- *If the output is missing or invalid, nothing is armed.*

*Revised 11-13 for Arch 01M7C13VBK: step 4 no longer asks about closing before the comment, because that would blur the two-confirm order; code's later close offer restates the open steps. The model produces the comment body and at most one line around it. The step-6 guard is one line. When step 3 asks how the work was checked, the output is a "need more from the person" state with no draft and nothing armed (Lead's schema).*

*Arch 01M7C1AHWA: CONFORMS to the mechanism rulings. His step-2 wording, "draft the evidence comment only", applied.*

*The text below never writes an ask (CXO: say what happens next, and leave the ask to code).*

*Product bar (PPM 01M7C0CZ3T): evidence before done. The person sees what was done and how it was checked before anything closes, and the close keeps its own confirm.*

*Register as in procedure 1 (CXO's pass): imperatives to Piper. Field names follow Lead's gather, as for procedure 1.*

*Size: 272 words, 1,524 bytes (`wc`, after Arch 01M7C13VBK), about 381 tokens estimated, against the 1,500 cap. Leak grep: 0 hits.*

---

**When someone asks you to close out a piece of work properly**

The person wants a closed item that someone else could trust later: what was done, and how it was checked.

1. **Work only from the issue below and from what the person tells you here.** If the issue couldn't be read, say so and stop. Don't draft from memory.
2. **If the issue below is already closed, say so.** Draft the evidence comment only.
3. **Draft a short evidence comment as the comment's body**, with two parts:
   - **What was done:** from the issue, its linked changes and the person's words.
   - **How it was checked:** what was actually run, looked at or confirmed, and by whom if known.

   If nothing below shows how it was checked, don't invent a check and don't write a comment yet. Ask the person how they confirmed it works. Their answer goes into the comment next time, in their words.
4. **Name what's still open, first.** If the issue lists steps or boxes that aren't done, name them before anything else. Don't ask about closing yet; that question comes after the comment is posted.
5. **Around the comment, write one line at most:** what happens next, in plain words, for example "Here's the comment I'd add. Closing comes after it, as a separate step." The comment and the yes-or-no question are shown for you.
6. **Never say anything is posted or closed.** You don't post or close, and those results are reported separately.

Keep the comment short and plain: a few lines someone can read in ten seconds a month from now.
