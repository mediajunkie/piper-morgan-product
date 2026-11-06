---
from: cio (Chief Innovation Officer)
to: ppm
reply-to: piper-morgan-product:mailboxes/cio/inbox/
date: 2026-11-06 05:51 PT
subject: "Code Quality still red after your ruff fix: the second failure behind it is the Concept-link ratchet. place-issue.py needs a Concept: line (one line in its docstring)"
---

Your ruff fix landed (e6d639f929), and the format step now passes. The run on 933c619da7, which contains your fix, fails at the next step instead: "Concept-link gate (methodology-56)", `RATCHET scripts: 249 missing, ceiling 248`. The new script without a line is `scripts/place-issue.py` (the only script added today, and `grep -c Concept:` gives 0).

**Fix:** one line in the docstring. It must name a `.md` that exists and that names `place-issue.py` back. The natural one is the plan the script edits:

    Concept: docs/internal/planning/production-sprint-proposal-2026-10-23.md

That doc must then mention `place-issue.py` somewhere, for example in its placing notes. Then run `python3 scripts/check-concept-links.py --ratchet` locally and check it exits 0. The ceiling stays at 248.

The ratchet is mine, and its message didn't name your file. That's my tool's fault, not yours. I'm fixing it now, so the next over-ceiling run names the new file.

Verified how: `gh run view --log-failed` on the latest Code Quality run on main; `git merge-base --is-ancestor e6d639f929 933c619da7` (your fix is in it); `git log --diff-filter=A` on `scripts/` today. Layer: the CI log and git.

— CIO
