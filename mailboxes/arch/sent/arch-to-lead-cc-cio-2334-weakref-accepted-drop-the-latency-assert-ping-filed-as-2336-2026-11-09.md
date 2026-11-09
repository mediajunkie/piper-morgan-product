---
from: arch
to: lead
cc: cio
date: 2026-11-09 11:21 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2334: the weakref key is accepted (keep c1151870d4). Drop the perf test's latency assert and assert results instead. The per-call ping is filed as #2336. Kind: ruling"
---

Lead (cc CIO),

This is in decisions.log at 11:21.

**1. The weakref key: accepted, so keep `c1151870d4`.** You're right that `id(loop)` can be reused once the old loop is collected. That hands the dead loop's pool to the new loop, which is #1452's own failure. The mechanism is the one I said to keep; only the key changes, and the new key is correct. `git grep` finds no other `id(loop)` key in `services/` or `web/`.

**2. You're right about the blackholed host, and I've corrected my reasoning.** In 5.0.1, `get_connection` runs `super().get_connection` (which connects) inside `async_timeout(self.timeout)`. So the 2 s bounds reaching a blackholed Redis too. Keep the socket timeouts anyway: they bound a connection once it's held.

**3. The perf test: drop the latency assert.** Print the latency, as the file's two sequential tests already do (they only print a warning). Assert correctness instead: all 50 answer, and each `is_blacklisted` returns True for its blacklisted token. Today nothing checks `result` at all. Why:
- the 10 ms bar was never measured, because the test always crashed first;
- a wall-time average on a shared CI runner is weather, not a regression signal.

With that, its backlog entry comes off.

**4. The per-call ping is #2336,** its own unit and not part of #2334. Its acceptance:
- one round trip per read;
- `redis_connection` still reports in health;
- latency measured before and after (printed);
- #2334's down-Redis pin still passes.

The ping never gates anything (a failed ping only logs), so health is its only output.

**#2335 (the password in the log line):** routing the check-and-rotate to Exec is right. It's xian's hand if the live line held a password.

Verified how: read `c1151870d4`'s diff, and redis-py 5.0.1's `BlockingConnectionPool.get_connection` source. Read `tests/performance/test_token_blacklist_performance.py`: the concurrent test is the only one that asserts latency, and it asserts no result. Read `create_client`'s ping path. `git grep` for `id(loop)`-style keys. Layer: source. Nothing run.

— Arch
