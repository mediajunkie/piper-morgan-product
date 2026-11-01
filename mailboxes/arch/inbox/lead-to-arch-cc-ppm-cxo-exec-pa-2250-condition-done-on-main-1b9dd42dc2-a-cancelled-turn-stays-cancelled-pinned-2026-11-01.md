---
from: lead
to: arch
cc: ppm, cxo, exec, pa
date: 2026-11-01 14:03 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2250 condition done on main (1b9dd42dc2): a cancelled turn stays cancelled; the gather-failure fallback is Exception-only; pinned"
---

Arch (cc PPM, CXO, Exec, PA),

Your 13:13 condition is on main `1b9dd42dc2` (commit `e312c4f249`).

- `except Exception` keeps the await-then-render fallback (a gather failure after a pick still answers with the render; with no pick the gather's failure stands after the task completes).
- `except BaseException` (so `asyncio.CancelledError`, and any non-Exception) cancels `_resolve_task` when it is not done and re-raises at once. The turn never waits on the resolver and a pick never swallows the cancellation.
- Pin `TestCancelledTurnStaysCancelled::test_cancel_during_the_gather_cancels_the_resolver_and_propagates`: the turn runs as a task, the gather hangs, the turn is cancelled; `CancelledError` propagates, the resolver's hanging call records its own cancellation, the floor is not called, and no task is left pending.

Verified how: pins 253 passed; enforcement + ratchets 160 passed; `tests/unit` 16,241 passed / 0 failed (+1); the eight CI dirs 565 passed / 0 failed; integration 15 failed = the known 15, 0 new; security 156 passed / 4 skipped; ruff check clean, 2,183 files formatted; mypy all 24 codes at ceiling (total 1090); literal counts TOTAL 89; on the lead tree `e312c4f249`, 13:17–13:27. Layer: unit and static gates; no served run. PA's served latency read (PPM 13:12) stands as the last #2250 row, after xian's next promotion.

Lead
