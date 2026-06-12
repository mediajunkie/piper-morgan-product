---
from: Lead Developer
to: Chief Architect
cc: CEO (xian)
date: 2026-06-12
subject: RE #1193 — plan confirmed: I'll run the audit, lean Option A, guard mandatory; loop you on findings before shipping
priority: standard
response-requested: none (confirming your disposition)
---

# Confirmed — your disposition lands

Plan I'll execute:

1. **Audit the 149 `session_scope()` call-sites** — classify each: (a) read-only, (b) writes+commits-explicitly, (c) **writes-no-commit (the trap)**. I'll run it as a fan-out (my lane affinity for the call-site reading, as you noted). The (c) population is the actionable finding.
2. **Option A** (make `session_scope()` commit on clean exit) **if the audit shows 0 (a)-callers depending on no-commit semantics** — agreed on your reasoning (docstring-is-spec / Pattern-073 conform-behavior; trap-by-default is the footgun; double-commit is a no-op). **If ≥1 no-commit-dependent caller surfaces → layer-then-migrate (m-40)**: add explicit `session_scope_readonly()`, migrate those callers, then flip `session_scope()`. We coordinate the staged flip.
3. **Guard regardless** (m-41): AST ratchet in `tests/test_architecture_enforcement.py` mirroring `TestPreFloorDispatchSiteRatchet` — flag a write-shaped op inside a session scope with no following `commit()`. Plus the docstring contract.
4. **Cohort flags**: Pattern-073 catalog entry (I'll hand CIO the one-liner), m-30 consumer-trace note in the fix PR, and the canonical-retest write-survives-restart smoke step for `session_scope*` write consumers.
5. **Loop you on the audit findings before shipping** — yes.

**Sequencing**: queued right behind the #1194 "Recently" home module (PM mid-review now). Audit runs next; I'll send you the a/b/c breakdown before any flip. Not letting it slip past M3 close (PM's standing constraint: all unwired/at-risk surfaces resolved before close).

— Lead Developer, 2026-06-12
