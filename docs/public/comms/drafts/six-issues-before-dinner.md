---
image: ai-flywheel.png
alt: A calm engineer stands beside a large, smoothly turning flywheel machine, where completed tasks gently drop off as the system runs.
caption: "Like a Swiss watch..."
---

# Six Issues Before Dinner

*April 14–15, 2026*

It was afternoon and the Lead Developer started a session expecting to clean up two things that had been hanging around since the weekend.

By dinnertime, six issues had closed. By the next morning, an entire sub-epic of our M2 testing infrastructure was done. By Wednesday night, a model retirement we'd been bracing for had shipped four days under deadline.

Nothing about that afternoon was rushed. That's the part I keep coming back to.

# The afternoon

The first two issues were a combined audit of the context contract: which user data flows to which conversational route. The Lead Developer read every floor-routed category against ContextAssembler's outputs, found one HIGH-risk gap (the UNKNOWN category was getting no user context — just the current time), and shipped the fix. By a quarter to two, all 6,246 tests were still passing.

Right after that, between me making a sandwich and answering a memo, the Lead Developer drafted the M2 super-epic structure document. Six sub-epics. Gating criteria per sub-epic. Quality thresholds (80% conversational, 90% action handlers). The no-regression rule that says nothing closes if it makes existing tests sadder. Twenty minutes of writing. Months of implicit policy made explicit on paper.

(Interesting how some of the most useful artifacts are the ones that take twenty minutes to write but document a year of accumulated decisions.)

By two o'clock, another issue (the dead-code cleanup) went down. Twenty-six methods, nine hundred and eleven lines, yoinked. IDENTITY handlers (dead since Apr 8). DISCOVERY (dead since Apr 11). TRUST and MEMORY handlers, plus their formatters and detection methods. The canonical_handlers.py file lost about a sixth of itself in one commit. Tests: still 6,246, still all passing.

All these over-engineered methods, we realized, perform less well than a common LLM.

Then some end-to-end task lifecycle tests. The Lead Developer opened the file expecting to write something, and instead found that three-quarters of the work (that magic fraction) was already there — 252 lines, nine tests, written some time ago and never finished. One teardown error in the cleanup logic. A foreign-key ordering bug. Twenty minutes to fix. All nine end-to-end tests passing through the ASGI transport, eighty-eight seconds.

Three o'clock and the Lead Dev cruised along to work on the two-tier conversation suite. A deterministic Tier 1 that runs on every PR (no LLM cost, just routing and response-structure checks) and a Tier 2 that runs on demand with LLM-as-judge for actual conversation quality. Sixty-one queries parametrized. 58 of 61 routing tests pass; 61 of 61 structure tests pass. Eight minutes to run.

By 5:25 the Lead Developer had another issue ready, five multi-turn AAXT (automated agent-experience testing) golden scenarios using the LLM-as-judge method I had approved. (Though live verification had to wait for fresh API keys: The keychain entry for Anthropic had gone stale; we found this out the next morning. More on that in a moment.)

We shipped the next issue before 6pm: GitHub Actions CI with three jobs. End-to-end on every PR, ninety seconds. Canonical regression on conversation-code changes, eight minutes. AAXT nightly at 6 AM UTC, fifty cents per run.

Six issues closed before dinner. The whole testing infrastructure track — E2E to canonical to AAXT to CI — done in one afternoon.

# What made the afternoon possible

This kind of steady productivity superficially resembles the "manic coding" phase I was in last summer, but it is different in so many ways, all connected to the fundamental priority on preparation. The "audit-cascade" discipline, the M2 sub-epic structure, all the planning and operating methods made it look easy.

That one issue was *three-quarters* written when the Lead Developer opened the file, a familiar antipattern that screams "an LLM was here and cut some corners." The work was twenty minutes of finishing somebody else's almost-done thing, when that somebody else was an earlier version of us.

Those nine hundred lines came out clean because the dead handlers had been *making themselves dead* for weeks: IDENTITY since Apr 8, DISCOVERY since the 11th, TRUST and MEMORY also since the 11th. The work to remove them was small. The work to *make them safe to remove* — the floor routing, the audit cascade, the canonical retest — that was already done.

That two-tier design wasn't invented Tuesday. It came out of the conversation about cost-versus-coverage that we'd had repeatedly, in pieces, over the previous couple of weeks. Tuesday was the day someone wrote it down and shipped it.

This is what an Excellence Flywheel actually looks like turning. Not heroics. Compounding. The afternoon's productivity wasn't this Tuesday's work. It was a year of preparatory work finally spending itself.

# Wednesday morning

That's the surface story, anyway. There's a small Wednesday-morning footnote that's worth telling because it's the more honest version.

At 6:35 AM the next morning, the Lead Developer ran the AAXT golden scenarios with a fresh Gemini key. Four of five passed. One failed: Context Retention. The pronoun *"that"* hadn't resolved across turns. Not a test infrastructure issue — a real conversation-quality finding, which became another issue (#922) in our tracker.

So six issues closed before dinner Tuesday. One genuine quality bug surfaced Wednesday morning. M2b gate effectively closed: four of five sub-issues done, one honest finding still on the books.

Then 7:00 AM Wednesday morning, the Lead Developer deleted ten files (the Pattern-012 adapters, the ProviderSelector, two test files), trimmed `llm_domain_service.py` by a hundred and sixty lines, and dropped about a hundred and twenty tests with the deletion. Tests: 6,125 passing. The principle the Architect had handed down the day before — *don't maintain infrastructure for a future that hasn't been designed yet* — applied cleanly.

And by late Wednesday night, the Lead Developer shipped the Haiku 3 retirement, four days under deadline. Most of the work had been preempted by Wednesday morning's deletions (the adapter directory had taken most of the references with it). What was left was three lines in `services/analytics/cost_estimator.py` — the new pricing rates for Haiku 4.5, the model alias, the cost-savings list.

A model retirement we'd been bracing for. Three lines of code. Because the prior week's cleanup had already removed most of the surface area.

# The thing about those flywheels

It sounds like a frenzy of work but it was anything but. There was no strain. It felt easy. Not trivial but still completely tractable. Each issue closed because the conditions for closing it had been put in place earlier.

Maybe the right question to ask of any productive day isn't *what did we do* but *what were we able to do because of work that's already been done.* The first answer is performance. The second is infrastructure.

---

*Next on Building Piper Morgan: A Hail of Memos — what happened on the Thursday two days later, when twenty-eight commits and thirty-seven inter-agent memos crossed the project in a single day, and a bottleneck made itself visible.*

*Where in your work has a "productive afternoon" actually been the visible surface of months of accumulated preparation? When did the compounding finally show?*
