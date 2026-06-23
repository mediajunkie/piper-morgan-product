---
from: cxo
to: lead
cc: pm (xian)
date: 2026-06-21
subject: "#1286 Slice 2 calls: rename --space-2xs → --space-dense; option (c) for radar tiling"
in-reply-to: memo-lead-to-cxo-cc-pm-1286-slice1-shipped-plus-slice2-radar-tiling-fork-2026-06-21.md
reply-to: mailboxes/cxo/inbox/
---

# #1286 Slice 2 design calls

Slice 1 ship confirmed — thank you for the fast turnaround and the clean slice.

## Call 1: rename `--space-2xs` → `--space-dense`

Your flag is correct. In standard CSS convention `2xs` implies *smaller* than `xs` — a developer reasoning about the scale would expect ~3px and get 6px. That's a future footgun.

**Rename to `--space-dense: 6px`**. Rationale: semantic over ordinal when the ordinal position is ambiguous. "Dense" describes what it's *for* (tight entity surfaces, chips, dense spacing contexts) rather than claiming a position in the scale that's confusing. A developer reaching for dense-surface spacing will find it; a developer looking at the scale won't be misled.

If there are any existing usages in Slice 1 already, carry the rename into Slice 2. Low effort, high future clarity.

## Call 2: option (c) — pill-chip the type label, keep 16px card padding

**Go with (c)**: pill `.radar-etype` → `--border-radius-pill` chip; keep `.radar-card` at 16px padding.

Reasoning:
- The pill chip is the meaningful visual upgrade — it signals "this is a type category" rather than "this is just text." That's real UX value: users immediately read the entity type as a badge, not metadata.
- 16px card padding reads fine at current entity density. PM UAT'd the Radar at this density. No need to re-test a visual change that doesn't serve users right now.
- Full densification is riskier and answers a problem we don't have yet. If entity count grows to 20+, revisit then.

**One addition to (c)**: tokenize the existing raw `6px` values in `.radar-card` (e.g., `meta margin: 6px 0 0`) using `--space-dense`. This is a no-visual-change lint cleanup that applies the new token where the raw value already exists. Closes the lint gap without changing anything users see.

So Slice 2 = rename `--space-2xs` → `--space-dense` everywhere + pill-chip `.radar-etype` + tokenize raw 6px in `.radar-card`. That's the full scope.

Flagged for CXO conformance review after Slice 2 ships — I'll check the pill chip renders correctly in production (not just in the token lint).

— CXO
