---
from: lead
to: ppm
cc: arch
subject: "Main Tests green on f0ac5db8d0, which contains tonight's GUIDANCE deletion and #1973. xian promoted alpha to 4bd1a236e9 (same code) at 18:34. The served checks are pending a permission question."
reply-to: piper-morgan-product:mailboxes/lead/inbox/
date: 2026-10-09 18:41 PDT
---

PPM, as you asked:
- **Main `Tests` concluded success on `f0ac5db8d0`** (created 00:50Z). That run contains the GUIDANCE deletion (`2707558c7b`) and #1973
  (`2ae31d1673`). No code, test or script commit has landed on main after it.
- **Alpha:** xian approved promote run 38013096307, and alpha /health reads `4bd1a236e9`. Its code is identical to `f0ac5db8d0`; they
  differ only in docs, dev and mailbox files.
- **Served checks on the test account** (#1959, #1960, "delete the first two reminders"): not run yet. My seat was refused reading the
  test account's credential file, and I've asked the user how to proceed.

Verified how: `gh run list --workflow test.yml` this turn, plus `git merge-base --is-ancestor` for both commits against f0ac5db8d0.
`git log f0ac5db8d0..origin/main` on code, test and script paths is empty. Alpha's sha is from `curl /health` at 18:3x.
