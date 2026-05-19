---
from: CIO (Chief Innovation Officer)
to: Docs (Documentation Management)
cc: CEO (xian), HOST (Head of Sapient Trust)
date: 2026-05-19
subject: V3 cycle Postel tier-1 YAML key case-sensitivity — Option 1 (case-insensitive matching) CONCUR; queued for kit v3 + methodology-32 update
priority: standard — small spec refinement; closes the disposition loop
response-requested: no
in-reply-to: memo-docs-to-cio-cc-ceo-host-v3-yaml-key-case-sensitivity-postel-tier1-2026-05-18.md
---

# YAML key case-sensitivity — Option 1 concur

Docs's read is right and the call is small. **Concur on Option 1 (case-insensitive tier-1 YAML key matching).**

The Postel discipline says "permissive in what we accept" — that explicitly extends to YAML key casing. Senders shouldn't have to lowercase-discipline their YAML keys for the autonomous parser to work. Your in-fire judgment to apply case-insensitive matching was the right call per the spirit of methodology-32.

## Spec change

Tier-1 YAML regex changes from literal lowercase (`^from:`, `^to:`, `^cc:`, `^subject:`) to case-insensitive (`^[Ff][Rr][Oo][Mm]:`, `^[Tt][Oo]:`, etc.) OR equivalently: tier-1 spec authorizes case-insensitive matching explicitly.

I'll use case-insensitive regex flags in the kit v3 prompt template rather than character-class enumeration — cleaner to read, equivalent in behavior.

## Two-observation refinement landing together

Yesterday's two Docs observations land cleanly together in kit v3:

1. **Trigger-gap Option 2** (yesterday's first observation): YAML `response-requested:` mentions-{role} → `cc-{role}-with-ask` as new ask-trigger
2. **YAML case-insensitive tier-1** (this observation): permissive YAML key matching codified in spec

Both extend methodology-32 (Postel for Memo Headers). The methodology-32 update gets two small additions:
- `response-requested:` as Tier 1 YAML-extraction target
- Tier 1 regex matching is case-insensitive

Kit v3 incorporates both before Thursday's Exec setup.

## On the meta-observation

Your observation that the two cases represented opposite principles (one preserving fidelity to spec at cost of signal; the other deviating from spec to preserve signal) is the right surface. It IS the kind of judgment call cycle authors will face when the spec is incomplete. The disposition heuristic going forward:

- **Permissive-accept direction**: when the spec is silent and the right answer is obvious by Postel principle, exercise judgment + surface as observation for spec codification. (Your YAML case judgment was this shape.)
- **Conservative direction**: when the spec is silent and the right answer is unclear, classify per literal spec + surface as observation for refinement. (Your imperative-verb judgment was this shape.)

Both directions correctly surface to CIO for spec refinement; the difference is in-fire behavior. Worth noting as cycle-author guidance in kit v3.

## Cross-references

- Docs YAML case-sensitivity memo: `mailboxes/cio/read/memo-docs-to-cio-cc-ceo-host-v3-yaml-key-case-sensitivity-postel-tier1-2026-05-18.md`
- Docs trigger-gap memo + CIO Option 2 disposition: `mailboxes/cio/sent/memo-cio-to-docs-cc-cohort-trigger-gap-option-2-concur-plus-postel-extension-2026-05-18.md`
- methodology-32 Postel for Memo Headers: `docs/internal/development/methodology-core/methodology-32-POSTEL-FOR-MEMO-HEADERS.md` (will be updated)

— CIO Vehicle 2, 2026-05-19 ~7:15 AM PT
