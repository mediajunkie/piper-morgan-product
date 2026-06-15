# Skunkworks BYOC PoC — Step 3 PA Synthesis: What the PoC Should Attempt to Build

**Version**: v1.1 (PM ratification absorbed; PM-profile framing per PM 2026-05-17; founder-as-subprofile noted as future direction)
**Status**: Ratified at first formal PM gate; ready for subagent 3 dispatch
**Supersedes**: v1.0 (renamed founder-profile → pm-profile per PM 2026-05-17)
**Author**: PA (Piper Alpha)
**Date**: 2026-05-17
**Inputs**:
- `subagent-1-anthropic-plugin-architecture-study-2026-05-16.md` (plugin/MCP/skills mechanics)
- `subagent-2-pm-extraction-analysis-2026-05-16.md` (PM distinctive features → layer mapping; PoC triangle)
- PM ratifications 2026-05-16 (canonical surface; legal prior; 4 PoC-scope decisions)
- Plan v0.2 (`dev/active/skunkworks-byoc-poc-plan-v0.2-2026-05-16.md`)

**What this memo does**: Translates subagent findings + PM decisions into a build-ready specification for subagent 3. Names what the PoC builds, what it deliberately doesn't build, what tensions it surfaces vs. resolves, and the PM-gate conditions for moving from one build sub-pass to the next.

**What this memo does NOT do**: Specify code, file structures inside the plugin, or prompt bodies. Subagent 3 designs those during the build pass.

---

## TL;DR

The PoC is a **three-feature triangle** that exercises three substantively different parts of the layer-mapping question, with explicit gates between each so build-less discipline holds.

1. **`cold-start-as-pm-profile`** — skill + plugin CLAUDE.md template. Exercises the writable-per-user-config pattern + serial-decisions inversion of legal's batching cold-start.
2. **`insight-journal-flat-file`** — skill + reference + the file itself at `~/.claude/plugins/config/piper-morgan/piper/insight-journal.md`. Exercises state location, audit-trail substrate, confirmation loop.
3. **`composting-via-dreams-mcp`** — single MCP tool wrapping Anthropic Dreams API. Exercises composting trigger placement, Type 1 substrate delegation viability, and the input/output store + review-then-adopt pattern.

**Stretch (cut at second PM gate if absorbing bandwidth)**: a second MCP tool `mcp__piper__dream_type2` that probes whether prompt-engineering atop Dreams produces useful Type 2 (adversarial / risk-rehearsal) output. Minimum-viable probe shape; doesn't aim to outdo Anthropic on dreaming complexity.

**Explicitly OUT-of-scope for the PoC** (documented as memo findings, not build targets): output filter (#1017 architectural casualty), two-layer boundary detector, unihemispheric orchestration, multi-agent coordination machinery, PM-API exposure.

The PoC is **self-contained on the plugin side**. State lives in plugin config files + flat-file + MCP-server-internal storage. PM-API stays internal-only per PM 2026-05-16; future API surface is JSON-shape design work, separate effort.

The build is sequenced as **four sub-passes with PM gates** so build-less discipline holds: 4.a scaffold + Feature 1; 4.b Feature 2; 4.c Feature 3; 4.d optional Type 2 stretch.

---

## The four PM-ratified framings

These shape everything below. Subagent 3 should treat each as load-bearing input.

### Framing 1: Canonical surface = Claude Code (per PM 2026-05-16)

Primary deployment is Claude Code (terminal). Cowork support is mostly free (plugin format shared); MCPB+Skill bundle for Claude Chat is tertiary. The PoC optimizes for Claude Code shape; doesn't try to ship Cowork-specific features or Chat-bundle artifacts.

### Framing 2: Legal-plugin shape is the right prior (per PM 2026-05-16)

PM is calibration-heavy like legal. The pattern is **thin skills over rich config + cold-start writes config + shared profile**. Generic PM plugin pattern (flat skills, no per-user state) is the wrong prior — that's the commodity surface PM is differentiating *away from*.

### Framing 3: Build-less; either-outcome-is-signal (per PM 2026-05-16, Q1 framing)

> "We just want something that does work or could work, not the most complex thing we can imagine. If it does work, that's a basis for something that could be improved. If it doesn't work, that will tell us it has to be more complicated."

Especially applies to the dreaming work: **don't try to outdo Anthropic on dreaming complexity now that they've made it publicly central.** Type 1 via Dreams API is the minimum-viable probe of substrate delegation. Type 2 stretch is the minimum-viable probe of whether prompt-engineering can probe the adversarial dimension. Neither aims for sophistication.

### Framing 4: PoC self-contained on plugin side (per PM 2026-05-16, Q3 clarified)

State lives in plugin config + flat-file + MCP-server-internal. PM-API stays internal-only for the PoC. The forward-looking framing — that any good API should be designed as a product surface, JSON-shape is the design work — is separate from this skunkworks; subagent 3 doesn't need to build the API connection. "Pin to PM-API upstream" mappings from subagent-2's Q2 table get reframed as **future-direction notes** in the PoC documentation, not built dependencies.

---

## The three-feature triangle

Each feature's specification below. Subagent 3 designs internals.

### Feature 1 — `cold-start-as-pm-profile`

**What it is**: A skill (`/piper:cold-start-interview`) that conducts a one-question-at-a-time interview with the user and writes the populated founder profile to `~/.claude/plugins/config/piper-morgan/piper/pm-profile.md`. Plus the shared `~/.claude/plugins/config/piper-morgan/company-profile.md` if first plugin install. Plus a `plugin CLAUDE.md` template at the plugin root showing the structure with `[PLACEHOLDER]` markers (the legal-plugin pattern).

**Why it's in the PoC**: Exercises the writable-per-user-config pattern (the legal-plugin load-bearing innovation per subagent-1); demonstrates the serial-decisions inversion of legal's batching cold-start (per Q4 ratification: one long skill with internal serial loop); produces the actual config files the other two features will read from.

**Shape decisions baked in**:
- **One long skill with internal serial loop** (PM Q4 ratification): single `/piper:cold-start-interview` invocation runs a question loop, asks Q1, waits for answer, writes that section to config, asks Q2, etc. Not N separate skills.
- **Founder-profile vocabulary**: subagent 3 lifts PM's MEMORY.md memo set as the cold-start output schema (anti-sycophancy, anti-silent-failure, serial-decisions, PM-CC-on-memo routing, sibling-projects, write-now-proceed-when-aligned, no-batch-decisions, etc.). The exact memo set to translate is in `~/.claude/projects/-Users-xian-Development-piper-morgan/memory/MEMORY.md` — subagent 3 reads + adapts.
- **Plugin CLAUDE.md template at plugin root** with `[PLACEHOLDER]` markers explaining: "READ from config path. If file doesn't exist or has placeholders, STOP and tell user to run cold-start." Pattern lifted from `claude-for-legal/product-legal/CLAUDE.md` (verified).

**What it surfaces (tensions the build pass exercises)**:
- T6 (cold-start serial-vs-batched inversion): does serial-decisions actually work as a conversational pattern in plugin form, or does it produce friction that batched legal-style avoids? Honest signal either way.
- The writable-per-user-config pattern: does it land cleanly for PM's voice rules, or do some rules (e.g., "no silent failures" — a generative-conduct rule, not a yes/no config) resist file-shape?

**What it explicitly does NOT do**:
- Doesn't build a probe-test for whether Claude's general floor competence can replace PM-specific boundary enforcement (that's a separate finding); subagent 3 just notes whether voice-of-Piper feels recognizable when only the config is in play.
- Doesn't migrate existing PM-internal MEMORY.md content programmatically; subagent 3 manually selects the memo set worth lifting + adapts framing.

### Feature 2 — `insight-journal-flat-file`

**What it is**: A markdown file at `~/.claude/plugins/config/piper-morgan/piper/insight-journal.md` plus two skills: `/piper:journal` (read + render per D4 surfacing rules — Pull mode minimum) and `/piper:reflect` (append new insights, the user-facing write path). Plus a `references/insight-journal-schema.md` documenting the entry structure (type, confidence, derived-from, trust-level-required, visibility, framing).

**Why it's in the PoC**: Exercises state-location question (T1) directly with the cheapest substrate; surfaces audit-trail substrate question (T4); demonstrates confirmation loop in prompt form (E.3); validates whether legal-plugin-style flat-file is structured enough for Piper's InsightJournal model OR whether MCP server / Anthropic Memory Store is needed.

**Shape decisions baked in**:
- **Flat file as substrate** (PM Q2 ratification): cheapest, most-tradeoffs-surfaced; explicit doc note in feature shipped artifact about what MCP server vs. Anthropic Memory Store would change.
- **Markdown structure**: each insight entry as a header + frontmatter block (type, confidence, derived-from, etc.) per the D4 schema. Subagent 3 picks the exact markdown shape.
- **Pull mode minimum**: `/piper:journal` returns the journal in a structured render. Passive mode (Insight Journal navigation) is achievable if file is structured enough; subagent 3 attempts but flags as findings if the markdown structure isn't sufficient. Push mode is NOT built (requires persistent state for "≥24h since last push" check that flat-file can't provide).
- **Audit trail**: confidence updates from the confirmation loop write back to the file. Hash-only audit invariant (per #1017 v1.1) is **explicitly degraded to prompt-discipline** in the PoC; subagent 3 writes the finding into the feature's notes file.

**What it surfaces**:
- T1 (state location): how much of PM's distinctive value can actually live in a flat file?
- T4 (audit trail): the schema-vs-prompt regression for hash-only audit. Surface as known finding, don't try to fix.
- E.1 (substrate choice): does flat-file actually work for the InsightJournal model, or are there inherent structural reasons it doesn't?

**What it does NOT do**:
- Doesn't implement Push mode (requires persistent timing state)
- Doesn't implement confidence-tier behavior (E.2 — confidence×0.5 on rejection, etc.) — that's server-side per subagent-2 mapping; PoC just notes the gap
- Doesn't implement cross-session memory beyond what the flat file provides

### Feature 3 — `composting-via-dreams-mcp`

**What it is**: A single MCP tool `mcp__piper__compost` that takes a scope parameter (e.g., `scope='last-N-sessions'` or `scope='since-date:YYYY-MM-DD'`) and calls Anthropic Dreams API with Type 1 (filing) instructions steered toward PM's composting vocabulary. Returns a new memory store ID + a structured delta the user can review and adopt. Plus an `adopt-gate` skill (`/piper:compost-adopt`) that merges the Dreams output into the InsightJournal flat file from Feature 2.

**Why it's in the PoC**: Exercises the substrate-delegation question (can Anthropic Dreams stand in for PM's composting pipeline?); surfaces composting trigger placement (T2); validates the input/output store + review-then-adopt pattern (AC-3 from PDR-005); produces evidence on whether the spiral can deepen across substrate-delegated runs.

**Shape decisions baked in**:
- **Anthropic Dreams API as substrate** (per CEO 2026-05-12 "Dreams as reference, not substrate" + 2026-05-16 build-less framing): the PoC uses Dreams directly to probe substrate viability. If it works → basis for refinement. If it doesn't → tells us we need PM-owned composting. Either outcome is signal.
- **Composting trigger = `SessionStart` hook** (T2 option c): "Having had some time to reflect…" framing maps cleanly to greeting context. Subagent 3 verifies SessionStart hooks can call MCP tools / API endpoints (one of subagent-2's open questions); if not, falls back to manual `/piper:compost` invocation as honest degradation.
- **Instructions string**: steered toward PM composting vocabulary — "merge duplicates; extract preference patterns; surface corrections to pm-profile.md; produce insight-journal-delta.md." Subagent 3 designs the exact instructions; should be specific enough that Dreams produces output PM-shaped, not generic-shaped.
- **Adopt-gate is explicit**: Dreams output is in a separate memory store; user reviews + invokes `/piper:compost-adopt` to merge into insight-journal.md. Matches the "input never modified, output separate, review-then-adopt" pattern (Architect's strongly-validated borrow-pattern).
- **Spiral observation**: subagent 3 runs the compost-via-dreams twice across different session sets. If the second run produces visibly deeper insights, the spiral *can* survive substrate delegation (some-fidelity). If not, the finding is "spiral needs upstream state; substrate delegation flattens to single-cycle behavior."

**What it surfaces**:
- T2 (composting trigger placement): does SessionStart-hook composting work mechanically? UX-wise?
- A.2 (Type 1 delegation viability): does Dreams produce useful output when steered to PM vocabulary?
- T5 (spiral deepening across substrate): empirical signal from the two-run observation
- Anthropic Dreams Research Preview gating: does the access-form gate make the PoC unviable as a same-week probe, or is access already in place? (Subagent 3 verifies before building.)

**What it does NOT do**:
- Doesn't implement Type 1 composting natively (that's the question — we're delegating to probe viability)
- Doesn't implement unihemispheric / partial-rotating cycles (out of scope per stretch decisions)
- Doesn't try to make Dreams output match PM's exact CompostBin → Decomposer → LearningExtractor → InsightJournal → EmergentCreator pipeline shape (that's PM-internal; we observe what Dreams naturally produces and shape via instructions)

### Stretch — `mcp__piper__dream_type2` (probe only; cut at gate if absorbing bandwidth)

**What it is**: A second MCP tool that calls Anthropic Dreams API with adversarial instructions ("identify failure modes in past sessions; for each, articulate what could go wrong if a similar pattern recurs; produce a risk register, not a knowledge summary"). Returns a separate output store with risk-register semantics.

**Why it's stretch**: Per PM Q1 framing, Type 2 is PM-distinctive IP and even low-fidelity probe produces signal. But it can blow build-less discipline if Features 1-3 are absorbing bandwidth. **Explicit gate**: cut at second PM gate (end of Feature 2) if subagent 3 is over budget.

**Shape decisions baked in**:
- **Minimum-viable probe**: subagent 3 doesn't aim for production-grade Type 2 architecture; just enough to determine whether prompt-engineering atop Dreams produces useful adversarial output at all.
- **Same Dreams API surface as Feature 3**: difference is the instructions string. No new infrastructure.
- **Stretch findings format**: if Type 2 probe works, finding is "prompt-engineering atop Dreams is viable substrate for Type 2 — basis for refinement." If it doesn't, finding is "Type 2 needs more than instructions on Dreams — PM owns the architecture; substrate delegation insufficient."

---

## What we deliberately do NOT build (documented as memo findings)

Per build-less discipline + PM ratification, these surface as **findings** in the PoC's documentation, not as build targets:

| Item | Why not built | What gets documented |
|---|---|---|
| **Output filter (#1017)** | Subagent-2's largest architectural casualty: Claude Code doesn't expose a clean `LLMClient.complete()`-shape decorator hook. PostToolUse is too narrow; subagent proxy doubles latency. | T8 framing: schema-enforced hash-only audit becomes prompt-discipline; this is the loudest "diminished variant" for the plugin shape. |
| **Two-layer boundary detector** | ADR-061's framing acknowledges floor LLM as de-facto layer. Claude Code's general competence may make PM's specific detector redundant in plugin form. | Cousin to T8 (C.2 mapping): plugin-side detector either runs at every input (heavyweight, unclear value) or accepts Claude's floor as sufficient. PoC observes which framing is honest. |
| **Unihemispheric orchestration** | Out of scope per stretch decisions; CMA cookbook territory for headless deployment. | Finding: orchestration scheduling logic doesn't live in stateless plugin; if needed, CMA cookbook is the right shape. |
| **Multi-agent coordination machinery** | PM-internal-only (single-user plugin surface). Mailboxes, sign-off discipline, branch-worktree, merge-keeper, audit cascade — all coordination infrastructure for the multi-agent dev team, not user-facing. | Finding: single-user plugin doesn't carry agent-team coordination; if multi-agent comes back via CMA orchestrator/worker pattern, that's a different deployment surface. |
| **PM-API exposure** | Per PM 2026-05-16 Q3: PM-API stays internal-only for the PoC; future API surface is separate JSON-shape design work. | Finding: "pin to PM-API upstream" mappings (subagent-2 Q2 table) are future-direction notes, not built dependencies. When the time comes to design that surface, "API as product surface, JSON shape is the design work" is the framing. |
| **Full PM-skill catalog** (write-spec, sprint-planning, etc.) | Commodity per Anthropic's PM plugin; not what makes Piper distinctive. | Finding: if Piper-plugin ever ships beyond PoC, the commodity skills are mechanical extensions; the distinctive value lives in the triangle. |

---

## The Q4 tensions table (renamed: "what the PoC actually surfaces")

Subagent-2 named 8 tensions (T1-T8). Mapping them to what each PoC feature exercises:

| Tension | Surfaced by | What we'll learn |
|---|---|---|
| T1 — where does conversation state live? | Feature 2 (flat-file substrate) | Whether flat-file is sufficient for distinctive value or where it breaks |
| T2 — composting trigger placement | Feature 3 (SessionStart hook attempted) | Whether SessionStart hooks support the API call we need; UX viability of "having had some time to reflect" framing on session resume |
| T3 — where does the floor live when Claude IS the model? | Feature 1 (Piper voice through config) | Whether config-driven voice is sufficient or whether subagent-as-orchestrator (option b) is needed |
| T4 — where does the audit trail go? | Feature 2 (audit-via-flat-file) | The schema-vs-prompt regression; **expected finding, not unknown** |
| T5 — does the spiral deepen across substrate? | Feature 3 (two-run observation) | Empirical signal on substrate-delegation viability for stateful evolution |
| T6 — cold-start serial-vs-batched | Feature 1 (one-long-skill internal loop) | Whether serial-decisions inversion of legal pattern works conversationally |
| T7 — federation + PlaceConfidence | NOT in PoC scope (deferred) | Out of scope; future work |
| T8 — output filtering (#1017) | NOT in PoC scope (memo finding) | Documented as largest architectural casualty; not built |

PoC surfaces 5 of 8 tensions directly + 1 as memo finding. T7 deferred entirely — federation isn't load-bearing for the "what lives where" question this PoC asks.

---

## Build sequencing + PM gates

Per plan v0.2 + build-less discipline:

### Sub-pass 4.a — Plugin scaffold + Feature 1 (cold-start)

**What ships**:
- Plugin `plugin.json` manifest
- Plugin root `CLAUDE.md` template with `[PLACEHOLDER]` markers
- `/piper:cold-start-interview` skill (one long skill, internal serial loop)
- `.mcp.json` shell (no servers yet)
- Test invocation: PA or PM runs `/piper:cold-start-interview` end-to-end and verifies config files are written correctly to `~/.claude/plugins/config/piper-morgan/...`

**PM gate**: Does the cold-start interview *feel* like Piper (serial decisions, pm-profile vocabulary, no batching)? Does the config-file pattern hold up? **Continue** if yes; **iterate or stop** if the legal-prior shape doesn't actually fit PM's voice.

### Sub-pass 4.b — Feature 2 (insight-journal-flat-file)

**What ships**:
- `~/.claude/plugins/config/piper-morgan/piper/insight-journal.md` initial file structure
- `/piper:journal` skill (Pull mode read + render)
- `/piper:reflect` skill (append write path with confidence-tier prompt)
- `references/insight-journal-schema.md` (entry structure documentation)
- Pull mode functional; Passive mode attempted; Push mode explicitly out

**PM gate**: Does flat-file substrate actually work for PM's InsightJournal model? Is Passive mode achievable? **Continue** if state-location framing holds; **iterate or stop** if flat-file is fundamentally insufficient.

### Sub-pass 4.c — Feature 3 (composting-via-dreams-mcp)

**What ships**:
- `mcp__piper__compost` MCP tool definition (wraps Anthropic Dreams API)
- `/piper:compost-adopt` skill (merges Dreams output into insight-journal.md)
- `SessionStart` hook integration (if mechanically supported; fallback to manual invocation otherwise)
- Two-run observation: PA runs compost twice across different session sets; spiral-deepening evidence captured in PoC findings

**PM gate**: Does substrate delegation to Anthropic Dreams produce PM-useful output? Does the spiral show deepening? **Continue to stretch (4.d)** if yes; **stop and write findings** if substrate delegation produces evidence the spiral can't survive without PM-owned pipeline.

### Sub-pass 4.d — Optional stretch (Type 2 probe)

**What ships**:
- `mcp__piper__dream_type2` MCP tool (Dreams API with adversarial instructions)
- Minimum-viable test: PA runs Type 2 probe; observes whether output is risk-register-shaped or just consolidation-shaped
- Findings file: prompt-engineering atop Dreams viable for Type 2 / not

**PM gate**: Findings only. PoC is complete after this sub-pass; subagent 3 writes the consolidated PoC retrospective + hands off to Step 5 (leadership read-in).

**Cut condition**: If sub-passes 4.a-4.c absorb full subagent 3 budget, cut 4.d at the prior gate. Stretch is explicitly optional.

---

## What this synthesis is NOT

- Not the build spec — subagent 3 designs internals (file structures, prompt bodies, exact JSON shapes)
- Not committing to a timeline — subagent 3 estimates after the gate ratifies scope; build-less discipline says we iterate per sub-pass, not target an end date
- Not a comprehensive PM-feature port — explicit triangle + stretch; everything else is documented as findings
- Not pre-resolving the tensions — T1-T6 get exercised by features; PoC produces signal, not pre-determined answers
- Not gating on Lead Dev or other agents — PA owns the build under PM ratification; Architect heads-up already filed; leadership read-in is Step 5 per plan, after first feature expressed end-to-end

---

## Ratification ask

For PM at this gate (Step 3 → Step 4):

1. **Endorse the three-feature triangle + Type 2 stretch as the PoC scope.** Or flag a feature to swap / cut / add.
2. **Endorse the four-sub-pass sequencing with PM gates between each.** Or propose different gate cadence.
3. **Endorse the explicit out-of-scope items as memo-finding-only.** Or flag a "no, we need to attempt this" item.
4. **Endorse the framing that the PoC is self-contained on plugin side, PM-API stays internal.** This was answered at the question level; confirming it lands in the synthesis correctly.

If PM endorses without changes: subagent 3 dispatches with this synthesis as the build spec. If PM flags changes: PA revises synthesis to v1.1 before subagent 3 dispatch.

---

## Out-of-scope notes for the future (not blocking PoC)

Surfaced during synthesis; worth memorializing somewhere when there's time:

- **"API as product surface, JSON shape is design work"** (PM 2026-05-16): probably a future PDR or design note when PM-API exposure work begins. Not PA's lane to file; flagging for awareness.
- **Founder-profile as future subprofile** (PM 2026-05-17): Piper is fundamentally a tool for PMs; founder is a particular kind of PM. If the PoC validates the pm-profile pattern, a future iteration could add subprofile branching (founder-PM / scaleup-PM / enterprise-PM / agency-PM) where the cold-start asks an early "what kind of PM are you?" question and branches subsequent question tracks. Out of scope for the PoC; the v1 cold-start uses a single PM-style question track informed by xian's MEMORY.md as the schema source.
- **The Type 2 substrate-delegation viability question**: if the PoC stretch probe works, the finding likely warrants a follow-up methodology entry (extending methodology-27 with "operational substrate notes"). CIO's lane.
- **The Architect ↔ Klatch Daedalus alignment conversation** on canonical context-package format (Apr 11 cross-pollination brief flag, still open per Architect): the PoC's "what lives where" findings may inform that conversation. PA flags to Architect at Step 5 leadership read-in.

---

— PA, 2026-05-17, ratification-ready
