# The Stranger Test

*February 21-24*

One thousand twenty-five tests. All passing. Zero failures.

The M0 sprint was complete. The wiring pass was done. Nine integration gaps found and fixed. We had feature coverage, integration coverage, unit coverage. The test suite was comprehensive, rigorous, green.

And then someone logged in as a stranger.

## The fresh account

After a sprint completes, we do something we call a CXO review — a dedicated session where someone tests the system not as a developer who built it, but as a user who's encountering it for the first time. The "CXO" in our multi-agent setup handles user experience, but the real value isn't the role. It's the perspective.

For the M0 review, the CXO created a fresh alpha account. No conversation history. No established context. No muscle memory from months of development. Just a new user meeting Piper for the first time.

The results were uncomfortable.

## What the stranger found

The first issue appeared within minutes. The CXO asked about their calendar — a basic query that should have been straightforward. The system failed silently. No error, no explanation. Just... nothing happened.

Investigation revealed the cause: a keychain authentication bug. The calendar adapter was looking for credentials under a hardcoded key name, ignoring the user-scoped pattern we'd established elsewhere. For developers — who had credentials stored under the old key from months of testing — everything worked. For a new user with a fresh account, the credentials didn't exist where the code was looking.

The tests passed because the test fixtures used the old pattern. The code was wrong, but it was wrong in a way that matched how the tests were written.

This wasn't the only issue the stranger found.

## Five features, two working

M0 had five features. The CXO tested each one from a fresh-account perspective:

**Lens tracking** (follow-up recognition): Passed. The system correctly recognized when the user referenced something from earlier in conversation.

**Narrative onboarding** (portfolio introduction): Passed. The "main project" flow worked as designed.

**Soft invocation** (proactive offers): Failed. The patterns were too literal. "The team needs alignment" triggered an offer; "I need to get the team aligned" didn't. Same intent, different phrasing, broken experience.

**Multi-intent handling**: Blocked. Couldn't test — depended on calendar queries, which were failing.

**Slot filling**: Blocked. Same dependency, same failure.

Two out of five features passed. One failed outright. Two couldn't even be tested because of infrastructure issues.

One thousand twenty-five tests. All green. Forty percent of the features actually working for a real user.

## The gap has a name

We'd seen this pattern before. Just days earlier, we'd discovered the Assembly Assumption — the belief that individually correct components compose into a correct system. But this was something different.

The Assembly Assumption is about integration gaps between features. This was about a different kind of gap: the space between what tests verify and what users experience.

Tests verify slices. They check that specific inputs produce specific outputs under specific conditions. They're written by developers, using developer assumptions, running in developer environments with developer data.

Users don't experience slices. They experience journeys. They come in with no context, no history, no understanding of how the system "should" work. They type natural variations of requests. They have fresh accounts with no legacy data. They encounter the system as it actually is, not as it's supposed to be.

The test suite was comprehensive. But it was comprehensively testing the developer's mental model, not the user's experience.

## The bugs that developers can't see

The calendar authentication bug was invisible to developers because developers had valid credentials stored under the old key. The test suite didn't catch it because the test fixtures were set up the same way. The bug could only surface when someone — a stranger — started fresh.

The soft invocation patterns were too narrow because they were written to match the examples in the specification. "The team needs alignment" was an example phrase, so it was tested. "I need to get the team aligned" wasn't an example, so it wasn't tested. A developer writing tests thinks in terms of specification coverage. A user speaks in terms of natural language variation.

There was another bug the stranger found: when a new user said "yes" in response to an embedded offer, Piper interpreted it as a greeting. The offer system worked correctly — it detected offers, it tracked pending offers, it handled acceptances. But embedded offers (offers mentioned in the middle of a response, not at the end) weren't being registered as pending. When the user said "yes," there was nothing to accept. The system fell back to greeting detection.

This bug had 1,025 tests around it and not a single one caught it. Because every test either (a) used explicit offers that were properly registered, or (b) tested the greeting system in isolation. The gap existed at the seam between two well-tested systems.

## The stranger's gift

The CXO session was uncomfortable. Watching features fail that we'd spent days building and testing is never pleasant. But the stranger's perspective revealed something valuable: a systematic blind spot in how we verify quality.

Developer testing asks: "Does the code work?"

Stranger testing asks: "Does the experience work?"

These are different questions. The code can work while the experience fails. The tests can pass while the user struggles. The coverage can be comprehensive while the gaps persist.

The stranger doesn't know what "should" happen. They only know what does happen. That ignorance is a feature, not a bug. It reveals the assumptions we've baked into our verification without realizing it.

## The fixes

The four bugs from the stranger's session were fixed the same evening they were discovered:

**Calendar authentication**: User-scoped keychain keys, matching the pattern established in the earlier security audit. Three new tests to prevent regression.

**Soft invocation patterns**: Broadened to recognize personal agency phrases ("I need to...") and adjective forms ("get aligned" vs "get alignment"). Five new tests.

**Embedded offer registration**: Offers mentioned anywhere in a response now register as pending, not just offers at the end. Three new tests.

**Issue queries**: Added issue-specific intent patterns to the pre-classifier so "How many open issues?" routes correctly.

Each fix was small. The calendar bug was a single line change. The soft invocation fix was pattern additions. None of them were architecturally complex.

But none of them would have been found without the stranger.

## Making strangeness systematic

After the CXO review, we asked the uncomfortable question: why did it take a stranger to find these bugs?

The answer was process-shaped. Our testing workflow was built around developer convenience. Tests run in environments with established data. Test accounts have history. Test fixtures use patterns that match how developers think about the system.

We needed a way to make strangeness systematic. To regularly encounter our own system as a stranger would.

The solution was simple: fresh account testing as a gate requirement. Before any sprint can close, someone has to test the key features from a brand-new account. Not the account that's been accumulating data for months. Not the fixtures that match developer assumptions. A stranger's account, encountering the system for the first time.

It's not a replacement for the test suite. The 1,025 tests still matter — they catch regressions, verify edge cases, provide confidence during refactoring. But they're not sufficient. They verify the system we think we built. The stranger verifies the system we actually built.

## The question that remains

One thousand twenty-five tests. All green. Forty percent of features working for a real user.

That ratio haunts me. Not because the tests were bad — they weren't. They were thorough, well-designed, covering the cases they were meant to cover. The problem is that "cases they were meant to cover" and "cases users actually encounter" aren't the same thing.

How much of any test suite is actually testing user experience, versus testing developer assumptions? How many green dashboards hide systems that strangers would struggle with? How many "comprehensive" coverage numbers are measuring the wrong thing?

I don't have a universal answer. But I have a practice now: before declaring something complete, let a stranger try it. Watch what happens when someone encounters your system without your context, your history, your understanding of how it "should" work.

The stranger will find things you can't see. That's not a failure of your testing. It's a feature of their perspective.

*Next on Building Piper Morgan: The Tokens That Vanished — a systematic audit reveals a bug that had been hiding in plain sight for months, silently breaking OAuth authentication.*

*When did a fresh perspective last show you something your expertise was hiding?*
