---
from: Lead
to: Arch
cc: CXO, PPM
date: 2026-10-04 11:47 PDT
subject: "Your 'delete the update/edit-project literals' can't be done as ruled: with them gone, 'edit my project description' lands on update_document_query 10/10, both legs. Not deleted. The gate would have allowed it, and that gap is 1933."
---

Arch —

I deposited the two rows as you ruled (`expected: floor`), scored them, and probed surface 2 before any deletion:
- **Router (Haiku): `update_document` on 2/2**, not floor.
- **Surface 2: `EXECUTION/update_document_query` on 10/10 samples, sonnet-4-6 AND gpt-4o.**

So deleting the literals would turn "update my project name to Atlas" into a document-update turn: a write on the wrong object. Today the pattern lands in the portfolio fallback, which is at least honest. **I haven't deleted them.**

**The part that matters more:** the gate credited both rows as safe through its **mis-serve rule** ("the pattern serves the wrong op, so deleting it can't make the fallback worse"). That premise fails when the fallback is a WRITE mis-route. The same rule ledgered one `misserved_at_deletion` row in each of the STATUS / TRUST / MEMORY / ANALYSIS deletions. **Filed as 1933** (MVP). I'm dispatching the fix now: the credit will require surface-2 evidence that no sample lands a WRITE or DESTRUCTIVE op. The lane will also re-verify those four ledgered rows against their probes and report any that fail, rather than passing them. Until it lands I'm not trusting PORTFOLIO's current "GO (partial), 14 deletable".

**For the dead claims themselves**, three options. Yours, with CXO on the copy:
- (a) Keep the literals and give `manage_portfolio` an honest "I can't edit projects yet" for update/edit, instead of the generic fallback. Small, honest, and the literal stays load-bearing.
- (b) Build an update-project op (PPM's product question).
- (c) Delete anyway once surface 2 is fixed to route there, which is a router/description problem.

My lean is (a) now, and (b) if PPM wants the capability.

Verified how: `scripts/inversion_phase1_shadow_score.py --provider anthropic --source-prefix phase3-conversion/PORTFOLIO_PATTERNS` and `scripts/inversion_phase3_surface2_floor_probe.py` (N=5 × 2 phrases × 2 providers), both wired into the gate. Layer: router + surface-2 classifier, not a live turn. Denominator: 2 rows, 20 surface-2 samples.

— Lead
