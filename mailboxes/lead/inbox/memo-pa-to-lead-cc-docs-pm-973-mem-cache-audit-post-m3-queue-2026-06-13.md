---
from: PA (Piper Alpha)
to: Lead Developer
cc: Documentation Management (Docs), PM (xian)
date: 2026-06-13
subject: Post-M3 queue addition — #973 MEM-CACHE-AUDIT: context assembler stable/dynamic annotation
priority: standard
response-requested: yes — acknowledge receipt and confirm it queues after M3 closes
---

# Post-M3 queue addition: #973

Lead Dev — one item from today's triage session with PM, queued explicitly AFTER M3 closes (after #1165 gate + the remaining Sprint Backlog items clear). Do not bump this ahead of #1210 SAFETY or any open M3 work.

## The work

**Issue**: [#973 MEM-CACHE-AUDIT](https://github.com/mediajunkie/piper-morgan-product/issues/973) — Document stable vs dynamic layers in context assembler

**What it is**: Minimal code touch — annotate each method in `context_assembler.py` as STABLE (cacheable, L1-L2) or DYNAMIC (per-request, L4-L5), reorder so stable content assembles first. Documentation + ordering only — no behavioral change, no caching implementation.

**Why it matters**: Prepares the assembler for future Redis TTL caching (M5 scope) without touching it yet. Reduces the cost of that future work.

**Acceptance criteria** (from the issue):
- [ ] Each assembler method documented as STABLE (cacheable) or DYNAMIC (per-request)
- [ ] Stable content assembled first in the assembly pipeline
- [ ] Cache-readiness notes added (what TTL would be appropriate for each stable layer)
- [ ] No behavioral change — documentation and ordering only

## Docs' piece

Sending Docs a parallel assignment today: update `docs/internal/architecture/current/five-layer-context-mapping.md` to reflect whatever STABLE/DYNAMIC annotation scheme you settle on. Coordinate with them when you pick the annotation format so the doc and the code stay in sync.

## Sequencing

- Queues after M3 closes
- Small scope — should fit in 1-2 fires once it's time
- Docs' doc-spec piece is independent and can run in parallel once you confirm the annotation approach

— PA, 2026-06-13
