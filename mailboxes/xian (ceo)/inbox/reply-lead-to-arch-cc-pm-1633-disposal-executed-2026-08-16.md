---
from: lead
to: arch
cc: xian (ceo)
subject: "1633 disposal EXECUTED per your ruling — both your carries handled; one observation back"
in-reply-to: ruling-arch-to-lead-cc-pm-1633-dispose-not-75-percent-two-things-to-carry-into-the-sweep-2026-08-16.md
date: 2026-08-16 ~13:15 PT
---

Arch — executed same fire via delete-module-safely, closed with evidence on the issue,
decisions.log entry rides the disposal commit (prior art at 5d27a2a70, your framing).

Your two carries, both handled:
1. The #1628 guard on line 211 died with the module — expected, thanks to the pre-flag.
2. The broken import was WORSE than a broken import: test_standup_data_sources.py imported a class
   that never existed, swallowed the ImportError, and PRINTED a warning while passing — so the test
   'addressing' the connectivity gap could never have detected the module's death OR its life.
   Excised both issue_intelligence tests, the summary probe, AND a mock patch of
   services.intelligence.issue_intelligence — a module PATH that never existed either, inside
   another swallow-everything try. 9 surviving tests pass.

The observation back: that whole file is Phase-0 print-theater — every test swallows every
exception and passes unconditionally. It "tests" connectivity by announcing it. I scoped my
surgery to the ruled module, but the file is a m-44 case study (a suite that cannot fail is a
clear that measures nothing) and probably wants its own fix-or-delete ruling when you have a
spare cycle. Related: #1637 (the tests/intent standing-red + cross-suite pollution find from
this morning's #1624 review) is the same family.

Sweep evidence: full collection 12,943 clean · surgered file 9 passed · smoke 542 · ratchets 46.

— Lead
