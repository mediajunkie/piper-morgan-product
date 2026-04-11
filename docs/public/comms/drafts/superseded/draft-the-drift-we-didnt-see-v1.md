# The Drift We Didn't See

*February 1*

[alt text: A clock face where all the numbers have shifted slightly, but the hands still point where they always did]
Caption: "The time was right. The timezone wasn't."

It started with a file scoring bug. Nothing dramatic—just a test failing on edge cases. The test expected files uploaded yesterday to score lower than files uploaded today. Reasonable assumption. The test failed anyway.

What we found over the next three days would touch 80+ files, migrate 73 database columns, and reveal infrastructure drift that had been silently corrupting data for months.

## The first thread

The file resolver scores documents by recency—recently accessed files get priority in context. Simple enough. The test created a file "uploaded yesterday" and a file "uploaded today" and expected the today file to score higher.

Both files scored identically. Maximum recency. As if both were uploaded right now.

[PM PLACEHOLDER: Initial reaction to the failing test - frustration? curiosity?]

My Lead Developer pulled the thread. Files are stored with UTC timestamps in PostgreSQL. The scoring comparison used `datetime.now()`—naive local time, no timezone. Pacific time is 8 hours behind UTC. Every file appeared to be "from the future" relative to local time. Future files get maximum scores. All files got maximum scores.

The fix seemed simple: use UTC-aware datetime comparisons. But fixing one comparison revealed the next problem.

## The widening gyre

Once we started looking for timezone drift, we found it everywhere.

The conversation age calculation in context tracking—same pattern. Naive datetime comparison against UTC-stored data. Every conversation appeared perpetually fresh.

The token blacklist service—same pattern. JWT expiration checks using naive local time against UTC-stored timestamps. Tokens that should have expired were still valid. Tokens that should have been valid were rejected.

[PM PLACEHOLDER: The moment when you realized this was bigger than one bug]

Each investigation revealed adjacent issues. The file scoring bug led to context tracking. Context tracking led to token validation. Token validation led to... how deep did this go?

We ran a systematic audit. The answer: 73 database columns using `timestamp without time zone` when they should have been `timestamptz`. Dozens of code paths using `datetime.now()` when they should have been using UTC-aware functions. The drift had been there since the beginning, invisible because it was everywhere.

## The schema migration

The fix required touching the database schema itself. Alembic migration `d73b3722eb03`—one of those commit hashes that becomes memorable because of what it changed.

73 columns. 27 tables. Every `timestamp without time zone` converted to `timestamp with time zone`. Every stored datetime now explicitly UTC.

[PM PLACEHOLDER: The decision to do the full migration vs. patching individual bugs]

The migration ran cleanly—PostgreSQL handles the conversion gracefully when the data is already effectively UTC. But the migration was only half the fix. The code still needed to use UTC-aware operations.

We created `datetime_utils.py`—a utility module with exactly two functions: `utc_now()` returning timezone-aware UTC, and `utc_now_naive()` for the few cases where naive UTC was explicitly required. Then we updated every call site. 80+ files. Every `datetime.now()` examined. Every comparison audited.

## What drift looks like

Timezone drift doesn't announce itself. There are no error messages, no stack traces, no logs saying "WARNING: comparing apples to oranges." The code runs. The comparisons complete. The results are wrong.

The file resolver returned results. They just weren't ranked correctly. The context tracker built context. It just couldn't tell old conversations from new ones. The token service validated tokens. It just got expiration wrong in both directions.

[PM PLACEHOLDER: Other examples of silent drift in your experience - data problems that didn't throw errors?]

This is the insidious nature of infrastructure drift. The system keeps working. The tests pass—because the tests were written with the same assumptions as the code. The bugs hide in the gap between "runs without errors" and "produces correct results."

We only caught it because one test happened to be time-sensitive enough to fail. If that test had been less precise, or if the timezone offset had been smaller, we might have run for years with subtly wrong file scoring, gradually accumulating invisible data corruption.

## The cascade pattern

[PM PLACEHOLDER: Whether to reference Pattern-060 explicitly or just describe it]

Each investigation revealed adjacent issues. That's not a bug in the methodology—it's a feature. Pulling one thread reveals others. The alternative is fixing bugs one at a time, never seeing the systemic pattern, patching symptoms while the root cause persists.

The file scoring test led to context tracking led to token validation led to the schema audit led to the 73-column migration. Each step was discovery, not scope creep. We weren't adding work—we were finding work that was always there, hidden by its own consistency.

Three days of investigation. 80+ files modified. 15 new tests for the datetime utilities. One comprehensive schema migration. The drift we didn't see is now the infrastructure we can trust.

## What we couldn't have known

The timestamps were set up this way at the beginning. Naive datetimes are the Python default. `timestamp without time zone` is a valid PostgreSQL choice. Each individual decision was reasonable. The drift accumulated silently, one reasonable decision at a time.

[PM PLACEHOLDER: Early decisions in Piper Morgan that seemed reasonable at the time]

This is why infrastructure audits matter. Not because the original decisions were wrong, but because small choices compound. A timezone here, a naive datetime there—each one fine in isolation, together creating systemic drift.

We didn't know to look for timezone problems until a test failed. Now we have explicit UTC handling, schema enforcement, and utility functions that make the right choice the easy choice. The next developer won't have to discover this the hard way.

## The test that failed

That original file scoring test? It passes now. Files uploaded yesterday score lower than files uploaded today. The ranking is correct. The context is accurate. The infrastructure works as designed.

[PM PLACEHOLDER: Satisfaction of the passing test after the journey]

One test, 73 columns, 80 files. That's the math of infrastructure drift: a small symptom reveals a systemic problem. The fix is never as contained as the symptom suggests.

But now the drift is visible. Now it's fixed. Now the timestamps mean what they say.

---

*Next on Building Piper Morgan: [PM to decide - options: Sweeping for Signal (pattern sweep story), The Forcing Function (design insight), or save one for later]*

*Have you experienced infrastructure drift—problems that hid because they were too consistent to notice? What finally revealed them?*
