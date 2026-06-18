# ADR-072: Skill-Routing Architecture — Fluid Model with Defense-in-Depth

**Status**: ACCEPTED (v0.2) — D1–D4 Arch-ratified in-lane; **D5 ratified 2026-06-17 with CXO + HOST trust-lens folded** (both aligned: gate Piper-initiated, never user-reaching-for-own; + HOST's consequential-action carve-out + transparency-when-gated)
**Date**: 2026-06-17
**Author**: Chief Architect
**Deciders**: Architect (author), PM (direction-ratified the "fluid model with defense-in-depth" framing 2026-06-15), PA (brief + topology correction), Lead Dev (implementation), CXO + HOST (D5 trust-lens, folded + ratified 2026-06-17)
**Supersedes / superseded by**: none
**Related**: ADR-059 (PIPER.md capability accuracy), ADR-066 D7 (Configuration Ownership / server-owned state), ADR-070 (MCP-Consumer Connector Architecture), ADR-071 (User-Auth Anchoring / Trust Gradient anchor), #1106 (MANIFEST derive mechanism), methodology-40 (layer-then-migrate), methodology-41 (mechanism-displaces-unreferenced-discipline), Pattern-073 (documentation-asserted-behavior drift)
**Unblocks**: Wave P plugin-path skills (`connect-piper` + `piper`); #1245 (PIPER-SKILL-MERGE)
**Grounding substrate**: `dev/active/adr-072-grounding-findings-2026-06-17.md`

---

## Context

Ten PM skills are live on `origin/main` (Wave 1: `draft-issue`, `close-issue`, `draft-spec`, `synthesize-feedback`, `update-piper`; Wave 2: `propose-feature`, `compost-review`, `trust-check`, `stakeholder-update`, `sprint-plan`). They are prompt-layer `SKILL.md` files. They work on the **native path** (Claude Desktop/Code with `.claude/skills/` loaded — Claude executes the SKILL.md procedure locally). On the **plugin path** (a PM connected to Piper via the MCP plugin), **they are invisible** — the plugin has no knowledge they exist, and no mechanism to execute their procedures.

Two sub-gaps (decisions.log 2026-06-15 ~16:15 PT):

- **Discovery** — Piper doesn't know which skills exist on the plugin path. Listing them in `PIPER.md` would violate ADR-059 (every capability there must be server-side-implemented, or the LLM offers a broken experience). A separate manifest is needed.
- **Invocation** — even knowing a skill exists, there is no mechanism to execute its procedure on the plugin path. Native path = the SKILL.md *is* the procedure; plugin path is an open design question (#1245 territory).

**PM's direction (2026-06-15, ratified)**: a **fluid model with defense-in-depth**. No single routing mechanism is authoritative; multiple independent layers, each catching what the others miss. No layer has to be perfect; together they make skill invocation robust across both paths — and the floor (normal prose response) means a miss is never a broken experience.

The plugin currently exposes **5 MCP tools** (corrected from the brief's conceptual "3"; PA addendum 2026-06-16): `ask_piper(message)`, `get_profile()`, `save_profile(content)`, `get_company_profile()`, `save_company_profile(content)`. Notably `get_profile`'s description already instructs Claude to call it "from any skill that wants the user's calibration" — **Layer 1 is already partially real.**

This ADR was authored evidence-first: the design below is grounded in the actual `PIPER.md` v3.0 format, the `SKILL.md` format (`sprint-plan` as representative), the native `SKILLS.md` index, and `services/intent_service/pre_classifier.py` (1934 lines). See the grounding substrate for the per-source findings.

---

## The defense-in-depth model (the architecture the 5 decisions sit within)

| Layer | Where | Mechanism | Catches | Authority |
|---|---|---|---|---|
| **1 — Tool / capability descriptions** | Plugin manifest + `PIPER.md`/`PIPER-SKILLS.md` | Descriptions embed skill trigger-phrases; Claude picks before the server is hit | Obvious skill-shaped queries | **Hint-only** |
| **2 — Intent pre-classification** | Server `pre_classifier.py` | Skill-detection pass tags intent with `skill_hint` (patterns **derived** from SKILL.md frontmatter) | Skill-shaped queries after parsing | **Authoritative on plugin path** |
| **3 — Procedure injection** | Server context-assembly | On `skill_hint`, inject the SKILL.md procedure into the response context | Makes imprecise routing produce structured output anyway | Fallback |
| **4 — Native-path execution** | Claude-side | Claude executes SKILL.md locally; no server round-trip | Native-path users entirely; highest fidelity | **Authoritative when present (native)** |
| **Floor** | Server | Normal intent handling, prose response | Everything unmatched | Never a broken experience |

The layers are **additive, not sequential gates** (PM's "fluid" property): each improves routing without being required. Layer 1 gets the obvious cases; Layer 2 catches the rest on the plugin path; Layer 3 rescues imprecise routing; Layer 4 owns the native path; the floor catches everything else.

---

## ⭐ The unifying mechanism: derive routing metadata from `SKILL.md` frontmatter (don't hand-maintain it)

**The load-bearing architectural decision of this ADR.** The `SKILL.md` frontmatter is already a single source of truth for routing: `sprint-plan`'s `description:` embeds its **trigger phrases** inline ("let's plan the sprint", "help me scope [sprint]", "which issues should we tackle next") plus `scope:` and (in changelog) deployment surface ("Native + Plugin"). That one source should **feed three layers via a derive mechanism**, not three hand-maintained copies:

1. the **skills manifest** (D2 / Layer 1),
2. the **Layer-2 `skill_hint` detection patterns** (D1), and
3. optionally the **Layer-1 tool/`PIPER.md` descriptions**.

**Why derive, not hand-maintain** — three independent pieces of evidence:
- The native `.claude/skills/SKILLS.md` index is **hand-maintained and already ~1 month stale** ("Last Updated 2026-05-15" against 10 live skills) — a live **Pattern-073** (documentation-asserted-behavior drift) instance proving hand-kept skill indices rot.
- `pre_classifier.py` is a 1934-line wall of ~30 hand-ordered `*_PATTERNS` lists with fragile "MUST be checked BEFORE X" caveats; hand-duplicating each skill's trigger phrases into it would compound that fragility — and those phrases already live in the SKILL.md frontmatter.
- **#1106 is the precedent**: mailbox MANIFESTs are *derived* from message frontmatter (sole-writer + idempotent regen) precisely so the index cannot drift from the directory.

This is **methodology-41** (mechanism-displaces-unreferenced-discipline) applied to skill-routing: the manifest can't go stale because it's generated, not maintained. The derived registry is **server-owned state per ADR-066 D7**.

---

## Decision

### D1 — Authoritative routing layer
**Layer 4 (native SKILL.md execution) is authoritative when present** (native path, highest fidelity). **Layer 2 (server pre-classifier `skill_hint`) is authoritative on the plugin path.** Layer 3 (procedure injection) is the fallback that makes imprecise routing still produce good output. Layer 1 (descriptions) is **hint-only**. When multiple layers fire, the **highest-confidence layer that fired wins**; layers are additive, never sequential gates; the floor catches everything unmatched. *(Layer 2 is a natural extension of the existing pre-classifier — it already tags 30 intent classes via ordered pattern lists, including recent additions PROVENANCE / TRUST / INSIGHT_PULL; skill-detection is one more class, with patterns **derived** per the unifying mechanism.)*

### D2 — Skills manifest location
**`PIPER-SKILLS.md`, alongside `PIPER.md`, governed by the ADR-059 discipline — and DERIVED from `SKILL.md` frontmatter, not hand-maintained.** `PIPER.md` is exactly a capability manifest under the ADR-059 "every capability MUST have a working implementation" rule, with a trigger-phrase→behavior "Usage Examples" pattern; the skills manifest extends it 1:1, the discipline becoming **"a skill listed here MUST be server-side-invocable on the plugin path."** Because the manifest is *generated* (a skill enters only when its plugin-path invocation exists), the ADR-059 guarantee holds by construction — the manifest cannot advertise an unrunnable skill. The plugin-path delivery option is to expose the derived manifest as an **MCP resource** (server injects it on connect). *(Do not hand-maintain it like the stale `SKILLS.md`.)*

### D3 — Plugin tool topology
**`ask_piper` (server routes within — Option B, the default) + `run_skill(name)` meta-tool escape hatch (Option A) — NOT per-skill tools.** Most PMs say "help me plan my sprint," not "run the sprint_plan skill," so `ask_piper` + server-side routing is the right default; `run_skill(name)` is the advanced explicit-invocation path. A single meta-tool keeps the namespace at 6 tools (vs. 16+ if every skill were its own tool — namespace explosion that degrades LLM tool selection). **No existing tool is renamed or removed** (methodology-40 layer-then-migrate); `ask_piper` *extends* with routing, the profile tools stay as I/O specialists. `run_skill`'s valid `name` set is the derived registry (D2) → discoverable and drift-free.

### D4 — Skill procedure invocation on the plugin path
**A static registry DERIVED from `SKILL.md` (frontmatter + body) at server start; inject the procedure into response context when a `skill_hint` fires (Layer 3); server-owned per ADR-066 D7; hot-reload.** `SKILL.md` is a self-contained prompt-layer procedure; on the plugin path the server loads + injects it (it doesn't "execute" it — the LLM does, from the injected procedure). Dynamic per-invocation file reads would add startup-latency + race risk; compiling the registry at server start gives O(1) lookup and immutable runtime state. `PIPER.md` already uses cached hot-reload (changes take effect without restart) — the same mechanism keeps the skill registry fresh. This is #1245's build target.

### D5 — Trust Gradient × routing *(RATIFIED v0.2 — CXO + HOST trust-lens folded 2026-06-17)*
**The Trust Gradient is a separate permission layer ABOVE Layers 1–4: the Gradient decides *should-we* (is the invocation permitted for this user/tier); routing decides *which-one*.** HOST confirmed the separation is **load-bearing, not just clean** — conflating them puts trust-property verification *inside* routing logic, making routing decisions trust-contract decisions (no longer testable per-layer or auditable as a unit). Keep the separation.

**The axis (CXO):** the Gradient governs **Piper's forwardness / Piper taking action** — *never* the user's access to their own content. Discriminator: **Piper-initiated** (proactive surfacing, autonomous action) = trust-gate-eligible; **user-reaching-for-their-own** (user-invoked skill execution, viewing own data) = **never gated**. Invoking a skill the user explicitly asked for is the user reaching for a capability — not gated. (The gradient is Gate B / `ProactivityGate`, ADR-053 — built for "may Piper show up uninvited, how forward"; D5 keeps it pointed there, not at user access.)

**The reactive line, sharpened (HOST):** reactive (user-asked) invocation is tier-independent for **information skills** (no side effects — `propose-feature` / `trust-check` / `compost-review`: the explicit ask *is* consent). But **consequential-action skills** — those that modify state, send external messages, spend credits, or take hard-to-reverse actions — are **tier-gated even when reactive**: "did the PM ask?" is necessary but not sufficient; the tier tells whether the account authorized that *class of action* for Piper. **The discriminator is side-effects, not just who-initiated.** Wave P skills are information-only today, so D5 names the consequential-action carve-out *now*, before the first such skill ships (m-36 — structure before the violation).

**Substantiability / fail-closed (HOST confirmed):** never surface a proactive proposal whose trust-gradient permission isn't substantiable — if the Gradient can't confirm permission, **don't surface** (the cost of an unwanted proactive proposal exceeds the cost of a withheld one). Same fail-closed shape as `PROTECTED_JOB_NAMES` MCP-caller gating.

**Transparency when gated (HOST):** when the Gradient gates a proactive proposal, the routing layer **surfaces that the gate exists** (via `trust-check` or a minimal transparency signal) — *not silence*. Silent non-action is itself a trust gap even when the action was correctly withheld; the user should understand why Piper did or didn't offer something. (Composes with HOST's People-entity trust-map legibility work.)

The per-user tier lookup is possible because of **ADR-071** (the user-auth anchor). **RATIFIED** — CXO + HOST both confirmed the separation honors the trust contract (CXO: "ratify if it gates proactive, not user-invoked execution" — it does); the consequential-action carve-out + transparency signal are folded.

---

## Consequences

**Positive**
- Skills become routable across both paths without per-skill tool sprawl (D3) or a hand-maintained, rot-prone index (the derive mechanism).
- The ADR-059 guarantee extends to skills *by construction* (D2) — no new class of "Piper offers a skill it can't run."
- Layer 2 is an incremental extension of the existing pre-classifier, not a new subsystem (D1).
- Wave P (`connect-piper` + `piper`) and #1245 are unblocked with a concrete build target (D4).

**Costs / risks**
- The derive mechanism (the registry generator + the SKILL.md-frontmatter → pre-classifier-pattern compilation) is net-new infrastructure to build (#1245). It is the right cost — it replaces three drift surfaces with one.
- Layer-2 pattern derivation must handle trigger-phrase ambiguity (two skills with overlapping triggers) — needs a confidence/ordering rule, the same class of concern the existing pre-classifier already manages with its "checked BEFORE" ordering.
- D5 is unresolved pending trust-lens review; proactive-surfacing behavior should not ship until D5 ratifies.

**Neutral / follow-ups**
- The stale native `SKILLS.md` should *also* become derived (kill the rot at its source) — a Pattern-073 follow-up, in or adjacent to #1245.
- `test_create_tables_from_scratch`-class staleness (asserting hand-kept indices) will surface as the derive mechanism lands.

---

## Composition with existing decisions
- **ADR-059** — the manifest discipline D2 extends; the derive mechanism makes it structural.
- **ADR-066 D7** — the derived registry is server-owned state (config never crosses host↔server as durable state).
- **ADR-070** — plugin tool topology (D3) composes with the MCP-consumer connector substrate; `run_skill` is a Piper-as-host tool, distinct from the downstream-connector boundary.
- **ADR-071** — the Trust Gradient tier lookup (D5) requires the per-user auth anchor.
- **#1106** — the MANIFEST-derive precedent the unifying mechanism generalizes.
- **methodology-40** — no existing tool renamed/removed (D3); layer-then-migrate.
- **methodology-41 / Pattern-073** — the derive mechanism is the mechanism-displaces-vigilance cure; the stale `SKILLS.md` is the live drift instance it cures.

---

## Open questions (v0.1 defers)
1. ~~**D5 trust-lens** — circulate to CXO + HOST~~ — **DONE 2026-06-17**: both folded into D5 v0.2 (consequential-action carve-out + transparency-when-gated); D5 ratified. Proactive-surfacing rules are now set.
2. **Derive-registry scope** — server-side registry is canonical; a generated `PIPER-SKILLS.md` is a committed *artifact* of it (regenerated by script, never hand-edited) — confirm at build.
3. **Trigger-phrase collision rule** — the confidence/ordering discipline for overlapping skill triggers in Layer 2.
4. **#1245 scope confirmation** — confirm the D2/D4 derive mechanism is precisely what #1245 builds.

## Status / Evolution
v0.2 ACCEPTED (2026-06-17) — all 5 decisions ratified. D1–D4 Arch-ratified in-lane; **D5 ratified** with CXO + HOST trust-lens folded (consequential-action carve-out + transparency-when-gated). Authored v0.1 + ratified same day per PM's escalation (grounding-first pass made the fast turnaround evidence-based). Lead Dev implements #1245 against this; further refinements fold into v0.3.
