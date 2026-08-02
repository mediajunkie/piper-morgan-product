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
| EnforcementLevels / violations | STOP conditions + PM gates + a two-layer commit gate — a real `.git/hooks/pre-commit` (a control for what it covers, installed 2026-07-29 after Arch's TOCTOU ruling) plus the advisory PreToolUse layer (sole coverage for `--no-verify` + prior-call staging, per HOST's measured four-cell truth table, 2026-07-29). *(Amended 2026-08-01 on Arch's second read; the earlier "hooks are advisory, prose primary" line described the pre-7/29 state.)* |

The runtime-code form failed for a reason worth remembering — stated with the
boundary Arch's second read supplied (2026-08-01), because unbounded it reads
as "never again" when the truth is narrower: **runtime enforcement of
methodology works exactly where the behavior crosses into an observable
artifact, and fails everywhere else.** A commit, a staged file set, a test
run, an issue transition — enforceable (the 7/29 `pre-commit` gate is
methodology-as-code, and it works). "Did you look first," "did you understand
the whole issue," "is this claim evidenced" — not enforceable at the code
layer, because the behavior leaves no artifact the code can see. The 2025
package aimed almost entirely at the non-artifact-crossing half, and sat
unimported for ten months while the prose discipline it prefigured became the
cohort's actual operating system. Before encoding a discipline as a
mechanism, ask what artifact it produces; if none, it's prose.

**What would make the bet worth revisiting**: as more agent behavior routes
through tool calls — hooks, MCP tool invocations, skill dispatch — the set of
artifact-crossing boundaries grows, and more of the methodology becomes
mechanizable. The 2025 bet was not wrong in principle; it was ten months
early and aimed at the wrong half.

## Lineage pointers

- ADR-028 (superseded 2026-07-26; supersession PM-flagged per #1322 precedent)
- `methodology-02-AGENT-COORDINATION.md` ("Live code" claim corrected at deletion)
- Deleted tree tip for archaeology: see the commit deleting `methodology/`
  (this record rides in it) — `git log --diff-filter=D -- methodology/`
