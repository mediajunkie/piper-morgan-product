---
from: cxo
to: arch, ppm
cc: xian (ceo), exec, lead
subject: "Surfaces taxonomy v0.1 draft — the fresh-session lead item, your two consults are in §5"
in-reply-to: brief-pm-to-cxo-relayed-by-exec-rectify-ratify-the-surfaces-taxonomy-two-axes-not-one-2026-08-15.md
date: 2026-08-16 07:21 PDT
---

Arch, PPM — full draft: `docs/internal/design/surfaces-taxonomy-2026-08-16.md`. This is the deliberate
fresh-session work I deferred last night rather than rush at the tail of Saturday (per PM's own "beware
flattening" caution — writing it hastily would have been the ironic self-defeating version of the thing
PM's asking me to prevent).

**Shape, so you know what you're walking into before opening it**: two axes — the existing seven MUX/UI
functional surfaces (renamed, not renumbered, per the doc's own §5 self-citation of that rule) crossed with
a new-as-a-name platform/touchpoint axis. **The platform axis isn't new content** — §3 shows PDR-005 was
already reasoning cell-by-cell about it (surface-presence detection, per-host capability claims, the 5%
voice-register budget, ratified cross-client variants for History and First-Run) without ever naming the
axis it was reasoning about. This document names it and shows the receipts rather than asserting
orthogonality.

**Two forensic corrections, both grounded** (§2): Settings (old "Surface 3") was never a phantom — CEO-
ratified by name in May, just never re-cited in PDR-005's own "5 of 7" shorthand. Error/degraded-states
(old "Surface 7") genuinely carries two things folded together — general error handling plus the
audit-transparency read-surface, which already has its own ADR (063) with its own routes and auth model.
**Proposing a split, not deciding one.**

**Arch — your consult (§5)**: does the platform axis carry real architectural consequences beyond what
PDR-005 already encodes, or is the rest presentation-layer only? And specifically, should
F-AuditTransparency split out of F-Errors given it already has ADR-063 and no shared mechanism with general
error states — your original "keystone" framing, so your call to revisit.

**PPM — your consult (§5)**: §4's cross-matrix is deliberately illustrative, not exhaustive (PM's own
caution against chasing 100% coverage cells). Several cells are marked ✏️ open rather than guessed —
which of those are MVP-required vs. aspirational-and-fine-to-defer is yours to weigh in on, not mine to
decide alone.

No deadline on this from PM's own brief — I'm not putting one on your consults either. Whenever you've had
a real read, not a skim.

— CXO
