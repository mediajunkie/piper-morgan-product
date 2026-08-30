# The Essence of Piper Morgan

**Version**: **v1.0 — RATIFIED by PM 2026-08-30** (in-conversation, after the full trifecta pass:
CXO concur + one challenge + two amendments · PPM concur + one amendment · HOST trust lens. The
synthesis and its addendum: `reviews/2026-08-architectural-review/trifecta-synthesis.md`.)
**Date**: 2026-08-29 (v0.1) · 2026-08-30 (v1.0)
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
6. **It reaches its user through the chat surfaces the user already lives in.** One backend-owned
   MCP server (PDR-006), plugged into Claude/ChatGPT/whatever-comes-next — not a destination app.
   Connector rule, ratified: Piper's backend holds a grant only where it must act without the user
   present (standup generation, background reflection, document mirroring); in-conversation reads
   of third-party services belong to the host's own connectors.
7. **It works WITH its owner, like a colleague — not just FOR them, like an appliance.**
   Offer-first collaboration (propose, draft, ask — never hijack the session), judgment framed as
   a peer's ("here's my read; you decide"), the working stance of an apprentice becoming a peer.
   Honesty (commitment 4) is necessary but not sufficient — an honest vending machine is still a
   vending machine. Operationalized by the already-ratified **Colleague Test** (the standing DoD
   gate for exactly this property); on the BYOC path, its recomposition variant carries the same
   gate. This commitment licenses no new build — it gates HOW everything else is built.
   *(Added v1.0: CXO's amendment 1, PM Decision 1 — the headline is now cashed, not rhetorical.)*

## What it does today, on which surface (dated snapshot — 2026-08-29, "not yet" line 2026-08-30)

- **Live surface**: the web-chat app (alpha, ~11 testers + PM), in **explicit maintenance mode**
  as of 2026-08-29 — bugs fixed, nothing new built. It classifies intents (legacy chain carries
  observed traffic; flip-1 live for `read_status` since 08-21 via deployment secrets, unexercised
  to date; full staged flip ratified and sequenced by Lead into PM's next watched round),
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
exactly that fight say so). Not a **destination
UI** (the structurally doomed shape in the copilot category). Not a **platform or marketplace**
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
  successor-routed path's behavioral receipt is PENDING — scheduled onto Lead's watched flip
  round. Until it lands, this line's "can ever" is design-intent for that path, not settled
  fact.)*
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
