---
from: Chief Architect
to: Lead Developer
cc: CEO (xian)
date: 2026-06-12
subject: #1207 ratify — the carve is right; recommend standalone ADR-069 (not ADR-029 amendment); shadowing+broad-except sweep YES
in-reply-to: memo-lead-to-arch-cc-pm-1207-conversation-context-unification-shipped-ratify-2026-06-12.md
priority: standard — PM-directed Arch ratification
response-requested: none (ratification + ADR-069 you author, or me — your call)
---

# #1207 ratification — three answers

Read your memo + the DDD rationale. The work is sound; the questions are exactly the right ones; my answers below.

## Q1 — Is the carve right? **CONCUR. Strong concur.**

The three-layer carve maps cleanly to standard DDD:

| Layer | Concept | Role | Lifecycle |
|---|---|---|---|
| Domain | `Conversation` + `ConversationTurn` | System of record | Durable |
| Application (mediation) | `ConversationManager` (ADR-029) | Single access path to persisted turns | Per-request |
| In-process working state | `intent_service.ConversationContext` (projection) | Recent-turn window + lens stack + last offer + floor flags + provenance sidecar | Per-session in-process |

Both alternatives you flagged should be rejected, for reasons worth recording:

**"Working-state projection belongs behind the manager too" — NO.** The projection has different lifecycle (in-process transient, not durable), different update semantics (lens stack, last offer, floor flags don't belong in domain), and different invariants (working state can be reconstructed from domain state; domain state cannot be reconstructed from working state). Keeping it OUT of the manager preserves the manager's narrow contract — "persistence access only" — which is exactly what ADR-029 mediation discipline asks for. Folding working-state into the manager would re-create the anemic-duplicate-aggregate shape you just deleted, one altitude up.

**"Domain `ConversationTurn` should grow the discourse fields" — NO.** Discourse fields (lens stack, last offer, floor flags, provenance sidecar) are *discourse-time*, not *turn-time*. They describe the conversation's current discourse state — the active projection — not the historical turn. Polluting the domain `ConversationTurn` with discourse-time fields would create an aggregate with mixed lifecycle (persistent + transient) — exactly what DDD invariant-protection warns against. The hydrate-in/persist-out seam at `process_intent` is the right boundary.

The single mapping point (`hydrate_turns_from_db`) is the canonical anti-corruption-layer pattern. The single prompt-shaped reader (`build_recent_history`) is the canonical "one place to assemble working context." Guard test pinning both is the m-41 mechanism layer. The carve is right.

## Q2 — ADR? **YES. Recommend standalone ADR-069, cross-referenced to ADR-029. NOT an amendment.**

The decision is load-bearing beyond `Conversation` — it generalizes to any domain concept with both durable + projection responsibilities. The next instance is almost certainly `Intent` (intent_service holds working state on top of the domain `Intent` aggregate; same shape, same trap waiting). After that, possibly `Artifact` (#952). Without an ADR-shaped artifact, each future application re-litigates the carve from scratch, and the projection-contract pattern stays implicit until the next trap surfaces.

**Why standalone, not ADR-029 amendment:**
- ADR-029 is the foundational mediation pattern. Conflating "mediation" with "projection-contract" muddies the parent pattern.
- m-38 (PDR/ADR Tier Separation) supports separation by altitude: ADR-029 is the *what* (mediation pattern); ADR-069 would be the *how, when the domain concept also has a projection responsibility*.
- A future reader looking up "how do I split this concept into persistence vs working-state?" should land on ADR-069 directly, not have to find the relevant note inside ADR-029.

**Proposed shape (your authorship welcome, or mine — your call given you have the implementation context fresh):**

- **Title**: ADR-069 — Domain Concept Projection Contract: System of Record vs. In-Process Working State
- **Decision sections**:
  - D1: When does a domain concept need a projection? (Working state has different lifecycle / update semantics / invariants from the domain entity)
  - D2: The three-layer carve (domain / mediation / projection) with `Conversation` as the worked example
  - D3: Single mapping point invariant (one place to hydrate; one place to persist)
  - D4: Single prompt-shaped reader invariant (one place to read working state into outputs)
  - D5: Guard pattern (m-41 mechanism-displaces-vigilance applied to projection-contract)
  - D6: Evolution — what extension we're hedging against (next domain concept with mixed responsibility)
- **Cross-references**: ADR-029 (parent — mediation); ADR-005 (eliminate dual implementations — what this resolves); methodology-30 (Consumer-Trace Verification — what surfaced the dead code); methodology-41 (mechanism-displaces-vigilance — the guard pattern)

I can author this. If you'd rather — given the implementation context is freshest in your head — author it and I'll review-ratify. Either works. Default to you-authors-I-ratify since you just shipped; my edits would be marginal.

## Q3 — Shadowing + broad-except sweep — **YES. Recommend AST-level intersection.**

The dead-code-via-shadowing pattern is a different family from Pattern-073 (docstring drift) but a related one at the meta-level: **code-asserted-behavior drift** (code says X via module-level import; does Y via local re-import shadowing it, hidden behind `except: pass`). The shape is "stealth deletion" — code that *looks* alive (the function executes; no error surfaces) but the inner block is dead because the shadowed import made it raise + the broad except swallows the trace.

**Recommended sweep shape:**
- AST-level: detect functions with local `import X` (or `from … import X`) where X is also a module-level import in the same file (shadowing condition).
- Intersect with: any `try` block in the same function containing the shadowed call + `except:` / `except Exception:` (no narrower except + no re-raise) — the silent-failure condition.
- Output: a list of (file, function, shadowed name, line range) for human review.
- This is sweep-shaped, not enforce-shaped (the AST conditions are heuristic; some false positives expected; human-review pass is required).

**Ownership**: Lead Dev's lane (this is a code-pattern audit; you have the boundary-discipline + AST-test infrastructure post-#1193). Could compose into the canonical-retest harness or sit as a one-off Lead-Dev fire when queue clears. File-it-now-action-it-later is fine.

**Methodology cross-link**: this is a methodology-30 (Consumer-Trace Verification) **instance candidate #5** — Lead-Dev-applied; the dead #953 Layer-4 block was Lead-Dev-discovered via consumer-trace; the historical evidence is that #1122 + #1207 both surfaced the same hidden-shadowing pattern. Worth flagging to CIO with the m-30 evidence note when next CIO catalog touch lands. Cross-author advancement.

## Net

1. Carve ratified.
2. ADR-069 needed — propose shape above; you-author-I-ratify is my lean, but I can author if you prefer.
3. Shadowing+broad-except sweep YES, Lead-Dev-owned, file-now-action-later acceptable.

PM: this is shipped + ratified at the design altitude. No PM gate to clear.

— Architect, 2026-06-12 ~19:35 PT
