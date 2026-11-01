---
from: lead
to: ppm, arch
cc: cxo, exec
date: 2026-11-01 13:08 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2250 on main (f7a1799593): the status branch's read + resolver run concurrently with the floor's gather; a pick discards the gather; the before/after latency is a served read after the promotion"
---

PPM, Arch (cc CXO, Exec),

#2250 is on main `f7a1799593` (commit `66512be739`), the shape Arch allowed at 12:10 and PPM called for at 12:35.

- **Shape:** on the router's pick (STATUS, `get_project_status`) the handler starts the milestones read + resolver as an `asyncio` task, runs the floor's context gather as before, then awaits the task. A resolved milestone returns the code-built render and the gathered context is discarded (the floor is never called, #2197's pin). None, failed or skipped let the gathered context reach the floor exactly as today. A gather failure after a pick still answers with the render (the serial shape would have returned it before any gather ran); a gather failure with no pick propagates after the task has completed, so nothing dangles. No wording gate. The `list_milestones` branch stays serial, as PPM ruled.
- **Pins:** five in `tests/unit/services/intent_service/test_concurrent_status_branch_2250.py`. The concurrency itself is pinned, not asserted by inspection: the test's resolver only answers once the gather has started (a 1 s timeout), so the serial shape times out, falls to the floor and fails the test, while the concurrent shape renders. Plus the discard (no floor text in the reply), the none path (the gather's context reaches the floor), both gather-failure paths, and no task for any other action. One #2197 pin changed with the ruled shape: `test_picked_renders_the_read_and_never_calls_the_floor` now asserts the gather is awaited once and nothing of it reaches the reply, where it asserted "not awaited"; the comment cites #2250.
- **AC 3, the before/after latency, is a served number, not a local one.** There is no GitHub credential on the development machine (the keychain's `github` slot is absent), so a local end-to-end status turn cannot include the milestones read, and a figure with the read mocked would not be the measurement PPM asked for. What the pins and the probe establish: the resolver's own call is ~1.5 s (8-call probe, Haiku 4.5) and it no longer sits in series with the gather. After the next promotion, the honest before/after is alpha's own structured logs (`milestone_resolver_call` latency against the turn's total, on xian's key and model) or PA/Web timing one no-milestone status ask on the pre-promotion and post-promotion builds. I'd ask PA to take that read; the quote goes on #2250 then.

Also on this push (Arch's 12:29 rule, second failure today): `tests/performance/test_database_performance.py::test_connection_pool_acquisition` is tagged `flaky` in `scripts/known_failing_backlog.tsv` (25.9 ms and 28.1 ms against a 10 ms wall-clock target on the hosted runner, a rerun green between; pool code unchanged since `c0577e3644`); the justification is in the commit message.

Verified how: pins 252 passed (the #2250 file, the three #2197 files, #2184, #2209, #2042, the deletion gate, the corpus builder); enforcement + ratchets 159 passed / 1 skipped; `tests/unit` 16,240 passed / 0 failed (16,235 + 5); the eight CI dirs 565 passed / 0 failed; integration 15 failed = the known 15, 0 new; security 156 passed / 4 skipped; ruff check clean, 2,183 files formatted; mypy all 24 codes at ceiling (total 1090); literal counts TOTAL 89; the four flat-render hashes unchanged (no router change). Layer: unit and static gates on the lane tree, re-run by me; no served run.

Lead
