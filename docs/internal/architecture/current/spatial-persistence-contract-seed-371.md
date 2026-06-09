# Spatial-persistence contract seed (#371 / #366 / Epic #361)

**Status**: SEED — contracts defined, build deferred (post-MVP). PM-authorized 2026-06-09 ("seed both, defer the build"). Arch (event-shape) + CXO (promise-contract) recommended the seed; this captures both.
**Why this exists**: #371 (time-series attention persistence) is post-MVP (value-unproven). But two *contracts* are cheap to lock now and expensive to retrofit later, so we seed them while the context is fresh — keeping the option open without paying for the (idle-until-proven) build. See `artifact-model`-adjacent reasoning + the 2026-06-08 Arch/CXO memos.

---

## Contract 1 — Event-shape (Arch's seed; the *data* surface)

**Trace (methodology-30 consumer-trace, 2026-06-09):** the attention-event shape that in-session code emits today is `AttentionEvent` (`services/integrations/slack/attention_model.py:50`), consumed by the decay path (`get_current_intensity` + `services/scheduler/attention_decay_job.py`) and the spatial/lens machinery.

**Finding: the shape is largely longitudinal-ready.** It already carries what time-series aggregation needs:
- **Identity**: `event_id`
- **Timestamps**: `created_at`, `last_updated`, `expires_at` (decay-respecting)
- **Decay semantics**: `AttentionDecay` enum (linear/exponential/stepped/contextual) + `get_current_intensity()`
- **Scores**: `base_intensity`, `urgency_level`, `personal_relevance`, `relationship_strength`, `deadline_pressure`
- **Grouping dimensions**: `source` (AttentionSource), `actor_id`, `target_users`, `keywords`, `spatial_coordinates`, `workflow_id`

**Candidate additive gaps for longitudinal aggregation** (NOT present today; would help #371's rolling-window / trend / decay-respecting-recall queries):
1. **`correlation_id` / `session_id`** — to group a *sequence* of related attention events into a trend/thread (today each event is standalone via `event_id` only).
2. **A flat `channel_id` / `workspace_id` dimensional tag** — for clean time-series grouping. ⚠️ *Verify*: may already be encoded inside `spatial_coordinates`; if so, no gap.
3. **`schema_version`** — to make future additive evolution explicit (methodology-32 Postel).

**The load-bearing conclusion — corner-painting risk is LOW, not high.** Because all three candidate gaps are **additive optional fields** (Postel: producers conservative, consumers liberal), #371 can add them *when it builds* without breaking any existing consumer — it is NOT the expensive cross-consumer retrofit Arch's seed-note worried about in the general case. **So: no code change needed now.** The seed is this documented list, so #371 adds them deliberately on day one rather than rediscovering them mid-build. (If a future change to the event shape were ever *non-additive* — renaming/removing a field consumers read — THAT would be the expensive retrofit; this trace found none pending.)

**Action**: none in code. This doc is the seed. Re-confirm gap #2 (channel dimension in spatial_coordinates) when #371 is picked up.

## Contract 2 — Promise-contract (CXO's seed; the *experience* surface)

**The user-facing promise about cross-session attention memory, at MVP (0.9.x beta):**

> **Piper's spatial/attention intelligence is IN-SESSION at MVP.** It reasons about where your attention is *now* (lens tracking, spatial guidance, attention decay within a session) — but does NOT yet remember attention *across* sessions ("I noticed last week you kept returning to the auth thread"). Cross-session attention memory is a deliberate post-MVP capability (gated on #371 longitudinal persistence + proven value).

**Why this bounds the data contract**: if we don't promise cross-session attention recall at MVP, the event shape doesn't *need* the cross-session correlation fields (gap #1) wired *yet* — they're seeded as known-additive, not built. Conversely, the event shape's decay-respecting timestamps mean the promise *can* later grow to "I remember your attention from last week" without a data-layer rewrite. The two contracts compose (Arch + CXO).

**CXO RATIFIED 2026-06-09** (`memo-cxo-to-lead-...-371-promise-wording-ratified...`). The data-facing boundary above is ratified as-is. CXO supplied the user-facing translation in two parts:

**(a) User-facing scope statement** (plain-language, for docs/onboarding if/when we describe it — de-jargoned per three-registers):
> "As you work together, Piper picks up on what you're focused on and follows along as that shifts during your conversation."
> *Deliberately says no "remembers"/"lately"/"over time"/"coming soon" — we don't advertise the boundary (stating an absence makes users notice it); we just stay honestly scoped to the present.*

**(b) The load-bearing piece — an in-session VOICE constraint** (CXO: "the teeth are in the voice, not a stated sentence"):
> In-session attention references stay **present-tense + session-scoped** ("right now", "in this conversation", "as we're working"); **avoid temporal-continuity words** ("lately", "keep", "usually", "you've been", "over the past…") that imply a multi-session memory Piper doesn't have at MVP.

This is **present-relevant** (a guardrail NOW, not deferred — even in-session copy must not imply cross-session memory). It's a testable copy-review rule → candidate lint on attention-referencing strings (same spirit as the `toast-messages.js` voice rules, #642). **Tracked as discovered-work for a lint check** (filed 2026-06-09). This voice rule — not a docs sentence — is what keeps the #371 deferral from becoming a felt broken promise.

---

## What is NOT seeded (deferred to the build, correctly)
- **Storage technology** (InfluxDB / TimescaleDB / Timescale-on-PG) — commits nothing today; chosen at build time, zero retrofit cost.
- **Ingestion pipeline, retention policies, aggregation queries** — the #371 build proper.
- **A lighter slice of #371** — concur (Arch + CXO): no value without longitudinal history to operate over.

*Seed authored by Lead Developer 2026-06-09 per PM "seed both" + the Arch/CXO 2026-06-08 recommendations. Cluster is Post-MVP (PM board-moved #371/#366).*
