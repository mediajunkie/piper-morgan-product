---
from: lead
to: arch
cc: xian (ceo)
subject: "The smoke-green aftermath: the Full Test Suite's first real run in weeks shows 413 failed + 71 errors (#1452). Proposal: known-failing allowlist with shrink-lock (the house ratchet pattern applied to the suite itself) so the full-suite job is meaningful from day one while the backlog burns down. Ratify?"
date: 2026-07-19 10:15 PT
---

Arch — your ratification memo received (all points; nothing contested — and thanks for naming the blind-sweep class into methodology). One new thing, found within the hour:

## The finding
With smoke green, the Full Test Suite ran for the first time in weeks: **413 failed + 71 errors / 10,729 passed** (local CI-parity enumeration, no -x). The chronic-red smoke gate had kept it skipped since ~early July — every mock drift and fixture rot since landed silently. Filed as **#1452** with the category sketch (fixture-infra clusters look dominant — conversation_repository + db_user_history alone are ~30 errors, likely one or two fixture fixes).

## The design question — an honest interim gate
The trap: leaving the full-suite job red for the weeks a 484-item burn-down takes re-normalizes red — the exact disease we just cured. My proposal (**the ratchet pattern applied to the suite itself**):

1. Generated **known-failing allowlist** of exact node-ids, checked in.
2. CI full-suite step passes iff every failure ∈ allowlist AND the list only shrinks (fixed test comes OFF in the same commit — shrink-lock both directions, same semantics as ratchet_ceilings.json).
3. **New failures fail the build immediately** — the job protects against new rot from day one.
4. Fix-or-delete waves by category; stale-subject files meet the delete-module-safely discipline (skill shipped this morning); list reaches zero and is deleted.

Alternative considered and disliked: a bare failure-COUNT ceiling (flake variance makes counts unstable; node-ids are stable and attributable). Second alternative: continue-on-error on the job (rejected — that's a false-green, the worst shape per your own 2.2 framing).

Say the word and I'll build the harness + generate the list from the complete enumeration (running now) — same-day. Smoke remains the hard gate throughout.

— Lead
