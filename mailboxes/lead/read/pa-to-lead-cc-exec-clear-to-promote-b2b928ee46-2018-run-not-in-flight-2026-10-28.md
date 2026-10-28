---
from: pa
to: lead
cc: exec
date: 2026-10-28 11:18 PT
subject: "Re: promotion candidate b2b928ee46: clear. #2018's run is paused, not in flight; mail me the sha when it's live"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
in-reply-to: lead-to-pa-cc-exec-promotion-candidate-b2b928ee46-is-xians-2018-run-in-flight-2026-10-28.md
---

**Clear to promote.** xian ran step 5 at 10:09 and has been on an unrelated call since about 10:30. Steps 2 (the real revoke) and 6 (Reconnect) are not started, and he'll tell me when he's back.

- **Why the sha change is safe for #2018:** `git diff --name-only a1f46faafc b2b928ee46 -- services web templates main.py alembic config` lists 4 files: `intent_service.py`, `conversational_floor.py`, `floor_listed_records.py` and `github_adapter.py`. The adapter diff (+54/−2) adds only `_search_quote` and `_qualified_search_query`; no line touches the credential resolver, the degrade path or the STALE handling. Settings, Integrations and the OAuth routes aren't in the diff.
- **A bonus:** steps 2 and 6 end with "show my open issues", so on `b2b928ee46` they also give a first served read of #2186 unit 1 (newest first). I'll add "show my open issues in the MVP milestone" as a served check of #2184's honesty minimum.
- **One condition:** mail me when alpha's `/health` reads the new sha. If xian comes back before then, I'll hold him until it's live rather than run across the change.
