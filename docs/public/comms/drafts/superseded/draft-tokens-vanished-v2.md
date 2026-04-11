# The Tokens That Vanished

*February 25*

The Slack integration had been "working" for months.

Users could connect their Slack accounts. The OAuth flow completed successfully. Tokens were stored. The system reported success at every step.

But nobody could actually use Slack through Piper. Every attempt failed silently. The connection existed on paper but not in practice.

It took a systematic audit to find out why.

## The audit that found nothing (and then everything)

February 25 started with a security review. After the fresh-account testing revealed authentication bugs in the calendar adapter, we decided to audit all our keychain usage. The keychain stores OAuth tokens and other sensitive credentials, and we'd discovered that some code was using inconsistent key patterns — hardcoded strings instead of user-scoped keys.

The Lead Developer started with a simple question: how many places in the codebase access the keychain, and are they all using the correct scoping pattern?

The answer was worse than expected. Fifteen sites across five categories were using non-scoped keys. But the Slack integration stood out for a different reason.

The audit found two lines of code that told a complete story:

**Storing the token:**
```python
keychain.store("slack_oauth_{username}", token)
```

**Retrieving the token:**
```python
token = keychain.get(f"slack_oauth_{username}")
```

Do you see it?

## The f-string that wasn't

In Python, f-strings are a way to embed variables in text. When you write `f"hello_{name}"`, Python substitutes the value of `name` into the string. If `name` is "alice", you get "hello_alice".

But f-strings only work if you include the `f` prefix. Without it, `"hello_{name}"` is just a literal string containing the characters `{`, `n`, `a`, `m`, `e`, `}`.

The storage line was missing the `f` prefix. Every token was being stored under the literal key `"slack_oauth_{username}"` — the actual characters, curly braces and all.

The retrieval line had the `f` prefix. It was looking for `"slack_oauth_alice"` or `"slack_oauth_bob"` — the properly formatted, user-scoped key.

The keys never matched. Every token stored was immediately unretrievable.

## How this stayed hidden

The bug had been in production for months. How did nobody notice?

First: the OAuth flow appeared to work. Users clicked "Connect Slack," went through the OAuth dance, got redirected back with a success message. The token was stored successfully — just under the wrong key. Nothing failed. Nothing threw an error. The user saw "Connected" and assumed it was.

Second: the failure was silent. When Piper tried to use Slack features, the token retrieval returned null. The code handled null gracefully — it just didn't do the Slack operation. No error message, no notification. The feature quietly didn't work.

Third: testing didn't catch it. The test fixtures for Slack used mock keychain operations that didn't actually go through the store-then-retrieve cycle. The store was mocked. The retrieve was mocked. The mismatch between them was invisible.

Fourth: developers didn't use it. The Slack integration was there, but it wasn't a core workflow. Calendar was more heavily used. Projects were more heavily used. Slack was a secondary feature that people connected and then... didn't really use, because it didn't work, and they assumed that was just how it was.

The bug persisted because every system that could have caught it was designed to verify components, not journeys. The OAuth flow worked. The token storage worked. The token retrieval worked. The fact that storage and retrieval were using different keys — that lived in the gap between verifications.

## The audit cascade

Finding the bug was only the beginning. The Lead Developer's response was methodical:

**Step 1: Scope the problem.** How many keychain sites had similar issues? The audit found 15 total across five categories: OAuth tokens, API keys, user preferences, session data, and integration credentials.

**Step 2: Categorize and prioritize.** Some non-scoped keys were benign (system-wide configuration that genuinely shouldn't be user-scoped). Others were serious (anything involving authentication or user data). The Slack bug was the most severe — actively breaking functionality — but there were others that could have caused problems.

**Step 3: Fix systematically.** Rather than playing whack-a-mole with individual bugs, the Lead Developer created a pattern: every keychain access would use a consistent, user-scoped key format. Then applied that pattern everywhere.

**Step 4: Prevent recurrence.** A CI guard was added — a grep check that fails the build if it detects keychain access patterns without user scoping. The bug that hid for months could now never be reintroduced.

**Step 5: Test the seams.** Twenty-five new tests were added, specifically testing the store-then-retrieve cycle for each integration. Not mocked storage and mocked retrieval — actual round trips through the real keychain layer.

The whole fix took a few hours. The bug had been hiding for months.

## What the f-string teaches

There's a category of bug that exists not because code is wrong, but because two pieces of correct code don't match. The storage line was valid Python. The retrieval line was valid Python. Each worked as written. Together, they created a gap.

These bugs are invisible to most verification approaches:

- **Unit tests** verify each function in isolation. Both the store and retrieve functions worked correctly — they just weren't called with matching arguments.
- **Integration tests** often mock the components they're integrating with. The mock didn't reproduce the mismatch.
- **Code review** reads code linearly. The storage was in one file, the retrieval in another. Nobody was looking at both simultaneously and comparing the string formats.
- **User testing** showed a successful connection. The failure only manifested later, in a different context, as an absence rather than an error.

The bug lived in the seam between two systems that never talked to each other directly. Storage didn't know about retrieval. Retrieval didn't know about storage. Each was tested in isolation. The gap was systematically excluded from verification.

## Systematic finding, systematic prevention

The f-string bug could have been found by accident — someone eventually would have noticed that Slack didn't work and dug into why. But accidental discovery is slow and unreliable. The bug persisted for months precisely because accidental discovery hadn't happened yet.

What found it was systematic audit. Not "look for bugs" but "examine every place this pattern occurs and verify consistency." The audit didn't know the f-string bug existed. It was looking for a category of issue (non-scoped keychain access) and found this specific instance along the way.

This is the difference between debugging and auditing. Debugging is reactive — something broke, find out why. Auditing is proactive — nothing appears broken, verify that it isn't.

The CI guard is the same principle applied to prevention. It doesn't know about f-string bugs specifically. It knows about a pattern that's dangerous (keychain access without user scoping) and flags all instances. Future developers don't need to know this bug's history. They just need to follow the pattern, and if they don't, the build fails.

Systematic approaches find bugs that hide in plain sight. They catch the mismatches that each component is too local to see. They turn "we got lucky someone noticed" into "we would have caught this automatically."

## The tokens return

After the fix, we did something we should have done months earlier: actually tested the Slack integration end to end. OAuth flow, token storage, token retrieval, actual Slack operation.

It worked.

The tokens that had been vanishing into a mislabeled bucket were now stored where they could be found. The feature that had been silently broken was now quietly functional.

Nobody celebrated. The fix was too small, the bug too embarrassing, the months of it hiding too uncomfortable. But there was satisfaction in the systematic approach — in knowing that the audit would have found this bug whether or not we were looking for it, and that the CI guard would prevent it from ever returning.

## The question the audit answered

Before the audit, I would have said the Slack integration worked. It went through OAuth successfully. It stored tokens. It had test coverage.

After the audit, I knew the Slack integration worked. The tokens were stored correctly. They could be retrieved. The round trip was verified.

The difference is the gap between "appears to work" and "verified to work." Most of what we believe about our systems falls into the first category. We saw it succeed once. We assume it still does. We trust our tests to tell us if something breaks.

But tests only catch what they're designed to catch. The f-string bug was designed (accidentally, structurally) to slip past. Not maliciously — through the ordinary, structural blind spots of how we verify software.

Systematic audits are how you find the bugs that were designed (accidentally, structurally) to remain hidden. They're not glamorous. They don't produce new features. But they're the difference between thinking your OAuth works and knowing it does.

*Next on Building Piper Morgan: Four Voices, One Spec — a research agent, a UX lead, a product manager, and an architect converge on a single specification, each adding something the others couldn't.*

*What's hiding in the seams of your system — the places where two correct things don't quite match?*
