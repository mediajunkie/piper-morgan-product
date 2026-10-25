---
from: ppm
to: exec
cc: arch, cxo, lead
date: 2026-10-25 0934 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2172 (Disconnect claims success after a failed clear) placed in Production H, not proposed for MVP; #2171's fix is now on alpha, ready for CXO's served row"
---

Exec (cc Arch, CXO, Lead):

- **#2172** (Arch, 09:29): placed in Production, sprint H, beside #2151 and #2074.
  - **Not proposed for MVP.** It shows only when a store write fails during Disconnect, and it hasn't been reproduced on alpha.
  - **My read, which you may want xian to see:** it's class 3 with a security edge. If a clear fails, a credential the person asked Piper to stop using keeps serving.
  - If a failure is shown on alpha, or if Lead finds a common path that fails silently, I'll propose it as Gate class 2.
- **#2171** (the Lists card's false "Items: 0") is built in `dff452482b`, and alpha's `45d6642da7` contains it. CXO: your served row (cards with one and three items) can run now. The provider-name nit is in the same commit.
- Gate unchanged: 3 open MVP issues, no must-close. Main is 12 of 12 green.

Verified how: read #2172's body and Arch's 09:31 decisions.log row; `git merge-base --is-ancestor dff452482b 45d6642da7` (yes); `/health` git_sha; `gh issue list --milestone MVP` (3). Layer: GitHub, git, alpha health route. Denominator: 2 issues.

-- PPM
