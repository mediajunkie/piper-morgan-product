---
image: ''
alt: ''
caption: ''
---

# Three Silent Failures Became One Law

*August 12, 2026*

I've learned to distrust green lights that never blink. This is the story of the day my team learned to distrust them too, and built a rule out of it.

The morning started with my lead developer agent (Lead) closing out something that had been eating at us for two days: the project's main code-quality gate, the automated check that's supposed to stop bad code from landing on the primary branch, had been failing silently since August 9th. Fourteen straight runs, red the whole time, and nobody had noticed until Lead went looking. Lead fixed the underlying issues and watched the gate turn green for the first time since it broke, then went further than closing the ticket: a harder question sat underneath the fix, how does a broken safety check go two full days without anyone seeing it fail? Lead parked that question rather than answer it alone, and handed it to me and my chief of staff agent (Exec) to think about.

The second failure showed up a few hours later, and it came from outside my own team. An agent from a sibling project, Janus, was doing unrelated cross-project work and stumbled onto something worse: our public documentation site's build process had been broken since the end of May. Not flaky, not intermittent. Zero successful builds in the last two hundred attempts, roughly two and a half months of a publishing pipeline that looked fine from the outside and had actually been dead the whole time. The root cause was almost funny in a grim way. Our own internal documentation had described an old templating bug by quoting the broken syntax directly, and the templating engine parsed that quoted example as if it were live code, breaking the very page that explained the break. A description of a bug had reproduced the bug one level up. Janus fixed it and flagged the resemblance to Lead's still-open question about the code gate.

The third piece had been sitting in my documentation agent's (Docs) queue even before that. Docs had already identified that the project's link-checker, the tool meant to catch broken links across our documentation, had a problem of its own: it reported green without actually verifying anything meaningful. It was passing falsely, every time, and calling that success — quieter and worse than simply failing loudly would have been.

By early afternoon Docs had verified Janus's fix and sat with all three cases side by side, and that's when the pattern became visible as one thing instead of three. Each failure was a check that existed, was trusted, and had quietly stopped doing its job while continuing to look fine or simply going unwatched. Docs wrote up the connective insight in a memo to Lead: these three needed exactly two kinds of new detector, not three separate patches. One detector needed to catch checks that had gone dark, stopped running, stopped succeeding, and nobody noticed. The other needed to catch a check that runs constantly and still lies about what it found.

Lead acted on both halves in the same sitting. The link-checker got rebuilt as a ratchet rather than a simple pass-or-fail gate, deliberately, because flipping it straight to strict would have turned a large backlog of legacy broken links into permanent failure on day one, which trains everyone to ignore red the same way the original gate got ignored. Lead closed that fix only after watching it actually fire correctly on a real run, not on the strength of the code being merged. Then, that evening, Lead built the liveness detector itself: a script that checks every workflow in the project for recent successful runs and flags the ones that have gone dark. Its first run found seven broken or abandoned workflows, not the two we already knew about. The detector even caught two bugs in itself before it shipped, including one that would have quietly excused a broken check the same way the original failures had been quietly excused.

In between those two builds, my chief innovation officer agent (CIO) gave the pattern a name and a permanent home: a new team rule about the gap between describing a fix and confirming it's alive. The rule is that a claim that something was fixed and an observation that it's actually working are two different kinds of statement, and only watching the thing behave proves which one you have — a sharper, separate rule from an earlier one about ambiguous check output, built specifically for the gap that let a broken pipeline sit unnoticed for two and a half months while its own documentation insisted it was fine.

Three separate teams found three separate breakages on the same day, and none of them would have connected without Docs doing the unglamorous work of asking what they had in common. That's the part I keep coming back to.

---

*Next on Building Piper Morgan: "Distribution Is a Product Decision, Not a Marketing One" — why choosing where a product lives changes what it actually is, using a listing we can't honestly write yet as the proof.*

*Is there a check in your own work you've stopped actually watching, one you trust just because it's always been green?*
