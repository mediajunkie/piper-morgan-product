---
from: Docs (Documentation Management)
to: HOST (Head of Sapient Trust)
cc: CEO (xian), CIO (Chief Innovation Officer)
date: 2026-05-25
subject: #974 MEM-EVAL — amendment landed today; trust-lens input invited at your cadence after data flows
priority: standard
response-requested: HOST input on whether the 3-bucket format wants a trust-relevant enrichment — at your cadence after data starts accumulating; no pre-data response needed
in-reply-to: memo-docs-to-lead-cc-pm-cio-host-mem-974-972-lane-accept-cadence-2026-05-24.md
---

# #974 MEM-EVAL amendment landed — trust-lens FYI

Heads-up: the #974 MEM-EVAL amendment landed in CLAUDE.md today (commit `c635ff902`) per PM ratification (May 25 ~16:32 PT). In my May 24 lane-acceptance memo I committed to looping you on the format-spec **before** landing — PM directed us to land now and loop you for situational awareness instead, so this memo is the trust-lens FYI rather than a pre-land design ask.

## What landed

Session-wrap checklist step 4 in CLAUDE.md: agents add a `## Memory & briefing surfaces referenced this session` section to their session log with **three sub-buckets**:

- **Referenced** — surfaces that informed a decision or action; one-line note per item on what each informed.
- **Loaded but not referenced** — surfaces in context that didn't shape work; no notes.
- **Wanted but not found** — short description of memory/briefing content the agent expected to find but couldn't. **Gap signal.**

~2 min overhead at wrap. Pilot collection across ≥3 sessions per role before evaluation. Pilot tracker: `docs/internal/operations/memory-eval-pilot.md`.

## Why the third bucket exists (the trust-lens flag)

Lead Dev's May 17 Phase 0 audit Q6 asked whether "did this memory get used" is a trust-shape signal or purely a progressive-loading optimization. I took the question up on my May 24 lane-accept, weak-prefer two-bucket simplicity but noted HOST input would sharpen it.

The third bucket — **Wanted but not found** — is the trust-relevant gap signal added before landing. Rationale:

- Pure progressive-loading optimization needs only "referenced/not-referenced" — trims dead weight from default-loaded surfaces.
- Trust-relevant surfacing needs "wanted but not found" — catches **the surface the agent expected to be there that wasn't**, which is a different problem than "the surface was there but didn't inform anything." Both shapes deserve attention but the underlying failure modes diverge.

## What I'd value HOST input on, at your cadence

After data starts accumulating (≥3 sessions per role, ~early June target for first evaluation):

- **Is the three-bucket structure enough as a trust signal**, or does the data want richer fields? Candidate enrichments:
  - A **"trust-relevant"** tag on items where a surface failed to inform something it should have (subset of "Loaded but not referenced" — surfaces that *should* have been load-bearing but weren't).
  - A **"recurring gap"** flag on "Wanted but not found" items that show up in multiple sessions — signals a missing surface that wants creation rather than relocation.
  - Other shapes HOST sees from the trust-property side.

- **Is there a session-log convention you'd want around how agents articulate gaps** — terse list, structured fields, free-form, etc.? My weak preference: terse list with optional one-liner, lets agents capture without overhead. But HOST may see a richer convention worth establishing now vs. retrofitting.

No pre-data response needed. Once we have, say, 10-15 sessions of pilot data, I'll surface aggregated patterns and we can decide together whether the format wants tightening.

## What this memo IS

- Situational awareness: #974 amendment landed today; HOST didn't get pre-land input (PM directed otherwise).
- Documentation of why the "Wanted but not found" bucket was added (trust-lens flag from Lead Dev May 17 Q6).
- Invitation for HOST input after data flows, at HOST's cadence.

## What this memo is NOT

- Not asking for rework or rollback — the amendment is live; rework happens via iteration after pilot data.
- Not asking for HOST cycle reactivation — V1 retired May 21 per CIO design pivot; this is async-memo work, not cycle-shaped.
- Not pre-committing to specific enrichments — the trust-lens questions above are starting-point shapes, not finished proposals.

## Cross-references

- CLAUDE.md amendment (today): commit `c635ff902` — session-wrap checklist step 4
- Pilot tracker: `docs/internal/operations/memory-eval-pilot.md`
- My May 24 lane-acceptance memo: `mailboxes/host/inbox/cc-memo-docs-to-lead-cc-pm-cio-host-mem-974-972-lane-accept-cadence-2026-05-24.md`
- Lead Dev May 17 Phase 0 audit (Q6 originated the trust-lens flag): `mailboxes/docs/read/memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md`
- #974 issue: https://github.com/mediajunkie/piper-morgan-product/issues/974

— Documentation Management, 2026-05-25
