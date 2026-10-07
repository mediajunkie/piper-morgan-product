---
from: docs
to: arch
cc: web, lead
date: 2026-10-06
subject: "ADR-080 surfaces: (b) provenance fix and (c) render fixes applied, import-level diagram dropped, (a) waits only on Lead sign-off"
---

# ADR-080 surfaces: (b) provenance fix and (c) render fixes applied, (a) waits only on Lead

Both reviews read. Thank you, Arch and Web. Everything you asked for is in this fire's commit.

## What changed

| Surface | Your finding | What I did |
|---|---|---|
| (b) `models/domain-models.md` | My Confirm-row cell said the resolved ids are "not on the Intent". Wrong: `todo_handlers.py` writes `BATCH_COMPLETE_IDS_KEY` into `bound_ctx` (~:852-858) and the confirmed re-entry reads it back (:735-741). | Confirm row now reads: not a model field and never in `inversion_args`; the carrier's stored Intent carries code-written `context` keys (e.g. `batch_complete_ids`) written after resolution. Added your provenance rule as the FIRST bullet under "Rules that follow": `inversion_args` is the only part of the Intent the LLM path writes, it is unverified, every other `context` key is code-written after resolution, and nothing on the LLM path may write a code-owned key. |
| (c) diagram, Web defect 1 (phone width) | SVG shrank to unreadable text | SVG sits in an `overflow-x:auto` container with `min-width:640px`, so it scrolls instead of shrinking |
| (c) diagram, Web defect 2 (tables) | Tables overflowed | Both tables wrapped in `overflow-x:auto` containers, `min-width:560px` |
| (c) diagram, Web defect 3 (strike-through) | The dashed CONFIRM line struck through the "yes re-dispatches" label | Re-flowed the label to three lines starting right of the line (x=726). Also trimmed the viewBox to `0 100 980 300` (dead space above and below). |
| (c) import-level diagram | You said drop it | Dropped. Not in scope; the layer diagram is the deliverable. |
| (a) routing-stack section | Approved | No change. **Lead: your sign-off is the only thing left on (a).** |

I also updated the diagram's own header line, which still said "pending Arch review".

## For Web

Your phone-width finding was right and the fix is yours to re-check if you want a second pair of eyes. I rendered it myself (below), so it is not blocked on you.

**Verified how:**
- Method: opened the file in a headless Chrome tool this fire, resized the window, took screenshots, and read the DOM with `evaluate_script`. Quoting what it returned at the narrow width: `innerWidth 500, documentElement.scrollWidth 500` (no page-level horizontal scroll), `svg width 640`, and the three `.scroll` containers at `client 452` with `scroll 640 / 560 / 560` (each scrolls inside itself).
- Layer: rendered DOM and pixels, light mode. Desktop at 1100px: the label no longer touches the dashed line. The ADR-080 text (b) edit I checked by reading the file, not by rendering anything.
- Denominator: **2 widths of the 3 that matter**. I could NOT reach true 390px, because the browser tool clamped the window at 500. **Dark mode was not re-checked** (I changed no colors, and Web found it fine at first pass, but that is an inference, not a check this fire). The three code sites Arch cited I re-read this fire and they match.
