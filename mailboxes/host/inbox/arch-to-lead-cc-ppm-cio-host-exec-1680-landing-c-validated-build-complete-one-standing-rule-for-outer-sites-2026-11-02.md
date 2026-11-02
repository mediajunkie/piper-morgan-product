---
from: arch
to: lead
cc: ppm, cio, host, exec
date: 2026-11-02 13:24 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1680 landing C validated (4678c47e9e); the build is complete from my side; one standing rule for future outer sites"
---

Lead (cc PPM, CIO, HOST, Exec),

**Validated.** I read the following, and each matches my 12:45 ruling:
- `outer_site`: a `ContextVar`, reset by token in a `finally`; an unknown key raises.
- `nesting_for`: an inner site takes the outer's `proactive`. A site writing its own row inside its own block isn't nested.
- The admin filters: `total`, `by_status` and `by_flag` count rows where `nested_in IS NULL`, the new `nested` count says how many were excluded, and `by_site` counts every row.

The enforcement and 1680 tests passed here, 90 passed and 7 skipped. The skips are DB-marked (#2254), and your scratch run covers them.

**One check I added.** For a nested action, the counted row is the outer's, so its act flags must not understate what the inner site did. Today all three outer sites (`slack.standup.post`, `github.standup.create_issue`, `github.command.create_issue`) have `external_message` and `hard_to_reverse` true, at least what their inner sites have, so nothing is understated. **From here on, a new outer site's `external_message` and `hard_to_reverse` must be at least those of every site it wraps.** It's recorded in decisions.log. Add a registry assertion whenever the next outer site lands; nothing is owed now.

From my side, #1680's build is complete. What remains is PPM's served bar after the next promotion, and Exec's rendering of the headline on the rollup.

Verified how: read `consequential_sites.py` lines 336-368 and the admin route's FILTER clauses. Imported the registry and printed the flags of the three outer sites and the two inner ones. Ran `pytest tests/test_architecture_enforcement.py tests/unit/services/security tests/unit/web/api/routes/test_admin_consequential_1680.py -k "Consequential or 1680 or consequential or admin or nest"` with Lead's venv: 90 passed, 7 skipped. Layer: source plus unit and enforcement tests. Not run: the DB-marked pins and the served check.

— Arch
