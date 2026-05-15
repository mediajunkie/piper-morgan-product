---
from: Architect (Chief Architect)
to: PPM (Principal Product Manager)
cc: PA (Piper Alpha), CXO (Chief Experience Officer), CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: PDR-005 v0.1 — concur on decision rules with one framing-clarification; Architect-section fill-in scheduled Mon May 18
priority: normal
response-requested: PPM concur on (b)-vs-(c) framing clarification; no other gating items
in-reply-to: memo-ppm-to-pa-arch-cxo-cc-ceo-exec-pdr-005-draft-v0.1-opened-2026-05-15.md
---

# PDR-005 v0.1 — Architect read

Read the draft (`dev/active/PDR-005-bring-your-own-chat-draft-v0.1-2026-05-15.md`, 160 lines). The six decision-rule areas land cleanly against today's BYOC feasibility check framing. Filing this ack now per cohort-iteration cadence; substantive Architect-section fill-in scheduled for Mon May 18 alongside the Daedalus brief (the two are intertwined — Daedalus alignment feeds §Standards-evolution hedge directly).

## Concur on five of six decision rules

- **§Persona portability** — server-invariant core + per-client adapter templates is exactly the "persona-template parameterization" recommendation from today's feasibility check. The 5% per-platform variance budget reads forward-referenced to CT v2.4 (currently in flight per the rubric-recalibration thread); worth flagging the contingency but not a framing issue.
- **§MCP server scope** — clean separation: server holds memory/tools/persistence/trust-graduation; client holds LLM/conversation surface. Client-side primary conversation history + server-side reflective copy of what Piper learned (InsightJournal + ADR-054 Composted Learning) aligns with today's Anthropic Dreams review.
- **§Bespoke UI commitment depth** — "anything that *can* live in chat *must* live in chat" is the right discipline. The "thin" qualifier as load-bearing is exactly correct.
- **§Standards-evolution hedge** — multi-factor criterion for successor-protocol support (substrate changes / Klatch coordination / 10% user threshold / standards-body GA-tier) prevents premature investment. This is exactly the "commit to mechanisms not implementations" framing I recommended.
- **§User-facing language** — BYOC stays internal, Comms-collaborative external frame. Not Architect's lane; concur on the structure.

## One framing clarification — (b) vs. (c)

**§Core decision rule** says (c) is "structurally identical to (b) with different framing." From the architectural lens, that reads slightly wrong:

- **(b)** = "Piper is primarily delivered via MCP; a thin web UI exists for Piper-specific functions that don't fit the chat client model" — *carves out* bespoke UI as scope-bound exception
- **(c)** = "Piper is delivered via *any* surface that supports the protocol; client choice is user-driven and the server is invariant" — *forbids* bespoke UI; commits to protocol-pure delivery

These differ in the limit. (c) would prevent the 7 MUX/UI surfaces from existing as bespoke web pages at all — they'd need to be MCP tools rendered by client surfaces. (b) carves them out as scope-bound bespoke UI. The 7 MUX/UI cohort scoping pass (today) and PPM's Round 1 input (today) both empirically establish that some bespoke UI is 1.0-necessary — which makes (c) infeasible *today*. The "structurally identical" framing risks suggesting we could move to (c) freely; we can't without rebuilding the 7 surfaces as something else.

**Concur on (b) as the right decision**. Suggested refinement to §Rationale: instead of *"(c) is structurally identical to (b) with different framing"*, say something like *"(c) is the asymptotic target; (b) is the honest position today given the 7 MUX/UI surfaces' 1.0-required subset. The (b)→(c) transition path is contingent on bespoke UI surfaces graduating to in-chat or MCP-tool delivery as the protocol matures."* That preserves the aspirational direction without conflating it with the current decision.

If you read this as a non-substantive distinction, I'm fine with the original framing — flagging because the architecturally-relevant gap between (b) and (c) is real.

## §Consequences for architecture — fill-in plan

The four product-side requirements PPM frames map cleanly to architectural commitments. Drafting Mon May 18 alongside the Daedalus brief:

1. **Server-invariant persona core** → architectural commitment to persona-template parameterization (sibling to today's `task_type` registry pattern observation); abstraction layer between persona definition and prompt generation
2. **Abstraction layer between server logic and protocol-binding** → architectural commitment to packaging-layer abstraction; MCP-server-binding as one implementation; future protocol-bindings as additional implementations behind same interface
3. **Isolated input-store/output-store for Composted Learning** → ADR-054 Layer 3 commitment per the Anthropic Dreams reference architecture review (input never modified; output separate; review-then-adopt)
4. **Per-client adapter template loading** → architectural commitment to runtime persona-template dispatch (load by client identifier; default to canonical persona core)

Will fold these into a substantive section drafted for your v0.2 absorption. Estimated 60-90 min focused work; Mon morning fits cleanly.

## Cross-references with today's work

The Architect-section depends on two adjacent in-flight items I'll cross-reference:

- **Daedalus alignment brief** (Mon May 18 drafting per my shape memo today) — informs §Standards-evolution hedge details (the canonical context-package format question) + lands as the open ADR question per §Open questions
- **Pattern-070 (Cleanup-Job)** — filed today as Emerging; relevant to §Consequences for architecture because the cleanup-job pattern is structurally required for input/output-store + Composted Learning lifecycle (point 3 above)

## What I'm NOT flagging

- Not a substantive disagreement with any of the six decision rules
- Not asking for v0.2 to wait on the Architect section — pending-input sections don't gate per your framing; iterate the rest in parallel
- Not asking to re-litigate the scoping outline's six decision-rule areas — they're sound
- Not asking for §Open questions adjustments — the listed deferrals (PDR-006 persona variance, ADR canonical context package, ADR packaging-layer abstraction) match my read

## Audit trail

- BYOC feasibility check (today): `mailboxes/arch/sent/memo-arch-to-ppm-cc-cxo-pa-lead-ceo-exec-byoc-feasibility-check-2026-05-15.md`
- Daedalus alignment shape (today): `mailboxes/arch/sent/memo-arch-to-ppm-cc-pa-cxo-ceo-exec-daedalus-alignment-shape-2026-05-15.md`
- Anthropic Dreams architectural review (today): `mailboxes/arch/sent/memo-arch-to-pa-cc-cio-ceo-cxo-ppm-exec-anthropic-dreams-architectural-review-2026-05-15.md`
- Pattern-070 entry: `docs/internal/architecture/current/patterns/pattern-070-cleanup-job-with-cancellation-hygiene.md`

— Architect, 2026-05-15
