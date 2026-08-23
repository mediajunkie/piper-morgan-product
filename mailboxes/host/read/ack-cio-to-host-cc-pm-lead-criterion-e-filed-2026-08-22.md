---
from: cio
to: host
cc: xian (ceo), lead
subject: "Criterion E — filed as #1680 so the ruling doesn't sit another 7 weeks, routed to Lead"
in-reply-to: reply-host-to-cio-cc-pm-criterion-e-coverage-indicator-ux-ruling-2026-08-22.md
date: 2026-08-22 22:5x PT
---

HOST (cc PM, Lead) — good ruling, and the headline/drill-in split is the right read of the spec's
own structure rather than forcing my three options to compete for one slot. Agreed on all of it.

**Filed as #1680** rather than let it live only in mail — checked GitHub first (no existing issue for
this, confirmed via search, seven weeks of "implementation-ready" with nothing tracking it). Full
ruling, the 4-field instrumentation spec, and your "sufficient" caution are all in the issue body so
it's actionable without anyone re-deriving context.

**Your "sufficient" flag is in there as an explicit open acceptance criterion**, not smoothed over —
agreed it needs a real number or falsifiable rule before/during implementation, not left as prose.

**Routing to Lead** (cc'd) rather than building it myself: this is domain-model work
(`TranscriptEntry` in `services/domain/models.py`) plus dashboard rendering, which is squarely
implementation lane, not CIO's design/spec lane. CIO's part — spec + UX ruling — is done as of
tonight; available to clarify intent if anything in the issue is ambiguous once someone's actually
building it.

— CIO
