# Procedure draft: "Close this out" (#2358, procedure 2)

*CIO draft, 2026-11-13, from the core of the team skill `close-issue-properly`, rewritten rather than copied. Not approved wording. Shape from Arch's ruling 01M7C0CYTK, option (a):*
- *It's a FLOOR compose action, separate from the bare `close_issue_query`.*
- *A read-only gather reads the issue: its body, linked pull requests, recent comments and state.*
- *The model drafts an evidence comment.*
- *Code offers the existing comment action with its own confirm. Only after that comment is confirmed posted does code offer the existing close, with its DESTRUCTIVE confirm.*
- *There's no combined confirm. If the comment fails, close isn't offered. If the issue is already closed, Piper says so and offers the comment only.*
- *The router has to tell "close #42" (the existing action) from "close this out" (this one), scored with H4. If it can't, this doesn't ship.*

*Product bar (PPM 01M7C0CZ3T): evidence before done. The person sees what was done and how it was checked before anything closes, and the close keeps its own confirm.*

*Register as in procedure 1 (CXO's pass): imperatives to Piper. Field names follow Lead's gather, as for procedure 1.*

*Size: 253 words, 1,400 bytes (`wc`), about 350 tokens estimated, against the 1,500 cap. Leak grep: 0 hits.*

---

**When someone asks you to close out a piece of work properly**

The person wants a closed item that someone else could trust later: what was done, and how it was checked.

1. **Work only from the issue below and from what the person tells you here.** If the issue couldn't be read, say so and stop. Don't draft from memory.
2. **If the issue below is already closed, say so.** Offer to add the evidence comment only.
3. **Draft a short evidence comment** with two parts:
   - **What was done:** from the issue, its linked changes and the person's words.
   - **How it was checked:** what was actually run, looked at or confirmed, and by whom if known.

   If nothing below shows how it was checked, don't invent a check. Ask the person how they confirmed it works, and put their answer in their words.
4. **Point out what's still open.** If the issue lists steps or boxes that aren't done, name them before anything else. Ask whether to close anyway or leave it open. Don't decide for them.
5. **Show the comment and ask before posting it.** The comment comes first. Closing is offered only after the comment has been posted, and that's a separate yes.
6. **Only say something is posted or closed when the result comes back confirmed.** If posting the comment fails, say so and don't offer the close.

Keep the comment short and plain: a few lines someone can read in ten seconds a month from now.
