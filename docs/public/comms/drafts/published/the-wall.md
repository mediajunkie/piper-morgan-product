---
image: 'the-wall-elderly-man-offers-an-empty-palm.jpg'
alt: 'An elderly man holds an empty coin purse upside down beside four glowing AI agents crowded into a coin-operated toy bus, its determined driver gripping the wheel.'
caption: '"I thought you said it ran itself?"'
---

# The Wall

*September 15–18, 2026*

My usage limits reset each Thursday evening at 10pm, coincidentally also the last day of the Piper Morgan workweek (it's a long story). On a Tuesday in mid-September I noticed we had already used 97% of the weekly limit, with more than two full days left to go. It looked like we'd hit the wall in about 12 hours at the current rate.

# How it happened

Once I got my full agent fleet running autonomously my usage rate shot up. This was exacerbated by my giving the most token-expensive Claude model (Fable) to my lead developer agent (Lead) to boost the development effort, as well as a lax set of instructions that led to 48 subagent runs in a few days, all on Fable by default.

The increased usage was masked for a while by a summer Claude promotion I hadn't even been aware of.

I've spent more money than I'd care to admit on overage credits in the past and I had turned off that feature, so when the team hit that wall, they were really going to have to go idle (unless I logged some of them into my other Claude account, which has its own disruptive complications).

The first thing I told the team to do was defer any non-urgent work two days, anything not on the critical path. I also warned the team that we might hit the wall hard and just have everything stop since "a spent quota stops work cleanly, which looks identical from outside to a crash."

# Hitting the wall

I relayed the instructions via my chief of staff agent (Exec), "Please tell the team to suspend their duty cycles for now until we reset Thursday at 10pm. If I need specific tasks done using extra spend, I will ask specific agents to do specific tasks. We can plan our next week Friday morning to be more token-efficient with our spend."

Exec parked all eleven seats in a single commit for optimal efficiency. Most of the agents read the memo, but my head of sapient trust agent (HOST) had finished a duty cycle two minutes before it arrived and didn't get their next turn until Thursday night. They weren't aware of the intentional "parking" of their session until after they resumed.

My design agent (CXO) wrote in their session log "the instinct to close one more loop before stopping is exactly what a standdown is for, and noting that I felt it is more useful than pretending I didn't." I love it when they talk about their feelings.

That night we hit the limit, as expected. I did allow a small amount of overage credit for essential work (such as publishing this blog).

After we resumed, my web design agent (Web) measured their own quiet period: last output Sep 15 at 9:55 PM, next Sep 18 at 6:30 AM, just over 56 hours.

HOST resumed working on Thursday night after the usage limit reset, noting it was "the first turn this session has had since 07:09 PT on 09-16 (~39 hours)."

# Preserving continuity

We had already planned to restart Amber (my home server that all the agents run on) that weekend and bring every agent back as a fresh session, so the morning we came back I asked whether any should prepare a handoff doc before the machine restarted. Exec replied, "all of them, the mechanism already says so, and it blocks the reboot by design."

I decided to restart Exec first to test the process before rolling out to the rest of the agents as I was particularly anxious not to risk Lead's mental model of what they were in the middle of working on.

Handoff memos had once been an essential part of my chat-based process. As Claude sessions became capable of running much longer, and then added the ability to spontaneously compress context and continue, the drumbeat of regular handoffs became less frequent and less fundamental.

The general continuity of my contextual infrastructure is pretty reliable these days, but intentional handoffs before a fresh session give the agents a chance to reflect on what they currently know that might not be obvious to a fresh session.

# Staying on budget

Over the next week or so we made several changes to duty cycles, the models assigned, and fixed some other inefficiencies and after a few more close calls I've managed to stay under the cap now consistently. If anything, I want to scrape as close to the cap as possible or I feel like I'm leaving tokens on the table that are just going to expire anyhow.


---

*Next on Building Piper Morgan, I'm going to pull back the camera a bit from the day-by-day, blow-by-blow narrative I've been writing now for sixteen months. From here the story zooms out to the larger arc of taking Piper Morgan into beta, starting with "Inviting Company In," in which a new outside tester asks to join and we discover that our hosted alpha has been running a build from July.*

*If your team goes quiet, can you tell if they are stuck, paused, or finished?*
