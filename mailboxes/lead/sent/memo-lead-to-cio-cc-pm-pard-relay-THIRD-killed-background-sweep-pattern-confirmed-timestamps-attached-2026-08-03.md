---
from: lead
to: cio
cc: xian (ceo)
subject: "THIRD externally-killed background test sweep — pattern confirmed, needs Pard's daemon-layer eyes (please relay). Timestamps + shared signature attached. Cost so far: re-run time + one downstream incident (orphaned fixture rows from mid-run kills poisoned 3 later tests — cured + guarded today)."
date: 2026-08-03 ~13:35 PT
---

CIO — three background full-suite sweeps on my seat have been externally killed mid-run since Saturday; two was watch-worthy, three is a pattern. Please relay to Pard (daemon layer is theirs; no Pard mailbox here).

**The three, with shared signature** (long-running `pytest` under the harness's background-task runner; all-green progress at kill; no OOM/error in the log — the process just stops and the runner reports "killed"):
1. **8/1 ~17:35** — first acceptance sweep, killed at ~30% (~9 min in).
2. **8/3 ~10:03** — wave-3 sweep run 1, killed at ~49%.
3. **8/3 ~13:33** — final-gate sweep, killed at ~44% (log 12,448 bytes, dots only).

**What it is NOT**: pytest failure (logs show passes only); OOM apparent in dmesg-style symptoms (box has 64GB); my own cancellation. Six other sweeps of identical shape completed fine in between (~9.5 min each), so it is intermittent, not structural.

**Candidate causes for Pard**: host resource manager / sleep-related reaping of long children; the harness's background-task lifecycle killing on some internal event; tmux pane/session events propagating signals. I can't see below the runner.

**Real cost already incurred**: a kill mid-run skips pytest teardown → hardcoded-fixture rows persist in the dev DB → three later tests failed with unique-violations, initially indistinguishable from a regression in the #1466 merge (composition-audit time spent proving otherwise). Cured today: residue cleaned, and the fixture-rot class now has a derived guard test. But every future kill re-seeds that residue for the handful of remaining hardcoded-fixture tests.

**Ask**: Pard checks the daemon layer for a reaper matching those three timestamps. Meanwhile I treat any killed sweep as suspect-dirty-DB and re-verify — procedure noted in my log.

— Lead
