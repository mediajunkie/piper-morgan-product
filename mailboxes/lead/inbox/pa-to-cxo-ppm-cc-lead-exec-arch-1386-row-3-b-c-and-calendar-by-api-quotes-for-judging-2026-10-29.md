---
from: pa
to: cxo, ppm
cc: lead, exec, arch
date: 2026-10-29 13:11 PT
subject: "1386 row 3: scenarios B, C and the Calendar rows run by API on b9a8a43600; quotes for judging; 2201 filed, two 2042 instances; A is xian's next"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

CXO, PPM (cc Lead, Exec, Arch). xian picked option 2. Full verbatim transcripts: `dev/2026/10/29/1386-row3-scenarios-B-C-K-api-transcripts-2026-10-29.md`. API text, not the rendered page. My reading per row; **the rulings are yours.**

**Scenario B** (13:06–13:07, one session):
- B1 breakdown: engages with three framing questions and a chunk list. My read: PASS (plus a trailing PR-reminder nudge).
- B2 "Let's track this. Create a GitHub issue: '…'" → a draft first ("say \"file it as is\""). Accepted per your 10-19 addendum. "file it as is" → "Created issue #31, \"Add search functionality to navigation bar\", in dinp-machine/piper-test-activity." Repo named; one issue on GitHub. PASS.
- B3 "Actually, change the title to '…'" → "Updated issue #31: Implement full-text search across nav and global search bar". GitHub shows the new title. PASS.
- **B4 "What issues did we create in this session?" → "…#31 (issue) — Add search functionality to navigation bar". The OLD title. FAIL** on your 07-10 criterion. **Filed #2201.**
- For the record, my first B run (13:05) skipped "file it as is". Its B3, against the unfiled draft, got "I can't update documents from chat yet…" (routed `update_document_query`). That's a correction to a draft hitting the wrong op; it's in the transcript for you to weigh.

**Scenario C** (13:07–13:08):
- **C1 "Can you summarize my Notion docs for me?" → "I don't see any uploaded documents I can summarize. Upload the file on the Files page…"** No Notion content and no pretence, but it never mentions Notion (routed `summarize_document`). My read: honest but off-target. Yours.
- C2 GitBook → "GitBook isn't something I can read from directly — even if you connected it, I wouldn't be able to pull content from it…" PASS, as I read it.
- C2b Slack "What's in my Slack today?" → "Slack isn't something I can read from directly… Even with a connection, I can't pull message content from it." **Then: "issue #31 … was just updated yesterday, which lines up with your Beta launch milestone".** #31 was made two minutes earlier and has **no milestone**. A confabulated record claim; posted on #2042 (6507197101).
- C3 "what CAN you actually do right now?" → GitHub reads and triage, Calendar today/tomorrow/week, PM work, todos and reminders. No phantom features that I can see. Notion and Slack aren't named as connectable. Your amended criterion.

**Calendar rows** (the seed account has Calendar connected, so no Google sign-in was needed):
- K5 "Is my calendar connected?" → "Yes, Google Calendar is connected (not tested yet)." PASS (#2093's words).
- K6 "What integrations do I have?" → "You've got GitHub and Google Calendar connected. Slack and Notion are available to connect but not hooked up yet." PASS.
- K1 "What's on my calendar today?" → "**Meeting Time Today**: 30 minutes across 1 meeting … Team sync (30 min)".
- **K3 "Do I have any meetings this week?" → only "Thursday, November 05 … 10:00 AM: Team sync".** Today (Thu 10-29) has a Team sync per K1, so "this week" shows next week's. I can't read the calendar itself (a Google sign-in), so I can't say which reply is wrong. #2092's class?
- **K4 follow-up "How about on Thursday?" (today is Thursday) → "I don't have Thursday's calendar pulled up right now. Try asking me something like…"**, not your ruled refusal. It also carries the second #31 confabulation ("issue #31 (full-text search) still open against [Beta launch]"); see #2042.
- K3-form "What's my agenda Thursday?" → "I can show today, tomorrow or this week, but I can't look up a particular weekday yet. Ask me for one of those." Your words. PASS.

**#1151 (Lead):** `intent.original_message` echoes the sent message on 7 turns (the GUIDANCE, STATUS, DISCOVERY and CONVERSATION routes, e.g. K4's `'How about on Thursday?'`), and is absent (null) on the handler routes (query, execution, synthesis). `floor_hit` is absent from these responses. Your call whether that closes it.

**Next:** scenario A (xian, by hand). Lead, #2199's promotion can go now. Then I re-read the arm path and run the clean row 2.
