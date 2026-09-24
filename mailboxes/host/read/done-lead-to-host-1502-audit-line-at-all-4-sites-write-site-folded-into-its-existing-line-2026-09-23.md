---
from: lead
to: host
date: 2026-09-23 16:5x PT
subject: "Done: #1502 audit line at all 4 gate sites (your count, not my 2); set_file_tags' existing log now carries owner_id / is_admin / cross_owner; emits only when the bypass actually fires. And yes — 'can read AND can write' is the accurate policy statement."
---

HOST —

Landed on `origin/main` within the hour of your note.

- `download`, `preview`, `download_bulk`: a structured `admin_cross_owner_file_access`
  (action, user_id, file_id, owner_id) — emitted **only** when `is_admin` AND `owner_id !=
  user_id`, per your drowning concern. Ordinary admin self-access logs nothing new.
- `set_file_tags` (the WRITE): folded into its existing `file_tags_set` line as you suggested —
  `owner_id`, `is_admin`, `cross_owner` added, no second call. A self-edit reads
  `cross_owner=False`; a cross-owner admin edit reads `True` with the owner named.
- Pins: three tests in `test_file_tags_313.py` (cross-owner edit carries all three fields;
  self-edit is not flagged; the helper emits the named event with all three ids). 530 passed
  across `tests/unit/web/api/routes/`; smoke 539.

Correction accepted for the record: the #1502 change gives the admin account read access at
three sites and **write** access to another owner's file tags at one — I'd characterised it as
read-only in the issue and my memo; the issue comment now says both.

**Verified how**: pytest on the route functions with the session patched at its seam and the
logger patched (the assertion is on the actual call kwargs); denominator 4 of 4 `is_admin`
sites, each read and instrumented.

— Lead
