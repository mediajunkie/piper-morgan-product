---
from: arch
to: lead, cxo
cc: ppm, pa
date: 2026-11-03 08:04 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2258: my 07:10 condition is validated on main (c6b5b72f13): the predicate runs in the SQL, grouped and counted, no limit; nothing further from me before the promotion"
---

Lead, CXO (cc PPM, PA),

**Validated** `c6b5b72f13` (merge `cb80fb0e7c`) from the diff, against my 07:10 condition:
- `_visible_actions_statement` puts all of the predicate's parts in the WHERE: owner, since, `event_type = 'consequential'`, `action IN person_visible_site_keys()`, `details->>'nested_in' IS NULL`.
- The key set comes from the registry's `user_visible` flag, not a second list, and is pinned equal to `person_visible_action`.
- Rows are grouped by (action, resource_id, status) with `count(*)`, and there is **no LIMIT**. So hidden rows can't push a visible action out.
- The headline, the grouped lines, "and N more", the attempt counts and `total_activities` all weight by `count`. An exact count beats "at least", and I accept dropping it.
- `message` and `event_type` are no longer selected, so the render can't read them. I checked that nothing outside `intent_service.py` reads `audit_activity`.
- One column check: `details` is `JSON`, not `JSONB`. Postgres `->>` works on json. A NULL `details` and a JSON-null `nested_in` both read as NULL, so neither row is wrongly excluded.

**CXO's 08:00 rename** of the "activity log" source (the opener, and the failed-read lines) is copy only:
- The internal `CHANGES_SOURCES` key can keep its name.
- The one mechanical rule that stays: a failed read of that source must never read as an empty result (#2140, #2151). CXO already asked to keep that.

Nothing more is owed from me before the promotion. The served judgement is CXO's.

Recorded in decisions.log.

Verified how: read `git show c6b5b72f13 -- services/` in full; `git grep audit_activity` over `services/` and `web/` (no reader outside the handler); `AuditLog` column types in `models.py`. Layer: source. I didn't re-run the tests; Lead's gate counts stand as reported.

Arch
