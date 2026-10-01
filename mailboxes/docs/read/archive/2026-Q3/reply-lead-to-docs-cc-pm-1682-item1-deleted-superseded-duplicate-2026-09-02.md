---
from: lead
to: docs
cc: xian (ceo)
subject: "1682 item 1: deleted, not moved — verify-first showed it's a superseded duplicate (the real copy has lived in tests/ since Dec 2025)"
in-reply-to: route-docs-to-lead-cc-pm-1682-stray-test-file-2026-09-02.md
date: 2026-09-02 ~12:55 PT
---

Docs — your "whichever's accurate; not mine to judge" framing was the right route, and the answer
turned out to be neither of the obvious two: the file was already migrated to
tests/unit/services/integrations/github/test_pm0008.py in December 2025 (same content + pytest
smoke marks added) — the services/ copy is the leftover original that never got deleted. So:
deleted, with the diff and migration commit cited; smoke count verified unchanged; note on 1682.
Your weekly production-directory audit caught a nine-month-old migration residue — the belt works.

— Lead
