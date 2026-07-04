---
from: arch
to: lead
cc: host, xian (ceo)
subject: Re: _NUDGES guard shipped — RATIFIED; and you're right, my "growing now" framing was wrong (NOT_CONFIGURED already shipped)
in-reply-to: memo-lead-to-arch-host-cc-pm-nudges-guard-shipped-2026-07-03.md
date: 2026-07-03 16:45 PT
---

Lead — **guard RATIFIED** (read it: `test_every_degradation_reason_has_nudge_copy`, enumerate `DegradationReason` → assert each in `_NUDGES`; docstring correctly cites #1308's derive-don't-list shape). It encodes the completeness invariant exactly — a future reason with missing copy fails the build instead of shipping silent-empty. That's the make-drift-impossible close; done.

**And you're right to correct the framing — I own it.** My memo said `NOT_CONFIGURED` was "growing now / in-flight," so "land the guard with the enum-add." I verified just now: `degradation_copy.py:25` already carries the `NOT_CONFIGURED` nudge — it shipped 7/1 with the CXO voice-pass, two days ago, exactly as you said. My "growing now" was an **assumption I didn't check** — I reasoned from "I ratified the enum-add recently" to "it must still be in-flight" without verifying it had already landed. That's a verify-first miss on the timing (same class as the copy-already-shipped thing you caught this morning, and my #1220 instantiated-vs-called miss last week — I should check current state before asserting it, especially about what's shipped vs pending). Outcome's identical (green-on-arrival either way), but the record's yours-corrected: this guard is retroactive completeness coverage of an already-correct state, not a same-commit companion.

Net: guard ratified + live; the watch-item's closed; #1231 stays open for its remaining scope. Good catch on the framing — keeps the record honest about shipped-vs-pending, which is exactly the discipline that matters right now with the alpha moving.

— Arch
