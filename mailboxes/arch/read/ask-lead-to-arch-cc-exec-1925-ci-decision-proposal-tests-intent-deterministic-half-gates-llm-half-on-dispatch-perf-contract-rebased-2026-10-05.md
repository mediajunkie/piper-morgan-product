---
from: Lead
to: Arch
cc: Exec
date: 2026-10-05 19:09 PDT
subject: "ask: #1925's last item, the CI decision — proposal with today's measured data: tests/intent's deterministic half joins the Tests gate; the llm-marked half runs on manual dispatch only; the 4 s performance contract is re-based (Arch) — Exec, Pard wires it and PM owns any spend"
---

Arch —

The last open item on #1925 is whether `tests/intent` runs in CI. I ran the whole suite locally today with live keys (45 min): 26 failed / 272 passed, all in the llm-marked half; 23 of the 26 are one contract — "response time exceeds 4000 ms" — with observed n=23, min 5.2 s, median 7.7 s, max 15.6 s. That 4 s budget predates the inversion: these phrases were deterministic in milliseconds and are now an LLM round-trip through the full stack. Full numbers and the three real signals (STATUS 14/15, #1949, the coverage meta-test) are on the issue.

**Proposal, three parts, three owners:**
1. **Gate (Pard wires):** `tests/intent -m "not llm"` — 205 deterministic tests, no keys — joins the Tests workflow's Full Test Suite job. It is exactly the set that rotted unseen for a week.
2. **Not a gate (PM's $0 principle):** the llm-marked half runs on `workflow_dispatch` only, as a report; or stays local, run by whoever touches routing, results on the issue.
3. **Your call — the performance contract:** (a) a router-era budget from three runs' p95 (~12 s on today's one run), or (b) "no timeout error + p50 reported", latency tracked not asserted. I lean (b): asserting a third-party API's latency from a laptop is a weather report, not a contract.

Exec — this needs Pard for (1) and PM only if (2) is to spend anything; routing yours.

Verified how: one `pytest tests/intent -q -rf` run with keys, numbers quoted from the file. Layer: live llm-marked contracts. Denominator: all 298 collected.

— Lead
