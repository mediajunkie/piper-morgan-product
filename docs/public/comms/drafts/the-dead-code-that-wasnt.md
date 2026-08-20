---
image: 'the-dead-code-that-wasnt-live-wood.png'
alt: 'A ephemeral arborist pauses before sawing a dead-looking limb after a human supervisor has noticed a leafy branch growing from its hidden side'
caption: '"Don''t cut the live wood!"'
---

# The Dead Code That Wasn't

*July 16–18, 2026*

My agent team spent three days that week deleting code that produces lies. The code runs, returns a plausible answer, and never tells you the answer was fake.

We'd found a lot of this. A file-search feature that could quietly serve simulated results instead of real ones. A security check that failed silently instead of blocking. A recovery routine that claimed to recover and did nothing at all. My chief architect agent (Arch) and my lead developer agent (Lead Dev) had spent the prior week building instruments to find this class of problem systematically — a census of every place in the codebase where a failure gets swallowed instead of surfaced. The tally: 1,233 broad exception handlers, 244 of them sitting on paths real users touch. Of those, 274 got individually classified. 66 needed to stop swallowing and start telling the truth.

One family of fixes got its own name: remove-the-lie. A recovery routine that claimed success while doing nothing became an honest no-op. A security check that failed silently became a loud, unmissable error. The whole batch — sixteen modules across six families — went to Arch for a ruling before anyone touched a line: fabrication-removal, not simple cleanup, so treat it like the thing it actually was.

## The catch

Lead Dev started executing the ruling the next day, working through the families one at a time. Most of it was exactly what the census predicted: dead experiments, orphaned test scaffolding, a module nobody had constructed in months. Delete, verify, move on.

Then, about to delete a module called `protocol/` — ruled dead, on the list, nothing pointing to it as far as the original sweep could tell — Lead Dev checked one more time before the commit. The original evidence-gathering had only looked for absolute-style imports. It missed a live consumer importing `protocol/` through a relative path instead. The module was quietly still doing real work, and the sweep method itself had a blind spot nobody had noticed until it almost cost something.

Lead Dev restored the module, reclassified it, and — because Arch's ruling had been made on the strength of that original evidence — sent word back before committing anything else: the evidence behind that ruling needed a correction. The sweep method got fixed to check both import styles. The batch kept moving, one item lighter and one blind spot smaller.

It's a small moment in a three-day sprint that touched a lot of code. But it's the moment that actually mattered: the same instinct that built a census to catch the codebase's lies almost missed one of its own, and caught it in time, because someone checked before committing rather than after.

## The other catch, a day earlier

A different kind of check earned its keep the day before, in a different part of the system entirely. My team was cutting a release, and the pre-flight gate that runs before every deploy caught something real: a bare variable reference in the classification code, the kind of typo that only shows up when a specific code path actually executes. Left alone, it would have thrown an error on every primary classification, silently, and every message my system processes would have quietly fallen back to a lesser path — degraded, but never announcing that it was degraded.

The gate caught it before it ever reached beta. Different failure, different day, same shape: something in the system was about to quietly do less than it claimed, and a check built to notice exactly that noticed it in time.

## What actually held

The sweep missed an import style. The classifier had a typo nobody caught in review. What held wasn't that either mistake never happened — it's that the checks were built to catch failures like these, and that when one of the checks itself had a blind spot, someone was willing to say so before shipping rather than after.

That's a smaller claim than "we built a system that doesn't lie." It's the more honest one: we built a system that keeps getting better at admitting when it did.

---

*Next on Building Piper Morgan: "The Trust Gate That Wasn't" — a gate meant to govern one kind of behavior gets wired into a completely different one, and quietly hides something that was never supposed to be hidden.*

*Where does your own team's dead-code list hide its one live import — and would you catch it before the commit, or after?*
