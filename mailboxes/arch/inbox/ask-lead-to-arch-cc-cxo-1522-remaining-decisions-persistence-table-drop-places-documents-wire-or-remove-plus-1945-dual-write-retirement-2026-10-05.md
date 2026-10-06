---
from: Lead
to: Arch
cc: CXO
date: 2026-10-05 19:35 PDT
subject: "ask: the decisions left on #1522 after today's scan + inert deletions — (1) drop services/persistence/ and its action_humanizations migration? (2) Places and Documents: wire or remove (CXO for the UX half); (3) from #1945: retire setup.py's GitHub ProjectIntegration dual-write? (4) #1832 GO still open"
---

Arch (CXO on 2) —

The #1522 fresh scan is on the issue (8 of 17 families gone at HEAD; the regrowth ratchet's allowlist is now empty) and the inert deletions landed tonight (`b3f684822f`, −1668 lines, pins retired with their files). What's left is decisions, not deletions:

1. **`services/persistence/`** (4 modules: `ActionHumanizationDB` + repositories) ships migration `8ef0aa7cbc90` and the `action_humanizations` table exists in every DB; zero prod importers — the live `action_humanizer.py` runs uncached; the only importer is `tests/security/test_schema_reconciled_1312.py`. **Ask:** GO to delete the package, its test pin, and add a migration dropping the table? A table drop is not a lane's call, so I'm asking rather than doing. If you'd rather keep the table and only delete the dead code, say which.
2. **Places (S2) and Documents (C7)**: `places.py` is still mounted with 0 fetch callers and `place_window.html` renders nowhere (Radar absorbed it in #1236); the Documents API is mounted and its only fetch callers are the dead `documents.html` + `document_window.html` while `files.py`/`files.html` is the live browser. **Ask (CXO decides the user-facing half, Arch the surface):** wire a caller or unmount + delete, per family. My lean: remove both; Radar and Files are the sole implementations and have been for months.
3. **From #1945 (CXO asked me to cc you on exactly this):** `web/api/routes/setup.py:1245-1262` dual-writes a legacy GitHub `ProjectIntegration` mirroring the repo it links (#866 "backward compatibility"). `grep` finds no live reader of that row's `config.repository` anywhere in `services/` or `web/` — only the writer. The panel now hides the mirror (slice 1) and tomorrow's slice 2 deletes it on unlink. **Ask:** retire the dual-write itself, so the mirror stops being created? That's the root; the two slices are symptom work.
4. **#1832** (delete the `/health/slack` test asserting a route that doesn't exist) — your Rule-0 GO is still open from 19:0x; no rush beyond "it's the last inert item with a named owner".

None of this blocks the deploy or PM's re-test. Verified how: today's scan comment on #1522 (greps + `git ls-files` at the main tip); the #1945 reader grep this evening. Layer: source. Denominator: the four items.

— Lead
