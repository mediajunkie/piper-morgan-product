# Audit Cascade — #1272 MEM-EVAL corpus analysis (CIO, 2026-06-17)

Per PM 2026-06-17: gameplan → audit-cascade (vs the plan + issue + child issues + subagent prompts) → execute. Three audit gates below. **Template-fit note:** the canonical templates (gameplan v9.6, agent-prompt v10.2) are **code-task-oriented**; this is a **corpus-analysis** task (read 135 logs, aggregate, classify, recommend — no code, endpoints, DB, or UI). Per the audit-cascade rule I do **not** self-mark requirements N/A — I audit every **transferable** requirement (and fix gaps) and **flag the code-specific ones for PM confirmation** in the block at the bottom.

## Gate 1 — Issue #1272 vs `.github/ISSUE_TEMPLATE/feature.md`
| Requirement | Status | Notes |
|---|---|---|
| Clear title | ✅ | "MEM-EVAL corpus analysis — classify…" |
| Problem / objective | ✅ | Objective + the two downstream decisions |
| Acceptance criteria / phases | ✅ | 4 phase checkboxes (P1–P4) |
| Related issues linked | ✅ | #974 (pilot), gameplan doc |
| Scope / out-of-scope | ✅ | "RECOMMENDS only; implementation = child issue" |
| Guards / constraints | ✅ | propose-and-diff, role-spread, recency, lane |
| Labels | ✅ | enhancement |

## Gate 2 — Gameplan vs `knowledge/gameplan-template.md` (v9.6) — transferable requirements
| Requirement (transferable) | Status | Fix |
|---|---|---|
| Issue # referenced | ✅ | #1272 + #974 in header |
| Problem/objective stated | ✅ | one-liner + objective |
| Assumptions verified before building (Phase-1 analog) | ✅ | corpus confirmed (135 logs), 3-bucket format, pilot tracker read — **made explicit in the fix** |
| Success criteria (measurable) | ❌→✅ | **FIX: added "Success criteria" section** |
| Phases with estimates | ⚠️→✅ | 4 phases present; **FIX: added rough estimates** |
| Test / validation strategy | ⚠️→✅ | guards cover it; **FIX: framed the validation pass explicitly** (normalization spot-check, role-spread sanity, recency) |
| Rollback / resumability | ✅ | "Resumability" section (phase-commits + scratch capture) |
| Dependencies | ✅ | corpus, subagents, Docs/HOST |
| STOP conditions | ❌→✅ | **FIX: added "STOP conditions" section** |
| Risks identified | ✅ | 6-item risks/guards list |
| Web framework / CLI / DB / endpoints (Phase -1 code infra) | ⚠️ PM-CONFIRM | code-task requirement — see N/A block |
| Frontend-Backend contract (Phase 0.5) | ⚠️ PM-CONFIRM | UI-task requirement — see N/A block |

## Gate 3 — Gather-subagent prompt vs `knowledge/agent-prompt-template.md` (v10.2) — transferable
| Requirement (transferable) | Status | Fix |
|---|---|---|
| Identity / role | ✅ | "data-extraction subagent" |
| Acceptance criteria (explicit checkboxes) | ❌→✅ | **FIX: added explicit acceptance-criteria checkboxes** to the prompt |
| Evidence the agent must provide | ⚠️→✅ | **FIX: added data-extraction evidence** (logs-read count, section-found count, ambiguous count) |
| Handoff/return format | ✅ | JSON schema specified |
| Scope bounds | ✅ | per-role glob; return data only, no log contents |
| "Output enables next step" framing | ✅ | feeds Phase 2 aggregate |
| Post-compaction protocol | ⚠️ PM-CONFIRM | short single-shot subagent; see N/A block |
| Infra verification / test-count / pytest output / files-modified / user-testing-steps | ⚠️ PM-CONFIRM | code-task evidence — see N/A block |

## ❓ Code-specific requirements flagged for PM (NOT self-marked N/A)
These template requirements are specific to **code/UI/feature** work and have no analog in a read-logs-and-aggregate task. I'm flagging them per the audit-cascade no-self-N/A rule rather than silently skipping:
- Web framework / CLI / DB / existing-endpoints infrastructure verification (gameplan Phase -1)
- Frontend-Backend contract verification (gameplan Phase 0.5)
- Post-compaction protocol in the subagent prompt (these are short single-shot extraction subagents, not session-spanning)
- Code evidence: test count, `pytest` output, files-modified-with-line-counts, user-testing-steps (the subagent produces *data*, not code)

**Ask:** confirm these are not-applicable for this corpus-analysis task type, or tell me how you'd like them handled. (My read: not-applicable — but per the rule, your call, not mine.) This is the natural pre-execution checkpoint anyway: with the transferable gaps fixed, the plan is resilient + ready for Phase 1 on your nod (or the next autonomous fire, since it's committed + resumable).

## Result
All **transferable** ⚠️/❌ items fixed in the gameplan (success criteria, estimates, STOP conditions, validation strategy, explicit assumptions-verified, subagent acceptance-criteria + evidence). Only the code-specific block awaits PM confirmation. Drift caught + corrected before spending tokens on 5+ subagents × 135 logs.

— CIO, 2026-06-17
