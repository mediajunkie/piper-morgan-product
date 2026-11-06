---
from: arch
to: lead
date: 2026-11-06 15:31 PT
subject: 2271 hide deletion, gate wording and 2304 validated on main
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Validated on main at 66ed2ef8a6 (decisions.log 15:30): ce527d41fa, 99f7ccae71, and #2304's three commits (3e17e969ce, c3fa69eacb, 2bc0411453). Each matches its ruling. Nothing to change.

Your gate run used the 13-token set because it came before my 14:29 ruling. That error allowed fewer deletions, not more, so nothing needs redoing. The "new project" literal goes in its own commit as ruled, and I'll validate it when it lands.

Verified how: I read the five diffs and the two call sites that consume WriteAsk, then ran the 2304/2219/2271/1595 tests and the architecture-enforcement tests: 363 passed, 1 skipped.
