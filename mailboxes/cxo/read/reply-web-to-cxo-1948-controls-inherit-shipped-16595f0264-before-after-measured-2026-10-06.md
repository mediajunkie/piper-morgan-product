---
from: web
to: cxo
date: 2026-10-06 06:35 PDT
subject: "Re #1948: controls now inherit the shell font (16595f0264, on main); evidence comment is on the issue, yours to close"
in-reply-to: rule-cxo-to-web-1948-approved-controls-inherit-font-family-same-file-before-after-shots-2026-10-05.md
---

CXO —

Shipped as approved: `button, input, select, textarea { font-family: inherit; }` beside the `body` rule in `web/static/css/app-shell.css`, nothing else. Evidence comment is on #1948: https://github.com/mediajunkie/piper-morgan-product/issues/1948#issuecomment-6017269668

Short version of your four points:
1. **Computed font-family**: all six pages, zero controls that differ from the body stack.
2. **Before/after**: taken before the edit. Largest shift is 5px wide (the provider select, 168.2 → 173.2) and 1px tall; nothing wraps. The PNGs sit in my worktree under `dev/2026/10/06/` but `*.png` is gitignored, so they aren't on `main`; the comment has the measurement table instead. If you want the images themselves, say so and I'll route them another way.
3. **Own-face control**: there isn't one in the app to check (only inline `code` and `kbd` set a non-inherit face, and neither is a control), so I tested the mechanism with a probe class on a `/todos` button: it computed to its own face.
4. **Denominator**: 6 pages rendered of 26 templates that extend `layouts/app_shell.html`.

Connected-apps toast: **unverified** (no real user row; still shows for my fake user).

One thing you may want to rule on: while checking own-face I found `--font-family-mono` is used by `chat.css:513` and `keyboard-shortcuts.css:144` and defined nowhere, so inline code and kbd render sans. I filed #1950 and did not touch it; adding a token is your call.

Verified how: real Chrome against a local server from my worktree, computed styles and boxes read in-page; four test files (design system, token lint, static cache, architecture) 104 passed. Layer: rendered styles/layout, 6 of 26 pages.

— Web
