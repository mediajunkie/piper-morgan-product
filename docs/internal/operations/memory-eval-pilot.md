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

### ⚠️ "Wanted but not found" is a report about YOUR SESSION, not a claim about the repo (HOST, 2026-07-29)

**Write it in the experiential tense — "I looked for X and didn't find it" — never the existential — "X does not exist."** The bucket asks what you *wanted and couldn't locate*. That is a fact about your search. Whether the thing exists is a different claim, needs different evidence, and is the one that goes wrong.

**Why this rule exists**: HOST swept its own entries and found **3 of 5 negatives were false** — the surface existed, and in one case had been shipped **5.5 hours earlier by CIO** while HOST was recording it as missing. None were inherited from another agent; all three were self-generated in the ordinary course of writing the wrap.

The failure is structural, not sloppy. At wrap you are reconstructing the session from memory, under context pressure, and "I never came across X" compresses to "X isn't there" without feeling like an inference. The two are then indistinguishable on the page — and the existential reading is what a later reader acts on, because a gap report is *supposed* to drive someone to build the missing thing.

**How to apply:**

| write this | not this |
|---|---|
| "Looked for a PII-free aggregate tester view; didn't find one." | "There is no PII-free aggregate tester view." |
| "Wanted a per-commit vocabulary for coverage claims — as experienced this session, nothing supplied one." | "Nothing in the repo supplies a per-commit coverage vocabulary." |

If you *do* want to assert the existential — reasonable, it's more actionable — **verify it first and say you did**: "checked `docs/internal/operations/` and `gh issue list`; no such surface as of 2026-07-30." An unverified negative in a gap report is a work order pointed at nothing.

Same family as the never-guess-a-lookupable-fact rule and `feedback_verify_negative_claims_via_live_api`. Applies to any bucket asserting absence, not only this one.

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
