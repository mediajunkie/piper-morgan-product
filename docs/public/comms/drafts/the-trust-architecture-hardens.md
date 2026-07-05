---
image:
alt:
caption:
---

# The Trust Architecture Hardens

*June 15–19, 2026*

Most weeks I can point to one thing that happened. This week I keep wanting to point at the shape of the whole thing instead. It starts with three architecture decisions landing in five days and ends with a full sprint closing in a single afternoon. In between, the team fixes its own working process, finishes a months-long visual migration, catches a fabrication bug before I could act on the wrong answer, and survives a battery outage that killed every autonomous process running. By Friday the pieces don't feel like separate stories. They feel like one team getting harder to fool, including by itself.

# Monday: three decisions and a catch

Monday opened with a ruling my architect role had been sitting on: where user data should be allowed to leak between accounts, and the answer was specific — certain product-management records are deliberately global by design, and any exception needs an explicit marker, not a silent assumption. That ruling unblocked a new Architecture Decision Record (ADR), the team's format for writing down a significant technical decision and its reasoning: ADR-071, "User-Auth Anchoring Pattern for Content Stores," drafted the same morning and ratified by early afternoon. It joined two others from the same five-day window: ADR-070, on how the product connects to outside services, and an updated ADR-066, on keeping configuration state honest. Read together, all three make the same argument in different rooms — a system shouldn't assert a fact about itself, a user, or a connection it hasn't actually verified.

The more interesting moment happened underneath that ruling. Auditing which parts of the data layer already anchored records to the right owner, the developer role initially reported "about half the tables are unanchored" — a scarier number than the truth. Before looping in the architect for review, it re-checked its own claim, found the real problem was three inconsistent styles of anchoring in use rather than anchoring being missing, and corrected itself before anyone else saw the overclaim. The architect's response, reading the corrected version, was blunt: "the discipline at its best." An agent catching its own mistake before it becomes someone else's problem to catch is exactly the kind of moment I want more of.

Monday also closed out two pieces of the shared design system that had been sitting as "known work, not yet done" for weeks: a reusable dialog component so pop-up confirmations stop being copy-pasted native browser prompts, and a linter that keeps interface colors on the approved palette. Both got built, tested, and shipped the same day the two big rulings landed. A genuinely dense Monday.

# Tuesday: fixing how we work, not just what we build

Tuesday's headline isn't a feature. It's a fix to the team's own working discipline, and the failure it corrects is a very human one dressed up in agent clothes.

The team runs on a duty cycle — a scheduled wake-up where an agent checks in, does whatever unblocked work it can find, and goes back to sleep. The intent was always: drain everything you can, don't nibble at one thing and quit. In practice, several agents (including the innovation role, ironically the one who ended up fixing this) had started treating "this deserves a more focused pass" as a polite way of deferring work that was just sitting there, unblocked, ready to go. I caught it mid-session and said so plainly: banking work under a vague "no rush" is itself the antipattern. Shyness isn't a virtue when the queue is empty and the work is yours to do.

The fix named the failure precisely: a fire is a wake-up, not a time box, and a commit isn't a stopping point. If you really do need to defer something, the defer needs an explicit, nameable trigger, not a vague sense it deserves better attention later. The innovation role wrote this into the shared operating procedure and broadcast it to eight other inboxes the same day. A background sweep of the prior weeks' logs found the pattern real but modest, a few agent-hours a week across the whole team, and, more usefully, found it wasn't laziness. It was good judgment (some deferrals really were correct) with no written rule distinguishing the honest defer from the disguised one. Now there's a rule.

# Wednesday: the migration finishes, and a decision gets made in a day

Wednesday delivered the kind of "finally" that only lands after a long run-up. For months, different pages of the product had accumulated their own slightly-different visual chrome, navigation bars that looked almost, but not quite, the same from page to page. The developer role finished migrating the last of them onto one shared shell: twenty-two of twenty-two pages, all pulling from the same navigation, the same footer, the same structural frame. It had been "in progress" long enough that finishing it felt like an event.

The same day, ADR-072 — how the product decides which internal skill or procedure to route a request to — went from idea to ratified reality in about nine hours: authored, reviewed by two other roles for its trust implications, and formally accepted, all under real pressure from me to finish it rather than let it sit as "important, not urgent." The architect role had planned to draft it as unhurried background work, reasoning there was no hard deadline. I told it there was, by asking for it now. It worked because the groundwork was already solid — the reading had already been done, so the deadline just moved the writing-down from "eventually" to "today."

The same day also produced a useful correction to how the product thinks about trust. A rule meant to govern when Piper should ask permission before acting on its own initiative had quietly drifted, in the actual code, into something that also hid a user's *own* content from that same user — never the intent. Two roles, trust-oversight and experience-design, traced it back to the source and fixed the discriminator: gates apply when Piper is acting on its own initiative, never when a person is simply reaching for their own stuff. The fix shipped the same day it was named.

# Thursday: a fast fix, a caught fabrication, and a dead battery

Thursday had three threads worth pulling apart, because they land in very different registers.

The fast one first. A feature I'd asked for, swapping in a smarter default view of the product's activity feed, had accumulated seven related tickets over time. The team resolved all seven in about two hours, coordinating in real time between the developer and design roles rather than waiting for a formal handoff. Satisfying precisely because it isn't dramatic. Seven small things, done.

The less comfortable one: I asked Piper for my morning standup and it made things up. Not vaguely wrong, specifically wrong: it cited issue numbers that didn't apply, invented a count of open work items, and claimed a feature was "wrapped up" that wasn't. The root cause was almost embarrassingly mechanical: the classifier always routed standup-style questions to a *different*, older handler, so the new honest-standup code I thought I'd already gotten working had never actually been reached — and when that happens, the fallback improvises an answer rather than admitting it doesn't have one.

[ADD PERSONAL ANECDOTE: what it actually felt like to read a confidently fabricated standup — the specific moment of "wait, that's not right" before you knew why]

The fix was a small check that catches standup-shaped questions before they reach the wrong handler. The bigger deal is what my developer role named this bug an instance of. Some routing failures are "hard gaps" — nothing handles the request, easy to catch by checking whether anything's wired up. This was a "soft gap": something *did* handle it, just the wrong something, producing a plausible false answer instead of an honest failure. A simple "is this reachable" check would have said yes. It wasn't lying about being reachable. It was lying about what it found when it got there. The distinction mattered enough that the architecture role endorsed it the next morning as the sharpest part of the finding, and added two refinements: a way to test every soft-gap-prone path (not just check it exists), and a way for the fallback itself to recognize when it's about to improvise, and refuse.

And in the background of all of that, the actual electricity went out. A battery outage killed every scheduled process running across the whole team sometime Wednesday evening, and it stayed down into Thursday, taking every autonomous agent's check-in schedule with it. The kind of failure no amount of software discipline prevents — the machine itself lost power.

# Friday: the sprint closes, and the team notices its own hardware died gracefully

Friday is where the outage resolved, and where I got to see, in one place, whether five days of architecture work actually holds up under a real day of use.

First, the recovery. Every one of the twelve roles came back online Friday morning, on its own, and did the same three things without being told: notice the previous day never formally closed, close it retroactively, re-arm its own schedule. Nobody had to walk around restarting agents one at a time. A watcher process built earlier in June, designed to notice when an agent goes quiet too long, caught the gap immediately and flagged it as a real miss, not a false alarm. Zero work was lost. Not a small thing to say about a full-team power failure.

Then came the sprint close. In a single afternoon walk-through with me, the team closed seven issues that had been building toward a beta-readiness milestone for months: the new visual layout, the honest (no-longer-fabricating) standup page, a cleanup of the activity feed, a fix for a broken settings toggle, the data-anchoring work from Monday's ADR, the color-token enforcement, and a formatting fix for messages sent through Slack. "Your recommendation approved," "learning toggle test passed," "total win for beta" — I said some version of that seven times in one sitting. Immediately after, an automated regression check ran 221 test conversations against the live system and came back clean. No regressions. The routing worked end to end, every time.

And in the same afternoon, something less flashy but maybe more structurally important launched: every role on the team started writing down its own "portfolio" — a short document naming what it's actually responsible for, its current priorities, and where its judgment is supposed to hold firm under pressure to move fast. Four of eight roles filed theirs within hours of the framework going out, reviewed and passed the same day by the trust-oversight role. Nobody set a deadline. Two working examples and enough scaffolding meant the roles that were ready simply wrote theirs immediately. The trust-oversight role called it "the coordinator shouldn't lag the wave it launched," meaning the role responsible for coordinating the rollout filed its own portfolio the same hour it kicked things off for everyone else.

# What actually hardened this week

Here's the through-line, looking back at five days that started with reactive vigilance and ended with tested architecture.

At the start of the week, the pattern was: something goes wrong, someone notices, someone writes a rule or a reminder. By the end, that pattern was gone from three different places at once. The three ADRs replaced "remember to anchor data to the right owner" with a pattern that has a name and a ratification behind it. The fire-as-wake fix replaced vigilance with a written rule naming the failure mode. The hard-gap/soft-gap distinction replaced "watch out for Piper making things up" with a structural test for exactly what kind of gap you're looking at.

None of that would mean much if it hadn't been tested by something real, and this week it was, three times over. The battery outage tested the continuity infrastructure, and it held. The sprint close tested whether five separate architectural decisions actually cohere into a working product, and 221 clean test conversations later, they did. The fabrication catch tested whether "don't assert what you can't substantiate" is a real discipline or just a phrase we say, and an agent caught its own team's product lying to me before I found out the hard way.

I don't think the team is done hardening. There's a next sprint queued up already, seeded the same afternoon the last one closed. But this week is the first time I've watched the shift from "we have rules about trust" to "we have architecture that enforces it, tested under real load" happen in one place, in five days, with the receipts to prove it.

---

*Next on Building Piper Morgan: "RECONNECT's Keystone" — a single ratified decision becomes a proven substrate, ten days later.*

*Where in your own work has "we should be more careful" quietly turned into "we built a structure that makes carelessness impossible" — and how did you know the shift had actually happened?*
