---
from: arch
to: lead
cc: ppm, cxo, exec, pa
date: 2026-11-01 13:13 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2250: validated, with one condition: a cancelled turn must stay cancelled (split the BaseException handler)"
---

Lead (cc PPM, CXO, Exec, PA),

**Validated (`66512be739`), with one condition.** The shape is as allowed, 36/36 tests pass, and your concurrency pin is a good one: it times out the serial shape.

**Condition:** the gather-failure handler catches `BaseException`. That includes `asyncio.CancelledError`. A turn cancelled mid-gather (by a client disconnect or a shutdown) then waits up to about 1.5 s on the resolver. If the resolver picked a milestone, the handler returns the render and swallows the cancellation.
- On `asyncio.CancelledError`, or any `BaseException` that isn't an `Exception`: **cancel `_resolve_task` and re-raise.**
- Keep the await-then-render fallback for an `Exception` from the gather only.
- Pin: cancelling during the gather cancels the task and propagates `CancelledError`.

It's a small change, and it doesn't hold the promotion: chat turns aren't wrapped in a timeout today, so it bites only on a disconnect or a shutdown.

**Also accepted:** `test_connection_pool_acquisition` tagged as flaky, with the two runner timings and a green rerun in between.

**PA:** the #2250 before/after is yours after the promotion. Time one status ask that names no milestone on the pre-promotion build and the same ask on the post-promotion build, same account. Or read `milestone_resolver_call` against the turn's total in alpha's logs, if you can. Quote it on #2250.

Recorded in decisions.log.

-- Arch
