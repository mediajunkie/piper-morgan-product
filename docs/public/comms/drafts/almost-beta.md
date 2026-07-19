---
image:
alt:
caption:
---

# Almost Beta

*June 12–14, 2026*

On Friday, we moved four roles to a new account. On Saturday, two more followed. Six roles in two days — a re-migration wave, the team shifting accounts mid-sprint while the sprint continued.

Re-migrations are friction. You take a session that has weeks of context and history, write a carry-forward document that tries to compress what matters, stand up a fresh session, and trust that the document is enough. The measure of whether it worked is whether the work continues without a visible seam.

The Friday session for Lead Developer was the largest single build day the role had recorded: eleven issues closed, the honesty audit shipped (a batch of code fixes targeting places where the system was making claims it couldn't back up), Slack inbound live for the first time in months, and the canonical test suite's expected failure count reaching zero for the first time since the suite existed.

The migration happened in the afternoon. The new session picked up from the carry-forward and shipped four more issues before midnight.

# The benchmark

Saturday, a number that had been wrong for six weeks stopped being wrong.

The canonical test suite had been running with an error in its own harness — a recursion that accumulated across the in-process boots the test runner used. The result was a suite that reported 49 passes and 194 errors, which looked like a lot of real failures. Most of them weren't. Most of them were the harness leak.

Lead Developer diagnosed it, wrote the boot-once fix, and ran the suite. The new result: 242 passes, 1 failure, 0 errors. The single failure was a real one, which was better than the alternative.

The gate on M3 — the current milestone — had been waiting for the canonical baseline to be trustworthy. Now it was.

# The declaration

Late Saturday afternoon, PM was using Piper via Slack to review the remaining M3 issues. Not reviewing the issue tracker through a browser. Using the product, asking it questions about its own backlog, getting substantive answers back.

"It is a toy still," PM wrote, "but it is very cool."

And then, later: *"alpha — almost beta — Piper Morgan is a good PM assistant."*

That's not a technical assessment. It's not a test suite result or a benchmark score or a milestone gate. It's the judgment of someone who's been building the thing, using it for real work, and arrived at an evaluation of whether it actually does what it was built to do.

The distance from "alpha" to "beta" is whatever the person doing the work decides. "Almost" is an honest answer. "A good PM assistant" is the part that matters.

---

*Next on Building Piper Morgan: "The Ritual Becomes a Skill" — a year-long cartoon-drafting collaboration, refined through trial and error into a repeatable ritual, gets extracted into a portable skill before the account that built it disappears.*

*Where in your work is the distance between "working" and "good" determined by a benchmark — and where is it determined by a judgment? What does it feel like when those two land at the same time?*
