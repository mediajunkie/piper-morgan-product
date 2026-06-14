# Audit Cascade — RECONNECT sprint, ISSUE phase

**Skill**: `audit-cascade` (Pattern-049) · **Gate**: Issue → (Gameplan) · **Template**: `.github/ISSUE_TEMPLATE/feature.md` ("features, fixes, refactors" — the right template for all 12; `bug_report_alpha.md` is for tester-submitted bugs, not engineering issues) · **Date**: 2026-06-14 · **Auditor**: Lead Dev

## Audit matrix: 12 RECONNECT issues against feature.md (16 sections)

`✓` = section present · `·` = missing

| feature.md section | 1226 | 1199 | 1229 | 1230 | 1231 | 1232 | 1201 | 1109 | 1110 | 1220 | 1233 | 1227 |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Problem Statement (Current State) | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✓ | ✓ | ✓ | ⚠️ | ⚠️ |
| Impact (Blocks/User/Tech-Debt) | · | · | · | · | · | · | · | · | · | · | · | · |
| Strategic Context | · | · | ⚠️ | · | · | ⚠️ | · | · | · | · | · | · |
| Goal / Primary Objective | · | · | · | · | · | · | · | · | · | · | · | · |
| Not In Scope | · | · | · | · | · | · | · | · | · | · | · | · |
| What Already Exists | · | · | · | · | ⚠️ | ⚠️ | · | · | · | ⚠️ | · | · |
| Requirements (phased) | · | · | · | · | · | · | · | · | · | · | · | · |
| Acceptance Criteria | · | · | · | · | · | · | · | ✓ | ✓ | · | · | · |
| Completion Matrix | · | · | · | · | · | · | · | · | · | · | · | · |
| Testing Strategy | · | · | · | · | · | · | · | ✓ | · | · | · | · |
| Success Metrics | · | · | · | · | · | · | · | · | · | · | · | · |
| STOP Conditions | · | · | · | · | · | · | · | · | · | · | · | · |
| Effort Estimate | · | · | · | · | · | · | · | · | · | · | · | · |
| Dependencies | · | · | · | · | · | · | · | ⚠️ | ⚠️ | · | · | · |
| Related (ADRs/docs) | ✓ | · | ✓ | ⚠️ | ⚠️ | ⚠️ | · | ✓ | ✓ | ✓ | · | ✓ |
| Priority field | · | · | · | · | · | · | · | · | · | · | · | · |

**Per-issue conformance**: #1109 richest (~3/16); #1110/#1220 (~2/16); #1226/#1229/#1231/#1227 (~1/16); #1199/#1230/#1232/#1201/#1233 (0–1/16). **Sprint-wide: scoping-level, not implementation-ready.**

## Finding

The 12 issues were authored as a *workstream decomposition* (each has a Problem + Scope + refs), not against `feature.md`. Uniform gaps: **none** has a structured Impact, Goal/Not-In-Scope, phased Requirements, Acceptance Criteria (except #1109/#1110), Testing Strategy (except #1109), Success Metrics, STOP Conditions, Effort Estimate, Priority, or Completion Matrix.

## The decision this audit surfaces (skill critical rule → PM, not self-decided)

The `audit-cascade` skill grants **zero authorization to mark any requirement "N/A"/deferred without PM approval.** Two things make full feature.md conformance *now* non-trivial for this sprint:

1. **ADR-gating.** RECONNECT is gated on Arch's MCP ADR, which reshapes WS-1/2/5. Writing concrete phased Requirements / final Acceptance Criteria / Testing Strategy for #1226/#1199/#1229/#1230/#1231/#1232/#1233/#1220 *now* would be specifying detail the ADR will invalidate.
2. **The cascade has a later gate for that detail.** Issue → **Gameplan** → Prompts → Execute. Implementation detail (phased tasks, completion matrix, evidence) is the *gameplan* gate's job, per-WS, after the ADR. feature.md's own Evidence/Completion sections say "filled in during/after implementation."

→ **Bar decision is PM's** (recorded as PENDING below). Fixes are NOT applied until the bar is set, to avoid writing ADR-invalidated fiction.

## Bar options (recommendation: A)

- **A (recommended)** — *Issue-ready* bar now for all 12: fill the definitional sections (Problem Statement w/ Current State + Impact + Strategic Context, Goal + Not-In-Scope, What-Already-Exists, high-level Acceptance Criteria, Dependencies, Related/ADRs, Priority, Effort estimate). Defer phased Requirements / Testing specifics / Completion Matrix / Evidence to the **per-WS gameplan gate** after the ADR (the cascade's next gate). #1227 (no ADR dependency) can go to full conformance now.
- **B** — Full feature.md conformance now for all 12 (accept that ADR-gated sections get rewritten post-ADR).
- **C** — Full conformance now only for the non-ADR-gated issues (#1227 quick win; #1109/#1110/#1201 Slack robustness/UX); issue-ready bar (Option A) for the ADR-reshaped eight.

## Status

- [x] Template open during audit (feature.md)
- [x] Every template requirement has a matrix row
- [ ] All ⚠️/❌ fixed — **BLOCKED on PM bar decision** (above)
- [ ] No requirements marked N/A without PM approval — *honored: not self-deciding; asking*
- [x] Audit matrix saved (this file)
- [ ] Ready to proceed to gameplan gate — **after bar + fixes**

_This is the front bookend of the excellence flywheel; `close-issue-properly` is the back bookend._
