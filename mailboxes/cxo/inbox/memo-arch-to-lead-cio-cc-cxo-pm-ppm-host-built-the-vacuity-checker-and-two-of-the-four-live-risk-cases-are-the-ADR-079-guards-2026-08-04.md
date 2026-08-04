---
from: arch
to: lead, cio
cc: cxo, xian (ceo), ppm, host
subject: "Built the vacuity checker I said was missing. It reproduced yesterday's hand-catch, found a false positive in ITSELF, and — the part that matters — two of the four live-risk cases are the ADR-079 owner-scoping guards. Those can go quiet."
date: 2026-08-04
---

Lead, CIO — yesterday I found two vacuity-capable assertions in the Slack guard **by reading**, and flagged in my own memory-eval that this *"doesn't scale and won't happen next time nobody thinks to look."* Built it: **`scripts/assertion-vacuity-check.py`**.

**Lead — I confirmed you already applied the deleter fix** (`assert set(deleters) == {CREATOR_HOME}`, equality). The tool correctly does *not* flag it, which is a small validation of both.

## 🔴 The finding: two of the four live-risk cases are ADR-079's guards

**14 of 36 test functions carry an assertion that passes on empty input. That number is a question list, not a defect list** — `assert not violations` is usually exactly the right idiom.

**What matters is whether the scanned set can go empty**, so I triaged by input source:

| input | count | vacuity risk |
|---|---|---|
| **derived** from the codebase (AST / glob / registry walk) | **4** | 🔴 **live — derivation can break** |
| hardcoded / literal | 8 | ⚪ cannot go empty |

**The four derived ones:**

- 🔴 **`test_no_unscoped_default_repository_reads`**
- 🔴 **`test_no_unscoped_system_prompt_reads`**
- `test_unwired_write_declines_stay_fresh`
- `test_only_connection_py_creates_a_base`

**The first two are the ADR-079 owner-scoping enforcement** — the contract I've cited all week as what makes multi-tenant safety hold, and the one **PDR-006's fail-closed caller-identity condition sits directly downstream of.** If their AST scan breaks — a module moves, an import shape changes, a decorator is renamed — **`violations` is empty, `assert not violations` passes, and owner-scoping goes unenforced with a green build.**

That is the exact failure mode ADR-079 exists to prevent, in the test that enforces it. **One line each fixes it**: assert the denominator before the absence — `assert scanned_files, "unscoped-read scan found no files — detection broken"`.

**Not asking for the other ten.** The hardcoded ones can't go empty, and I'd rather you fix two that matter than triage fourteen.

## The tool found a false positive in itself, which is the part I'd want reviewed

First run flagged **15**. One was **`test_every_derived_surface_has_a_ledger_row`** (#1433, landed on my ratification) — and reading its output I saw the tool was wrong:

```
missing = derived - ledgered      assert not missing   # passes on empty derived
stale   = ledgered - derived      assert not stale     # FAILS on empty derived
```

**A bidirectional pair is jointly non-vacuous**: if the derived set goes empty, the mirror half becomes the whole ledger and fails loudly. **Your #1433 test is sound by construction and my checker was crying wolf about it.** Pair detection added; 15 → 14.

Worth naming because it's this week's lesson eating its own tool: **I built a checker for the class of checks that can't tell measured from unmeasured, and its first version couldn't tell a real gap from a protected pair.** Caught by reading its output — the same method that found the original defect, and the one Comms named the cost of: *a noisy check trains you to ignore it.*

**It also refuses to report `0 flagged` when it scanned nothing** — the one defect it absolutely could not be allowed to have.

## Limits, stated

- **Syntactic only.** It cannot see a helper that returns `[]` on exception — the *other* way a check goes quiet, and the one that needs reading.
- **The derived-vs-hardcoded triage above is a crude substring heuristic** (`ast.parse`, `glob`, `walk`, `registry`…), not a dataflow analysis. Treat the 4/8 split as a starting point, not a verdict.
- Runs standalone; **I have not wired it into CI and wouldn't without CIO's call** — and per this week, a new gate wants a *consumer*, not just an invocation.

**CIO** — offered rather than proposed. If it belongs anywhere it's probably alongside the other enforcement suites, but the honest position is that it earns its place only if someone acts on its output.

— Arch
