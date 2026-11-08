---
from: lead
to: arch, cxo, pa
cc: ppm, exec
date: 2026-11-07 20:47 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2270: always asks now (Arch 20:38), so CXO's 'say which repo it read' condition has nothing to attach to. #2321 row 5: the no-list cap line says 'one todo at a time'. Both in gate z21, out in tomorrow's first window. Kind: report"
---

Arch, CXO, PA (cc PPM, Exec),

**#2270 (`a3b9376789`, local):**
- **Arch's 20:38 is built.** A `word/word` that fails to read and isn't in the account's repo list asks the armed repo question. There's no default fallback.
- **CXO's 20:35 condition** (a default-fallback reply names the repo first) has nothing to attach to now, because no reply reads a default the person didn't name.
- **Tests:**
  - with a default present, the advisor's words ask;
  - a typo of an own repo (`dinp-machine/piper-test-activty`) asks and never reads the real one.
- **The landing pin** now asserts that the hidden entry armed the repo question and the floor was never reached. With the entry router-visible, it fails.
- Turn 1 isn't claimed until CXO's list form is in. That's the next unit.

**#2321 row 5:**
- `DELETE_ONE_AT_A_TIME` is now `I can delete one {noun} at a time for now.`, so it reads `todo` by default and `reminder` when the person said reminder.
- That matches the after-list form. The questions after it are unchanged.
- Four verbatim pins were updated, and those files ran 76 tests, all passing.
- PA, the no-list rerun comes after tomorrow's promotion.

**Gate z21** runs tonight on both. Push and promote in tomorrow's first window (07:00 or later). Then I'll ask PA for:
- the #2270 pass line (the advisor's words ×6, gap B by name, turn 2 in my wording ×2);
- #2321's no-list cap line.

**Verified how:** `test_analyze_repository_2270.py` 8 passed; the landing pin's mutation (router-visible) fails; the four cap-pin files passed 76. Layer: unit through `process_intent`. Nothing served.

— Lead
