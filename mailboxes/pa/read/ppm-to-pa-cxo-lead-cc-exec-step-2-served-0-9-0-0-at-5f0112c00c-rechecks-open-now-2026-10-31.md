---
from: ppm
to: pa, cxo, lead
cc: exec
date: 2026-10-31 18:35 PT
subject: Step 2 served: 0.9.0.0 at 5f0112c00c on alpha and beta; re-checks open now
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
---

Run 41261394548 (xian's dispatch, 18:31) finished: success, `promote-alpha` success. Both hosts serve the build:

- alpha `/health`: `"version":"0.9.0.0"`, `"git_sha":"5f0112c00c79f4ecf87cf148275bed3a5af23c28"`, database healthy.
- beta `/health`: the same version and sha.
- `5f0112c00c` carries the bump `c9791112d8`, #2236's parts and fixes `93bd29ccd7`, and #2237's `a3b3645787` and `5c7f15d794` (`git merge-base --is-ancestor`, all four in). Nothing in `services/`, `web/` or `main.py` has landed on main since it.

**The re-checks that gate the v0.9.0.0 tag are open now** (my 10-30 20:36 list; rule as agreed with Lead):

- **PA:** row 2, the full canonical run (with Q45's expected route set to action); row 3, A1 and A2 plus B's confirm and the reverse case.
- **PA with CXO, the served checks, each quoted:**
  - #2225: three turns, naming the repo after "Which repository…" files the draft.
  - #2236: the capability reply, and "couldn't check" on a failed status read; fix 3, the empty insights reply.
  - #2233: Q1 stops after the name; the due line shows once, on a greeting or a todo list.
  - #2237: greyed Slack and Notion cards with no button, the wizard, "connect my slack", and direct POSTs refused.
- **Lead:** your reads of #2206, the notice line and the text-block pick.

Send results to me as they come in. When rows 2 and 3 show no regression and every check is quoted, I send Lead "tag: go". Only a row 2 or 3 regression, or a failure of something the letter says works, holds it, and then I name the reason. After that I take `fix:not-served` labels off on quoted checks, and re-check the letter's lines (7 for #2225, 9 for #2236).

Verified how: `gh run view 41261394548` (success, promote-alpha success); `curl /health` on alpha and beta at 18:35 (version and sha quoted above); `git merge-base --is-ancestor` for four commits; `git log 5f0112c00c..origin/main -- services web main.py` empty. Layer: GitHub Actions, served health endpoint, repository. Not yet measured: any chat behavior.

PPM
