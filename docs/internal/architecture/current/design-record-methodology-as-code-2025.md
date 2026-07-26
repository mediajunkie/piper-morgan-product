# Design record: the methodology-as-runtime-code bet (Sept 2025)

**Status**: extracted 2026-07-26 at deletion of the `methodology/` package (Arch
fix-or-delete ruling 2026-07-25, decisions.log ~23:35 PT; ADR-028 superseded).
**Why this record exists**: per the ruling, the package's *ideas* predate and
seeded the cohort's live working discipline; the *code* was a dead island
(zero importers, last touched 2025-09-15). PM-033d/chain-of-draft precedent:
preserve the thinking, delete the scaffolding.

## The bet

ADR-028 (Sept 2025) proposed encoding working methodology as **enforceable
runtime code**: a `methodology/` package whose classes would gate agent
behavior programmatically rather than by prose instruction.

Two ideas carried real design weight:

### 1. The Three-Tier Verification Pyramid (`methodology/verification/`)

> PATTERN → INTEGRATION → EVIDENCE

- **PATTERN** — "archaeological discovery of existing implementations" before
  writing anything new (a `PatternDiscovery` scanner over the repo).
- **INTEGRATION** — validation of coordination requirements between agents.
- **EVIDENCE** — "concrete proof requirements, no claims without evidence";
  an `EvidenceCollector` with typed evidence and per-task-complexity
  requirements (`TaskEvidenceRequirements`).

Explicit target: **preventing verification theater** — agents claiming
completion without demonstrable results.

### 2. The Mandatory Handoff Protocol (`methodology/coordination/`)

Zero-bypass handoff enforcement between agents: typed `HandoffContext` /
`HandoffResult`, `EnforcementLevel`s, and a taxonomy of violations
(`HandoffBypassError`, `EvidenceRequirementViolation`,
`StrictEnforcementViolation`) — the idea that an agent-to-agent handoff is a
*contract* whose evidence requirements can be violated, not a message.

## What actually happened

The ideas won; the mechanism lost. The cohort's live discipline implements
every load-bearing concept — as prose, hooks, skills, and gates rather than
runtime classes:

| 2025 code concept | 2026 live mechanism |
|---|---|
| PATTERN tier (archaeological discovery) | CLAUDE.md "Verify First, Create Second" / 75%-complete rule |
| EVIDENCE tier, `EvidenceCollector` | CLAUDE.md "Evidence Required" + issue-closure evidence template + close-issue-properly skill |
| verification-theater prevention | Completion-Theater pattern family (045/046/047/049) + the #1452 burn-down gate (CI-arbitrated, shrink-locked) |
| MandatoryHandoffProtocol | Mailbox discipline (push-to-ref, MANIFEST regen, per-memo commit) + session logs + carry-forwards |
| EnforcementLevels / violations | STOP conditions + PM gates + hooks (check-branch et al.) — with the 2026-07-25 lesson that a hook is an advisory backstop, prose discipline primary |

The runtime-code form failed for a reason worth remembering: **methodology
enforced from inside the codebase can only see code paths, but the behavior
it needed to shape lives in the agent loop** — which is exactly where the
prose+hooks+skills model operates. The package sat unimported for ten months
while the prose discipline it prefigured became the cohort's actual operating
system.

## Lineage pointers

- ADR-028 (superseded 2026-07-26; supersession PM-flagged per #1322 precedent)
- `methodology-02-AGENT-COORDINATION.md` ("Live code" claim corrected at deletion)
- Deleted tree tip for archaeology: see the commit deleting `methodology/`
  (this record rides in it) — `git log --diff-filter=D -- methodology/`
