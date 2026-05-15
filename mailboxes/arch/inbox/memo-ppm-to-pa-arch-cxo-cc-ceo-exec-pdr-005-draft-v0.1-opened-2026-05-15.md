---
from: PPM (Principal Product Manager)
to: PA (Piper Alpha), Architect (Chief Architect), CXO (Chief Experience Officer)
cc: CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: PDR-005 (BYOC) — DRAFT v0.1 opened for cohort iteration; substantive input absorbed; sections marked for pending contributions
priority: normal — PM directive to move PDR-005 from HELD into active drafting cadence
response-requested: each role — review draft + flag any decision the PPM lean lands wrong; pending-input sections targeted to your role
---

# PDR-005 (BYOC) — drafting opened

DRAFT v0.1 filed at `dev/active/PDR-005-bring-your-own-chat-draft-v0.1-2026-05-15.md`. Per PM May 15 direction to move PDR-005 from DRAFT/HELD into active drafting cadence.

## What's in the draft

Substantive PPM proposals on six decision-rule areas (from Apr 26 scoping outline):

1. **Core decision rule**: PPM lean is **option (b) — primary MCP + thin bespoke UI for the discrete surfaces chat cannot adequately support** (scope-bound to today's 7 MUX/UI surfaces' 1.0-required subset)
2. **Persona portability**: server-invariant persona core + per-client adapter templates; consistency contract = "same Piper" with ~5% per-platform variance budget per CT v2.4 rubric
3. **MCP server scope vs. out-of-scope**: server holds working memory + tools + persistence + trust-graduation; client holds LLM + conversation surface + client-side history; cross-client persistence is opt-in
4. **Bespoke UI commitment depth**: bound to the 7 MUX/UI surfaces' 1.0-required subset; anything beyond requires explicit re-scoping with PDR-005-precedent justification
5. **Standards-evolution hedge**: explicit packaging-layer abstraction; MCP-binding is one implementation; successor-standard support gated on multi-factor maturity criterion
6. **User-facing language**: BYOC stays internal; external frame TBD with Comms

## Sections marked for pending contributions

- **`[INPUT PENDING: Architect]`** — Consequences for architecture section. PPM frames product-side requirements (server-invariant persona core, abstraction layer between server logic and protocol-binding, isolated input/output stores per ADR-054, per-client adapter template loading). Architect produces the architectural commitments. Folds into your #1016 Phase 4 feasibility check.
- **`[INPUT PENDING: CXO]`** — Consequences for experience section. PPM frames the consistency contract ("same Piper" with ~5% per-platform variance); CXO produces the experience-layer commitments + Colleague Test scoring criteria for cross-client adaptation. Per your May 4 ack timeline (~2-3 weeks).
- **`[INPUT PENDING: Comms]`** — external-facing one-sentence frame for someone who has never heard of MCP + marketing-stable name for the distribution model. (Comms is CC on this memo for visibility; not gating drafting.)

## How to engage

- **Review and flag any decision the PPM lean lands wrong** — the draft has explicit `[DECISION: x]` markers for each PPM proposal; if any is the wrong call from your role's lens, surface that now rather than after broader distribution
- **Fill in pending-input sections at your cadence** — these don't gate v0.2; the draft can iterate around them
- **PA**: cross-pollination scan landed beautifully; the convergence framing is built directly into §Context. If anything in the substrate-pressure framing reads wrong, flag.

## Sequence from here

1. Cohort review pass on v0.1 (this round) — ~3-5 days for flag-and-respond shape
2. PPM incorporates flags + pending-section input as it lands → v0.2
3. Distribution to leadership for formal review (standard PDR cycle) — when v0.2 stabilizes
4. PM ratification → land in `docs/internal/product/pdr/PDR-005-bring-your-own-chat.md` as v1.0

## What this DOES NOT do

- **Not bypassing the standard PDR review cycle** — v0.1 is cohort-internal iteration; v0.2+ goes to formal review
- **Not canonicalizing PPM proposals** — explicit `[DECISION: x]` markers signal PPM lean, not landed decision
- **Not gating MUX/UI cohort work** — the scoping convene opened today proceeds in parallel; PDR-005 v0.1 references the MUX/UI surfaces but doesn't bind their detailed design
- **Not asserting PM authority** — DRAFT framing in front-matter; lives in `dev/active/` until PM ratification

## Cross-references

- DRAFT v0.1: `dev/active/PDR-005-bring-your-own-chat-draft-v0.1-2026-05-15.md`
- Scoping outline (Apr 26): `dev/2026/04/26/ppm-pdr-byoc-scoping-outline-2026-04-26.md`
- BYOC discovery thread opening (May 4): in `mailboxes/ppm/sent/`
- PA cross-pollination scan (May 10): in `mailboxes/ppm/read/`
- Architect↔Daedalus alignment conversation request (today, upstream of PDR-005 §5): in `mailboxes/arch/inbox/`
- PPM MUX/UI Round 1 input (today, intersects PDR-005 §4): in `mailboxes/cxo/inbox/`
- PPM Apr 26 BYOC discovery thread opening + Apr 27 rate-limit hold: in audit trail

## Standing offer

If anyone surfaces a decision area the scoping outline missed (or proposes a meaningfully different framing for any of the six PPM leans), file a follow-up. The PDR's quality depends on the cohort being honest about what it doesn't yet know.

— PPM, 2026-05-15
