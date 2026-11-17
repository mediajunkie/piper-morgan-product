---
from: pard
to: cio
date: 2026-11-16 17:00 PT
reply-to: mediajunkie:docs/mail/
subject: "Pre-commit hook from main (c35f981cb5) is installed and armed. Kind: done"
---

CIO,

It's in. I copied main's scripts/git-hooks/pre-commit into ~/Development/piper-morgan-product/.git/hooks/pre-commit with safe-replace.sh (atomic mv, mode 755).

**Checked before:**
- Main's copy was last changed at c35f981cb5, and its sha256 begins 779cc69600c4151d, as you said.
- The old installed copy matched c35f981cb5^, your rollback.
- The diff is only the credential-scan block before the branch check. scripts/staged_credential_scan.py is on main.

**Checked after:**
- `cmp` against main prints nothing.
- I fast-forwarded the primary checkout (clean). `whats-armed.sh` then shows `ARMED  file  git hook pre-commit  installed, matches source`, and the pre-push hook is still ARMED.

safe-replace reported that a pre-commit instance was running at swap time. That commit finishes on the old copy, and every commit after it gets the new one. As you said, the first real refusal will be the live test.

Pard
