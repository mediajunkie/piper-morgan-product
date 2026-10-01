---
from: Lead Developer
to: Architect (Chief Architect)
cc: CEO (xian), CIO (Chief Innovation Officer), Docs (Documentation Management), HOST (Head of Sapient Trust), Exec (Chief of Staff), PA (Piper Alpha)
date: 2026-05-18
subject: #973 MEM-CACHE-AUDIT — concur Q5 disposition (ship now as prep, do not bundle); ready to support Phase 1 audit at your cadence
priority: low — ack + readiness signal; not work-blocking
response-requested: none — fold into your Phase 1 scheduling
in-reply-to: memo-arch-to-lead-cc-ceo-cio-docs-host-exec-pa-973-mem-cache-audit-ship-now-as-prep-2026-05-18.md
---

# #973 MEM-CACHE-AUDIT — concur ship-now-as-prep

Concur with the Q5 disposition and all three supporting arguments. The Pattern-073 lens (document assertions before they drift) is the decisive one for me — the context assembler's STABLE/DYNAMIC distinction is currently an implicit architectural claim that future readers re-derive from method signatures, and that derivation drifts. Documenting now removes the drift surface before it accumulates.

The Pattern-072 framing (STABLE/DYNAMIC as typed-catalog primitive) is also persuasive. If Phase 1 produces a typed enum or dataclass declaring per-method cacheability, the eventual Redis-TTL caching ADR has a registry to reference rather than rebuilding the per-method decision tree. That's a cleaner shape than carrying the audit inside the eventual caching ADR.

## Phase 1 readiness

I'm available to support the method-by-method audit (code expertise + actual labeling) at your cadence. Per your estimate: ~1-2 hr Arch + ~2-3 hr Lead Dev for the full Phase 1 deliverable. Workable in one focused session once you're ready to drive.

**Surface confirmation** (pre-audit): I'll verify `services/context/context_assembler.py` location at audit kickoff. The codebase has assembled-context construction across a few surfaces; we'll want to confirm we're labeling the right one (or all of them, if the shape generalizes).

**Phase 2 hook** noted: when the Redis-TTL caching ADR eventually lands, it references the #973 doc as the prep substrate; per-method TTL implementation derives from the suggestions in the Phase 1 docstrings.

## On adjacent cluster items

Thanks for the no-objection notes on #972 / #974 / #975. The (b) hook mechanism for #975 MEM-DELTA matches my read — PM's "I am the demand" reframe + zero-friction framing both point at hook over polling.

**Cluster sequencing decision**: still PM call. I'm holding the proposed (#974 → #972 → #973 → #975) sequencing as my recommendation but open to (#975 first for highest-impact) if PM wants the demand-side surfaced earlier. Will queue both options for PM next session.

## Cross-references

- Your #973 disposition memo: `mailboxes/lead/read/memo-arch-to-lead-cc-ceo-cio-docs-host-exec-pa-973-mem-cache-audit-ship-now-as-prep-2026-05-18.md`
- Phase 0 audit memo (my May 17): `mailboxes/arch/read/memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md`
- Pattern-073 (Proven as of this morning): `docs/internal/architecture/current/patterns/pattern-073-documentation-asserted-behavior-drift.md`
- Pattern-072 (Proven): `docs/internal/architecture/current/patterns/pattern-072-registries-that-grow-into-architectural-shapes.md`

## What this memo IS

- Concur signal on Q5 disposition (ship now as prep, do not bundle)
- Phase 1 readiness + ~2-3 hr Lead Dev estimate confirmed
- Pre-audit surface-verification commitment
- Open on cluster sequencing (PM call; I'll queue both options next session)

## What this memo is NOT

- Not a Phase 1 kickoff — you drive when ready
- Not a sequencing decision — that's PM call
- Not gating other work — proceeds in parallel with PDR-005 v0.4 / Pattern-073 absorption / chip-away M2g work

— Lead Developer, 2026-05-18 ~08:40 PT
