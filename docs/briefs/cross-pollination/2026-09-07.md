# Cross-Pollination Brief — September 7, 2026

Two transferable findings today: one about how invariant proofs systematically miss UPDATE routes, and one about what a single type annotation change reveals in a dispatch layer. Both surfaced in substantive research sessions on September 6.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Invariant proofs need UPDATE routes enumerated separately from CREATE routes

**From:** Klatch (Theseus, Round 165, 2026-09-06 — `docs/research/round165-layer5-invariant-is-reachable-2026-09-06.md`)
**Relevant to:** Piper Morgan, any project with CRUD APIs and documented invariants

The Klatch invariant "assembly never hands the model a zero-length system prompt" was proven by enumerating three writers of the `entities.system_prompt` column, all of which substitute a non-empty default when the value would be blank. Round 165 found a fourth writer the enumeration missed: the `PATCH /entities/:id` update route (`routes/entities.ts:125`), which passes `systemPrompt: body.systemPrompt?.trim()` with no `|| DEFAULT` fallback — unlike the create route twelve lines above at `:87` that has one. The DB query at `queries.ts:409` uses `??` coalesce, which treats `''` as a value rather than an absence, so an empty-string PATCH stores empty and the invariant is violated. The bug is reachable from the UI in two gestures on the default agent.

The underlying pattern: **UPDATE routes are a systematic gap in invariant proofs.** They're almost always written separately from CREATE routes, often later, and often without the substitution fallbacks the create paths carry. An enumeration of "all writers" that grep-scopes to insert paths can pass cleanly while an update path violates the invariant silently.

Theseus noted the fix belongs at the writers (two one-liners in `routes/entities.ts` and `import/klatch-import.ts`), not at the assembly layer — which the prior round had correctly ruled out as the wrong fix location.

**Suggested action:** When documenting an invariant that relies on "all writers substitute X," verify the enumeration includes both insert and update paths for the relevant column. Grep for the column name in update-shaped queries separately from insert-shaped ones — they often live in different files.

---

### 2. Typing a dispatcher's return from `Any` to a Protocol surfaces dead dispatches and unimplemented operations at build time

**From:** Piper Morgan (Arch, #1723, 2026-09-06 — `mailboxes/arch/sent/shipped-arch-to-lead-cc-exec-cio-pm-github-operations-protocol-1723-...`)
**Relevant to:** Klatch, any project with router or dispatcher patterns

Piper Morgan's GitHub integration router had `_get_integration() -> Any`. A single annotation change — to `_get_integration() -> GitHubOperations`, where `GitHubOperations` is a typed Protocol — immediately made visible that 6 of 11 dispatched methods had zero external callers (deleted rather than enshrined), and that the spatial intelligence fallback in the dispatcher implemented none of the dispatched operations (replaced with an immediate `RuntimeError` rather than a deferred `AttributeError` deep in a handler). Arch described `-> Any` as "the single annotation that made #892 and #1709 possible" — the annotation had suppressed type errors for months, allowing dead dispatches to accumulate unnoticed.

Protocol membership rule: a method qualifies for the Protocol only if it is both dispatched AND has at least one live external caller. Writing the Protocol forces a census at that moment. A ratchet test (regex over the router source) ensures new unbacked dispatches fail the build going forward, keeping the census current without relying on discipline.

**Suggested action:** If your project has a dispatcher or router returning `Any`, consider defining a Protocol class with a "dispatched AND live-called" membership rule. Writing the Protocol forces the census; typing the return annotation makes the type system enforce it. The deletion of dead methods is often the most valuable outcome — dead code removed is cheaper than implementing it and clarifies what the system actually does.

---

## Sources Read

**Klatch:** `docs/research/round165-layer5-invariant-is-reachable-2026-09-06.md` (Theseus, Round 165 STOP fire) — primary source for Insight 1.

**Piper Morgan:** `mailboxes/arch/sent/shipped-arch-to-lead-cc-exec-cio-pm-github-operations-protocol-1723-written-enforced-4-live-unbacked-ops-route-to-you-2026-09-06.md` (Arch, #1723 ship notice) — primary source for Insight 2.

**Secondary repos** scanned against `origin/main --since="48 hours ago"`: globe, weather, one-job, nyt-crossword, mediajunkie, and cookie-monster had commits in the window; none produced brief-worthy content. Atlas, cuneo, and optilisten had no commits in the window. Full provenance in front matter.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
