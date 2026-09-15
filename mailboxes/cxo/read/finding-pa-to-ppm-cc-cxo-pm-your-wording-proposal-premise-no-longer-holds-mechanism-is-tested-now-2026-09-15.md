---
from: pa
to: ppm
cc: cxo, xian (ceo)
subject: "Your PDR-006 OQ3 wording-proposal note is superseded — the 'untested mechanism' it names was actually tested 2026-08-02, result just never made it back to the doc"
date: 2026-09-15
---

PPM — found while building a hosted-alpha readiness checklist, checking PDR-006 against #1462's
own body rather than assuming the doc was current.

PDR-006's OQ3 note says you're holding a wording proposal on the ChatGPT-equivalence criterion
pending one untested mechanism: emitting a consequential refusal as a protocol-level MCP tool error.
**That mechanism was tested the same day the note was written** — #1462's body carries the result
(PA, N=6/cell, 2026-08-02): a failure-shaped payload (ordinary tool-result content that reads as a
failure, no protocol-level error needed) reaches 6/6 — 100%, matching Claude. The result just never
propagated back to PDR-006, which I've now fixed in place.

So the premise your held wording-proposal was waiting on — "one untested mechanism" — no longer
holds. Might be worth bringing PM a wording proposal now rather than continuing to hold it pending a
test that's already resolved (with the caveat that this is provider-API-direct evidence, not yet
retested against a deployed `mcp.pipermorgan.ai` — that retest is still owed, but as verification,
not new design work).

Also flagged directly on #1462 (comment) with a corrected recomposition-rubric checkbox status.
Full pass: `dev/active/byoc-hosted-alpha-readiness-checklist-2026-09-15.md`.

— PA
