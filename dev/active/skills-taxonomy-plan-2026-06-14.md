# Piper Morgan Skills Taxonomy — Planning Doc

**Date**: 2026-06-14  
**Owner**: PA (Piper Alpha)  
**Status**: Proposal ready — awaiting PM direction on Wave 1  
**Feeds**: BYOC plan-of-record, plugin experience track

---

## Deployment paths

Skills are portable SKILL.md files — they can be deployed two ways, often both simultaneously:

| Path | How | Who gets it |
|---|---|---|
| 🟢 **Native** | SKILL.md in `.claude/skills/` — available in any Claude Code/Desktop session with Piper's context loaded | PM immediately; no distribution friction |
| 🔵 **Plugin** | Exposed as a tool via the BYOC MCP server (`server.py`) | Alpha testers with the plugin installed |

Most prompt-layer skills are **Native + Plugin** — write once, deploy both ways. The plugin isn't the origin; it's the distribution mechanism. Server-dependent skills (connector wiring, profile storage) are Plugin-only until server APIs are exposed natively.

**Implication**: PM can start using most Wave 1 skills today via native path. Plugin packaging comes after internal refinement.

---

## What we're trying to produce

A **broad taxonomy** of possible Piper Morgan skills (organized by type/function), plus a **core set** recommendation — the skills to write first that give the most value for the least duplication of what the floor already handles well.

The output is a proposal for PM's direction, not a final list. PM decides what makes the cut.

---

## Research completed — 2026-06-14

All three sources have been read. This document is now a **living proposal** ready for PM direction.

### Source 1 — Design intent ✅ DONE
- `docs/briefing/PROJECT.md` — vision, architecture, DDD principles
- `docs/internal/design/mux/` — 21 MUX design documents (see below)
- Competitive landscape: Anthropic PM plugin (8 skills), product-tracking-skills (7 skills), productivity (3 skills), ChatPRD (web app). See §Competitive landscape.

### Source 2 — Actual capability ✅ DONE
- `services/shared_types.py` — 20 IntentCategory values
- `services/intent_service/workflow_entries.py` — 47+ registered workflow actions
- Key finding: the floor handles most information retrieval + simple actions as **prose responses**. Skills add value by providing **structured templates and repeatable output shapes**.

### Source 3 — Empirical learning ✅ DONE
- `pa-skunk-research-R1-marketplace-chatgpt-2026-06-12.md` — marketplace + ChatPRD
- `pa-skunk-research-R2-auth-architecture-2026-06-12.md` — auth + distribution
- Gate-run findings 2026-06-14: ask-piper confirmed; consult-piper enrichment has two gaps (GitHub not wired in Cowork; re-ask payload too large in Code)
- Existing skills: `ask-piper`, `consult-piper`, `meet-piper`

---

## The MUX model as organizing framework

Piper's `docs/internal/design/mux/` contains 21 design documents defining a rich conceptual model. Key elements:

**15 persistent objects**: Product, Project, Feature, WorkItem, Todo, Repository, Conversation, Document, List, KnowledgeNode, Place, UserTrustProfile, and more. Two ownership types: NATIVE (created in Piper) and FEDERATED (windows into external systems like GitHub).

**8-stage lifecycle** every object can move through:
1. EMERGENT — "I just noticed…"
2. DERIVED — "I figured out from…"
3. NOTICED — "I'm aware of…"
4. PROPOSED — "I think we should…"
5. RATIFIED — "We're doing…"
6. DEPRECATED — "This used to be…"
7. ARCHIVED — "I remember when…"
8. COMPOSTED — "I learned that…" (decomposed into learnings)

**Trust Gradient**: 4 stages (New → Building → Established → Trusted) that gate what Piper proactively shares.

**Two-Journal Architecture**: Session Journal (audit trail, immutable) + Insight Journal (learnings, user-correctable).

This model suggests a skills taxonomy that goes far beyond "document generation" — it covers the full PM lifecycle including learning, trust, and reflection.

---

## Competitive landscape

| Plugin | Coverage | Gap vs. Piper |
|---|---|---|
| Anthropic PM plugin (8 skills) | Artifact generation — spec, roadmap, update, brief, research, metrics, sprint, brainstorm | Generic templates; no personalized context; no lifecycle or learning layer |
| product-tracking-skills (7 skills) | Analytics/telemetry instrumentation | Specialist niche; not core PM; future expansion candidate |
| productivity (3 skills) | Memory + task management | General-purpose; Piper's is PM-domain-specific |
| ChatPRD (web app) | Fast document production + CPO coaching + integrations | No personalization; no multi-session compounding; no "colleague who knows you" |

**Key insight**: The marketplace covers Clusters 4 and 5 (artifact generation + analysis) with generic templates. Clusters 3 and 7 (lifecycle + learning/trust) have **no equivalent in any marketplace plugin** — they're Piper-unique.

The correct framing is not "build more skills than competitors" but "build the same skills better (with personalized context) and build the skills nobody else has (lifecycle + trust)."

---

## Taxonomy — 7 clusters

### Cluster 1 — Onboarding & Context *(foundation for everything)*
Skills that establish and maintain Piper's understanding of the PM and their world.

| Skill | Description | Status | Deployment |
|---|---|---|---|
| `meet-piper` | One-time PM profile interview: working style, team, projects | ✅ EXISTS (needs connector setup added) | 🔵 Plugin (profile stored server-side) |
| `connect-piper` | Wire a connector (GitHub, Calendar, Notion) during or after onboarding | 📋 NEEDED — highest leverage item; gates all enrichment-dependent skills | 🔵 Plugin (token storage is server-side) |
| `update-piper` | Refresh profile sections that have drifted | 📋 NEEDED — without this, meet-piper is one-shot and degrades | 🟢 Native + Plugin |
| `show-context` | Show what Piper knows about you right now | 📋 USEFUL — trust-building transparency | 🟢 Native + Plugin |

### Cluster 2 — Daily Interaction *(the main loop)*
The core ask-Piper-a-question flow. Currently split into ask/consult; design decision is to collapse.

| Skill | Description | Status | Deployment |
|---|---|---|---|
| `ask-piper` | Bare passthrough — ask Piper a PM question (rung 2) | ✅ EXISTS | 🔵 Plugin |
| `consult-piper` | Enriched ask — Piper fetches GitHub context before responding (rung 3) | ✅ EXISTS (partial — enrichment gaps) | 🔵 Plugin |
| → `piper` | Collapsed single skill — smart about when to enrich; replaces ask + consult | 📋 DESIGN DECISION (2026-06-14) | 🔵 Plugin (MCP → intent flow) |
| `standup` | Generate standup from recent GitHub + Calendar activity | 📋 FLOOR PARTIALLY HANDLES — skill adds consistent structure | 🟢 Native + Plugin |
| `attention-review` | Structured review of what needs PM attention right now | 📋 FLOOR HAS `attention_query` — skill adds prioritization frame | 🟢 Native + Plugin |

### Cluster 3 — Object Lifecycle *(MUX-unique — no marketplace equivalent)*
Skills for moving objects through the 8-stage lifecycle. These express Piper's unique model of how PM work evolves.

| Skill | Description | Status | Deployment |
|---|---|---|---|
| `propose-feature` | Advance something from NOTICED → PROPOSED: surface a thing Piper noticed and help PM decide to act | 📋 PIPER-UNIQUE | 🟢 Native + Plugin |
| `ratify-decision` | Advance from PROPOSED → RATIFIED: confirm a path, record the decision | 📋 PIPER-UNIQUE | 🟢 Native + Plugin |
| `archive-project` | Guide graceful lifecycle close: ACTIVE → DEPRECATED → ARCHIVED with learnings captured | 📋 PIPER-UNIQUE | 🟢 Native + Plugin |
| `compost-review` | Surface what Piper learned when objects were composted (stage 8 → Insight Journal) | 📋 PIPER-UNIQUE | 🟢 Native + Plugin |

### Cluster 4 — Artifact Generation *(where Anthropic's plugin lives — Piper does it with context)*
Skills that produce structured PM documents. Floor gives prose; skills give templates grounded in YOUR projects and voice.

| Skill | Description | Status | Deployment |
|---|---|---|---|
| `draft-spec` | Feature spec / PRD from a brief — uses your team's patterns + project context | 📋 HIGH VALUE | 🟢 Native + Plugin |
| `draft-issue` | Turn a problem statement into a properly-formed GitHub issue | ✅ DONE (2026-06-14) | 🟢 Native + Plugin |
| `close-issue` | Close an issue properly: update description checkboxes, add evidence comment, then close — no unchecked boxes left unexplained | 📋 HIGH VALUE *(Excellent Flywheel — generalizes `close-issue-properly`)* | 🟢 Native + Plugin |
| `capture-discovered-work` | You found a problem while doing other work — quickly file it so it doesn't vanish | 📋 HIGH VALUE *(Excellent Flywheel — generalizes `discovered-work-capture`)* | 🟢 Native + Plugin |
| `draft-weekly-update` | Weekly PM status update covering what shipped, what's in flight, and what's blocked — in your voice | 📋 HIGH VALUE *(Excellent Flywheel — generalizes `draft-weekly-ship`)* | 🟢 Native + Plugin |
| `draft-update` | Stakeholder update memo — knows your stakeholders and their preferred framing | 📋 | 🟢 Native + Plugin |
| `write-release-notes` | Release notes from closed issues + milestone context | 📋 | 🟢 Native + Plugin |
| `announce-launch` | Launch announcement in your voice | 📋 | 🟢 Native + Plugin |
| `draft-hypothesis` | User/product hypothesis in a structured format | 📋 | 🟢 Native + Plugin |

### Cluster 5 — Analysis & Synthesis *(sense-making from data)*
Piper reads a body of material and produces structured insights. Anthropic's plugin has some of these generically; Piper's versions are grounded in your roadmap and priorities.

| Skill | Description | Status | Deployment |
|---|---|---|---|
| `synthesize-feedback` | Distill themes from user feedback → roadmap recommendations | 📋 HIGH VALUE | 🟢 Native + Plugin |
| `sprint-wrap` | End-of-sprint synthesis: what shipped, what didn't, what carries forward — structured retro artifact | 📋 *(Excellent Flywheel — methodology practice, not yet a skill; generalizes the retro discipline)* | 🟢 Native + Plugin |
| `review-sprint` | Sprint retrospective synthesis from closed issues + velocity data | 📋 | 🟢 Native + Plugin |
| `insight-review` | Surface insights from the Insight Journal — what has Piper been learning? | 📋 PIPER-UNIQUE (ties to Trust architecture) | 🟢 Native + Plugin |
| `competitive-brief` | Quick competitive landscape on a topic | 📋 | 🟢 Native + Plugin |
| `metrics-review` | Review product metrics and surface what matters | 📋 (floor partially handles) | 🟢 Native + Plugin |

### Cluster 6 — Planning *(roadmap + sprint + backlog)*
Piper helps with structured planning work. Floor handles ad-hoc questions; skills provide consistent frameworks.

| Skill | Description | Status | Deployment |
|---|---|---|---|
| `sprint-plan` | Scope a sprint from the GitHub backlog — velocity, capacity, dependencies | 📋 | 🟢 Native + Plugin (richer with GitHub data via plugin) |
| `write-implementation-plan` | Before you build: scope the work, identify dependencies, define phases and done criteria | 📋 *(Excellent Flywheel — gameplan practice; helps any PM planning before coding)* | 🟢 Native + Plugin |
| `audit-phase` | Before moving to the next phase, verify what you have matches what you said you'd produce — catches drift early | 📋 *(Excellent Flywheel — generalizes `audit-cascade`; universally valuable)* | 🟢 Native + Plugin |
| `record-decision` | Capture a decision with its context, rationale, and what it rules out — ADR-lite for any PM | 📋 *(Excellent Flywheel — ADR practice generalized; pairs with `ratify-decision` in Cluster 3)* | 🟢 Native + Plugin |
| `milestone-check` | Check milestone health given open issues and current trajectory | 📋 (floor has `list_milestones` — skill adds health analysis) | 🟢 Native + Plugin |
| `triage-backlog` | Prioritize a set of issues by value/effort, grounded in current product strategy | 📋 | 🟢 Native + Plugin |
| `roadmap-update` | Update roadmap in light of new decisions or shipped work | 📋 | 🟢 Native + Plugin |

### Cluster 7 — Learning & Trust *(the long game — Piper-unique, no marketplace equivalent)*
Skills that surface and manage Piper's compounding knowledge of how this PM works. The longer PM uses Piper, the more valuable these become.

| Skill | Description | Status | Deployment |
|---|---|---|---|
| `pattern-review` | What has Piper learned about how I work? Surface behavioral patterns from the Session Journal | 📋 PIPER-UNIQUE | 🟢 Native + Plugin |
| `trust-check` | What trust tier am I at, and what does that unlock? Transparency into the trust gradient | 📋 PIPER-UNIQUE | 🟢 Native + Plugin |
| `insight-surface` | Proactively surface a Piper learning at the right moment — the "thoughtful colleague" move | 📋 PIPER-UNIQUE | 🟢 Native + Plugin (proactive push needs server-side trigger) |

---

## Core set criteria

A skill belongs in the **core set** (write first) if it meets at least 2 of:
1. **Floor gap** — floor handles this ad-hoc at best; a skill produces a meaningfully better output
2. **Demo value** — makes a compelling moment (visible before/after; shows what's different about Piper)
3. **Unblocked** — doesn't require server-side capabilities we haven't built yet
4. **Piper-unique** — does something no marketplace plugin offers
5. **Low complexity** — writable in <1 day; mostly prompt engineering + profile context injection

---

## Proposed core set (for PM direction)

**Wave 1 — write first:**

| # | Skill | Cluster | Deployment | Status | Why first |
|---|---|---|---|---|---|
| 1 | `draft-issue` | 4 — Artifacts | 🟢 Native + Plugin | ✅ DONE 2026-06-14 | High frequency; clear template; floor won't produce a properly-formed issue |
| 2 | `close-issue` | 4 — Artifacts | 🟢 Native + Plugin | 🔲 Next | Natural pair with draft-issue; PM confirmed; universal GitHub discipline *(Excellent Flywheel)* |
| 3 | `draft-spec` | 4 — Artifacts | 🟢 Native + Plugin | 🔲 | Biggest floor gap; floor gives prose, skill gives a proper PRD; demo-worthy |
| 4 | `synthesize-feedback` | 5 — Analysis | 🟢 Native + Plugin | 🔲 | Piper synthesizes against YOUR roadmap; genuinely better than generic tools |
| 5 | `update-piper` | 1 — Onboarding | 🟢 Native + Plugin | 🔲 | Without this, meet-piper is one-shot and the model degrades over time |
| 6 | `connect-piper` | 1 — Onboarding | 🔵 Plugin | ⏳ Plugin-only | Gates all enrichment-dependent skills; needs server-side token storage |
| 7 | `piper` | 2 — Daily | 🔵 Plugin | ⏳ Plugin-only | The main interaction; replaces ask + consult; wraps MCP → intent flow |

**Direction needed from PM**: confirm write order from #3 onward — does `draft-spec → synthesize-feedback → update-piper` feel right, or does any newly identified skill (e.g. `draft-weekly-update`, `audit-phase`) jump the queue?

**Wave 2 — after Wave 1 ships:**

| Skill | Cluster | Why this wave |
|---|---|---|
| `propose-feature` | 3 — Lifecycle | Piper-unique; ties to MUX model; strong demo once context is established |
| `compost-review` | 3 — Lifecycle | Piper-unique; surfaces the long-game learning value |
| `stakeholder-update` | 4 — Artifacts | High frequency for most PMs; knows your stakeholders |
| `sprint-plan` | 6 — Planning | Needs GitHub backlog integration to be meaningfully better than Anthropic's version |
| `trust-check` | 7 — Learning/Trust | Transparency skill; makes the trust gradient visible to PM |

**Deferred (needs server-side work first):**
- `metrics-review` — needs richer data surface
- `roadmap-update` — needs GitHub write or structured roadmap model
- `insight-surface` (proactive) — needs trust-tier-gated push capability

---

## Work plan

1. ✅ **Research** — all three sources read; competitive landscape mapped; MUX model understood
2. ✅ **Taxonomy proposal** — 7 clusters, 30 skills, core set of 6 (Wave 1) identified
3. 🔲 **PM direction** — PM decides Wave 1 list and ordering
4. 🔲 **Implementation** — PA writes skill files (SKILL.md, prompt-layer); CXO reviews UX of each interaction; Lead Dev for any server-side dependencies
5. 🔲 **Integration** — connect-piper wired into meet-piper onboarding; piper skill replaces ask + consult

---

## Notes on scope

- Skills are prompt-layer artifacts (SKILL.md files), not server-side features. Most can be written without server changes.
- The enrichment gap (consult-piper in Cowork can't reach GitHub) is a connector problem, not a skills problem. `connect-piper` in Wave 1 unblocks all enrichment-dependent skills.
- Some skills (draft-spec, metrics-review, sprint-plan with velocity) benefit from richer server-side tools. These are flagged above; implement the prompt-layer version first, enhance later.
- Cluster 3 (lifecycle) and Cluster 7 (trust/learning) are the most strategically important — no marketplace equivalent, directly express the MUX model's unique value. They belong in Wave 2 because they need the context that Wave 1 (onboarding, connect-piper, daily interaction) provides first.
