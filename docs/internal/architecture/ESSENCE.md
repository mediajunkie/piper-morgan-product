# The Essence of Piper Morgan

**Version**: v0.1 — DRAFT for PM ratification
**Date**: 2026-08-29
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

**A product-management colleague — not a tool, not a platform, not a harness.** Six commitments
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
3. **It shows up once a day, and answers whenever asked.** The morning standup is the proactive
   ritual — the one feature where the original vision survived, and the specific behavior that
   converts "a chatbot I visit" into "an assistant that works for me." Responsiveness the rest of
   the day is table stakes; the ritual is the relationship.
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

## What it does today, on which surface (dated snapshot — 2026-08-29)

- **Live surface**: the web-chat app (alpha, ~11 testers + PM), in **explicit maintenance mode**
  as of 2026-08-29 — bugs fixed, nothing new built. It classifies intents (legacy chain carries
  observed traffic; flip-1 live for `read_status` since 08-21 via deployment secrets, unexercised
  to date; full staged flip ratified and sequenced by Lead into PM's next watched round),
  files/updates GitHub issues via a real MCP consumer path, manages todos/reminders
  (consent-gated), generates the standup, ingests and answers questions about documents, and holds
  the conversational floor with the honesty rails.
- **Build surface**: the hosted MCP path (`mcp.pipermorgan.ai`, PDR-006) — where all new effort
  goes, in roughly the clean-room agent's increment order: cold-start reflection first.
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

*Amendment log: (none yet — v0.1 awaiting PM ratification.)*
