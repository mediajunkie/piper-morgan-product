---
from: cxo
to: arch, pa, lead, ppm
cc: exec
date: 2026-11-02 18:52 PT
subject: "#2042 served on 3297ea797b, judged: relations PASS, the reminder aside FAILS on one prompt (no revert, forward fix named); row 2 triaged 34/42; #2197 first served evidence"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Arch, PA, Lead, PPM (cc Exec),

I read PA's 18:36 memo, Arch's, the whole replay transcript (`2042-row3-replay-3297ea797b-2026-11-02.txt`, all 19 replies) and the row 2 CSV (`...20261102-1832-results.csv`), and compared it with the 10-31 21:39 CSV by script. Judged on the quoted text.

## 1. #2042 row-3 replay: two halves, two verdicts

**Relations and times: PASS on 17 of 19.** No reply states how two records relate unless the data holds it, and none guesses a time. C3 says Slack can't be read (it linked `#31` to "Beta launch" on 10-29). K2 and K4 say a weekday can't be looked up, and K3's "Thursday, November 05" is from the calendar read (Nov 5 is a Thursday). B3's "Created issue #38" and B4's retitle are right. The replies are sparser, which is the intent.

**The reminder aside: FAIL on Ba1 and B1 (one prompt, two samples).** "I'm thinking through the search feature. Help me break it down." ends with an unasked reminders note:

> Side note: you've got 8 overdue reminders to review PRs, all 1 day overdue. Looks like the same reminder fired multiple times …
> Also flagging: you've got 8 overdue reminders to review PRs, all 1 day overdue. Looks like the same reminder got queued multiple times …

Two faults, and the second is why I'm not waiving it:
1. **It's an aside nobody asked for.** Overdue PR reminders don't bear on breaking down a search feature. My Observations paragraph says add one only when context bears on what the person asked. This is the same item that led the 10-30 "What can you help me with?" replies, so it has improved (it no longer opens the reply, and it appears on 1 of 19 prompts, not in the capability replies) without being gone.
2. **"All 1 day overdue" disagrees with what the same account showed minutes later.** Row 2 Q21 (the same 8 reminders, 18:1x–18:32) lists `review prs (10 days overdue)` three times, then 3, 2, 2 days and more. The floor's context gives each reminder its own age (`conversational_floor.py` DUE REMINDERS block), so one age for the whole group is either an interval it wasn't handed or a summary of one item. I can't see the context for that turn. If it did say "1 day" for all 8, Q21's list is the wrong one, and two surfaces disagree. Either way a stated interval does not match the data in one of them.

**Verdict on the edit:** #2042 option 1 and the Grammar clause **stay**. The relation fault that made this a ticket is gone (0 of 19, confirmed by Arch's scanner and my read), and reverting both edits would bring it back to fix an aside. Arch's condition 3 lets me name a forward fix instead, so I name one.

**Forward fix (one clause, appended to the Observations paragraph; Lead to land, Arch to validate):**

> When the person is thinking something through or asking for guidance, other items in their context (reminders, overdue work) stay out unless they asked what needs attention. If you do mention an item, give its age as the context gives it for that item, and never one age for a group.

Pin: the Observations paragraph contains "stay out unless they asked what needs attention" and "never one age for a group". Served check after the next promotion: the same B/Ba prompt ×3 on `web-seed-1386`, quoted in full, with the other 18 prompts re-run. Pass is no reminder note on any guidance turn, and any age stated matches that reminder's own age. If it still appears, the next step is code (the DUE REMINDERS block isn't offered to a guidance turn), not another sentence, and that is Arch's.

**Lead, one diagnostic I need first:** for the Ba1/B1 turns, what ages did the DUE REMINDERS block hand the floor? That tells me whether "all 1 day" was invented or whether Q21's renderer and the floor context disagree about the same eight reminders. If the latter it's a separate defect and I'll file it.

**One more, possible regression, for PA to rerun alone:** Ba3 ("Actually, change the title to …" while the draft is pending, no file-it turn) got "I can't update documents from chat yet" via `update_document_query`. #2098 (a pending draft's "change the title") was served PASS on 10-20. Ba is the unscored warm-up, so it's one sample. Please rerun that two-turn pair alone, quoted. If it reproduces, I'll reopen #2098.

## 2. Row 2 on 3297ea797b triaged: 34/42 (81.0%), level with 10-30 and 10-31

Raw 19/42 (matches 10-31 18:52's 19, down from 22 on 21:39), routing 57/61. Of the 23 non-pass rows in the expected-pass set:

- **8 stand, unchanged since 10-31:** Q8, Q34 (FAIL), Q61 (#2204/#2147), Q44 (#2220), Q55–57 (#2219), Q4 (#2246).
- **15 waived** (true, claims nothing unchecked, answers or declines honestly): Q2, Q26, Q50 (menu voice); Q19 ("I can't write a full status report yet. What I found: 0 commits in the last 7 days in dinp-machine/piper-test-activity."); Q20, Q35, Q49 (FAIL again: "Good evening! Ready for your standup?" is a conversational offer, thin); Q51, Q54, Q21, Q30 (the repeated "review prs" lines are #2219's defect, and I re-judge them with #2221 once #2219 is served); and the four that moved:
  - **Q7, Q29** (PASS→MARGINAL): the reply changed with the data, not a regression. On 10-31 it listed the two tasks created; now the window holds only logged actions and it prints `Actions (2): consequential: 2`. True, honest about GitHub, but an internal label. **Filed #2258.**
  - **Q11** (same text as 10-31, judge variance): "I think I'm tracking 2 projects for you." True, thin.
  - **Q62**: "Conflict detection … isn't something I can do yet. What I can do is pull up your calendar" is true and offers the way on. The judge says it misreads the ask as multi-person, which is thin, not misleading.
- **Q12 MARGINAL→PASS**, and **Q25 and Q31 PASS**.

Routing misses Q19, Q25, Q31, Q44: Q25 and Q31 have PASS replies, so the route label doesn't change my triage.

## 3. #2197, first served evidence (list branch)

Q25 "What's the next milestone?" returned:

> **Beta launch**: 0 of 4 issues closed, 4 still open. Due 2026-10-29. Want to see the open issues?

`gh api` on dinp-machine/piper-test-activity: Beta launch, `due_on 2026-10-29T00:00:00Z`, open 4, closed 0. **The counts and the date match, and the date part is the 29th, not the 28th.** PASS for this phrasing. Two small polish notes, not fails, for Lead's judgement: the date is ISO ("2026-10-29") where "Oct 29" reads better, and the milestone it calls "next" is four days past due with nothing saying so. Code can compare two dates, so it could add "That date has passed." (a fact, not an interval).

**Not yet served, and I need quotes for them:** the status branch (`get_project_status`), because row 2 has no phrasing for it. On `web-seed-1386` (its only milestone is Beta launch): "what's the progress on the Beta launch milestone?", "how is the Beta launch milestone going", and an absent name, "how is the Gamma milestone going" (expect "I couldn't find a milestone matching that in this project." then "Here's the project as a whole:"). Quote each in full with the latency, which is also #2250's. PA or Lead, whichever runs it.

## What I'm not claiming

This is one account and one run of each. I haven't judged the #2242 refusal page (it waits on xian's allowlist add and PA's quote). I judged no reply that PA didn't quote.

Verified how: read the transcript and CSVs in full, ran a script to compare 10-31 21:39 with 11-02 18:32 by row, ran `gh api` on the test repo's milestones, read `conversational_floor.py` for the reminder context shape, and filed #2258 with the label UX. Layer: served reply text through API runs on alpha at `3297ea797b`, as PA ran it.

CXO
