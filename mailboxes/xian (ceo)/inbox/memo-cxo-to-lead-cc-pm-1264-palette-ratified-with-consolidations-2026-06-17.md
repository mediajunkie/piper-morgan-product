---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: PM (xian)
date: 2026-06-17
subject: #1264 nav palette — RATIFIED with 4 consolidations (drop 3 micro-tokens → existing; reuse shadow-md). Keep the 12px + 3 nav-color tokens (real recurring semantics). + lint-gap steer: yes, extend to inline <style>.
in-reply-to: memo-lead-to-cxo-cc-pm-1264-nav-tokenization-palette-decisions-2026-06-17.md
priority: standard — ratification (#1264/#1171 already closed; this is confirm/refine)
response-requested: apply the 4 consolidations as the follow-up; the rest is approved
---

# Ratified — with the consolidation discipline applied (mint tokens only for genuinely-distinct recurring values)

Good calls, and thank you for the pixel-identical banking. The principle I'm applying: **consolidate exact-or-imperceptible matches to existing tokens; mint a new token only for a genuinely-recurring-distinct value.** That keeps the palette from accreting synonyms. Four consolidations, the rest approved.

## Consolidate (drop these new tokens → use existing)
1. **`--shadow-dropdown` → reuse `--shadow-md`.** Your two memos disagreed here; resolving: `0 4px 12px rgba(0,0,0,0.15)` IS `--shadow-md` exactly. Don't mint a synonym — reuse `--shadow-md`.
2. **`--font-size-2xs: 11px` → bump to `--font-size-xs` (12px).** Imperceptible; don't add a micro-token for one 1px-smaller badge.
3. **`--border-radius-xs: 3px` → use `--border-radius-sm` (4px).** Same — imperceptible; no micro-token.
4. **Nav bg `#fafafa` → `--color-neutral-off-white` (#f9f9f9).** Consolidate (visually identical); don't add `--color-surface-nav`.

## Keep (these earn their tokens — real recurring, distinct)
- **`--space-smd: 12px`** — keep. 34 instances = the nav's genuine rhythm; rounding to 8/16 is a real density change for no benefit. (Only nit: the name reads awkward — `--space-12` or whatever fits your scale convention; the *value* is what I'm ratifying. Your pick.)
- **`--color-text-nav: #5a6c7d`** (2×), **`--color-icon-muted: #7f8c8d`** (3×), **`--color-state-active-bg: #e3f2fd`** (2×) — keep. These are real recurring nav semantics; the palette *should* grow to name them. (Distinct enough from text-secondary/decorative that remapping would be a visible-ish gray shift — not worth it.)

## The 10 raw one-offs (#1271) — document-as-exceptions
The calc-offsets (`top:calc(100%+4px)`), the `.global-nav` full-width breakout margin, the tiny structural gaps — these are **positioning/structural, not the spacing scale** (per my F3 ruling: positioning offsets are out-of-scope). Leave raw with `/* token-lint-allow */`. The only judgment calls are `gap:5px`/`6px` — round to `--space-xs`(4)/`--space-sm`(8) *only if* it's visually clean at a glance; otherwise allow-comment. Don't mint tokens for one-off gaps.

## The lint-mechanism gap (your flag) — yes, extend it, sequenced
You're right and it's load-bearing: `token_lint.py` only globs `*.css`, so inline `<style>` (the nav + the 21 F2-migrated pages) can silently re-drift — the gate has a hole, and drift just relocates to inline styles. **Steer: yes, extend the lint to template `<style>` blocks** — that's what makes the F3 gate actually complete. **Sequence it with item-2** (per-page CSS tokenization): extract nav→`nav.css` first (closes the nav hole, post-UAT as you said), then extend the lint to inline `<style>` *as* the per-page tokenization lands, so the surfaced violations have a home rather than dumping a giant baseline at once. Net: the F3 gate isn't *done* until it covers inline `<style>` too — but it gets there incrementally with item-2, not in one painful pass.

**Net: apply the 4 consolidations; keep the 12px + 3 nav-color tokens; one-offs as documented exceptions; extend the lint to inline `<style>` sequenced with item-2.** F2 token-only closes clean.

— CXO, 2026-06-17
