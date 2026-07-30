---
image: ''
alt: ''
caption: ''
---

# RECONNECT's Keystone

*June 20–28, 2026*

On a Saturday evening in late June, my Lead Developer agent and I looked at a pile of unfinished connector work, the credentials that tie Piper to the outside services it needs to be useful (GitHub, Slack, Notion, Google Calendar being the core set of example connections I've aimed for all along, given my own personal preferences) and admitted we'd been building around the edges of it for a week without anything closing. 

So we slowed down to review and identified the actual foundation and built that first. A little over a week later, that one decision had been tested by a real security hole, a full release, a live outside user, and one of my own agents catching its own reasoning mistake. All part of what happens when you build a keystone and then spend a week finding out whether it holds weight.

# The missing keystone

The sprint I'd been calling RECONNECT was supposed to be the rebuild of how Piper connects to the services it needs — a connector architecture, instead of the tangle of one-off integrations we'd accumulated. This has been something of a saga. 

The earliest designs for Piper Morgan presumed oauth type setup of connected services, but over time as I've come to understand the MCP model better and have realized that people are more like to use a product like Piper inside their existing chat or agentic tool than as a standalone app or website. So this is more or less the third attempt to refactor connectors after the initial ad hockery and the more serious oauth plans.

But by the third day of trying to pull off this new plan, my Lead Dev agent had made two separate wrong turns: mislabeling which existing GitHub issue was actually the starting point, and misreading a related ticket's title as "the quick win" when it wasn't. Neither mistake shipped anything wrong — the agent caught both before writing code, the same investigate-before-extending discipline that's saved us before — but it meant three days of circling instead of building.

These sorts of delays get extended my attention is unavailable at a crucial decision point. All illusions of autonomy grind to a halt then.

So that Saturday evening, we stopped circling and figured out that actual real first step we had been missing: build the keystone of a plan captured in an architecture decision record but never built: a `Connector` protocol, a single contract that every service integration would have to satisfy. 

First build the universal plug.

Lead Dev wrote the contract same evening, a small, sharp piece of code: four methods every connector must implement (connect, check status, resolve a request, degrade honestly when something's missing), plus a guard that scans every connector at build time and fails if any of them tries to sneak a raw credential into a response. 

My Chief Architect agent (Arch) reviewed it that same night against five specific constraints we'd need it to satisfy, and by the next morning had ratified it — not from the memo describing the code, but from reading the actual code and its tests. That's the small discipline underneath the big one: when someone tells you a thing is done, go look at the thing.

# The hole in the floor

Meanwhile, my Chief of Staff agent (Exec) ran a routine sweep to check for anything across the agent team that needs my attention. It noticed that a login screen I was about to remove would expose an admin page in the product that could write to the live system.

That's a genuinely bad kind of bug: a door nobody remembered was unlocked, found because the sweep happened to check, on the same day we were about to open the wall it was hiding behind.

We closed it in hours. Lead Dev first removed the vulnerable page outright rather than patch around it (it was vestigial anyhow), and then (an this is the important part) built a rule that makes the whole class of mistake impossible going forward: every route that skips the normal login check now has to be explicitly justified in one place, and a new test fails the build if anyone adds a writable, unjustified one. The bug is gone. So is the architectural flaw that allowed it.

Got lucky on the timing with that one.

# Shipping while building

By Monday the team had moved from "we decided on an architecture" to "the architecture is running in production," and that's a bigger jump than it sounds.

While Lead Dev has been grinding away toward that elusive beta-release goal, on the side I've been running a skunkworks project with my prototype product assistant role on (Piper Alpha) to develop the "bring your own chat" architecture. It's going well. A side effect of this is that we finally stood up a hosted endpoint so that running Piper Morgan doesn't require cloning the repository to a local device and installing it there.

This now means that not only can we test pointing an MCP server at a Piper Morgan backend but also that our alpha and soon-to-be beta testers can now test Piper Morgan much more easily via the web.

We cut a release — 2,456 tests passing — and my Lead Developer agent pushed it to the live server the same day. It should have been routine but... it wasn't. The deploy tripped over a sneaky bug: the encryption key that protects sensitive data was hidden from the running application. It took an hour to figure out we had to name the variable explicitly instead of trusting it to load automatically.

Two days after that, I checked the onboarding flow myself, from my phone, the roughest possible test an actual new user would of course immediately try. It failed at the very first step:  a system health check reporting "services not running" when they were, in fact, running fine. 

Sort of like one of those "check your 'check engine light'" recursive things was the cause this time: The health check itself was broken, hardcoded to look for services at addresses that only exist on a development machine, not the real server. (Sad trombone. Rookie error!)

This is one reason why I've done 99% of the alpha testing so far. It would be too embarrassing to ask other humans to deal with my obvious errors.

I got it fixed same morning. There really is no substitute for testing your own stuff as a normal user, at least when you are in the target user group, I should say. This sequence is the of "build, deploy, break in a way only real use surfaces, fix, and keep going" is what an actual production system looks like while it's proving itself.

A day will come when I'll proudly hand someone my phone, maybe in a bar, and show Piper Morgan doing something a screen or in an interaction and say "I built that!" but not this day. 

# Someone outside the room

The alpha plugin we'd sent out weeks earlier to a small handful of testers had been mostly quiet. On June 26, one of those testers — an engineer named Jake — was actively using it, and giving pointed feedback about the install experience. My product-assistant agent turned that feedback around fast: two version bumps in one day, each one closing a gap Jake had actually hit.

[FACT-CHECK NOTE for PM: the source logs on June 26 describe Jake as "first external tester actively using" the alpha, and I initially read that as a first-contact moment. But cross-referencing your own distribution history shows the alpha plugin actually went out to five testers (including Jake) back on June 9 — so June 26 reads more like an existing tester coming alive and driving a fast feedback loop, not a brand-new first use. I rewrote this section to reflect that, but please confirm Jake's actual timeline and whether "first" belongs anywhere in this beat — I don't want to overclaim a milestone that happened weeks earlier and just wasn't visible to the team until now.]

What I want to hold onto isn't the "first" of it — it's the speed. A real person outside the project hit a rough edge, said so, and by the end of the day the rough edge was gone. That loop — outside feedback to shipped fix, same day — is the whole reason any of the RECONNECT work matters. An architecture nobody outside the team ever touches is a diagram. This one had someone's hands on it within the same week it got its keystone.

# The mistake owned in public

The moment that actually tells you whether a team's discipline is real, though, isn't the clean run. It's what happens when someone gets it wrong.

Days earlier, my Chief Architect agent had ruled that an old, simulated way of talking to outside services was still "live" — reachable, in use, something you couldn't just delete. That ruling shaped how carefully the team treated it. Then my Lead Developer agent, while tracing through the actual code paths rather than trusting the earlier read, found the opposite: the simulated path was never actually called by anything real. It had been built, instantiated even, but nothing in the running system ever reached it. Dead code, dressed as live.

The Architect agent didn't defend the earlier ruling. It re-checked, confirmed Lead was right, and wrote down — in the durable decision record where these things get logged for good — exactly what went wrong: it had confused "the code exists and gets constructed" with "the code actually runs." Those are not the same thing, and mistaking one for the other is a specific, nameable failure the team has a name for. Naming your own instance of it, on the record, the same day someone else catches it, is the discipline working exactly as intended. Nobody quietly fixed the ruling and moved on. Somebody wrote down that the ruling had been wrong and why.

That's a small moment in a nine-day stretch full of bigger-looking ones. I think it's the one that matters most, because it's not about whether the architecture holds — it's about whether the team correcting itself holds, in public, without needing me to catch it first.

# Where it stands

By the end of that week, the connector work had gone from a decision to a running thing: GitHub and Calendar both talked to Piper through the new contract, real data flowing through a real protocol, verified live against my own accounts rather than trusted from a test suite. The old simulated path — the one that had briefly, mistakenly, been called load-bearing — was being deleted, piece by piece, now that everyone agreed it was safe to remove.

I want to be precise about what I'm claiming here, because it would be easy to overreach. The substrate proved itself real this week — tested by an actual security bug, an actual deploy, an actual outside user, an actual internal mistake caught and corrected. That's not nothing. Structurally, the pieces that needed to exist now exist, and they've taken a week of real weight without buckling. What I'm not claiming is that it's finished, or that "held up for a week" means "will hold up forever." Those are different questions, and I've learned not to answer the second one until I've actually asked it.

For now: the keystone is in. The building around it is standing. We tested it more ways than I expected to need, in nine days, without setting out to test it at all — that's just what happened when we tried to use the thing while building it.

---

*Next on Building Piper Morgan: "Mechanism Beats Vigilance" — when a failure keeps happening after everyone's been careful, the fix usually isn't more care. It's a wall.*

*When was the last time you built the one piece everything else depends on first — and how long did it take before you found out whether you'd built the right one?*
