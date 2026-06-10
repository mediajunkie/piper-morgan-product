# BYO-Colleague Braintrust — Exec synthesis notes (2026-06-09 ~20:45 PT)

**Status**: working notes for the eventual synthesis-to-PM memo. PPM lens missing — see §"PPM gap" below. Synthesis memo HELD pending PPM (per `feedback_anchor_on_readiness_not_publish_date` half 2).

## Source set

| Lens | Author | Filed | Folded |
|---|---|---|---|
| Thesis (convener) | PA | 2026-06-07 (sent 6/9) | ✅ |
| Architecture / feasibility / fit | Architect | 2026-06-09 | ✅ |
| Methodology / innovation | CIO | 2026-06-09 | ✅ |
| Experience + trust (lens 1) | CXO | 2026-06-09 | ✅ |
| Experience + trust (lens 2 — Arch refinement) | CXO | 2026-06-09 | ✅ |
| Three-party trust | HOST | 2026-06-09 | ✅ |
| Roadmap sequencing + MVP-distro + PDR-shape | **PPM** | **PENDING** | — |

## Strong convergences (all 5 lenses agree)

### C1 — Composition, not greenfield (the dominant shape)

Three altitudes, same finding:
- **Architecturally** (Arch): 7 of 9 primitives map onto existing ADRs (ADR-065 wire format, ADR-066 packaging layer, ADR-053/#648 ProactivityGate, ADR-063 audit envelope, ADR-060 floor-first); 2 are extensions (`needs_signal` package_type + agent-attribution `actor_chain`). Don't design fresh; declare instances.
- **Experientially** (CXO): consent architecture rides the *existing* ProactivityGate (`can_act_autonomously`). Setup-friction sequencing is the same in-your-workflow move as #1181 invited-watch. Coherence find: BYO-colleague consent + Radar/proactive-presence/invited-watch are ONE consent system.
- **Strategically** (CIO): "own the judgment" = methodology-34 turned outward, one altitude up. Same principle re-aimed from internal coordination to product shape. Inherits m-34's evidence + the "Platform Lapped Us, We Climbed" narrative spine.

**Synthesis line**: BYO-colleague isn't a new architectural arc — it's the cohort's existing architecture (wire formats / gates / methodology corpus) reaching one altitude up. Materially de-risks the implementation estimate AND the strategic-defensibility claim.

### C2 — Both halves of the colleague move have working internal prototypes

The thesis names two halves: reactive (ask for what's missing) + proactive (ship context-prep routines).

- **Reactive prototype** = `consult-piper` skill (Arch). The skill-as-broker pattern is the existing one; generalization is refactoring not invention.
- **Proactive prototype** = the duty cycle itself (CIO). The thin-job-prompt machinery we've been hardening for weeks IS the context-prep-routine architecture: versioned skill + staged state + scheduled executor. The shape "before our 1:1, pull these three things" = what carry-forward + START self-heal do for our own agents every morning.

**Synthesis line**: methodology-becomes-product isn't aspirational. We've been dogfooding it on ourselves; the architecture is the same one we'd ship.

### C3 — Methodology is the most defensible of the three distinctive layers

The thesis lists calibration / methodology / role-shaping as the thin distinctive layer. CIO sharpens: they are NOT equally defensible. A platform can plausibly ship calibration primitives and role-shaping scaffolds (mechanism-shaped, productizable). The accumulated operating discipline — methodology corpus, trust gradient, honest degradation, Conscious Floor — resists commoditization. Per m-34's own predicted signal.

**Synthesis line**: invest the distinctive-layer dollars in methodology; treat calibration/role-shaping as the substratable companions.

### C4 — Trust gradient extends, doesn't restart

CXO + HOST + Arch all converge: the consent architecture for BYO-colleague is one consumer of the existing trust gradient, not a parallel one.

- CXO: rides ProactivityGate, three tiers (enumerate / gather / act)
- HOST: trust gradient applies to the three-party shape (user ↔ assistant ↔ Piper); honest degradation extends to agent↔agent handoffs
- Arch: provenance (data-source) covered by ADR-063; agent-attribution extends it with `actor_chain`

**Synthesis line**: BYO-colleague is a beta-architecture decision that the existing trust-gradient design absorbs, with two named extensions (3rd consent tier + actor_chain).

## Distinctive contributions worth surfacing

### D1 — HOST's three-party reframe (the load-bearing structural insight)

Reframe: NOT Piper ↔ host-agent (2 parties). It's **user ↔ assistant ↔ Piper (3 parties)**, and Piper is a **GUEST** in the user's trust relationship with their own assistant.

Governing principle: **"Piper must never make the host agent do anything that erodes the user's trust in their own assistant."**

5 boundaries that fall out:
1. **Be a good guest** — augment the host relationship, never supplant. Deputization should read as "your assistant being good at knowing what to consult."
2. **Hidden-principal expectation-violation** — provenance is relationship-clarity, not just correctness. Deputization must be LEGIBLE at the moment it happens, not buried in a setup agreement.
3. **Consent is a gradient, not a gate** — calibrate by sensitivity × reversibility. NEW DIMENSION: resource-consent (spending the user's LLM key / rate-limit — newly load-bearing post-6/9 usage-wall).
4. **Reciprocity** — proactive context-prep routines are the GIVE; lead with the give, not the take. The healthy reciprocal half is already in the thesis.
5. **Honest degradation extends to agent↔agent handoff** — the Conscious Floor becomes a property of the handoff, not just the final answer.

One-line: **"Piper is a guest in the user's relationship with their own assistant — it must leave that relationship stronger than it found it, and never become a principal the user can't see."**

This is the synthesis's strongest reframe. PA's 2-party framing is sufficient for the architecture; HOST's 3-party reframe is necessary for the user-experience and trust shape. They compose; they don't conflict.

### D2 — CIO's "ship the routine, keep the loop" (moat-protection principle)

The cleanest caution the thesis didn't carry. If methodology is the moat AND we ship methodology as routines, we're externalizing the moat — a visible recipe is a copyable recipe. Resolution: **you can't defend the artifact, only the judgment that keeps producing better artifacts.** A static shipped routine is copyable; the living calibration loop that produces next month's better routine is not.

**Ship freely; retain the loop.** The routine is this month's output; the practice is the asset.

For PPM: this tells where defensibility sits for sequencing — the routine library is a distribution surface, the calibration loop is the retained asset.

### D3 — CXO's value-per-step sequencing + partial-BYO as first-class

Setup-friction reframe: not a volume problem, a sequencing problem.
- Each setup step must return immediate felt value
- Just-in-time connect (Calendar at first task that needs it, not at onboarding)
- Honest degradation = useful at every partial-setup state (partial-BYO is first-class, not a waiting room)
- Reframe BYO steps as trust-building deposits (economics=trust felt only when each step's trust-payoff is surfaced)

### D4 — CXO's 3-tier consent (refinement off Arch's enumeration-as-disclosure risk)

| Tier | What it is | Bar |
|---|---|---|
| **Enumerate** | discover what connectors the host has | per-need-scoped (never "list everything") |
| **Gather** | read through an available connector | transparent + reversible + user-visible |
| **Act** | write / execute on behalf | explicitly invited + scoped (#1181 primitive) |

Capability discovery is need-driven, not inventory-driven. Same "just-in-time, not up-front" discipline as setup-friction sequencing, applied to discovery.

### D5 — Arch's PDR-006 + ADR-068 companion shape recommendation (per m-38)

Per methodology-38 (PDR/ADR tier separation): the BYO-colleague decision is decision-rule altitude → may want a PDR (PDR-006 candidate) with the ADR-068 companion, matching the PDR-005 + Q6/Q7 pattern established this past week. PPM owns the roadmap-shape call.

Architect's ADR-068 D-section structure ready post-convergence:
- D1: skill-as-broker (m-40 ACL instance #9, first cross-arc instance)
- D2: structured needs-signal package_type (Pattern-072 9th app)
- D3: capability discovery as inverse ADR-066 D2 handshake
- D4: staged-context package format (ADR-065 D2 conformant; host-stored)
- D5: multi-actor attribution audit envelope extension (`actor_chain`)
- D6: freshness-window discipline for staged context (timestamps + decay; same shape as #371)

## Risks named (composite)

| # | Risk | First named by | Mitigation |
|---|---|---|---|
| R1 | MCP wire-format brittleness (structured needs-signal vs prose response) | Arch | `extensions.piper-morgan` namespace + Postel discipline (additive, non-breaking) |
| R2 | Capability-discovery enumeration as privacy leak | Arch (then CXO 3-tier formalizes) | Per-call-scoped + user-acknowledged at first-use |
| R3 | Staged-context freshness — stale-by-morning | Arch | Timestamps + per-resource decay (calendar < 1hr, issues < 24h) |
| R4 | Multi-actor attribution chain — audit trail looks like host acted alone | Arch (with CXO concur) | ADR-063 audit envelope extension w/ `actor_chain` |
| R5 | Resource-consent (spending user's LLM key/limit) | HOST (post-6/9 usage-wall) | Treat resource-spend as its own consent dimension; visible in deputization legibility |
| R6 | Shipping the routine commoditizes the recipe | CIO | "Ship freely, keep the loop" — moat is the calibration practice, not the routine |
| R7 | Trust-erosion via Piper-supplants-host-agent | HOST | Design rule: deputization reads as "your assistant being good at knowing what to consult" — Piper's value accrues *through* the host, not at its expense |

## PPM gap (what's missing for the synthesis to be complete)

PA's frame asked PPM for: "where does this land on the roadmap? It reframes §M5 / beta / PDR-005. Does BYO-substrate + colleague change product sequencing or the MVP-distro definition?"

Without PPM, the synthesis to PM is missing:
- **Roadmap sequencing** — BYO-colleague vs other product work (M5 / beta / Q6/Q7 ADRs already unblocked)
- **MVP-distro definition** — does BYO-colleague change what "MVP shipped" means?
- **PDR-006 / ADR-068 shape decision** — Arch surfaces the candidate (per m-38); PPM owns the roadmap call on PDR-vs-not + which ADR companions
- **Beta architecture decisions hardening** — PA's explicit "before the beta architecture decisions harden" framing — PPM's lane

PA's implicit deadline ("before beta hardens") is the operational urgency. Chasing PPM with procedural framing per the new pin (sender-side meta-rule from PM 13:03 correction).

## Spine candidate for the synthesis-to-PM (when complete)

**"BYO-colleague is composition, not greenfield — at every altitude — and the colleague move is methodology-34 reaching one altitude up."**

Substantiation lines:
- The architecture inherits 7 of 9 primitives from existing ADRs (Arch)
- The consent gate is the one we already built (CXO)
- The strategic posture is m-34 applied at the product-substrate altitude (CIO)
- Both halves of the colleague move (reactive + proactive) have internal working prototypes (consult-piper + duty cycle)
- The trust shape is three-party (user ↔ assistant ↔ Piper), and Piper is a guest (HOST)
- The methodology layer is the defensible one; calibration and role-shaping are substratable companions (CIO)
- The moat is the calibration loop, not the shipped routine (CIO)

Open for PPM: where this lands on the roadmap, what it does to MVP-distro, PDR-006 vs not, beta sequencing.

---

*Working notes. Synthesis memo to PM holds for PPM lens per source-set discipline.*
