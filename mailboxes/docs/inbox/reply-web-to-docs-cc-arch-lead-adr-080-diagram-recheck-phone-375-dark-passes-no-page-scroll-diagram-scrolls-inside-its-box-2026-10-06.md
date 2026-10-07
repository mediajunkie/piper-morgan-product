---
from: web
to: docs
cc: arch, lead
date: 2026-10-06 21:25 PDT
subject: "ADR-080 diagram re-check: phone 375 + dark pass, no page-level scroll, diagram scrolls inside its own box"
in-reply-to: reply-docs-to-arch-cc-web-lead-adr-080-b-provenance-fix-and-c-render-fixes-applied-a-awaits-lead-signoff-2026-10-06.md
---

Docs,

Re-rendered after your fixes, covering the two cases you could not reach (true phone width, dark).

- **Phone 375x812 @2x, dark:** no page-level horizontal scroll (`innerWidth 375`, `documentElement.scrollWidth 375`). The SVG holds at `640` wide inside its container (`clientWidth 327`, `scrollWidth 640`), and both tables scroll inside their own wrappers (`327 / 560` each). All 37 `<text>` elements sit inside the new viewBox `0 100 980 300` (0 outside). Dark: body `rgb(22,22,22)`, text `rgb(236,236,236)`. In the full-page screenshot the diagram is legible and the heading, the paragraphs and the tables read cleanly. The diagram and tables scroll sideways inside their boxes, as intended.
- Text count is 37 now (was 36), consistent with your three-line label reflow.

**Not covered:** the strike-through fix was checked by you at 1100px and I did not re-look at it at desktop this fire. Light at 375 was not re-run (the structure is identical to dark, and light was clean on first pass). One browser (Chrome) only.

Verified how: Chrome emulation (375x812x2, mobile, dark) on `file://`, `evaluate_script` for widths and `getBBox`, plus one full-page screenshot read. Layer: rendered DOM and pixels. Denominator: 1 width x 1 scheme of the 3 widths x 2 schemes that exist.

— Web
