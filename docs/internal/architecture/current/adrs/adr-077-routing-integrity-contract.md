# ADR-077 — Routing-Integrity Contract (Action↔Handler Reachability)

**Status**: ACCEPTED (v0.1, 2026-07-09) — Arch-authored; formalizes the #1283 AC-4 SSOT ruling (2026-07-08) after Lead's static audit + behavioral probe validated the approach. Lead builds the enforcement.
**Author**: Chief Architect (arch)
**Deciders**: Architect (author/ruling); Lead Dev (static audit + behavioral probe + build); PM (#1283 direction, 6/18).
**Related**: **ADR-059** (capability accuracy — this extends it from "capability exists" to "action is *reachable*"), **ADR-060** (floor-first / floor-fall guard — this refines the floor's honest-degrade to cover unhandled actions), #1124 (workflow-dispatcher rail / no-elif-chains), #1269 (the fabrication that motivated this), #1308 (exempt-list lint — the enforcement shape), methodology-41 (derive-don't-maintain / make-drift-impossible), methodology-30 (consumer-trace = the behavioral probe).
**Note**: originally reserved as "ADR-073" in the 6/18 #1283 scope; 073 was assigned to the no-destructive-git ADR (PM-approved 6/27) before the reservation was noticed (Docs #1375 sweep, 7/9). This contract is **ADR-077**; the "ADR-073" references in the 7/8 #1283 memos + decisions.log should read ADR-077.

---

## Context

The action-classification path had **no single source of truth for action names.** Three hand-maintained vocabularies drifted independently (Lead's static audit, #1283): the classifier prompt (~17 example actions), the workflow registration (~43 canonicals), and the rail alias lists (~86 keys) — with near-zero overlap. The failure this produces (#1269): the LLM emits a plausible action name that no handler is registered for, and — worse than a clean miss — the request can silently floor-improvise a fabricated success rather than honestly degrade.

Lead's **behavioral probe** (29 real classifications, `dev/2026/07/08/routing-probe-1283-run1.md`) gave the decisive evidence:
- **Aliases provably cannot enumerate LLM paraphrase space.** `any stale PRs?` → the LLM emitted `list_stale_prs`, a *5th* variant past the rail's 4 hand-maintained aliases → fell through to generic handling. Hand-listing paraphrases is a losing race.
- **A documented canonical was itself unregistered.** `productivity_query` (a registry canonical) is not on the rail — if the LLM emitted the *documented* name it would also miss (a structural gap, not a paraphrase gap).
- **Routing is a 4-surface chain, not rail-only.** Several actions (`get_identity`, `pull_insights`, `write_stakeholder_update`, `get_project_status`) are handled by the pre-classifier + the conversational-floor / context-assembler internal dispatch, *not* the rail. A rail-membership check alone false-flags these as unreachable.

**Real-world instance (2026-07-09, retroactive):** `Intent.original_message` was never set by *any* classifier construction path, while two reader populations diverged — one reading the `.original_message` attribute, one reading `context["original_message"]`. That two-reader contract-drift (which retroactively explains #1332's intermittent empties) is the same *class* this contract exists to prevent, one layer down from action-name drift: a value with two hand-maintained access idioms and no single authority. The lesson generalizes — the SSOT + derive discipline applies wherever a value has multiple readers, not only to action vocabulary.

## The failure taxonomy (mode-1..4)

| Mode | What | Caught by |
|---|---|---|
| **1** — dead registration | a registered handler no name reaches | static lint |
| **2** — unregistered canonical | a documented/registry canonical with no reachable handler (`productivity_query`) | static lint (reachability) |
| **3** — prompt/registry name-drift | the prompt teaches a name the registry doesn't have | static lint (derive-the-prompt) |
| **4** — undocumented emission | the LLM emits a plausible name nobody registered (`list_stale_prs`) | behavioral corpus + the normalization shim |

## Decision

**D1 — Single source of truth = the ACTION_REGISTRY canonicals.** Action names have one authority: the workflow registration's canonical-name set. The prompt vocabulary and the rail keys are **derived from / validated against** it, never independently hand-maintained. (m-41: one source projects to the others; drift becomes unrepresentable.)

**D2 — Derive the prompt's action vocabulary from the registry.** The classifier prompt's list of valid actions is generated-from / validated-against the registry canonicals, not a hand-kept 17-item list. Kills mode-3 (prompt/registry drift) by construction.

**D3 — Normalization shim, ADDITIVE to the rail aliases (never replacing them).** A near-miss emission (`*_prs`/`*_productivity`-shaped, or any close-but-unregistered name) is normalized to its canonical **if unambiguous**, else an **honest re-ask** — never a silent floor-improvised success (the #1269 guard; refines ADR-060). The rail's ~61 "unemitted" aliases **stay** — they are load-bearing mode-4 defense, not dead code. Layering: D2 (derive-the-prompt) shrinks what reaches the shim; the shim + the aliases together catch the mode-4 residue; **nothing is pruned.**

**D4 — CI-validated reachability lint (rail ⊇ registry canonicals), across the 4-surface predicate.** Every registry canonical must be **reachable**, checked every commit (the #1308 / token-lint shape: failing reachability = failing build). Catches modes 1/2/3 deterministically. The reachability predicate is:

> a canonical is *reachable* iff it is handled via **rail ∪ category ∪ pre_classifier ∪ floor-internal-dispatch ∪ intentional-floor-allowlist**.

A canonical reachable through *any* surface is fine; only one reachable through *none* is a real gap. This 4-surface predicate is the false-positive guard — without it the lint flags the floor-handled actions (`get_identity` etc.) as unreachable and becomes noisy-then-ignored. The `intentional-floor-allowlist` remains the one small hand-maintained surface (keep it small + reviewed — it is itself a drift candidate).

**D5 — Behavioral golden-corpus on the canonical-retest harness (real LLM, gated cadence).** The static lint (D4) catches structural gaps; only a behavioral suite catches mode-4 (undocumented emission). `tests/fixtures/routing_corpus_1283.yaml` (Arch-ratified 7/8, one representative phrasing per capability, expected-destination annotated) is frozen as the CI enforcement corpus; a failing route = a failing build at the gated cadence.

## Consequences

- **Two-altitude enforcement**: D4 static lint (every commit, deterministic, modes 1/2/3) + D5 behavioral corpus (gated, real-LLM, mode 4). Neither alone suffices — a classifier-only probe undercounts handledness; a rail-only lint undercounts correctness.
- Refines **ADR-059** (capability-accuracy → runtime action-*reachability*) and **ADR-060** (the floor's honest-degrade now explicitly covers "confident action, no handler" → re-ask, never fabricate).
- The `productivity_query` structural hole and the `list_stale_prs` paraphrase miss (probe evidence) are both closed by construction under D1–D5.
- Same make-drift-impossible spine as ADR-072 (frontmatter-derive), #1106 (MANIFEST-derive), #1308 (exempt-list lint), #1344/#1312 (impossible-by-construction) — the recurring architectural move this week.

## Open questions

None blocking. The normalization shim's ambiguity threshold (when to map vs re-ask) is a build-time calibration on the corpus (Lead), not an architectural gate.

---

*ADR-077 v0.1, Arch-authored 2026-07-09. Formalizes the #1283 AC-4 SSOT ruling; probe-validated. The routing vocabulary now has one authority and two enforcement altitudes — the #1269 fabrication class is closed by construction.*
