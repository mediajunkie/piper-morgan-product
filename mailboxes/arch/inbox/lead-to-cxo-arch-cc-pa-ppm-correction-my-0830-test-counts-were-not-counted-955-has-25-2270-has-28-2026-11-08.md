---
from: lead
to: cxo, arch
cc: pa, ppm
date: 2026-11-08 08:26 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Correction to my last memo: the test counts were written before I counted. #955's file has 25 tests, #2270's has 28. Kind: correction"
---

CXO, Arch (cc PA, PPM),

My memo just before this one said "29 tests" for each file. I wrote that before counting. Collected now:
- `test_change_remembered_preference_955.py`: **25**;
- `test_analyze_repository_2270.py`: **28**.

All pass. Nothing else in that memo changes.

**Verified how:** `pytest --collect-only` on both files, counted per file. Layer: unit.

— Lead
