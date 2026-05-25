# Memory & Briefing Surfaces — Eval Pilot (#974 Data Collection)

**Status**: Pilot data collection — launched 2026-05-25 per #974 MEM-EVAL (Docs lane).
**Owner**: Documentation Management (Docs).
**Cross-reference**: CLAUDE.md "Session wrap-up checklist" step 4 (memory eval).

## Purpose

Capture which memory files, briefing docs, methodology docs, patterns, ADRs, and other context surfaces actually inform agent work — and which sit in context unused or are wanted-but-missing. Pilot data feeds two downstream decisions:

1. **Progressive-loading optimization** — which surfaces are load-bearing vs. dead weight? Can we trim what nobody references?
2. **Trust-property surfacing** (HOST lens) — when "memory not used" is a trust gap rather than just an optimization signal. If a surface that should be load-bearing is consistently not referenced, that's a different problem than a surface that's stably dead.

## Format (mirrors CLAUDE.md session-wrap step 4)

Each session log gets a `## Memory & briefing surfaces referenced this session` section with three sub-buckets:

- **Referenced** — surfaces that informed a decision or action this session. One-line note on what each informed.
- **Loaded but not referenced** — surfaces in context that didn't shape work this session. No notes needed.
- **Wanted but not found** — short description of memory/briefing content the agent expected to find but couldn't. Gap signal.

## Pilot scope

- **Duration**: collection runs across ≥3 sessions per role before evaluation.
- **Coverage**: all roles that produce session logs (per `dev/YYYY/MM/DD/` schema).
- **Evaluation target**: ~3 weeks after pilot launch (early June), once enough data has accumulated.

## What Docs does at evaluation time

- Aggregate the three buckets across the pilot session corpus.
- Identify surfaces consistently in "Loaded but not referenced" — candidates for progressive-loading trim or relocation to demand-loaded.
- Identify surfaces consistently in "Wanted but not found" — candidates for surface creation, relocation, or briefing additions.
- Surface trust-relevant patterns (HOST lens) — surfaces that should be load-bearing but aren't being referenced.

## Cross-references

- #974 issue: https://github.com/mediajunkie/piper-morgan-product/issues/974
- Lead Dev May 17 Phase 0 audit: `mailboxes/docs/read/memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md`
- Lead Dev May 24 routing memo: `mailboxes/docs/read/memo-lead-to-docs-cc-pm-cio-mem-cluster-974-972-routing-2026-05-24.md`
- Docs lane-acceptance memo: `mailboxes/docs/sent/memo-docs-to-lead-cc-pm-cio-host-mem-974-972-lane-accept-cadence-2026-05-24.md`
- CLAUDE.md session-wrap checklist step 4 (the amendment landing this pilot)

— Documentation Management, 2026-05-25
