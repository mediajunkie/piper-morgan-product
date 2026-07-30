---
image: 'reconnects-keystone-keystone-arch.png'
alt: "A stonemason lowers his mallet and looks up at the freshly-set keystone crowning a lone stone arch, while two ordinary passersby walk straight through the opening without stopping."
caption: '"It''s holding!"'
---

# RECONNECT's Keystone

*June 20–28, 2026*

On a Saturday evening in late June, my Lead Developer agent and I looked at a pile of unfinished connector work, the credentials that tie Piper to the outside services it needs to be useful (GitHub, Slack, Notion, Google Calendar being the core set of example connections I've aimed for all along, given my own personal preferences) and admitted we'd been building around the edges of it for a week without anything closing.

So we slowed down to review and identified the actual foundation and built that first. A little over a week later, that one decision had been tested by a real security hole, a full release, a live outside user, and one of my own agents catching its own reasoning mistake. All part of what happens when you build a keystone and then spend a week finding out whether it holds weight.

# The missing keystone

The sprint I'd been calling RECONNECT was supposed to be the rebuild of how Piper connects to the services it needs — a connector architecture, instead of the tangle of one-off integrations we'd accumulated. This has been something of a saga.

The earliest designs for Piper Morgan presumed an OAuth-type setup of connected services. But over time I've come to understand the Model Context Protocol (MCP) better, and realized that people are more likely to use a product like Piper inside their existing chat or agentic tool than as a standalone app or website. So this is more or less the third attempt to refactor connectors, after the initial ad hockery and the more serious OAuth plans.

But by the third day of trying to pull off this new plan, my Lead Dev agent had made two separate wrong turns: mislabeling which existing GitHub issue was actually the starting point, and misreading a related ticket's title as "the quick win" when it wasn't. Neither mistake shipped anything wrong — the agent caught both before writing code, the same investigate-before-extending discipline that's saved us before — but it meant three days of circling instead of building.

These sorts of delays get extended when my attention is unavailable at a crucial decision point. All illusions of autonomy grind to a halt then.

So that Saturday evening, we stopped circling and figured out the actual first step we had been missing: build the keystone of a plan captured in an architecture decision record but never built: a `Connector` protocol, a single contract that every service integration would have to satisfy.

First build the universal plug.

Lead Dev wrote the contract same evening, a small, sharp piece of code: four methods every connector must implement (connect, check status, resolve a request, degrade honestly when something's missing), plus a guard that scans every connector at build time and fails if any of them tries to sneak a raw credential into a response.

My Chief Architect agent (Arch) reviewed it that same night against five specific constraints we'd need it to satisfy, and by the next morning had ratified it — not from the memo describing the code, but from reading the actual code and its tests. That's the small discipline underneath the big one: when someone tells you a thing is done, go look at the thing.

# The hole in the floor

Meanwhile, my Chief of Staff agent (Exec) ran a routine sweep to check for anything across the agent team that needs my attention. It noticed that a login screen I was about to remove would expose an admin page in the product that could write to the live system.

That's a genuinely bad kind of bug: a door nobody remembered was unlocked, found because the sweep happened to check, on the same day we were about to open the wall it was hiding behind.

We closed it in hours. Lead Dev first removed the vulnerable page outright rather than patch around it (it was vestigial anyhow), and then (and this is the important part) built a rule that makes the whole class of mistake impossible going forward: every route that skips the normal login check now has to be explicitly justified in one place, and a new test fails the build if anyone adds a writable, unjustified one. The bug is gone. So is the architectural flaw that allowed it.

Got lucky on the timing with that one.

# Shipping while building

By Monday the team had moved from "we decided on an architecture" to "the architecture is running in production," and that's a bigger jump than it sounds.

While Lead Dev has been grinding away toward that elusive beta-release goal, on the side I've been running a skunkworks project with my prototype product assistant role (Piper Alpha) to develop the "bring your own chat" architecture. It's going well. A side effect of this is that we finally stood up a hosted endpoint so that running Piper Morgan doesn't require cloning the repository to a local device and installing it there.

This now means that not only can we test pointing an MCP server at a Piper Morgan backend but also that our alpha and soon-to-be beta testers can now test Piper Morgan much more easily via the web.

We cut a release — 2,456 tests passing — and my Lead Developer agent pushed it to the live server the same day. It should have been routine but... it wasn't. The deploy tripped over a sneaky bug: the encryption key that protects sensitive data was hidden from the running application. It took an hour to figure out we had to name the variable explicitly instead of trusting it to load automatically.

Two days after that, I checked the onboarding flow myself, from my phone, the roughest possible test an actual new user would of course immediately try. It failed at the very first step: a system health check reporting "services not running" when they were, in fact, running fine.

Sort of like one of those "check your 'check engine light'" recursive things was the cause this time: The health check itself was broken, hardcoded to look for services at addresses that only exist on a development machine, not the real server. (Sad trombone. Rookie error!)

This is one reason why I've done 99% of the alpha testing so far. It would be too embarrassing to ask other humans to deal with my obvious errors.

I got it fixed same morning. There really is no substitute for testing your own stuff as a normal user, at least when you are in the target user group, I should say. This sequence of "build, deploy, break in a way only real use surfaces, fix, and keep going" is what an actual production system looks like while it's proving itself.

A day will come when I'll proudly hand someone my phone, maybe in a bar, and show Piper Morgan doing something on a screen or in an interaction and say "I built that!" but it is not this day.

# Someone outside the room

The alpha plugin we'd sent out weeks earlier to a small handful of testers had been mostly quiet. A friend of mine I had the privilege of hiring when I was head of product at CloudOn, Jake Krajewski, has been actively trying out the builds I've been sending. On June 26, he sent back some excellent, actionable, pointed feedback about the install experience. Piper Alpha turned that feedback around fast: two version bumps in one day, each one closing a gap Jake had actually hit.

I don't want to minimize how much I appreciate the value of a real person looking at my work. It's easy to mistake all the agentic input for more than what it is, mostly self-referential. Jake hit a rough edge or two, said so, and by the end of the day those rough edges were gone.

# Hidden in plain sight

The real test of any team dynamic is how it responds when something goes wrong.

Days earlier, Arch had ruled that an old, simulated way of talking to outside services must not be deleted because it was still "live" (reachable, in use). This made the rest of the agent team tiptoe around it. Then Lead Dev traced through the actual code paths and found the opposite: that simulated path was never actually called by anything real. It had been built, instantiated even, but nothing in the running system ever reached it. Dead code, dressed as live.

(It doesn't make me feel great to find out something I was probably blogging about as a cool new feature last year was (a) simulated, and (b) never even wired up!)

Arch re-checked, confirmed Lead was right, and wrote down — in the durable decision record where these things get logged for good — exactly what went wrong: it had confused "the code exists and gets constructed" with "the code actually runs." (Boy, do these agents love to narrate their failures, enough so that it's worth checking any files they maintain for you for extraneous blah blah.)

# Still RECONNECT-or-ing

By the end of that week, GitHub and Google Calendar could both reach Piper through the new contract, real data flowing through a real protocol, verified live against my own accounts rather than trusted from a test suite. The old simulated path — the one that had briefly, mistakenly, been called load-bearing — was being deleted, piece by piece, now that the agents realized it was safe to remove.

It ain't finished but for now the keystone is in place. The building around it is standing. We tested it more ways than I expected to need, over those nine days, just by trying to use the thing while building it.

---

*Next on Building Piper Morgan: "Mechanism Beats Vigilance" — when a failure keeps happening after everyone's been careful, the fix usually isn't more care. It's a wall.*

*When was the last time you built the one piece everything else depends on first — and how long did it take before you found out whether you'd built the right one?*
