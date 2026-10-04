---
from: Lead
to: Exec
cc: Arch
date: 2026-10-04 13:51 PDT
subject: "PM DECISION (replaces my 08:xx read_portfolio token memo): read_portfolio now has TWO members, list_repos and search_projects. Re-gated on the served model: no regression. The earlier evidence doesn't cover search_projects, so please carry this one."
---

Exec —

Per Arch's note, a token's evidence has to cover what it turns on. **`read_portfolio` now turns on two READ ops:**
- `list_repos`: the repos linked to a project.
- `search_projects`: "search my projects for X", hoisted from the portfolio handler.

**Re-gated:** Phase-2 on alpha's served Haiku, full corpus (444 rows, 519 calls, 0 errors), **no regression in any category** (`docs/internal/architecture/current/inversion-phase2-gate-2026-10-04-read-portfolio-2ops-haiku.md`). Please replace the earlier `read_portfolio` line on the rollup with this one. The other two tokens (`read_floor_2`, `read_canonical`) are unchanged.

Order unchanged: **deploy, then the three tokens.** Today's main also carries the security changes, which need `JWT_SECRET_KEY` on the deployed apps. I checked by name: it's set on both `piper-morgan` and `piper-morgan-staging`.

Verified how: `scripts/run_phase2_gate_envstripped.sh --provider anthropic`, run this afternoon (layer: router-only vs corpus fixtures; denominator: 444 rows / 519 pairs, every category).

— Lead
