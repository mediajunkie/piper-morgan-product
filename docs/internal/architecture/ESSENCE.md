# The Essence of Piper Morgan

**Version**: **v1.1 — RATIFIED by xian 2026-10-25** (v1.0 RATIFIED by PM 2026-08-30, in-conversation, after the full trifecta pass:
CXO concur + one challenge + two amendments · PPM concur + one amendment · HOST trust lens. The
synthesis and its addendum: `reviews/2026-08-architectural-review/trifecta-synthesis.md`.)
**Date**: 2026-08-29 (v0.1) · 2026-08-30 (v1.0) · 2026-10-14 (v1.0.3) · 2026-10-25 (v1.1, ratified by xian 10-25 12:40; amendment log at the end)
**Authors**: Chief Architect, from the Architectural Review 2026 (PM+Arch co-led); every claim
traces to the review's evidence (`docs/internal/architecture/reviews/2026-08-architectural-review/`)
or a PM ratification recorded in `decisions.log` on 2026-08-29.

**What this document is**: the single current answer to *what Piper Morgan IS — what it does today,
for whom, on which surface* — and the classification of everything else in the repo relative to
that. It exists because a clean-room agent handed our full doc set concluded the corpus was "rich
in decisions and forensics and nearly empty of current state" and could not tell which of three
described products was real. This is the document that answers that. **It is living current law**:
the ADR corpus is history (append-only, citable); when reality changes, this changes, by PM
ratification, with dated amendments.

---

## For whom

**xian, first and definitionally.** In PM's own ratified words: *"if this product does not work
for me then it fails."* One rung of the ladder at a time: the alpha testers (~11, real) are the
second rung; a beta wave is the third — each positioned relative to the first, never displacing
it. Purchases justified by users beyond the current rung go through the scope-bet gate
(`docs/internal/architecture/bets/`), with a named buyer, or they don't happen.

## What Piper Morgan is

**A product-management colleague — not a tool, not a platform, not a harness.** Seven commitments
make that sentence mean something. Each is load-bearing: remove it and the product is something
else.

1. **It accumulates its owner's context, and the owner can walk away with it.** Memory, knowledge,
   preferences, and working history compound per-owner — this is the retention moat the entire
   field's evidence points at, and the reason Piper exists instead of a chat tab. **Portability is
   architectural, not policy**: the accumulated context must be exportable-by-construction, in
   open formats, because every ownership promise enforced by policy eroded in the field's record
   and none enforced by structure did. (PM: "empowering the user, not the rent-seeking
   service-provider.")
2. **It works on the judgment artifacts its owner is accountable for.** GitHub issues first —
   real, filed, in the owner's repos — then the PRD/spec/document family. The field's verdict:
   own the artifact or own the record system; everything between is acquisition inventory. Piper
   owns the artifact side.
   *(Scope, xian 2026-10-24: GitHub issues are the 1.0 artifact. Drafting PRDs and specs comes after 1.0, built on the document and GitHub capabilities once they're solid; #2139 is the nearest existing work. The commitment is unchanged; only its sequencing is recorded.)*
3. **It shows up once a day, answers whenever asked — and earns the relationship in the first
   exchange.** The morning standup is the proactive ritual — the one feature where the original
   vision survived, and the specific behavior that converts "a chatbot I visit" into "an assistant
   that works for me." Responsiveness the rest of the day is table stakes; the ritual is the
   relationship — and first contact is where colleague-or-chatbot is decided, which is why
   cold-start reflection is the first build increment. The ritual is **surface-bounded**: where
   the host affords initiation (web today; a notification layer if that bet is ever made), Piper
   opens; on MCP — structurally request-response, per ratified PDR-005 — it takes the
   **response-shaped variant**: the user opens the conversation, and Piper's first turn IS the
   briefing. *(v1.0: surface qualification + first-contact clause, per the trifecta pass.)*
4. **It never lies, and it degrades honestly.** No fabricated data, no claimed actions it didn't
   perform, no capability overclaim, honest decline over silent improvisation. This discipline is
   the one assumption re-ratified after every reckoning in the project's history, and it is
   enforced structurally where possible (consent gates, EffectClass tiers, anti-confabulation
   rails) rather than by vigilance.
5. **It understands requests through one derived, constrained authority.** The registry-backed
   routing rail — not N surface-local opinions. The incident record's largest cluster came from
   violating this; the Inversion (chat path) and the MCP tool catalog (BYOC path) are the same
   derived artifact wearing two interfaces, and both converge here.
6. **It meets its user on whichever surface they're working in, as one Piper.** The hosted web app, the MCP endpoint and plugin inside the user's own chat, and chat platforms when they return are complementary surfaces over one backend. The user chooses where to meet Piper, and we don't decide that for them. The web app is a real surface, the beta surface, where conversations, the radar and settings live. The MCP and plugin surface ships during the beta, and its completion gates public beta. Each surface expresses the same Piper as that surface allows (initiation where the host affords it, per commitment 3). Connector rule, ratified: Piper's backend holds a grant only where it must act without the user present (standup generation, background reflection, document mirroring), or where Piper is itself the host (the web app reads with the user's own grant). Inside another host's chat, in-conversation reads of third-party services belong to that host's connectors.

   *(v1.1, xian 2026-10-24: "not a destination app" retired as an overreading; sources: xian 08-08 and 08-10, gate R7, PDR-005 and PDR-006 Amendment 1.)*
7. **It works WITH its owner, like a colleague — not just FOR them, like an appliance.**
   Offer-first collaboration (propose, draft, ask — never hijack the session), judgment framed as
   a peer's ("here's my read; you decide"), the working stance of an apprentice becoming a peer.
   Honesty (commitment 4) is necessary but not sufficient — an honest vending machine is still a
   vending machine. Operationalized by the already-ratified **Colleague Test** (the standing DoD
   gate for exactly this property); on the BYOC path, its recomposition variant carries the same
   gate. This commitment licenses no new build — it gates HOW everything else is built.
   *(Added v1.0: CXO's amendment 1, PM Decision 1 — the headline is now cashed, not rhetorical.)*
   *(Instrument status, dated 2026-08-30, precision-corrected same night — the REQUIREMENT here
   is ratified; the recomposition INSTRUMENT is not: its honesty-under-recomposition axis **still
   scores PENDING-PROBE for issuing a pass** — the first probe revised its criteria rather than
   validating them. Claude arm: the core fabrication case confirmed live (prose fabricated from a
   failed read — a fluent, correct answer to a different question; the directive-carrying
   structured payload stayed honest), AND the reversed case **falsified the scale's
   structural-guarantee clause** (a host silently dropped a descriptor field — structure alone
   buys no rendering guarantee; whether directives or salience carry the effect is confounded,
   deconfounding re-run designed). GPT arm blocked on credits, zero data. **The gate can inform
   design decisions; it cannot yet issue a T-axis pass.** Per CXO's flag: a reader applying this
   gate should know its instrument's state without excavating #1463.)*

## What it does today, on which surface (dated snapshot — 2026-08-29, "not yet" line 2026-08-30)

- **Live surface**: the web-chat app (alpha, ~11 testers + PM), in **explicit maintenance mode**
  as of 2026-08-29 — bugs fixed, nothing new built *(superseded 10-23: the hosted web UI is the beta surface (PDR-005 Amendment 1); Sprint E builds on it.)*. It classifies intents (legacy chain carries
  observed traffic; flip-1 live for `read_status` since 08-21 via deployment secrets, unexercised
  to date; full staged flip ratified and sequenced by Lead into PM's next watched round — *superseded
  10-14: the live router now runs first on unarmed turns for the flipped read waves and ten
  allowlisted writes, per ADR-080; see SYSTEM.md*),
  files/updates GitHub issues via a real MCP consumer path, manages todos/reminders
  (consent-gated), generates the standup, ingests and answers questions about documents, and holds
  the conversational floor with the honesty rails.
- **Build surface**: the hosted MCP path (`mcp.pipermorgan.ai`, PDR-006) — where all new effort
  goes, in roughly the clean-room agent's increment order: cold-start reflection first.
- **What the MCP path cannot do yet** *(dated 2026-08-30 — update this line as items close, per
  the tense discipline: these sentences describe the path we're building, and here is the honest
  gap between it and today)*: it **cannot initiate a turn** (the ritual runs response-shaped
  there until a push-capable surface exists); **honesty hedges are not yet payload-borne** (the
  structured `source_failed` flag travels end-to-end, but the hedge text lives in a floor prompt
  that doesn't exist on BYOC — recomposition probe + tool-output design precede the first tool
  results); and **its build items sit at the FRONT of the Production milestone, not in MVP**, per
  PM's 2026-08-30 ruling: **MCP-path completion is the PUBLIC-BETA GATE.** Private beta (v0.9.0,
  invitation-only) starts when the MVP milestone closes and runs on the existing surface; public
  beta requires the MCP path complete. The one prior MVP-resident MCP item (#1688) moves to
  Production-front accordingly.
- **Connectors, honestly stated**: GitHub — real MCP, load-bearing. Calendar — live via Google SDK
  (an honest shim; MCP upgrade is an implementation detail). Notion — live via REST, its held
  grant governed by Bet 003 (the mirror bet). Slack — descoped to Fast Follow, adapter dead.
- **The numbers behind "today"** (Leg B census, denominator stated): 491 non-init modules; ~69%
  load-bearing; ~19% dead or loaded-but-never-invoked, being retired with provenance.

## What everything else is — the classification

Every module, doc, and capability in the repo is exactly one of these, with the census
(`findings/leg-b-live-state-census.md`) as the evidence base:

- **Essence** — implements a commitment above. Protected; changes need PM ratification.
- **Extension** — reachable, useful, optional (operator CLI, publishing tools). Kept while cheap.
- **Experiment** — flag-gated, labeled, with an owner and a question it exists to answer.
  Unlabeled experiments get labeled or retired.
- **Superseded** — decided-out by a recorded ruling (spatial committed-theory, Era-2 platform
  code). Retired with provenance; the deletion record is the July model.
- **Dead** — no callers, no decision keeping it. Retired through fix-or-delete; no eulogy needed.

## What Piper Morgan is NOT (the boundary, stated so it can't drift)

Not an **agent harness** (that's a commodity knife-fight against the platform vendors' own
products — both the field's evidence and the lived experience of solo builders currently in
exactly that fight say so). Not a **walled garden**: no surface is required, and none is the only way in. The web app is a surface the user can choose, never one they're made to come to. Not a **platform or marketplace**
(Era 2 bought that vision on unverified claims; July deleted its remains). Not **enterprise
multi-tenant SaaS** — unless and until a Bet Memo with a named buyer says otherwise. The
scope-bet gate governs all *becoming*; this document governs all *being*.

## Standing architectural rules carried into current law

- The classifier stays stateless (ADR-078 D4); state resolves before or beside the call, never by
  injecting history.
- Every intent-understanding mechanism feeds one dispatch rail. Piper currently has two such
  mechanisms on the chat path (the legacy LLM-classifier chain and its successor, the
  constrained registry-backed router it is migrating to); whichever one interprets a request,
  the same rail dispatches it and the same consent gate evaluates the operation's declared
  effect class — so no routing change can ever loosen a safety check. *(Verified how, per HOST's
  2026-08-29 trust-lens flag: the single-convergence-point structure is verified by static trace
  (08-25); the legacy-routed path is verified behaviorally by #1685's A/B seam assertion; the
  successor-routed path's behavioral receipt LANDED for one write: 2026-10-06, Lead, in-process app
  plus Postgres, `complete_todo` chosen by the live router (`route=inversion`) stopped at the confirm
  and acted only after "yes"; served again on the alpha test account 10-07. That is one write op of
  the ten in `FLIP_WRITE_ALLOWLIST`; for the other nine the "can ever" rests on the static trace
  (the router hands the rail the same WorkflowEntry the legacy chain does, Arch 09-25), not on a
  served receipt.)*
- **The LLM decides meaning; code decides permission, checks meaning against real data, and shows
  you before it acts** (ADR-080, PM-confirmed 2026-10-06). Permission code (identity and ownership,
  consent and confirm, the single dispatch rail, honest refusal, CI and deploy gates) stays.
  Uncertain meaning never writes. The interpretation layer only shrinks, by ratchet: the
  pre-classifier literal ceiling fell 567 → 90 (10-14), of which 29 are a ruled permanent floor.
- The LLM floor guarantee: at least as good as a well-prompted LLM with the user's context —
  handlers make it better, never different.
- Derive, don't hand-maintain: registries, catalogs, prompts, and manifests are generated from
  one source; hand-maintained copies are the documented failure mode.
- Verification names its layer, and every coverage claim states its denominator.

---

*Amendment log:*
- *v1.0, 2026-08-30 — **RATIFIED by PM** after the full trifecta pass. Changes from v0.1: seventh
  commitment added (colleague, cashed via the Colleague Test — Decision 1); commitment 3
  surface-qualified + first-contact clause (CXO challenge resolution (a) + amendment 2); dated
  MCP "not yet" line added recording Decision 2 (**MCP stays Production, front-loaded;
  MCP-path completion = PUBLIC-BETA GATE**; #1688 → Production-front) and the payload-honesty
  gap (#1463 trace). Consent-invariance verification footnote retained pending the watched-round
  behavioral receipt. Full synthesis: `reviews/2026-08-architectural-review/trifecta-synthesis.md`.*
- *v1.0.1, 2026-08-30 (same evening) — instrument-status note added to commitment 7 per CXO's
  dependency flag (ratified requirement vs. not-yet-validated instrument, stated in place) and
  updated same-hour with the first probe results (PA's Claude-arm run: governing hypothesis
  confirmed on the core case; GPT arm pending credits). Tense-honest per the document's own rule.*
- *v1.0.2, 2026-08-31 (precision, per CXO's same-night correction — their interpretation of the
  probe landed after v1.0.1 was written): the instrument note no longer says "can begin issuing
  informed judgments" (reads as scoring license the instrument forbids on T); the accurate split —
  inform design decisions YES, issue a T-axis pass NOT YET — plus the falsification framing (the
  probe revised the scale's criteria rather than validating them; rubric now v0.2). The drift this
  fixes is requirement-vs-instrument running the subtle direction: law saying slightly more than
  its instrument permits, which reads as progress.*
- *v1.0.3, 2026-10-14 (Arch; recording a PM-confirmed ratification and a landed receipt, no new
  commitment): ADR-080 added to the standing rules; the consent-invariance footnote moves from
  PENDING to landed-for-one-write with its denominator (1 of 10 allowlisted writes served; the rest
  static); the 08-29 snapshot's flip-1 clause marked superseded. Overdue against this doc's own
  rule (same-day on a ratification touching the boundary): ADR-080 was confirmed 10-06.*
- *v1.1, 2026-10-24 (xian's Production-map rulings 3 and 4; drafted by Arch; ratified by xian 2026-10-25 12:40, relayed by Exec): commitment 6 rewritten (surfaces complementary, web is the beta surface, the connector rule gains the Piper-as-host clause); the "destination UI" boundary line replaced by "walled garden"; commitment 2 records PRD/spec drafting as post-1.0; the 08-29 maintenance-mode clause marked superseded.*
