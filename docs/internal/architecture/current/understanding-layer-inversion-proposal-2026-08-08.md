# The Understanding-Layer Inversion — proposal for Arch review

**Author**: Lead, 2026-08-08 (the day PM moved beta a month and said "period or not period is
not how these things ultimately get solved" — this document is the structural answer).
**Status**: PROPOSAL — the concrete object for the routing/floor design review Arch accepted.
**Exhibit A**: PM's 13:19–13:24 live transcript (session log 2026-08-08): 8 distinct
understanding-layer failures around two successful executions. The rails work; the
understanding between the user and the rails does not.

## The diagnosis (one paragraph)

The chat interface is built inside-out. Deterministic string machinery — regex pre-classifiers
(surface 1), word-template entity extraction, pattern-guarded flow claiming — performs the
"understanding," while the LLM is consulted only as a fallback classifier with an UNENFORCED
action vocabulary (surface 2, emits paraphrase drift by design) and as the prose floor (which
fabricates capability denials under confusion — #1517 ×2 live). Result: string matching does
language; intelligence does damage control. Every fix adds a pattern; every phrasing is a new
bug; the failure catalog (#1471, #1490, #1521, #1527, #1492-partial, #1529, #1530, #1488-class)
is one defect wearing eight numbers.

## The inversion

**One LLM routing call does the understanding; determinism does what determinism is for.**

1. **Tool-selection routing**: a single small-model call per turn whose output is CONSTRAINED to
   the action registry (the 106 rail keys + NONE→floor) — enforced structured output, not
   prompt-suggested strings. The registry (ACTION_REGISTRY + workflow_entries) becomes the
   grammar, not a suggestion. Vocabulary drift becomes structurally impossible.
2. **Context-carrying**: the routing call sees session state — pending soft-offer, active guided
   flow, B3 referent ledger, the user's OWN entity names (projects, lists) — so "yes please"
   binds to the actual offer, "the CoVa project" resolves against the real project list
   (case/article/punctuation trivially irrelevant), and "i am not doing the standup right now"
   reads as the refusal it is. Entity extraction as a template problem DISAPPEARS; it becomes
   arguments in the tool call, validated against real data before execution.
3. **Guided flows lose claiming power**: a flow may REQUEST the next turn, but the routing call
   sees the request and the user's words together — refusal/topic-change routes out. Universal
   escape is a property of the architecture, not a pattern list (#1529).
4. **The floor gets a capability manifest and honesty guardrails**: derived from the same
   registry (per #1433's reachable-set), with hard instructions — never deny a registered
   capability, never retract a recorded success (#1517). The decline-freshness ratchet extends
   to floor prose via judge-evaluated corpus cases.
5. **The deterministic front shrinks to exact-match only**: slash-command-like verbatims and the
   B3 ledger (already deterministic-by-construction and session-relative). Everything else goes
   to the routing call. The pre-classifier as a ROUTER dies; its patterns become test fixtures.

## What survives untouched (most of the system — this is a subsystem rebuild, not a rewrite)

The action rail + 30 handlers (proven by the same transcript: archive/restore EXECUTED correctly
when reached) · ACTION_REGISTRY + MAX_DISPATCH_SITES=0 ratchet · #1433 reachability ledger (its
POINTER assertions retarget to the new resolver) · repositories/data layer · Slack surface ·
security floor · canonical corpus + judge (becomes the rebuild's acceptance instrument).

## Latency & cost (the original reason the pre-classifier exists — answered)

Haiku-class routing call: ~200–400ms, fractions of a cent, cacheable on (normalized utterance ×
state fingerprint). The current architecture already pays an LLM call for most non-pattern turns
(surface-2 classification) — this REPLACES that call with a cheaper, constrained one rather than
adding a call. Deterministic exact-match front keeps the truly-hot paths free.

## Migration, measured not vibed

Phase 0 (this week): corpus grows from PM's live failures — every transcript sentence above
becomes a judged case; baseline the current architecture's corpus score honestly.
Phase 1: routing call built behind a flag, shadow-scored against the corpus + live-mirrored
traffic (routes logged, not executed). Gate: corpus ≥ current baseline AND the 8 Exhibit-A
failures all pass.
Phase 2: flag flips per-category (queries first, writes last — writes keep confirmation).
Phase 3: pattern-router deletion via delete-module-safely; ratchet asserts the pre-classifier
file's pattern count only shrinks.
Convergence instrument: scripts/discovery-rate.py weekly (the PM commitment) — this rebuild is
the bet that bends it.

## Decision requested from Arch

1. Ratify the inversion direction (or counter-propose within one week — PM's month is burning).
2. Rule on the routing call's model tier + structured-output mechanism.
3. Own the floor-honesty contract spec (#1517) as part of this, not separate.
4. The pin:/ledger mechanics under the new resolver.

**Standing moratorium (Lead, effective 2026-08-08, PM's direction)**: no new routing patterns,
extraction tweaks, or flow-claiming fixes outside this rebuild — emergencies excepted. Routing
failures found meanwhile are corpus material, not patch tickets.

## Addendum (same day, PM conversation): local-model sequencing — for explicit Arch ruling

PM's standing question: a small LOCAL model for routine understanding/parsing. Agreed sequencing
(decision requested as part of the review): build the inversion against a Haiku-class API model
FIRST — this forces the routing call into a clean, swappable component with the corpus as its
acceptance instrument. A local 3–8B model then AUDITIONS against the same corpus (the task —
constrained selection + argument extraction — is classification-adjacent and locally plausible);
swap when the corpus says it routes as well and the economics say it matters. Model choice becomes
a config decision with a scoreboard, never an architecture bet. Contra-indicators recorded: the
contextual cases (offer-binding, refusal-mid-flow) are where small models are weakest; local
inference grows the Fly footprint; beta-scale API routing costs pennies/day and REPLACES the
existing surface-2 call rather than adding one.

## Addendum 2 — PM priority ruling (2026-08-08, in-conversation): FUNDAMENTALS FIRST

PM: *"I would like to unblock addressing the most fundamental unfinished business first, before we
spend too much time polishing specific workflows."* Month-plan ordering follows: inversion Phase 0
(corpus baseline) starts immediately pre-ratification; floor-honesty contract, observability
restoration (#1518), and false-trails cauterization steps 1–2 rank ABOVE all surface polish
(#1497/#1515/#1519/#1512 explicitly deferred). Recorded in decisions.log.
