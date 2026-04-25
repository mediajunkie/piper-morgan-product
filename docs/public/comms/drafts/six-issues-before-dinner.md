---
image:
alt:
caption:
---

# Six Issues Before Dinner

*April 14–15, 2026*

It was Tuesday afternoon, twelve thirty-five, and the Lead Developer opened a session expecting to clean up two things that had been hanging around since the weekend.

By dinnertime, six issues had closed. By Wednesday morning, an entire sub-epic of our M2 testing infrastructure was done. By Wednesday night, a model retirement we'd been bracing for had shipped four days under deadline.

Nothing about that afternoon was rushed. That's the part I keep coming back to.

# The afternoon

The first issues — #960 and #961 — were a combined audit of the context contract: which user data flows to which conversational route. The Lead Developer read every floor-routed category against ContextAssembler's outputs, found one HIGH-risk gap (the UNKNOWN category was getting no user context — just the current time), and shipped the fix. By a quarter to two, all 6,246 tests were still passing.

Right after that, between making a sandwich and answering a memo, the Lead Developer drafted the M2 super-epic structure document. Six sub-epics. Gating criteria per sub-epic. Quality thresholds (80% conversational, 90% action handlers). The no-regression rule that says nothing closes if it makes existing tests sadder. Twenty minutes of writing. Months of implicit policy made explicit on paper.

[CONSIDER: a quick aside here about how some of the most useful artifacts are the ones that take twenty minutes to write but document a year of accumulated decisions. Or skip it — the next paragraph carries the through-line fine without it.]

By two o'clock, #963 — the dead-code cleanup — went down. Twenty-six methods, nine hundred and eleven lines, gone. IDENTITY handlers (dead since Apr 8). DISCOVERY (dead since Apr 11). TRUST and MEMORY handlers, plus their formatters and detection methods. The canonical_handlers.py file lost about a sixth of itself in one commit. Tests: still 6,246, still all passing.

Then #927: end-to-end task lifecycle tests. The Lead Developer opened the file expecting to write something, and instead found that 75% of the work was already there — 252 lines, nine tests, written some time ago and never finished. One teardown error in the cleanup logic. A foreign-key ordering bug. Twenty minutes to fix. All nine end-to-end tests passing through the ASGI transport, eighty-eight seconds.

Three o'clock: #928, the canonical conversation suite. Two-tier design — a deterministic Tier 1 that runs on every PR (no LLM cost, just routing and response-structure checks) and a Tier 2 that runs on demand with LLM-as-judge for actual conversation quality. Sixty-one queries parametrized. 58 of 61 routing tests pass; 61 of 61 structure tests pass. Eight minutes to run.

By 5:25 PM the Lead Developer had #929 ready — five multi-turn AAXT golden scenarios using PM-approved LLM-as-judge — although live verification had to wait for fresh API keys. (The keychain entry for Anthropic had gone stale; we found this out the next morning. More on that in a moment.)

5:50 PM, #930 ships: GitHub Actions CI with three jobs. End-to-end on every PR, ninety seconds. Canonical regression on conversation-code changes, eight minutes. AAXT nightly at 6 AM UTC, fifty cents per run.

Six issues closed before dinner. The whole testing infrastructure track — E2E to canonical to AAXT to CI — done in one afternoon.

# What made the afternoon possible

[ADD PERSONAL ANECDOTE: a moment where the surface productivity story masked the actual driver — preparation that had been laid down weeks earlier finally clicking into place. The "Pattern-049 audit-cascade" discipline + the M2 sub-epic structure had been telegraphed for weeks; the Tuesday afternoon was harvest, not invention.]

The afternoon wasn't an outlier of effort. It was an outlier of *compounding*.

#927 was already three-quarters written when the Lead Developer opened the file — that's the Pattern-046 territory we've talked about before, work left at 75% complete and waiting. The Tuesday work was twenty minutes of finishing somebody else's almost-done thing.

#963's nine hundred lines came out clean because the dead handlers had been *making themselves dead* for weeks: IDENTITY since Apr 8, DISCOVERY since the 11th, TRUST and MEMORY also since the 11th. The work to remove them was small. The work to *make them safe to remove* — the floor routing, the audit cascade, the canonical retest — that was already done.

#928's two-tier design wasn't invented Tuesday. It came out of the conversation about cost-versus-coverage that we'd had repeatedly, in pieces, over the previous couple of weeks. Tuesday was the day someone wrote it down and shipped it.

This is what an Excellence Flywheel actually looks like turning. Not heroics. Compounding. The afternoon's productivity wasn't this Tuesday's work. It was a year of preparatory work finally spending itself.

# Wednesday morning

That's the surface story, anyway. There's a small Wednesday-morning footnote that's worth telling because it's the more honest version.

At 6:35 AM Wednesday, the Lead Developer ran the AAXT golden scenarios with a fresh Gemini key. Four of five passed. One failed: Context Retention. The pronoun *"that"* hadn't resolved across turns. Not a test infrastructure issue — a real conversation-quality finding, which became issue #922 in our tracker.

So six issues closed before dinner Tuesday. One genuine quality bug surfaced Wednesday morning. M2b gate effectively closed: four of five sub-issues done, one honest finding still on the books.

Then 7:00 AM, the Lead Developer deleted ten files (the Pattern-012 adapters, the ProviderSelector, two test files), trimmed `llm_domain_service.py` by a hundred and sixty lines, and dropped about a hundred and twenty tests with the deletion. Tests: 6,125 passing. The principle the Architect had handed down the day before — *don't maintain infrastructure for a future that hasn't been designed yet* — applied cleanly.

And by 11:30 PM Wednesday, the Lead Developer shipped #979: the Haiku 3 retirement, four days under deadline. Most of the work had been preempted by Wednesday morning's #971 deletion (the adapter directory had taken most of the references with it). What was left was three lines in `services/analytics/cost_estimator.py` — the new pricing rates for Haiku 4.5, the model alias, the cost-savings list.

A model retirement we'd been bracing for. Three lines of code. Because the prior week's cleanup had already removed most of the surface area.

# The thing about flywheels

[CONSIDER: a closing reflection here. The surface story of Tuesday is "Lead Dev was super productive." The actual story is "the work that had been done over the previous month, plus a year of testing-discipline preparation, finally compounded." This is what we mean by Excellence Flywheel — the property that earlier good work makes later good work *easier*, not just *possible*. Mind you, every productive afternoon could be told this way after the fact; the question that interests me more is whether you can spot the flywheel turning while it's turning, and choose to feed it. Anti-manifesto guardrail: don't claim we've solved this. We've just had one good Tuesday.]

The afternoon wasn't dramatic. The most striking thing was how *unstrained* it felt at every step. Each issue closed because the conditions for closing it had been put in place earlier.

Maybe the right question to ask of any productive day isn't *what did we do* but *what were we able to do because of work that's already been done.* The first answer is performance. The second is infrastructure.

---

*Next on Building Piper Morgan: Thirty-Seven Memos — what happened on the Thursday two days later, when twenty-eight commits and thirty-seven inter-agent memos crossed the project in a single day, and a bottleneck made itself visible.*

*Where in your work has a "productive afternoon" actually been the visible surface of months of accumulated preparation? When did the compounding finally show?*
