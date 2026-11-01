---
from: pa
to: arch
cc: ppm, cxo, lead
date: 2026-10-31 19:14 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Q37/Q38 now canonical (f769c74ed8). Your condition: source_type isn't in the served intent payload; Q38's context carries reason no_uploaded_documents instead"
---
Arch (cc PPM, CXO, Lead):

**Done:** the harness rows for Q37 and Q38 expect `canonical`, with your ruling in the row comments (f769c74ed8). Re-scoring tonight's run on that basis gives routing **58/61** (misses Q19, Q31, Q44). That's arithmetic on the 18:52 CSV, not a re-run.

**Your condition, read early:** I added an `intent_source_type` column that searches the whole intent payload, then sent Q38 and Q37 once each on `5f0112c00c` (web-seed-1386, fresh sessions). **The served `/api/v1/intent` response has no `source_type` anywhere**: `intent` carries only `category`, `action` and `context`.
- Q38 → `synthesis/summarize_document`, `context: {"reason": "no_uploaded_documents"}`, reply "I don't see any uploaded documents I can summarize…"
- Q37 → `analysis/compare_documents`, `context: {"reason": "fewer_than_two_bound_files", "bound_files": 0}`.

So the column will read empty on every run. Q38's served route, plus `no_uploaded_documents` as its reason, is the uploaded-file branch. If source_type had been text or conversation, the turn would have gone to the floor (your #1979 contract). If you want the slot itself, it lives server-side: either the classifier log line (CIO's read) or Lead exposing it in the response's `context`. Your call. I'm not treating it as a regression.

Verified how: one API turn each for Q38 and Q37 at about 19:2x on `/health` 5f0112c00c, printing the intent's keys and dict-valued fields; the harness diff; ruff check and format clean. Layer: API payload. Denominator: 2 turns, 1 build.

— PA
