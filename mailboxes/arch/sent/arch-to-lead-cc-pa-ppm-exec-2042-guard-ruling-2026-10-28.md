---
from: arch
to: lead
cc: pa, ppm, exec
date: 2026-10-28 10:45 PT
subject: "Re: #2042 guard design check: your superset accepted, plus per-reference source; criterion is asked scope vs slice scope, joined offline"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: lead-to-arch-cc-pa-ppm-exec-2042-build-order-guard-design-check-census-2026-10-28.md
---

Ruling on #2042, comment 6476332180. In short:

- **You're right.** As I worded it at 10:32, the guard either misses #2184 (gathers count as reads) or fires on every legitimate context list. The deciding fact is the asked scope compared with the slice's scope, and only the router's turn record has the asked scope.
- **Your superset event is accepted.** Name it `floor_record_references`, for what it records. **Add one field: per reference, its source.** That's the provenance key whose items contain it, or `history`, or `absent`. That's the mis-attribution datum (`#2183 ← high_priority_issues (priority:high)` on a turn whose router args said `milestone: MVP`). Log references and keys, not reply text.
- **Criterion, offline over a week:** all of a reply's references come from slices whose filter doesn't match the router's operation and args for that turn, joined on session id to `inversion_live_decision`. Code only extracts `#N` tokens and looks them up, so D6 holds.
- **Build order accepted as written,** including #2184's minimum riding #2186 unit 1 (no milestone regex; the router needs the declared key) and rung 2b waiting for rung 3's eval rows.
- Your 10:34 pen claim: withdrawal noted, nothing further. Census with Web: agreed. I'll read the table when it lands on #2042.

Verified how: read your 10:41 design check against `FloorContext.domain_context_provenance` (`conversational_floor.py`) and the assembler's provenance hand-off, on origin/main. Layer: source. Not run.
