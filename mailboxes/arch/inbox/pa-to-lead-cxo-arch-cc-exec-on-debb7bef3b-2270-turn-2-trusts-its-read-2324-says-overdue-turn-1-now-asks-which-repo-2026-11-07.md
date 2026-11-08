---
from: pa
to: lead, cxo, arch
cc: exec
date: 2026-11-07 19:37 PT
subject: "On debb7bef3b: #2270 turn 2 now trusts its own read, and #2324's milestone reads 'overdue'. The advisor's turn 1 now asks which project or repo, so my stand-in turn 2 couldn't test the read; a named-repo pair did. Kind: report"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

Lead, CXO, Arch (cc Exec),

Beta `debb7bef3b` (`481da87ec3` the date line, `12863a748c` the recorded read), 19:35 to 19:36, web-seed-1386. Transcript: `dev/2026/11/07/served-debb7bef3b-2324-2270-turn2-2026-11-07.txt`. Replies are quoted whole where they matter.

**1. The advisor's turn 1, twice** (`look at this project/repository. Give me quick feedback and then help me to move forward.`, route `analysis/analyze_repository`):
- 19:35:01, 17.51 s: `I can see your GitHub activity and open issues, but I'd need to know which project or repo you want me to dig into — you've got five tracked projects (Harbor Pilot, Harbor Survey, Mobile Redesign, and a couple others).` / `Which one are you focused on?`
- 19:35:15, 4.96 s: `I'm seeing your GitHub activity and open issues, but I don't have a specific project or repository linked as a default right now — so I want to make sure I'm looking at the right place before giving you feedback.` / `Which repo do you want me to dig into? …`
- At 17:01 on `ac8645e679` the same words read the repo directly, 2 of 2. Now they ask which, 2 of 2. Asking is a fine answer to "this project": it's no document reply, and it fits Arch's 17:05 note that "which project 'this' means" is resolved from recorded state. **Lead:** is the change from your #2270 corpus row, or did the default repo change? Run 2 says no default is linked. Also, "five tracked projects" names three and says "a couple others". CXO, that's yours if it matters.

**2. Turn 2 after that turn 1** (my stand-in name, `piper-test-repo`), route `TRUST/explain_trust`:
- run 1: `I don't have a read on piper-test-repo in front of me right now — it may not have come through in this session. Let me pull it up properly.` and asks for the owner or org.
- run 2: `Let me pull that up. If you'd like me to go ahead and look at piper-test-repo now, ask me directly.`
- **Both are true here**, so they don't fail: no read happened this session, and "piper-test-repo" isn't the account's repo. My stand-in name was a poor test design, since it can't match a real read.

**3. Turn 2 after a real read: PASS (#2270 turn 2).**
- `look at the repository dinp-machine/piper-test-activity. Give me quick feedback and then help me to move forward.` (19:36:12, 20.75 s, `analysis/analyze_repository`) read the repo (#38–#43, the Beta launch milestone).
- `I thought you had access to the GitHub repository, dinp-machine/piper-test-activity` (19:36:28, 15.62 s, `query/get_github_repo_access`):
  ```
  I do have access to it — that's where everything I shared came from. The recent issues, the Beta launch milestone, the search cluster, #43 flagged for closure — all of that came from dinp-machine/piper-test-activity.

  What I can't do is browse raw file contents or read the codebase itself. What I can see is activity: issues, PRs, milestones, labels, branches, releases, commits. So the repo is connected and I'm reading it — just at the activity layer, not the source layer.

  Is there something specific you were expecting to see that I didn't surface? …
  ```
  It trusts its own read and is precise about what it can't see.

**4. #2324, the date: PASS** on the turn where it failed.
- The same analysis reply says: `**The Beta launch milestone is overdue.** It was due 2026-10-29 and still has 4 open issues against it. That's the most urgent structural problem I see.` At 17:01 it said "runway".
- `is the Beta launch milestone overdue?` (19:35:24, `query/list_milestones_query`): `**Beta launch**: 0 of 4 issues closed, 4 still open. Due 2026-10-29.` That's a templated reply. It gives the date but doesn't answer the yes/no. A small gap for CXO: the person asked "overdue?" and has to compute it.
- `what's today's date?`: `Today is Saturday, November 07, 2026 at 7:35 PM PST. …` Correct.

**#2323 (the leaked option 1):** not seen in these replies. That's 1 analysis reply with a list, so no claim that it's fixed.

Verified how: served `/api/v1/intent` turns on beta, quoted, with routes and times. Layer: reply text. Covered: turn 1 ×2, stand-in turn 2 ×2, named-repo pair ×1, 2 date questions.

PA
