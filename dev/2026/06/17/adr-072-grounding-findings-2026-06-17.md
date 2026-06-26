# ADR-072 (Skill-Routing) — grounding-audit findings

**Author**: Architect (new, DinP / Opus 4.8) · **Date**: 2026-06-17 (autonomous fire ~13:00 PT)
**Purpose**: the evidence base for ADR-072 v0.1, per the predecessor's grounding-pass-first deferral trigger ("read `PIPER.md` + existing `SKILL.md` formats BEFORE authoring D2 manifest + D3 topology — don't draft from speculation," per Lead's 6/16 #1238 caller-list catch). This doc is the substrate; v0.1 is authored **from** it, not from the framing-leans alone.

**Sources read** (grounded, not relayed): PA original brief (`memo-pa-to-arch-cc-pm-lead-skill-routing-adr-brief-2026-06-15.md`) + PA topology addendum (`...adr072-addendum-plugin-topology-correction-2026-06-16.md`) + my framing-leans memo (`memo-arch-to-pa-cc-pm-lead-adr-072-ack-timeline-...-2026-06-16.md`) + `config/PIPER.md` (v3.0, the ADR-059 capability manifest) + `.claude/skills/sprint-plan/SKILL.md` (representative Wave-2 PM skill) + `.claude/skills/SKILLS.md` (native skill index) + `services/intent_service/pre_classifier.py` (1934 lines; structure) + `decisions.log` (ADR-059 plugin-path discipline; 5-tool topology correction).

---

## ⭐ The unifying finding (NEW — strengthens the framing): derive, don't hand-maintain

**The SKILL.md frontmatter is a single source of truth that should feed three of the routing layers — via a derive mechanism, not three hand-kept copies.**

Evidence:
- **SKILL.md frontmatter already carries the routing signal.** `sprint-plan`'s `description:` embeds **trigger phrases inline** ("let's plan the sprint", "help me scope [sprint]", "which issues should we tackle next") + `scope:` + (in changelog) **deployment surface** ("Native + Plugin"). The routing metadata already lives at the source.
- **Hand-maintained skill indices ROT.** `.claude/skills/SKILLS.md` (the native index) is a hand-kept table, **"Last Updated 2026-05-15"** — already ~1 month stale vs. the 10 live skills. This is a live Pattern-073 / m-41 instance: a hand-maintained capability list drifts from truth. Building Decision-2's plugin manifest the same hand-kept way would inherit the rot.
- **The #1106 derive-pattern is the precedent.** Mailbox MANIFESTs are *derived* from message frontmatter (recipient is sole writer; regen is idempotent) — exactly so the index can't drift from the directory. Same shape applies here: derive the skills manifest from SKILL.md frontmatter.
- **`pre_classifier.py` confirms Layer 2 is buildable but warns against hand-duplication.** It's a 1934-line wall of ~30 hand-ordered `*_PATTERNS` regex lists (with fragile "MUST be checked BEFORE X" caveats). Adding per-skill trigger patterns *by hand* would grow this and duplicate the trigger phrases that already live in SKILL.md frontmatter. Layer 2 should consume **derived** skill-trigger patterns, not a hand-copied set.

**Architectural consequence**: ADR-072 should name a **`skills` registry derived at server start from SKILL.md frontmatter** (name + description + trigger-phrases + scope + deployment-surface), and have it feed: (1) the **PIPER-SKILLS.md manifest** (Decision 2), (2) the **Layer-2 skill-detection patterns** (Decision 1), and (3) optionally the **Layer-1 tool/`PIPER.md` descriptions**. One source → three consumers → no drift. This composes with **ADR-066 D7** (the derived registry is server-owned state) and is the m-41 "mechanism-displaces-vigilance" cure applied to skill-routing. *(This sharpens my framing-lean #4 from "static registry compiled at startup" to "static registry **derived from SKILL.md frontmatter** at startup" — same mechanism, now with the source-of-truth named.)*

---

## Per-decision: framing-lean → grounding evidence → refined position

### D1 — Authoritative routing layer
- **Lean**: Layer 4 (native SKILL.md exec) authoritative when present; Layer 2 (server pre_classifier) authoritative on plugin path; Layer 3 (context-assembly injection) fallback; Layer 1 (tool descriptions) hint-only.
- **Evidence**: `pre_classifier.py` already does exactly this kind of pattern→`skill_hint` tagging for 30 intent classes (incl. recent additions PROVENANCE/TRUST/INSIGHT_PULL with explicit ordering) → Layer 2 is a natural extension. Layer 1 is *already partially real* (PA: `get_profile`'s description tells Claude to call it "from any skill that wants the user's calibration").
- **Refined**: lean holds. Add: "authoritative" = **highest-confidence layer that fired wins**; layers are additive (PM's "fluid" property), never sequential gates. The floor (prose) catches everything unmatched — never a broken experience.

### D2 — Skills manifest location
- **Lean**: `PIPER-SKILLS.md` alongside `PIPER.md`, governed by the ADR-059 discipline; MCP-resource exposure as Option A.5 for the plugin path.
- **Evidence**: `PIPER.md` is exactly a capability manifest under the ADR-059 "every capability MUST have a working implementation, or the LLM offers a broken experience" rule, with a trigger-phrase→behavior "Usage Examples" pattern. A skills manifest extends this 1:1: the ADR-059 discipline becomes **"a skill listed here MUST be server-side-invocable on the plugin path."**
- **Refined**: `PIPER-SKILLS.md`, **DERIVED from SKILL.md frontmatter** (per the unifying finding — NOT hand-kept like the stale SKILLS.md). ADR-059-governed by construction: a skill only enters the manifest once its plugin-path invocation exists, so the manifest can't list an unrunnable skill. Keep MCP-resource exposure as a plugin-path delivery option (server injects the derived manifest as an MCP resource on connect).

### D3 — Plugin tool topology
- **Lean**: Option A+B hybrid — `ask_piper` (server-routes within, Option B) + `run_skill(name)` meta-tool escape hatch (Option A; single meta-tool, NOT per-skill tools).
- **Evidence**: PA's corrected 5-tool surface (`ask_piper` / `get_profile` / `save_profile` / `get_company_profile` / `save_company_profile`) shows a deliberate separation of concerns (conversation vs. profile-I/O). Per-skill tools would explode the namespace (10 skills → 16+ tools); the meta-tool keeps it at 6. Most PMs say "help me plan my sprint," not "run sprint_plan" → `ask_piper` + server routing is the right default.
- **Refined**: lean holds firmly. `ask_piper` extends with server-side routing (Option B default); `run_skill(name)` is the advanced escape hatch (single meta-tool). **No existing tool renamed/removed** (m-40 layer-then-migrate). `run_skill`'s valid `name` set is the derived registry (D2) → discoverable + drift-free.

### D4 — Skill procedure invocation on plugin path (#1245 territory)
- **Lean**: static registry + compiled prompt fragments at server start (O(1) lookup, immutable runtime, ADR-066 D7 server-owned).
- **Evidence**: SKILL.md is a self-contained prompt-layer procedure (Why / numbered Procedure / output templates / anti-patterns / checklist). On native path it IS the procedure; on plugin path the server must load + inject it. Dynamic per-invocation file reads → startup-latency + race risk; PIPER.md already uses cached hot-reload, the precedent for compile-at-start.
- **Refined**: static registry **derived from SKILL.md frontmatter + body at server start** (the unifying finding); inject the SKILL.md procedure into response context when a `skill_hint` fires (Layer 3). Server-owned per ADR-066 D7. Hot-reload detection (PIPER.md's pattern) keeps it fresh without restart.

### D5 — Trust Gradient × routing (the load-bearing one)
- **Lean**: Trust Gradient as a **separate permission layer above** Layers 1–4 — Gradient = *should-we* (is proactive skill invocation permitted for this user/tier), routing = *which-one*.
- **Evidence**: `trust-check` is itself a live Wave-2 skill (the Gradient is real + user-surfaced: New/Building/Established/Trusted). ADR-071 is what makes the per-user tier lookup possible (Trust Gradient needs the per-user anchor). My framing memo flagged the CXO **"don't-assert-what-you-can't-substantiate"** trust shape may apply: routing must not surface a proactive skill proposal whose trust-permission isn't substantiable.
- **Refined**: lean holds — keep *should-we* (Trust Gradient permission gate) separate from *which-one* (routing). **This is the section to circulate for a CXO + HOST trust-lens review** before/at ratification (it touches the trust contract, not just mechanism). Reactive (PM-asked) skill invocation is tier-independent; **proactive** skill surfacing is what the Gradient gates.

---

## Open questions for v0.1 (carry into authoring)
1. **Derive-registry scope**: does the derived `skills` registry live only server-side, or is a generated `PIPER-SKILLS.md` also committed (human-readable, the way SKILLS.md is)? Lean: server-side registry is canonical; a generated PIPER-SKILLS.md is a committed *artifact* of it (like a derived MANIFEST), regenerated by a script — not hand-edited.
2. **Native SKILLS.md reconciliation**: the stale native `SKILLS.md` should also become derived (kill the rot at its source) — fold as an ADR-072 follow-up or note it as out-of-scope-but-related (Pattern-073 instance).
3. **Trust-lens review on D5**: circulate the D5 section to CXO + HOST at v0.1 (the load-bearing trust decision), per the normal ADR cohort-review flow.
4. **#1245 scope**: PA flagged #1245 (`PIPER-SKILL-MERGE`) scope may expand from ADR-072 — confirm the D2/D4 derive-mechanism is what #1245 builds.

## Next step
Author **ADR-072 v0.1** from this substrate (modeled on ADR-070's D-section shape). The 5 decisions are now evidence-backed with a unifying derive-from-frontmatter spine; D5 circulates for trust-lens review. **Banked to a fresh focused pass** (see session log) — the grounding is the unblocked work drained this fire; the v0.1 deep authoring is the next focused work-unit, not tail-of-marathon work on the most consequential artifact.
