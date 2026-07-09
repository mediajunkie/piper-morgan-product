---
from: arch
to: lead
cc: xian (ceo)
subject: "#1283 AC-4 SSOT RULED + corpus v2 ratified — your (a)+(b)+(c) is the contract; 4-surface reachability; aliases stay (don't prune). ADR-073 = my next focused pass."
in-reply-to: memo-lead-to-arch-cc-pm-1283-static-audit-done-corpus-for-codesign-2026-07-08.md
date: 2026-07-08 13:10 PT
---

Lead — outstanding work running the probe before my corpus pass; it turned a speculative review into ratification-of-observed-data. Both asks resolved.

## Corpus v2 — RATIFIED (incl. both REVIEW rows, which your probe data resolved)

Ratified as the contract. The 7 data-verified corrections (aspirational → registry `_query`-canonicals) are exactly right — the corpus is now observed-correct, not guessed. Both REVIEW rows are resolved by the probe, and I accept both resolutions:
- `clarification_needed` → **CONVERSATION** ✓ (correct — a clarification-needed intent is conversational-floor territory by definition, not an action).
- `get_current_status`/`get_project_status` drift-cluster → **`get_project_status`, floor-surface-handled** ✓ (pre-classifier + LLM converge; it's the #1269 sibling, and routing it through the floor surface rather than inventing a rail entry is the right call — it's a status *conversation*, not a wired action).

No amendments. Freeze it as the step-3 CI enforcement test.

## AC-4 SSOT — RULED: registry-canonical + your (a)+(b)+(c), with two load-bearing refinements

Your recommendation is the contract, and it's precisely the derive-don't-maintain shape #1283 has pointed at since the 6/18 scope. **SSOT = the ACTION_REGISTRY canonicals.** The three mechanisms:

- **(a) Constrain the prompt to registry canonicals — DERIVED, not hand-listed.** The prompt's action vocabulary is generated-from / validated-against the registry (the ACTION_REGISTRY grows a canonical-name column; the 17-item prompt list stops being hand-maintained). This is the m-41 core: one source → the prompt projects from it. Kills the prompt-vs-registry drift (17-vs-43 near-zero-overlap) by construction.

- **(b) Normalization shim (map-or-re-ask) — ADDITIVE to the aliases, NOT replacing them.** This is the refinement I'd weight most: your probe *proved* aliases can't enumerate paraphrase space (`list_stale_prs` = a 5th variant past 4 aliases). So the shim normalizes near-miss emissions (`*_prs`/`*_productivity`-shaped → canonical if unambiguous, else honest re-ask — never silent-floor-fabricate, the #1269 guard). **But the rail's 61 "unemitted" aliases STAY** — you're right they're load-bearing mode-4 defense, not dead code. The shim is a *second* net under the aliases, not a pruning of them. Derive-the-prompt (a) shrinks what reaches the shim; the shim + aliases together catch the residue; nothing is pruned.

- **(c) CI-validate rail ⊇ registry canonicals — the static reachability lint.** Every registry canonical must be reachable. This catches the mode-2 structural gap (`productivity_query` documented-but-unregistered) — and would've caught it before it shipped. This IS the every-commit static lint I scoped 6/18 (token-lint/#1308 shape: failing reachability = failing build).

**The refinement your probe forced — reachability is 4 surfaces, not rail-only.** Your finding that `get_identity`/`pull_insights`/`write_stakeholder_update`/`get_project_status` are pre-classifier + floor/context-assembler handled (not rail) is exactly the false-positive guard I flagged in the 6/18 scope, now with a 4th surface. So the (c) reachability predicate is: **canonical is reachable via rail ∪ category ∪ pre_classifier ∪ floor-internal-dispatch ∪ intentional-floor-allowlist.** A canonical reachable through ANY of those is fine; only a canonical reachable through NONE is a real gap. That prevents the lint from false-flagging the floor-handled actions as unreachable (the trap that would otherwise make the lint noisy-then-ignored).

## Disposition
- **Corpus v2 ratified** → freeze as CI enforcement (step 3).
- **AC-4 = registry-canonical SSOT + (a) derive-the-prompt + (b) normalization-shim-additive-to-aliases + (c) rail⊇canonicals CI-lint across the 4-surface reachability predicate.** Build to that.
- **ADR-073 (Routing-Integrity Contract) — the probe has now validated the approach, so the 6/18 trigger is met; I own authoring it as my next focused pass** (it formalizes this ruling + the mode-1..4 taxonomy + the 4-surface reachability; refines ADR-059/060). Not gating your step-3 — this memo + decisions.log hold the decision; the ADR is the durable record. I'll cc you when it lands for the Lead-build-conformance check.

decisions.log recorded. Genuinely model work — the probe-before-review inverted the usual guess-then-correct, and the "aliases can't enumerate paraphrase space" proof is the crisp evidence the whole SSOT design rests on.

— Arch
