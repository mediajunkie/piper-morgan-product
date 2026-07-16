
# Cross-Pollination Brief — July 16, 2026

One finding from Piper Morgan. A reachability lint that audits the action registry can pass with a blind spot for handlers that live only in a legacy elif dispatch chain — the lint doesn't know what it can't see, so a green pass reads as "all actions reachable" when it really means "all registered actions reachable." The fix and the lesson are both worth carrying forward. Globe and Klatch quiet this window.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### A vocabulary lint only audits what it was built to cover — handlers on parallel dispatch paths are invisible

**From:** Piper Morgan, Architect + Lead Dev (#1411, ADR-077 scoped-gap; `decisions.log` Jul 15; Arch session log `dev/2026/07/15/2026-07-15-0636-arch-code-log.md`)

**Relevant to:** Any project building action registries with enforcement/reachability tests — Klatch (workflow-entries registry for agent tools); any system where action dispatch lives on more than one surface.

Piper Morgan's ADR-077 vocabulary lint verifies that every action name the LLM classifier might emit maps to a registered handler. When Lead Dev found `update_issue` missing from the registry — a live risk, because a misrouted follow-up would have hit `create_issue` and silently created a duplicate — the Architect ran the lint as a check. It passed. Passed, even though the handler was missing from the registry.

The reason: `update_issue` (and the whole `EXECUTION` mapped_action cohort, including `create_issue`) is dispatched via an `elif intent.action == "update_issue"` chain — PM's surface-4 "fourth vocabulary," the original hand-coded dispatch mechanism that ADR-059/#1124 is migrating to the rail cohort by cohort. The lint was built to audit surfaces 1–3 (the action registry, the workflow-dispatcher rail, and the pre-classifier step). It has no visibility into surface-4. A handler can be live, reachable, and functionally correct — and the lint will report it as missing, or in this case, report all-green while the handler is entirely unregistered.

Arch called this explicitly the "the exact trap that `intent-routing-stack.md` warns against" — after Arch had authored the 4-surface model and then only checked two of four surfaces when diagnosing the gap.

The #1411 fix registers `update_issue` on the rail (one handler → now lint-visible). The ADR-077 note now documents the scoped-gap: "this lint covers registry/rail/pre-classifier surfaces; elif-only mapped_action handlers are unaudited until migrated to the rail" (ADR-059/#1124 governs the migration).

**The transferable principle:** a reachability or vocabulary lint is correct relative to the dispatch surface it covers — not relative to all dispatch in the system. If your system has two dispatch mechanisms (an audited registry and a legacy elif chain), the lint's pass result means "all registry-dispatched actions are reachable" — a weaker claim than "all actions are reachable." The gap is structurally invisible until you explicitly look for it, because the lint, by design, doesn't report on what it can't reach.

**Suggested action:** When building or trusting a routing lint or reachability test, check whether it covers all dispatch surfaces in the system, not just the primary one. If your project has a registry/rail path AND a legacy elif/fallback path, either (a) migrate all handlers to the audited surface so the lint has complete coverage (the full fix), or (b) document the scope limit explicitly — "this lint does not audit elif-only handlers; those are unverified until migrated" — so future agents don't read a passing lint as a guarantee of complete reachability. Green on an incomplete-surface audit is not the same as all-clear.

## Sources Read

- **Klatch** — git log (48h): brief delivery commits only. No new Klatch-internal methodology this window; skipped.
- **Piper Morgan** — git log (48h, full): #1394 B4 built and ratified (session-activity ledger primitive — the architecture for this was covered in the July 13 brief; B4 is the build, not a new direction); B3 plan ratified by Arch (pre-classifier reference resolution, direct-emit form — downstream refinement of the July 13 ADR-078 direction); #1411 shipped (update_issue registered on rail + registry) + Arch's create_issue-cohort scoped-gap finding documented in ADR-077; ADR-070 Amendment A fully built (config-masquerades-as-outage fix, #1398); DNS cutover resolved (3-bug chain, operational); Ship #051 LinkedIn syndication (Comms). One transferable finding above; rest build completions or operational.
- **Globe** — git log (48h): new session Jul 15 (flat-v7 HD morph verified + ensemble uncertainty spike). Flat-v7 technique approved by xian ("very smooth action"). Ensemble rendering implemented: N perturbed reconstructions averaged (per-plate rotation-pole jitter σ=5°·u + time jitter σ=25 Ma·u), producing probability-cloud visualization of geologic uncertainty (dense at well-constrained positions, dissolving at the uncertain fringe). Activity noted; no cross-relevant methodology finding for non-viz projects.
- **weather, one-job** — brief delivery commits only; skipped.
- **nyt-crossword** — automated status commits; skipped.
- **atlas, cuneo, optilisten, mediajunkie** — no commits in 48h window; skipped.

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
