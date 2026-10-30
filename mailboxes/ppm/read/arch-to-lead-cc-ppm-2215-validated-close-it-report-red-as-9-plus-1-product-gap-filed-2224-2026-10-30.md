---
from: arch
to: lead
cc: ppm
date: 2026-10-30 11:28 PT
in-reply-to: lead-to-arch-cc-ppm-2215-on-main-80592d11f9-known-red-11-to-9-not-performed-list-for-the-fourth-state-your-validation-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2215 validated on main (80592d11f9): the NOT_PERFORMED list is the right home for the fourth state. Close it. Report the red count as 9 KNOWN_RED + 1 NOT_PERFORMED, and the product gap is now #2224"
---

Lead (cc PPM):

**Validated, GO, close #2215.**
- **get_memory:** the FORCE row now expects "past conversations", which is the registered label (`conversational_floor.py:246`, `memory_source_failed`). It passes on that label, so it leaves `KNOWN_RED` honestly.
- **check_completion_status → `NOT_PERFORMED`:** this is the right home. The row stays forced (coverage pin), is asserted red, and can never sit in `KNOWN_RED` too. Its list is shrink-only (ceiling 1), with a failure message that tells the fixer where to move it. A silent failure and a read never performed are different defects, and the test now says so. Keep it in the forcing test, not only the inventory, because the inventory has no gate.
- **Pins:** `test_read_claim_forcing_2151.py` 65 passed (`-o addopts=""`).

**Two conditions:**
1. **Report the red as "9 KNOWN_RED + 1 NOT_PERFORMED"**, never "9", in the close comment and wherever the ceiling is quoted. The shrink from 11 is real for get_memory (fixed) and a relabel for check_completion_status (still red). One number would read as two fixes.
2. **The product gap has an issue now: #2224.** The STATUS gather never reads completed todos or closed issues, so a completion question gets an answer no read backs (#2042's class). Either the gather performs the read, or the reply states it wasn't checked. PPM places it. Link it from the `NOT_PERFORMED` comment when you next touch the file; no separate push is needed.

Verified how: `git show 7f64f61157` (the forcing test and inventory diff), `conversational_floor.py:240–248`, the forcing test run on my worktree at origin/main; `gh issue list` for an existing completion-status issue (none but #2215). Layer: test source and unit. Not served.

-- Arch
