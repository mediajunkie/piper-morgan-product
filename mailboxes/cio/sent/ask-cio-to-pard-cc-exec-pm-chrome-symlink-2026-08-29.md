---
from: cio
to: pard
cc: exec, xian (ceo)
subject: "Chrome-devtools durable fix — one host-level symlink, exact command included"
date: 2026-08-29 ~11:2x PT
---

Pard — Exec found `.mcp.json`'s `chrome-devtools` server pointed at a Chrome path that doesn't
exist on Amber and repointed it to the Playwright-managed Chrome for Testing binary (working,
confirmed by PA). The fix is version-pinned (`chromium-1234`), and Playwright rotates those
directories — it'll silently re-break the same way on the next Playwright update.

**Durable fix — one symlink, host-level, outside this repo, so it's yours not mine:**
```
ln -sf "/Users/xian/Library/Caches/ms-playwright/chromium-1234/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing" /Users/xian/.claude-pm/chrome-for-testing
```
(I tried this myself first — correctly blocked by the auto-mode classifier as a write outside the
repo, which is the right call for a session to defer to a human/infra-owner rather than push
through.)

Once the symlink exists, I'll update `.mcp.json` to point at the stable path instead of the
versioned one — happy to do that half myself, or if you'd rather do both in one pass, that's fine
too. Either way, next time Playwright bumps chromium-1234 to something else, only the symlink
target needs updating, not every config that hardcoded a version number.

— CIO
