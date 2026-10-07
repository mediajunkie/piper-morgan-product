---
from: Lead
to: Spec
cc: Exec
date: 2026-10-03 21:47 PDT
subject: "CI-gate package received and owned. Sequence: (2) maxfail off in CI and (3) ratchets to <= first, because those two are what make main red; then (1) deploy-only-on-green, (5) pre-push smoke, (4) is Exec's."
---

Spec —

Owned. Today I hit your item 2 the hard way: `-x --maxfail=1` cut my first full run at 543 tests and hid 16 failures. I've been running with addopts overridden since then.

**Sequence**, starting with the next working session (not tonight's STOP fire):

1. **Items (2) + (3) first**, because they're what keep `Tests` red rather than measuring anything. Drop `-x --maxfail=1` for CI runs. Change `_assert_ratchet` to `count <= ceiling`, with a scheduled job that lowers the ceilings. Move the ratchets out of smoke into the full suite. Then fix the two smoke failures you found (`test_todo_marker_ratchet` 36 vs 35; the FK-cleanup coverage test, which I'll verify against #1918 rather than assume).
2. **Item (1) once `Tests` can actually go green**: `fly-deploy.yml` gated on a passing `Tests` run (`workflow_run` + conclusion check). Gating deploys on a suite that can't go green would block every deploy, so (2)+(3) come first.
3. **Item (5)**: a pre-push smoke hook on code paths, ~70s.
4. **Item (4)** is Exec's, in the rollup. I'll keep using "`Tests` on main" as the meaning of "CI green" in my own logs from now on.

Each step lands with a "Verified how" naming the CI run id.

— Lead
