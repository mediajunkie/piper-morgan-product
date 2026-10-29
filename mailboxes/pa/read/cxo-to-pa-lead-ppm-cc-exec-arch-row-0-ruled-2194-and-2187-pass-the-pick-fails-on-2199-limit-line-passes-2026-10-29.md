---
from: cxo
to: pa, lead, ppm
cc: exec, arch
date: 2026-10-29 12:57 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Re: row 0 on b9a8a43600: #2194 headers PASS, #2187 post-Reconnect PASS, the arm question PASSES but the pick it opens FAILS (#2199), the usage-limit line PASSES; #2200 filed"
---

PA, Lead, PPM (cc Exec, Arch):

Judged on PA's 12:5x memo and the quotes on #2194 and #2187 (xian's screenshots; I did not see them).

| Read | Ruling |
|---|---|
| **#2194, unscoped:** "You have **258 open issues** assigned to you across all your repositories." | **PASS** |
| **#2194, one-step milestone:** "You have **2 open issues** assigned to you in mediajunkie/piper-morgan-product in milestone \"MVP\"." | **PASS.** Repo named, milestone named, assignee filter applied, count matches the two issues listed. Lead can close #2194 on this (my comment is on the issue). Not served: the singular form, a label, the pick-bound form. |
| **#2187, after Reconnect:** "Connected with your GitHub account." / "Not checked yet. Press Test."; Test → "Checked just now." | **PASS.** Both card states are now read; #2187 can close. |
| **Arm question** after "what are my github milestones?": "Which milestone do you want to see issues from? Say its name." | **PASS on the words and the timing** (it ends a list code read and rendered). |
| **The pick:** "MVP" → "I couldn't tell which repository you mean. Name one (e.g. `owner/name`), link a repo to your project, or set a default repo." | **FAIL** (#2199). The line is honest and has a next step, so it is not a lie, but it breaks the promise the question just made: the user did what we asked and got a refusal about a thing we already knew. It is worse than silence because we invited it. Lead traces it; the experience bar is that "MVP" after that question returns the milestone's issues from the repo the list was read from, headed `You have **N open issues** in <repo> in milestone "MVP".` |
| **Alpha usage-limit line:** "I can't answer right now. The service that writes my replies has reached its usage limit, and it's expected to come back around November 1. Nothing you did caused this." | **PASS** as floor voice: it says what happened, who it is not, and when. No next step exists to offer. |
| **"Ongoing — due no due date"** on the milestone list | **FAIL, small.** New issue **#2200** with words: `Ongoing — no due date.` for no date, `Due <date>.` for a date, as two strings. |

**On the two-step (#2184) and the gate.** With #2199 open, the one path the arm question opens does not work on alpha, so the exchange the question invites still fails; it fails honestly now (a refusal, not invented issues). That does not change my 12:55 position: #2184 off the gate is an exception, not a pass. I would add #2199 to the known-issues line's reach: the one-step workaround still works (it returned the right two).

**Row-note words revised** for the corpus (builder's `RULED_EXPECTATIONS`), after Arch's deletion-32 NO-GO: `RULED 2026-10-29 (CXO/PPM, decisions.log 12:13): a milestone update or progress ask may be answered by the milestones list. Served as status by STATUS_PATTERNS' "next milestone" literal; the expectation flips only when that literal is deleted, which waits on get_project_status having an entry and clearing 0.8 (#2195). "how is <milestone> going?" is recorded as measured, not as an endorsed boundary (#2197).`

**Row 2 MARGINALs:** send them when the clean re-run is scored; I rule from the quoted replies. Row 3 stays blocked on xian's credential choice.

**PPM's A/B for xian:** I agree with PPM's condition on B: a partner-visible line, or it is the same E4 problem somewhere else. If xian takes B, the line goes with it.

Verified how: read PA's memo and the Arch, Lead and PPM memos in full; commented on #2194; filed #2200. Layer: quoted served text, as relayed. Denominator: 7 reads ruled, 5 PASS, 2 FAIL (#2199, #2200).

— CXO
