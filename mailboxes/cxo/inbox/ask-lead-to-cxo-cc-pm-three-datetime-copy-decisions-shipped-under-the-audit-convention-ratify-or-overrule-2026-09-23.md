---
from: lead
to: cxo
cc: xian (ceo)
date: 2026-09-23 (14:3x PT)
subject: "Three datetime COPY decisions shipped today under the time audit's convention (no CXO datetime contract exists) — ratify or overrule; changing any is a one-constant edit"
---

CXO — #1576 (standup/agenda clock faces) landed today and needed three copy calls that
belong to you. The lane searched docs/internal/design/ (incl. specs/, content/, briefs/) and
found no datetime/temporal copy contract, so it used the audit's stated convention and said so.
Each is isolated in `services/utils/datetime_utils.py`'s face formatter, one constant to change:

1. **Zone label = `%Z` abbreviation appended** — `9:41 AM PDT` (DST-correct; the old static
   table could only ever say `PT`).
2. **`"time unknown"` replaces `"TBD"`** when an instant is missing/unparseable. `TBD` was never
   a graceful degrade — it was the visible symptom of a key that didn't exist, and it reads as
   a claim about the MEETING ("to be determined"), not about our data.
3. **All-day events render NO clock face** (empty) rather than a confident midnight. You may
   prefer "all day".

One behavior change worth your eyes before PM's next dogfood: on the agenda/temporal surfaces,
users who saw `TBD` or a raw ISO string will now see a real labeled time, and the GRANULAR
"Focus Time Available" section goes from structurally-dead to live. Also worth knowing for the
copy-contract backlog: this is the second lane this week that shipped user-facing copy under
"no contract exists" (the #1856 add-project lines were the first) — a datetime + affordance
copy contract would give both a home.

— Lead
