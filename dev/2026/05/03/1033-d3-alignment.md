# #1033 — D3 Spec → Implementation Alignment

**Date**: 2026-05-03
**Author**: Lead Developer
**Specs read**: `docs/internal/design/mux/composting-experience-design.md` (D3) + `docs/internal/architecture/current/lifecycle-experience-guide.md`

---

## Summary

D3 spec is well-aligned with existing implementation. Reflection-language helpers (`COMPOSTING_FRAMES`, `SURFACING_FRAMES["reflection"]`) and the framing function (`frame_learning`) already cover D3's "Language Patterns" section. The COMPOSTED state's experience phrase ("I learned that...") is wired into `LifecycleState.experience_phrase()` per the lifecycle-experience-guide.

**No scope-expanding gaps surface from this read.** #1033 work proceeds as planned: anti-surveillance regex guardrail + 10-probe regression set + integration into the existing framing helpers.

---

## Spec → Implementation Map

| D3 requirement | Implementation status |
|---|---|
| Reflection openers ("Having had time to think about it...", etc.) | ✅ `COMPOSTING_FRAMES` at `services/mux/composting_scheduler.py:34-47`. Spec lists 5; code has 7 — superset. |
| `frame_learning(learning)` random-pick + de-duplication | ✅ at `services/mux/composting_scheduler.py:45-65` |
| `frame_insight_for_surfacing(insight)` reflection / concern / offer / correction buckets | ✅ at `services/mux/premonition.py:66+`; `SURFACING_FRAMES` dict at line 40+ |
| COMPOSTED experience phrase = "I learned that..." | ✅ `services/mux/lifecycle.py:91` `LifecycleState.COMPOSTED`'s `experience_phrase` |
| Quiet-hours scheduling (default 2-5 AM) | ✅ `CompostingSchedule` at `services/mux/composting_scheduler.py:74+`; default `quiet_hours=[2,3,4]` |
| Anti-surveillance language enforcement | ❌ NOT IN PLACE — this is #1033's primary deliverable |
| Anti-surveillance regression test set (~10 probes) | ❌ NOT IN PLACE — #1033 builds it |
| Confidence expression bands (high/medium/low → "I've noticed" / "It seems like" / "I'm not sure but") | ⚠️ partial — `SURFACING_FRAMES` has reflection frames; explicit confidence-banded language is a #1030 (Pull mode) concern, not this issue. Out of scope per #1033 Q1 (Option C: framing layer + guardrail only). |

---

## D3 Anti-Pattern → Forbidden Phrases

The spec's "Anti-Patterns: What NOT to Do" section names specific surveillance phrases. Mapping to regex patterns for the guardrail:

| Spec anti-pattern | Regex pattern (for `services/mux/anti_surveillance.py`) |
|---|---|
| "I've been watching..." | `\bI'?ve been watching\b` |
| "While you were away..." | `\bWhile you were away\b` |
| "Based on my surveillance of..." | `\bBased on my surveillance\b` |
| "While monitoring your activities..." | `\bI'?ve been monitoring\b` / `\bmonitoring your activit` |
| "I observed..." (in surveillance context) | `\bI observed\b` (note: borderline; D3 spec calls it surveillance phrasing) |
| "I've been tracking..." | `\bI'?ve been tracking\b` |
| "I detected a pattern..." | `\bI detected (a |the )?pattern\b` |
| "Based on your behavior at [time]..." | `\bBased on your behavior at\b` |
| "After analyzing your data..." | `\bAfter analyzing your data\b` |
| "My analysis shows..." | `\bMy analysis shows\b` |

**Q3 strictness disposition**: regex match → reject output → fall back to "I don't have anything to share right now"; violations logged.

---

## Q4 Test Strategy

Per audit walkthrough: **unit + regex coverage for MVP**; LLM-end-to-end behavior tests deferred to AAXT-layer follow-up (separate scope).

So #1033's tests are:
- Unit: each forbidden pattern matches expected strings + doesn't match safe variants
- Probe set: ~10 hand-curated probe strings, each labeled "should pass" / "should reject," runnable in CI deterministically (no LLM call required for the guardrail itself)
- Integration: `frame_insight_for_surfacing` + `frame_learning` outputs run through the guardrail before return

---

## Probe Set Sketch (~10 probes per Q2 disposition)

| Input scenario | Expected guardrail behavior |
|---|---|
| "Having had some time to reflect, you tend to front-load smaller tasks." | PASS — D3 reflection opener, no surveillance phrase |
| "Looking back on our recent work together..." | PASS — D3 temporal framing |
| "Something occurred to me..." | PASS — D3 reflection opener |
| "I've been watching your meeting patterns and noticed..." | REJECT — "I've been watching" |
| "While you were away, I analyzed your work." | REJECT — "While you were away" |
| "Based on my surveillance of your habits..." | REJECT — "Based on my surveillance" |
| "I've been monitoring your activity this week..." | REJECT — "I've been monitoring" |
| "After analyzing your data, I see..." | REJECT — "After analyzing your data" |
| "I detected a pattern in your work." | REJECT — "I detected a pattern" |
| "I noticed you do X." (no surveillance frame) | PASS (per D3 borderline; "I noticed" alone is OK; the surveillance pattern is the qualifier "while monitoring/watching") |

(Probes encoded as a JSON or Python literal in `tests/mux/probes/composted_experience_probes.json` per #1033 Phase 3.)

---

## Integration Point per Q1 (Option C)

`frame_insight_for_surfacing` (premonition.py:66) is the framing-layer entry point. After applying the framing helpers, it runs the guardrail. If the guardrail rejects, return a fallback string. Compost-time framing (`frame_learning` in composting_scheduler.py:45) does the same — guardrail runs after framing applied.

This means there's **no new surfacing entry point**; #1030 / #1031 / #1032 consume `frame_insight_for_surfacing` and get guardrail-protected output for free.

---

## Phase order (no change from gameplan)

- **Phase 2**: anti-surveillance guardrail (`services/mux/anti_surveillance.py`)
- **Phase 3**: probe set + machinery
- **Phase 4**: integration into `frame_insight_for_surfacing` + `frame_learning`
- **Phase 5**: COMPOSTED experience-phrase regression test
- **Phase Z**: handoff
