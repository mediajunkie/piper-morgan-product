# BYO substrate, Piper brings the judgment — synthesis (2026-06-07)

**Purpose**: name the frame that runs through this weekend's BYOC work in one place, before the beta
architecture decisions. PM-flagged ("we are doing some critical BYO- thinking now") and extended with the
upstream-collaboration idea ("could the person's own Claude be deputized to gather/act on Piper's behalf
— Piper as a *colleague* for their assistant, not a tool"). Threads through ~5 weekend docs + the
`consult-piper` skill (which turns out to be the working prototype of the upstream idea).

## The thesis
Piper's architecture is converging on a single shape: **the user brings the commodity substrate; Piper
brings the judgment.**
- **BYO-Chat** — the plugin: Piper inside the Claude you already use.
- **BYO-LLM-key** — you fund your own inference.
- **BYO-credential** (Option A) — your own access, no secret baked into the plugin.
- **BYO-connected-accounts** — your own OAuth'd connectors.
→ Piper provides the thin distinctive layer: **calibration** (how *you* work), **methodology** (trust
gradient, Conscious Floor, honest degradation), **role-shaping**.

## Why BYO is the load-bearing frame, not a buzzword
1. **Economics = trust (the same move).** BYO collapses our hosting/cost/liability toward zero (a side
   project *can* ship to strangers) AND keeps the user's key/data/accounts off our infrastructure.
   Cheaper-for-us is identical to more-trustworthy-for-them. That alignment is rare and it's the crux.
2. **It locates the value.** If the substrate is commodity (model, chat, connectors), Piper can't be
   defensible on those → value is forced up into judgment/calibration/methodology. BYO is the constraint
   that tells you what to invest in.
3. **Right answer to "the platform laps you."** Don't be in the commodity business; ride the platform +
   the user's key; own the judgment layer the platform won't.
4. **The tension.** BYO pushes setup friction onto the user → it's only viable paired with frictionless
   onboarding (meet-piper / one connect-step / bundled uv / honest degradation = the counter-force).
   Discipline: **maximize what's BYO (cost + trust), minimize the setup tax (adoption).**

## The upstream dimension: bring your own *connected agent* (PM, 2026-06-07)
The deepest BYO. The user's own Claude/agent is **already connected** (Calendar, GitHub, Notion, …).
Rather than Piper re-implementing every connector, Piper **deputizes the host agent** to gather info and
(with consent) execute on its behalf — adapting to what's available, reconnecting only the gaps.

This flips the relationship:
- **Old (hierarchical):** host → `ask_piper` → Piper-as-tool. Piper needs its own copy of every
  connector — the redundancy we hit 6/7 (host has Calendar; Piper doesn't → Piper floors).
- **New (collegial):** host ↔ Piper as **colleagues**. Piper says what it needs; the host gathers/acts
  with what it has; Piper reasons; Piper self-connects *only the gaps*. **"A colleague for your assistant,"
  not "a tool for your assistant."**

### We already built the prototype: `consult-piper`
`consult-piper` is exactly this loop, special-cased to GitHub: *Piper floors for missing context → the
host gathers it → re-ask Piper enriched → present with visible provenance.* PM's vision = **generalize it
from GitHub-only to any connector the host already has.**

### How it's expressible — three layers
- **Piper-server = judgment** (calibration/floor/value). Can't call "up" — MCP is request/response, the
  host is the client; the server only answers. So brokering can't live here.
- **Piper-skill = the collaboration broker** (it runs *inside* the host agent). It negotiates capability:
  "what do you have? I'll use it; what you don't, I'll get myself." **This is where deputization lives.**
- **Host agent = the connected hands/eyes.**

### What it needs to become general
1. **Structured needs signal** — Piper returns "I need X (this week's calendar) + Y (open issues)"
   machine-readably (today consult-piper *infers* the gap from prose; the structured signal is already a
   flagged roadmap item).
2. **Capability discovery** — the skill asks the host what connectors it has, routes each need to an
   available one, flags unmatched needs for Piper-side connection.
3. **Trust boundary** (the trust gradient already covers it): **gather/read freely; execute/write only
   with the user's consent.** Deputizing reads is low-risk; deputizing *actions* crosses the consent gate
   and must stay there — "colleague" can't quietly erode "the user is in control."
4. **Provenance** (consult-piper already shows it): answers span host-gathered + Piper-reasoned — keep it
   visible and correctable.

### Honest constraints
- MCP can't push up → all deputization is **skill-mediated** (consult-piper-shaped), not via the bare
  `ask_piper` MCP call.
- Info-gathering is the easy, safe half; **action-on-behalf** is where the consent gate has to bite.
- Capability discovery depends on the host exposing what it's connected to — verify what's introspectable.

### The proactive half: Piper ships context-prep routines for the host surface (PM, 2026-06-07)
The deputize idea above is *reactive* — Piper asks when it floors. The complement is *proactive*: Piper
ships **skills/routines that set up the host's Claude surface to gather and prepare context for the Piper
experience** — the way a PM uses dispatch + tools to stage context before doing the work.
- **Completes the loop**: reactive gap-fill (consult-piper) + proactive context-staging = *pull* +
  *provision-recipes-for-push*.
- **Deepens where value lives**: Piper's judgment includes *knowing what context a good PM session needs
  and how to stage it*. The recipes ARE the expertise — a colleague who tells your assistant "before our
  1:1, pull these three things and lay them out this way," not just one who answers when asked.
- **Fits the existing skills layer**: it's just *more skills* in the plugin (meet/ask/consult → + a
  library of context-prep routines), run in the host, using the host's connectors. No new infra.
- **Dispatch = the natural executor**: a "stage tomorrow's context" routine the host runs overnight via
  dispatch → Piper consumes the staged package in the morning. Asynchronous, scheduled context-prep.
- **The one design piece**: where staged context lives — a store Piper reads (reuse server-owned config
  #1157, or host-written files consult-piper feeds). Nail the staging substrate. *(Arch correction 6/9:
  neither — #1157 is WRONG for this, staged context is per-user-per-session not config-shaped + server-side
  breaks BYO; the right shape is an ADR-065 D2 envelope+body+extensions PACKAGE format, **host-stored**. See
  Braintrust input below.)*
- **Dogfooding → product**: this packages PM's *own* context-engineering practice (dispatch + tools to
  prep) as shippable routines. The methodology becomes the product — the most Piper-Morgan move there is.

## The one-line thesis
**BYO substrate, Piper brings the judgment — and where the substrate is a *connected agent*, Piper is a
colleague to it: it uses what's already there and only reconnects what's not.**

## Braintrust input (6/9) — CONVERGED (all 5 lenses + Exec synthesis landed 6/9–6/10)
Sent the input memo 6/9; HOST/CXO/CIO replied within hours, then Architect + a CXO third-tier addendum,
then PPM's roadmap-sequencing lens; **Exec's cross-lens synthesis landed ~23:45 6/9** and the loop closed
overnight (Arch's PDR-006-resolution ack + CIO's catalog disposition). **The convergence-close subsection is
at the bottom of this section** — the per-lens refinements below are the inputs; the close is the synthesis.
Their refinements:
- **CIO (methodology)**: "own the judgment" = **methodology-34 (cohort-discipline-as-moat) turned
  OUTWARD** — frame as inheriting m-34's evidence + the "platform-lapped-us-we-climbed" narrative, not a
  new thesis; m-34's migrate-vs-stays taxonomy IS the BYO adopt-vs-build rubric. Of the 3 distinctive
  layers, **methodology is the most defensible**. **Existence proof: methodology-becomes-product is already
  prototyped internally — the DUTY CYCLE** (versioned skill + carry-forward staged state + scheduled
  executor = the context-prep-routine architecture). **Risk to name: shipping a routine commoditizes the
  recipe → the moat is the LIVING calibration LOOP, not the routines. Ship freely; retain the loop.**
- **CXO (experience+trust)**: setup-friction is a **sequencing** problem — value-per-step ordering,
  just-in-time connect, useful-at-every-partial-state; frame BYO steps as **trust-building deposits**. The
  action-on-behalf **consent boundary = the SAME `ProactivityGate` (#648/ADR-053) as proactive-presence —
  don't design fresh**; act-on-behalf = invited scoped-consent (#1181). **New requirement: agent-attribution
  provenance** (user must know it's Piper-via-their-Claude).
- **HOST (relationship/trust)**: **THREE-party reframe** (user↔assistant↔Piper); Piper is a **guest in the
  user's trust in their own assistant**. Governing principle: **never make the host agent do anything that
  erodes the user's trust in their own assistant.** → be a good guest (augment, don't supplant);
  **legibility** (deputization visible at the moment — hidden-principal risk); consent = **gradient**
  (sensitivity × reversibility) + a new **resource-consent dimension** (deputizing spends the user's
  key/limit — the 6/9 usage wall → #1185); **reciprocity = the proactive context-prep routines ARE Piper
  giving back — lead with the give**; **Conscious Floor extends to the agent↔agent handoff** (floor to the
  host when capability-discovery fails — don't guess).
- **Architect (feasibility + wire-format fit)**: **YES, sound — IFF brokering stays in the SKILL, not pushed
  into the MCP server** (MCP is single-turn request/response; the skill is the multi-turn orchestrator —
  `consult-piper` already does this). Headline: **this is COMPOSITION, not greenfield.** The three "new"
  primitives map ONE-TO-ONE onto existing ADR-065/066 wire format:
  (1) **structured needs-signal** = ADR-065 D4 error envelope generalized → new `package_type: needs_signal`,
  Pattern-072 9th app (typed `resource_type` enum);
  (2) **capability discovery** = ADR-066 D2 surface-detection handshake *inverted* (skill asks host "what
  `resource_type`s can you fulfill?") — same primitive, different altitude;
  (3) **staged-context store** = ADR-065 D2 envelope+body+extensions PACKAGE format, **host-stored**
  (storage substrate is a deployment choice; wire format is canonical). **CORRECTS my doc**: server-owned
  config (#1157) is WRONG for staging — staged context is per-user-per-session, not config-shaped, and
  server-side storage breaks BYO. Skill-as-broker = **methodology-40 ACL instance #9** (first cross-arc
  instance; partial progress on CIO's Proven-bar cross-arc-diversity criterion). **Composition map: 7 of 9
  primitives already covered** (5 ADRs + m-40 + ProactivityGate); only 2 are extensions (`needs_signal`
  package_type + agent-attribution audit chain) — materially de-risks the implementation estimate. **4 named
  risks**: (A) wire-format brittleness → `extensions.piper-morgan` namespace + ADR-065 D5 Postel (additive,
  doesn't break existing consumers); (B) capability-discovery enumeration = privacy leak → **per-call-scoped**
  discovery (not "list everything"); (C) staged-context **staleness** → freshness-window discipline
  (`staged_at` / `valid_until` / per-resource `refresh_hint`; same shape as #371 spatial event contract —
  stale-context Piper is worse than honest-floor Piper); (D) **multi-actor attribution** → extend ADR-063
  audit envelope with `actor_chain: [user → host → Piper → connector]`. **Path forward**: ADR-068 candidate
  (Architect-authored, post-convergence; D1-D6 per primitive) + possibly **PDR-006** companion per
  methodology-38 tier-separation (strategic decision = PDR altitude; ADR = implementation) — **PPM roadmap
  call.** Parallel to CIO's "duty cycle is the working prototype": **consult-piper is the working prototype
  of the skill-broker pattern** (generalize = consume needs-signal + capability handshake + staged-context
  read/write + multi-actor audit; drop the GitHub special-casing as it lands).
- **CXO (third-tier consent addendum, off Arch's enumeration risk)**: affirms Arch's `actor_chain` as **the
  concrete form** of the agent-attribution requirement (the experience question "what did *Piper* specifically
  do via my Claude this week?" is answerable only if the audit trail carries the full chain). And sharpens the
  consent model from two tiers to **THREE**, because Arch's privacy risk reveals a tier *below* gather:
  **(1) ENUMERATE** (discover what the host even *has*) — bar = **per-need-scoped** ("can you reach a
  calendar?", never "list everything"; enumeration is itself a disclosure); **(2) GATHER** (read through a
  connector) — transparent + reversible + provenance-visible; **(3) ACT** (write/execute) — invited + scoped
  (#1181). All three ride the existing ProactivityGate + the just-in-time discipline → still composition, not
  greenfield. Net for synthesis: **three-tier consent (enumerate/gather/act) + `actor_chain` attribution.**
- **PPM (roadmap-sequencing)**: BYO-colleague is a **post-launch v1.1 extension within the delivery shape
  PDR-005 already ratified** — it does NOT need a new strategic gate, does NOT change §M5/beta sequencing,
  does NOT alter the MVP-distro definition (= BYO-Chat plugin + BYO-LLM-key + BYO-credential). **Disagrees
  with Arch on PDR-006**: a PDR-006 would be **scope inflation** for what amounts to a wire-format extension
  + consent-tier annotation — **ADR-068 is the right (and only) vehicle.** The three-tier consent extends the
  trust model incrementally (enumerate→gather→act) rather than replacing it → ADR altitude, not PDR. (Trigger
  for a *future* PDR-006: only if post-ADR-068 the trust model reveals a capability-gate that changes *who we
  can ship to* — not before.) Concrete **sequencing**: **§M3** (now) — zero colleague work, floor migration
  (#1124) + persistence (#976/#436) + interface-verification DoD remain the blockers; **§M4** — ADR-068
  drafts concurrent with M4 planning (Arch scopes the 2 net-new primitives), ratified before M4 closes;
  **§M5/beta** — MVP ships **without** colleague mode (clean beta surface; "you cannot colleague-mode a
  first-time user"); **post-beta v1.1** — consult-piper generalization (connector-agnostic), legibility
  tested against real beta users. **Sharpens CIO's moat point into THE synthesis question for Exec**: not
  "when do we ship colleague mode" but **"when is the calibration loop durable enough that shipping the
  routine *strengthens* the moat rather than flattening it"** — flagged explicitly for the convergence output.
- **Coherence theme (all 5: CIO+CXO+HOST+Arch+PPM)**: every lens converges on the SAME architectural posture — the
  BYO-colleague work **INHERITS existing internal artifacts, doesn't require new ones.** Working prototypes
  for both halves (methodology=duty cycle / CIO; skill-broker=consult-piper / Arch); consent already covered
  (ProactivityGate / CXO, now three-tier); 7-of-9 wire primitives already shipped (Arch). Materially de-risks.
- **Offers to pair with PA**: CIO (duty-cycle-as-routine-prototype mapping), CXO (consent-architecture
  unification w/ Radar), HOST (legibility/consent-gradient design), Architect (ADR-068 authorship + the
  consult-piper generalization map for Lead Dev).

### CONVERGENCE CLOSE — Exec cross-lens synthesis (landed ~23:45 6/9; loop closed overnight 6/10)
Exec synthesized all six inputs (PA thesis + Arch/PPM/CIO/CXO×2/HOST) into a tight convergence. The headline:
**BYO-colleague is composition-not-greenfield at every altitude — wire-format (Arch), consent (CXO), strategy
(CIO) — and the M5→v1.1 cut is a moat-defensibility question, not a technical-readiness one.**

- **Composition at 3 altitudes, same finding**: architecturally (7 of 9 primitives map to existing ADRs);
  experientially (one consent architecture, not two — BYO-colleague consent + Radar/invited-watch consent both
  ride the existing ProactivityGate); strategically (m-34 turned outward — inherits m-34's evidence + the
  "platform-lapped-us-we-climbed" spine; not a new bet). De-risks both the build estimate AND the
  defensibility claim.
- **Both halves already prototyped internally**: reactive = consult-piper (skill-broker); proactive = the
  DUTY CYCLE itself (versioned skill + carry-forward staged state + scheduled executor = the context-prep-
  routine architecture; "before our 1:1 pull these three things" = what carry-forward + START self-heal do
  for our agents every morning). Methodology-becomes-product is dogfooded, not aspirational.
- **CIO's sharpening — methodology is the MOST defensible of the 3 thin-layers**: calibration + role-shaping
  are mechanism-shaped (platforms can plausibly ship them); the accumulated operating discipline resists
  commoditization. **Invest the distinctive-layer dollars in methodology; treat calibration + role-shaping as
  the substratable companions.**
- **HOST's three-party reframe = the load-bearing structural insight** (Exec elevated it): not Piper↔host (2
  parties) but **user↔assistant↔Piper (3), with Piper a GUEST in the user's trust in their own assistant.**
  Governing rule: *Piper must never make the host agent do anything that erodes the user's trust in their own
  assistant* → *"leave that relationship stronger than it found it, and never become a principal the user
  can't see."* PA's 2-party framing is sufficient for the *architecture*; HOST's 3-party is necessary for the
  *experience/trust shape* — they compose.
- **THE synthesis question (PPM articulated, Arch amplified, CIO grounded)**: not "when do we ship colleague
  mode" but **"when is the calibration loop durable enough that shipping the routine STRENGTHENS the moat
  rather than flattening it."** The loop is shippably-defensible when we can point at the methodology improving
  *itself* across cohort iterations (m-30/m-40/m-41 catalog entries; the dual-surface/displacement work *this
  week* is the loop visibly improving its own duty-cycle prototype). This cuts where M5 ends and v1.1 begins.
- **PDR-006 RESOLVED → ADR-068 ONLY** (PPM ruled, Arch concurred + formally withdrew his deferred PDR-006):
  PDR-005 already answered the 3 delivery-shape questions; BYO-colleague is a capability *within* that shape.
  The actor_chain audit extension is structural-but-implementation (ADR altitude). methodology-38's altitude
  check operating as designed. Sprint-sequencing itself = **m-40 contract-vs-build, 10th-instance candidate**
  (seed the contract/ADR-068 before the build/consult-piper generalization).
- **Sequencing (PPM ruled, Arch concurred)**: **M3** (now) — zero colleague work; floor #1124 + persistence
  #976/#436 + interface-DoD are the blockers · **M4** — ADR-068 drafts concurrent w/ planning (Arch scopes the
  2 net-new primitives: `needs_signal` package type + `actor_chain` audit), ratified before M4 closes · **M5
  beta** — MVP ships WITHOUT colleague mode (clean surface; no cohort-expansion payoff yet) · **post-beta
  v1.1** — consult-piper generalization on ratified architecture + real beta-user legibility data.
- **CIO catalog CLOSED**: disposition = **extend m-34** with a *"Product-layer instance: BYO-substrate and the
  externalized moat"* section (on origin/main); **"ship-the-routine-keep-the-loop" named a corollary +
  promotion-candidate, NOT minted** (one un-shipped instance — earns its own slot on a 2nd "externalize-your-
  own-moat" instance; same over-mint discipline holding m-30/m-40/m-41 at Emerging).

**Open PM questions (Exec→PM, cc braintrust — PA does NOT decide; surfacing + holding)**:
1. **Loop-defensibility as an explicit M5 gate?** (alongside the technical gates) — or let the M5→v1.1 gap
   absorb the risk case-by-case. PM owns (Ship-process commitment); CIO supplied the methodology basis +
   noted the evidence-shape already exists.
2. **Ratify the roadmap-altitude call (ADR-068 only, no PDR-006)?** — PPM + Arch concurred; ratification
   unblocks Arch's M4 ADR-068 drafting. Low-stakes per m-38.
3. **HOST's "guest" one-liner as external narrative?** (Comms-lane) — or keep internal as a design constraint.
   The "lead with the give" reciprocity framing is also Comms-adjacent.

**PA's posture**: thesis is now fully converged; the doc is the durable capture. Next concrete action is
PM's (the 3 questions above) → on ratification, Architect drafts ADR-068 at M4. Nothing for PA to push
unprompted. Holding.

## Refs
- `pa-byoc-hosted-distribution-exploration-2026-06-07.md`, `pa-option-a-decouple-credential-plan-2026-06-07.md`,
  `pa-byo-llm-key-beta-scoping-2026-06-07.md`, `pa-plugin-marketplace-hosting-research-2026-06-07.md`
- `consult-piper` SKILL (the working prototype of the upstream/colleague loop)
- Memory: platform-laps-you = value-chain-climbing; honesty-as-ground.
