# Skunkworks BYOC → v17 §M5/PDR-005 roadmap bridge

**Author**: Piper Alpha (PA)
**Date**: 2026-05-31
**Purpose**: bring the skunkworks learnings + PM's thin-full-stack-PoC proposal "to a point" against the
current roadmap, per PM 5/31. **This is pointed input for PM's roadmap/strategy catch-up — it does NOT
make architecture decisions** (those stay with Architect/PPM via PDR-005 + the BYOC ADRs).
**Status**: step-2 of the 5/31 path (1 = fan-out for ratification; 2 = this bridge; 3 = PoC scope-sketch, gated).

---

## 1. What skunkworks has established (two test events)

- **Sub-pass 4.a (5/19, Claude Code CLI)** — local plugin install + skill-invoke via `--plugin-dir`
  **gated PASSED**. Proves BYOC as a **zero-server / zero-cloud capability-transfer vehicle**.
- **Cowork-runtime test (5/31)** — the same `/cold-start-interview` skill run end-to-end in Claude
  Cowork as a **no-software value-floor benchmark**. Resolved the shared-profile path, validated
  patch-vs-redo, and surfaced the runtime/filesystem-mismatch finding.
- **Standing relationship to canonical work**: the PoC is a **predecessor-pattern study, not a
  competing track** with PDR-005 (skunkworks README, 5/20). That framing is the load-bearing guardrail
  for everything below.

## 2. What it has PROVEN vs. EXPOSED

- **Proven**: the *intake* — a strong, serial, anti-sycophantic interview that captures things generic
  Claude can't infer (role lenses, trust gradient, burst/quiet capacity-coupling), and the
  onboarding-as-demo quality (rules enacted, not described) that reads as "a colleague who knows how
  you work." The **latitude** to flag/propose/disagree is the hard-to-copy moat.
- **Exposed (the ceiling)**: value is only *gestured at*, not *delivered*, because **nothing downstream
  reads the profile yet**. PM's human read agrees: "a small piece of what the experience could be —
  makes me want to do more." The intake is proven; the **payoff loop is not built**.
- **Exposed (fragility)**: the skill assumes the shell is the host; false in non-Code runtimes
  (Cowork). Calibrated severity (PM): an **expected** multi-context-testing finding, not a crisis.
  Fix = host-verification-as-step-one (no-silent-failures applied to the skill itself).

## 3. PM's proposed next experiment — the thin plugin PoC

**Packaging model (PM 6/1 — corrects earlier framing).** The canonical Anthropic package is **the
plugin itself** (hosted, or installable from a zip) — **NOT an MCPB bundle, NOT a hosted MCP**. A plugin
*contains* config files + a CLAUDE.md template for its own use + one or more Skill files + the MCP server
(+ bundled `uv` if the MCP is Python, or write it in Node). The reference is the **Anthropic legal
plugin** (studied at OpenLaws to reverse-engineer the conventions). **Marketplace** is the wrapper level
above plugin — out of scope here.

**The thin plugin PoC** is one such plugin, pointed at Piper Morgan:
- **Plugin wrapper + core files** (incl. CLAUDE.md template)
- **Onboarding skill** (cold-start, already built) **+ one Piper-specific skill** (kept to one for a
  genuinely thin first pass; second skill sequenced after)
- **Minimal MCP server** wrapping one real Piper API call
- plus the work to **make that API call reachable from the MCP**.

**The decided first rung (PM 6/2 — `/intent`-first).** Gall's-Law smallest-working-piece:
1. **Value-prop + API call**: Piper's conscious-floor engine = **`POST /api/v1/intent`** (`{message,
   session_id}`; **auth-optional** → zero token plumbing for a first pass). The front end's core call.
2. **Thin MCP** wrapping that one call → install locally → test conversationally.
3. **Skill on top** = the B+C *"ask Piper to read your situation and propose your next step, in your
   voice"* (reads the captured profile = exercises the payoff loop).
4. Then iterate; **`GET /api/v1/insights`** (trust-graduated proactivity; read-path, needs auth) is the
   natural **rung 2**.
- *Scope caveat (Lead/Arch)*: `/intent` is the full engine — target query/propose-type intents or
  confirm propose-only; settle the `/insights` auth path before rung 2.

**Why it's the right next step, not scope-creep**: it directly attacks the §2 ceiling — it's the first
rung that **builds the payoff loop** (a downstream skill + real API reach reading the profile) instead
of re-proving the intake.

## 4. How it maps onto v17 (already-roadmapped) — with a packaging correction for PDR-005

- **Packaging correction owed to v17 §M5 / PDR-005.** The roadmap's BYOC build sequence is written as
  "MCP server → **MCPB packaging** → Project template → MCP Apps," which implies MCPB is the packaging
  target. Per PM 6/1 the **plugin is the canonical unit** (MCP server is a component inside it). PPM/
  Architect should correct the §M5 / PDR-005 build-sequence language to plugin-as-canonical. **This
  PoC's build order is the corrected one** (identify value-prop API call → thin MCP → test → skill →
  test → iterate).
- **v17 §M5 / PDR-005 v0.5** is the canonical BYOC vehicle; **Architect Q6 (context-package format) +
  Q7 (packaging-layer abstraction)** are the companion ADRs. The thin-PoC's natural **deliverable is
  evidence + sharpened questions for PDR-005 + Q6/Q7** — e.g. "here's what minimal MCP-against-real-API
  actually required," "here's where the persona-template parameterization held or broke."
- **Differentiator stack**: the moat finding (latitude/colleague-stance) is concrete evidence for
  Pillar-1/2 (Context Methodology + Conscious Floor) and the cross-client identity-coherence framework
  CXO absorbed into PDR-005.

## 5. The coordination guardrail (non-negotiable)

Keep the thin-PoC a **predecessor-study that FEEDS the canonical work**, not a parallel architecture
track that front-runs PDR-005/Architect. The forcing-function value comes from **informing** the
canonical decisions ahead of time and **de-risking** them — not from making them in skunkworks. This
is how we get speed without getting ahead of strategy (the tension PM named).

## 6. The ask + open questions for leadership

**Ask**: ratify the *idea* of a single-purpose MVP/PoC plugin with all layers present but **not
overbuilt** — as a forcing function, explicitly feeding PDR-005 + Q6/Q7.

**Open questions** (for the roadmap/strategy catch-up, not for skunkworks to answer):
1. Which slice of the **real PM API** is the right minimal target? (Lead Dev + Architect)
2. Which 1–2 **PM skills** are the highest-value "down payment"? (PPM + CXO)
3. Does the thin-PoC's evidence-deliverable change the **PDR-005 v0.5 → v1.0** path or the Q6/Q7
   sequencing? (Architect + PPM)
4. Where does this sit against current MVP/M2g-closure + Phase 2 build priorities? (Exec + PM)

---

*Pointed input only. Sequencing per PM 5/31: ratify the idea (1) before scoping the build (3).*
