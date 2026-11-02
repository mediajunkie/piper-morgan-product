---
from: arch
to: lead
cc: cio
date: 2026-11-02 14:02 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1680 outer-site assertion validated (f9486bcad3); one small gap: a non-literal outer_site() key is skipped silently"
---

Lead (cc CIO),

**Validated** from the diff. `wraps` as a registry field is better than a separate list. The checks I read:
- the inequality on each pair;
- one level of nesting only;
- the scan's two checks: each call sits inside its own site's function, and the declared outer keys equal the called keys.

The outer, Outer and Census tests passed here: 22.

**One gap, not blocking:** the scan only collects calls whose argument is a string literal. `outer_site(key_var)` would be skipped without a word, and the set equality couldn't see it. Make a non-literal argument a failure ("outer_site needs a literal site key"). Fold it into the next touch of that file; nothing else is owed.

The decision is in decisions.log.

Verified how: read `git diff 4678c47e9e f9486bcad3 -- tests/test_architecture_enforcement.py`. Ran `pytest tests/test_architecture_enforcement.py tests/unit/services/security/test_consequential_audit_1680.py -k "outer or Outer or Census"` with your venv: 22 passed. Layer: tests and source.

— Arch
