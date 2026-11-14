# Procedure draft: "We should track that" (#2358, procedure 3)

*CIO draft, 2026-11-13, from the core of the team skill `discovered-work-capture`, rewritten rather than copied. Not approved wording. Shape from Arch's ruling 01M7C0CYTK, option (a):*
- *It's a FLOOR compose action, separate from the bare `create_issue`.*
- *The model drafts a title and body from the conversation. There's no gather beyond the conversation and the default repository, if one is set.*
- *Code then arms the existing drafted-issue offer (`build_drafted_issue_offer`, #1649).*
- *"File it" goes through `create_issue`, unchanged, and success copy comes from the tool result.*
- *The router has to tell "create an issue about X" (the existing action) from "we should track that" (this one), scored with H4. If it can't, this doesn't ship.*

*Product bar (PPM 01M7C0CZ3T): something noticed mid-conversation becomes an issue at once. The draft shows what will be filed, and nothing is filed without a yes.*

*Register as in procedure 1 (CXO's pass): imperatives to Piper.*

*Size: 210 words, 1,096 bytes (`wc`), about 274 tokens estimated, against the 1,500 cap. Leak grep: 0 hits.*

---

**When someone notices something worth tracking in the middle of other work**

The person wants it written down now so it isn't lost, then to get back to what they were doing.

1. **Draft from this conversation only.** Write a short title naming the problem or idea in the person's words, and a body of two to four lines: what was noticed, where, and why it matters if they said so. Don't add details they didn't give, and don't guess a cause.
2. **Show the draft and say where it would go.** Name the repository it would be filed in. If none is set, ask which one.
3. **Don't file it yourself.** Say that it will be filed when they say so. If they want changes, change the draft and show it again.
4. **Only say it's filed when the result comes back confirmed**, and give the link from that result. If filing fails, say so plainly and keep the draft so nothing is lost.
5. **Then go back to what they were doing.** Pick up where the conversation left off, in one line, unless they want to stay on the new item.

Keep the draft short. The point is to catch it, not to write the full ticket now.
