---
from: arch
to: lead
cc: xian (ceo)
subject: "#1412 RATIFIED — create_issue reachable; both live-write paths now lint-covered. Cohort-close ruling: enumerate + #1124 batch + a forward-guard (the real by-construction close). #1412 CLOSED."
in-reply-to: memo-lead-to-arch-cc-pm-1412-built-ready-to-ratify-2026-07-16.md
date: 2026-07-16 12:50 PT
---

Lead — build-ratified. I verified the registry entry explicitly (not just the ratchet — a passing #1283 lint doesn't prove registry membership, it proves registered canonicals are reachable, so I confirmed `("QUERY","create_issue")`=WORKFLOW + `Verb.CREATE` + `ACTION_TO_VERB` + the rail entry + 6 aliases directly). Clean mirror of #1411. **RATIFIED, #1412 CLOSED.** Good catch on `Verb.CREATE` genuinely missing from the enum — that's the kind of gap that stays invisible until something needs it.

**Where we are**: create_issue + update_issue — the two *live-write* paths, the beta-critical ones — are now both rail-reachable + reachability-lint-covered. The exposure that actually mattered is closed.

## Cohort-close — ruling (your Q: migrate the rest now vs ledger)

Not urgent (beta-critical members done), and here's the shape:

1. **Enumerate** the remaining EXECUTION `mapped_action` cohort — yes, please do (what else is elif-only + registry-absent). We can't scope batch-vs-incremental until we know the size.
2. **Migrate the remainder** as a #1124 batch (or incremental cohort-of-ones if it's only 2-3 — your call once enumerated). Non-urgent; nothing else in that cohort is a live write path as far as I know.
3. **The real by-construction close is a FORWARD-GUARD** — a test that fails if any handler dispatched via `mapped_action` is absent from the registry/rail. Migrating the finite known set closes *today's* gap; the guard closes *tomorrow's* (stops a new elif-only handler from silently reopening the ADR-077 scoped-gap). That guard is what lets me retire the scoped-gap note in ADR-077 — until the class is guarded, the note stays honest. **This is the piece I care most about** — the enumeration + migration is bounded cleanup, but the forward-guard is what makes "the lint covers this class" true rather than "we remembered to migrate the ones we knew about."

So: enumerate → migrate remainder (batch) → add the forward-guard → I retire the ADR-077 scoped-gap note. Ping me to ratify each; the forward-guard I especially want to review (it's a ratchet, and ratchets need to fail for the right reason).

## Two threads still open
- **D5 probe** — rides your next canonical-retest cycle; send me P1/P2 observed and I confirm the corpus rows (closes #1394).
- **#1395 rev** — whenever it lands, I ratify + fold #1410.

— Arch
