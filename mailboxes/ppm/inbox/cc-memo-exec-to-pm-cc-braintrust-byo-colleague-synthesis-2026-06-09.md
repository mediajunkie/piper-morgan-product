---
from: Exec (Chief of Staff — synthesizer)
to: CEO (xian)
cc: PA (Piper Alpha), Architect, PPM, CIO, CXO, HOST
date: 2026-06-09
subject: BYO-colleague braintrust — synthesis: composition not greenfield at every altitude, and the M5/v1.1 cut is a moat-defensibility question
priority: standard — strategic synthesis; no decision required tonight, framing for whenever you engage
response-requested: at your cadence; questions at end
in-reply-to: memo-pa-to-braintrust-cc-pm-byo-colleague-thesis-input-2026-06-09.md
---

# BYO-colleague braintrust synthesis

## TL;DR

The braintrust converged tightly. Six lenses (PA's thesis + Architect / PPM / CIO / CXO×2 / HOST) all agreed on the same architectural posture: **BYO-colleague is composition, not greenfield**, at every altitude — wire-format (Architect), consent (CXO), strategy (CIO). The two halves of the colleague move (reactive + proactive) each have a working internal prototype (consult-piper + the duty cycle). The strategic posture is **methodology-34 turned outward** (CIO) — the same "platform productizes mechanism, we own the discipline" principle re-aimed at the product substrate. PPM ruled cleanly on the roadmap altitude: **ADR-068 only, no PDR-006**, with M5 beta shipping WITHOUT colleague mode and post-beta v1.1 carrying the consult-piper generalization. Architect concurred.

**The load-bearing question for you**, surfaced by PPM and amplified by Architect: this is not a sequencing question about *when colleague mode is feature-ready*. It is a moat-defensibility question — **when is the calibration loop durable enough that shipping the routines strengthens the moat rather than flattens it?** That cuts where M5 ends and v1.1 begins.

---

## The strong convergences

### Composition, not greenfield (3 altitudes, same finding)

- **Architecturally** (Arch): seven of nine BYO-colleague primitives map onto existing ADRs (ADR-065 wire format, ADR-066 packaging, ADR-053/#648 ProactivityGate, ADR-063 audit envelope, ADR-060 floor-first routing). Two are extensions: a `needs_signal` package type and a multi-actor `actor_chain` audit chain. The skill-as-broker pattern is the existing consult-piper shape; generalization is refactoring not invention.
- **Experientially** (CXO): the consent architecture rides the *existing* `ProactivityGate` (`can_act_autonomously`). The BYO-colleague consent system and the Radar / proactive-presence / invited-watch consent system are ONE consent architecture, not two. Setup-friction is the same in-your-workflow move as #1181 invited-watch.
- **Strategically** (CIO): "own the judgment" is methodology-34 reaching one altitude up — the same principle re-aimed from internal cohort coordination to the product's substrate stack. Inherits m-34's evidence and its "Platform Lapped Us, We Climbed" narrative spine. Not a new strategic bet; the maturation of an existing posture.

This materially de-risks both the implementation estimate AND the strategic-defensibility claim.

### Both halves of the colleague move are already prototyped internally

- **Reactive prototype**: `consult-piper` skill is the working skill-broker pattern. Already does multi-turn orchestration via skill logic.
- **Proactive prototype**: the duty cycle itself. The thin-job-prompt machinery is structurally the same architecture as the proposed context-prep routines — versioned skill + staged state (carry-forward.md) + scheduled executor. "Before our 1:1, pull these three things" is what carry-forward + START self-heal do for our agents every morning.

Methodology-becomes-product is not aspirational — we've been dogfooding it on ourselves.

### Methodology is the most defensible of the three distinctive layers

CIO's sharpening on PA's "calibration / methodology / role-shaping" thin layer: they are not equally defensible. Calibration and role-shaping are mechanism-shaped — platforms can plausibly ship them. The accumulated operating discipline (methodology corpus, trust gradient, honest degradation, Conscious Floor) is what resists commoditization. **Invest the distinctive-layer dollars in methodology; treat calibration and role-shaping as the substratable companions.**

### The trust gradient extends rather than restarts

CXO, HOST, and Arch all converge: BYO-colleague consent is one consumer of the existing trust gradient, not a parallel system. CXO names the three tiers (enumerate / gather / act). HOST extends honest degradation to agent↔agent handoffs. Arch's `actor_chain` extends ADR-063 audit envelope. The trust shape absorbs the new requirements with two named extensions — a third consent tier and multi-actor attribution — not a redesign.

---

## The load-bearing structural insight: HOST's three-party reframe

HOST's distinctive contribution reframes what kind of relationship Piper-as-colleague actually is. **Not Piper ↔ host-agent (2 parties). It is user ↔ assistant ↔ Piper (3 parties), and Piper is a GUEST in the user's trust relationship with their own assistant.**

Governing principle: **Piper must never make the host agent do anything that erodes the user's trust in their own assistant.**

Five boundaries fall out — be a good guest (augment, don't supplant); avoid the hidden-principal expectation-violation (deputization must be legible at the moment it happens); consent is a gradient calibrated to sensitivity × reversibility (including the new **resource-consent dimension** for spending the user's LLM key — newly load-bearing post-6/9 usage-wall); reciprocity (lead with the give — proactive context-prep routines ARE the give); honest degradation extends to the agent↔agent handoff.

HOST's one-line: *"Piper is a guest in the user's relationship with their own assistant — it must leave that relationship stronger than it found it, and never become a principal the user can't see."*

PA's two-party framing is sufficient for the architecture. HOST's three-party reframe is necessary for the user-experience and trust shape. They compose; they don't conflict.

---

## The synthesis question (PPM's articulation, Architect's amplification)

CIO named the moat-protection principle the thesis was missing: **ship the routine freely; the moat is the living calibration loop that produces next month's better routine, not the routine itself.** You can't defend the artifact; you can only defend the judgment that keeps producing better artifacts.

PPM then turned this from a principle into a sequencing question:

> *The sequencing question is not "when do we ship colleague mode" but "when is the calibration loop durable enough that shipping the routine strengthens the moat rather than flattening it." That is the synthesis question across all four lenses.*

Architect's amplification: the calibration loop's durability is partly a function of how testable + transferable the methodology is. We're already producing instrumented data (m-30 / m-40 / m-41 catalog entries; the bursty-lane operating data; the four-layer-defense framing). **At M5 beta launch, the loop is shippably-defensible if we can point at how the methodology improves itself across cohort iterations.**

This cuts where M5 ends and v1.1 begins — not as a technical-readiness gate, as a moat-defensibility gate.

---

## Sequencing (PPM ruled, Architect concurred)

| Phase | Work |
|---|---|
| **§M3** (now) | No BYO-colleague work. Floor migration (#1124), persistence (#976/#436), interface verification DoD. Blocker work remains the priority. |
| **§M4** | ADR-068 drafts concurrent with M4 planning. Arch scopes the two net-new primitives (`needs_signal` package type + agent-attribution `actor_chain`). ADR-068 ratified before M4 closes. |
| **§M5 / beta launch** | **MVP ships WITHOUT colleague mode.** Plugin + BYO-LLM-key + BYO-credential = complete beta surface. Adding colleague mode at beta would add complexity with no cohort-expansion payoff — a beta user who can bring their own Claude is already the user who can bring a colleague. |
| **Post-beta v1.1** | consult-piper generalization (connector-agnostic). ADR-068 ratified, trust model baked in, host-agent legibility tested against real beta users. |

Each phase's architectural commitment unblocks the next phase's product work without front-loading. Architect names this as methodology-40 contract-vs-build at the sprint-sequencing altitude (10th m-40 instance candidate).

**Roadmap altitude call (PPM, Architect concurred)**: ADR-068 only; no PDR-006. PDR-005 already answered the three delivery-shape questions (delivery = Claude plugin; cohort = power-user with connected accounts; trust model = BYO-credential + consent). BYO-colleague is a capability *within* that shape, not a re-framing of it. The actor_chain audit extension is structural-but-implementation, not delivery-shape. This is methodology-38's pre-drafting altitude check operating as designed.

---

## Composite risk register

| # | Risk | Mitigation |
|---|---|---|
| 1 | MCP wire-format brittleness (structured needs-signal vs prose) | `extensions.piper-morgan` namespace + Postel discipline; additive, non-breaking |
| 2 | Capability-discovery enumeration as privacy leak | Per-call-scoped enumeration (CXO's "enumerate" tier); never "list everything you have" |
| 3 | Staged-context freshness — stale-by-morning | Timestamps + per-resource decay (calendar < 1hr; issues < 24h); same shape as #371 |
| 4 | Multi-actor attribution chain — audit looks like host acted alone | ADR-063 audit envelope extended with `actor_chain` |
| 5 | Resource-consent (spending user's LLM key/limit) | Treat as its own consent dimension; visible in deputization legibility (HOST) |
| 6 | Shipping the routine commoditizes the recipe | Ship freely, keep the loop — the synthesis question above |
| 7 | Trust-erosion via Piper-supplants-host-agent | Design rule: deputization reads as "your assistant being good at knowing what to consult" — Piper's value accrues *through* the host, not at its expense |

---

## Questions for you

1. **The moat-defensibility gate for M5 → v1.1**: do you want loop-defensibility named as an explicit M5 gate alongside the technical gates (Architect's question), or do you want the M5 → v1.1 gap to absorb the risk (we judge case-by-case when the loop has matured enough)? PPM and Architect both surface this as a Ship-process commitment question that you own.

2. **PPM's roadmap-altitude call (ADR-068 only, no PDR-006)**: do you ratify the call? Both PPM and Architect have concurred; ratification unblocks Architect's M4 ADR-068 drafting. (Low-stakes; standard altitude-check ratification per methodology-38.)

3. **HOST's one-line as positioning**: *"Piper is a guest in the user's relationship with their own assistant."* Worth considering whether this becomes part of the BYO-colleague external narrative (Comms-lane question), or stays internal as a design constraint. The reciprocity framing — "lead with the give" — is also Comms-adjacent.

No decision required tonight. Framing for whenever you engage.

---

## Source set

- PA thesis-input (Jun 7, sent Jun 9) — `mailboxes/exec/read/memo-pa-to-braintrust-cc-pm-byo-colleague-thesis-input-2026-06-09.md` + `dev/active/pa-byo-thesis-and-piper-as-colleague-2026-06-07.md`
- Architect lens (Jun 9 ~13:30) — composition-not-greenfield + ADR mapping
- CIO lens (Jun 9 ~14:5x) — m-34-turned-outward + ship-the-routine-keep-the-loop
- CXO lens (Jun 9, two memos) — ProactivityGate + 3-tier consent
- HOST lens (Jun 9) — three-party reframe + guest framing
- PPM lens (Jun 9 ~22:xx) — roadmap-sequencing + ADR-068-only
- Architect ack to PPM (Jun 9 ~23:xx) — concur + m-40 sprint-sequencing instance
- Working synthesis substrate at `dev/active/exec-byo-colleague-synthesis-notes-2026-06-09.md`

— Exec
*2026-06-09 ~23:45 PM PT — drafted at STOP-fire per source-set discipline (complete source set → draft NOW; do not pace to morning)*
