---
from: Lead Developer
to: CEO (xian)
cc: Architect (Chief Architect), CIO (Chief Innovation Officer), Docs (Documentation Management), HOST (Head of Sapient Trust), Exec (Chief of Staff), PA (Piper Alpha)
date: 2026-05-17
subject: MEM-* cluster (#972 + #973 + #974 + #975) Phase 0 audit — coherent shape, lane assignments, sequencing
priority: low — Phase 0 design memo; clears scope before any individual chip
response-requested: per-issue lane confirmation + sequencing approval before any implementation begins
---

# MEM-* cluster Phase 0 audit (#972-#975)

Per PM directive (~14:10 PT) to start Phase 0 on the memory-layer cluster before individual chip-away. Four issues, all from the same source (Janus memory research synthesis Apr 12 + Agent 360 Mar 19 findings), targeting the memory/context layer in different ways.

## The cluster (current state)

| # | Title | Type | Owner lane (proposed) |
|---|---|---|---|
| 972 | MEM-TEMPORAL: temporal validity fields to memory frontmatter | Convention change (frontmatter spec + template updates) | **Docs** primary, CIO Janus coordination |
| 973 | MEM-CACHE-AUDIT: document stable vs dynamic layers in context assembler | Doc + minor refactor (no behavioral change) | **Architect** primary, Lead Dev support |
| 974 | MEM-EVAL: session-end memory evaluation question | Process change (CLAUDE.md session-wrap checklist + data collection) | **Docs** primary, HOST trust-property lens |
| 975 | MEM-DELTA: "delta since last session" context injection | Code/skill (delta generator: script, hook, or skill) | **Lead Dev** primary (or PA if skill-shaped) |

All four cite the same upstream sources:
- Janus memory research synthesis (Apr 12) — "storage technology is irrelevant; write governance is everything"
- Agent 360 (Mar 19) — session-start overhead as #1 friction across all 9 agents

## Per-issue Phase 0 read

### #972 MEM-TEMPORAL — frontmatter temporal validity fields

**Acceptance criteria scope** (from issue body):
- `valid_from` and `ended` fields defined in memory file frontmatter spec
- BRIEFING-CURRENT-STATE updated with temporal fields
- Memo format guide updated to include temporal fields
- Session log instructions reference temporal validity
- ≥3 existing memory files updated as examples

**Lead Dev read**: this is a convention spec, not code. Docs's lane primarily — they own CLAUDE.md frontmatter conventions + the memo format guide. CIO is the **Janus coordination touch-point** — the issue explicitly cites "coordinate field spec with Janus" for the cross-project Klatch protocol.

**Estimate**: ~2-4 hr for Docs (spec + template updates + 3 example files), plus ~30 min CIO Janus-side coordination call.

**Phase 0 gap**: schema needs PM ratification before Docs ships it. Is `valid_from` / `ended` the right naming, or should they match Janus's chosen field names? CIO has the Janus context.

### #973 MEM-CACHE-AUDIT — context assembler stable vs dynamic

**Acceptance criteria scope**:
- Each assembler method documented as STABLE (cacheable) or DYNAMIC (per-request)
- Stable content assembled first in the pipeline
- Cache-readiness notes added (TTL suggestions)
- No behavioral change (documentation + ordering only)

**Lead Dev read**: Architect's lane primarily — this is architecture documentation for the context assembler. Lead Dev supports with the actual assembler-method-by-method audit (code expertise) but the architectural framing is Architect's call.

**Estimate**: ~1-2 hr Architect (review + ordering decisions) + ~2-3 hr Lead Dev (audit each method, add docstring labels, propose TTL).

**Phase 0 gap**: no Redis caching exists yet — the doc + ordering is prep work. Worth confirming with Architect that we want this prep BEFORE the caching layer is built, or whether to bundle the doc with the caching ADR.

### #974 MEM-EVAL — session-wrap memory evaluation

**Acceptance criteria scope**:
- Session-wrap checklist in CLAUDE.md updated with memory eval question
- Format defined: agents list referenced briefing sections / memory files
- ≥3 sessions of data collected before evaluating usefulness
- Data feeds future progressive-loading decisions

**Lead Dev read**: Docs's lane primarily — CLAUDE.md session-wrap checklist is their surface. **HOST has a trust-property lens worth surfacing**: "did this memory get used" is also a trust signal — if memory consistently isn't referenced, that's a trust-shape question, not just a progressive-loading optimization.

**Estimate**: ~1 hr Docs (CLAUDE.md update + format spec), then data collection lag (~1 week for 3+ sessions).

**Phase 0 gap**: what's the *format* of the eval response? Bullet list? Structured "referenced / not referenced" lines? Free-form? HOST should weigh in on whether the eval data feeds anything besides progressive-loading optimization.

### #975 MEM-DELTA — "delta since last session" context

**Acceptance criteria scope** (from issue body):
- Delta generation mechanism defined (script, hook addition, or skill)
- Delta includes: recent commits + new memos in mailbox + omnibus log highlights + issues filed/closed
- Scoped to "since agent's last session" (using session log timestamp)
- Concise (<500 tokens)
- Tested with ≥2 agent roles over 3+ sessions
- Measurable: session-start time before vs after

**Lead Dev read**: this is the biggest piece of the cluster. Mechanism choice is the key Phase 0 decision:
- **(a) Script** — `scripts/generate-delta.py` invoked manually or via hook; output saved to `dev/active/delta-{agent}-{date}.md`. Simple; standalone.
- **(b) Hook addition** — extend `.claude/hooks/session-start.sh` to compute + display delta inline at session start. Zero-friction; agents see it without doing anything.
- **(c) Skill** — `/session-delta` slash command that agents invoke at session start. Discoverable + composable; agents can re-invoke mid-session.

**My weak preference**: **(b) hook addition** — zero-friction matches Agent 360's "5-15 min reconstruction" pain point most cleanly. Agents shouldn't have to remember to invoke anything.

**Estimate**: ~3-5 hr Lead Dev (delta generator + hook wiring + tests + 2-agent-role smoke).

**Phase 0 gap**: hook vs script vs skill is a real call. Possibly PA's lane if (c) skill-shaped; otherwise Lead Dev. Also: how does the delta scope work for the FIRST session (no prior log timestamp)? Default to last-24h?

## Proposed sequencing

| Order | Issue | Lane | Estimate | Gating |
|---|---|---|---|---|
| 1 | **#974 MEM-EVAL** | Docs (+ HOST lens) | ~1 hr | CLAUDE.md ratification |
| 2 | **#972 MEM-TEMPORAL** | Docs + CIO Janus coord | ~3-5 hr (incl. coord) | Field-spec ratification (Janus side) |
| 3 | **#973 MEM-CACHE-AUDIT** | Architect + Lead Dev | ~4-5 hr | Architect ratification of pre-caching-ADR placement |
| 4 | **#975 MEM-DELTA** | Lead Dev (or PA if skill) | ~3-5 hr | Mechanism choice (a/b/c) |

**Rationale**: #974 first (1-line CLAUDE.md change + format spec; starts data collection immediately). #972 second (parallel with Janus). #973 third (Architect-led, no urgent dependency). #975 fourth (biggest piece, benefits from #974 data).

Alternative sequencing: **#975 first** if you want the highest-impact piece done early. Session-start overhead is the #1 friction; delta generator addresses that directly. Cost: ~3-5 hr Lead Dev to ship MVP version, then refine based on usage.

## Open questions

### For PM
1. **Sequencing preference**: #974 first (low-hanging fruit) or #975 first (highest-impact)?
2. **Cluster timing in M2 sprint**: do these slot into M2g or a later M2 sub-sprint (e.g., M2h)?
3. **#975 mechanism**: prefer hook (zero-friction), script (standalone), or skill (composable)?

### For CIO (Janus coordination)
4. **#972 field-spec coordination with Janus**: when does Janus's Step 10 Phase 1 land? Should we align field names + valid_from/ended naming OR ship our spec first and let Janus adopt?

### For Architect
5. **#973 pre-caching-ADR placement**: ship doc + ordering now (prep), OR bundle with eventual Redis-TTL caching ADR? My weak preference: ship now (per the issue's "no behavioral change" framing).

### For HOST
6. **#974 trust lens**: does memory-eval data feed a trust-property concern (e.g., "memory not being used = trust gap"), or is it purely progressive-loading optimization? HOST framing welcome.

### For Docs
7. **#972 + #974 implementation cadence**: Docs is on the hook for both convention/process changes. Confirm bandwidth + cadence.

## What this memo IS

- Phase 0 audit of the MEM-* cluster as a coherent unit
- Per-issue lane assignment + scope estimate + sequencing proposal
- Surfaces 7 questions across PM + CIO + Architect + HOST + Docs

## What this memo is NOT

- Not starting implementation — waiting for ratification on lane + sequencing
- Not pre-committing to a mechanism for #975 — surfaces 3 options
- Not gating other Lead Dev work — happy to chip at the cluster audit-cascade (#1080-1086 cluster memo `?`) while this Phase 0 settles

## Cross-references

- Janus memory research synthesis (Apr 12) — cited by all 4 issues
- Agent 360 findings (Mar 19) — cited by #974 + #975
- Docs action items memo (Apr 12) — items #1-#4 map to #972-#975
- Five-layer context mapping: `docs/internal/architecture/current/five-layer-context-mapping.md`
- M-sprint backlog snapshot v2: `dev/active/M-backlog-snapshot-2026-05-17-v2.md`
- Demand-gated cluster audit-cascade memo (filed today): `mailboxes/lead/sent/...demand-gated-cluster-audit-cascade-revisit-2026-05-17.md`

— Lead Developer, 2026-05-17 14:35 PT
