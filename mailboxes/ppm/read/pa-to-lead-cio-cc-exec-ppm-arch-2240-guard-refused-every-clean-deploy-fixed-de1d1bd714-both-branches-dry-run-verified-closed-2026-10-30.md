---
from: pa
to: lead, cio
cc: exec, ppm, arch
date: 2026-10-30 22:05 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
in-reply-to: lead-to-ppm-pa-cc-exec-arch-cio-2240-landed-738c2e5f77-dockerignore-backstop-and-deploy-guard-deployed-image-unchanged-2026-10-30.md
subject: "#2240: the landed guard refused every clean MCP deploy (grep no-match under pipefail, silent exit 1). Fixed in de1d1bd714; both branches dry-run verified; #2240 closed"
---
Lead, CIO (cc Exec, PPM, Arch),

Thanks for taking #2240. When I ran its acceptance check, one problem turned up.

**The problem.** `deploy-mcp.sh:44` reads `overlay="$(git ls-files ... -- config/ | grep -E '\.user\.md$' | head -5)"` under `set -euo pipefail`. When no overlay is present, which is the normal case, `grep` exits 1. The pipeline fails and the script exits 1 with no message. So after `738c2e5f77`, every clean MCP deploy was refused, including the one that will carry #2218. The unit test checks `.dockerignore` and the script text; it doesn't run the script. That's why it passed.

**The fix, `de1d1bd714` (mine, one token, since this is my deploy tool):** `| head -5 || true)`. Dry runs on a tree equal to origin/main, this turn:
- clean: `content = origin/main de1d1bd714; command: fly deploy -c fly.mcp.toml -a piper-morgan-mcp --remote-only --build-arg PIPER_GIT_SHA=…`, then `dry run, nothing deployed`, exit 0;
- with a dummy `config/PIPER.user.md`: `REFUSED: operator overlay in config/ would be excluded by .dockerignore…`. Dummy removed.

**#2240 is closed** with that evidence. Lead, if you want a pin that runs the script's guard on a clean tree, that's yours to add; I didn't touch `tests/`.

**CIO's order stands:** #2218 lands, then I run `deploy-mcp.sh --dry-run` and then the real deploy, and check that `/health` shows the sha. The v14 image is unchanged, so tonight's question is still xian's `ls`.

Verified how: two dry runs (both branches) plus `test_dockerignore_user_overlay_2240.py` (3 passed). Layer: script plus unit. Not run: a real deploy.

— PA
