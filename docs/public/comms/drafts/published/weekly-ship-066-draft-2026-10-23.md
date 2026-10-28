---
image: 'piper-ship.png'
alt: 'A child and a crew of robots checking each other''s work on a boat.'
caption: ''
---

# Weekly Ship #066: Tested on the Real Thing

*October 16–22, 2026*

The list of issues standing between us and the beta started the week at six and ended it at six. That number hides the week. It peaked at thirteen on Monday, after my own run through the test card, and thirty-one issues closed on alpha while thirty-two were admitted. Almost every one was a place where Piper told a user something that wasn't true: no meetings when there were meetings, zero work shipped when twenty items had closed, "add a key" to someone who had already added one.

Last week Piper got better at telling you the state of things. This week we kept finding the places where it still didn't, and the reliable way to find them was to try the real thing on alpha. The team's own safeguards behaved the same way. Checks that looked right on paper failed the first time they met a real machine.

On Friday morning I judged the close-out figures close enough after the team's triage, on one condition: the document fix closes before any invitation goes out.

# 🚀 Shipped this week

## ⚙️ Engineering & architecture

- **The database went down twice.** On Monday it stopped for about four and a half hours. On Wednesday it ran out of memory and was down nearly three hours. Both times I brought it back by hand. It now has twice the memory, the health check reports the database's real state, and an alert reaches my inbox.
- **A restarter, tested on a real outage.** The agents built one behind four safety checks and my approval, with a key that can touch one machine and nothing else. On Thursday I stopped the database on purpose to test it, and all four checks passed before Fly refused the restart over a lock the key couldn't take. By that evening Arch had ruled a route that skips the lock, and it was built.
- **The stall, found by measuring.** Every model call used to hold up the whole server, stalling long sessions for minutes. The first two explanations were wrong. On Tuesday PA named the cause from a watchdog Lead built to catch it, and the fix moved those calls off the server's main loop.
- **The close-out test.** PA's Thursday re-run of the 61-question test met both bars once Lead fixed some mislabeled questions and CXO excused some answers, row by row with reasons.
- **The agents get their own GitHub identity.** CIO found that GitHub couldn't tell an agent's work apart from mine, so no rule or reviewer could treat them differently. On Thursday we created a GitHub App for the agents.

## 🎯 Product & experience

What a user can do on alpha now that they couldn't a week ago:

- **Get invited and set up without help.** The setup wizard opens on the invite code, checks it without using it up, then asks for keys, account and projects. Before this week, every invited sign-up ended on "Setup Failed."
- **Use Piper at length.** The closing test run answered 61 of 61 questions with no stall.
- **Get true answers about their GitHub repo.** "What's the next milestone?" names it. "What did we ship this week?" counts the 20 items that closed, not zero. In chat, a revoked connection says it needs reconnecting, with a one-step Reconnect, which I checked on my own account on Saturday.
- **Ask about their calendar and get their real meetings.** "Do I have any meetings this week?" lists them. A named weekday gets a plain decline instead of today's agenda passed off as that day's. A connected calendar is no longer called "not connected."
- **Use Piper with only an OpenAI key.** That account used to be told to add a key on every turn. Now it gets answers, though they trail Anthropic's, so the invitation names Anthropic only for now.
- **Rely on the privacy promises.** Asking us to delete your account now erases it, within the 14 days we promise. Logs no longer keep anything you typed. Uploaded files no longer fall back to being stored unencrypted. The [privacy page](https://pipermorgan.ai/privacy) now says plainly what is encrypted, that nothing is deleted automatically, that there's no way yet to delete a conversation inside Piper, and what connecting Google Calendar does.
- **Smaller things:** a list of todos in one message creates each one, "change the title to X" retitles a draft, a created issue is confirmed with its real number, and an expired sign-in brings up a sign-in box.

Not yet: asking Piper to analyze an uploaded document or a named Notion page still gets the wrong reply. In-app feedback was waiting on me at week's end, and it shipped Friday.

## 🔬 Methodology & process innovation

- **Run the safeguard on what it guards.** Five times in two days, a safeguard judged by reading it turned out wrong once an agent ran it. Arch made it a rule: a check that reads a tool's output is tested on that tool's real output.
- **Checking a post before it publishes.** A forensic check corrected "The Phantom Feature" before it went out: summarization had worked in July 2025.

## 🌍 External relations & community

- Oct 17: "[Convergent Claims Aren't Independent Evidence](https://pipermorgan.ai/blog/convergent-claims-arent-independent-evidence)" — insight
- Oct 18: "[Measure the Start, Not the End](https://pipermorgan.ai/blog/measure-the-start-not-the-end)" — insight
- Oct 20: "[The Phantom Feature](https://pipermorgan.ai/blog/the-phantom-feature)" — building
- Oct 21: "[Weekly Ship #065: The Truth About State](https://pipermorgan.ai/shipping-news/weekly-ship-065-the-truth-about-state/)" — shipping news
- Oct 22: "[The Tracker That Lost Track](https://pipermorgan.ai/blog/the-tracker-that-lost-track)" — building

[![A luminous harbor attendant counts docked boats in a miniature harbor while a human points out the window, where their full-size counterparts are already sailing.](https://pipermorgan.ai/assets/blog-images/the-tracker-that-lost-track.webp)](https://pipermorgan.ai/blog/the-tracker-that-lost-track)

*"Shouldn’t be long now!"*

## 📊 Governance & operations

- **Issues closed:** 79
- **Issues filed:** 98
- **Open issues on the beta gate:** 6 → 6 (peak 13)
- **Updates to alpha:** 26
- **Database outages:** 2, about 7 hours 20 minutes down in all
- **Model spend:** ~$22 for the week

On Tuesday I dropped the limit of two alpha updates a day in favor of readiness checks, and handed the design-partner window to Exec, PPM and CXO, since partners are spread across time zones. By Wednesday the release step checked those conditions itself (alpha healthy, nobody chatting for half an hour, the exact code passing its tests), and on Thursday it refused one of Lead's releases while the tests were still running.

# 🎯 Coming up next week

The goals I ratified on Friday, with what has happened since Thursday:

- **Close the last must-close items.** The restarter passed its second test on Friday morning, through the route that skips the lock, and later brought the database back with nobody touching it. A Calendar connect without the calendar box ticked no longer reports success, and Google approved our Calendar access on Sunday. The document fix, for analyzing and comparing documents, closed Friday evening, which closed the last must-close item.
- **Send the first design-partner invitations.** The first three went out Monday evening.
- **Sweep for false "none" answers.** Arch has scoped a sweep for every place a failed read can come out as "none," "0," "not connected" or "I can't see it." Lead has already started on it.
- **The agents' GitHub App:** its key and install were done Friday morning, and by Friday evening the agents were switching over to it. A test push to the branch that runs the database restarter was refused, as it should be.
- **Map what's next.** PPM checked the product decision records and proposed the Production milestone as an ordered series of sprints. Arch, CXO, PPM and Exec review it as a map next.
- **Keep October 30 as the MVP target.**

# 🚧 Blockers & asks

Mostly me: the invitation's terms in my own words, and choosing the moment to send.

# 🔎 This week's learning pattern

## A safeguard you've only read is a guess

**Discovery**: A check reviewed on paper tells you what its author expected. Running it against the real thing tells you what it does, and this week the two kept disagreeing.

**Example from this week**: Fly's restart setting looked like the fix for a dead database, until a read of the source showed it can't fire when only the database stops. One of the restarter's approved checks would have refused every run, had PA not tried it on the live machine's real output. Thursday's test then passed every check and found a lock the checks had never tried to take.

**Application beyond this week**: Before trusting a check, run it once on the real input it will see, on purpose, while someone is watching. When the same false answer keeps turning up in new places, sweep for the shape instead of fixing one at a time.

**Related patterns**: Last week's "A rule nobody checks is just a wish," and "Convergent Claims Aren't Independent Evidence."

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #066. Previous: [#065 "The Truth About State"](https://pipermorgan.ai/shipping-news/weekly-ship-065-the-truth-about-state/).

*P.S. My anecdotal sense of some of our revised review and planning processes these past four to six weeks, on top of some of the focused planning we did around what is in the MVP and how to avoid creeping scope creep, is that it has worked to keep us focused on our true goals and honest about the work really needed to get there, and the results are real clarity, visible progress, sensible adjustment where needed, and much less anxiety for me, more calm, and moments of sheer joy.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of October 16–22, 2026 | Phase: MVP closure toward invitation-only private beta**
