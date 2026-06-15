---
from: Lead Developer
to: Architect
cc: PM (xian), CIO
date: 2026-06-15
subject: RE #1241 — framing confirmed (refinements A+B folded); audit starting now; ADR-071 I'll author post-audit
in-reply-to: memo-arch-to-lead-cc-cio-pm-1241-content-anchoring-lens-adr-071-yes-doc-store-first-2026-06-15.md
priority: standard — confirmation + kickoff
response-requested: none now — I'll loop you at ~half the stores classified
---

# Confirmed + starting

Concur on all four. Folding both refinements:
- **A — two-axis classification**: ownership-at-write (a stamped / b post-hoc / c never) × scoping-at-read (1 by-principal / 2 post-hoc / 3 never). Doc store = (c, 3); conversations = (a, 1) per #849. The 2×2 makes remediation cost legible — exactly right.
- **B — auth-resolution sub-inventory**: separate pass for where the principal originates and where it degrades to `Optional` mid-chain (the `conversation_handler.py` `intent.context.get("user_id")` shape). Read-side completeness.

Confirmed:
- **No bespoke doc-store fix** — holding it as ADR-071's first migration instance. Audit → ADR → worked-example.
- **ADR-071 authorship**: I'll author post-audit (context fresh); you ratify. Your D1–D7 strawperson is a strong starting frame — I'll ground it in the inventory evidence rather than pre-committing.
- **Loop point**: I'll send you the half-done classification (≈half the stores) for empirical ADR-071 scoping before I go further.

Starting the inventory now. — Lead, 2026-06-15
