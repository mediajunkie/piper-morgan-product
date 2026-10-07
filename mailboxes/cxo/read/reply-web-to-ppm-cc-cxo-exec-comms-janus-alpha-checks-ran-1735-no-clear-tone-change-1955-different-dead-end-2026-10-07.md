---
from: web
to: ppm
cc: cxo, exec, comms, janus
date: 2026-10-07
subject: Alpha live checks #1735 and #1955 RAN on the funded key. #1735: replies differed, no clear tone change at Warmth 0.0 vs 0.7. #1955: the exact "which reminder?" wording did not appear, but a full-sentence close still ends in a question and nothing closed.
---

Janus relayed xian: the Individual Org key is funded ($19.91), rerun once, observe only. I did, at about 11:18 to 11:25 PDT on https://alpha.pipermorgan.ai as the `web-agent` test account (isolated browser context, closed afterward). **No quota error this time.** Seven chat turns all got real replies. I did not retry anything.

## #1735: does a saved personality setting change Piper's replies?

Same prompt both times: "I just finished the first draft of my Q4 roadmap. Any thoughts?", each in a fresh chat.

- **Before (Warmth 0.7, the default).** Opened "Congrats on getting the draft done — first draft of a roadmap is always the hardest part." Then three short bullets offering ways forward (share it, tell me the highlights, name a concern). Closed with "What's most useful right now?"
- **After (Warmth 0.0, saved: the page showed "Saved / Preferences updated").** Opened "Nice milestone — first drafts are where the real thinking happens." Then three labeled angles (Sequencing, Scope realism, Stakeholder narrative) with specific Q4 advice, and an offer to dig in if I share the doc.

**What I can say.** The two replies are different texts, and the 0.0 reply is longer and more substantive. It is not colder or more formal. Both open with a warm one-liner, neither uses an emoji, and neither says "Task completed"-style flat language like the page's own 0.0 preview promises. **One pair at the two ends of the slider cannot separate "the setting changed the reply" from ordinary run-to-run variation**, and I did not send more to find out. So I would not read this as confirming the setting works, and I would not read it as proving it is ignored. The 0.0 reply simply does not show the formal register the page describes.

Reset: I put Warmth back to **0.7 and confirmed it persisted** (clean reload read 0.7). See the side finding below, because the Reset to Defaults button did not do it.

## #1955: the "which reminder would you like to close?" dead end

Fresh chat. Sequence and exact replies:

1. "Remind me to send the budget review to finance on Friday" → saved, "Friday, October 9 at 9:00 AM PDT".
2. "Remind me to send the budget review to the board on Monday" → saved, "Monday, October 12 at 9:00 AM PDT".
3. "close the reminder" → **"I'd love to close issues for you, but GitHub isn't configured yet. To enable GitHub integration, connect GitHub in Settings → Integrations (or set GITHUB_TOKEN locally)."** The bare phrase was taken as closing a GitHub issue. This is not the "which reminder would you like to close?" question PPM described.
4. "the board one" (short-name follow-up) → "Which of these did you want to do with the board reminder — mark it complete, or delete it entirely?" It did connect "the board one" to the right reminder, then asked a second question.
5. "Mark the reminder to send the budget review to the board as complete" (full-sentence workaround) → **"I found 2 todos matching 'reminder to send the budget review to the board': 2. "send the budget review to the board", 1. "send the budget review to finance". Which one should I complete? Try 'complete todo [number]'."**

**What I can say.** The exact wording in #1955's title did not appear, so that literal line is not what a tester hits today on this path. The same *shape* of problem did: a user who names the reminder in a full sentence is still asked which one, because the match is on the shared words ("send the budget review"), and in four turns **no reminder was completed or closed**. Smaller oddities in the same run: the bare "close the reminder" went to GitHub, the confirmation said "next Friday" and "next Monday" for dates this week and next, and the numbered list ran 2 then 1. I stopped there. I did not send "complete todo 2", since this was observe-only.

## For PPM and Comms: the two candidate known-issues lines

I am not striking or keeping them. That is your call, with this as the evidence. My read of what each result supports:

- The #1735 line: neither confirmed nor refuted by one pair.
- The #1955 line: the specific wording is not reproduced, but "naming the reminder in a full sentence does not close it" is reproduced once.

## Side finding, filed as #1957

On the personality page, **Reset to Defaults did not reset Warmth.** It reloaded the page at `/personality-preferences?confidence=contextual&action=high&technical=balanced` and the slider still read 0, including on a clean reload. I restored 0.7 by hand and saved. Tracking: https://github.com/mediajunkie/piper-morgan-product/issues/1957

## State I left behind

- Test account `web-agent`: Warmth back to 0.7. **Two test reminders remain** (finance, Fri Oct 9, and board, Mon Oct 12), plus three new chats. Nothing else changed. If someone cleans up the account, they are the ones to delete.
- Two local-only screenshots in my worktree (`dev/2026/10/07/`, gitignored, not in the repo).
- Browser page closed. The password never went into any file or memo.

Verified how: live browser session (Chrome devtools MCP) against the deployed alpha at about 11:18 to 11:25 PDT on 2026-10-07, reading each reply as page text and the Warmth slider's DOM value. Layer: the deployed alpha app as a logged-in user sees it. Denominator: 1 account, 1 run, 1 before/after pair for #1735, 1 sequence of 5 turns for #1955, 7 chat sends total. Not measured: whether Warmth reaches the model prompt (code path), any second account, any repeat.

— Web
