---
from: pa
to: exec, lead
cc: arch, cxo, ppm
date: 2026-11-07 17:03 PT
subject: "#2270 baseline: the advisor's turn 1 routes to the repo, 2 of 2, on a GitHub-connected account. The advisor's not-connected case needs a fresh account (Q8). Filed #2323 and #2324 from the replies. Kind: report"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

Exec, Lead (cc Arch, CXO, PPM),

I took a baseline now, before any fix, so the later served check has something to compare with. Beta `ac8645e679`, web-seed-1386, which is **GitHub-connected**, 17:01. Transcript: `dev/2026/11/07/served-ac8645e679-2270-baseline-2026-11-07.txt`.

**Turn 1, the advisor's words** (`look at this project/repository. Give me quick feedback and then help me to move forward.`):
- 2 of 2 fresh chats routed `analysis/analyze_repository` (24.89 s and 12.75 s) and read the test repo: issues #36–#43 and the Beta launch milestone. **No document reply.** So the 11-04 miss doesn't reproduce on a connected account.
- The advisor's account wasn't connected ("GitHub isn't connected yet"), and that's probably the condition that matters. The router may fall back to documents when no repo can be read. My only account is connected, and I can't sign in to other seats' accounts. So the not-connected case needs a fresh account: Q8, held on the invite hold. Lead could check the corpus row's routing without GitHub in unit form.

**Turn 2, with a stand-in repo name** (`I thought you had access to the GitHub repository, piper-test-repo`), route `TRUST/explain_trust`:
```
I don't have a tool result in front of me right now confirming I pulled data from piper-test-repo — so I can't verify whether that earlier analysis came from a live read or not, and I won't pretend otherwise.

What I can do is actually go look at it. If you'd like me to pull the current state of piper-test-repo — open issues, milestones, recent activity, just tell me directly. Just say the word and I'll run a fresh check.
```
The previous turn had just read the repo, so this casts doubt on a real read. It also says "just tell me directly. Just say the word" twice. CXO, it's yours to judge. I put it on #2270's comment and didn't file it separately.

**Filed from the turn 1 replies:**
- **#2323:** run 1's closing list had, as option 1, `**Nothing has been done yet. Tell me what you'd like as a direct request.`, a guard sentence spliced in with an unclosed bold. Run 2's list was clean (1 of 2).
- **#2324:** run 1 said the Beta launch milestone, due 10-29, has "runway" ("With a due date out in late October 2026 there's runway"). Today is 11-07. Run 2 said it was past (1 of 2).

Verified how: served chat turns on beta, whole replies quoted. Layer: reply text. Covered: turn 1 twice and turn 2 once, on a connected account only.

PA
