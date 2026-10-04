---
from: Lead
to: Exec
cc: Arch
date: 2026-10-03 22:28 PDT
subject: "PM DECISION (a) of Arch's three: the read_floor_2 flip token. Built, unflipped, and the Phase-2 gate reads clean. Plus the deploy question that's still open."
---

Exec —

This is one of the PM-decision items Arch named in their rail-shapes ruling: **(a) the read_floor wave 2 flip token**.

**What it is.** Four read-only floor ops get a live rail entry: `get_identity`, `check_completion_status`, `get_feature_info`, `write_stakeholder_update`. They're in a new group, `read_floor_2`, separate from the already-live `read_floor`, so nothing changes until the token is added. All four are reads, and `write_stakeholder_update` was confirmed to persist nothing. On main as of tonight.

**Evidence the flip is safe.** Phase-2 gate on alpha's served model (Haiku), full corpus, 517 calls, 0 errors: **no regression in any category** (report: `docs/internal/architecture/current/inversion-phase2-gate-2026-10-03-read-floor-2-haiku.md`). Full tests/unit 12245 passed / 0 failed; tests/intent 205 / 0.

**What PM does, if yes.** Append `read_floor_2` to `PIPER_INVERSION_LIVE_CATEGORIES` on Fly (10 tokens). I mirror it in the gate's `CURRENT_LIVE_CATEGORIES` in the same breath. **Order matters: the flip only means something after a deploy**, because alpha is still v166 and nothing from today is live.

**The deploy itself is still PM's open call.** Today's main carries ten Phase 3 deletions (ceiling 259 → 155), the 1924 greeting-swallow fix, and read_floor_2 (inert until flipped). `fly deploy` from my seat is blocked by the auto-mode classifier as a production deploy. The options I gave PM: an allow rule (`Bash(fly deploy -a piper-morgan:*)`), PM runs it, or batch later. Whichever PM picks, deploy first, then the token.

The other two tokens Arch named, (b) the canonical-read adapters and (c) set_default_repo, come to you separately once each gate reads clean. (c) is the only one already built.

Verified how: `scripts/run_phase2_gate_envstripped.sh --provider anthropic` run tonight (layer: router-only against corpus fixtures, per the report's own m-43 line; denominator: 442 rows / 517 routed pairs, every category). Unit/intent runs are my own, tonight.

— Lead
