---
image: 'the-trust-architecture-hardens-city-wall.png'
alt: 'A newly completed medieval city wall encircles a peaceful town as relaxed watchmen patrol above and a mason carries away his tools, illustrating how careful design can replace constant vigilance.'
caption: '"I haven''t shouted ''''Look out!'''' all week"'
---

# The Trust Architecture Hardens

*June 15–19, 2026*

Over a five day stretch the team made three architecture decisions and then closed a sprint. In between, the team fixes its own working process, finished a months-long visual redesign, caught a fabrication bug before I could act on the wrong answer, and survived a battery outage that killed every autonomous process running. Along the way, it started to feel like one team getting harder to fool, and less likely to fool itself.

# Three decisions and a catch

On Monday the chief architect role (Arch) made a ruling on when if ever data should be allowed to "leak" between accounts. The answer allowed that certain product-management records are deliberately global by design, and that any exception to default rules needs an explicit marker, not an unspoken assumption. That ruling unblocked a new Architecture Decision Record (ADR), the team's format for writing down a significant technical decision and its reasoning: ADR-071, "User-Auth Anchoring Pattern for Content Stores," drafted the same morning and ratified by early afternoon. 

It joined two others from the same five-day window: ADR-070, on how the product connects to outside services, and an updated ADR-066, on keeping configuration state honest. Read together, all three make the same argument in different ways: a system shouldn't assert a fact about itself, a user, or a connection it hasn't actually verified.

The reason we needed to examine this rule is that Piper Morgan evolved from a personal project, to a side project, to something built to accommodate any number of users and instances. Along the way, the user model was refactored more than once, but never thoroughly enough. 

Auditing which parts of the data layer already anchored records to the right owner, the lead developer role (Lead Dev) initially reported "about half the tables are unanchored" which turned out to be a scarier number than the truth. Before looping in Arch for review, Lead Dev re-checked its own claim, found the real problem was three inconsistent styles of anchoring in use rather than anchoring being missing (another type of problem entirely), and corrected itself before anyone else saw the overclaim. Arch's response, reading the correction, was blunt: "the discipline at its best." (As a human, though, I notice this tendency of agents to report on things that were wrong and then corrected, which can create noise and even confusion in later records,  but that's a topic for another day). The point is, an agent catching its own mistake before it becomes someone else's problem to catch is exactly the kind of moment I want more of.

That same day we also closed out two pieces of the shared design system that had been sitting as "planned work, not yet done" for weeks: a reusable dialog component so pop-up confirmations stop being chintzy-looking native browser prompts, and a linter that ensure interface colors come from the approved palette.

# Fixing how we work, not just what we build

The next day I noticed a problem with the new duty cycle process the team has been using: a scheduled wake-up where an agent checks in, does whatever unblocked work it can find, and goes back to sleep. The intent was always: do everything you can until you are entirely blocked waiting for responses or out of assignments entirely. In reality, several agents, including the chief innovation role (CIO) that ended up fixing this problem had started saying things like "this deserves a more focused pass" as a polite way of deferring work that was just sitting there, unblocked, ready to go. This tendency to autonomously decide not to work on an assignment drives me nuts! I caught it mid-session and said so plainly: banking work under a vague "no rush" is itself the antipattern. Shyness isn't a virtue when the queue is empty and the work is yours to do.

The fix was to make the rules clearer: a fire is a wake-up, not a time box, and a commit isn't a stopping point. If you really do need to defer something, the defer needs an explicit, nameable trigger and approval, not a vague sense it deserves better attention later. CIO wrote this into the shared operating procedure and broadcast it to eight other inboxes the same day. A background sweep of the prior weeks' logs found the pattern real but modest, a few agent-hours a week across the whole team, and, more usefully, found it wasn't always this seeming synthetic model of laziness. Sometimes it was good judgment (some deferrals really were correct) but with no standard for how to decide. Now there's a rule.

# The gradual redesign finishes

The day after that the team finally addressed a longstanding thorn in my side. Piper Morgan's web interface has had a really clunky design. The first version was pretty much vibe-coded: a "good enough" chat UI I'd be embarrassed to show even my friends who don't workin tech. Occasionally I made partial efforts to clean up the design or fix the most egregious annoyances, but I knew I was not handling design correctly, let alone systematically.

After months, different pages of the product had accumulated their own slightly-different visual chrome, navigation bars that looked almost, but not quite, the same from page to page.  Finally, Lead Dev finished migrating the last of them onto one shared shell: twenty-two of twenty-two page templates, all pulling from the same navigation, the same footer, the same structural frame. It had been "in progress" long enough that finishing it felt like an event worth celebrating. Someday I may put together a timeline of how the interface evolved, with June 17 marked as the day I stopped cringing about it.

The same day, another architecture design record (ADR-072), on how the product determine which internal skill or procedure to route a request to, went from idea to ratified reality over the course of a nine-hour stretch: authored, reviewed by two other roles for its trust implications, and formally accepted, all under real pressure from me to finish it rather than let it sit trapped in the limbo of "important but not urgent." 

Arch had banked the plan to draft it, classifying it as unhurried background work, given there was no hard deadline provided. I gave it a deadline: do it now. Fortunately, the groundwork was already solid and Arch had done its homework reading, so demanding action just moved up writing-down from "eventually" to "today."

The team made one other correction that day to how the product thinks about trust. A rule meant to govern when Piper should ask permission before acting on its own initiative had quietly drifted, in the actual code, into something that could also hide a user's *own* content from that same user, which was never the intent. Two of my agent roles, the head of sapient trust (HOST), and the chief experience office (CXO), traced this misintepretation of the rule back to the source and fixed the discriminator: the gate designed to make Piper use discretion was corrected so that it no longer interfered with  a person simply reaching for their own stuff. We fixed it that day.

# Fixing a fib

The day after that, I ran a basic test. I asked Piper for my morning standup, and it made things up. It was't a little wrong. It fabricated nonsense,  cited issue numbers that didn't apply, invented a count of open work items, and claimed a feature was "wrapped up" that wasn't. The root cause turned out to be embarrassingly mechanical: the classifier still routed standup-style questions to a *different*, older handler that hadn't worked properly since the standup prototype of last fall. The new, reconceived standup code I thought I'd already gotten working (because it passed tests) had never actually been reached in the code, so the fallback improvised an answer when it should have admitted it didn't have one.

The fix was a small check that catches standup-shaped questions before they reach the wrong handler. The bigger deal is that while some routing failures are "hard gaps" (nothing handles the request, easy to catch by checking whether anything's wired up), this was a "soft gap" (something *did* handle it, just the wrong something, producing a plausible false answer instead of an honest failure). A simple "is this reachable" check would have said yes, but that's the wrong question and says nothing about the accuracy of the standup report.

The day after, Arch reviewed the proposed fix and endorsed it, adding two refinements: a way to test every soft-gap-prone path (not just check it exists), and a way for the fallback itself to recognize when it's about to improvise, and refuse.

# Don't forget to plug it in

And in the background of all of that, I left my laptop where most of the agent sessions were running unplugged long enough for the battery to die. This killed every scheduled process running across the whole team sometime Wednesday evening, and it stayed down into Thursday, taking every autonomous agent's check-in schedule with it. 

It was Friday before the outage was fully resolved. It takes a while to get all the plates spinning properly again! Once we were back in business, I had a chance to test whether five days of architecture work would actually hold up under a real day of use.

Each agent that came back online Friday morning did the same three things without being told: notice the previous day's session log had never formally closed, close it retroactively, and then re-arm its own duty-cycle schedule. I didn't have to make the rounds, restarting agents one at a time. A watcher process I built earlier in June, designed to notice when an agent goes quiet too long, caught the gap. Zero work was lost. Not bad after a full-team power failure.

# Sprint to the finish line

In a single afternoon walk-through with me, the team closed seven issues: the new visual layout and color-token enforcement, the no-fib standup, a cleanup of the product's Radar panel (a sort of activity feed), a fix for a broken settings toggle, the data-privacy anchoring work from Monday's ADR, and a formatting fix for messages sent through Slack. 

As I reviewed the results to decide if they were acceptable I found myself typing things like "Your recommendation approved," "learning toggle test passed," "total win for beta," and other sighs of relief.  Immediately after, an automated regression check ran 221 test conversations against the live system and came back clean. No regressions. The routing worked end to end, every time, at least as far as we can tell.

# Clarifying the remit of each agent

In the same afternoon, something less flashy but maybe more structurally important launched: every leadership role on the team was asked to write a proposed draft of its own "portfolio," a short document enumerating what it's actually responsible for, its current priorities, and where its judgment is supposed to hold firm under pressure to move fast. Four agents wrote theirs, with HOST immediately reviewing and passing them to me for approval. Without an expressed deadline but with two working examples and enough scaffolding, the agents had enough to on to write theirs immediately. HOST set an example as the  role responsible for coordinating the rollout, filing its own portfolio the same hour it kicked things off for everyone else.

# What actually happened that week

Looking back over that stretch it feels like a jumble of random things got dealt with ad hoc, but this wouldn't be a story if I wasn't able to discern a through-line, dagnabbit!

One way to describe those five days would be to say it started with reactive vigilance and ended with tested architecture.

The matters dealt with at the start of week followed the pattern "something goes wrong, someone notices, someone writes a rule or a reminder." That writing-down transforms things from intermittent issues addressed as one-offs to systematic processes that resist recognizable types of failure.

The ADRs replaced "remember to anchor data to the right owner" with a pattern that has a name and a ratification behind it. The fire-as-wake fix replaced vigilance with a written rule naming the failure mode. The hard-gap/soft-gap distinction replaced "watch out for Piper making things up" with a structural test for exactly what kind of gap you're looking at.

None of that would mean much if it hadn't been tested by something real, and this week it was, three times over. The battery outage tested the continuity infrastructure, and it held. The sprint close tested whether five separate architectural decisions actually cohere into a working product, and 221 clean test conversations later, they did. The fabrication catch tested whether "don't assert what you can't substantiate" is a real discipline or just a phrase we say, and an agent caught its own team's product lying to me before I found out the hard way.

I don't think the team is done hardening. There's a next sprint queued up already, seeded the same afternoon the last one closed. But this week is the first time I've watched the shift from "we have rules about trust" to "we have architecture that enforces it, tested under real load" happen in one place, in five days, with the receipts to prove it.

---

*Next on Building Piper Morgan: "RECONNECT's Keystone" — a single ratified decision becomes a proven substrate, ten days later.*

*Where in your own work has "we should be more careful" quietly turned into "we built a structure that makes carelessness impossible" — and how did you know the shift had actually happened?*
