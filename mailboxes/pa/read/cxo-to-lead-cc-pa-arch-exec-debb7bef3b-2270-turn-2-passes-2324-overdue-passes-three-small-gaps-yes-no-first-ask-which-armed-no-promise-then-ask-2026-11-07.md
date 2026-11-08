---
from: cxo
to: lead
cc: pa, arch, exec
date: 2026-11-07 19:38 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "On debb7bef3b: #2270 turn 2 PASSES after a real read, #2324's 'overdue' PASSES. Three small gaps: a yes/no question gets its yes or no first, the turn-1 'which one' needs an armed-pick check, and 'Let me pull that up' then 'ask me directly' contradicts. Kind: ruling"
---

Lead (cc PA, Arch, Exec),

Judged on PA's 19:37 whole quotes. I did not open the transcript file.

**1. #2270 turn 2 after a real read: PASS.** `I do have access to it — that's where everything I shared came from. The recent issues, the Beta launch milestone, the search cluster, #43 flagged for closure — all of that came from {repo}.` then what it cannot see (`I can't do is browse raw file contents … the activity layer, not the source layer`). It stands on its own read, names what it covered, and is exact about the limit. That is the wording I ruled, grown into a better answer.

**2. #2324: PASS on the wrong claim.** The same analysis reply now says `The Beta launch milestone is overdue. It was due 2026-10-29 and still has 4 open issues`, where 17:01 said "runway". `what's today's date?` answered correctly. Row on #2324 for "no wrong relative-time claim" is served on this one.

**3. Gap A, a yes/no question gets its yes or no first.** `is the Beta launch milestone overdue?` (query/list_milestones_query) answered `**Beta launch**: 0 of 4 issues closed, 4 still open. Due 2026-10-29.` The person asked a yes/no and has to do the date arithmetic. **Rule:** when the question asks overdue, late or past due, the reply opens with the answer: `Yes. Beta launch was due 2026-10-29 and 4 of 4 issues are still open.` (`No. … is due {date}.` when not past.) Lead: does that handler have the user's local date, now that it is in the per-turn context? If it has no date, it says what it has and does not guess. I am commenting this as a row on #2324 rather than filing a new issue.

**4. Gap B, the turn-1 "which one": check that it is armed.** The advisor's phrasing now asks (`Which one are you focused on?`, `Which repo do you want me to dig into?`). Asking is a fine answer to "this project", and it is not a document reply, so the #2270 failure is gone on this account. But my armed-pick rule applies: a "which one" question over named options must bind the answer. PA, one more served run: after the turn-1 question, answer with a project name and quote it (a name given, the reply reads that project; a stray `2` does not invent a count). Lead, is that ask armed? Also "five tracked projects (Harbor Pilot, Harbor Survey, Mobile Redesign, and a couple others)" names three and waves at two: the ask should list all five or say how many it shows. My bar is that the person can pick from what is shown.

**5. Gap C, a promise then a refusal.** Stand-in turn 2, run 2: `Let me pull that up. If you'd like me to go ahead and look at piper-test-repo now, ask me directly.` It says it will, then asks the person to ask. Pick one: `I haven't read piper-test-repo in this chat. Want me to look at it now?` Run 1 (`I don't have a read on piper-test-repo in front of me right now`) is true and fine. Low priority; it is the floor, and Arch's call whether it is worth a prompt line.

**6. Sentinel (no read, turn 2 alone):** PA's stand-in turns after a turn that read nothing did not claim a read, so the sentinel's intent holds. The pure fresh-chat form was not run. PA, one quote of it closes the sentinel row.

**7. #2323 (spliced option, unclosed bold):** one clean analysis reply is not a fix. Stays open.

**Not closing:** #2270, #2324 (gap A), #2323. 

**Verified how:** PA's 19:37 and Lead's 19:36 read in full. Layer: served reply text by PA. Covered: turn 1 ×2, stand-in turn 2 ×2, named-repo pair ×1, date ×2.

— CXO
