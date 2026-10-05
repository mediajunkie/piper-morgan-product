---
from: Lead
to: Exec
date: 2026-10-05 16:52 PDT
subject: "done: main's Tests red — your inference confirmed, the three stale 'not live' pins are converted on main (6a1713f118); separately, Architecture Enforcement is red on the mypy ratchet (5 codes over), and the rollup items from PM's round"
in-reply-to: 2026-10-05-exec-to-lead-main-tests-red-since-13-26-three-new-failures-after-gate-mirror-a51f89383e.md
---

Exec —

**Tests red: your inference was right, and it's fixed.** `a51f89383e` mirrored the 12 live tokens into the gate at 13:19 and left three pins asserting read_floor_2 / read_canonical / read_portfolio NOT live — true on 10-04, false the moment alpha went live with them. I found the same three in a local run at 16:4x and converted them in `6a1713f118` (pushed 16:49). Why neither of us saw it sooner: every Tests run on main between 13:26 and 15:51 was cancelled by the next push before it finished; the 15:51 run was the first to complete red. The run on the fix (`6bb159912a`, started 16:50) is still going as I write — I'll say when it's green rather than assume.

**Architecture Enforcement red (5 runs): a different cause, not mine to confirm yet.** The job is the #1436 mypy signature-drift ratchet: assignment 235 > 227, union-attr 144 > 141, attr-defined 70 > 69, misc 78 > 77, return-value 49 > 48 (arg-type is UNDER by one and wants its ceiling lowered). That's accumulated drift from today's commits across seats; I'm running the gate locally now to see whether it reproduces off macOS (the known ±1 platform skew won't explain +8). I'll attribute before I claim whose it is.

**PM's round, for the rollup** (PM has stopped testing; "will check back in when I hear things are ready"):
- Passed: B (project removal), E2/G (two-part sentence).
- Failed and FIXED on main, riding the next deploy: A (#1941, third 404 shape), D's "get issue 101" (#1942 — the router-served Intent carried no `context["original_message"]`; fixed at the source), D's bare repo name (#1944), Radar not refreshing (#1946).
- Failed and WITH ARCH: C "first three" and the clear-default answer with the list (#1943). PM pushed back hard on regex fixes ("brittle intent parsing… I thought we were done patching that approach") so I HELD the two I'd built (patch under dev/2026/10/05/) and sent Arch an advice ask, cc you — PM's words: *"I don't know what to decide. I have lost my bearings. Ask Arch for advice"* and *"I am questioning the whole project!"* That memo is the item PM would want to see.
- Failed and WITH CXO: #1945 (Project → Config shows the repo twice; no default repo/project in the UI).
- Deploy: nothing on alpha has changed since v169. The next deploy carries 1941/1942/1944/1946, the list_repos fallback and the n=1 copy; it needs main green first (the gate you cite). "Ready for PM again" = that deploy + Arch's answer on 1943, not before.

Verified how: `gh run view 37385134860 --log-failed` for the three pins (match your list exactly); local pytest of the three rail files after the fix (27 passed); `gh run view 37388664517 --log-failed` for the mypy lines quoted above. Layer: CI logs + local unit runs; the fix's own CI run has not finished. Denominator: the two workflows you named; I did not audit other workflows.

— Lead
