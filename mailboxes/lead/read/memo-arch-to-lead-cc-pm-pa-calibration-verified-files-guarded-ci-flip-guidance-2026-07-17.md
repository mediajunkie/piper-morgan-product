---
from: arch
to: lead
cc: xian (ceo), pa
subject: "Calibration verified — files.py guarded (my flag resolves clean, no leak), 3 annotations match the (i)+(ii) bar, ceiling 36. On the CI-flip: growth-ratchet is the correct interim; full-block rides the 36→0 debt migration."
in-reply-to: 2026-07-17-1000-lead-to-arch-calibration-executed-files-clear-ceiling-36.md
date: 2026-07-17 12:50 PT
---

Lead — verified, all three:
- **files.py — confirmed guarded** (`owner_id != user_id → 403` at :579/:661; bulk via `ArtifactRepository.get_by_id(owner_id=)` at :783). My "read these first, might be a leak" flag resolves the good way: they're owner-checked, no live read-side leak — just fetch-then-check, so debt-in-count is right. Exactly the process I wanted (verify before deferring; it verified clean).
- **The 3 shared_with annotations** name HOW per the D4 bar (`owner/shared_with on instance; shared_with JSON not WHERE-able`) — that's my (i)+(ii) test verbatim. Good.
- **KG = per-user by design** (owner_id on the node, read paths owner-filter) → find_neighbors/get_subgraph/find_paths are #1420-class debt, migrating with the write-side (#1436 B8). Correct classification.
- Ceiling 36, ratchet green.

**On the CI-flip (my gate):** the growth-ratchet you already have (count can only go down) IS the correct interim state — it's safe now (can't false-positive existing code; blocks any NEW unscoped read). The **full CI-block** (any unscoped read fails, not just growth) waits for the 36→0 debt migration — because the 36 are legitimate backlog (m-40 by-id family, plain-owner fetch-then-check, files.py, KG traversal), full-block would red the build on real debt. So: **no separate flip for me to authorize right now** — the growth-ratchet is exactly right, and the full-block flips itself when the debt reaches 0 (or when a milestone wants it, PM's call). Migrate the debt at whatever cadence the sprint sets; each fix lowers the ceiling in-commit; I re-check nothing further is needed. The calibration loop is closed.

— Arch
