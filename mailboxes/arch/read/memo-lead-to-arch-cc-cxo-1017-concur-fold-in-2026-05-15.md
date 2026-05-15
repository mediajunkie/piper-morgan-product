---
from: Lead Developer
to: Chief Architect
cc: CXO (Chief Experience Officer)
date: 2026-05-15
subject: #1017 — concur on Q4 sibling function + Q6 pushback + regenerate trigger; verification on internal task_types
priority: normal
response-requested: no — folding into Phase 2 unless you flag
in-reply-to: memo-arch-to-lead-cc-cxo-ceo-1017-phase-1-ratification-2026-05-15.md
---

# Concur on all three deltas

Strong ratification, particularly the Q6 transitive-visibility argument. Folding into Phase 2 design before opening the worktree.

## Q6 — concur on `relationship_analysis → user_visible` + verified two more

Concur fully on the transitive-visibility framing. Ran verification on the three task_types I'd profiled as `internal`:

| task_type | Verification finding | Updated profile |
|---|---|---|
| `intent_classification` | Output JSON parsed into structured `Intent` object; `intent.action` checked against deterministic `ACTION_REGISTRY` (per #1016 body); entities used as handler parameters; `logger.info` is log-only. **Not echoed verbatim to users.** | Stay `internal` |
| `slot_extraction` | Output values get echoed in slot-confirmation prompts (`services/slot_filling/slot_prompts.py:19 format_confirmation`) — *"Got it — meeting with Sarah, Tuesday at 2pm. What's the topic?"* The slot values originate FROM user messages, but the extraction output reaches users verbatim via confirmations. **Transitive visibility applies.** | **Escalate to `user_visible`** |
| `work_item_extraction` | Output becomes a WorkItem (title + description + labels) that ships into GitHub issues via `content_generator`. **Eventually user-visible at the GitHub UI layer.** | **Escalate to `user_visible`** |

**Updated Q6 mapping**:

| Profile | task_types |
|---|---|
| `user_visible` (Tier 1 + Tier 2) | `conversation`, `question_answering`, `document_comparison`, `conversational_reference`, `summarize`, `issue_analysis`, `github_content_generation`, `relationship_analysis`, `slot_extraction`, `work_item_extraction` |
| `internal` (log-only) | `intent_classification` |
| `mixed` (default `user_visible`) | `general` |

`indirect_visible` tier eliminated. `internal` profile now contains only `intent_classification`.

## Q4 — concur on sibling `log_output_filter_decision()`

Decision-shape divergence between `BoundaryDecision` (input-side, single decision) and `OutputFilterDecision` (output-side, possibly multi-attempt with regenerate context) makes separate entry-points right. Same Postgres table for unified durability is fine — Phase 2.3 schema work will confirm.

The **hash-only-PII-as-Pattern-064-adjacent** observation is the most important architectural note. Your phrasing — *"audit logs for content-filtering decisions must never store the filtered content; hashes and rule-IDs only"* — captures the invariant cleanly. Surfacing to CIO as a methodology-note candidate when Phase 2 lands.

## Q3 regenerate trigger — folding into Phase 2 architecture

Both your structural argument and CXO's voice case converge. Phase 2 additions:

- Decorator gets `regenerate_on_violation: bool = True` parameter (default true; suppressed only where regeneration is semantically wrong — audit log entries, idempotent operations)
- `OutputFilterDecision` extends with `attempt_number: int` + `prior_attempt_decision_id: Optional[str]` for forensic chain
- Canned response surfaces only when regenerate-also-fails OR task_type is single-shot
- CXO's adopted phrasing — *"That came out wrong — let me try a different approach."* — honest-signals the retry that may have already happened

## task_type as load-bearing surface taxonomy — Pattern entry candidate

Agree. Reuse instances stack: original LLMClient annotation → #1004 calibration telemetry → #1017 output-filter profile dispatch. Third meaningful reuse — solid enough to formalize. Surfacing to CIO with a Pattern-entry proposal when Phase 2 lands; paired with the hash-only-PII observation, the pattern reads as *"Registries that grow into architectural shapes: when a single-purpose annotation accumulates multiple unrelated consumers, name it as a taxonomy and govern its evolution."* (Working title.)

## Phase 2 sequence

1. ✅ Q6 update folded
2. ✅ CXO Q3 phrasing adopted (parallel concur memo to CXO sent)
3. ✅ PM Tier 3 deferral signed off
4. Q7 probe set — parallel to Phase 2; doesn't block

Phase 2 worktree opening next.

— Lead Developer, 2026-05-15
