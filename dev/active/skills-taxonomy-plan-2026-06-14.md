# Piper Morgan Skills Taxonomy — Planning Doc

**Date**: 2026-06-14  
**Owner**: PA (Piper Alpha)  
**Status**: Planning — research sprint pending (new chat)  
**Feeds**: BYOC plan-of-record, plugin experience track

---

## What we're trying to produce

A **broad taxonomy** of possible Piper Morgan skills (organized by type/function), plus a **core set** recommendation — the skills to write first that give the most value for the least duplication of what the floor already handles well.

The output is a proposal for PM's direction, not a final list. PM decides what makes the cut.

---

## Research method: three sources

### Source 1 — Design intent (what Piper imagines doing)
- `docs/briefing/PROJECT.md` — product vision and positioning
- `docs/briefing/BRIEFING-CURRENT-STATE.md` — current sprint + design decisions
- Any product vision / narrative docs in `docs/`
- Competitive landscape from R1 (Anthropic's PM plugin skills: `/write-spec`, `/roadmap-update`, `/stakeholder-update`, `/synthesize-research`, `/competitive-brief`, `/metrics-review`)
- `phuryn/pm-skills` (68 skills, 9 plugins) as a reference for breadth

### Source 2 — Actual capability (what Piper can do right now)
- `services/intent/` — intent categories and action types
- `services/intent_service/workflow_entries.py` — workflow dispatcher entries
- `services/domain/models.py` — domain model surface
- `services/shared_types.py` — enums (what types of things Piper understands)
- What the conscious floor handles vs. what specialized workflows handle

### Source 3 — Empirical learning (what has been prototyped and learned)
- PA session logs in `dev/2026/` — especially skunkworks sessions
- `pa-skunk-research-R1-marketplace-chatgpt-2026-06-12.md`
- `pa-skunk-research-R2-auth-architecture-2026-06-12.md`
- `pa-1185-multi-tenant-byo-key-investigation-2026-06-10.md` (if exists)
- Gate-run findings from 2026-06-14 (ask-piper confirmed; consult-piper enrichment gaps)
- Existing skills as proof of what's writable: `ask-piper`, `consult-piper`, `meet-piper`

---

## Draft taxonomy (initial sketch — to be validated by research)

### Category A — Context & onboarding
Skills that establish Piper's understanding of the PM and their context. Foundation for everything else.

| Skill | Description | Status |
|---|---|---|
| `meet-piper` | One-time PM profile interview | ✅ EXISTS |
| `update-piper` | Refresh profile sections that have drifted | 📋 NEEDED |
| `connect-piper` | Wire a connector (GitHub, Calendar, Notion) | 📋 NEEDED — currently missing from meet-piper |
| `show-context` | Show what Piper knows about you right now | 📋 USEFUL |

### Category B — Daily PM questions
The core value prop — ask Piper a question and get a grounded answer. Currently split into ask/consult; design decision is to collapse into one.

| Skill | Description | Status |
|---|---|---|
| `ask-piper` | Ask Piper a PM question (bare passthrough, rung 2) | ✅ EXISTS |
| `consult-piper` | Ask Piper enriched with GitHub context (rung 3) | ✅ EXISTS (partial — enrichment gaps) |
| → `piper` | Collapsed single skill (ask + consult, smart about when to enrich) | 📋 DESIGN DECISION |

### Category C — Creation & drafting
Piper helps produce artifacts. Floor handles ad-hoc; skills handle structured templates.

| Skill | Description | Status |
|---|---|---|
| `draft-issue` | Turn a problem statement into a GitHub issue | 📋 HIGH VALUE |
| `draft-spec` | Feature spec / PRD from brief | 📋 HIGH VALUE |
| `draft-update` | Stakeholder update memo | 📋 HIGH VALUE |
| `draft-brief` | Quick competitive or research brief | 📋 |
| `draft-hypothesis` | User/product hypothesis in a standard format | 📋 |

### Category D — Analysis & synthesis
Piper reads a body of material and synthesizes it.

| Skill | Description | Status |
|---|---|---|
| `synthesize-feedback` | Distill themes from user feedback | 📋 HIGH VALUE |
| `competitive-brief` | Quick competitive landscape on a topic | 📋 |
| `metrics-review` | Review metrics and surface what matters | 📋 |
| `review-sprint` | Sprint retrospective synthesis | 📋 |

### Category E — Planning & prioritization
Piper helps with roadmap and sprint work.

| Skill | Description | Status |
|---|---|---|
| `roadmap-update` | Update roadmap in light of new decisions | 📋 |
| `sprint-plan` | Help scope a sprint from the backlog | 📋 |
| `milestone-check` | Check milestone health given open issues | 📋 |
| `triage-backlog` | Prioritize a set of issues by value/effort | 📋 |

### Category F — Communication
Piper helps PM communicate with the team, stakeholders, users.

| Skill | Description | Status |
|---|---|---|
| `stakeholder-update` | Status update for a stakeholder | 📋 |
| `announce-launch` | Draft a launch announcement | 📋 |
| `write-release-notes` | Release notes from closed issues | 📋 |

### Category G — Research
Deep or structured research on a topic.

| Skill | Description | Status |
|---|---|---|
| `deep-research` | Multi-source, fact-checked research report | ✅ EXISTS (PA has this) |
| `user-research-plan` | Plan a user research study | 📋 |

---

## Core set criteria

A skill belongs in the **core set** (write first) if it meets at least 2 of:
1. **Floor gap** — Piper frequently floors on this type of request (high-frequency miss)
2. **Demo value** — it makes a compelling demo moment (visible before/after)
3. **Unblocked** — doesn't require capabilities we haven't built yet
4. **Differentiated** — does something the Anthropic PM plugin doesn't (personalized context, knows YOUR projects)
5. **Low complexity** — writable in <1 day; mostly prompt engineering + profile context injection

---

## Proposed core set (hypothesis — validate after research)

1. **`connect-piper`** — wires connectors during onboarding; eliminates Cowork enrichment gap; high leverage for everything downstream
2. **`draft-issue`** — turns a problem into a tracked issue; floor handles it ad hoc but a structured skill with templates would be much better
3. **`synthesize-feedback`** — Piper synthesizes user feedback into themes; high-value PM task, fits the floor's category model
4. **`update-piper`** — refresh the PM profile; without this, meet-piper is one-shot and drifts
5. **Collapsed `piper`** — the one smart skill that replaces ask + consult; core to the product

---

## Work plan

1. **Research sprint** (new chat, ~1 session): read the three sources in parallel, validate/extend the draft taxonomy above, identify the core set with evidence
2. **Proposal**: structured doc + proposed issue list for PM review
3. **PM direction**: PM decides which skills to build first and in what order
4. **Implementation**: Lead Dev (or PA subagent) writes the skill files; CXO reviews UX of the skill interaction

---

## Notes on scope

- Skills are prompt-layer artifacts (SKILL.md files), not server-side features. They can be written without server changes in most cases.
- The enrichment gap (consult-piper in Cowork can't reach GitHub) is a connector problem, not a skills problem. Fixing `connect-piper` during `meet-piper` unblocks all enrichment-dependent skills.
- Some skills (draft-spec, metrics-review) benefit from richer server-side tools (GitHub write, structured output). Flag those as "server-side dependency" in the proposal.
- The Anthropic PM plugin's skill names are a useful reference for what PMs expect — but Piper's differentiation is context-awareness, not more skills. Quality over quantity.
