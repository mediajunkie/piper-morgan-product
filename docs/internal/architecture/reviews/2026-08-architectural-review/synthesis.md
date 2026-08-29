# Architectural Review 2026 — Discovery Synthesis

**Author**: Chief Architect (personally — reading was delegated, judgment was not)
**Date**: 2026-08-29
**Inputs**: nine discovery legs (`findings/`), run blind to each other per the plan's method
disciplines. C5 (Dialog/Granola) pending PM transcript paste; nothing below depends on it.
**Status**: DISCOVERY SYNTHESIS — this prepares the PM+Arch discussion (phase 3). It contains an
explicitly-labeled POV hypothesis for that discussion. It decides nothing by itself.

---

## How to read this

Nine researchers worked the same system from nine non-overlapping angles: three read only the
decision record, only the incident record, or only the scope trail; one read only the code (docs
forbidden); four scanned the outside world in industry-generic vocabulary (one not even knowing the
project exists); one tried to rebuild the product from 25 curated docs with no code. Where they
converge, the convergence is evidence — they could not have copied each other. Where they diverge,
the divergence is a finding too, and I report it rather than smooth it.

Every claim below cites its leg(s). The legs cite their own denominators; notable ones: A1 read 78
ADRs + 9 PDRs + all 194 decisions.log entries; A2 reviewed all 274 closed bug titles + 9 forensic
docs; B classified all 491 non-init modules (198K LOC) with a corrected tracer; D read all ~12,300
lines of the curated set.

---

## Convergence 1 — The documented architecture and the real one are different systems, and every leg found the gap independently

- **A2 (incidents only)**: the real architecture is "N independent local opinions where the
  documented architecture claims one authority" — for routing, identity, status, time, capability
  inventory, and the liveness graph itself — with a runtime that converts disagreement into silence.
- **A1 (decisions only)**: eight Era-2 commitments still read "Accepted"/"Implemented" while their
  implementing code was deleted in July as fabrication; the ADR index itself claims "Superseded: 0"
  while carrying superseded ADRs. The record is ahead of reality in both directions.
- **B (code only)**: ~19% of the codebase (38K LOC) is dead or loaded-but-never-invoked; lore-level
  claims fail spot-checks (the "deliberate exception" routes are simply unmounted; a docstring
  claims liveness via a file that no longer exists; the app's real personality enhancer is a
  duplicate of the dead one).
- **D (docs only)**: the docs describe *three different products* by date, unreconciled; "revision
  logs in this corpus cannot be trusted"; the corpus is "rich in decisions and forensics and nearly
  empty of current state."

**What this means**: the missing artifact is not more documentation — it is a different *kind* of
document. Nothing states what the system IS; everything states what was decided or what broke. Leg
D, knowing nothing of our plans, independently specified the essence document as its #1
recommendation: "a single, dated, one-page 'what the product does today, for whom, on which
surface.'" The review's central deliverable is confirmed by a witness who didn't know it existed.

## Convergence 2 — The expansion was a scope loan, and 2026 is the interest

- **A3**: eleven inflections carried the project from own-assistant to multi-tenant SaaS. Only one
  (ADR-000 — never formally Accepted) was even *shaped* like a scope decision; none was cost-boxed.
  The pivotal one — "alpha = multiple external users, therefore this is a multi-user product" —
  **has no artifact at all**; by ADR-058 it appears as settled fact. Enterprise NFRs arrived as
  requirements-template boilerplate on **day 5** of the project, before any code or user.
- **A1**: the record's rhythm is expansion-on-unverified-claims → reckoning, three full cycles.
  Six of the last ten ADRs are ownership/tenancy/hosted-load architecture — the tail of the decision
  record is dominated by paying for the earlier inflections.
- **A2**: the single largest incident cluster after routing is principal-dropping/single-tenant
  residue — a bug class that exists *only because* N>1 users share state, being drained fix by fix.
- **C1/C3 (blind outside view)**: overbuild — not underbuild — is the dominant cause of death in
  both adjacent categories. "Building the platform for assistants instead of an assistant" is the
  named category error; every failure is "shipping generalized capability before proving one daily
  habit."

**A3's closing line earns quoting because it's the sharpest sentence in the whole discovery**:
PDR-006's ratified model is functionally a rediscovery of "the user brings their own everything;
the server holds one person's tools and memory" — the shape a single-owner architecture would have
grown toward directly. *The inflections were scope loans, and 2026 has been the year of paying
interest.*

**Fairness note, PM's own words honored**: blame is shared and structural. A3 documents the
counter-inflections — the corrective instinct appeared repeatedly (ADR-044, ADR-051 amendment,
ADR-071 D1, PDR-006, no-optional-complexity) — but always locally and late. The failure mode was
never bad judgment on a given day; it was the absence of a gate that forced the scope question to
be asked as a question.

## Convergence 3 — What the field says the essence is, and what our own evidence says survives

Four blind outside scans and our own three inward legs agree to a striking degree on what carries
value:

| Essence candidate | Outside evidence | Inside evidence |
|---|---|---|
| **Accumulated owner-scoped memory/context** | C1: memory is THE retention moat ("context compounding"; 68% ChatGPT M12 retention; users keep ONE assistant because switching abandons context) | B: memory/knowledge substrate live; D anchors "Same Piper" as increment 6 |
| **The judgment artifact (GitHub issues, PRDs, tickets)** | C3: "own the artifact or own the record system — everything in between is acquisition inventory"; ChatPRD reached 100K users on document-writing alone | B: github_adapter is REAL MCP, load-bearing, 7 protocol call sites; the one deployed sidecar |
| **One proactive daily ritual (standup/brief)** | C1: the daily brief is what users pay $50–200/mo for; "the line between a chatbot I visit and an assistant that works for me" | A1: standup is the record's own designated north star, "the ONLY feature where the original vision survived" |
| **Honesty/trust discipline** | C3: the trust stack (act-as-user, audit, tiered gates, self-disclosure, instant stop) is now the price of entry — and the autonomy frontier is real: judgment work ships human-led everywhere | A1: honesty is the one assumption re-ratified after every reckoning; A2: fabrication incidents are what the discipline exists to prevent |
| **A single canonical routing/understanding authority** | — (internal-only concern) | A2: routing fragmentation is the #1 incident cluster (30+); B: the Inversion rail is fully built and dark; the elif chains are fully migrated (MAX_DISPATCH_SITES=0) |
| **One backend-owned MCP surface** | C4: your own product's surface is non-negotiably backend-owned; one server covers every host; C2: "intelligence beside the knowledge" won 2026 | PDR-006 ratified; D's rebuild anchors on it as both strategy and leanest path |

And what the field says is NOT essence — matching B's dead-code census almost item for item:
custom UI as destination (C3: "the structurally doomed shape"; B: mounted-orphan places route, dead
demo routes), orchestration frameworks and multi-agent planes (C1: "built and then removed or
declined by every successful project"; A1: ours deleted as fabrication July 2026), vector-index
infrastructure as source of truth (C2: agentic search made it optional; B: ChromaDB live but
unobserved per A2), breadth of connectors (C3: MCP made "100+ integrations" a weekend; B: 6 of 8
adapters are shims or dead), and speculative multi-tenancy (A3's entire table).

## Convergence 4 — The connector-layering question now has an evidence-backed answer shape

C4 (blind) produced a decision rule; B (code) tells us where we stand against it; PDR-006 (ratified)
is compatible with both. The rule: **hold the grant only where you must act without the user
present.**

Applied to Piper's four connectors, from B's census + the rule:
- **GitHub — backend-owned, correctly.** Standup generation, background reflection, and
  issue-filing under user identity are headless or write-bearing; B confirms it's our one real MCP
  consumer path, already talking to a deployed official-image sidecar. Keep.
- **Calendar — backend-owned, justified by the standup ritual** (headless morning brief needs
  calendar without a chat turn open). Currently a shim over Google SDK (B) — honest, works;
  upgrade-to-MCP is an implementation detail, not an architecture question.
- **Notion — genuinely ambiguous under the rule.** If Notion is only ever read in-conversation,
  the rule says delegate to the host's connector on the BYOC path; if the knowledge pipeline
  ingests from it headlessly, backend-owned stands. This is a *product* question about what Notion
  is FOR — flagging for the phase-4 discussion, not ruling here.
- **Slack — already descoped (PM, 08-27), and every leg retroactively endorses that call.** B:
  adapter is a shim AND dead; A2: the #1481/#1484 hold; C4: chat-platform reads are exactly what
  hosts mediate.

## Convergence 5 — The strategic question the evidence poses (the one that needs PM)

This is the tension I am obligated to surface rather than resolve alone.

**B's headline**: as configured today, 100% of chat traffic rides the legacy routing chain through
a 14,389-line file; the Inversion rail is fully built, reviewed, armed — and dark by default
config. *(Dated correction 2026-08-29, from Lead's live probe: "dark by config" was a
config-file-layer claim; the deployment layer has `read_status` live via fly secrets since 08-21,
genuinely unexercised — 0 events from real traffic absence. The observed-behavior claim stands;
the mechanism claim is corrected. See the correction block atop leg-b-live-state-census.md.)* **A2's headline**: that legacy chain is the single largest incident generator in the
project's history. **D's G2**: under the BYOC anchor, the four-surface routing stack *does not need
to be rebuilt at all* — the host LLM does tool selection; our own Inversion program was already
migrating toward "a constrained LLM call over a derived registry," which is architecturally the
same shape as an MCP tool catalog.

So the question: **the Inversion and the BYOC catalog are converging on the same destination — one
derived, constrained, registry-backed understanding authority. Do we finish walking there on the
chat path, the MCP path, or both, and in which order?** The web-chat path serves today's alpha
users and is where the honesty disciplines were forged; the MCP path is the ratified distribution
strategy and D's evidence says it's the leanest route to a new real user. These are not enemies —
the registry, the consent gates, and the EffectClass/allowlist machinery transfer across both
(that's what "the rail" was for). But *sequencing effort* between them is a product-strategy call
with real architectural consequences, and it has been living implicitly. It should live explicitly.

## Divergences and honest tensions (reported, not smoothed)

1. **"Mostly dead" lore vs. B's census**: the codebase is 69% load-bearing by module. The dead 19%
   is real and large (38K LOC) but the system is not a ruin — the correction cuts both ways: less
   catastrophizing, but also no comfort that the live 69% includes the 14K-line intent_service.py.
2. **C1's "memory is the moat" vs. the ruled rule-based colleague model** (no server LLM, #558
   deferred): not a contradiction — rule-based storage still accumulates the moat — but C1's
   evidence raises the *priority* of memory investment relative to where our roadmap has it.
3. **A2 flags genuine classifier non-determinism (#1467, #1677) while failure-class 8 blames dual
   implementation**: both mechanisms are live; no doc apportions the incident stream between them.
   The Inversion addresses both, which is convenient, but we should not claim we know the split.
4. **The demo plugin mounts live routes in every default deployment** (B) — small, concrete,
   nobody decided it, and exactly the shape of unchosen surface this review exists to catch.
5. **No numbered ADR since 079 (Jul 16)** while six weeks of substantial rulings live only in
   decisions.log (A1). Deliberate cadence change or drift? Not recorded. I own this one — it's my
   surface.

## The POV hypothesis (labeled as such, for the phase-3/4 discussion)

If discovery had to compress to one paragraph: **Piper Morgan's essence is a PM colleague that (1)
accumulates owner-scoped memory of one person's work, (2) produces and acts on the judgment
artifacts that person is accountable for — GitHub first, (3) shows up once a day, proactively and
honestly, in the standup ritual, (4) understands requests through ONE derived, constrained routing
authority, and (5) reaches its user through the chat surface the user already lives in, via one
backend-owned MCP server.** Everything else in the repo is extension (fine), experiment (fine, if
labeled and gated), or residue of the scope loan (to be retired with provenance, as the July
deletions modeled). The single-owner instinct the project started with was not naïveté the
architecture outgrew — on this evidence it was the correct read of the product, temporarily buried
under defaults, and PDR-006 is the architecture finding its way back.

## Proposed next steps (for PM to reorder or veto)

1. **Phase-3 discussion** on this synthesis — the five convergences, the strategic question in
   Convergence 5, and the Notion-purpose question from Convergence 4.
2. **Essence of Piper Morgan v0.1** drafted from the discussion (deliverable 6) — one page, dated,
   "what the product does today, for whom, on which surface," plus the essence/extension/experiment/
   superseded/dead classification keyed to B's census.
3. **Cheap mechanical wins that need no new decisions** (already-ruled or obviously-unchosen):
   execute the ruled spatial disposal; retire B's newly-found dead families through the same
   fix-or-delete pipeline; unmount the demo plugin from default deployments; correct the eight
   still-"Accepted" Era-2 ADR statuses with supersession notes (A1's list — the ADR trail should
   tell the truth about itself).
4. **The bet-shaped scope gate** (phase-5 candidate, flagged at kickoff): A3's evidence makes the
   case — eleven inflections, one shaped like a decision. Design the gate so the *next* "should we
   become X" question must be asked as a question, with a named buyer and a cost box.
5. **C5** when transcripts arrive; it feeds the ship-early discussion, not the essence.
