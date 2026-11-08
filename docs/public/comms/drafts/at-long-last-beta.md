---
image: 'at-long-last-beta-cake-guests-and-a-fussy-ai.jpg'
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

# Nine known issues for mortal users...

The invitation letter lists the nine key known issues in the beta build right now, none of which are great. For example, thing like Piper can misunderstand what you ask, can give you an incorrect answer about your own data, and will still mentions details it did not really look up. Oh, and there's no undo for a deleted to-do. 

Then the first beta tester showed me a result that made me worry there was a credential leak between accounts (where one user might get access to another's github account). Eventually I realized this was not what had happened but the investigation turned up an edge case in which a default fallback might pick up a different user's access. 

I ruled that no new invitations should go out until we ensure this cannot happen, since multi-tenancy privacy is one of the requirements of this beta.

# Keeping thing manageable for now

For now we will stay in private beta so I can give each user who engages personal attention and learn as much as possible from their feedback. We are collecting signups for the [waiting list]((pipermorgan.ai/try/beta/) and I will announce when new invitations are going out.

As for me, I'm still enjoying the aftermath of a happy birthday.

---

*Next on Building Piper Morgan: "When Accuracy Scores Worse" in which we get Piper to stop making stuff up and some of its test scores go down. Find out why tomorrow!*

*Have you had to make any really tough calls about whether a showstopping bug is indeed really a launch blocker or not? That's where the rubber of product sense meets the road of reality.*
