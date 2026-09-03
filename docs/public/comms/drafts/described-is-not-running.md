---
image:
alt:
caption:
---

# Described Is Not Running

*August 12, 2026*

A colleague at a partner project traced a documentation build that had been silently broken for two and a half months. Nothing was checking whether the deploy actually happened — no test, no health check, no exit code anywhere in the pipeline that would fail if the build quietly stopped working. The configuration described a working deployment. It just wasn't one, and had not been for ten weeks.

That finding landed the same day my team named something related but distinct from a pattern we'd already been tracking. We already had a name for "a check reports clear without measuring what it claims to measure." This was a different failure: not an instrument giving an ambiguous answer, but a *description standing in for the thing it describes* — a config file, a status report, a design doc, treated as equivalent to the running system it's supposed to represent, with nobody ever confirming the two actually match.

# The test that proves the point on itself

The clearest demonstration of why this matters happened a few hours later, inside my own team's work, on a completely unrelated project.

We'd just finished scoping down a large public documentation site — cutting it from roughly 1,370 served pages to about 160 that visitors actually need, via a configuration file that lists which paths to exclude. The config was reviewed, ratified, and applied. By the letter of the description, the job was done.

Instead of stopping there, the person who applied it went and checked the site as a visitor would — actually loading pages, not reading the config that was supposed to govern them. That single step found two real defects the config's own text gave no hint of. One exclusion pattern was written broadly enough that it silently swallowed a sibling folder that was supposed to stay included — the two paths looked distinct in the config but overlapped in practice. And a page that was already supposed to be live had, it turned out, never actually rendered at all, even before the day's changes — a quirk of the hosting platform that skips certain filenames without an extra line of setup nobody had added.

Neither defect was visible from the configuration. Both were visible in about ten minutes of actually looking at the deployed pages.

# Why the description looks sufficient

A config file, once it's written and reviewed, has a strong pull toward feeling finished. It's specific, it's been checked by more than one person, and it says exactly what you intended. All of that is real, and none of it tells you whether the system built from that description actually does what the description says. A config can be internally consistent and still produce a different result than the one it describes, for reasons that only show up once something runs against it — a pattern-matching quirk, a platform default, an edge case in how two rules interact.

This is the same shape as the dead documentation build, just compressed from ten weeks to ten minutes. Nobody there was lying either. The pipeline's configuration described a deployment. The description simply stopped being true at some point, and nothing was positioned to notice, because nothing was checking the running thing — only the description of it.

# The discipline, stated plainly

A description of a system — a config, a plan, a status line, a design doc — is a claim about the system, not a substitute for checking it. The gap between the two doesn't announce itself. It sits quietly until someone happens to look at the actual running behavior instead of the artifact that's supposed to produce it, and the longer nobody looks, the wider that gap can get before anyone notices — two and a half months, in the case that started this.

The fix isn't "review configs more carefully." Careful review is exactly what both examples already had, and it wasn't enough on its own in either case. The fix is treating "we wrote it down correctly" and "we confirmed it does that" as two separate steps, with the second one mandatory before calling anything done — because a description that's never been checked against its own referent is a hypothesis, not a fact, no matter how carefully it was written.

---

*Next on Building Piper Morgan: "Three Seats Stay Dark Longer" — the whole team hits its usage limit and goes offline together, but three roles don't come back for twenty-one hours after everyone else does, and nobody knows why until the next day.*

*Where in your own systems is a config, a doc, or a status line quietly standing in for a check you haven't actually run?*
