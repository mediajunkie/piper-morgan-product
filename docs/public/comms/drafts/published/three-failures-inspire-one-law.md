---
image: 'three-failures-inspire-one-law-elephant-meets-the-impossible-zero.jpg'
alt: 'An elephant stands on a scale reading zero while a luminous AI assistant records the result and a skeptical human leans in to inspect the dial.'
caption: '"I’m beginning to suspect the scale!"'
---

# Three Failures Inspire One Law

*August 12, 2026*

I wouldn't trust a stoplight if I saw everyone running the red. Nor would I trust a light that was always green. I've had to teach my team to be equally suspicious of tests that always pass.

The morning started with my lead developer agent (Lead) closing out a problem that had been sitting there for two days: the project's main code-quality gate, the automated check that's supposed to stop bad code from landing on the primary branch, had been failing since August 9th without anybody (or anything) noticing.

Lead fixed the underlying issues and watched the gate turn green for the first time since it broke. Then we went looking at the bigger question: how does a broken safety check go two full days and at least fourteen runs without raising an alarm? Lead escalated this question for me and my chief of staff agent (Exec) to think about.

That same day, a few hours later, a second failure cropped up, this time from outside of Piper Morgan proper. An agent that oversees all of my projects, Janus, stumbled onto something even more embarrassing: my [public documentation site](https://pmorgan.tech)'s build process had been broken *since the end of May*. Not too many picky readers, I guess!

Zero successful builds in the last two hundred attempts, roughly two and a half months of a publishing pipeline that looked fine from the outside and had actually been useless the whole time. The root cause was almost funny in a depressing way. Basically a document discussing a bug failed to escape the bug sufficiently so that the build process was breaking each time by encountering the documented bug.

A *description* of a bug had reproduced the bug one level up. What is this, Borges? Janus fixed it and (reading over our shoulders) pointed out a resemblance to Lead's still-open question about the code gate.

The third example was sitting in the queue of my documentation agent (Docs) even before that. Docs had already identified that the project's link-checker, the tool meant to catch broken links across our documentation, had a problem of its own: it reported green without actually verifying anything meaningful. It was passing falsely, every time.

Each failure involved an existing, trusted check that was misleading us. Docs wrote up the connective insight in a memo to Lead: these three problems called for two new kinds of detector. One detector needed to catch checks that had gone dark, stopped running, or stopped succeeding. The other needed to catch a check that falsely reports success.

The link-checker got rebuilt as a ratchet rather than a simple pass-or-fail gate because flipping it straight to strict would have turned a large backlog of legacy broken links into permanent failure on day one (which then trains everyone to ignore red the same way the original gate got ignored). Lead closed the GitHub issue for that fix only after verifying it actually fired correctly on a real run.

Then, that evening, Lead built the liveness detector itself: a script that checks every workflow in the project for recent successful runs and flags the ones that have gone dark. Its first run found seven broken or abandoned workflows, up from the two we already knew about. The detector even caught two bugs in itself before it shipped, including (naturally) one that would have excused a broken check the same way the original failures had been ignored.

In between those two builds, my chief innovation officer agent (CIO) gave the new pattern a name and a permanent home: a new team rule about the gap between describing a fix and confirming it's alive. The rule clarifies that a *claim* that something was fixed and an *observation* that it's actually working are two different kinds of statement, and only the second can confirm the first.

So much of this work requires verification and checking, and until you can trust your instruments, it's almost impossible to make real progress.

---

*Next on Building Piper Morgan: "No Undo" — three agents, three destructive commands, and what it actually means that being careful with the reversible stuff tells you nothing about the irreversible stuff.*

*Is there a check in your own work you've stopped actually watching, one you trust just because it's always been green?*
