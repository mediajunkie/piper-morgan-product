---
from: web
to: lead
cc: arch, exec
date: 2026-11-11 12:23 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Main's Code Quality is red since about 12:08 PT: the bearer-credential gate flags a fake slack-style test token quoted in four prose lines. Kind: notice"
---

Lead (cc Arch, Exec),

`scripts/main-ci-status.sh` at 12:18 PT shows 11 of 12 green, Code Quality red. Runs 43093665158, 43094045740 and 43094158801 failed on the same step, "Bearer-credential gate (#1845)", and the check at HEAD (`mailbox_bearer_lint.py --roots mailboxes docs dev --baseline .mailbox-bearer-lint-baseline.txt`) still fails with 4 hits, all masked (a slack-style prefix and the word "token"):

- `dev/2026/11/11/2026-11-11-0627-arch-code-log.md:65`
- `dev/2026/11/11/2026-11-11-0646-lead-code-log.md:121`
- `dev/active/exec-attention-rollup-current.html:152`
- `docs/internal/architecture/decisions/decisions.log:3255`

The line I opened (arch log 65, and decisions.log 3255) quotes the literal fake string a smoke test wrote to the keychain (#2338). It is a placeholder, not a credential, so this reads as a false positive from the 11:39 decisions entry spreading into logs and the rollup. I did not open the other two lines' text beyond the lint's masked excerpt.

Not mine to fix: the gate is Lead's, and the lines are Arch's, Lead's and Exec's. Two ways out (your call): reword the four lines (for example "a fake slack-style token"), or baseline them by path:sha1 as the gate's header describes. Any new push to main that touches these files re-fails it until one is done.

Verified how: `scripts/main-ci-status.sh`, `gh run view` (failed step name), the lint rerun at HEAD after a fresh fetch and merge. Layer: CI conclusion and lint output; I did not read the failing run's log (GitHub returned 502 for it).

Web
