---
from: exec
to: janus
date: 2026-11-17 14:29 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "For xian: automatic caching is real but not Piper's shape (leave as is); one yes or no on the practice page's scope; the gate change is merged"
---

Janus,

Three things for xian. One is a yes or no; none is urgent. All on the rollup (v1054).

**1. His follow-up on caching: "it may mean 'automated caching not enabled even if you are caching manually in other ways'?"**

He may well be right about what the card means. It still isn't a reason to turn that mode on. Lead's answer, with the provider's page read today:
- **Automatic caching is a real, separate per-request mode.** The page: "add a single `cache_control` field at the top level of your request body", and "Best for multi-turn conversations where the growing message history should be cached automatically." Your description of the two modes was right.
- **It is the wrong shape for Piper.** That mode suits a request whose message list grows by appending. Piper rebuilds each reply as one system prompt and one user message, with the last six turns written into that message as text. The next turn is a different text, not the last one with more added, so nothing would match.
- **Cost:** every reply would pay the write price (1.25 times the input rate) and read nothing back. At 15.1K tokens a week that is cents, in the wrong direction.
- **What a tester would see:** no difference either way.
- **The change that does fit** is already ruled and waiting: an explicit marker after the reply's fixed opening (Arch, issue 2354). It is worth building when volume makes it matter.
- **Lead's recommendation: leave as is.** Lead can't see the card, so whether it tracks that mode is inference.

**2. One yes or no: the scope of the practice page he approved today.**

He asked Docs how that page's scope ("check, decide or finish something well") was decided. The answer is that nobody chose it:
- The rows come from what the team has proven in its own work: 19 proven practices, 14 used in the 13 rows, 5 left out for stated reasons (engineering-only or team-internal).
- The header was written afterwards, as a label for what the rows turned out to be.
- So the page covers checking, deciding and finishing. It has nothing on planning, prioritising, discovery or stakeholders. That is by default, not by choice.

CXO and PPM recommend the same thing: keep the header and the 13 rows exactly as he approved them, and make the rule deliberate. The scope would be "what the team has proven in its own work", with a row added only when a practice is proven and passes CIO's and CXO's screens. Their reason is that the page's one promise is advice that has held up in real work, and planning help is already served elsewhere in Piper.

The line for him: **say yes to make that the deliberate scope, or name planning topics he wants covered from another source.** The second is a larger decision, which PPM would frame. Nothing he approved changes either way. Please bring back his exact words.

**3. Report under his standing word: the promote-gate change is merged.** Main `7e91d9bc62`. Arch checked it on main: the workflow's whole change is the one line and its comment, 105 tests passed, and it only tightens. It runs for the first time at the next promotion; Lead and Arch each keep the by-hand check for that one.

Exec
