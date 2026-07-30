---
image: ''
alt: ''
caption: ''
---

# RECONNECT's Keystone

*June 20–28, 2026*

On a Saturday evening in late June, my Lead Developer agent and I looked at a pile of unfinished onnector work — GitHub, Google Calendar, the credentials that tie Piper to the outside services it needs to be useful — and admitted we'd been building around the edges of it for a week without anything closing. So we did the thing you do when a project keeps almost-starting: we picked the actual foundation and built that first. Nine days later, that one decision had been tested by a real security hole, a full release, a live outside user, and one of my own agents catching its own reasoning mistake in public. None of that was staged. It's just what happens when you build a keystone and then spend a week finding out whether it holds weight.

# The keystone, chosen out loud

The project I'd been calling RECONNECT was supposed to be the rebuild of how Piper connects to the services it needs — a connector architecture, instead of the tangle of one-off integrations we'd accumulated. But by the third day of trying to start it, my Lead Dev agent had made two separate wrong turns: mislabeling which existing GitHub issue was actually the starting point, and misreading a related ticket's title as "the quick win" when it wasn't. Neither mistake shipped anything wrong — the agent caught both before writing code, the same investigate-before-extending discipline that's saved us before — but it meant three days of circling instead of building.

So that Saturday evening, we stopped circling and made the call directly: activate the architecture decision record that had been sitting ratified but unbuilt, and build its keystone first — a `Connector` protocol, a single contract that every service integration (GitHub, Calendar, whatever comes next) would have to satisfy. Not the whole system. Just the shape everything else would plug into.

My Lead Dev agent wrote that contract same evening — a small, sharp piece of code: four methods every connector must implement (connect, check status, resolve a request, degrade honestly when something's missing), plus a guard that scans every connector at build time and fails if any of them tries to sneak a raw credential into a return value. My Chief Architect agent reviewed it that same night against five specific constraints we'd need it to satisfy, and by the next morning had ratified it — not from the memo describing the code, but from reading the actual code and its tests. That's the small discipline underneath the big one: when someone tells you a thing is done, go look at the thing.

[FACT-CHECK NOTE for PM: I'm calling this the "RECONNECT keystone" per your framing, referencing the connector-protocol build (issue #1232) ratified the evening of June 20. Confirm "keystone" is the word you want to carry through the piece, or if you'd rather a different image.]

# The hole in the floor, same day

Here's the part that still gets me. The same evening the keystone shipped, a completely unrelated process — a routine sweep my Chief of Staff agent runs to check what needs my attention — turned up something nobody had been looking for: an admin page in the product that could write to the live system, sitting open, unauthenticated, protected by nothing but a login screen at the edge of the network that RECONNECT was about to remove.

That's a genuinely bad kind of bug. Not a crash, not a bad output — a door nobody remembered was unlocked, found because the sweep happened to check, on the same day we were about to open the wall it was hiding behind.

We closed it in hours. My Lead Developer agent deleted the vulnerable page outright rather than patch around it, and then — this is the part I actually care about — built a rule that makes the whole class of mistake impossible going forward: every route that skips the normal login check now has to be explicitly justified in one place, and a new test fails the build if anyone adds a writable, unjustified one. The bug is gone. So is the shape of bug that produced it.

I keep coming back to the timing. If the sweep hadn't run that particular evening, the hole would have stayed open right through the moment we removed a whole layer of protection around it. The keystone didn't cause the vulnerability — the vulnerability was already there, quietly, probably for a while — but the keystone's arrival is what made someone check the door.

# Shipping while building

By Monday the team had moved from "we decided on an architecture" to "the architecture is running in production," and that's a bigger jump than it sounds.

My product-assistant agent (Piper Alpha) cut a release — 2,456 tests passing — and my Lead Developer agent pushed it to the live server the same day. It should have been routine. It wasn't quite. The deploy tripped over a genuinely sneaky bug: the encryption key that protects sensitive data was sitting correctly in the server's configuration file, but the specific way the deploy script loaded environment variables meant the running application never actually saw it. The first attempt to prove encryption was working failed. The fix — naming the variable explicitly instead of trusting it to load automatically — took an hour to find and rewired the deploy process for good.

Two days after that, I checked the onboarding flow myself, from my phone, the way an actual new user would. It failed at the very first step — a system check reporting "services not running" when they were, in fact, running fine. The check itself was broken, hardcoded to look for services at addresses that only exist on a development machine, not the real server. I hadn't gone looking for a bug. I'd just tried to use the thing, and the thing told me it was broken when it wasn't — which is its own particular kind of alarming, because "broken at hello" is exactly what a real alpha tester would have hit first, before the flaw had a chance to matter to anyone but me.

Fixed same morning. But the sequence is the point: build, deploy, break in a way only real use surfaces, fix, and keep going. That's not a triumphant arc. It's what an actual production system looks like while it's proving itself — not a straight line, a series of things going wrong in exactly the ways you can only discover by running the thing for real.

[CONSIDER: is there a personal beat here worth adding about doing that phone check yourself — what it's like to be your own first bug report?]

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
