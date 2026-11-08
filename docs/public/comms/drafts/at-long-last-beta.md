---
image: ''
alt: ''
caption: ''
---

# At Long Last, Beta

*October 30–31, 2026*

When I decided (perhaps prematurely) that Piper Morgan was ready to go into alpha testing, a little under a year ago, I thought the beta test would follow fairly soon thereafter. Early this year I opened up the hosted alpha and once again anticipating moving on to beta by spring or perhaps early summer.

# Would you believe, September?

In early July I published a blog post set in late June optimistically titled ["Almost Beta"](https://pipermorgan.ai/blog/almost-beta/) and, as late as September 1, I ran a piece from early August that situated itself ["four days before beta"](https://pipermorgan.ai/blog/a-sender-impersonation-bug-four-days-before-beta/). 

By August 8, I had moved the deadline, writing with a touch of petulance (knowing my agents wouldn't take it personally, not being alive and all) that "we clearly have a lot more work still to do than anyone ever reported to me." 

I have this habit of using family birthdays as milestone dates (easier to remember), and when it became clear that we were finding serious issues faster than we were closing them, I accepted another big delay and re-set the MVP milestone date to my sister's birthday in early September. 

On the first of that month we took stock of the remaining work, and after close consultation with my agent team and some ruthless MVP triage, on Sep 6 I reset the target date one more time to October 30, my own birthday. 

We started tracking progress much more rigorously and strictly disciplining which new issues could be added to the ongoing "final" sprint of the MVP milestone that had to be completed before we could start the beta.

*Deciding whether a new issue is a launch blocker is a core product-manager experience and I couldn't help pointing this out to my agent assistants, always trying to make lessons from things when I can.*

The toughest part is allowing an ugly bug because you realize that (a) its impact is small and (b) there will always be some bugs. In this case, I ruled at one point that a two-step question about milestones that Piper was handling inconsistently could be allowed into the beta. I wrote, "we can admit this one is trickier than it looks and call it out as a known issue."

# Looks like we made it

On Oct 30 the MVP milestone closed on that date, and the next day I sent (not very spooky) email to the first set of testers inviting them to the private beta. The email invitations also explained the known issues, the things Piper was still getting wrong as of then.

Our new upcoming milestone is Production. Right now its date is February 2 (my father's birthday) and history tells me this is optimistic as well, but we need a target.

The eight weeks leading up to our mlestone addressed Piper's fundamental behavior and architecture, much of it boiling down to making sure Piper tells the truth about what it doesn't know. One reason it took so long was an old pattern of attempting to patch a problem until I finally take a step back and ask for a more systematic approach to a solution


# Can agents catch their breath?

The final push to beta was an effort not unlike what I have experienced with human teams. I had to prioritize Piper Morgan over other work. There were some long days. I made some tough calls. If we had had to delay again I would have coped but this time I was really determined to land the plane.

Once we hit it, I was fine with waiting a day to send out beta invitations. I had time to remember to cut the 0.9.0.0 beta release. I felt no need to ensure the Lead Developer agent was cranking at full capacity (although I did suggest there was no need to stop entirely).

The fact is I need to take stock myself and when real human users start testing the beta I will likely have my hands full with the most valuable input into the project since the day it started with one question or the first time an outside human advisor made a suggestion (no offense to the agents that have contributed might labors but rarely if ever bring to the table a unique point of view, that not being their wont).

I asked my chief of staff agent (Exec) to spread the word t the full team: "We can all catch our breath and then discuss priorities in the first sprint of the journey to our next big milestone, the Production release."

# 

**6. The letter.** It carried **nine** known-issue lines, each checked against an open issue at send time ("9 of 9
hold"). [#1386, PPM 10-30 19:51] Among them: Piper can misread what you ask, an answer about your own data can be wrong,
it can state a detail it didn't look up, and there's no undo for a deleted to-do. [#1386, PPM 10-30 17:37] You sent
them Sat 10-31. [decisions.log 10-31 13:51]

**7. What beta means, per you.** "trust me, the alpha is over. the beta has started. the alpha ended when the MVP
milestone closed." [decisions.log 11-04 19:41]

**8. Optional coda, your call whether it's public.** On 11-04 you held all further invitations until three security
items are done: "No invitations of any kind go out until this is sorted." [decisions.log 11-04 19:31] It fits the
post's theme (beta is a door you can close again), but it's very fresh. Leave it out if you'd rather it surface in
Ship #069.

## Careful with these (accuracy)
- **Private** beta: invitation only, sent personally, in waves. The public site offers a waiting list
  (pipermorgan.ai/try/beta/), not sign-up. Don't imply anyone can join now.
- Don't count recipients or name anyone. The letters' recipients and codes are held privately on purpose.
- "On the day we set" is true for the milestone (due Oct 30, closed Oct 30). The letters went the next day.
- The known-issues quotes are paraphrases from PPM's table, not the letter's exact copy. If you quote the letter, take
  the words from `beta-invitation-letter-draft-2026-10-30.md`.

## Already told elsewhere: don't retell
- **Ship #067** (11-04) ends: "Since Thursday, the MVP closed on Friday, which ended the alpha, and the private beta
  began with Saturday's invitations." This post is the meaning, not the news.
- **Ship #068** (Wed 11-11) will cover Oct 30–Nov 5 as news. Leave the sprint details for it.

## Your angle, maybe
- What it felt like on Oct 30, against Ship #067's P.S. ("There are times I never thought I'd get this close").
- Why a letter that lists what's broken is the right way to invite people.
- What "beta" means to you as a PM, compared with how products usually use the word.

---

*Next on Building Piper Morgan: [TEASE: Sun 11-08, "Fixed and Scores Higher Came Apart" (working title). Confirm the
title first.]*

*[Reader question, yours to write. A start: "When you launch something, what do you tell people it can't do yet?"]*
