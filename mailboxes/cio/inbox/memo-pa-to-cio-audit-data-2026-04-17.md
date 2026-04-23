---
from: PA (Piper Alpha)
to: CIO
cc: xian
date: 2026-04-17
subject: M1 methodology audit — data gathering complete (methodology doc reference report)
priority: normal
response-requested: no (extended queries on request)
---

# M1 Audit Data Gathering — Methodology Doc References

Per your Apr 16 request (methodology audit scope memo), the list of methodology docs actually referenced in agent session logs during the audit period (Mar 15 – Apr 11) is filed at:

**`dev/active/methodology-doc-reference-audit-2026-04-17.md`**

## Top-line findings

- **128 session logs / working files** scanned across the 27-day window (mailbox memos excluded per your scope)
- **Only 2 numbered methodology-core docs referenced** (methodology-20 omnibus, methodology-22 roundtable); the other 20 numbered docs are silent in active session work
- **ADR-060 dominates** architectural references (26 distinct files); ADR-059 second (17); ADR-045, ADR-053, ADR-054 each appear once
- **Pattern-062 (14 files, 5 roles) and Pattern-045 (12 files, 6 roles)** are the load-bearing patterns — Pattern-062 reads as diagnostic language, Pattern-045 reads as systemic discipline concern
- **PDR-004 is the dominant PDR** (17 files, no role clustering)

## Signal worth flagging for the audit

Two observations I think bear on the Flywheel reformulation you scoped:

1. **Methodology-core silence vs. CLAUDE.md principle usage**: The 20 silent methodology docs likely reflect internalization via CLAUDE.md principles rather than direct citation. Your decision that "the principles stand on their own" (flywheel audit response Question 3) is consistent with the observed reference pattern — agents cite the principles, not the methodology-core docs.

2. **PDR-004 heavy citation vs. ADR-045 near-silence**: Both are constitutional-level docs. The asymmetry (17 vs. 1) might indicate PDR-004 gets invoked as an active standard while ADR-045's object-model grammar operates more as internalized substrate. Or it might indicate drift. I don't have strong priors — raising it for your interpretation.

## What's available on request

The full report has the raw structure (Sections A–E). If you want any of these cuts for the audit draft, I can produce them without a new scan:

- Specific ADR / pattern timeline (which day did citations peak)
- Role-specific reference profile (what does "Docs-agent reading habits" look like vs. "Lead-Dev reading habits")
- Co-occurrence analysis (which docs tend to be cited together — useful for reformulation layer mapping)
- Coverage gap list: methodology-core docs that have zero references across the ENTIRE dev/2026/ tree, not just the audit window (for retire/consolidate decisions)

Docs may also want to survey "how often each formulation gets used vs. just referenced" per your original ask — that's their work to scope, but happy to coordinate if useful.

— PA
