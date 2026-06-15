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

## Bar options → **PM chose B (full conformance now), 2026-06-14**

- **A (recommended)** — *Issue-ready* bar now for all 12: fill the definitional sections (Problem Statement w/ Current State + Impact + Strategic Context, Goal + Not-In-Scope, What-Already-Exists, high-level Acceptance Criteria, Dependencies, Related/ADRs, Priority, Effort estimate). Defer phased Requirements / Testing specifics / Completion Matrix / Evidence to the **per-WS gameplan gate** after the ADR (the cascade's next gate). #1227 (no ADR dependency) can go to full conformance now.
- **B** — Full feature.md conformance now for all 12 (accept that ADR-gated sections get rewritten post-ADR).
- **C** — Full conformance now only for the non-ADR-gated issues (#1227 quick win; #1109/#1110/#1201 Slack robustness/UX); issue-ready bar (Option A) for the ADR-reshaped eight.

## Resolution (2026-06-14)

**PM bar decision: Option B — full `feature.md` conformance now for all 12** (accept that ADR-gated sections refine post-ADR).

**Fix applied** via 5-agent fan-out (one cluster each: WS-1/2 · WS-3/4+quick-win · WS-5/8 · WS-6/7 · WS-9), each rewriting its issues to the full 16-section template, grounded in this audit's file:line facts + the scope doc, preserving prior substance, flagging ADR-dependent specifics `(provisional — refines once Arch's MCP ADR #1232 lands)`. Titles unchanged (body-only edits). Agents independently corrected a few of my path references (e.g. `canonical_handlers.py`/`calendar_offer_policy.py` under `services/intent_service/`; `google_calendar_adapter.py` under `services/mcp/consumer/`; integration routers under `services/integrations/`) and re-verified line numbers against source.

**Re-audit (objective, same section-presence check): all 12 now 16/16.** Bodies grew from ~0.7–3 KB to ~14–22 KB (real content, not stubs). Spot-checked #1232 — grounded, honest provisional flags, correct ADR-001/052/058 reconciliation + precise Not-In-Scope. Priorities: WS-1/2/3/4/5/8/9 → P1; Slack-robustness (#1109/#1110/#1201) + #1227 quick win → P2. Provisional markers heaviest on #1232/#1220 (~6 each) and #1233 (Phase-0 "same human" kept as a gating open question, NOT asserted); **#1227 fully concrete (0 provisional)**.

## Status

- [x] Template open during audit (feature.md)
- [x] Every template requirement has a matrix row
- [x] All ⚠️/❌ fixed (PM bar = full conformance; all 12 at 16/16, verified)
- [x] No requirements marked N/A without PM approval (bar was PM-decided; ADR-gated sections flagged *provisional*, not N/A)
- [x] Audit matrix saved (this file)
- [x] Issue gate COMPLETE — next gates are **per-WS Gameplan → Prompts → Execute**, run as each workstream is picked up (after Arch's ADR for the ADR-gated ones)

_Front bookend of the excellence flywheel; `close-issue-properly` is the back bookend._
