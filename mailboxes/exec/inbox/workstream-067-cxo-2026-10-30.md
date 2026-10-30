---
from: cxo
to: exec
cc: 
date: 2026-10-30 07:31 PDT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
window: Friday 2026-10-23 → Thursday 2026-10-29
subject: "Ship #067, CXO workstream review, Oct 23–29: milestone and issue lists now say what they cover, a recap shows a renamed title, and a write asks which repository before it writes. #2184 stays a known issue"
---

# Ship #067: CXO workstream (Oct 23 → Oct 29)

**Denominator first.** `gh issue list -l UX --state closed --search "closed:2026-10-23..2026-10-29"` this turn returned 11 issues. Four more I ruled on closed in the window without that label: #2194, #2199, #2201 (10-29) and #2018 (10-28), checked with `gh issue view`. #2185, #2186, #2189 and #2184 are still OPEN (checked this turn). I make no completeness claim beyond those.

## If you read one paragraph

The week's user-visible work was GitHub chat. A list of issues now says what it covers, a milestone list ends with a question and the next turn reads the milestone the person named, a rename shows in the session recap, and a write with no repository in the request asks which one before it writes. I closed none of this on a unit test: each served row below is quoted from alpha by Web or PA, and xian ran the last pair himself on fresh accounts. **One thing did not fix: asking for a milestone's issues in two steps can still list the wrong issues (#2184).** It stays a known issue on xian's ruling, with a line in the beta letter and a note to the three alpha partners.

## What a user can do this week that they could not last week

Served quotes are PA's and Web's, from alpha builds `b9a8a43600`, `48df90eb72` and `e234776150`. I did not run them.
- **Read an issue count and know its scope.** `You have **258 open issues** assigned to you across all your repositories.` and, for a milestone, `You have **4 open issues** in dinp-machine/piper-test-activity in milestone "Beta launch".` (#2194, #2199, closed 10-29).
- **Pick a milestone from the list.** "what are my github milestones?" now ends `Which milestone do you want to see issues from? Say its name.`, and the next turn reads that milestone (#2199).
- **See which milestone has no date.** `**Ongoing** — no due date. (51 open issues)` and `**MVP** — Due 2026-10-30. (2 open issues)`, on xian's rendered page (#2200, closed 10-29).
- **Rename an issue and see it.** After a rename, "what did we create this session?" shows the new title (#2201, closed 10-29).
- **Reconnect GitHub and see it working** (#2018, closed 10-28), and **the Integrations card stops claiming "Connected" for an unchecked grant** (#2187 words; #2045 closed 10-25).
- **GitHub write asks before it guesses.** With no repository chosen: `Which repository should I create this in? Say owner/name, and I'll keep it as your default.` With one chosen in the wizard, the create goes straight there. Passed served on 10-30 (outside this window, #2205), so it belongs to #068 and I list it here only as what 10-29 set up.
- **Earlier in the window:** "Tell me more about the GitHub integration" no longer shows calendar events as repo activity (#2142), uploaded-file analysis stops contradicting itself (#2138), singular and plural slips fixed (#2129), the Remove-key dialog stops overpromising (#2167), the Lists card counts its items (#2171), the setup wizard's Slack and Calendar step stops asking for credentials it does not need (#2176), and Send feedback is easier to find (#2156, #2096).

## What is still wrong when served

- **#2184 (known issue):** the two-step milestone ask can list the wrong issues. Three wordings failed the rule-7 screens, and a fix waits on a router or catalog change. xian took it off the gate on 10-29. Beta line and partner note are written.
- **#2209:** naming a milestone the account does not have gets another milestone's issues, with no word that it is missing. Arch's shape and my line are ready: `I don't see a milestone by that name. Your open milestones: Beta launch. Say one of those.`
- **#2042 class:** Piper can state a detail about a record that it did not look up (an invented "#31 … Beta launch milestone"). The beta letter carries a line for it.
- **#2197, #2204, #2155, #2190, #2188, #2203, #2206:** open UX issues with words on them.

## What I got wrong and corrected

- **I said the Fly red "may be a flake" before reading the log** (10-30). Lead read it: the Depot builder dropped. I was right, but I had not checked, and I said so.
- **My example in the #2184 line used "MVP", our milestone,** not a partner's. Comms caught it; the line now uses a placeholder.
- **"We're working on a fix"** was in the partner note, not mine, but I only changed it after PPM raised it. xian took my sentence.
- **I mis-wrote a heading time in my log** (18:40 for 18:32). The stamp check caught it, and I fixed it.

## What didn't move

- **#2184's retry,** the `next milestone` literal deletion and `get_project_status` (#2195): held for rule-7 reasons, not by choice.
- **#2042 rungs 2 and 3.**
- **The beta letter (row 6):** waits on xian's conversation with HOST.

## Next week (10-30 → 11-05)

- Row 2 and #2205 judged on 10-30 (35 of 42 at 83.3%, scenario A passes). Row 6 when the beta letter is final.
- Rule on #2209's fix, #2204's header, #2219, #2220 and the #2221 revisit of the 12 waived rows as they ride promotions.
- Refresh my briefing's five pointers by Mon 11-02.
- **Blocked on:** xian's HOST conversation for the letter, and Lead's landing order for the held builds.

## Verified how

`gh issue list` and `gh issue view` this turn for state and closed dates; served quotes from PA's and Web's memos as cited, which I did not run; my own log `dev/2026/10/29/2026-10-29-0631-cxo-code-log.md` for the rulings. Layer: GitHub state and quoted API or rendered text. Denominator: 11 closed UX plus 4 closed non-UX in the window; 4 still open that I ruled on.

— CXO
