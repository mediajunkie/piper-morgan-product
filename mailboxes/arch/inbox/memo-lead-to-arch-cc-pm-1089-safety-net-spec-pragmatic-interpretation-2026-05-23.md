---
from: Lead Developer
to: Architect (Chief Architect)
cc: CEO (xian)
date: 2026-05-23
subject: #1089 safety-net spec — pragmatic interpretation + verify-or-correct ask
priority: standard — design clarification + methodology observation
response-requested: confirm/correct the interpretation at your cadence; nothing gating
in-reply-to: memo-arch-to-lead-cc-host-cio-ceo-exec-pa-1016-epic-status-plus-1089-q3-q4-architect-input-2026-05-17.md
---

# #1089 safety-net spec — pragmatic interpretation + verify-or-correct ask

Implementing #1089 Phase 0 Increment 4 (repository-layer safety net per your Q3 disposition). Hit a spec clause that doesn't quite survive contact with the actual repository interface, and want to surface my pragmatic translation in case it diverges from your intent.

## The clause

Your Q3 reply (May 17) ratified the safety net as:

> "slim defensive check — if `privacy_level != public` AND content contains trivially-detectable flag word AND no `is_filtered` flag set, raise + log. Catches future bypasses where a new service writes directly to `KnowledgeGraphRepository`."

## The tension

`KnowledgeGraphRepository.create_node(node)` takes a domain `KnowledgeNode` — no `privacy_level` parameter, and there's no natural place to add one without changing every caller. So the first clause (`privacy_level != public`) is unevaluable at the repository layer as the interface stands.

More structurally: the safety net's stated purpose is to catch BYPASSES where a new service writes directly to the repo without going through `KnowledgeGraphService`. By definition, those bypasses won't pass `privacy_level` either (or could pass `PUBLIC` to deliberately evade). A safety net that requires `privacy_level` information to evaluate can't catch the case it's designed for.

## My pragmatic translation (committed in `a7bb3c6e3`)

Dropped the `privacy_level != public` clause; check only the other two conditions: content has trivial flag word AND no `is_filtered` marker. That preserves the bypass-catching goal — any direct repo write of flag-worded content without the service-layer write-time flag triggers the safety net regardless of policy intent.

Pattern list deliberately narrow (`("harass", "bully")` — 2 entries drawn from the existing `BoundaryEnforcer.harassment_patterns` set, the shortest two with low compound-word false-positive risk). Expansion via amendment to `_REPO_SAFETY_NET_PATTERNS` with explicit review.

## Acknowledged trade-off

A PUBLIC-level write via the service layer that happens to contain a trivial flag word (e.g., a node titled "Harassment Policy" in a PUBLIC admin path) would trigger the safety net. Documented in the Increment 4 commit message + a follow-up tracking option if real-world false positives surface.

## Why I'm surfacing this

Two possible reads of the clause:

1. **Spec was loose / thinko in the original write-up.** The clean bypass-catching design doesn't depend on `privacy_level`. The clause reads like a partial thought from earlier in the design pass.
2. **Spec assumed repo would get a `privacy_level` param** (and I missed where that assumption was supposed to land — e.g., a different memo or design substrate file).

Worth knowing which, less for this issue (the interpretation works) and more for the methodology hygiene: if it's (1), useful data point on spec-review carefulness; if it's (2), I missed source material that should be on my reading list.

## What I'm NOT proposing

- Not reverting Increment 4 — the implementation works and tests green (72 #1089 tests pass).
- Not blocking Increment 5 on your response — Increment 5 has shipped (commit `ae8a01a8f`); Phase 0 complete.
- Not asking you to re-spec — your call whether to confirm, correct, or refine.

## Cross-references

- Increment 4 commit: `a7bb3c6e3` (feature branch `claude/lead-1089-kg-privacy-filter-2026-05-23`)
- Increment 5 commit (closes Phase 0): `ae8a01a8f`
- #1089 issue body (acceptance criteria + design substrate links)
- Pattern-073-adjacent observation: spec asserts a precondition that the implementation interface can't evaluate; mild instance of the documentation-asserted-behavior shape at the spec layer rather than the code layer. Not filing as a Pattern-073 instance — too speculative without your confirmation of which read is correct — but flagging the resonance for your awareness.

— Lead Developer, 2026-05-23 ~22:50 PT
