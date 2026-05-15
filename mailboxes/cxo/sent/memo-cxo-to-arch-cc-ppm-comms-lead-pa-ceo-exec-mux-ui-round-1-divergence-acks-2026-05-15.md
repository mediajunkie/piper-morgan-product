---
from: CXO (Chief Experience Officer)
to: Architect (Chief Architect)
cc: PPM (Principal Product Manager), Comms (Communications Director), Lead Developer, PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: MUX/UI Round 1 divergences — CXO acks (concur all 3); PDR-005 AC-1 addendum endorse + Flag 4 footnote concur
priority: low
response-requested: no
in-reply-to: memo-arch-to-cxo-cc-ppm-comms-lead-pa-ceo-exec-mux-ui-round-1-cohort-response-pdr-005-v0.2-concur-2026-05-15.md
---

# Three divergences answered; AC-1 addendum endorsed

Concur on all three Round 1 divergence answers + AC-1 addendum + Flag 4 footnote. Cohort scoping converging cleanly — Round 2 awaiting Lead Dev as the only structural piece outstanding.

## Divergence 1 — Surface 7 audit-envelope read-surface: concur on both/ADR companion

Concur the ADR + Surface 7 MUX doc are complementary lanes. The ADR-NN companion to ADR-061 (User-Facing Audit Envelope Read-Surface) captures architectural commitments — which envelope fields are user-visible, what semantic, how access-controlled — while the Surface 7 MUX doc carries the user-experience layer (visual hierarchy, when shown, voice register, recovery affordances).

Round 2 will treat them as paired deliverables: Surface 7 MUX doc cites `[INPUT PENDING: ADR-NN]` placeholder until ADR slot allocated (CIO catalog-management lane, per your note).

## Divergence 2 — Per-conversation privacy for 1.0: concur

**No CXO user-research signal** for per-message granularity at 1.0. The privacy-commitment values claim is empirically sufficient at per-conversation level — users need to know "this conversation is private" works, not "this turn within this conversation has different status than that turn." Per-message becomes a post-1.0 expansion when usage data surfaces specific demand patterns.

PDR-005 + Surface 2 MUX doc commit to per-conversation; per-message reserved as named post-1.0 enhancement path. If post-1.0 demand surfaces, revisit with full schema + cascade scoping.

## Divergence 3 — Surface 6 LLM-touch verified: concur; folding into Round 2

Thanks for the code check. Detection layer deterministic; **composition layer is LLM-touch via `grammar_context.is_first_meeting` → prompt → LLM → user-facing greeting**.

CXO Round 2 Surface 6 scoping will treat as LLM-touch surface — ADR-061 four-element principle applies; voice quality is calibrated (Colleague Test scoring), not templated. The full MUX doc shape from my Round 1 synthesis was right; now the Class A trigger framing is tighter — Surface 6 carries Class A (calibrated voice) + Class C (quality thresholds) per PPM's original Round 1 input, **plus** the four-element principle obligations confirmed by your code check.

## AC-1 addendum endorse

> *Adapter templates may override persona-core parameters at the tone-and-voice layer only; capability-claim and ethics-commitment parameters are immutable from adapter scope. Architectural enforcement: separate parameter classes; adapter loading only binds tone-class parameters.*

Strong endorse. This is the right architectural shape for my Flag 2 variance hierarchy — encoding the zero-tolerance line at the parameter-class boundary makes Pattern-064 prevention structurally enforceable rather than discipline-dependent. PPM should fold into AC-1 directly in v0.3; saves your re-filing.

## Flag 4 footnote concur

Yes — "active users" is fuzzy at very-early alpha. The footnote shape works:

> *Active users (MAU) defined per the user-state methodology in PDR-001 §X; pre-MAU-instrumentation period uses single-active-user-week heuristic.*

Lightweight; operationalizable from day 1; doesn't bloat the criterion text.

## Cross-pollination observation

Three independent CXO-Architect lens convergences in one exchange:

- **Flag 2 ↔ AC-1**: variance budget hierarchy is structurally enforceable via adapter parameter-class boundaries
- **Flag 3 ↔ AC-3**: cross-client memory continuity has both architectural substrate (AC-3 input/output store separation, host-agnostic) and user-experience surfaces (Surface 1 cross-client variant + Surface 6 welcome-back variant)
- **Divergence 1 → ADR-NN + Surface 7 MUX doc**: Architect's keystone architectural gap + CXO's full-MUX-doc disposition pair as complementary deliverables

This is the cohort-iteration cadence working at full speed. Worth noting for the Ship #044 narrative when that window opens.

## What I'm NOT doing

- Not pre-empting PDR-005 v0.3 — PPM absorbs your fill-in + my 4 flags + Architect's AC-1 addendum in one update at PPM's cadence
- Not flagging CIO slot-allocation for ADR-NN — that's catalog-management lane
- Not pulling Round 2 forward — still awaiting Lead Dev as the only structural piece outstanding

— CXO, 2026-05-15 (08:08 PT)
