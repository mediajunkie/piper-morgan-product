# Procedure draft: "We should track that" (#2358, procedure 3)

*CIO draft, 2026-11-13, from the core of the team skill `discovered-work-capture`, rewritten rather than copied. Not approved wording. Shape from Arch's ruling 01M7C0CYTK, option (a):*
- *It's a FLOOR compose action, separate from the bare `create_issue`.*
- *The model drafts a title and body from the conversation. There's no gather beyond the conversation and the default repository, if one is set.*
- *Code then arms the existing drafted-issue offer (`build_drafted_issue_offer`, #1649).*
- *"File it" goes through `create_issue`, unchanged, and success copy comes from the tool result.*
- *The router has to tell "create an issue about X" (the existing action) from "we should track that" (this one), scored with H4. If it can't, this doesn't ship.*

*Write fields (Arch 01M7C0QSG0, Lead's three conditions accepted):*
- *The compose call returns `title` and `body` as structured output.*
- *Code renders the shown draft from those fields and arms the offer from the same value (pinned byte for byte).*
- *Code appends the ask line and stores it as `question`, and sets `drafted_issue_pending`.*
- *If the output is missing or invalid, nothing is armed and the plain create flow is offered.*

*So the text below governs what goes into the two fields and the one line around them. It never writes the ask (CXO: say what happens next, and leave the ask to code).*

*Product bar (PPM 01M7C0CZ3T): something noticed mid-conversation becomes an issue at once. The draft shows what will be filed, and nothing is filed without a yes.*

*Register as in procedure 1 (CXO's pass): imperatives to Piper.*

*Size: 227 words, 1,208 bytes (`wc`, after the write-fields edit), about 302 tokens estimated, against the 1,500 cap. Leak grep: 0 hits.*

---

**When someone notices something worth tracking in the middle of other work**

The person wants it written down now so it isn't lost, then to get back to what they were doing.

1. **Draft from this conversation only, as a title and a body.** Write a short title naming the problem or idea in the person's words, and a body of two to four lines: what was noticed, where, and why it matters if they said so. Don't add details they didn't give, and don't guess a cause.
2. **Say plainly what happens next**, in one line above the draft: it will be filed in the named repository if they say yes. If no repository is set, ask which one instead. Don't write the yes-or-no question yourself; it's added after your draft.
3. **You never file it.** If they want changes, write the title and body again with the changes.
4. **Only say it's filed when the result comes back confirmed**, and give the link from that result. If filing fails, say so plainly and keep the draft so nothing is lost.
5. **Then go back to what they were doing.** Pick up where the conversation left off, in one line, unless they want to stay on the new item.

Keep the draft short. The point is to catch it, not to write the full ticket now.
