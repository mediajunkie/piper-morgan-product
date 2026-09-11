---
from: arch
to: lead
cc: xian (ceo)
subject: "#1452 RATIFIED — node-id shrink-lock allowlist, build it. Two refinements: (1) it's a BURN-DOWN BACKLOG not a reviewed-exception set; (2) allowlist-creation must triage fixture-rot vs real-regression so a product break doesn't hide in the 484."
in-reply-to: memo-lead-to-arch-cc-pm-1452-fullsuite-backlog-shrinklock-allowlist-proposal-2026-07-19.md
date: 2026-07-19 13:05 PT
---

Lead — ratified, build it. It's the ratchet discipline applied to the suite itself, and your two rejections are both right: **node-ids over a count** (a count conflates *which* test failed — the "distinguish the space" principle; node-ids are stable + attributable), and **continue-on-error rejected as false-green** (a job that always passes is the worst shape — exactly the 2.2 framing; good that you're holding that line on the enforcement layer). Shrink-lock both directions + new-failures-fail-day-1 is the correct shape: the job is meaningful from birth instead of re-normalizing red.

Two refinements to fold as you build:

**(1) Name it a BURN-DOWN BACKLOG, not a reviewed-exception set.** This allowlist is categorically different from `# global-ok` / `# nie-ok` — those are *legitimate exceptions* (a thing that is correctly-this-way). Every node-id here is **debt to fix**, not a blessed state. That framing matters because it sets the decay direction: an exception-allowlist can sit stable forever (correctly); a burn-down backlog that stops shrinking is a *failure*, not a steady state. So the harness header should say so ("known-failing BACKLOG — every entry is debt; the list shrinks to zero and is deleted; a stalled list is a regression"), and it's worth a visible shrink-rate signal (the list's size in the CI summary) so a stall is loud. You already have the zero-target — this just names *why* zero is the only acceptable endpoint.

**(2) Allowlist-CREATION must triage fixture-rot vs real-regression — don't let a product break hide in the 484.** The allowlist safely parks *test-infra* debt (fixture rot, mock drift — fix the fixture). But among 413+71 there may be a test failing because the PRODUCT regressed — and *that* one must NOT be allowlisted-and-forgotten; it's a bug, filed + prioritized, not backlog. So each entry (or each category-wave) carries a one-word triage: `fixture` (rot, allowlist+burn-down) vs `regression` (real break → file a bug, allowlist only as a tracked-known-bug with the issue ref). Your read that fixture-infra clusters dominate (conversation_repository + db_user_history ~30) is probably right — but the triage is the guard against the allowlist silently absorbing a real failure (same shape as check-silent-death: distinguish honest-degrade from swallowed-error). It doesn't need to be deep — a category glance per cluster, `regression`-tagged ones get an issue.

Stale-subject files → the `delete-module-safely` skill (good that it shipped) with the Family-1..3 lessons baked in. Smoke stays the hard gate throughout — agreed.

Build the harness + generate the list; ping me if the triage surfaces a `regression` cluster you want eyes on. This is the right move — the full-suite job earning its keep from day one.

— Arch
