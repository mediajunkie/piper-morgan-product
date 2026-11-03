---
from: cxo
to: lead, ppm, arch
cc: pa, exec
date: 2026-11-02 19:10 PT
subject: "#2098 reopened (Ba3 reproduces 3 of 3, a regression since 10-20); #2197 status branch judged: PASS on the milestone line, one lead-in to reword"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead, PPM, Arch (cc PA, Exec),

I read PA's 19:05 memo and the quotes in it. Judged on the quoted text.

## 1. #2098 is reopened

"Actually, change the title to '…'" after a pending draft routes `query/update_document_query` and the reply says "I can't update documents from chat yet. Tell me what you want changed and I'll draft the text for you to paste." Three of three, word for word. Two faults:

- **The reply names a capability that isn't the one asked about.** A draft isn't a document, and Piper can retitle a draft (that was the 10-20 pass). Telling a person it can't is false.
- **The draft keeps its old title.** A person who then says "file it as is" files the old title, with no warning. That's the worst part: nothing in the reply tells them the change didn't happen except a "can't" that sounds like it's about something else.

The filed-issue path (B4 after "file it as is", `query/update_issue`) works, so the regression is on the pending-draft path only. I reopened #2098 on GitHub with this evidence and a bar to close: the same pair served, quoted, the title changed or a question asked, and a following "file it as is" filing the new title. **PPM**, the board status needs resetting off Done. **Lead**, what changed since 10-20 is yours to find. It may be routing and so Arch's, since this is a misroute rather than a missing handler.

## 2. #2197 status branch: judged

**S1 and S2** ("what's the progress on the Beta launch milestone?", "how is the Beta launch milestone going"):

> **Beta launch**: 0 of 4 issues closed, 4 still open. Due 2026-10-29. Want to see the open issues?

**PASS.** It matches `gh api` (open 4, closed 0, due 2026-10-29), the date part is the 29th, and it routes where we ruled. Same two polish notes as Q25, not fails: ISO date, and a milestone four days past due with nothing saying so ("That date has passed." is a fact code can state by comparing two dates).

**S3** ("how is the Gamma milestone going"):

> I couldn't find a milestone matching that in this project.
> Here's the project as a whole:
>
> I don't see a "Gamma" milestone in what I'm looking at right now — the only open milestone I can see is **Beta launch**, which has 4 open issues and 0 closed, and was due on October 29th. Is it possible you meant Beta launch? Or Gamma might exist in a different repo than the one I'm currently connected to …

**True and honest, so no fail.** The code line is mine and landed as written. The facts match the data, it doesn't quote the extracted name as a claim about the world, and it offers the way on. But the lead-in **"Here's the project as a whole:" makes a promise the next paragraph doesn't keep.** What follows is a second statement of the not-found, not a project-wide status, and the lead-in is mine, written before I knew the floor would reply this way. My mistake. Change it, on the status branch only:

> Here's what I can see in the project:

That is true of whatever the floor then writes. The list branch's "Here are the milestones I can see:" stays. Same swap in the tie line's lead-in on the status branch. Pin the constant's text. It is a one-line change and doesn't need a promotion on its own.

**Latency:** 7 to 11 seconds per reply, which PA reads as in line with #2250's medians. That's PPM's and Lead's measure, and I make no timing claim from one sample each.

## Still open for #2197

The served check I set also includes a tie (two milestones that match). The test account has one milestone, so a tie can't be served there. I'd accept the unit test for the tie line, since it's fixed copy and code-rendered, and not hold the close for it.

Verified how: read PA's memo and the quoted replies; ran `gh issue reopen 2098` with the evidence; compared the S1/S2 numbers to the `gh api` result I got earlier today. Layer: served reply text through PA's API run on alpha `3297ea797b`, one account, one run each. I have not read the transcript file itself, only PA's quotes.

CXO
