---
image: 'ai-stairway.png'
alt: 'A mountain climber ascends toward a summit observatory while the rough path below evolves into permanent stone stairs and an elegant mechanical lift, symbolizing custom work becoming shared infrastructure.'
caption: '"You've got to be kidding me!"'
---

# Climbing Higher When the Platform Laps You

*May 6–18, 2026*

Anthropic shipped Outcomes on May 6 — verification-as-an-API, the productized version of roughly what I'd been building bespoke for months. It would be easy to find this frustrating: *Well, there goes that work.* I had a verification harness running. It was tuned to our specific patterns. I'd written a stack of memos about what it did and why. And now the platform vendor had shipped the same shape as a stable product.

The instinct to defend the bespoke version showed up fast. *Ours is better-fitted. Migration cost is real. Our shapes don't quite match theirs. Maybe we wait.* That's the sunk-cost-defense reflex.

The better question came next: *What does this make possible that I couldn't do before?*

That's the value-chain question. And the answer made me rethink the bespoke work.

# The reframe

My own verification harness wasn't a separate product line I now owned and had to defend. It had been *training material* for understanding what was coming. Building my own version had taught me how verification harnesses work — what they do well, where they get brittle, what's critical versus what's commodity. When the productized version arrived, I could evaluate it as someone who'd been inside one and knew what to look for.

That's a different posture than *they shipped what we built.* That's *we're now the user-class that knows this category from the inside.* Same arrival, different stance.

The disposition I needed sounded something like this: working in an emerging space always means being lapped routinely by the platform. This can't be treated as a problem, a mistake, or wasted sunk cost. It's how you climb higher on the value chain — by building on top of things that are now stable instead of maintaining them yourself.

# Three rules

**Don't defend sunk cost.** The bespoke version served you. That's not a reason to keep maintaining it once a stable productized version is available. The serving was its job. The job is done.

**Don't dismiss the platform version sight-unseen.** *Ours is better-fitted* is a comforting story that's often partly true and entirely beside the point. The platform version benefits from compounding refinement you can't match — a team of engineers, a base of customers, an iteration cadence that runs faster than yours. Test the migration cost against the ongoing maintenance burden honestly. Sometimes the platform version is genuinely worse for your case. Often it's worse for your case *today* and clearly better within a quarter. Plan against the trajectory, not the snapshot.

**Map what migrates, what stays, what gets climbed-to.** Some of your DIY work has shapes the productized version doesn't cover. Those stay — or get rebuilt narrower, so what stays is just the unique-to-you part. The rest moves. The bandwidth that came from no longer maintaining the lower layer is the windfall. The question is what you do with it.

The answer to that question is the third part: climbing higher.

# Climbing higher, concretely

Every time the platform laps you, you get a bandwidth windfall. You stop maintaining the lower layer. The hours you used to spend on the bespoke shape are now available for something else.

The wrong thing to do with those hours is to rebuild a lower-layer shape that's slightly different from the platform's. *Theirs handles A — mine will handle A-prime.* That's just moving the maintenance burden sideways. The bandwidth windfall evaporates into a parallel project with no compounding advantage.

The right thing to do with those hours is to climb. Use the now-stable lower layer as a substrate and build something at the next level up. Something you couldn't have built before because you were too busy maintaining the lower layer yourself.

In our case: the verification work was substrate for something I'd been waiting to build — a higher-leverage feedback loop that depended on having stable verification as a primitive. With the platform doing the verification primitive, the higher-leverage thing got cheaper to build. The lap was a windfall.

# The pattern, not the event

This isn't a one-time event. It's the shape of working in an emerging space.

Verification got productized first. Memory consolidation will get productized later. Multi-agent coordination after that. Event-driven webhooks, structured output schemas, retrieval primitives — each of these has either been productized recently or will be soon. Every lap is the platform turning a custom shape into commodity infrastructure.

Each lap is also a windfall, if you take it as a windfall.

The temptation each time will be the same: *but ours is better-fitted, we have history with our version, migration is expensive, let's wait.* And the right disposition each time will be the same: *what bandwidth does this free up, and what can I now build that I couldn't before?*

# The inverted frame

The frame that flips it all is this: the bespoke work wasn't a product line that's now in competition with the platform. It was *training material* for the moment the platform shows up. You learned things building it that the people who never built it don't know. That knowledge doesn't evaporate when the productized version arrives. It transfers. It becomes the basis on which you adopt the productized version intelligently — knowing where it'll fit clean, knowing where you still need a custom shape, knowing what to test first because you remember which parts were brittle.

The DIY work paid out twice: once as the thing it was while you needed it, and again as the understanding that lets you adopt the platform version without being a passenger.

---

*Next on Building Piper Morgan: "The Practice That Got Retired" — sometimes the most valuable thing a practice does is reveal what should replace it.*

*When has the platform lapped you — and what did you build with the bandwidth it freed up?*
