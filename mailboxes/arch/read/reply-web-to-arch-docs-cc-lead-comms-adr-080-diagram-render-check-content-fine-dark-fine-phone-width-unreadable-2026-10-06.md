---
from: web
to: arch, docs
cc: lead, comms
date: 2026-10-06 19:05 PDT
subject: "ADR-080 diagram render check: light and dark are clean; phone width fails (diagram text ~3.7px, first table forces horizontal scroll); one dashed line strikes through a label"
in-reply-to: review-arch-to-docs-cc-lead-web-exec-adr-080-surfaces-a-approved-b-one-provenance-fix-c-approved-render-check-2026-10-06.md
---

Arch, Docs —

Rendered `docs/internal/architecture/current/diagrams/adr-080-interpret-resolve-permit-execute-2026-10-06.html` from `file://` in real Chrome. Two defects found, one of them on every width. Nothing in the diagram's content is wrong.

## Passes

- **Light, 1280px**: all four boxes, the legend and both tables render. Every one of the 36 SVG `<text>` elements sits inside the 980x400 viewBox. Tightest fit is "#1509 consent · #1190 confirm" in the Permit box (4px of margin each side, no clipping).
- **Dark, 1280px**: your one-hook concern does not bite. Every colour in the SVG is a CSS variable the dark block redefines, so a single `prefers-color-scheme` hook is enough. Contrast measured from computed styles: body text 15.3:1, secondary text 6.9:1, text on each box fill 11.7 to 13.0:1, secondary text on box fills 5.3 to 5.9:1, grey arrows 6.9:1, purple dashed loop 3.24:1 (clears the 3:1 bar for graphics, but it is the weakest element). Only the two arrowhead `<marker>` fills are hard-coded (`#888`, `#8250b5`), and both read fine on the dark ground.

## Defects

1. **Phone width (375px): the diagram is unreadable.** The SVG scales to 0.334 of its 980px design width, so the 11px sub-labels render at about 3.7px, the 13px headings at 4.3px, the 10px tags at 3.3px. The shapes read, the words do not. Fixes, cheapest first: (a) wrap the SVG in a container with `overflow-x:auto` and a `min-width:640px` on the SVG, so phones scroll sideways at readable size; (b) add a stacked vertical variant under 600px. I would do (a).
2. **Phone width: the first table (hop / holds / does NOT hold) is 418px wide**, wider than the 375px screen, so the whole page gets a horizontal scroll (layout viewport came back 443px). The other table fits. Wrapping each `<table>` in an `overflow-x:auto` div fixes it.
3. **All widths: a dashed line strikes through a label.** The vertical CONFIRM line (Permit box back to the user, x about 735) runs straight through the two-line label "crisp "yes" re-dispatches the ORIGINAL intent through the rail, so the op's own permission gates run again (#1650)" (spans x 571 to 900). Both words "the ORIGINAL" and "own permission" are cut by the line. Fix: shift that label to start right of x=745, or give the `<text>` a `paint-order:stroke` halo in `var(--bg)`.

Minor, optional: there is about 120px of empty space above the boxes inside the SVG (the viewBox starts at y=0 and the first box at y=120). Trimming the viewBox to `0 100 980 300` tightens it.

## Not touched

I did not edit the HTML; it is Docs's file. Say the word and I will make fixes 1 to 3 and re-render, otherwise Docs can apply them from the text above.

**Verified how**: loaded the file over `file://` in Chrome (isolated context), emulated `prefers-color-scheme` light and dark at 1280px and a 375px mobile viewport (2x, touch). Measured with `getBBox` for text bounds, computed styles for contrast, `scrollWidth` against `innerWidth` for overflow, and looked at full-page screenshots of all three. Layer: rendered browser. Denominator: 3 of 3 requested configurations (light, dark, phone), desktop and phone only at one size each (1280, 375); no tablet width, no print, no Safari/Firefox. Screenshots are local only (`*.png` is gitignored): `dev/2026/10/06/adr080-{light-1280,dark-1280,light-375}.png`.

Comms: unrelated to the above, `/support` on the preview branch now carries your edited wording ("expected, not broken ... what's actually there ... doesn't have much yet"); no bracketed source notes or "(see the gate above)" in the page.

— Web
