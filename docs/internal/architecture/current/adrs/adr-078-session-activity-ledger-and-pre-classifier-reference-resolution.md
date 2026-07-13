# ADR-078 — Session-Activity Ledger + Pre-Classifier Reference Resolution (the #1394 cross-turn continuity architecture)

**Status**: **PROPOSED (v0.1, 2026-07-12; HOST trust-lens PASS folded 2026-07-13 → D1a session isolation)** — Arch-authored; PM-directed determination (2026-07-12, "maintain the architectural integrity"). **Gated to ACCEPTED on**: (1) Lead's ledger-feasibility read over the existing substrate, and (2) PM/Lead concurrence on the pre-classifier direction (D2/D4). Do not build against this as final until those two clear.
**Author**: Chief Architect (arch)
**Deciders**: Architect (author/ruling); Lead Dev (feasibility + build); PM (direction, integrity mandate).
**Related**: **#1394** (the two-symptom gap this resolves), **#1122** (the floor-path antecedent fix — establishes the machinery this ADR routes to the right layers), **ADR-077** (routing-integrity — D4 here protects it), **#1283** (the 4-surface routing chain + D5 corpus), **#1269** (fabrication guard — why the classifier stays stateless), **#1312** (MUX phase-0 park-with-model — the `conversation_turns.parent_id` / `conversation_links` substrate), **#952** (the Artifact unifying-lens `ArtifactDB` — the artifact model this associates to, does NOT duplicate), ADR-051 (session_id IS conversation_id).

---

## Context

#1394 is two cross-turn continuity failures, confirmed as shipped behavior on both alpha and Fly (not an env regression):
- **B3** — a follow-up ("Actually, change the title…") **misroutes** to the Notion document handler.
- **B4** — "what did we create this session?" **honestly finds nothing.**

**The determination (Arch, 2026-07-12, code-verified — decisions.log same date): this is an ARCHITECTURAL GAP, not a wiring lapse.** The #1122 antecedent machinery (`build_recent_history` / `hydrate_turns_from_db` / the floor's "Reference binding" block) **is already wired and runs in production** on `/api/v1/intent` — so "just call the tested function on this path" fixes neither symptom. The machinery feeds the **conversational floor (surface 4)**, which is the wrong layer for both behaviors.

**Root cause — context stratification.** Prior-turn conversational context reaches only surface 4. It never reaches the two seams that actually govern #1394:
- **B3**: routing is decided at the **LLM classifier (surface 2)**, which is antecedent-blind *by construction* — `llm_classifier._build_classification_prompt` injects only similar-intents + detected-domains; `classify()` has no `conversation_history` parameter and the prompt has no history slot. The only cross-turn signal is a `contextual_continuation_hint`, set *only* when Piper made an explicit offer last turn (an issue-creation is not an offer → null). So the classifier routes the follow-up before the floor's binding (downstream) can ever engage.
- **B4**: turns are persisted and hydrated correctly (this is *not* a session-id wiring bug — the persistence loop over `conversation_turns` via `conversation_manager` is sound). The gap is that **no authoritative session-activity reader exists**: the only consumers of saved turns are the floor's ephemeral 10-turn/30-min window and a truncated `turn_count` summary. Neither records *created artifacts*; "what did we create" routes to a live-repo GitHub query with no session-scope.

**The unifying insight: both symptoms are ONE missing primitive at two seams.** Both need a durable, session-scoped record of *what this session did* — its turns AND the artifacts it created. B3 reads it to resolve "the title" → the issue created last turn; B4 reads it to answer "what did we create." Build the primitive once; both resolve.

## Decisions

**D1 — The missing primitive is a Session-Activity Ledger: the session/turn → created-artifact ASSOCIATION. It LINKS existing models; it does not duplicate them.** Two ratified substrates already exist and must be reused, not reinvented:
- **Turns**: `conversation_turns` + `conversation_manager` (persisted, queryable) — the conversational half already works.
- **Artifacts**: `ArtifactDB` (#952 Artifact unifying-lens) — the "what Piper produces" model (owner-scoped, NOT session-scoped).
The genuinely missing piece is the **association** — a record that "turn T in session S created artifact A" (turn_id / session_id → artifact reference/type). This is the minimal new structure; it composes the #1312 phase-0 `conversation_turns.parent_id` / `conversation_links` threading (parked-with-model) with the #952 artifact model. NOT a new parallel artifact store.

**D1a — the ledger is keyed by (session_id, user_id), never session alone (HOST trust-lens, 2026-07-13).** In a shared / BYOC instance, session-alone keying would let one user's activity bleed into another's resolution context — a cross-user leak of exactly the class ADR-071 / #1366 closes. The ledger inherits the server-owned-state family's per-user owner-scoping: every read is scoped to the acting principal, so cross-user resolution is not expressible (impossible-by-construction, same bar as the personalization store). Both consumers (D2 pre-classifier resolution, D3 recall) resolve only within the acting (session_id, user_id).

**D2 — B3 closes via a PRE-CLASSIFIER reference-resolution step (surface 1), reading the ledger.** A follow-up referent ("the title", "that", "it", "the issue") is detected and resolved against the session-activity ledger *before* classification, annotating/rewriting the message so the classifier and handlers see an explicit referent ("change the title of issue #107"). The resolution is an explicit, inspectable, testable transform on the pre_classifier surface.

**D3 — B4 closes via a session-activity retrieval capability over the ledger** (a reader + routing to reach it) — "what did we create/do this session" reads the ledger as the authoritative record, not the floor's ephemeral window or a live-repo query.

**D4 — The classifier (surface 2) STAYS STATELESS. Do NOT inject conversation history into the classification prompt.** This is the load-bearing integrity constraint. Surface 2 is the one we have worked hardest to keep clean and deterministic (ADR-077 routing-integrity, #1283, the #1269 fabrication guard). Making it conversation-stateful would: change *all* routing behavior (every follow-up now history-influenced), risk over-anchoring (a genuine topic-switch misread as a continuation), and force a full ADR-077 D5 corpus re-validation. Antecedent resolution belongs at surface 1 (explicit, bounded, testable), not diffused into the routing LLM.

**D5 — The new follow-up-routing behavior (B3) must be covered by ADR-077 D5 corpus rows** (the behavioral golden-corpus), Arch-ratified, before it ships — a follow-up that now routes differently is exactly the class the D5 corpus governs.

## Consequences

- **Sequencing**: **B4 first** (near-term, pre-wave-2) — it is self-contained AND it builds the ledger primitive D1. **B3 second** — the pre-classifier resolution reads the ledger B4 established; it is the design-heavier step and needs the D5 rows.
- Both symptoms resolve from one primitive; neither is a wire. Lead's "could be a wiring fix, could be a real build" resolves to: **a build, split across two seams, over two existing models + one new association.**
- Routing integrity preserved: the classifier is untouched; the only routing-behavior change (B3) is an explicit upstream referent resolution, gated by the D5 corpus.
- Reuses #952 (ArtifactDB) + #1312 phase-0 (the parked threading substrate earns its keep) + #1122 (its machinery stays; this ADR just stops relying on it to do a job it structurally can't — pre-routing antecedent resolution).

## Open questions (the gates to ACCEPTED)

1. **Lead's ledger-feasibility read (GATING).** Can the session/turn→artifact association be built cleanly over the parked #1312 phase-0 tables + `ArtifactDB`, or does the substrate need more than park-with-model declared? This is the feasibility fold I want *before* this goes ACCEPTED — Lead's build-lens sharpens D1's exact shape.
2. **Referent-detection for D2**: deterministic (pronoun/definite-reference patterns on the pre_classifier surface, cheap) vs a small LLM resolution call — a build-time calibration, not an architectural gate, but it interacts with the pre_classifier's deterministic character.
3. **Artifact-capture point**: where does "this turn created artifact A" get written to the ledger — at handler-success (each creating handler records), or a central post-handler observer? Leans central (one write path, mirrors the #1122 outer-seam turn-recording), but Lead's call.

## Sequencing

B4 (ledger primitive + reader) → B3 (pre-classifier resolution + D5 corpus rows). Neither is a wire; the ledger is the shared foundation.

---

*ADR-078 v0.1 PROPOSED, Arch-authored 2026-07-12, on PM's #1394 integrity determination. Both #1394 symptoms are one missing primitive — a session-activity ledger associating turns to created artifacts — surfaced at two seams; the classifier stays stateless. ACCEPTED pending Lead's ledger-feasibility read + PM/Lead concurrence on the pre-classifier direction.*
