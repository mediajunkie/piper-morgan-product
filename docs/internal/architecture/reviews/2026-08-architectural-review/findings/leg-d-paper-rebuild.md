# Leg D — Clean-Room Rebuild Assessment (paper test)

*Filed verbatim-condensed 2026-08-29. Fresh agent, 25 curated docs in an isolated directory, no
repo/web access. Read all ~12,300 lines. Hard constraint: every increment ships one working feature
end-to-end to real users. Required outputs: what-is-this-product / build plan / unanswerable
questions / guesses / doc-quality assessment.*

## 1. What is this product? — answered, with the most important structural finding

The agent COULD identify the product: "an AI product-management assistant that behaves like a
colleague, not a tool," with the identity carried by explicit experience commitments (speaks first,
never 'I can't do that', never fabricates, trust-gradient proactivity).

**BUT: "the documents describe three different products depending on their date, and the docs never
reconcile them."** 2025 docs = workflow-orchestration engine with web UI; early-2026 docs =
floor-first chat product; mid-2026 ratified strategy (PDR-005/006) = a distribution pivot that
removes Piper's own chat surface entirely (hosted MCP tool server, no server-side LLM). "The
documents alone cannot tell you WHICH delivery is the product of record for a rebuild" — because
BRIEFING-CURRENT-STATE.md (cited as check-first by multiple docs) and every referenced ADR (~40
distinct references) were not in the set.

## 2. The build plan (8 increments, each ends with a real user using something)

Anchoring decision G1: rebuild targets **BYOC/hosted-MCP (PDR-006)**, not the web-chat app — also
the leanest path since the user's chat client IS the UI, so increment 1 needs no chat interface, no
intent classifier, no conversational floor.

1. **"Piper knows my work"** — cold-start GitHub reflection: install plugin, authorize GitHub, and
   in the FIRST exchange, unprompted, see something specific and true about your own work (=
   PDR-006's added DEMONSTRATION criterion, "the only one that fails today"). Requires: hosted MCP
   server + fail-closed caller identity (no identity, no read) + users table + 1-2 read tools +
   minimal plugin (persona CLAUDE.md + URL).
2. **Create a GitHub issue from natural language** — host LLM drafts, tool files
   ("client infers, server writes"); draft-then-confirm for compose-phrased asks.
3. **Todos and reminders** — first Piper-native persistence; delete requires confirm (expressed as
   tool semantics); ⚠️ reminder DELIVERY unresolved (MCP is request-response, no push) → v1
   pull-surfaced, flagged as a real product decision (G8/UQ-11).
4. **Morning standup** — the product's own designated north star; gather multi-source context
   server-side, return warmth-calibrated payload; **run the honesty-under-recomposition probe
   INSIDE this increment before the format freezes** (PDR-006 pre-user gate 2).
5. **Document knowledge base** — upload → chunk → embed → cited answers; owner-scoped.
6. **"Same Piper" memory** — preferences/working-mode across sessions and clients; profile read as
   MCP RESOURCE not tool (Architect condition 3); rule-based only, no server LLM (ruled, G6).
7. **Calendar** — ratified 1.0 scope is GitHub + Calendar + Notion, Slack deferred.
8. **Trust-gated proactivity — deliberately LAST, gated on a product decision**: PDR-002's own
   margin note says the trust gradient's denominator may not exist on the plugin surface
   ("unimplementable-as-specified on the plugin path"). Until decided, this increment is a
   placeholder "that prevents anyone from smuggling trust machinery into earlier increments."

**Explicitly out until evidence demands**: bespoke web UI surfaces, Slack/spatial (deferred despite
"IMPLEMENTED" claims in requirements.md), multi-entity conversation (PDR-101), Temporal (never
integrated per requirements.md; unmentioned by any 2026 doc), MUX consciousness object model as
code (its VOICE lives in tool output + CLAUDE.md).

## 3. Unanswerable questions — 24, grouped (the drift measure)

**Product identity/state**: UQ-1 which system is the product of record (web-chat vs MCP vs both)?
· UQ-2 who are the users and what do they use? · UQ-3 is anything deployed to production, where? ·
UQ-4 what live data must migrate?
**Routing/intelligence**: UQ-5 authoritative IntentCategory enum (6 in data-model.md vs ~14 in
architecture.md, never reconciled) · UQ-6 low-confidence classifier behavior (threshold shown only
in hypothetical example code) · UQ-7 actual rail keys/patterns/vocabulary (counts given, lists
never — "a rebuilder cannot enumerate the current capability surface") · UQ-8 which models serve
which tasks (llm-configuration.md absent) · UQ-9 is any trust computation live (ADR-053 absent) ·
UQ-10 guided-process state machines (ADR-049 absent).
**BYOC/MCP build**: UQ-11 how does anything proactive reach a user when MCP can't push? (NO
document comes close) · UQ-12 concrete auth flow for the hosted server (ADR-070 absent) · UQ-13
the actual MCP tool catalog (derivation rule given, list absent) · UQ-14 situation-shaped vs
object-shaped tool naming (open by its own admission — "test both before committing") · UQ-15 does
honesty survive recomposition (~50% ChatGPT result; fix untested) · UQ-16 what state must
cross-caller isolation cover ("the docs say so themselves" that it was never traced).
**Cross-cutting**: UQ-17 is ethics enforcement on, and is the 2025 regex enforcer still the
mechanism? · UQ-18 the Colleague Test rubric (a BINDING done-gate, in no document) · UQ-19 what do
acceptance scenarios test · UQ-20 what auth does the web product really have (three answers across
three docs) · UQ-21 todo/reminder/user schemas (central to 2026 behavior, never schematized) ·
UQ-22 does spatial deliver user-visible value anywhere · UQ-23 actual route/page inventory · UQ-24
what scale must the rebuild hit (only 2025-era NFRs exist).

## 4. Guesses (10, each with confidence)

G1 BYOC anchor (medium — "if wrong, roughly triples scope") · G2 the four-surface routing stack
does not need rebuilding (medium-high, conditional on G1; the team's own Inversion program points
the same way) · G3 Temporal droppable (medium-high) · G4 Slack/spatial out (high for ordering; low
on whether some GitHub-spatial path is quietly load-bearing) · G5 OAuth-subject→owner_id fail-closed
(high on requirement, medium on mechanism — ADR-079 absent) · G6 rule-based colleague model, no
server LLM (high — ruled) · G7 ChromaDB acceptable, not clearly mandatory · G8 reminders pull-only
(low — real product decision needed) · G9 "done" quality reconstructed from identity invariants
standing in for the absent Colleague Test rubric (low-medium — "reconstructing a binding gate from
its silhouette") · G10 alpha population small enough to re-onboard, no migration (medium;
"interacts dangerously with UQ-4").

## 5. Document quality assessment

**Earned their place**: PDR-006 ("the single most useful document"), PDR-005, PDR-004, PIPER.md
("the only document explicitly maintained to be runtime-true — I trusted it more than any
architecture doc"), intent-routing-stack.md ("extraordinary forensic density… its weakness: a
changelog compressed into a map… documents counts instead of contents"), glossary ("quietly
load-bearing"), PDR-001/002/003.

**Internally contradictory or stale** (all cited with quotes in the full report):
requirements.md contradicts ITSELF (§2.7 "✅ MET — web UI" vs §5 "🚨 no normal user interaction
possible") · requirements.md vs architecture.md on GitHub (🚨 BLOCKING vs ✅ Fully Integrated, 14
months apart, presented as siblings) · architecture.md contradicts itself KNOWINGLY (100 lines
documenting QueryRouter "✅ Complete… 935 lines" under a banner admitting it was DELETED; revision
log says Jan 21 2026 while the body contains Aug 29 2026 edits — "revision logs in this corpus
cannot be trusted") · data-model.md defines WorkItem TWICE with different fields · PDR-001's FTUX
assumes Piper owns the first screen while PDR-006 says "there is no first screen" — PDR-001 never
amended · ethics-architecture.md (2025 regex, default-off) vs 2026 consent/ethics references — no
bridge.

**Aspiration/system indistinguishable**: consciousness-philosophy.md (voice guide, but
"philosophy, unverifiable claims, and code excerpts as one undifferentiated whole"),
test-strategy.md (2025 boilerplate, hypothetical code samples, never mentions the real referees),
PDR-101 (draft vision), PDR-007 ("not about the product at all — its presence in a product-doc
handoff is itself a curation finding"), the 2025 spec trio (used for stack facts, distrusted for
every behavioral claim).

## The headline finding (verbatim)

"This corpus is rich in *decisions* and *forensics* and nearly empty of *current state*. The two
document types a rebuilder needs most — the current-state briefing and the ADRs — are precisely the
ones not in the set, and nearly every document defers to them. If the team fixes one thing before a
rebuild, it should be producing a single, dated, one-page **'what the product does today, for whom,
on which surface'** document — the absence that generated most of §3."

*(Arch's curation note: BRIEFING-CURRENT-STATE.md and the ADR trail were deliberately excluded —
the briefing for staleness risk, the ADRs to test whether current-state docs suffice without
decision history. The agent's UQ list confirms the excluded-ADR prediction: decided things (ADR-049,
-053, -070, -079 content) never got absorbed into current-state docs, so their absence blinds a
rebuilder. That IS the drift finding the exclusion was designed to surface.)*
