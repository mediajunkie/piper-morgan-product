# The Drift We Didn't See

*February 1*

[alt text: A clock face where all the numbers have shifted slightly, but the hands still point where they always did]
Caption: "The time was right. The timezone wasn't."

[PM PLACEHOLDER: What was the actual trigger for discovering the timezone drift? The logs show you were debugging the todo bug when you noticed "timestamp-without-timezone warnings" in the terminal. How would you describe the moment you realized this was worth investigating?]

What we found over the course of the day would touch 80+ files, update 47 database columns, and reveal infrastructure drift that had been silently accumulating since the beginning.

## The first thread

[PM PLACEHOLDER: How did the initial investigation unfold? The logs show you asked the Lead Developer about the timestamp warnings observed during todo debugging, and this led to creating #747 for "Schema drift - DateTime vs timestamptz mismatches." What was your thinking as this emerged?]

The fix seemed simple at first: use UTC-aware datetime comparisons. But fixing one comparison revealed the next problem.

## The widening gyre

Once we started looking for timezone drift, we found it everywhere.

[PM PLACEHOLDER: What specific systems showed the same pattern? The logs mention 47 DateTime columns and 239 utcnow() calls needed updating, but don't detail which subsystems were most affected. What stood out to you as you audited the codebase?]

Each investigation revealed adjacent issues. The scope kept expanding. We ran a systematic audit. The answer: 47 database columns using `timestamp without time zone` when they should have been `timestamptz`. Dozens of code paths using `datetime.utcnow()` when they should have been using timezone-aware functions. The drift had been there since the beginning, invisible because it was everywhere.

## The schema migration

The fix required touching the database schema itself.

[PM PLACEHOLDER: Do you remember the migration hash or any other details about running the schema migration? The logs don't include this. If not memorable, we can cut this detail.]

47 columns updated. Every `timestamp without time zone` converted to `timestamp with time zone`. Every stored datetime now explicitly UTC.

The migration ran cleanly—PostgreSQL handles the conversion gracefully when the data is already effectively UTC. But the migration was only half the fix. The code still needed to use UTC-aware operations.

We created `datetime_utils.py`—a utility module with functions for timezone-aware datetime handling: `utc_now()` for the current time in UTC, `ensure_utc()` to normalize incoming datetimes, `is_timezone_aware()` to validate. Then we updated every call site. 80+ files. Every `datetime.utcnow()` examined. Every comparison audited.

## What drift looks like

Timezone drift doesn't announce itself. There are no error messages, no stack traces, no logs saying "WARNING: comparing apples to oranges." The code runs. The comparisons complete. The results are wrong.

[PM PLACEHOLDER: Can you give a concrete example of what the drift caused? The logs don't detail specific symptoms — just that warnings appeared and the schema was mismatched. What would have gone wrong if left unfixed?]

This is the insidious nature of infrastructure drift. The system keeps working. The tests pass—because the tests were written with the same assumptions as the code. The bugs hide in the gap between "runs without errors" and "produces correct results."

We only caught it because warnings appeared during an unrelated debugging session. If I hadn't noticed them scrolling by in the terminal, or hadn't asked about them, we might have run for months with subtle datetime mismatches, gradually accumulating invisible issues.

## The cascade pattern

Each investigation revealed adjacent issues. That's not a bug in the methodology—it's a feature. Pulling one thread reveals others. The alternative is fixing bugs one at a time, never seeing the systemic pattern, patching symptoms while the root cause persists.

[PM PLACEHOLDER: The logs show this work led to discovering 3 pre-existing test failures (#756, #757, #758) that were "not related to #747." Do you want to mention how the timezone work surfaced these other issues?]

The todo debugging led to noticing warnings led to the schema audit led to the 47-column migration. Each step was discovery, not scope creep. We weren't adding work—we were finding work that was always there, hidden by its own consistency.

One day of investigation. 80+ files modified. 15 new tests for the datetime utilities. One comprehensive schema migration. The drift we didn't see is now the infrastructure we can trust.

## What we couldn't have known

The timestamps were set up this way at the beginning. Naive datetimes are the Python default. `timestamp without time zone` is a valid PostgreSQL choice. Each individual decision was reasonable. The drift accumulated silently, one reasonable decision at a time.

[PM PLACEHOLDER: Any early decisions in Piper Morgan that seemed reasonable at the time but accumulated into this kind of drift?]

This is why infrastructure audits matter. Not because the original decisions were wrong, but because small choices compound. A timezone here, a naive datetime there—each one fine in isolation, together creating systemic drift.

We didn't know to look for timezone problems until warnings appeared during unrelated work. Now we have explicit UTC handling, schema enforcement, and utility functions that make the right choice the easy choice. The next developer won't have to discover this the hard way.

## The test that passes

[PM PLACEHOLDER: What's a good concrete ending here? The v1 referenced the file scoring test, but that was actually a pre-existing failure discovered during this work, not the trigger. Is there a specific verification moment you remember — like running the todo feature after the fix and seeing clean output?]

One day, 47 columns, 80 files. That's the math of infrastructure drift: a small symptom reveals a systemic problem. The fix is never as contained as the symptom suggests.

But now the drift is visible. Now it's fixed. Now the timestamps mean what they say.

---

*Next on Building Piper Morgan: [PM to decide - options: Sweeping for Signal (pattern sweep story), The Forcing Function (design insight), or save one for later]*

*Have you experienced infrastructure drift—problems that hid because they were too consistent to notice? What finally revealed them?*

---

## FACT-CHECK NOTES (for PM review, delete before publishing)

**Corrected from v1:**
- "73 columns" → "47 columns" (per logs)
- "27 tables" → removed (not in logs)
- "Three days" → "One day" (all Feb 1)
- "file scoring bug" trigger → replaced with placeholder (actual trigger was todo bug + warnings)
- Migration hash → removed (not in logs)
- "utc_now_naive()" → replaced with actual functions from logs (utc_now, ensure_utc, is_timezone_aware)

**Needs PM input:**
- The actual opening/trigger narrative
- Specific examples of what drift caused
- Any memorable moments from the investigation
- How to end the piece (v1 ending referenced wrong test)

**Verified from logs:**
- ✅ 80+ files
- ✅ 47 DateTime columns
- ✅ 15 new tests
- ✅ datetime_utils.py with utc_now(), ensure_utc(), is_timezone_aware()
- ✅ Cascade pattern
- ✅ All work on Feb 1, 2026
