# Inversion Sweep Report — Issue #962

**Date**: 2026-04-12
**Author**: Lead Developer (via subagent research)
**Scope**: 8 components audited for "LLM shortcut inversion" pattern

## Summary

3 actual inversions found across 8 components. 2 are being actively retired by floor migration work. The remaining systemic risk is concentrated in STATUS and PRIORITY — the two categories that haven't migrated to floor yet.

## Findings

| # | Component | Inversion? | Current Impact | M2 Risk | Action |
|---|-----------|-----------|----------------|---------|--------|
| 1 | PreClassifier (644 patterns) | Partial | Low (mitigated by Action Gate) | Medium | Monitor; consider confidence < 1.0 |
| 2 | ActionMapper (31 mappings) | No | None | Low | Leave as-is |
| 3 | _detect_* methods (13 methods) | Yes (retiring) | Medium for STATUS/PRIORITY | Medium | Fix when #925 lands |
| 4 | MODEL_CONFIGS | No (fixed in #940) | None | Low | Leave as-is |
| 5 | Response formatters (52 methods) | Partial | Low-Medium | Low-Medium | Ensure is_generic_response coverage |
| 6 | Workflow Dispatcher | No | None | Low | Leave as-is (good architecture) |
| 7 | ConversationHandler | Partial (justified) | Low | Low | Clean dead code in M2 |
| 8 | Generic signatures (7 entries) | No (anti-inversion) | Low | Low | Remove when migration complete |

## Key Insight

The Action Gate (#911) has already defused the inversion pattern for most categories. The remaining risk is concentrated in STATUS and PRIORITY, which still trust the pre-classifier + _detect_* methods without LLM involvement. #925 (STATUS/PRIORITY floor-first) is the keystone fix.

## Specific Findings

### PreClassifier
- 644 regex patterns across 24 groups
- Acts as hard gate: confidence always 1.0, LLM never sees matched queries
- Overlapping patterns between groups (CALENDAR vs TEMPORAL, PRIORITY vs GUIDANCE) with ordering-dependent disambiguation
- Mitigated by Action Gate for IDENTITY, DISCOVERY, TRUST, MEMORY, GUIDANCE, CONVERSATION, TEMPORAL (non-date)
- Still active for STATUS, PRIORITY, EXECUTION, PORTFOLIO

### Response Formatters
- 52 _format_* methods generate template content without LLM
- Safety net: is_generic_response flag + _GENERIC_CANONICAL_SIGNATURES
- Coverage gap: only 6 of 52 formatters set is_generic_response
- Mostly moot once remaining categories migrate to floor

### ConversationHandler
- Greeting stays canonical (justified: calendar side effects)
- RESPONSES dict for farewell/thanks/chitchat is dead code (Action Gate routes these to floor)

## Recommendations for M2

1. **#925 is the priority**: STATUS/PRIORITY floor migration eliminates the primary remaining inversion
2. **After #925**: _detect_* methods become dead code — clean up
3. **After #925**: _GENERIC_CANONICAL_SIGNATURES become unnecessary — remove
4. **Monitor**: PreClassifier confidence 1.0 gating — consider < 1.0 for fuzzy matches + LLM confirmation in M2c
5. **Clean up**: ConversationHandler dead RESPONSES dict, CLAUDE_OPUS naming mismatch
