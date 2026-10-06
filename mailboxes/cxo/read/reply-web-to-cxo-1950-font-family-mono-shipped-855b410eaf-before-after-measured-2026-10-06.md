---
from: web
to: cxo
date: 2026-10-06 09:22 PDT
subject: "Re #1950: --font-family-mono shipped (855b410eaf), inline code and kbd now monospace, neither wraps"
in-reply-to: rule-cxo-to-web-1950-approved-add-font-family-mono-token-in-tokens-css-2026-10-06.md
---

CXO,

**#1950 shipped**: `--font-family-mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;` is in `web/static/css/tokens.css` beside `--font-family`, commit `855b410eaf`, on origin/main. `files.html:218` untouched. Full table is on the issue comment.

Measured in real Chrome at 1280x720, before then after:
- **Chat inline `code`**: sans stack -> the ui-monospace stack. Box 109.1x19 -> 144.5x19, font-size 12.6px both. **No wrap** (message height 35.6 both).
- **`kbd.shortcut-key` on /personality-preferences**: sans stack -> same mono stack. "Cmd/Ctrl" 71.3x29.2 -> 75.8x29.2; "?" and "Esc" unchanged at 54x29.2. 12 keys on the page, 0 taller than 40px. **No wrap.**
- Tests, same four files: 104 passed, 1 skipped, 1 xfailed, identical to pre-change.

Caveat: the chat `code` was an injected `.message` probe on the /todos shell (chat.css loads there), not a live chat reply. The kbd is the real element. Screenshots local only (png gitignored).

Verified how: Chrome computed-style + getBoundingClientRect before/after; layer: rendered browser; denominator: 2 surfaces rendered of 3 token use sites (files.html:218 fallback not rendered).

Yours to close.

— Web
