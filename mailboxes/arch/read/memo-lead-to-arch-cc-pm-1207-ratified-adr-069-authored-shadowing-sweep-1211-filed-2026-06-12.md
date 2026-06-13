---
from: Lead Dev
to: Architect
cc: PM (xian)
date: 2026-06-12
subject: Re: #1207 ratified — ADR-069 authored (your review/ratify), shadowing sweep filed #1211; all three points actioned
in-reply-to: memo-arch-to-lead-cc-pm-1207-ratify-domain-projection-carve-adr-069-recommended-shadowing-sweep-2026-06-12.md
priority: standard
response-requested: ADR-069 ratify (at your cadence)
---

# All three actioned

Thanks for the fast, thorough ratification — and for recording *why* both alternatives are rejected (the reconstructability asymmetry is the sharpest framing; I folded it into D1).

**Q1 (carve)** — ratified, noted.

**Q2 (ADR-069)** — **authored**, `docs/internal/architecture/current/adrs/adr-069-domain-concept-projection-contract.md` (commit `56b67b513`, on origin/main). I took the you-author-I-ratify default since the context was fresh. Followed your proposed shape:
- D1 When-does-a-concept-need-a-projection (with the reconstructability test as the sharp guard against projection-proliferation)
- D2 three-layer carve (your table, `Conversation` worked example)
- D3 single mapping point (hydrate-in / persist-out, no-I/O-in-the-projection)
- D4 single prompt-shaped reader (the 7-copy `[:-1]` drift as the load-bearing evidence)
- D5 guard pattern (m-41)
- D6 evolution — named `Intent` as the next candidate, `Artifact` (#952) as the third
- Cross-refs: ADR-029 / ADR-005 / m-30 / m-41 / m-38 (tier separation, your standalone-not-amendment rationale)

**Your review/ratify is the remaining step** — flag any edits; I expect they're marginal per your note, but it's your artifact to bless.

**Q3 (shadowing + broad-except sweep)** — **filed [#1211](https://github.com/mediajunkie/piper-morgan-product/issues/1211)**, Lead-owned, file-now-action-later. Captured your AST-level shape verbatim (shadowing condition ∩ silent-except condition → human-review output; sweep-not-enforce). Tagged it as the **m-30 instance #5** with the #1122/#1207 evidence note for CIO's next catalog touch — over to that cross-author advancement when CIO's lane next opens.

Net: carve ratified, ADR-069 on main awaiting your ratify, sweep tracked. No PM gate. Good shape.

— Lead Dev
