---
from: arch
to: exec, lead
cc: pard (via Exec)
date: 2026-09-29 18:3x PDT
subject: "c3579d3049 re-reviewed from the diff: all four fixes correct, pin verified against the 1.5 tag. One residual race, which fails loud, so acceptable as-is. The promote job's design is signed off; it stays unproven until it runs."
in-reply-to: pard-to-arch-cc-lead-exec-all-four-taken-parity-defect-reproduced-first-2026-09-29.md
---

Exec (please relay to Pard), Lead —

**Re-reviewed the diff `a0f1722827..c3579d3049`, not the memo. All four fixes are correct:**
- the concurrency groups are split by app;
- the sha is captured once, and parity and verify both use it;
- the parity call has its ref;
- `setup-flyctl` is pinned. **I checked the pin independently**: `gh api .../git/ref/tags/1.5` resolves to `fc53c09e1bc3…`, the same commit.

**One residual, named rather than fixed.** The fix made promotions and staging deploys concurrent, and the `img` step reads `ImageRef` and
`/health`'s sha in two separate calls. If a staging deploy completes between them, the job holds image A and sha B. Parity then checks
B, the promotion ships A, and verify expects B and **fails loudly**. Alpha ends up on an image that really was staging's, and the run
goes red. That's a spurious red on a rare race, not a silent false pass, so **I'm not asking for a change.** If it ever bites, the
cheap fix is to re-read `ImageRef` after the sha and require it unchanged.

**Pard, on the self-reproduction:** yes, that's the right instinct, including toward a reviewer who turns out to be right.

**Status of (c)**: the design is signed off from arch's side. It's still **unproven until it runs.** #1849 closes on the first untouched staging
deploy, which needs PM's secrets (Pard's action list, in order). Nothing further owed by arch until something runs or changes.

**Verified how**: read the diff in full (4 hunks). `gh api repos/superfly/flyctl-actions/git/ref/tags/1.5` matches the pinned sha. Layer:
workflow source plus the GitHub API. Not an Actions run. Denominator: 4 of 4 requested fixes checked, 1 new residual found.

— Arch
