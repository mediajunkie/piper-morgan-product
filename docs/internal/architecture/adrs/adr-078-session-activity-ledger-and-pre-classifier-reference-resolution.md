# ADR-078 — Session-Activity Ledger + Pre-Classifier Reference Resolution (the #1394 cross-turn continuity architecture)

**Status**: **ACCEPTED (v0.2, 2026-07-14)** — Arch-accepted on the integrity authority PM delegated (2026-07-12, "maintain the architectural integrity") + greenlit authorship. Both ACCEPT gates cleared: (1) **Lead's ledger-feasibility read — DONE** (2026-07-14; it *corrected* D1 from association-over-existing to a dedicated additive `session_activity` ledger — see OQ-1); (2) **pre-classifier direction (D2/D4) — Lead CONCURS + HOST trust-lens PASS** (2026-07-13). **PM retains veto** — flagged to PM on acceptance (this is the architecture call PM asked me to hold; surfaced, not silently flipped). Lead is cleared to build B4 against the D1 `session_activity` contract. *(v0.1 PROPOSED 2026-07-12; HOST D1a folded 2026-07-13; D1 corrected + accepted 2026-07-14. **B4 built + Arch-ratified 2026-07-15** — SessionActivityDB + owner-scoped reader + central observer + recall, suite-green; B3 pre-classifier resolution pending, needs new ADR-077 D5 rows.)*
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

**D1 — The missing primitive is a dedicated, additive `session_activity` ledger of external creations (v0.2, corrected by Lead's feasibility read + Arch code-verification, 2026-07-14).** *v0.1 assumed this could be an ASSOCIATION over existing models (`conversation_links` + `ArtifactDB`). Lead's build-lens read (OQ-1, below) + my verification proved that reuse doesn't fit — the instinct not to proliferate stores was right, the specifics were wrong:*
- `conversation_links` is **turn↔turn by FK** (both `source_id`/`target_id` FK `conversation_turns.id`, models.py:1740/1746) — it structurally cannot hold `turn → artifact`, and it's the protected #1312 park (zero writes; loosening its FK breaks the autogen-empty invariant).
- `ArtifactDB` (#952) is an **owner-scoped encrypted-content store** — a created *issue* writes **no** artifacts row (github_adapter has zero ArtifactDB writes; the issue# is an external pointer, not stored content). Reusing it conflates "created an external reference #107" with "stored a doc's bytes."
- **The "session created issue #107" fact exists in no table today** — it is a genuine new write path, not an assembly.

So D1 is a **purpose-built, additive** table holding *external references* (not content):
```
session_activity(
  id,
  conversation_id  FK conversations   (indexed),
  owner_id / user_id  NOT NULL        (D1a — see below; the read-scoping key),
  turn_id          FK conversation_turns (nullable) — which turn created it,
  action_type      -- 'issue_created' | 'doc_created' | ...
  target_ref       -- 'mediajunkie/test-piper-morgan#107' (external pointer, NOT content)
  target_title     -- 'Fix the login bug' (for antecedent display)
  created_at
)
```
One new migration, no touch to the protected #1312 tables, passes autogen-empty clean. Reads trivially for both seams (B4: `WHERE owner scope`; B3: same, ordered by turn, to resolve "the title" → the last `issue_created`). Forward-compatible with the #1312 graph: `session_activity` rows can *project onto* `conversation_links` when MUX-resume lands, without either owning the other.

**D1a — the ledger carries `owner_id`/`user_id` NOT NULL and every read is owner-scoped; never session alone (HOST trust-lens, 2026-07-13; realized in the D1 schema).** In a shared / BYOC instance, session-alone keying would let one user's activity bleed into another's resolution context — a cross-user leak of exactly the class ADR-071 / #1366 closes. The `owner_id` column is not optional metadata: the reader's WHERE clause is scoped to the acting principal by construction, so cross-user resolution is **not expressible** (impossible-by-construction, same bar as the personalization store — the standard the whole server-owned-state family is held to). Both consumers (D2 pre-classifier resolution, D3 recall) resolve only within the acting (owner_id, conversation_id). **Build note for Lead**: this is the one requirement I will not accept as implicit — an unscoped `SELECT ... WHERE conversation_id = ?` is the silent-leak default a new ledger table invites; the read path must key on the resolved owner, and a test must assert a second user's activity is not returned.

**D2 — B3 closes via a PRE-CLASSIFIER reference-resolution step (surface 1), reading the ledger.** A follow-up referent ("the title", "that", "it", "the issue") is detected and resolved against the session-activity ledger *before* classification, annotating/rewriting the message so the classifier and handlers see an explicit referent ("change the title of issue #107"). The resolution is an explicit, inspectable, testable transform on the pre_classifier surface.

**D3 — B4 closes via a session-activity retrieval capability over the ledger** (a reader + routing to reach it) — "what did we create/do this session" reads the ledger as the authoritative record, not the floor's ephemeral window or a live-repo query.

**D4 — The classifier (surface 2) STAYS STATELESS. Do NOT inject conversation history into the classification prompt.** This is the load-bearing integrity constraint. Surface 2 is the one we have worked hardest to keep clean and deterministic (ADR-077 routing-integrity, #1283, the #1269 fabrication guard). Making it conversation-stateful would: change *all* routing behavior (every follow-up now history-influenced), risk over-anchoring (a genuine topic-switch misread as a continuation), and force a full ADR-077 D5 corpus re-validation. Antecedent resolution belongs at surface 1 (explicit, bounded, testable), not diffused into the routing LLM. **(HOST trust-lens framing, 2026-07-13, the clearest statement of the *why*): explicit resolution creates a legible, inspectable intermediate state — you can see, test, and explain "the title" being rewritten to "issue #107" before the classifier runs; implicit context-blending inside the classifier does not, and its routing effects can't be reasoned about or debugged the same way.**

**D5 — The new follow-up-routing behavior (B3) must be covered by ADR-077 D5 corpus rows** (the behavioral golden-corpus), Arch-ratified, before it ships — a follow-up that now routes differently is exactly the class the D5 corpus governs.

## Consequences

- **Sequencing**: **B4 first** (near-term, pre-wave-2) — it is self-contained AND it builds the ledger primitive D1. **B3 second** — the pre-classifier resolution reads the ledger B4 established; it is the design-heavier step and needs the D5 rows.
- Both symptoms resolve from one primitive; neither is a wire. Lead's "could be a wiring fix, could be a real build" resolves definitively to: **a genuine additive build — one new `session_activity` table + its central-observer write path — read at two seams.** (The v0.1 hope of assembling it over existing tables did not survive the feasibility read; the honest answer is a small new table, cleanly additive.)
- Routing integrity preserved: the classifier is untouched; the only routing-behavior change (B3) is an explicit upstream referent resolution, gated by the D5 corpus.
- Reuses #952 (ArtifactDB) + #1312 phase-0 (the parked threading substrate earns its keep) + #1122 (its machinery stays; this ADR just stops relying on it to do a job it structurally can't — pre-routing antecedent resolution).

## Open questions (the gates to ACCEPTED)

1. **~~Lead's ledger-feasibility read (GATING)~~ — RESOLVED 2026-07-14.** Lead's build-lens read (code-grounded) + Arch verification: the parked substrate can't carry it (`conversation_links` turn↔turn FK + protected; `ArtifactDB` content-store; issue-creations recorded nowhere) → a genuine additive `session_activity` build. **D1 rewritten accordingly** (v0.1 association-over-existing → v0.2 dedicated additive ledger). This gate is cleared.
2. **Referent-detection for D2** (still open — build-time, not an architectural gate): deterministic (pronoun/definite-reference patterns on the pre_classifier surface, cheap) vs a small LLM resolution call — interacts with the pre_classifier's deterministic character. Lead's calibration at build.
3. **~~Artifact-capture point~~ — RESOLVED 2026-07-14 (Arch lean, Lead concurs).** A **central post-handler observer at the #1122 outer-seam** (`intent_service.py:380`, `conversation_manager.save_conversation_turn` — already central, already holds session_id + the turn), NOT per-handler. When a handler's structured result carries a "created X" (the github write already returns the created issue ref), the observer writes one `session_activity` row; creating handlers stay ignorant of the ledger. Mirrors the #1122 design; avoids threading `turn_id` through six handlers. The one per-handler ask is a small uniform "creation-result" shape the observer recognizes (a light contract, not a rewrite).

## Sequencing

B4 (ledger primitive + reader) → B3 (pre-classifier resolution + D5 corpus rows). Neither is a wire; the ledger is the shared foundation.

---

*ADR-078 v0.2 ACCEPTED, Arch 2026-07-14, on PM's #1394 integrity determination. Both #1394 symptoms are one missing primitive — a dedicated additive `session_activity` ledger of external creations (owner-scoped), written by a central observer, read at two seams (B3 pre-classifier resolution + B4 recall); the classifier stays stateless. Lead's feasibility read corrected D1 (no reuse over parked tables) and concurred the direction; HOST trust-lens PASS folded (D1a + D4). Lead cleared to build B4 against the D1 contract; PM retains veto.*
