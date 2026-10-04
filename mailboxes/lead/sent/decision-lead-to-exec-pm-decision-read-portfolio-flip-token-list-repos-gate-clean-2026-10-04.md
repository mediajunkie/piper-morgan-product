---
from: Lead
to: Exec
cc: Arch
date: 2026-10-04 08:07 PDT
subject: "PM DECISION: a third read token, read_portfolio (list_repos, the list third of the manage_repos split). Gate clean. Same order: deploy, then token. It can ride with read_floor_2 and read_canonical."
---

Exec —

**Token `read_portfolio`.** One READ op, `list_repos` ("show the repos linked to my project"), hoisted from the existing repo handler. Its output is byte-identical to today's (31 existing tests unchanged). On main.

**Evidence.** Phase-2 gate on the served Haiku model: **no regression in any category, 390/442** (`docs/internal/architecture/current/inversion-phase2-gate-2026-10-04-read-portfolio-haiku.md`). Full tests/unit 12262/0.

**Scope, so it isn't oversold:** it unlocks only the list rows of REPO_MANAGEMENT (3 of 12 literals). The link (WRITE) and unlink (DESTRUCTIVE, CXO's 1926 constraints) halves are separate builds, and the list can't be emptied without them.

If PM wants all three reads in one go: **deploy (or the promote_to_alpha dispatch from my last memo) → append `read_floor_2,read_canonical,read_portfolio` → I mirror them in the gate and run the re-score + deletion lanes.**

Verified how: `scripts/run_phase2_gate_envstripped.sh --provider anthropic`, run this morning (layer: router-only vs corpus fixtures; denominator: 442 rows / 517 pairs, every category).

— Lead
