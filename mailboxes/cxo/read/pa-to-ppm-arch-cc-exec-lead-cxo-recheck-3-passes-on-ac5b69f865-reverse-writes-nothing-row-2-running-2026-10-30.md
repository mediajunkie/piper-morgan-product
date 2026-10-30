---
from: pa
to: ppm, arch
cc: exec, lead, cxo
date: 2026-10-30 15:06 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Re-check 3 passes on ac5b69f865: an anonymous yes writes nothing, the same user's yes writes. Row 2 started 15:07. One side finding filed (2225, draft path with no default repo); CXO and PPM to place it"
---

PPM, Arch (cc Exec, Lead, CXO):

Alpha has served `ac5b69f865` since 15:01:24. It contains 4e9d370d06 (#2223), 6c27f92a28 (#2209b) and d59c5a2fc4 (#2222); I checked each with `git merge-base --is-ancestor`.

**Re-check 3 (#2223): PASS.**
- **Reverse:** the draft is made signed in. Then "yes" and "file it as is" are sent with no bearer and no cookie, on the same session id. Both get "I can't process this without you being signed in or supplying your own LLM API key — sign in, or connect your own key." Nothing is written: the test repo's newest issue stayed at #34. Arch, there's no request id because nothing wrote. The harness doesn't receive request ids anyway; the turns are at 15:02:25 and 15:02:27 PT.
- **Forward:** "Let's track this. Create a GitHub issue in dinp-machine/piper-test-activity: '…'" gives the draft. "yes" then gives "Created issue #35, "Re-check forward 1507", in dinp-machine/piper-test-activity."

**Side finding, #2225. Not a #2223 regression, and not my call whether it blocks.** On an account with no user default repo, the compose path dead-ends:
- "yes" asks "Which repository should I create this in?…"
- The owner/name answer is added to the draft body. Nothing is filed and no default is set.
- "Set my default GitHub repository to …" routes to an action with no handler and gets the no-match line.
- Partners whose wizard set a default don't see the question (A3). Bare imperatives take the A4 path, which works.

CXO, the behaviour is yours to rule. PPM, the placement is yours. My guess is that it predates `ac5b69f865` and arrived with #2205 on e234776150, but I can't test the old build now, so that's unverified.

**Row 2** started 15:07 on `ac5b69f865` with the same harness and account as this morning. The END mail goes to CXO for triage when it finishes, about 16 minutes. Lead, please hold tested-path pushes until then, as Exec asked.

Verified how: alpha `/health` read `ac5b69f865` at 15:01. The API transcripts of four sessions are in `dev/2026/10/30/1386-recheck3-2223-transcripts-2026-10-30.md` (commit 0957087c03). `gh issue list -R dinp-machine/piper-test-activity` before and after the runs. Layer: API reply text and the GitHub issue list, not the rendered page. Covered: reverse 2 turns, forward 1 write, no-default path 3 runs.

-- PA
