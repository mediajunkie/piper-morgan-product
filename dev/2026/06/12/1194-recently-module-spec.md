# "Recently" module spec (#1194) — good-enough, forward-compatible

**Status:** good-enough slice (PM-approved 2026-06-12); the real IA + design language is CXO-referred (home-as-start-screen memo, 2026-06-12). This spec is the contract for the slice + a seed for CXO's module/card system.

## Purpose
Surface composted reflections (Surface 6 / #1033) — learnings Piper "filed away" during quiet-hours composting — back to the user on the home surface, with reflective first-person framing. The first *reachable* home for these (they had none).

## Data contract
- Source: `HomeStateService.generate_home_state(context)` → `HomeStateResult.surfaced_insights: List[{"id": str, "text": str}]`.
- `text` is the framed reflection (`premonition.frame_insight_for_surfacing`, single-framed per the #1194 double-frame fix).
- Trust-gated: populated only for ESTABLISHED+ (Stage 3+). Marked surfaced on render (`surfaced_count++`) so a reflection shows once, not every load.

## Render (good-enough)
- A module in the Stage-3+ home area: header **"Recently"**.
- Body: a single-column stack of **little cards**, one per reflection (the framed text).
- **Empty state** (required per PM's module-defaults rule): *"Nothing to look back on yet — as we work together, I'll gather reflections here."*

## Module / card design tokens (seeded; CXO owns the real system)
Introduced as CSS custom properties so CXO's design-language pass can re-skin centrally:
- `--module-bg`, `--module-radius`, `--module-pad`, `--module-gap`
- `--card-bg`, `--card-radius`, `--card-pad`, `--card-border`
Reuses existing spacing/color tokens where present. The "module = labeled section; content = cards" pattern is the seed CXO formalizes (applies to What-I'm-seeing/Places, History, etc.).

## Out of scope (CXO referral)
Home-vs-chat split, left-nav chat, the full module set + arrangement, cross-form-factor composition, the finalized token system. This slice intentionally fits *inside* the current home.html so it converges on CXO's eventual IA rather than pre-empting it.

## Refs
#1194 (this), #1033 (Surface 6), #419 (home-state design, closed), #1195 (unwired surfaces incl. Places), CXO referral memo 2026-06-12.
