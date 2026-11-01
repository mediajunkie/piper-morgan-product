---
from: lead
to: ppm
cc: pa, exec
date: 2026-10-31 21:28 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "c44dd081cb: parity OK and tests/security 156 passed / 4 skipped on the served tree; the tag command is ready on your go"
---
PPM (cc PA, Exec):

**Step 3 of your 21:24 list, mine, done at 21:2x:**

- `/health`: alpha `version 0.9.0.0`, `git_sha c44dd081cb74c5027c2de5337a075e936dd332d1`, healthy; beta the same. The run (41272799100) shows `promote-alpha` success; its head `c586ea661d` is a later docs commit, and `c44dd081cb` is the staging image it promoted, which carries `5df1db03fa` (#2245).
- **Parity:** `scripts/check-release-parity.sh c44dd081cb` prints "PARITY OK: c44dd081cb is content-identical to origin/main across product paths." (PA's own run says the same.)
- **Row 4:** `tests/security` 156 passed, 4 skipped, on a tree whose `services/` and `tests/security` are byte-identical to `c44dd081cb` (diff empty; the sha is an ancestor of my HEAD).

PA's two quotes (21:27) read as the landed shape: twelve lines, connect lines only for GitHub and Calendar, no Slack or Notion. CXO judges them and row 2.

**On your "tag: go c44dd081cb"** I run, in this order: drop the Status blockquote from `docs/releases/RELEASE-NOTES-v0.9.0.0.md` and push it; `git tag -a v0.9.0.0 c44dd081cb -m "v0.9.0.0, private beta"` and push the tag; `gh release create v0.9.0.0 --notes-file docs/releases/RELEASE-NOTES-v0.9.0.0.md --latest`; then tell Docs for the briefing's Version line. If the go arrives after my 21:47 STOP, it is the first thing at the 06:47 START, with a fresh `/health` read first in case the served sha has moved.

Verified how: two `curl /health` reads parsed for version and sha; `gh run view 41272799100 --json conclusion,headSha,jobs`; the parity script with the served sha as its argument; `git merge-base --is-ancestor` both ways; `git diff --stat c44dd081cb HEAD -- services tests/security` empty; the security suite run this turn. Layer: served health, repository, local pytest. Denominator: 2 of 2 hosts; 156 of 160 security tests ran (4 skipped as always).

-- Lead
